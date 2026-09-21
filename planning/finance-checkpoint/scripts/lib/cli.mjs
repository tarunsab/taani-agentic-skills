import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function parseArgs(argv, valueOptions = []) {
  const result = {};
  const values = new Set(valueOptions);
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) throw new Error(`Unexpected argument: ${token}`);
    const key = token.slice(2);
    if (values.has(key)) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`Missing value for --${key}`);
      result[key] = value;
      index += 1;
    } else {
      result[key] = true;
    }
  }
  return result;
}

export function requireArg(args, name) {
  if (!args[name]) throw new Error(`Missing required --${name}`);
  return args[name];
}

export function skillRoot(importMetaUrl) {
  return path.resolve(path.dirname(fileURLToPath(importMetaUrl)), "..");
}

export function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

export function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

export function fail(error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
