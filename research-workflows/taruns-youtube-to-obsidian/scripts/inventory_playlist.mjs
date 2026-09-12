import fs from "node:fs";
import { fileURLToPath } from "node:url";

export function normalizeVideo(item) {
  if (!item || typeof item !== "object") throw new Error("Playlist item must be an object");
  const id = String(item.id ?? "").trim();
  const title = String(item.title ?? "").trim();
  const creator = String(item.creator ?? "").trim();
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) throw new Error(`Invalid video ID: ${id}`);
  if (!title) throw new Error(`Missing title for ${id}`);
  if (!creator) throw new Error(`Missing creator for ${id}`);
  const canonicalUrl = `https://www.youtube.com/watch?v=${id}`;
  return { id, title, creator, canonicalUrl };
}

export function validatePlaylist(payload) {
  const reportedCount = Number(payload?.reportedCount ?? payload?.count ?? 0);
  const rawVideos = Array.isArray(payload) ? payload : payload?.videos;
  if (!Array.isArray(rawVideos)) throw new Error("Expected a playlist array or {videos: [...]} payload");
  const videos = rawVideos.map(normalizeVideo);
  const ids = new Set();
  for (const video of videos) {
    if (ids.has(video.id)) throw new Error(`Duplicate playlist ID: ${video.id}`);
    ids.add(video.id);
  }
  if (reportedCount && videos.length !== reportedCount) {
    throw new Error(`Collected ${videos.length} videos but playlist reports ${reportedCount}`);
  }
  return {
    reportedCount: reportedCount || videos.length,
    collectedCount: videos.length,
    complete: true,
    videos
  };
}

function main() {
  const input = fs.readFileSync(0, "utf8");
  const payload = JSON.parse(input);
  process.stdout.write(`${JSON.stringify(validatePlaylist(payload), null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) main();
