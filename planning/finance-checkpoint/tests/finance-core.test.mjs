import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  calculateMetrics,
  parseFinanceDocument,
  validateFinanceDocument,
  validateSnapshot,
} from "../scripts/lib/finance-core.mjs";
import { knownSnapshot, renderSnapshotMarkdown } from "./helpers.mjs";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const freshness = JSON.parse(fs.readFileSync(path.join(skillRoot, "config/freshness.json"), "utf8"));

test("parser returns frontmatter and the single embedded versioned data object", () => {
  const parsed = parseFinanceDocument(renderSnapshotMarkdown());
  assert.equal(parsed.frontmatter.type, "financial-snapshot");
  assert.equal(parsed.frontmatter.schema_version, 1);
  assert.deepEqual(parsed.frontmatter.approved_by, []);
  assert.equal(parsed.data.assets[0].id, "joint-cash");
});

test("parser rejects ambiguous duplicate data blocks", () => {
  const markdown = `${renderSnapshotMarkdown()}\n\`\`\`finance-data\n{}\n\`\`\``;
  assert.throws(() => parseFinanceDocument(markdown), /exactly one finance-data block/i);
});

test("seal validation rejects unsupported schemas and metadata disagreement", () => {
  const badSchema = knownSnapshot({ schema_version: 2 });
  assert.throws(
    () => validateFinanceDocument(renderSnapshotMarkdown(badSchema), { mode: "seal", freshness }),
    /unsupported schema_version 2/i,
  );

  const mismatched = renderSnapshotMarkdown(knownSnapshot(), { as_of: "2027-03-02" });
  const result = validateFinanceDocument(mismatched, { mode: "seal", freshness });
  assert.equal(result.blocking[0].code, "metadata_mismatch");
});

test("unknown and explicitly stale required records prevent sealing", () => {
  const snapshot = knownSnapshot({
    assets: [
      {
        id: "cash-unknown",
        label: "Cash awaiting confirmation",
        category: "cash",
        value: null,
        value_date: null,
        quality: "unknown",
        source: "Not yet supplied",
      },
      {
        id: "investment-stale",
        label: "Investment awaiting refresh",
        category: "investment",
        value: 1000,
        value_date: "2026-12-01",
        quality: "stale",
        source: "Previous checkpoint",
      },
    ],
    liabilities: [],
  });
  const result = validateSnapshot(snapshot, { mode: "seal", freshness });
  assert.deepEqual(result.blocking.map(({ code }) => code), ["unknown_value", "stale_value"]);
});

test("mechanical freshness blocks old checkpoint-current balances", () => {
  const snapshot = knownSnapshot();
  snapshot.assets[0] = { ...snapshot.assets[0], value_date: "2027-02-01" };
  const result = validateSnapshot(snapshot, { mode: "seal", freshness });
  assert.equal(result.blocking[0].code, "freshness_exceeded");
  assert.match(result.blocking[0].message, /joint-cash/);
});

test("material estimates require a method, valuation date, and enclosing range", () => {
  const snapshot = knownSnapshot();
  snapshot.assets[3] = {
    ...snapshot.assets[3],
    method: "",
    valuation_method: "",
    valuation_date: null,
    range_low: 340000,
    range_high: 350000,
  };
  const result = validateSnapshot(snapshot, { mode: "seal", freshness });
  assert.deepEqual(
    result.blocking.filter(({ item_id }) => item_id === "home").map(({ code }) => code),
    ["estimate_method_missing", "valuation_date_missing", "valuation_method_missing", "estimate_range_invalid"],
  );
});

test("schema validation rejects calculated input quality, invalid categories, and broken secured-asset links", () => {
  const snapshot = knownSnapshot();
  snapshot.assets[0] = { ...snapshot.assets[0], quality: "calculated" };
  snapshot.assets[1] = { ...snapshot.assets[1], category: "crypto-magic" };
  snapshot.liabilities[1] = { ...snapshot.liabilities[1], secured_asset_id: "missing-car" };
  const result = validateSnapshot(snapshot, { mode: "seal", freshness });
  assert.deepEqual(
    result.blocking.map(({ code }) => code),
    ["invalid_quality", "invalid_category", "secured_asset_missing"],
  );
});

test("recorded overrides are visible and do not conceal unsafe data", () => {
  const snapshot = knownSnapshot({
    assets: [
      {
        id: "cash-unknown",
        label: "Cash awaiting confirmation",
        category: "cash",
        value: null,
        value_date: null,
        quality: "unknown",
        source: "Not yet supplied",
      },
    ],
    liabilities: [],
    overrides: [
      {
        id: "override-cash",
        item_id: "cash-unknown",
        reason: "User asked to retain the draft while locating a statement",
        approved_by: ["Alex"],
        approved_at: "2027-03-01T10:00:00Z",
      },
    ],
  });
  const result = validateSnapshot(snapshot, { mode: "seal", freshness });
  assert.ok(result.blocking.some(({ code }) => code === "unknown_value"));
  assert.ok(result.warnings.some(({ code }) => code === "override_recorded"));
});

test("calculation rejects unvalidated unknown inputs", () => {
  const snapshot = knownSnapshot();
  snapshot.liabilities[0] = { ...snapshot.liabilities[0], balance: null, quality: "unknown", value_date: null };
  assert.throws(() => calculateMetrics(snapshot), /validated snapshot/i);
});

test("known snapshot produces exact hand-checked canonical metrics", () => {
  const metrics = calculateMetrics(knownSnapshot(), { freshness });
  assert.deepEqual(metrics, {
    total_assets: 570000,
    total_liabilities: 321000,
    net_worth: 249000,
    net_worth_excluding_pensions: 129000,
    liquid_assets: 100000,
    home_equity: 30000,
    vehicle_equity: 5000,
    monthly_debt_service: 2400,
    monthly_fixed_costs: 2000,
    monthly_surplus: 2750,
    mortgage_ltv: 90.91,
    high_interest_debt: 6000,
    pension_total: 120000,
  });
});

test("validation and calculation CLIs expose machine-readable results", () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "finance-core-cli-"));
  const snapshotPath = path.join(directory, "Financial Snapshot.md");
  fs.writeFileSync(snapshotPath, renderSnapshotMarkdown(knownSnapshot(), {
    status: "approved",
    approved_by: ["Alex"],
  }));
  const validateResult = spawnSync(process.execPath, [
    path.join(skillRoot, "scripts/finance-validate.mjs"),
    "--snapshot", snapshotPath,
    "--mode", "seal",
  ], { encoding: "utf8" });
  assert.equal(validateResult.status, 0, validateResult.stderr);
  assert.equal(JSON.parse(validateResult.stdout).valid, true);

  const calculateResult = spawnSync(process.execPath, [
    path.join(skillRoot, "scripts/finance-calculate.mjs"),
    "--snapshot", snapshotPath,
  ], { encoding: "utf8" });
  assert.equal(calculateResult.status, 0, calculateResult.stderr);
  assert.equal(JSON.parse(calculateResult.stdout).metrics.net_worth, 249000);
});

test("validation CLI returns a non-zero status for a blocking unknown", () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "finance-validate-cli-"));
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
  const snapshotPath = path.join(directory, "Financial Snapshot.md");
  fs.writeFileSync(snapshotPath, renderSnapshotMarkdown(snapshot, {
    status: "approved",
    approved_by: ["Alex"],
  }));
  const result = spawnSync(process.execPath, [
    path.join(skillRoot, "scripts/finance-validate.mjs"),
    "--snapshot", snapshotPath,
    "--mode", "seal",
  ], { encoding: "utf8" });
  assert.equal(result.status, 2);
  assert.ok(JSON.parse(result.stdout).blocking.some(({ code }) => code === "unknown_value"));
});
