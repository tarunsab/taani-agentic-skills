import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { sealCheckpoint, verifyCheckpointIntegrity } from "../scripts/lib/finance-sealing.mjs";
import {
  knownSnapshot,
  renderAssessmentMarkdown,
  renderGoalsMarkdown,
  renderPolicyMarkdown,
  renderReviewMarkdown,
  renderScenariosMarkdown,
  renderSnapshotMarkdown,
} from "./helpers.mjs";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const freshness = JSON.parse(fs.readFileSync(path.join(skillRoot, "config/freshness.json"), "utf8"));

function git(cwd, args) {
  return spawnSync("git", args, { cwd, encoding: "utf8" });
}

function setupFixture({ snapshot = knownSnapshot(), snapshotApprovers = ["Alex"], sharedApprovers = ["Alex", "Sam"] } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "finance-sealing-"));
  const stagingDir = path.join(root, "staging");
  const financeRoot = path.join(root, "Finance");
  fs.mkdirSync(stagingDir, { recursive: true });
  fs.mkdirSync(financeRoot, { recursive: true });
  fs.writeFileSync(path.join(financeRoot, "Financial Policy.md"), renderPolicyMarkdown({ approvedBy: sharedApprovers }));
  fs.writeFileSync(path.join(stagingDir, "Financial Snapshot.md"), renderSnapshotMarkdown(snapshot, {
    status: "approved",
    approved_by: snapshotApprovers,
  }));
  fs.writeFileSync(path.join(stagingDir, "Financial Review.md"), renderReviewMarkdown({ approvedBy: sharedApprovers }));
  fs.writeFileSync(path.join(stagingDir, "Financial Goals.md"), renderGoalsMarkdown({ approvedBy: sharedApprovers }));
  fs.writeFileSync(path.join(stagingDir, "Financial Assessment.md"), renderAssessmentMarkdown());
  return { root, stagingDir, financeRoot };
}

function approvedOptions(fixture) {
  return {
    ...fixture,
    freshness,
    approvedBy: ["Alex", "Sam"],
    approvedAt: "2027-03-01T10:00:00Z",
  };
}

test("sealing requires an explicit approval event", () => {
  const fixture = setupFixture();
  assert.throws(
    () => sealCheckpoint({ ...approvedOptions(fixture), approvedBy: [] }),
    /explicit approval/i,
  );
  assert.equal(fs.existsSync(path.join(fixture.financeRoot, "Checkpoints/2027-03-01")), false);
});

test("sealing requires the stage-three Financial Assessment", () => {
  const fixture = setupFixture();
  fs.rmSync(path.join(fixture.stagingDir, "Financial Assessment.md"));
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /missing Financial Assessment\.md/i);
});

test("sealing does not require a Financial Policy when no policy change is part of the checkpoint", () => {
  const fixture = setupFixture();
  fs.rmSync(path.join(fixture.financeRoot, "Financial Policy.md"));
  const sealed = sealCheckpoint(approvedOptions(fixture));
  assert.equal(sealed.integrity.valid, true);
});

test("a maintainer can seal when the Goals record already carries the required joint approval", () => {
  const fixture = setupFixture();
  const sealed = sealCheckpoint({ ...approvedOptions(fixture), approvedBy: ["Alex"] });
  assert.deepEqual(sealed.manifest.approved_by, ["Alex"]);
});

test("sealing refuses unknown data and leaves no partial checkpoint", () => {
  const snapshot = knownSnapshot({
    assets: [{
      id: "cash-unknown",
      label: "Cash",
      category: "cash",
      value: null,
      value_date: null,
      quality: "unknown",
      source: "Not supplied",
    }],
  });
  const fixture = setupFixture({ snapshot });
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /unknown_value/i);
  assert.equal(fs.existsSync(path.join(fixture.financeRoot, "Checkpoints/2027-03-01")), false);
});

test("sealing rejects an incomplete goal record", () => {
  const fixture = setupFixture();
  fs.writeFileSync(path.join(fixture.stagingDir, "Financial Goals.md"), `---
type: financial-goals
schema_version: 1
as_of: 2027-03-01
status: approved
approved_by:
  - Alex
  - Sam
---
# Financial Goals

## Goals Data

\`\`\`finance-data
{
  "schema_version": 1,
  "as_of": "2027-03-01",
  "goals": [{"id":"incomplete","goal":"Incomplete goal"}]
}
\`\`\`
`);
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /goal incomplete is missing priority/i);
});

test("sealed checkpoint hashes verify and tampering fails loudly", () => {
  const fixture = setupFixture();
  const sealed = sealCheckpoint(approvedOptions(fixture));
  assert.equal(sealed.checkpointDate, "2027-03-01");
  assert.equal(verifyCheckpointIntegrity(fixture.financeRoot, "2027-03-01").valid, true);

  const snapshotPath = path.join(sealed.directory, "Financial Snapshot.md");
  fs.appendFileSync(snapshotPath, "\nUnexpected historical edit.\n");
  const tampered = verifyCheckpointIntegrity(fixture.financeRoot, "2027-03-01");
  assert.equal(tampered.valid, false);
  assert.equal(tampered.errors[0].code, "hash_mismatch");
});

test("optional stage-four scenarios are sealed and integrity checked with the same checkpoint", () => {
  const fixture = setupFixture();
  fs.writeFileSync(path.join(fixture.stagingDir, "Financial Scenarios.md"), renderScenariosMarkdown());
  const sealed = sealCheckpoint(approvedOptions(fixture));
  assert.equal(sealed.manifest.manifest_version, 2);
  assert.ok(sealed.manifest.files["Financial Assessment.md"]?.sha256);
  assert.ok(sealed.manifest.files["Financial Scenarios.md"]?.sha256);
  assert.equal(verifyCheckpointIntegrity(fixture.financeRoot, "2027-03-01").valid, true);

  fs.appendFileSync(path.join(sealed.directory, "Financial Scenarios.md"), "\nUnexpected scenario edit.\n");
  const tampered = verifyCheckpointIntegrity(fixture.financeRoot, "2027-03-01");
  assert.equal(tampered.valid, false);
  assert.equal(tampered.errors[0].file, "Financial Scenarios.md");
});

test("sealing creates local Git history with no remote and a recoverable original", () => {
  const fixture = setupFixture();
  const sealed = sealCheckpoint(approvedOptions(fixture));
  assert.equal(git(fixture.financeRoot, ["remote"]).stdout.trim(), "");
  assert.match(git(fixture.financeRoot, ["log", "-1", "--format=%s"]).stdout, /Seal finance checkpoint 2027-03-01/);
  assert.equal(git(fixture.financeRoot, ["tag", "--list", "checkpoint-2027-03-01"]).stdout.trim(), "checkpoint-2027-03-01");

  const original = fs.readFileSync(path.join(sealed.directory, "Financial Snapshot.md"), "utf8");
  fs.writeFileSync(path.join(sealed.directory, "Financial Snapshot.md"), "accidental edit");
  const recovered = git(fixture.financeRoot, ["show", "HEAD:Checkpoints/2027-03-01/Financial Snapshot.md"]);
  assert.equal(recovered.status, 0, recovered.stderr);
  assert.equal(recovered.stdout, original);
});

test("sealing never silently overwrites a sealed date", () => {
  const fixture = setupFixture();
  sealCheckpoint(approvedOptions(fixture));
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /already sealed/i);
});

test("a tampered prior checkpoint stops a later seal", () => {
  const fixture = setupFixture();
  const first = sealCheckpoint(approvedOptions(fixture));
  fs.appendFileSync(path.join(first.directory, "Financial Snapshot.md"), "\ntampered\n");

  const secondStaging = path.join(fixture.root, "staging-2027-06-01");
  fs.mkdirSync(secondStaging);
  const secondSnapshot = knownSnapshot({ as_of: "2027-06-01" });
  for (const collection of ["income", "assets", "liabilities", "recurring_flows"]) {
    secondSnapshot[collection] = secondSnapshot[collection].map((record) => ({
      ...record,
      value_date: "2027-06-01",
      ...(record.quality === "estimated" ? { valuation_date: "2027-06-01" } : {}),
    }));
  }
  fs.writeFileSync(path.join(secondStaging, "Financial Snapshot.md"), renderSnapshotMarkdown(secondSnapshot, {
    status: "approved",
    approved_by: ["Alex"],
  }));
  fs.writeFileSync(path.join(secondStaging, "Financial Review.md"), renderReviewMarkdown({ asOf: "2027-06-01" }));
  fs.writeFileSync(path.join(secondStaging, "Financial Goals.md"), renderGoalsMarkdown({ asOf: "2027-06-01" }));
  fs.writeFileSync(path.join(secondStaging, "Financial Assessment.md"), renderAssessmentMarkdown({ asOf: "2027-06-01" }));

  assert.throws(
    () => sealCheckpoint({ ...approvedOptions(fixture), stagingDir: secondStaging, approvedAt: "2027-06-01T10:00:00Z" }),
    /existing checkpoint integrity failure/i,
  );
  assert.equal(fs.existsSync(path.join(fixture.financeRoot, "Checkpoints/2027-06-01")), false);
});

test("sealing refuses a Finance repository with a configured remote", () => {
  const fixture = setupFixture();
  assert.equal(git(fixture.financeRoot, ["init"]).status, 0);
  assert.equal(git(fixture.financeRoot, ["remote", "add", "origin", "https://example.invalid/private.git"]).status, 0);
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /remote/i);
});

test("sealing refuses to absorb unrelated staged Finance changes", () => {
  const fixture = setupFixture();
  assert.equal(git(fixture.financeRoot, ["init"]).status, 0);
  fs.writeFileSync(path.join(fixture.financeRoot, "Unrelated.md"), "unrelated staged content");
  assert.equal(git(fixture.financeRoot, ["add", "Unrelated.md"]).status, 0);
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /staged changes/i);
  assert.equal(fs.existsSync(path.join(fixture.financeRoot, "Checkpoints/2027-03-01")), false);
});

test("a failed Git commit rolls back the newly promoted checkpoint", () => {
  const fixture = setupFixture();
  assert.equal(git(fixture.financeRoot, ["init"]).status, 0);
  const hookPath = path.join(fixture.financeRoot, ".git/hooks/pre-commit");
  fs.writeFileSync(hookPath, "#!/bin/sh\nexit 1\n", { mode: 0o755 });
  assert.throws(() => sealCheckpoint(approvedOptions(fixture)), /Git command failed/);
  assert.equal(fs.existsSync(path.join(fixture.financeRoot, "Checkpoints/2027-03-01")), false);
});

test("seal CLI produces machine-readable output", () => {
  const fixture = setupFixture();
  const result = spawnSync(process.execPath, [
    path.join(skillRoot, "scripts/finance-seal.mjs"),
    "--staging", fixture.stagingDir,
    "--finance-root", fixture.financeRoot,
    "--approved-by", "Alex,Sam",
    "--approved-at", "2027-03-01T10:00:00Z",
  ], { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.sealed, true);
  assert.equal(output.integrity.valid, true);
});
