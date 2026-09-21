import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  classifyCheckpointAge,
  formatApproximateMoney,
  generateDashboard,
} from "../scripts/lib/finance-dashboard.mjs";
import { sealCheckpoint } from "../scripts/lib/finance-sealing.mjs";
import {
  knownSnapshot,
  renderAssessmentMarkdown,
  renderGoalsMarkdown,
  renderPolicyMarkdown,
  renderReviewMarkdown,
  renderSnapshotMarkdown,
} from "./helpers.mjs";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const freshness = JSON.parse(fs.readFileSync(path.join(skillRoot, "config/freshness.json"), "utf8"));

function git(cwd, args) {
  return spawnSync("git", args, { cwd, encoding: "utf8" });
}

function createRoot() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "finance-dashboard-"));
  const financeRoot = path.join(root, "Finance");
  fs.mkdirSync(financeRoot, { recursive: true });
  fs.writeFileSync(path.join(financeRoot, "Financial Policy.md"), renderPolicyMarkdown());
  return { root, financeRoot };
}

function sealAt(fixture, asOf) {
  const stagingDir = path.join(fixture.root, `staging-${asOf}`);
  fs.mkdirSync(stagingDir);
  const snapshot = knownSnapshot({ as_of: asOf });
  for (const collection of ["income", "assets", "liabilities", "recurring_flows"]) {
    snapshot[collection] = snapshot[collection].map((record) => ({
      ...record,
      value_date: asOf,
      ...(record.quality === "estimated" ? { valuation_date: asOf } : {}),
    }));
  }
  fs.writeFileSync(path.join(stagingDir, "Financial Snapshot.md"), renderSnapshotMarkdown(snapshot, {
    status: "approved",
    approved_by: ["Alex"],
  }));
  fs.writeFileSync(path.join(stagingDir, "Financial Review.md"), renderReviewMarkdown({ asOf }));
  fs.writeFileSync(path.join(stagingDir, "Financial Goals.md"), renderGoalsMarkdown({ asOf }));
  fs.writeFileSync(path.join(stagingDir, "Financial Assessment.md"), renderAssessmentMarkdown({ asOf }));
  return sealCheckpoint({
    stagingDir,
    financeRoot: fixture.financeRoot,
    freshness,
    approvedBy: ["Alex", "Sam"],
    approvedAt: `${asOf}T10:00:00Z`,
  });
}

test("checkpoint age boundaries are explicit and non-overlapping", () => {
  assert.equal(classifyCheckpointAge("2027-03-01", "2027-06-29").label, "Current");
  assert.equal(classifyCheckpointAge("2027-03-01", "2027-06-30").label, "Review due");
  assert.equal(classifyCheckpointAge("2027-03-01", "2027-08-28").label, "Stale");
  assert.equal(classifyCheckpointAge("2027-03-01", "2027-02-28").label, "Future-dated");
});

test("headline money avoids unsupported precision", () => {
  assert.equal(formatApproximateMoney(207029.89, "GBP"), "~£207k");
  assert.equal(formatApproximateMoney(1234567, "GBP"), "~£1.2m");
  assert.equal(formatApproximateMoney(-12500, "GBP"), "~-£12.5k");
});

test("dashboard has a loud safe empty state when no approved checkpoint exists", () => {
  const fixture = createRoot();
  const dashboard = generateDashboard({ financeRoot: fixture.financeRoot, today: "2027-03-01", freshness });
  assert.match(dashboard.markdown, /No approved checkpoint/i);
  assert.equal(dashboard.latestCheckpoint, null);
});

test("dashboard derives current position, goals, decisions, and history from sealed state", () => {
  const fixture = createRoot();
  sealAt(fixture, "2027-03-01");
  const dashboard = generateDashboard({ financeRoot: fixture.financeRoot, today: "2027-06-29", freshness });
  assert.equal(dashboard.latestCheckpoint, "2027-03-01");
  assert.match(dashboard.markdown, /Status: Current/);
  assert.match(dashboard.markdown, /Approximate net worth: ~£249k/);
  assert.match(dashboard.markdown, /Maintain the confirmed liquidity buffer/);
  assert.match(dashboard.markdown, /Confirm the next review date/);
  assert.match(dashboard.markdown, /\[\[02 - Taani\/Finance\/Checkpoints\/2027-03-01\/Financial Snapshot\|2027-03-01\]\]/);
  assert.doesNotMatch(dashboard.markdown, /OUT OF DATE/);
});

test("stale dashboard prominently warns against relying on conclusions", () => {
  const fixture = createRoot();
  sealAt(fixture, "2027-03-01");
  const dashboard = generateDashboard({ financeRoot: fixture.financeRoot, today: "2027-08-28", freshness });
  assert.match(dashboard.markdown, /OUT OF DATE/);
  assert.match(dashboard.markdown, /Do not rely on balances or planning conclusions/i);
});

test("adding a later checkpoint preserves and lists prior history", () => {
  const fixture = createRoot();
  const first = sealAt(fixture, "2027-03-01");
  const firstManifest = fs.readFileSync(path.join(first.directory, "manifest.json"), "utf8");
  sealAt(fixture, "2027-06-01");
  const dashboard = generateDashboard({ financeRoot: fixture.financeRoot, today: "2027-06-02", freshness });
  assert.equal(dashboard.latestCheckpoint, "2027-06-01");
  assert.match(dashboard.markdown, /2027-03-01/);
  assert.match(dashboard.markdown, /2027-06-01/);
  assert.equal(fs.readFileSync(path.join(first.directory, "manifest.json"), "utf8"), firstManifest);
});

test("unsupported historical schema fails loudly instead of disappearing", () => {
  const fixture = createRoot();
  const checkpointDirectory = path.join(fixture.financeRoot, "Checkpoints/2027-03-01");
  fs.mkdirSync(checkpointDirectory, { recursive: true });
  const snapshot = knownSnapshot({ schema_version: 2 });
  const files = {
    "Financial Snapshot.md": renderSnapshotMarkdown(snapshot, { status: "approved", approved_by: ["Alex"] }),
    "Financial Review.md": renderReviewMarkdown(),
    "Financial Goals.md": renderGoalsMarkdown(),
  };
  const hashes = {};
  for (const [filename, contents] of Object.entries(files)) {
    fs.writeFileSync(path.join(checkpointDirectory, filename), contents);
    hashes[filename] = { sha256: crypto.createHash("sha256").update(contents).digest("hex") };
  }
  fs.writeFileSync(path.join(checkpointDirectory, "manifest.json"), JSON.stringify({
    manifest_version: 1,
    checkpoint_date: "2027-03-01",
    schema_version: 2,
    approval_timestamp: "2027-03-01T10:00:00Z",
    approved_by: ["Alex", "Sam"],
    files: hashes,
  }));
  assert.throws(
    () => generateDashboard({ financeRoot: fixture.financeRoot, today: "2027-03-02", freshness }),
    /unsupported schema_version 2/i,
  );
});

test("dashboard CLI commits only the dashboard and preserves unrelated staged work", () => {
  const fixture = createRoot();
  assert.equal(git(fixture.financeRoot, ["init"]).status, 0);
  assert.equal(git(fixture.financeRoot, ["add", "Financial Policy.md"]).status, 0);
  assert.equal(git(fixture.financeRoot, [
    "-c", "user.name=Test",
    "-c", "user.email=test@local.invalid",
    "commit", "-m", "seed",
  ]).status, 0);
  fs.writeFileSync(path.join(fixture.financeRoot, "Unrelated.md"), "preserve this staged work");
  assert.equal(git(fixture.financeRoot, ["add", "Unrelated.md"]).status, 0);

  const result = spawnSync(process.execPath, [
    path.join(skillRoot, "scripts/finance-dashboard.mjs"),
    "--finance-root", fixture.financeRoot,
    "--today", "2027-03-01",
    "--commit",
  ], { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  const committedFiles = git(fixture.financeRoot, ["show", "--format=", "--name-only", "HEAD"]).stdout.trim().split(/\r?\n/);
  assert.deepEqual(committedFiles, ["Financial Dashboard.md"]);
  assert.equal(git(fixture.financeRoot, ["diff", "--cached", "--name-only"]).stdout.trim(), "Unrelated.md");
});
