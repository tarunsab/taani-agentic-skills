import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import path from "node:path";

import fsSync from "node:fs";

function findVaultRoot() {
  if (process.env.VAULT_ROOT && fsSync.existsSync(process.env.VAULT_ROOT)) {
    return process.env.VAULT_ROOT;
  }
  let current = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 6; i++) {
    current = path.dirname(current);
    if (fsSync.existsSync(path.join(current, ".git"))) {
      return current;
    }
  }
  return path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");
}

const vaultRoot = findVaultRoot();

function git(args) {
  return spawnSync("git", args, {
    cwd: vaultRoot,
    encoding: "utf8",
    env: { ...process.env, GIT_CONFIG_GLOBAL: "/dev/null" },
  });
}

test("parent repository ignores every sensitive Finance tree", () => {
  for (const financePath of [
    "02 - Taani/Finance/example.md",
    "04 - Areas/Finance/example.md",
    "11 - Agents/Workspace/Finance/example.md",
    "08 - Attachments/Finance/example.pdf",
  ]) {
    const result = git(["check-ignore", "-q", financePath]);
    assert.equal(
      result.status,
      0,
      `${financePath} must be excluded from the parent repository`,
    );
  }
});

test("parent repository does not already track sensitive Finance files", () => {
  const result = git([
    "ls-files",
    "02 - Taani/Finance",
    "04 - Areas/Finance",
    "11 - Agents/Workspace/Finance",
    "08 - Attachments/Finance",
  ]);
  assert.equal(result.status, 0);
  assert.equal(result.stdout.trim(), "");
});
