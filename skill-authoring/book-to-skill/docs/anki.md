# Stage 2: Anki Deck Specification

This stage turns an existing generated book skill into a portable Anki deck. It
is a retention layer, not a second book summary: the generated chapter files
remain the source of truth, while the cards turn their important ideas into
retrieval, explanation, discrimination, and application practice.

## Route and inputs

Run this stage when the user asks to turn a generated book skill into Anki,
flashcards, a deck, or spaced-repetition cards. Accept either the generated
skill directory or its `SKILL.md`. If only a source book is supplied, complete
Stage 1 first, then run Stage 2 against the newly generated skill.

Read, in this order:

1. `SKILL.md` for the book's core frameworks, chapter index, and limits.
2. Every file under `chapters/` for chapter-level coverage.
3. `patterns.md`, `cheatsheet.md`, and `glossary.md` for techniques, decisions,
   and exact term definitions.

Do not silently use general model knowledge to fill gaps. If the skill does not
support a card, omit it or report that the source skill is insufficient. If the
user requests a source-fidelity deck and the original book is available, use it
only for verification; do not copy long passages into cards.

## Output contract

Create an `anki/` directory inside the generated book skill containing:

- `anki/<book-slug>.tsv` — UTF-8, tab-separated, one physical row per card.
- `anki/import.md` — deck name, field mapping, import steps, card counts, and
  any limitations or omitted source areas.

The TSV header is exactly:

```text
Front	Back	Tags
```

Use Anki's Basic note type by default. Keep each card on one physical line;
represent display line breaks in the Back field as `<br>`. Replace literal tab
characters in generated content with spaces. Put chapter and card-type
traceability in space-separated tags such as
`book-slug::ch03::mechanism` and `book-slug::application`.

Run the bundled validator before reporting success:

```bash
python tools/validate_anki_tsv.py anki/<book-slug>.tsv
```

Fix invalid rows before delivery. Do not ship a deck with duplicate fronts,
blank fields, a wrong header, or ambiguous tab/newline escaping.

## Card design: Feynman plus tutor practice

If the host exposes a `book-learning-tutor` or Feynman companion skill, use it
for its teaching/retrieval conventions; otherwise follow this specification
directly. Use the Feynman method as the standard for card quality: ask the learner to
retrieve an idea, explain it plainly, expose the mechanism, and distinguish it
from a tempting wrong idea. Use the book-learning tutor pattern to vary the
practice: move from preparation and recall to explanation, application,
feedback-oriented correction, and later review. The cards should make the
learner generate an answer, not merely recognize a familiar phrase.

Prefer atomic cards with one testable demand. Build a balanced deck from these
card types, using only types supported by the chapter:

| Type | Front should ask | Back should contain |
|---|---|---|
| Concept | What is `<term>`? | Plain definition, significance, and chapter tag |
| Mechanism | Why/how does `<framework>` work? | Causal steps and the author's reasoning |
| Contrast | How is `<A>` different from `<B>`? | The distinction and when it matters |
| Procedure | What do I do when `<situation>` occurs? | Ordered steps or decision rule |
| Application | Given `<scenario>`, which idea applies and why? | Choice, reasoning, and relevant boundary |
| Failure mode | What commonly goes wrong with `<idea>`? | Anti-pattern, consequence, and correction |
| Worked example | What happened in the chapter's example? | Faithful compact reconstruction |
| Synthesis | How do chapters `<A>` and `<B>` fit together? | Relationship without inventing a new theory |

Backs should be self-contained enough to teach the answer after a failed
retrieval. Use concise prose or bullets; do not turn the Back into a chapter
dump. Include a source marker such as `Source: ch03 — <title>` at the end when
it improves traceability.

## Quantity and selection

Card counts are adaptive targets, not quotas. A useful default is 6–12 cards
for a substantive chapter, fewer for a genuinely short chapter, and 8–20
cross-chapter synthesis/application cards for the whole book. Increase the
count when the chapter contains distinct mechanisms, examples, or decision
rules; decrease it when cards would merely rephrase one idea.

Prioritize, in order:

1. The book's load-bearing principles and named frameworks.
2. Mechanisms and distinctions needed to apply them correctly.
3. The author's concrete examples, procedures, and failure modes.
4. Chapter connections and transfer questions.

Do not create cards just to satisfy a sentence or card count. Do not create a
card for every glossary entry. Do not duplicate a concept across multiple
fronts unless the card tests a genuinely different direction, such as recall
versus application.

## Fidelity and safety gate

Before writing each card, locate the supporting passage in the generated skill.
For each chapter, check that the selected cards collectively cover the chapter's
thesis, major frameworks, mechanisms, examples/evidence, caveats, and practical
use. Mark a card's answer as the author's claim, an anecdote, evidence, or an
inference when that distinction matters. Do not upgrade an anecdote into a
fact, turn a metaphor into a mechanism, or present a self-help or financial
claim as professional advice.

Reject or rewrite cards that:

- contain unsupported detail, invented examples, or fabricated quotations;
- ask two unrelated questions on one Front;
- have an answer that merely repeats the Front;
- test trivia that does not improve understanding or application;
- hide a necessary qualification on the back;
- require rereading the entire book to understand the answer.

At the end of `import.md`, report the number of cards by chapter and type and
list any source areas deliberately omitted because the generated skill did not
contain enough reliable material.
