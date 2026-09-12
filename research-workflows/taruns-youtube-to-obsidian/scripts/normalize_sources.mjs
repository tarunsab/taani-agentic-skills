import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function normalizeYouTubeUrl(value) {
  const url = String(value ?? "").trim().replace(/^['"]|['"]$/g, "");
  const watch = url.match(/[?&]v=([A-Za-z0-9_-]{11})/);
  if (watch) return watch[1];
  const short = url.match(/youtu\.be\/([A-Za-z0-9_-]{11})/);
  if (short) return short[1];
  const shorts = url.match(/\/shorts\/([A-Za-z0-9_-]{11})/);
  return shorts?.[1] ?? null;
}

export function indexSources(youtubeFolder) {
  const byId = {};
  for (const file of fs.readdirSync(youtubeFolder).filter(name => name.endsWith(".md"))) {
    const fullPath = path.join(youtubeFolder, file);
    const text = fs.readFileSync(fullPath, "utf8");
    const sourceLine = text.split("\n").find(line => line.startsWith("source:"));
    if (!sourceLine) continue;
    const id = normalizeYouTubeUrl(sourceLine.slice("source:".length).trim());
    if (!id) continue;
    (byId[id] ??= []).push(file);
  }
  return byId;
}

function main() {
  const folder = process.argv[2];
  if (!folder) throw new Error("Usage: node normalize_sources.mjs <youtube-folder>");
  process.stdout.write(`${JSON.stringify(indexSources(folder), null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) main();
