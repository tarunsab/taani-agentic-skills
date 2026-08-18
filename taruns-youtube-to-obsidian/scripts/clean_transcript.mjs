import fs from "node:fs";
import { fileURLToPath } from "node:url";

function sameWords(words, left, right, length) {
  for (let i = 0; i < length; i += 1) {
    if (words[left + i] !== words[right + i]) return false;
  }
  return true;
}

export function collapseRepeatedCaptionSpans(text) {
  const words = text.split(/\s+/).filter(Boolean);
  const output = [];
  let index = 0;
  while (index < words.length) {
    let collapsed = false;
    for (let length = Math.min(80, Math.floor((words.length - index) / 2)); length >= 3; length -= 1) {
      if (!sameWords(words, index, index + length, length)) continue;
      output.push(...words.slice(index, index + length));
      index += length * 2;
      while (index + length <= words.length && sameWords(words, index, index - length, length)) {
        index += length;
      }
      collapsed = true;
      break;
    }
    if (!collapsed) output.push(words[index++]);
  }
  return output.join(" ");
}

export function cleanTranscript(raw) {
  const text = String(raw ?? "");
  if (!text.includes("## Transcript")) {
    throw new Error("Transcript response is missing the expected transcript marker");
  }
  const body = text.split("## Transcript", 2)[1].split("\n---", 1)[0];
  const paragraphs = body.split("\n")
    .map(line => line.trim())
    .filter(line => /^\[\d{1,3}:\d{2}\]/.test(line))
    .map(line => line.replace(/^\[\d{1,3}:\d{2}\]\s*/, ""))
    .map(line => collapseRepeatedCaptionSpans(line)
      .replace(/\[(?:music|applause)\]/gi, "")
      .replace(/&gt;&gt;|>>/g, "")
      .replace(/\s{2,}/g, " ")
      .trim())
    .filter(Boolean);
  if (!paragraphs.length) throw new Error("Transcript contains no timestamped content");
  return paragraphs.join("\n\n");
}

function main() {
  process.stdout.write(`${cleanTranscript(fs.readFileSync(0, "utf8"))}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) main();
