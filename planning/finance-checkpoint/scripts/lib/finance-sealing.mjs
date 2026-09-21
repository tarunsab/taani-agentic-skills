import { spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { parseDocumentFrontmatter, parseFinanceDocument, validateFinanceDocument } from "./finance-core.mjs";

const LEGACY_CHECKPOINT_FILES = ["Financial Snapshot.md", "Financial Review.md", "Financial Goals.md"];
const CHECKPOINT_FILES = [...LEGACY_CHECKPOINT_FILES, "Financial Assessment.md"];
const OPTIONAL_CHECKPOINT_FILES = ["Financial Scenarios.md"];
const ALLOWED_CHECKPOINT_FILES = new Set([...CHECKPOINT_FILES, ...OPTIONAL_CHECKPOINT_FILES]);

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function git(financeRoot, args, { allowFailure = false } = {}) {
  const result = spawnSync("git", args, {
    cwd: financeRoot,
    encoding: "utf8",
    env: { ...process.env, GIT_CONFIG_GLOBAL: "/dev/null" },
  });
  if (!allowFailure && result.status !== 0) {
    throw new Error(`Git command failed: git ${args.join(" ")}\n${result.stderr.trim()}`);
  }
  return result;
}

function ensureLocalRepository(financeRoot) {
  if (!fs.existsSync(path.join(financeRoot, ".git"))) {
    const initialized = git(financeRoot, ["init", "-b", "main"], { allowFailure: true });
    if (initialized.status !== 0) git(financeRoot, ["init"]);
  }
  const remotes = git(financeRoot, ["remote"]).stdout.trim();
  if (remotes) throw new Error(`Finance repository has configured remote(s): ${remotes}. Remove them before sealing.`);
  const staged = git(financeRoot, ["diff", "--cached", "--name-only"]).stdout.trim();
  if (staged) throw new Error(`Finance repository has staged changes unrelated to this seal: ${staged}`);
}

function validateApprovedRecord(markdown, { expectedType, asOf = null, requiredApprovers = [] }) {
  const metadata = parseDocumentFrontmatter(markdown);
  if (metadata.type !== expectedType) throw new Error(`${expectedType} record has incorrect type metadata`);
  if (metadata.schema_version !== 1) throw new Error(`${expectedType} record must use schema_version 1`);
  if (asOf && metadata.as_of !== asOf) throw new Error(`${expectedType} as_of must be ${asOf}`);
  if (metadata.status !== "approved") throw new Error(`${expectedType} must be explicitly approved before sealing`);
  if (!Array.isArray(metadata.approved_by) || metadata.approved_by.length === 0) {
    throw new Error(`${expectedType} must record approved_by`);
  }
  for (const approver of requiredApprovers) {
    if (!metadata.approved_by.includes(approver)) {
      throw new Error(`${expectedType} requires household approval from ${approver}`);
    }
  }
  return metadata;
}

function validateGoals(markdown, checkpointDate) {
  const { data } = parseFinanceDocument(markdown);
  if (data.schema_version !== 1) throw new Error(`Unsupported Goals schema_version ${data.schema_version}`);
  if (data.as_of !== checkpointDate) throw new Error(`Goals data as_of must be ${checkpointDate}`);
  if (!Array.isArray(data.goals)) throw new Error("Goals data must contain a goals array");
  const ids = new Set();
  const required = ["id", "goal", "priority", "current_position", "target", "strategy", "status"];
  for (const goal of data.goals) {
    const label = goal?.id || "unnamed";
    for (const field of required) {
      if (typeof goal?.[field] !== "string" || !goal[field].trim()) {
        throw new Error(`Goal ${label} is missing ${field}`);
      }
    }
    if (ids.has(goal.id)) throw new Error(`Goal id ${goal.id} is duplicated`);
    ids.add(goal.id);
    if (goal.target_date !== undefined && goal.target_date !== null
      && (typeof goal.target_date !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(goal.target_date))) {
      throw new Error(`Goal ${goal.id} has an invalid target_date`);
    }
  }
  return data;
}

function verifyExistingHistory(financeRoot) {
  const checkpointsRoot = path.join(financeRoot, "Checkpoints");
  if (!fs.existsSync(checkpointsRoot)) return;
  const dates = fs.readdirSync(checkpointsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(entry.name))
    .map((entry) => entry.name)
    .sort();
  for (const checkpointDate of dates) {
    const integrity = verifyCheckpointIntegrity(financeRoot, checkpointDate);
    if (!integrity.valid) {
      throw new Error(`Existing checkpoint integrity failure for ${checkpointDate}: ${integrity.errors.map(({ code, file }) => `${code}${file ? `:${file}` : ""}`).join(", ")}`);
    }
  }
}

export function verifyCheckpointIntegrity(financeRoot, checkpointDate) {
  const checkpointDirectory = path.join(financeRoot, "Checkpoints", checkpointDate);
  const manifestPath = path.join(checkpointDirectory, "manifest.json");
  const errors = [];
  if (!fs.existsSync(manifestPath)) {
    return { valid: false, checkpointDate, errors: [{ code: "manifest_missing", message: "Checkpoint manifest is missing" }] };
  }
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch (error) {
    return { valid: false, checkpointDate, errors: [{ code: "manifest_invalid", message: error.message }] };
  }
  if (manifest.checkpoint_date !== checkpointDate) {
    errors.push({ code: "date_mismatch", message: "Manifest checkpoint date does not match its directory" });
  }
  const requiredFiles = manifest.manifest_version === 1 ? LEGACY_CHECKPOINT_FILES : CHECKPOINT_FILES;
  const manifestFiles = Object.keys(manifest.files ?? {});
  const unexpectedFiles = manifestFiles.filter((filename) => !ALLOWED_CHECKPOINT_FILES.has(filename));
  for (const filename of unexpectedFiles) {
    errors.push({ code: "unexpected_file", file: filename, message: `${filename} is not a supported checkpoint record` });
  }
  const filesToVerify = [...new Set([...requiredFiles, ...manifestFiles.filter((filename) => ALLOWED_CHECKPOINT_FILES.has(filename))])];
  for (const filename of filesToVerify) {
    const expected = manifest.files?.[filename]?.sha256;
    const filePath = path.join(checkpointDirectory, filename);
    if (!expected || !fs.existsSync(filePath)) {
      errors.push({ code: "file_missing", file: filename, message: `${filename} is missing from the sealed checkpoint` });
      continue;
    }
    const actual = sha256(fs.readFileSync(filePath));
    if (actual !== expected) {
      errors.push({ code: "hash_mismatch", file: filename, expected, actual, message: `${filename} does not match its sealed hash` });
    }
  }
  return { valid: errors.length === 0, checkpointDate, manifest, errors };
}

export function sealCheckpoint({
  stagingDir,
  financeRoot,
  freshness,
  approvedBy,
  approvedAt,
}) {
  if (!Array.isArray(approvedBy) || approvedBy.length === 0) {
    throw new Error("Sealing requires an explicit approval event with at least one approver");
  }
  if (typeof approvedAt !== "string" || Number.isNaN(Date.parse(approvedAt))) {
    throw new Error("Sealing requires an explicit ISO approval timestamp");
  }
  if (!stagingDir || !financeRoot) throw new Error("stagingDir and financeRoot are required");
  fs.mkdirSync(financeRoot, { recursive: true });
  ensureLocalRepository(financeRoot);
  verifyExistingHistory(financeRoot);

  const contents = {};
  for (const filename of CHECKPOINT_FILES) {
    const filePath = path.join(stagingDir, filename);
    if (!fs.existsSync(filePath)) throw new Error(`Staging bundle is missing ${filename}`);
    contents[filename] = fs.readFileSync(filePath, "utf8");
  }
  for (const filename of OPTIONAL_CHECKPOINT_FILES) {
    const filePath = path.join(stagingDir, filename);
    if (fs.existsSync(filePath)) contents[filename] = fs.readFileSync(filePath, "utf8");
  }
  const snapshotValidation = validateFinanceDocument(contents["Financial Snapshot.md"], {
    mode: "seal",
    freshness,
  });
  if (!snapshotValidation.valid) {
    throw new Error(`Snapshot cannot be sealed: ${snapshotValidation.blocking.map(({ code }) => code).join(", ")}`);
  }
  const checkpointDate = snapshotValidation.parsed.data.as_of;
  const householdMembers = snapshotValidation.parsed.data.household_members;
  validateApprovedRecord(contents["Financial Review.md"], {
    expectedType: "financial-review",
    asOf: checkpointDate,
  });
  const goals = validateGoals(contents["Financial Goals.md"], checkpointDate);
  validateApprovedRecord(contents["Financial Goals.md"], {
    expectedType: "financial-goals",
    asOf: checkpointDate,
    requiredApprovers: goals.goals.length > 0 ? householdMembers : [],
  });
  validateApprovedRecord(contents["Financial Assessment.md"], {
    expectedType: "financial-assessment",
    asOf: checkpointDate,
  });
  if (contents["Financial Scenarios.md"]) {
    validateApprovedRecord(contents["Financial Scenarios.md"], {
      expectedType: "financial-scenarios",
      asOf: checkpointDate,
    });
  }
  const policyPath = path.join(financeRoot, "Financial Policy.md");
  if (fs.existsSync(policyPath)) {
    validateApprovedRecord(fs.readFileSync(policyPath, "utf8"), {
      expectedType: "financial-policy",
      requiredApprovers: householdMembers,
    });
  }

  const checkpointsRoot = path.join(financeRoot, "Checkpoints");
  const destination = path.join(checkpointsRoot, checkpointDate);
  if (fs.existsSync(destination)) throw new Error(`Checkpoint ${checkpointDate} is already sealed; refusing to overwrite it`);
  fs.mkdirSync(checkpointsRoot, { recursive: true });
  const temporary = path.join(checkpointsRoot, `.${checkpointDate}.sealing-${crypto.randomUUID()}`);
  fs.mkdirSync(temporary);
  let promoted = false;
  let committed = false;
  try {
    const fileHashes = {};
    for (const filename of Object.keys(contents)) {
      const buffer = Buffer.from(contents[filename]);
      fs.writeFileSync(path.join(temporary, filename), buffer);
      fileHashes[filename] = { sha256: sha256(buffer) };
    }
    const manifest = {
      manifest_version: 2,
      checkpoint_date: checkpointDate,
      schema_version: snapshotValidation.parsed.data.schema_version,
      approval_timestamp: approvedAt,
      approved_by: [...approvedBy],
      files: fileHashes,
    };
    fs.writeFileSync(path.join(temporary, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
    fs.renameSync(temporary, destination);
    promoted = true;

    const relativeCheckpoint = path.relative(financeRoot, destination);
    const pathsToCommit = [relativeCheckpoint];
    if (fs.existsSync(policyPath)) pathsToCommit.push("Financial Policy.md");
    git(financeRoot, ["add", ...pathsToCommit]);
    git(financeRoot, [
      "-c", "user.name=Finance Checkpoint",
      "-c", "user.email=finance-checkpoint@local.invalid",
      "commit", "-m", `Seal finance checkpoint ${checkpointDate}`,
    ]);
    committed = true;
    git(financeRoot, ["tag", `checkpoint-${checkpointDate}`]);
    const commit = git(financeRoot, ["rev-parse", "HEAD"]).stdout.trim();
    const integrity = verifyCheckpointIntegrity(financeRoot, checkpointDate);
    if (!integrity.valid) throw new Error(`Post-seal integrity verification failed: ${JSON.stringify(integrity.errors)}`);
    return { checkpointDate, directory: destination, commit, manifest, integrity };
  } catch (error) {
    if (fs.existsSync(temporary)) fs.rmSync(temporary, { recursive: true, force: true });
    if (promoted && !committed && fs.existsSync(destination)) {
      fs.rmSync(destination, { recursive: true, force: true });
      const head = git(financeRoot, ["rev-parse", "--verify", "HEAD"], { allowFailure: true });
      if (head.status === 0) {
        const resetPaths = [path.relative(financeRoot, destination)];
        if (fs.existsSync(policyPath)) resetPaths.push("Financial Policy.md");
        git(financeRoot, ["reset", "--quiet", "HEAD", "--", ...resetPaths], { allowFailure: true });
      } else {
        const cachedPaths = [path.relative(financeRoot, destination)];
        if (fs.existsSync(policyPath)) cachedPaths.push("Financial Policy.md");
        git(financeRoot, ["rm", "-r", "--cached", "--ignore-unmatch", "--", ...cachedPaths], { allowFailure: true });
      }
    }
    throw error;
  }
}
