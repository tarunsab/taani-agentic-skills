import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(__dirname, "..");
const skillMdPath = path.join(skillDir, "SKILL.md");
const scriptPath = path.join(skillDir, "scripts", "vault-sentry.py");

test("vault-sentry SKILL.md has valid frontmatter", () => {
  const content = fs.readFileSync(skillMdPath, "utf8");
  assert.match(content, /^---\nname:\s*vault-sentry\n/);
  assert.match(content, /description:\s*.+/);
});

test("vault-checkpoint SKILL.md does not contain hardcoded private user paths", () => {
  const content = fs.readFileSync(skillMdPath, "utf8");
  assert.doesNotMatch(content, /\/Users\/[a-zA-Z0-9_-]+\//, "Should use $HOME or generic paths in skill instructions");
  assert.doesNotMatch(content, /Dhwani|Tarun Sabbineni/, "Should not contain private personal names");
});

test("vault-sentry CLI script is syntax valid and executable", () => {
  assert.ok(fs.existsSync(scriptPath), "vault-sentry.py exists");
  const output = execFileSync("python3", [scriptPath, "--help"], { encoding: "utf8" });
  assert.match(output, /usage:\s*vault-sentry\.py/i);
});

test("vault-checkpoint references exist and are populated", () => {
  const refPath = path.join(skillDir, "references", "36-dimensions.md");
  assert.ok(fs.existsSync(refPath), "36-dimensions.md exists");
  assert.ok(fs.readFileSync(refPath, "utf8").length > 200);
});
