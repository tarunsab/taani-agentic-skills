# Stage 2: Generated book skill to self-help Anki

This stage converts an existing `book-to-skill-with-depth` output into a
memory and re-teaching system. The generated skill is the canonical input. Do
not independently re-process or reinterpret the original book during ordinary
Anki generation. The original source may be consulted only when the user asks
for verification, the skill marks a claim uncertain, generated files conflict,
or a readily available source check is needed to prevent a misleading card.

The target is usable recall months or years later: the learner should remember
important ideas, understand why they work, recognise when they apply, and
reconstruct a forgotten concept from the card itself.

## Input and source hierarchy

Accept a generated skill directory or its `SKILL.md`; resolve a `SKILL.md` path
to its enclosing directory. Require `SKILL.md` and `chapters/`. Prefer, but do
not require, `patterns.md`, `cheatsheet.md`, and `glossary.md`. Do not silently
treat an arbitrary Markdown directory as a book skill.

Read sources in this order:

1. `SKILL.md` for the thesis, load-bearing ideas, named frameworks, relationships,
   techniques, intended application, and chapter map.
2. Every file under `chapters/` for definitions, mechanisms, examples, procedures,
   caveats, evidence, failure modes, and connections. These are the primary
   semantic sources for card generation.
3. `patterns.md` for repeatable techniques, procedures, decision rules, and
   trigger-to-response relationships.
4. `cheatsheet.md` for high-value decisions and synthesis. Do not make a card
   from every bullet.
5. `glossary.md` to preserve terminology and resolve distinctions. Do not make a
   definition card for every entry.

The deck is not a quiz about chapter numbers, anecdotes, quotations, names, or
trivia. Optimise for principles, mechanisms, application, distinctions,
procedures, failure modes, and reconstruction of the book's model.

## Forgotten-book assumption

Assume that a learner may remember nothing when any card appears. Every
important card has two jobs:

```text
Front → test memory
Back  → confirm memory or teach the idea again
```

This is a hard requirement. A card that merely names a concept, repeats a
slogan, or uses unexplained jargon fails even if its answer is factually true.

## Teaching-answer requirement

This rule is domain-neutral: apply it to self-help, psychology, productivity,
leadership, relationships, and other behavior-oriented books. The source's own
terms and frameworks determine what gets explained; do not import a fixed
framework or assume every book has the same laws.

The Front may be a short quiz prompt, a glossary term, or a realistic situation.
The first `Answer` section on the Back is the primary teaching unit; do not put
the actual explanation only in `Re-teach`. A learner who has forgotten the book
must be able to read `Answer` and understand the concept without reopening the
source notes.

Use the answer shape that fits the target:

- **Concept or glossary term:** give a plain definition, why it matters, the
  mechanism or role it plays, and a boundary, distinction, or use condition
  when the source supports one.
- **Framework, law, or named list:** name every member and explain what each
  one changes, why it works, and its inversion or example when applicable. A
  sentence that only lists the names is insufficient.
- **Mechanism:** state the causal chain in order, then connect it to the
  practical decision it changes.
- **Pattern or procedure:** give the trigger, the steps, and the reason the
  steps work; include a source example when it clarifies transfer.
- **Situation or application:** name the relevant idea, explain the choice, and
  state the limitation or tempting mistake that would change the decision.

Aim for three to eight clear sentences or a short labelled list in `Answer`;
major frameworks may need one explanatory sentence per member. Keep `Re-teach`
as a second pass that restores the idea after a miss, adds a compact memory
cue, or explains a common confusion. Never use a one-sentence label as the
only explanation for a major concept, mechanism, glossary definition, or
framework.

## Concept model before cards

Do not turn paragraphs into questions in a single pass. First construct an
internal semantic model and save it as `anki/concepts.json`. Each important
entry should include the fields that the source supports:

```json
{
  "id": "environment-design",
  "name": "Environment Design",
  "importance": "tier1",
  "chapter": "ch06",
  "type": "principle",
  "definition": "...",
  "core_claim": "...",
  "why_it_matters": "...",
  "mechanism": "...",
  "when_to_use": "...",
  "how_to_apply": "...",
  "example": "...",
  "counterexample": "...",
  "failure_mode": "...",
  "distinction": "...",
  "limitations": "...",
  "related_concepts": ["friction", "cues"]
}
```

Do not invent values for unsupported fields. The concept model separates
extraction, ranking, card generation, and later regeneration.

## Importance and card selection

Rank concepts by value rather than by chapter length:

- **Tier 1 — Load-bearing:** forgetting it substantially harms understanding or
  application. Normally generate complementary retrieval directions.
- **Tier 2 — Important:** worth retaining and likely useful. Normally generate
  one or two cards.
- **Tier 3 — Supporting:** context, examples, qualifications, or evidence. Put
  it on a related card unless independent retrieval has meaningful value.
- **Tier 4 — Not worth memorising:** omit.

Use `importance × retrieval usefulness × application usefulness × likelihood of
forgetting × conceptual distinctiveness` as a qualitative ranking aid. Do not
use a fixed number of cards per chapter. A standard self-help deck is often
roughly 70–140 cards, but compact (~40–70) and deep (~120–220) variants are
valid ranges, never quotas. Prefer 85 excellent cards to 180 repetitions.

## Companion coverage pass

The deck normally sits on top of the generated skill rather than replacing it.
When `SKILL.md` has a cheatsheet, patterns, glossary, templates, or a default
workflow, perform a companion coverage pass after the core concept ranking:

- add direct retrieval for the skill's model, workflow, response modes, and
  guardrails;
- cover the cheatsheet's build/break procedures, diagnostic worksheet, failure
  modes, and review questions;
- give each named reusable pattern a trigger, application, or failure card when
  the source supports one;
- give glossary terms a direct card or a meaningful contrast/application card,
  grouping only terms whose distinction is the actual learning target; and
- keep source examples on the cards where they teach transfer, rather than
  creating anecdote or trivia cards.

Use a procedure overview plus smaller component cards for long checklists. Do
not turn every bullet into a card or use duplicate definition fronts to meet a
target. If the user requests an exhaustive companion deck or a card count such
as 100, treat the count as a ceiling/floor constraint only after these source
areas have direct coverage, and report any deliberately omitted material.

## Card types and retrieval networks

Use only types supported by the source. The approximate mix below guides balance
for self-help, psychology, and productivity books; the source controls the deck.

| Type | What it tests |
|---|---|
| Concept recall | What the idea means, with definition and significance |
| Mechanism / why | Why the idea works and what causal link matters |
| Situation → concept | Recognising an unnamed real-life situation and retrieving the relevant idea |
| Concept → application | Using the idea in a specified situation, including a limitation |
| Trigger | What observation should make the idea come to mind |
| Contrast | A meaningful distinction and when it matters |
| Failure mode | Mistake → consequence → correction |
| Procedure | A genuine process; use an overview plus small cards for difficult components |
| Book-map / synthesis | The conceptual spine and relationships between ideas |
| Worked example | What a source example illustrates, not incidental trivia |

Typical shares are concept 20–25%, mechanism 15–20%, situation 20–25%,
application 10–15%, trigger 5–10%, contrast 5–10%, failure 5–10%, and
book-map/synthesis 5–10%. Treat these as diagnostics, not targets.

For a Tier 1 concept, build a retrieval network when the source supports it:

```text
                    ┌── Why does it work?
                    │
Situation ──→ CONCEPT ──→ How do I apply it?
                    │
                    ├── What should trigger it?
                    │
                    └── What is it confused with?
```

This is useful redundancy. “What is X?”, “Define X,” and “What does X mean?”
are bad redundancy when they test the same recall route.

## Question and back design

Each Front has one primary retrieval target and enough context to make sense
after long forgetting. Context should disambiguate without revealing the
answer. Prefer recall and realistic situations over recognition, yes/no, and
multiple choice. Do not ask “What is the second law?” without naming the
framework. Do not hide the answer in a scenario that asks the learner to
identify the concept.

Every substantial card uses progressive disclosure:

```html
<b>Answer</b><br>
{direct teaching answer in 2–6 sentences or a short labelled list}
<br><br>
<b>Re-teach</b><br>
{why it matters, how it works, and the source-supported detail needed to recover it}
<br><br>
<b>Example</b><br>
{source example or clearly labelled illustration, when useful}
<br><br>
<b>Remember</b><br>
{one compact decision rule or connection, when useful}
<br><br>
<span class="source">Source: {chapter and section}</span>
```

Omit empty sections, but do not omit re-teaching for Tier 1 or Tier 2 cards.
The first visible section answers the question quickly and teaches the idea;
the re-teach section must make recovery easier after retrieval failed. Define a term before
using it, explain its mechanism, and include why it matters or when it applies
when the source supports that detail. A one-sentence back is acceptable only for
a genuinely simple fact or precise label that remains intelligible without
prior context. Do not optimise for short answers or turn the back into another
chapter. The ideal is quick verification plus compact re-learning.

Keep the learner's grading target clear: the Answer is what must be retrieved,
while Re-teach is feedback that restores understanding. This does not mean
Re-teach is optional or that the learner must recite every sentence. A single
learning target can have several explanatory sentences.

Prefer examples already present in the generated skill. Generic examples may be
used only when they teach transfer, must be labelled illustrative or
hypothetical, and must not be attributed to the author. A caveat, statistic, or
quote normally belongs on a related card rather than receiving its own card.

## Source fidelity and epistemic status

Every substantive claim must be supported somewhere in the generated skill.
Distinguish the author's argument, a framework proposal, a chapter
illustration, cited research, and an anecdote. Do not upgrade an anecdote or
metaphor into a universal fact. Do not fill gaps with general model knowledge,
another book, internet knowledge, or what the author “probably meant.” Omit
unsupported cards or report the gap. If the original book is explicitly used for
verification, record that separately; it does not replace the generated skill
as the normal Stage 2 source.

## Stable IDs, fields, and tags

Give every card a deterministic ID:

```text
<book-slug>::<concept-slug>::<card-type>::<variant>
```

Never assign random IDs. They allow future regeneration to retain notes and
identify changed cards. Logically model these fields:

```text
ID, Front, Answer, Reteach, Example, Connections, Source, Tags
```

For portable Basic-note import, render the latter fields into one HTML `Back`
field while retaining the richer structure in `concepts.json`. Use hierarchical
tags such as:

```text
atomic-habits atomic-habits::ch06 atomic-habits::concept::environment-design atomic-habits::type::scenario atomic-habits::tier::core
```

Add thematic tags only when they aid filtering. Do not create tags for every
word or heading.

## Output files

Create inside the generated skill's `anki/` directory:

```text
<book-slug>.tsv
concepts.json
preview.md
report.md
import.md
```

The canonical portable TSV has exactly:

```text
ID<TAB>Front<TAB>Back<TAB>Tags
```

It must be UTF-8, deterministically ordered, one physical line per card, free
of literal tabs inside fields, and use `<br>` for display line breaks. Validate
IDs, duplicate fronts, duplicate IDs, blank fields, and HTML. If maximum Anki
portability is needed, emit a separate header-safe import file using Anki
directives (`#separator:Tab`, `#html:true`, `#columns:ID\tFront\tBack\tTags`)
and tell the user to preview it. Do not silently treat the ordinary field row as
a card.

## Preview and report

`preview.md` is organised for human review rather than only by row number:

```text
## Book-wide cards
## Chapter 1
### Core concepts
### Mechanisms
### Application / scenarios
```

Show Front, Answer, Re-teach, Example, and Source for each card. `report.md`
must include the book, concepts extracted and their tiers, total cards, counts
by card type and chapter, Tier 1 concepts lacking application or trigger
practice, potential duplicates removed, omitted source areas, unsupported or
ambiguous material, and the top ten load-bearing concepts.

## Multi-pass generation

Do not generate the final TSV in one pass. Follow this sequence:

1. Understand the generated skill architecture.
2. Extract concepts into `concepts.json`.
3. Rank concepts by importance.
4. Generate candidate concept, mechanism, contrast, procedure, and failure cards.
5. Generate situation, application, and trigger cards for actionable Tier 1/2 ideas.
6. Add re-teaching explanations and source examples.
7. Deduplicate and test atomicity.
8. Audit book and supporting-file coverage and source fidelity.
9. Run the forgotten-book, book-reconstruction, and real-life retrieval tests.
10. Export, validate, and write preview/report/import files.

## Required quality tests

For each Tier 1 concept, ensure there is an understanding/reasoning card and,
when a meaningful real-life cue exists, a situation, trigger, or application
card. Tier 2 usually needs one or two cards. Before finalising, sample Tier 1
and Tier 2 cards under the following forgotten-book test:

1. Is the Front understandable without remembering the chapter?
2. Does it require meaningful generation rather than recognition?
3. If the learner says “I have no idea,” does the Back teach the concept?
4. Does the learner understand why it matters afterward?
5. Where appropriate, would the learner recognise a future situation where it applies?

Then run a book-reconstruction test: after mastering the deck, could the learner
explain the thesis, principles, frameworks, mechanisms, procedures, distinctions,
failures, use conditions, and relationships? If the deck feels like unrelated
facts, revise it. Run a real-life retrieval test for each major actionable idea:
what observation should make it come to mind, and is that cue represented by a
scenario, trigger, or application card?

For companion coverage, also verify that the learner can reconstruct the
cheatsheet workflow, the named patterns and their triggers, the glossary's
important distinctions, and the skill's practical templates without reopening
the supporting files. Record source-area counts and omissions in `report.md`.

Per-card gate:

- **Importance:** forgetting it matters.
- **Retrieval:** the learner must generate an answer.
- **Atomicity:** one primary test.
- **Context:** the Front still makes sense in a year.
- **Re-teaching:** the Back can recover the idea after complete forgetting.
- **Transfer:** important actionable concepts have use-in-context practice.
- **Fidelity:** every substantive claim is supported by the generated skill.
- **Duplication:** another card does not test essentially the same route.

Reject or rewrite cards that fail any gate. Specifically reject slogan cards,
chapter-number cards, trivia, unsupported claims, giant enumeration cards,
unexplained jargon, and backs that merely repeat the Front.

## Updating an existing deck

If `anki/concepts.json` exists, compare the current model semantically with the
new generated skill. Retain stable concept and card IDs; update changed cards,
create genuinely new cards, and flag obsolete cards. Do not silently remove
cards. Write `anki/changes.md` with counts and an old-to-new mapping, for
example: unchanged, updated, added, and potentially obsolete. A changed Front
may be treated as a new note by Anki, so do not claim that a TSV rewrite
preserves review history. Never invent random GUIDs, reset schedules, delete
notes, or modify a live Anki collection without explicit scope.

## Default behaviour and routine

For a normal request, discover and read the generated skill, build and save the
concept model, rank concepts, generate complementary retrieval and
re-teaching cards, run all quality tests, and export the files. Default to:

```yaml
depth: standard
reteach: true
scenarios: true
applications: true
triggers: true
synthesis: true
source_markers: true
```

The learner should understand the chapter before introducing its cards. Start
with core cards and a manageable number of new cards, retrieve before revealing,
and use the Re-teach section after a miss. Once a week, explain a framework from
a blank page and try a fresh situation. For actionable books, run one small real
experiment and review what happened outside the graded deck. Inspect review
time, repeated lapses, unaided explanation, and application; rewrite or suspend
low-value cards before adding more.

Success means that spaced repetition preserves usable intellectual value. After
six or twelve months, the learner should be able to recognise the situation,
retrieve the important idea, explain why it works, and recover it from the card
when forgotten.
