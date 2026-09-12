import fs from "node:fs";
import { fileURLToPath } from "node:url";

export function sanitizeFilename(title) {
  const cleaned = String(title ?? "")
    .replace(/[\\/:*?"<>|\u0000-\u001F]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/[. ]+$/g, "");
  if (!cleaned) throw new Error("Video title produces an empty filename");
  return cleaned;
}

function main() {
  const title = process.argv.slice(2).join(" ");
  process.stdout.write(`${sanitizeFilename(title)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) main();
