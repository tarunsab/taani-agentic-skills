#!/usr/bin/env node
import path from "node:path";
import { sealCheckpoint } from "./lib/finance-sealing.mjs";
import { fail, loadJson, parseArgs, printJson, requireArg, skillRoot } from "./lib/cli.mjs";

try {
  const args = parseArgs(process.argv.slice(2), [
    "staging",
    "finance-root",
    "approved-by",
    "approved-at",
    "freshness",
  ]);
  const root = skillRoot(import.meta.url);
  const sealed = sealCheckpoint({
    stagingDir: requireArg(args, "staging"),
    financeRoot: requireArg(args, "finance-root"),
    approvedBy: requireArg(args, "approved-by").split(",").map((name) => name.trim()).filter(Boolean),
    approvedAt: requireArg(args, "approved-at"),
    freshness: loadJson(args.freshness ?? path.join(root, "config/freshness.json")),
  });
  printJson({
    sealed: true,
    checkpoint_date: sealed.checkpointDate,
    commit: sealed.commit,
    integrity: sealed.integrity,
  });
} catch (error) {
  fail(error);
}
