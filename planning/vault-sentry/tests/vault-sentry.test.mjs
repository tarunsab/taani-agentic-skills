import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
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
  assert.match(output, /--suggest\s+SUGGEST/);
  assert.match(output, /--suggest-file\s+SUGGEST_FILE/);
  assert.match(output, /--json/);
});

test("vault-sentry --suggest returns valid formatted destination recommendation", () => {
  const output = execFileSync(
    "python3",
    [scriptPath, "--suggest", "Air Fryer Sourdough Pizza Recipe"],
    { encoding: "utf8" }
  );
  assert.match(output, /VAULT SENTRY — NOTE DESTINATION RECOMMENDATION/);
  assert.match(output, /Recommended Folder:\s+02 - Taani\/Food\/Recipes\//);
  assert.match(output, /Parent Index:\s+\[\[00 - Food Index\]\]/);
  assert.match(output, /Recommended Icon:\s+🍳/);
  assert.match(output, /#food, #recipe/);
});

test("vault-sentry --suggest --json outputs valid parseable JSON with all required keys", () => {
  const jsonStr = execFileSync(
    "python3",
    [scriptPath, "--suggest", "Running my first Half Marathon in Cardiff", "--json"],
    { encoding: "utf8" }
  );
  const parsed = JSON.parse(jsonStr);
  assert.equal(parsed.query, "Running my first Half Marathon in Cardiff");
  assert.equal(parsed.recommended_folder, "03 - Projects/");
  assert.equal(parsed.parent_index, "[[00 - Projects Index]]");
  assert.equal(parsed.recommended_icon, "🏃");
  assert.ok(parsed.rationale.length > 10);
  assert.ok(parsed.frontmatter_scaffold.includes("parent: \"[[00 - Projects Index]]\""));
});

test("vault-sentry --suggest-file parses draft file heading and infers destination", () => {
  const tmpFile = path.join(os.tmpdir(), `test-draft-${Date.now()}.md`);
  fs.writeFileSync(
    tmpFile,
    "# Replacing Bathroom Spotlights with Dimmer LEDs\n\nNeed 4 GU10 LED spotlights.\n",
    "utf8"
  );
  try {
    const jsonStr = execFileSync(
      "python3",
      [scriptPath, "--suggest-file", tmpFile, "--json"],
      { encoding: "utf8" }
    );
    const parsed = JSON.parse(jsonStr);
    assert.equal(parsed.query, "Replacing Bathroom Spotlights with Dimmer LEDs");
    assert.equal(parsed.recommended_folder, "02 - Taani/House/Renovation/");
    assert.equal(parsed.parent_index, "[[00 - House Index]]");
    assert.equal(parsed.recommended_icon, "🪵");
  } finally {
    if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
  }
});

test("vault-checkpoint references exist and are populated", () => {
  const refPath = path.join(skillDir, "references", "36-dimensions.md");
  assert.ok(fs.existsSync(refPath), "36-dimensions.md exists");
  assert.ok(fs.readFileSync(refPath, "utf8").length > 200);
});
