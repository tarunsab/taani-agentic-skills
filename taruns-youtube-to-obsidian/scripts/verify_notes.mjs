import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeYouTubeUrl } from "./normalize_sources.mjs";

const REQUIRED_SECTIONS = [
  "## Source",
  "## Executive Summary",
  "## Key Ideas",
  "## Useful Details",
  "## Actionable Takeaways",
  "## Caveats and Limitations",
  "## Related Topics"
];
const ALLOWED_PROPERTIES = new Set(["parent", "tags", "source", "date"]);
const TAXONOMY = new Set([
  "obsidian", "ai", "books", "learning", "productivity", "health",
  "house", "hardware", "photography", "games", "buy-it-for-life"
]);

function fail(failures, message) {
  failures.push(message);
}

function readFrontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const lines = match[1].split("\n");
  const keys = lines
    .filter(line => /^[A-Za-z][A-Za-z0-9_-]*:/.test(line))
    .map(line => line.split(":", 1)[0]);
  const sourceLine = lines.find(line => line.startsWith("source:"));
  const tags = [];
  let inTags = false;
  for (const line of lines) {
    if (line.startsWith("tags:")) { inTags = true; continue; }
    if (inTags && /^[A-Za-z][A-Za-z0-9_-]*:/.test(line)) inTags = false;
    if (inTags && /^\s+-\s+/.test(line)) tags.push(line.replace(/^\s+-\s+/, "").trim());
  }
  return {
    body: match[1],
    keys,
    tags,
    source: sourceLine ? sourceLine.slice("source:".length).trim().replace(/^['"]|['"]$/g, "") : null
  };
}

function sourceIndex(youtubeFolder) {
  const byId = {};
  for (const file of fs.readdirSync(youtubeFolder).filter(name => name.endsWith(".md"))) {
    const fullPath = path.join(youtubeFolder, file);
    const text = fs.readFileSync(fullPath, "utf8");
    const fm = readFrontmatter(text);
    const id = normalizeYouTubeUrl(fm?.source);
    if (id) (byId[id] ??= []).push(file);
  }
  return byId;
}

function wikilinkTargets(text) {
  return [...text.matchAll(/\[\[([^|\]]+)/g)].map(match => match[1]);
}

export function verifyNotes({ vault, playlist, preExistingIds, createdFiles, failed = [], collisions = [] }) {
  const failures = [];
  const youtubeFolder = path.join(vault, "06 - Resources/YouTube");
  const playlistIds = playlist.videos.map(video => video.id);
  const preExisting = new Set(preExistingIds ?? []);
  const failedIds = new Set(failed.map(item => item.id));
  const finalById = sourceIndex(youtubeFolder);
  const createdIds = new Set();

  if (!Array.isArray(preExistingIds)) fail(failures, "preExistingIds was not provided");
  for (const file of createdFiles ?? []) {
    const fullPath = path.join(youtubeFolder, file);
    if (!fs.existsSync(fullPath)) {
      fail(failures, `Created note is missing: ${file}`);
      continue;
    }
    const text = fs.readFileSync(fullPath, "utf8");
    const fm = readFrontmatter(text);
    const id = normalizeYouTubeUrl(fm?.source);
    if (!id) {
      fail(failures, `Created note has no valid source: ${file}`);
      continue;
    }
    if (createdIds.has(id)) fail(failures, `Duplicate created source ID: ${id}`);
    createdIds.add(id);

    const expected = playlist.videos.find(video => video.id === id);
    if (!expected) fail(failures, `Created note source is not in playlist: ${file}`);
    if (!fm) {
      fail(failures, `Missing frontmatter: ${file}`);
      continue;
    }
    const unexpectedKeys = fm.keys.filter(key => !ALLOWED_PROPERTIES.has(key));
    if (unexpectedKeys.length) fail(failures, `${file} has forbidden properties: ${unexpectedKeys.join(", ")}`);
    if (fm.keys.length !== ALLOWED_PROPERTIES.size || ![...ALLOWED_PROPERTIES].every(key => fm.keys.includes(key))) {
      fail(failures, `${file} does not have exactly parent/tags/source/date frontmatter`);
    }
    if (fm.tags.length < 1 || fm.tags.length > 2 || fm.tags.some(tag => !TAXONOMY.has(tag))) {
      fail(failures, `${file} has invalid taxonomy tags`);
    }
    if (!text.includes('parent: "[[06 - Resources/YouTube/00 - YouTube Index|YouTube Index]]"')) {
      fail(failures, `${file} has an invalid parent link`);
    }
    for (const section of REQUIRED_SECTIONS) {
      if (!text.includes(section)) fail(failures, `${file} is missing ${section}`);
    }
    for (const target of wikilinkTargets(text)) {
      if (!target.startsWith("06 - Resources/")) continue;
      const targetPath = path.join(vault, target.endsWith(".md") ? target : `${target}.md`);
      if (!fs.existsSync(targetPath)) fail(failures, `${file} has a broken link: ${target}`);
    }
    const iconFile = path.join(vault, ".obsidian/plugins/obsidian-icon-folder/data.json");
    const icons = JSON.parse(fs.readFileSync(iconFile, "utf8"));
    const icon = icons[`06 - Resources/YouTube/${file}`];
    if (!icon || icon.startsWith("Li")) fail(failures, `${file} lacks a relevant ordinary-note emoji icon`);
  }

  const groups = [
    ["pre-existing", preExisting],
    ["created", createdIds],
    ["failed", failedIds]
  ];
  const seen = new Map();
  for (const [name, ids] of groups) {
    for (const id of ids) {
      if (seen.has(id)) fail(failures, `ID ${id} appears in both ${seen.get(id)} and ${name}`);
      seen.set(id, name);
    }
  }
  for (const id of playlistIds) {
    if (!seen.has(id)) fail(failures, `Playlist ID is unclassified: ${id}`);
    const files = finalById[id] ?? [];
    if (failedIds.has(id)) {
      if (files.length) fail(failures, `Failed ID unexpectedly has a source note: ${id}`);
    } else if (files.length !== 1) {
      fail(failures, `Expected exactly one source note for ${id}, found ${files.length}`);
    }
  }
  for (const id of seen.keys()) {
    if (!playlistIds.includes(id)) fail(failures, `Non-playlist ID was included in run partition: ${id}`);
  }
  if (collisions.length) fail(failures, `Unresolved filename/source collisions: ${collisions.join(", ")}`);

  const basePath = path.join(youtubeFolder, "01 - YouTube Base.base");
  const base = fs.readFileSync(basePath, "utf8");
  if (!base.includes('file.inFolder("06 - Resources/YouTube")')) fail(failures, "Base folder filter is missing");
  if (fs.existsSync(path.join(youtubeFolder, "To Obsidian Playlist.md"))) fail(failures, "Forbidden stale playlist-index file exists");

  return {
    verificationPassed: failures.length === 0,
    failures,
    counts: {
      playlist: playlistIds.length,
      skipped: preExisting.size,
      created: createdIds.size,
      transcriptFailures: failedIds.size
    },
    createdFiles: [...createdFiles]
  };
}

function main() {
  const vault = process.argv[2];
  if (!vault) throw new Error("Usage: node verify_notes.mjs <vault-root> < run-result.json");
  const payload = JSON.parse(fs.readFileSync(0, "utf8"));
  const result = verifyNotes({ vault, ...payload });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (!result.verificationPassed) process.exitCode = 1;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) main();
