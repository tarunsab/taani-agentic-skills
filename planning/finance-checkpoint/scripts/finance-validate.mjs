#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { validateFinanceDocument } from "./lib/finance-core.mjs";
import { fail, loadJson, parseArgs, printJson, requireArg, skillRoot } from "./lib/cli.mjs";

try {
  const args = parseArgs(process.argv.slice(2), ["snapshot", "mode", "freshness"]);
  const snapshotPath = requireArg(args, "snapshot");
  const root = skillRoot(import.meta.url);
  const freshnessPath = args.freshness ?? path.join(root, "config/freshness.json");
  const result = validateFinanceDocument(fs.readFileSync(snapshotPath, "utf8"), {
    mode: args.mode ?? "draft",
    freshness: loadJson(freshnessPath),
  });
  const output = {
    valid: result.valid,
    blocking: result.blocking,
    warnings: result.warnings,
    metadata: result.parsed.frontmatter,
  };
  printJson(output);
  if (!result.valid) process.exitCode = 2;
} catch (error) {
  fail(error);
}
