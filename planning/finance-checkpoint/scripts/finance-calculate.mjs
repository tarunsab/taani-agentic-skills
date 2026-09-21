#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { calculateMetrics, validateFinanceDocument } from "./lib/finance-core.mjs";
import { fail, loadJson, parseArgs, printJson, requireArg, skillRoot } from "./lib/cli.mjs";

try {
  const args = parseArgs(process.argv.slice(2), ["snapshot", "freshness"]);
  const snapshotPath = requireArg(args, "snapshot");
  const root = skillRoot(import.meta.url);
  const freshness = loadJson(args.freshness ?? path.join(root, "config/freshness.json"));
  const validation = validateFinanceDocument(fs.readFileSync(snapshotPath, "utf8"), {
    mode: "draft",
    freshness,
  });
  if (!validation.valid) {
    printJson({ valid: false, blocking: validation.blocking, warnings: validation.warnings });
    process.exitCode = 2;
  } else {
    printJson({
      valid: true,
      as_of: validation.parsed.data.as_of,
      currency: validation.parsed.data.currency,
      metrics: calculateMetrics(validation.parsed.data, { freshness }),
      warnings: validation.warnings,
    });
  }
} catch (error) {
  fail(error);
}
