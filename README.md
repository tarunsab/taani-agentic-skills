# Personal Codex and Bionic Skills

This public repository is the shared local skills source for Codex and Bionic.

It contains reusable agent skills, book-to-skill converters, and synthesized
book-derived knowledge skills for personal sharing.

The local checkout is `/Users/sai/.codex/skills`. Codex loads personal skills from that directory. Bionic can be configured to use the same directory through its configurable skills plugin.

System-managed Codex/plugin caches are intentionally excluded. EPUBs and other source books are not included; book-derived folders contain synthesized notes and guidance rather than the source books themselves.

## How to use this repository

The directory layout mirrors the catalog below:

- `start-here/` — conversation routing and collaboration
- `planning/` — planning, coordination, and delivery
- `engineering/` — engineering, debugging, and quality
- `design/` — design, prototyping, and presentations
- `research-workflows/` — research and media workflows
- `skill-authoring/` — creating and improving skills
- `books/` — book-derived personal knowledge skills

Skills are discovered from each linked `SKILL.md`. Use a skill when the request
matches its “When to use it” guidance. For a skill that is not automatically
selected, explicitly name it or point the agent at its `SKILL.md`.

## Start here and route work

- [`using-superpowers`](start-here/using-superpowers/SKILL.md) — Establish the skill-first workflow and require the right skill to be selected before work begins. Use at the start of every conversation or task.
- [`ask-matt`](start-here/ask-matt/SKILL.md) — Route a request to the skill or workflow that best fits it. Use when you are unsure which skill to invoke.
- [`handoff`](start-here/handoff/SKILL.md) — Turn the current conversation into a handoff document for another agent. Use when work needs to continue in a fresh context or be passed to someone else.
- [`teach`](start-here/teach/SKILL.md) — Teach a concept or skill within the workspace. Use when the goal is explanation, guided learning, or building understanding rather than changing a codebase.
- [`grilling`](start-here/grilling/SKILL.md) — Stress-test a plan, decision, or idea through relentless questioning. Use when the user explicitly wants hard challenge or says to grill the thinking.
- [`grill-me`](start-here/grill-me/SKILL.md) — Run a focused, relentless interview to sharpen a plan or design. Use when the user wants interactive questioning without necessarily creating project documents.
- [`grill-with-docs`](start-here/grill-with-docs/SKILL.md) — Combine a rigorous planning interview with live ADR and glossary documentation. Use when the decisions should be challenged and recorded as the discussion progresses.

## Planning, coordination, and delivery

- [`brainstorming`](planning/brainstorming/SKILL.md) — Explore intent, requirements, constraints, and design options before implementation. Use before creative work, new features, components, or behavior changes.
- [`writing-plans`](planning/writing-plans/SKILL.md) — Produce a concrete implementation plan from requirements. Use before multi-step work when the plan should be reviewed or executed separately.
- [`executing-plans`](planning/executing-plans/SKILL.md) — Execute an existing written plan with review checkpoints. Use when a plan already exists and the task is to carry it through.
- [`implement`](planning/implement/SKILL.md) — Implement work from a specification or set of tickets. Use when requirements are already clear and the task is hands-on delivery.
- [`dispatching-parallel-agents`](planning/dispatching-parallel-agents/SKILL.md) — Split independent work across agents without shared-state conflicts. Use when two or more tasks can proceed in parallel.
- [`subagent-driven-development`](planning/subagent-driven-development/SKILL.md) — Execute an implementation plan through independent subtasks in the current session. Use when delegation will speed up a coordinated build.
- [`domain-modeling`](planning/domain-modeling/SKILL.md) — Build and sharpen a project’s domain model and shared terminology. Use when naming, concepts, boundaries, or an architectural decision need to become explicit.
- [`wayfinder`](planning/wayfinder/SKILL.md) — Map a large body of work into decision tickets and resolve them sequentially. Use for projects too large for one agent session.
- [`to-spec`](planning/to-spec/SKILL.md) — Synthesize the current conversation into a project specification and publish it to the issue tracker. Use when discussion has converged and needs to become an actionable spec.
- [`to-tickets`](planning/to-tickets/SKILL.md) — Break a plan, specification, or conversation into tracer-bullet tickets with dependencies. Use when work needs to be organized into small, agent-ready units.
- [`triage`](planning/triage/SKILL.md) — Categorize, verify, and brief issues or external pull requests. Use when incoming work needs a consistent triage state and next action.
- [`finance-checkpoint`](planning/finance-checkpoint/SKILL.md) — Run a low-admin household Finance checkpoint that moves through four clear stages: review the position, review Goals, give an expert-style assessment against those Goals, then optionally model scenarios or answer a specific financial question.
- [`habits-checkpoint`](planning/habits-checkpoint/SKILL.md) — Manage an evidence-led, compounding habit system in Obsidian or Markdown vaults using the Atomic Habits framework, with baseline scorecards, AI audits, explicit approval gates, daily tracking, weekly reviews, and habit graduation.
- [`setup-matt-pocock-skills`](planning/setup-matt-pocock-skills/SKILL.md) — Configure a repository’s issue tracker, labels, and domain-document layout for the engineering workflow. Use once before using the related engineering skills in a new repo.

## Engineering, debugging, and quality

- [`codebase-design`](engineering/codebase-design/SKILL.md) — Improve module boundaries, interfaces, seams, testability, and AI navigability using deep-module design vocabulary. Use when designing or refactoring a codebase structure.
- [`improve-codebase-architecture`](engineering/improve-codebase-architecture/SKILL.md) — Scan a codebase for architectural deepening opportunities and produce a visual report before selecting one to pursue. Use when the architecture feels shallow, tangled, or hard to evolve.
- [`diagnosing-bugs`](engineering/diagnosing-bugs/SKILL.md) — Run a diagnosis loop for difficult bugs and performance regressions. Use when something is broken, throwing errors, failing, or slow and the cause is not yet established.
- [`systematic-debugging`](engineering/systematic-debugging/SKILL.md) — Investigate failures methodically before proposing a fix. Use whenever a bug, test failure, or systematic failure appears.
- [`tdd`](engineering/tdd/SKILL.md) — Apply test-driven development. Use when the user asks for test-first work, red-green-refactor, or integration tests.
- [`test-driven-development`](engineering/test-driven-development/SKILL.md) — Enforce a test-first workflow before writing implementation code. Use for feature work or bug fixes where behavior should be specified by tests.
- [`code-review`](engineering/code-review/SKILL.md) — Review changes against both repository standards and the originating specification. Use for branches, pull requests, work-in-progress changes, or requests to review since a fixed point.
- [`requesting-code-review`](engineering/requesting-code-review/SKILL.md) — Prepare a completed change for review against its requirements. Use after major implementation work or before merging.
- [`receiving-code-review`](engineering/receiving-code-review/SKILL.md) — Evaluate review feedback rigorously before acting on it. Use when feedback is unclear, conflicting, or technically questionable.
- [`resolving-merge-conflicts`](engineering/resolving-merge-conflicts/SKILL.md) — Resolve an in-progress Git merge or rebase conflict. Use when the repository is stopped on conflicting changes.
- [`using-git-worktrees`](engineering/using-git-worktrees/SKILL.md) — Create or reuse an isolated worktree for feature work or plan execution. Use when changes should be separated from the current checkout.
- [`finishing-a-development-branch`](engineering/finishing-a-development-branch/SKILL.md) — Decide how to integrate completed, tested branch work. Use when implementation is done and the next step is merge, PR, handoff, or cleanup.
- [`verification-before-completion`](engineering/verification-before-completion/SKILL.md) — Require fresh evidence before claiming work is complete, fixed, or passing. Use immediately before completion messages, commits, or pull requests.

## Design, prototyping, and presentations

- [`algorithmic-art`](design/algorithmic-art/SKILL.md) — Create original seeded, interactive generative art with p5.js. Use for code-generated art, flow fields, particle systems, or related experiments.
- [`anydesign`](design/anydesign/SKILL.md) — Analyze a visual reference and document its design tokens, components, and reconstruction notes. Use for screenshots, websites, Figma files, mockups, dashboards, or visual design audits.
- [`canvas-design`](design/canvas-design/SKILL.md) — Create original visual artwork as PNG or PDF. Use for posters, illustrations, and other static graphic-design requests.
- [`frontend-design`](design/frontend-design/SKILL.md) — Shape distinctive, intentional visual design for interfaces. Use when building or reshaping a UI and the result should avoid generic, templated styling.
- [`prototype`](design/prototype/SKILL.md) — Build a throwaway prototype to answer a design or interaction question. Use to test a state model, flow, or UI idea before committing to production implementation.
- [`beautiful-html-templates`](design/beautiful-html-templates/SKILL.md) — Select and adapt a distinctive bundled HTML slide template. Use for web presentations, template shortlists, or decks built from the included design systems.
- [`frontend-slides`](design/frontend-slides/SKILL.md) — Create animation-rich HTML presentations or convert PowerPoint decks to the web. Use when the deliverable is a web-based presentation or a PPT/PPTX conversion.

## Research, media, and document workflows

- [`research`](research-workflows/research/SKILL.md) — Investigate a question using high-trust primary sources and capture the findings in a Markdown file. Use when research, documentation facts, or delegated reading needs to become a repo artifact.
- [`taruns-youtube-to-obsidian`](research-workflows/taruns-youtube-to-obsidian/SKILL.md) — Import and refresh notes from Tarun Sabbineni’s “To Obsidian” YouTube playlist. Use for that playlist’s videos, transcripts, or Obsidian additions.

## Creating and improving skills

- [`skill-creator`](skill-authoring/skill-creator/SKILL.md) — Create, modify, optimize, and evaluate Codex skills. Use when building a new skill, improving an existing one, measuring behavior, or tuning its trigger description.
- [`writing-skills`](skill-authoring/writing-skills/SKILL.md) — Create or edit skills and verify them before deployment. Use for practical skill-authoring work that needs a disciplined workflow.
- [`writing-great-skills`](skill-authoring/writing-great-skills/SKILL.md) — Apply the vocabulary and principles of predictable, effective skill writing. Use when reviewing the quality, scope, or trigger behavior of a skill.
- [`book-to-skill`](skill-authoring/book-to-skill/SKILL.md) — Convert a book or document into a structured agent skill containing frameworks, mental models, principles, techniques, and anti-patterns. Use with EPUB, PDF, DOCX, HTML, Markdown, plain text, RTF, or Calibre-supported MOBI/AZW files.
- [`book-to-skill-with-depth`](skill-authoring/book-to-skill-with-depth/SKILL.md) — Perform the same book-to-skill conversion with deliberately deeper, source-grounded sections instead of one-line summaries. Use when the generated skill should preserve more explanatory substance without padding or inventing content.
- [`technical-book-to-skill`](skill-authoring/technical-book-to-skill/SKILL.md) — Convert technical books, papers, manuals, programming guides, and code-, table-, formula-, or diagram-heavy sources with technical extraction defaults, deeper chapter coverage, and the same optional Anki stage.

The book converters can optionally run a second stage after conversion: turn the generated skill into a portable UTF-8 Anki TSV and import guide using Feynman-style explanation, tutor-style retrieval, and source-grounded application cards. The Anki stage is opt-in and does not alter the Stage 1 skill structure.

## Book-derived personal knowledge skills

Each book-derived skill appears exactly once under `books/`; read-book skills
are direct children, while book skills awaiting reading are grouped under
`books/unread/`. These are the canonical repository copies and are not
duplicated at the repo root.

The `books/unread/` group contains the latest generated book skills. Their
iCloud companion folders use an `unread-` prefix, and their duplicate
Obsidian folders are kept out of the vault until the books have been read.
Interrupted conversions may remain in this group as partial drafts; check for
the presence of `SKILL.md` before invoking one.

- [`atomic-habits-skill`](books/atomic-habits-skill/SKILL.md) — Apply James Clear’s habit-change framework. Use to build, break, diagnose, track, or sustain habits; shape an environment; recover from lapses; or turn goals into repeatable systems.
- [`i-will-teach-you-to-be-rich-second-edition-skill`](books/i-will-teach-you-to-be-rich-second-edition-skill/SKILL.md) — Apply Ramit Sethi’s personal-finance frameworks. Use for conscious spending, automation, debt, investing, negotiation, and designing a Rich Life.
- [`ikigai-the-japanese-secret-to-a-long-and-happy-life-skill`](books/ikigai-the-japanese-secret-to-a-long-and-happy-life-skill/SKILL.md) — Apply the Ikigai framework to purpose, meaningful activity, flow, healthy practices, community, resilience, and long-term engagement. Use when reflecting on life direction or sustainable wellbeing.
- [`rich-dad-poor-dad-skill`](books/rich-dad-poor-dad-skill/SKILL.md) — Apply Robert Kiyosaki’s financial-education framework. Use for cash-flow thinking, assets and liabilities, financial intelligence, investing mindset, and behavioral obstacles to financial progress.
- [`the-courage-to-be-disliked-skill`](books/the-courage-to-be-disliked-skill/SKILL.md) — Apply the Adlerian framework from The Courage to Be Disliked. Use for personal responsibility, interpersonal boundaries, contribution, encouragement, and present-focused action.
- [`the-mountain-is-you-skill`](books/the-mountain-is-you-skill/SKILL.md) — Apply Brianna Wiest’s framework for self-sabotage, emotional processing, self-mastery, inner peace, purpose, and aligned action. Use when turning triggers, unmet needs, and recurring patterns into deliberate change.
