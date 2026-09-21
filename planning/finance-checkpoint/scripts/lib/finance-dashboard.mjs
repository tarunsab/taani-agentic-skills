import fs from "node:fs";
import path from "node:path";
import { calculateMetrics, parseFinanceDocument, validateFinanceDocument } from "./finance-core.mjs";
import { verifyCheckpointIntegrity } from "./finance-sealing.mjs";

function daysBetween(older, newer) {
  return Math.floor((Date.parse(`${newer}T00:00:00Z`) - Date.parse(`${older}T00:00:00Z`)) / 86_400_000);
}

export function classifyCheckpointAge(asOf, today) {
  const ageDays = daysBetween(asOf, today);
  if (ageDays < 0) return { label: "Future-dated", ageDays };
  if (ageDays <= 120) return { label: "Current", ageDays };
  if (ageDays < 180) return { label: "Review due", ageDays };
  return { label: "Stale", ageDays };
}

function currencySymbol(currency) {
  return currency === "GBP" ? "£" : `${currency} `;
}

function compactNumber(value, divisor, decimals) {
  const rounded = Math.round((value / divisor) * (10 ** decimals)) / (10 ** decimals);
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(decimals).replace(/\.0+$/, "");
}

export function formatApproximateMoney(value, currency = "GBP") {
  if (value === null || value === undefined || !Number.isFinite(value)) return "Not available";
  const sign = value < 0 ? "-" : "";
  const absolute = Math.abs(value);
  const symbol = currencySymbol(currency);
  if (absolute >= 1_000_000) return `~${sign}${symbol}${compactNumber(absolute, 1_000_000, 1)}m`;
  if (absolute >= 100_000) return `~${sign}${symbol}${Math.round(absolute / 1_000)}k`;
  if (absolute >= 10_000) return `~${sign}${symbol}${compactNumber(absolute, 1_000, 1)}k`;
  if (absolute >= 1_000) return `~${sign}${symbol}${compactNumber(absolute, 1_000, 1)}k`;
  return `~${sign}${symbol}${Math.round(absolute)}`;
}

function formatExactMoney(value, currency) {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function extractSectionBullets(markdown, heading) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `## ${heading}`);
  if (start === -1) return [];
  const endOffset = lines.slice(start + 1).findIndex((line) => line.startsWith("## "));
  const section = endOffset === -1 ? lines.slice(start + 1) : lines.slice(start + 1, start + 1 + endOffset);
  return section
    .map((line) => line.match(/^\s*-\s+(.+)$/)?.[1]?.trim())
    .filter(Boolean);
}

function nextQuarterDate(asOf) {
  const [year, month, day] = asOf.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1 + 3, day));
  return date.toISOString().slice(0, 10);
}

function loadHistory(financeRoot, freshness) {
  const checkpointsRoot = path.join(financeRoot, "Checkpoints");
  if (!fs.existsSync(checkpointsRoot)) return [];
  const dates = fs.readdirSync(checkpointsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(entry.name))
    .map((entry) => entry.name)
    .sort();
  return dates.map((checkpointDate) => {
    const integrity = verifyCheckpointIntegrity(financeRoot, checkpointDate);
    if (!integrity.valid) {
      throw new Error(`Integrity error for checkpoint ${checkpointDate}: ${integrity.errors.map(({ code, file }) => `${code}${file ? `:${file}` : ""}`).join(", ")}`);
    }
    const directory = path.join(checkpointsRoot, checkpointDate);
    const snapshotMarkdown = fs.readFileSync(path.join(directory, "Financial Snapshot.md"), "utf8");
    const validation = validateFinanceDocument(snapshotMarkdown, { mode: "seal", freshness });
    if (!validation.valid) {
      throw new Error(`Checkpoint ${checkpointDate} is not a valid approved Snapshot: ${validation.blocking.map(({ code }) => code).join(", ")}`);
    }
    const reviewMarkdown = fs.readFileSync(path.join(directory, "Financial Review.md"), "utf8");
    const goalsMarkdown = fs.readFileSync(path.join(directory, "Financial Goals.md"), "utf8");
    const goals = parseFinanceDocument(goalsMarkdown).data;
    if (goals.schema_version !== 1) throw new Error(`Unsupported Goals schema_version ${goals.schema_version}`);
    if (goals.as_of !== checkpointDate) throw new Error(`Goals as_of does not match checkpoint ${checkpointDate}`);
    return {
      checkpointDate,
      snapshot: validation.parsed.data,
      metrics: calculateMetrics(validation.parsed.data, { freshness }),
      goals: goals.goals ?? [],
      openDecisions: extractSectionBullets(reviewMarkdown, "Open Decisions"),
      integrity,
    };
  });
}

function emptyDashboard(today) {
  return `---
type: financial-dashboard
schema_version: 1
status: generated
generated_on: ${today}
---
# Financial Dashboard

> [!warning] No approved checkpoint
> No approved and integrity-verified household Finance checkpoint exists yet. Do not treat the household budget note or staged drafts as current financial truth.

## Current Checkpoint

- As of: Not available
- Status: No approved checkpoint

## Current Position

Complete and approve the first checkpoint before using dashboard balances or planning conclusions.

## Current Priorities

No approved Financial Goals exist.

## Goal Progress

Not available until Financial Goals are approved.

## Open Decisions

See [[11 - Agents/Workspace/Finance/Open Questions|Finance Open Questions]].

## Checkpoint History

No sealed checkpoints.

## Data Quality

Blocking baseline information remains missing. See [[11 - Agents/Workspace/Finance/Data Quality|Finance Data Quality]].

## Next Review

Run the \`finance-checkpoint\` skill to prepare the \`${today}\` baseline. Explicit approval is required before sealing.
`;
}

function categoryValue(snapshot, category) {
  return snapshot.assets.filter((asset) => asset.category === category).reduce((sum, asset) => sum + asset.value, 0);
}

function liabilityValue(snapshot, category) {
  return snapshot.liabilities.filter((liability) => liability.category === category).reduce((sum, liability) => sum + liability.balance, 0);
}

function qualitySummary(snapshot) {
  const counts = { confirmed: 0, estimated: 0, stale: 0, unknown: 0 };
  for (const collection of [snapshot.income, snapshot.assets, snapshot.liabilities, snapshot.recurring_flows]) {
    for (const record of collection) counts[record.quality] += 1;
  }
  return counts;
}

export function generateDashboard({ financeRoot, today, freshness }) {
  const history = loadHistory(financeRoot, freshness);
  if (history.length === 0) {
    return { markdown: emptyDashboard(today), latestCheckpoint: null, history: [] };
  }
  const latest = history.at(-1);
  const { snapshot, metrics } = latest;
  const age = classifyCheckpointAge(latest.checkpointDate, today);
  const currency = snapshot.currency;
  const qualities = qualitySummary(snapshot);
  const warning = age.label === "Stale"
    ? `\n> [!danger] OUT OF DATE\n> This checkpoint is ${age.ageDays} days old. Do not rely on balances or planning conclusions until a new checkpoint is completed.\n`
    : age.label === "Review due"
      ? `\n> [!warning] Review due\n> This checkpoint is ${age.ageDays} days old. Refresh it before making a material decision.\n`
      : age.label === "Future-dated"
        ? `\n> [!danger] Future-dated checkpoint\n> The latest checkpoint date is after the dashboard date. Verify the date before relying on it.\n`
        : "";
  const priorities = latest.goals
    .slice()
    .sort((a, b) => String(a.priority).localeCompare(String(b.priority)))
    .map((goal) => `- **${goal.priority}:** ${goal.goal}`)
    .join("\n") || "No approved goals recorded.";
  const goalRows = latest.goals.map((goal) => `| ${goal.goal} | ${goal.current_position} | ${goal.target} | ${goal.target_date ?? "—"} | ${goal.status} |`).join("\n")
    || "| No approved goals | — | — | — | — |";
  const decisions = latest.openDecisions.map((decision) => `- ${decision}`).join("\n") || "No open decisions recorded.";
  const historyRows = history.map((entry) => `| [[02 - Taani/Finance/Checkpoints/${entry.checkpointDate}/Financial Snapshot|${entry.checkpointDate}]] | ${formatApproximateMoney(entry.metrics.net_worth, entry.snapshot.currency)} | Verified |`).join("\n");
  const markdown = `---
type: financial-dashboard
schema_version: 1
status: generated
generated_on: ${today}
generated_from: ${latest.checkpointDate}
---
# Financial Dashboard
${warning}
## Current Checkpoint

- As of: ${latest.checkpointDate}
- Status: ${age.label}
- Age: ${age.ageDays} days

## Current Position

- Approximate net worth: ${formatApproximateMoney(metrics.net_worth, currency)}
- Cash: ${formatApproximateMoney(categoryValue(snapshot, "cash"), currency)}
- Investments: ${formatApproximateMoney(categoryValue(snapshot, "investment"), currency)}
- Pensions: ${formatApproximateMoney(metrics.pension_total, currency)}
- Home equity: ${formatApproximateMoney(metrics.home_equity, currency)}
- Mortgage: ${formatApproximateMoney(liabilityValue(snapshot, "mortgage"), currency)}
- Other debt: ${formatApproximateMoney(metrics.total_liabilities - liabilityValue(snapshot, "mortgage"), currency)}
- Monthly surplus: ${formatApproximateMoney(metrics.monthly_surplus, currency)}

Exact reconciled net worth: ${formatExactMoney(metrics.net_worth, currency)}.

## Current Priorities

${priorities}

## Goal Progress

| Goal | Current position | Target | Target date | Status |
|---|---|---|---|---|
${goalRows}

## Open Decisions

${decisions}

## Checkpoint History

| Checkpoint | Approximate net worth | Integrity |
|---|---:|---|
${historyRows}

## Data Quality

- Confirmed items: ${qualities.confirmed}
- Estimated items: ${qualities.estimated}
- Stale items: ${qualities.stale}
- Unknown items: ${qualities.unknown}

Estimated assets retain their valuation dates, methods, and ranges in the underlying Snapshot.

## Next Review

Quarterly review target: ${nextQuarterDate(latest.checkpointDate)}. A material event may justify an earlier checkpoint.
`;
  return { markdown, latestCheckpoint: latest.checkpointDate, age, history };
}
