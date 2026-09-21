#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { generateDashboard } from "./lib/finance-dashboard.mjs";
import { fail, loadJson, parseArgs, printJson, requireArg, skillRoot } from "./lib/cli.mjs";

function git(financeRoot, args) {
  const result = spawnSync("git", args, { cwd: financeRoot, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`Git command failed: ${result.stderr.trim()}`);
  return result;
}

try {
  const args = parseArgs(process.argv.slice(2), ["finance-root", "today", "freshness"]);
  const financeRoot = requireArg(args, "finance-root");
  const root = skillRoot(import.meta.url);
  const today = args.today ?? new Date().toISOString().slice(0, 10);
  const generated = generateDashboard({
    financeRoot,
    today,
    freshness: loadJson(args.freshness ?? path.join(root, "config/freshness.json")),
  });
  const dashboardPath = path.join(financeRoot, "Financial Dashboard.md");
  if (!args["no-write"]) fs.writeFileSync(dashboardPath, generated.markdown);
  let commit = null;
  if (args.commit) {
    if (!fs.existsSync(path.join(financeRoot, ".git"))) throw new Error("Finance repository is not initialized");
    if (git(financeRoot, ["remote"]).stdout.trim()) throw new Error("Refusing to commit a dashboard while a Finance remote is configured");
    git(financeRoot, ["add", "Financial Dashboard.md"]);
    const diff = spawnSync("git", ["diff", "--cached", "--quiet", "--", "Financial Dashboard.md"], { cwd: financeRoot });
    if (diff.status === 1) {
      git(financeRoot, [
        "-c", "user.name=Finance Checkpoint",
        "-c", "user.email=finance-checkpoint@local.invalid",
        "commit", "--only", "-m", `Update finance dashboard ${today}`, "--", "Financial Dashboard.md",
      ]);
      commit = git(financeRoot, ["rev-parse", "HEAD"]).stdout.trim();
    }
  }
  printJson({
    generated: true,
    dashboard_path: dashboardPath,
    latest_checkpoint: generated.latestCheckpoint,
    age: generated.age ?? null,
    commit,
  });
} catch (error) {
  fail(error);
}
