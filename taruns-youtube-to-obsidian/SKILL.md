---
name: taruns-youtube-to-obsidian
description: Use when the user asks to process Tarun Sabbineni's “To Obsidian” playlist, import new playlist videos, refresh Tarun's YouTube notes, add videos to the vault, or turn that playlist's transcripts into Obsidian notes—even when they do not name this skill.
compatibility: Requires a browser-control session that can load YouTube, outbound HTTPS to YouTube, yt-dlp for caption retrieval, Node.js for bundled helpers, and write access to the Taivault vault.
---

# Tarun's YouTube to Obsidian

Process newly absent videos by default. When the user explicitly asks to refresh or rerun the YouTube notes, process every existing note in scope in place, using the note's source video ID and preserving its vault relationships.

## Fixed scope

- Playlist: `https://www.youtube.com/playlist?list=PLfkZJsUFkayU`
- Vault folder: `06 - Resources/YouTube`
- Index: `06 - Resources/YouTube/00 - YouTube Index.md`
- Base: `06 - Resources/YouTube/01 - YouTube Base.base`
- Transcript source: YouTube captions retrieved with `yt-dlp`

Use `yt-dlp` only. Prefer creator-uploaded English captions and accept automatic English captions when no uploaded English track is available. Do not use alternate transcript providers, web search, or an LLM-generated transcript. Never save raw transcripts in the vault unless the user explicitly asks.

## Before processing

Read these files every run because they are the current source of truth:

- this skill's `Note contract` and `Regression coverage` sections
- `09 - Templates/YouTube Summary Template.md`
- `06 - Resources/YouTube/00 - YouTube Index.md`
- `06 - Resources/YouTube/01 - YouTube Base.base`
- Existing Markdown notes in `06 - Resources/YouTube`
- `.obsidian/plugins/obsidian-icon-folder/data.json`

Do not require a separate summary-instruction file: this skill and the template are the authoritative contract. If the template, index, or Base is missing, stop before writing notes and report the missing dependency. Do not create `To Obsidian Playlist.md` or change unrelated vault files.

## Bundled helpers

Use the scripts in `scripts/` for deterministic work instead of reimplementing it in prose:

- `inventory_playlist.mjs` validates compact browser-extracted playlist JSON.
- `normalize_sources.mjs` builds the existing YouTube source-ID index.
- `clean_transcript.mjs` removes caption metadata, timestamps, caption repetition, and filler markers from stdin in memory.
- `sanitize_filename.mjs` creates a safe readable filename stem.
- `audit_summary.mjs` checks framing, list cardinality, named-item coverage, title-answer coverage, explanatory depth, and high-stakes qualification.
- `refresh_notes.mjs` applies a refresh-mode rewrite from a run-local cleaned-transcript manifest while preserving filenames and vault relationships. It must receive one result for every existing source ID, consume non-empty cleaned transcript evidence, and record the transcript provider/evidence in the run-local manifest.
- `verify_notes.mjs` checks the final playlist/scope partition, note contract, semantic coverage, links, icons, stale files, and Base filter.

Run `node tests/test_helpers.mjs` after changing the helpers.

## Workflow

### 1. Inventory the playlist once

Open the fixed playlist in the browser-control session. Read the reported video count. Prefer one compact DOM evaluation that returns only `{id, title, creator, canonicalUrl}` records. Do not pass the full page snapshot into the model when compact extraction is available.

Run `inventory_playlist.mjs` on the extracted JSON. Scroll or load more only when `collectedCount < reportedCount`; stop when the count matches and IDs are unique. Every ID must be exactly 11 characters and every canonical URL must be `https://www.youtube.com/watch?v={ID}`.

### 2. Index existing notes once

Run `normalize_sources.mjs` against `06 - Resources/YouTube`. Normalize `watch?v=`, `youtu.be/`, and `/shorts/` URLs to IDs. A matching ID is already processed, even if the filename or title differs. Store the pre-existing ID set in memory for final verification.

Use the requested mode:

- **Import mode:** process only playlist IDs without an existing source note.
- **Refresh mode:** when the user asks to rerun, refresh every existing ordinary YouTube note in scope, preserving its filename, source ID, frontmatter, icon, and valid Related Topics links.

The playlist ID set must be partitioned into:

```text
pre-existing IDs + successfully created IDs + explicitly failed IDs
```

No ID may appear in more than one group, and the union must equal the full playlist.

### 3. Fetch captions with a bounded queue

Fetch target IDs serially with a small per-run request budget. In refresh mode, the target IDs are the existing source IDs; in import mode, they are the new playlist IDs. Do not fetch the same ID more than once unless retrying a transient failure.

Use `yt-dlp` in subtitle-only mode (for example, `--skip-download` with `--write-subs`, `--write-auto-subs`, `--sub-langs "en.*,en"`, and `--sub-format "vtt/best"`). Prefer a creator-uploaded English track; use an automatic English track only when no uploaded English track is available. Keep any VTT file in run-local temporary storage, pipe it to `clean_transcript.mjs`, and delete it immediately; never retain raw VTT in the vault or final run artifacts.

- Retry only network failures and HTTP `502`, `503`, or `504`.
- Honor `Retry-After` when present; otherwise use 5s, then 15s, then 45s backoff.
- Treat no English captions, bot checks, age/private/login/geo restrictions, and other non-transient `yt-dlp` failures as terminal failures for that ID.
- Do not retry a malformed caption file or a provider-policy failure.
- `clean_transcript.mjs` must collapse both exact repeated caption lines and rolling caption windows where the next cue repeats the previous cue’s suffix or prefix. Keep only cleaned transcript text in the run directory.

Record failures as `{id, title, reason}` and continue only with other already-fetched transcripts. A failed transcript must not produce a note.

### 4. Clean, inventory, and summarize

Use the cleaned transcript, this skill's Note contract, and the current template. Remove introductions, sponsors, calls to subscribe, repetition, filler, and transcript-shaped prose. Preserve methods, examples, trade-offs, and limitations. Distinguish personal anecdotes from general evidence.

- Before drafting, create a run-local coverage manifest for each transcript with `file`, `sourceId`, `mode`, `expectedCount` where applicable, every named item in source order, `supportingItems` for exhaustive inventories nested under a level or category, rank/tier where applicable, scope for “every/all/complete” titles, `requiresTitleAnswer`, `titleIntent`, and `titleAnswerKeywords` for titles that ask or imply why/how/best/worth-it questions, and `requiresQualification` for sensitive or high-stakes topics. Do not write the manifest into the vault.
- For counted lists, use exactly one top-level numbered Key Ideas entry per source item. Preserve product, book, game, system, exercise, metric, tool, example, recommendation, step, rule, and comparison names rather than replacing them with themes.
- Begin Key Ideas with a framing paragraph. Make every substantive item a short explanatory paragraph, normally 2–4 sentences or roughly 35–80 words; allow one sentence only when the transcript provides no further explanation.
- Treat the title as a second coverage track: answer what the video covers and the question or claim the title makes. For “Why I Only Focus on 7 Exercises”-style titles, Key Ideas must contain both the exhaustive exercise inventory and an explicit synthesis explaining why this set or approach was chosen; descriptions of the exercises alone are insufficient.
- For title-question or title-claim notes, add `requiresTitleAnswer: true`, a concise `titleIntent`, and source-supported `titleAnswerKeywords` to the manifest. Include a direct rationale paragraph in Key Ideas, usually after the framing paragraph and before or after the inventory, so a reader can answer the title without opening the transcript.
- For “every”, “all”, “complete”, and “full guide” titles, state the video’s scope and enumerate every item actually covered without implying universal completeness.
- For health, financial, legal, medical, exercise, safety, and privacy topics, attribute recommendations to the speaker or video and preserve risks, uncertainty, limitations, and context.
- Run `audit_summary.mjs` against each draft and its manifest. For counted lists, every title-relevant item belongs in a direct top-level entry; for title-question/claim notes, every `titleAnswerKeywords` term must appear in Key Ideas; for “every/all/complete” scopes, level/category entries may carry an explicit `supportingItems` inventory, but the inventory must appear in Key Ideas. Revise failures before writing the note.
- Keep the executive summary concise, but let Key Ideas carry the complete source coverage.

### 5. Name and write notes

Use `sanitize_filename.mjs` on the original title. Remove path separators, control characters, and invalid filename characters while preserving a readable title. If a safe filename already exists for a different source, append ` - {ID}`. Keep the original video title as the H1.

In refresh mode, write back to the existing filename instead of renaming it. Preserve existing frontmatter values and valid Related Topics links unless they are invalid; canonicalize the source URL to `https://www.youtube.com/watch?v={VIDEO_ID}`. Promote title-relevant content from legacy Useful Details into Key Ideas before removing or changing legacy sections.

Write all successful new or refreshed notes in one controlled bulk rewrite under `06 - Resources/YouTube`. Do not overwrite the folder or use shell redirection. If `yt-dlp` cannot retrieve an acceptable English caption for a note, leave that note unchanged and record the failure.

### 6. Assign icons

- Add one relevant emoji mapping for every new ordinary note in `.obsidian/plugins/obsidian-icon-folder/data.json`. Keep folders, indexes, and `.base` views on their existing monochrome `Li...` icons. Never assign a `Li...` icon to an ordinary note. Verify that each newly created note has a valid icon mapping before committing.

### 7. Verify before reporting

Run `verify_notes.mjs` with `mode: "import"` or `mode: "refresh"`, the playlist inventory, the complete `scopeIds` set, pre-existing IDs, `refreshedIds` when in refresh mode, refreshed or created note paths, coverage manifest, and failed transcript records. In refresh mode, every in-scope pre-existing ID must be refreshed or explicitly failed; an explicit transcript failure may retain its pre-existing note unchanged. Indexed notes that are no longer in the current playlist remain in `scopeIds` and are validated as refreshed legacy scope; they must not be silently discarded.

Verification passes when all of these are true:

- The playlist partition is complete and disjoint.
- The complete refresh/import scope is classified, including indexed legacy videos outside the current playlist when refresh mode was explicitly requested.
- Every non-failed playlist ID has exactly one matching source note.
- Every failed ID has no newly created note and appears in the failure report.
- New or refreshed notes have only the allowed frontmatter properties, non-empty required sections, valid parent links, canonical source URLs, reliable Creator values, valid Related Topics links, and compact taxonomy tags.
- New or refreshed notes pass semantic coverage: framing paragraph, list cardinality, named-item presence, explanatory depth, and required high-stakes qualification.
- New notes have non-`Li...` icons.
- No stale playlist-index file exists.
- The Base still contains `file.inFolder("06 - Resources/YouTube")`.

“Verification passed with transcript failures” is valid when the invariants above hold and every failure is explicit. Do not claim full import success when the partition is incomplete or any structural check fails.

## Note contract

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

This video covers the scope or central theme.

1. **Named source item or substantive idea.** Explain what it is, why it matters, how it works, and include source-supported context, examples, trade-offs, or qualifications in 2–4 sentences.

For list-based videos, use one direct top-level numbered entry per source item. Do not use `###` subheadings inside Key Ideas. Nested bullets are allowed only for supporting details.

For titles that ask or imply “why”, “how”, “best”, “worth it”, or a similar question, include a direct rationale or answer paragraph in Key Ideas in addition to the item inventory. A list of what was covered is not a complete answer to the title.

## Useful Details

Optional technical specifications, setup steps, measurements, or tables. Do not hide title-relevant items here.

## Actionable Takeaways

- Brief concrete action list.

## Caveats and Limitations
## Related Topics
```

For health, financial, legal, medical, exercise, safety, and privacy claims, include attribution and limitations and do not turn the video into individualized professional advice. Link Related Topics only to notes that exist in the vault.

## Final report

Report:

- Playlist videos found.
- Indexed scope extras outside the current playlist, if any.
- IDs skipped because their source already existed in import mode.
- Notes created or refreshed, with links.
- Transcript failures with ID, title, and reason.
- Filename/source collisions.
- Verification status, including whether it passed with explicitly reported transcript failures.

## Regression coverage

Keep `evals/evals.json` updated with realistic cases for: no new videos; mixed existing/new/failed IDs; refresh-all mode; indexed legacy scope outside the current playlist; alternate YouTube URL forms; yt-dlp-only caption retrieval; missing or restricted captions; exact and rolling caption repetition; filename collisions; counted-list cardinality; named products/books/games/systems in Key Ideas; title-rationale plus inventory coverage; supporting-item inventories; explanatory paragraph depth; “every/all” scope; high-stakes qualification; and broken-link or metadata regressions. Keep trigger-query coverage in `evals/trigger-queries.json` when the description changes.
