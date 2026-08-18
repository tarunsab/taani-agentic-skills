---
name: taruns-youtube-to-obsidian
description: Use when the user asks to process Tarun Sabbineni's “To Obsidian” playlist, import new playlist videos, refresh Tarun's YouTube notes, add videos to the vault, or turn that playlist's transcripts into Obsidian notes—even when they do not name this skill.
compatibility: Requires a browser-control session that can load YouTube, outbound HTTPS to the transcript endpoint, Node.js for bundled helpers, and write access to the Taivault vault.
---

# Tarun's YouTube to Obsidian

Process only videos newly absent from the vault into concise, discoverable Obsidian notes.

## Fixed scope

- Playlist: `https://www.youtube.com/playlist?list=PLfkZJsUFkayU`
- Vault folder: `06 - Resources/YouTube`
- Index: `06 - Resources/YouTube/00 - YouTube Index.md`
- Base: `06 - Resources/YouTube/01 - YouTube Base.base`
- Transcript API: `https://youtube-transcript.ai/transcript/{VIDEO_ID}.txt`

Use the exact transcript API path. Do not use web search or a different transcript provider as a workaround. Never save raw transcripts unless the user explicitly asks.

## Before processing

Read these files every run because they are the current source of truth:

- `05 - Knowledge/YouTube Summary Gemini Prompt.md`
- `05 - Knowledge/YouTube Summary Prompt-Skill.md` only when the Gemini Prompt file is absent
- `09 - Templates/YouTube Summary Template.md`
- `06 - Resources/YouTube/00 - YouTube Index.md`
- `06 - Resources/YouTube/01 - YouTube Base.base`
- Existing Markdown notes in `06 - Resources/YouTube`
- `.obsidian/plugins/obsidian-icon-folder/data.json`

If neither prompt file exists, stop before writing notes and report the missing dependency. Do not create `To Obsidian Playlist.md` or change unrelated vault files.

## Bundled helpers

Use the scripts in `scripts/` for deterministic work instead of reimplementing it in prose:

- `inventory_playlist.mjs` validates compact browser-extracted playlist JSON.
- `normalize_sources.mjs` builds the existing YouTube source-ID index.
- `clean_transcript.mjs` removes API metadata, timestamps, caption repetition, and filler markers from stdin in memory.
- `sanitize_filename.mjs` creates a safe readable filename stem.
- `verify_notes.mjs` checks the final playlist partition, note contract, links, icons, stale files, and Base filter.

Run `node tests/test_helpers.mjs` after changing the helpers.

## Workflow

### 1. Inventory the playlist once

Open the fixed playlist in the browser-control session. Read the reported video count. Prefer one compact DOM evaluation that returns only `{id, title, creator, canonicalUrl}` records. Do not pass the full page snapshot into the model when compact extraction is available.

Run `inventory_playlist.mjs` on the extracted JSON. Scroll or load more only when `collectedCount < reportedCount`; stop when the count matches and IDs are unique. Every ID must be exactly 11 characters and every canonical URL must be `https://www.youtube.com/watch?v={ID}`.

### 2. Index existing notes once

Run `normalize_sources.mjs` against `06 - Resources/YouTube`. Normalize `watch?v=`, `youtu.be/`, and `/shorts/` URLs to IDs. A matching ID is already processed, even if the filename or title differs. Store the pre-existing ID set in memory for final verification.

The playlist ID set must be partitioned into:

```text
pre-existing IDs + successfully created IDs + explicitly failed IDs
```

No ID may appear in more than one group, and the union must equal the full playlist.

### 3. Fetch transcripts with a bounded queue

Fetch new IDs serially with a small per-run request budget. Do not fetch the same ID more than once unless retrying a transient failure.

- Retry only network failures and HTTP `502`, `503`, or `504`.
- Honor `Retry-After` when present; otherwise use 5s, then 15s, then 45s backoff.
- Treat HTTP `429`, quota text, “high volume” text, or other rate-limit responses as a terminal failure for that ID and stop further transcript requests for the run.
- Do not retry a malformed response or a provider policy/quota failure.
- Keep each successful response in memory and pipe it directly to `clean_transcript.mjs`; never write the raw response to disk.

Record failures as `{id, title, reason}` and continue only with other already-fetched transcripts. A failed transcript must not produce a note.

### 4. Clean and summarize

Use the cleaned transcript, current prompt, and current template. Remove introductions, sponsors, calls to subscribe, repetition, filler, and transcript-shaped prose. Preserve methods, examples, trade-offs, and limitations. Distinguish personal anecdotes from general evidence.

- Cleaned transcripts of 8,000 words or fewer: summarize directly.
- Longer transcripts: summarize chunks into internal key points, then write one final note from those key points.
- Target 500–1,000 words; allow up to 1,500 only for unusually dense material.
- Do not copy transcript metadata into the note.

### 5. Name and write notes

Use `sanitize_filename.mjs` on the original title. Remove path separators, control characters, and invalid filename characters while preserving a readable title. If a safe filename already exists for a different source, append ` - {ID}`. Keep the original video title as the H1.

Write all new notes in one `apply_patch` operation under `06 - Resources/YouTube`. Do not overwrite the folder or use shell redirection.

### 6. Assign icons

Add one relevant emoji mapping for every new ordinary note in `.obsidian/plugins/obsidian-icon-folder/data.json`. Keep folders, indexes, and `.base` views on their existing monochrome `Li...` icons. Never assign a `Li...` icon to an ordinary note.

### 7. Verify before reporting

Run `verify_notes.mjs` with the playlist inventory, pre-existing IDs, created note paths, and failed transcript records. Verification passes when all of these are true:

- The playlist partition is complete and disjoint.
- Every non-failed playlist ID has exactly one matching source note.
- Every failed ID has no newly created note and appears in the failure report.
- New notes have only the allowed frontmatter properties, required sections, valid parent links, valid Related Topics links, and compact taxonomy tags.
- New notes have non-`Li...` icons.
- No stale playlist-index file exists.
- The Base still contains `file.inFolder("06 - Resources/YouTube")`.

“Verification passed with transcript failures” is valid when the invariants above hold and every failure is explicit. Do not claim full import success when the partition is incomplete or any structural check fails.

## New-note contract

Use only these generated frontmatter properties:

```yaml
---
parent: "[[06 - Resources/YouTube/00 - YouTube Index|YouTube Index]]"
tags:
  - topic-tag
source: "https://www.youtube.com/watch?v=VIDEO_ID"
date: YYYY-MM-DD
---
```

Use one or two specific, lowercase, kebab-case content tags from: `obsidian`, `ai`, `books`, `learning`, `productivity`, `health`, `house`, `hardware`, `photography`, `games`, or `buy-it-for-life`. Do not add provenance, location, creator, or near-duplicate tags. Do not add `type`, `title`, `description`, `author`, `published`, `created`, or `status`.

## Required note structure

```markdown
# Original Video Title

## Source

- Creator: Channel name
- Video: [Original Video Title](https://www.youtube.com/watch?v=VIDEO_ID)

## Executive Summary
## Key Ideas
## Useful Details
## Actionable Takeaways
## Caveats and Limitations
## Related Topics
```

For health, financial, legal, or safety claims, include limitations and do not turn the video into professional advice. Link Related Topics only to notes that exist in the vault.

## Final report

Report:

- Playlist videos found.
- IDs skipped because their source already existed.
- Notes created, with links.
- Transcript failures with ID, title, and reason.
- Filename/source collisions.
- Verification status, including whether it passed with explicitly reported transcript failures.

## Regression coverage

Keep `evals/evals.json` updated with realistic cases for: no new videos; mixed existing/new/failed IDs; alternate YouTube URL forms; caption repetition; filename collisions; and broken-link or metadata regressions. Keep trigger-query coverage in `evals/trigger-queries.json` when the description changes.
