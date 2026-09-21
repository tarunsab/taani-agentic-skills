import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(__dirname, "..");
const skillMdPath = path.join(skillDir, "SKILL.md");

test("habits-checkpoint SKILL.md has valid frontmatter", () => {
  const content = fs.readFileSync(skillMdPath, "utf8");
  assert.match(content, /^---\nname:\s*habits-checkpoint\n/);
  assert.match(content, /description:\s*.+/);
});

test("habits-checkpoint SKILL.md does not contain hardcoded private user paths", () => {
  const content = fs.readFileSync(skillMdPath, "utf8");
  assert.doesNotMatch(content, /\/Users\/[a-zA-Z0-9_-]+\//, "Should use $HOME instead of hardcoded paths");
  assert.doesNotMatch(content, /Dhwani|Tarun Sabbineni/, "Should not contain private personal names");
});

test("habits-checkpoint references exist and are populated", () => {
  const lifecyclePath = path.join(skillDir, "references", "lifecycle.md");
  const templatesPath = path.join(skillDir, "references", "templates.md");
  assert.ok(fs.existsSync(lifecyclePath), "lifecycle.md exists");
  assert.ok(fs.existsSync(templatesPath), "templates.md exists");
  assert.ok(fs.readFileSync(lifecyclePath, "utf8").length > 100);
  assert.ok(fs.readFileSync(templatesPath, "utf8").length > 100);
});
