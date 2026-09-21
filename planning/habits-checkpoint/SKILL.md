---
name: habits-checkpoint
description: Manage an evidence-led, compounding habit system in Obsidian or Markdown vaults using the Atomic Habits framework. Handles baseline observation, AI audits, experiment proposals, explicit human approval gates, daily tracking, weekly reviews, and habit graduation.
---

# Habits Checkpoint

Manage an evidence-grounded, compounding habit system within a Markdown-first personal knowledge base (such as Obsidian). This skill bridges daily behavioral observations with James Clear's *Atomic Habits* methodology, enforcing strict boundaries between human-approved truth, persistent AI reasoning, and disposable local computation.

## Key Distinction: Methodology vs Checkpoint Skill

- **`atomic-habits-skill` (Methodology)**: The pure behavioral psychology framework (Four Laws, habit loop, 2-minute rule, habit stacking, inversion of laws, recovery rules). It contains zero vault paths, zero personal context, and serves as the coaching engine.
- **`habits-checkpoint` (Checkpoint & Workspace Orchestrator)**: This skill. It guides agents and users through the operational lifecycle in the vault: managing baseline scorecards, structuring non-canonical AI audits and proposals, enforcing human approval gates, tracking daily check-ins, drafting diagnostic reviews, and graduating solidified habits back into the baseline.

## Four-Tier Storage Discipline

Every file created or modified must belong to one of four strict tiers:

```text
TIER 1: EPHEMERAL LOCAL COMPUTATION
$HOME/.taani-agent/workspaces/habits/
→ Scratch analysis, JSON munging, API caches, raw mobile exports parsing, one-off scripts.
→ Disposable, local-only, strictly OUTSIDE the vault / iCloud.

TIER 2: PERSISTENT AI WORKING KNOWLEDGE
11 - Agents/Workspace/Habits/
→ Non-canonical AI reasoning: Current State Analysis.md, Atomic Habits Audit.md, Proposed Changes.md.
→ Subdirectories: Experiments/ (proposals without canonical IDs), Reviews/ (AI drafts).
→ Durable across sessions, but NOT canonical life truth.

TIER 3: CANONICAL VAULT TRUTH & HISTORY
04 - Areas/Habits/
→ Human-approved state: 00 - Habits Index.md, Current Habits.md, Active Habit Experiments.md, Daily Habit Tracking.md.
→ Subdirectories: Experiments/ (canonical H### notes), Reviews/ (approved weekly reviews), Tracking/ (daily/weekly tracking sheets).
→ Requires EXPLICIT user approval for creation, promotion, or modification.

TIER 4: GENERIC REUSABLE METHODOLOGY
~/.codex/skills/books/atomic-habits-skill/
→ Git-controlled, generic behavioral design methodology. Free of any personal data.
```

## The 8-Stage Compounding Lifecycle

```text
Real life
→ 1. Current Habits Baseline (Observational Scorecard)
→ 2. AI Baseline Analysis & Audit (Apply atomic-habits-skill)
   ↳ Local ephemeral computation occurs outside the vault
→ 3. Draft Proposed Experiment (Non-canonical in AI Workspace)
→ 4. Explicit Human Approval Gate
→ 5. Canonical Experiment Active (04 - Areas/Habits/Experiments/H###)
→ 6. Daily Tracking (Daily Habit Tracking & Tracking/)
→ 7. Weekly Diagnostic Reviews (AI draft in Workspace → Approved to Habits/Reviews/)
→ 8. Habit Graduation & Compounding (Merge into Current Habits, stack next experiment)
```

### Stage 1 — Baseline Observation (The Habits Scorecard)
- File: `04 - Areas/Habits/Current Habits.md`
- Procedure: User logs recurring behavioral routines without moralizing or character judgment.
- Columns: `Context or time | Cue | Observed behaviour | Immediate reward or need | Later effect | Assessment (helpful/neutral/harmful) | Notes`.

### Stage 2 — AI Baseline Audit & Analysis
- Files: `11 - Agents/Workspace/Habits/Current State Analysis.md` and `Atomic Habits Audit.md`
- Procedure:
  1. Read `Current Habits.md` and any active experiment notes.
  2. Invoke `atomic-habits-skill` to decompose routines into the 4-step loop (Cue → Craving → Response → Reward).
  3. Identify friction bottlenecks, cue unreliability, or natural anchor moments.
  4. Separate Evidence (facts), Interpretation (inferences), Hypotheses (unproven theories), and Confidence (qualitative: high/medium/low with rationale).

### Stage 3 — Propose a Single Low-Friction Experiment
- File: `11 - Agents/Workspace/Habits/Proposed Changes.md` or `11 - Agents/Workspace/Habits/Experiments/<slug>.md`
- Procedure:
  1. Propose **one** focused experiment (cognitive load is always 1).
  2. Ground it in the Four Laws: Make it Obvious (cue/habit stack), Attractive (craving/bundle), Easy (2-minute rule gateway), Satisfying (immediate reward/tracking).
  3. Enforce the Recovery Rule: *"Never miss twice."*
  4. Explicitly label the mechanism: `**Atomic Habits mechanism:** [e.g. Implementation Intention + 2-Minute Gateway]`.
  5. Keep non-canonical: **Do NOT assign an `H###` identifier.**

### Stage 4 — Explicit Human Approval Gate
- Rule: **No AI proposal is canonical truth until the user explicitly approves it.**
- Approval pattern: The user states approval and any desired modifications.
- Promotion actions:
  1. Create `04 - Areas/Habits/Experiments/H### <Title>.md` using `09 - Templates/Habit Experiment.md`.
  2. Assign the next sequential ID (`H001`, `H002`, etc.).
  3. Separate `approved_date` from `start_date`.
  4. **Preserve the proposal note intact** in `11 - Agents/Workspace/Habits/Experiments/` for historical provenance. Never delete or overwrite it.
  5. Log the promotion in `11 - Agents/Logs/Decisions and Corrections.md`.

### Stage 5 — Daily Tracking
- Hub: `04 - Areas/Habits/Daily Habit Tracking.md` and `04 - Areas/Habits/Tracking/`
- Procedure:
  - Track daily check-ins using markdown checklists or weekly tracking sheets.
  - Active experiments are automatically queried and surfaced via Dataview on `Active Habit Experiments.md`.
  - Focus on identity votes and 2-minute completions on low-energy days.
  - Any raw external app exports go to `08 - Attachments/Habit Exports/`.

### Stage 6 — Weekly Diagnostic Reviews
- Draft: `11 - Agents/Workspace/Habits/Reviews/YYYY-Www.md`
- Canonical: `04 - Areas/Habits/Reviews/YYYY-Www.md`
- Template: `09 - Templates/Habit Weekly Review.md`
- Procedure:
  1. Agent analyzes tracking data against the experiment target.
  2. Pinpoint **where the habit loop failed first** (Cue, Craving, Response, or Reward).
  3. Prescribe **one single system adjustment** (e.g. lowering friction, changing the cue) with its `Atomic Habits mechanism:`.
  4. Present draft to user.
  5. User approves → file promoted to `04 - Areas/Habits/Reviews/`. AI draft preserved.

### Stage 7 & 8 — Habit Graduation & Compounding
- When an experiment reaches consistency and automaticity (typically 3–8 weeks):
  1. Update experiment status: `phase: completed`, `result: successful`.
  2. **Graduate into Baseline**: Add the solidified routine as a permanent row in `04 - Areas/Habits/Current Habits.md` with note `Graduated from [[H###]]`.
  3. **Stack the Next Experiment**: The graduated habit now becomes the anchor cue for the next proposal (`H###+1`), enabling genuine compound growth.

## Core Rules and Boundaries

1. **No Hallucinated Promotion**: Never create or modify notes under `04 - Areas/Habits/` without explicit user confirmation.
2. **Proposal Preservation**: When promoting a proposal to canonical, keep the draft note in the workspace as an audit trail.
3. **No Vault Pollution**: Intermediate scripts, temporary JSON transformations, and app munging must stay in `$HOME/.taani-agent/workspaces/habits/`.
4. **Qualitative Confidence**: Distinguish facts from inferences; never use fake pseudo-mathematical confidence scores.
5. **No Moralizing**: Missed days are diagnostic data about system design, not character judgments.
