---
name: finance-checkpoint
description: Use when the user asks to run, prepare, update, compare, approve, seal, inspect, or review a Taivault household-finance checkpoint, Snapshot, Goals, expert financial assessment, scenario, Financial Policy, or Financial Dashboard.
---

# Finance Checkpoint

Run a low-admin household Finance checkpoint that moves through four clear stages: review the position, review Goals, give an expert-style assessment against those Goals, then optionally model scenarios or answer a specific financial question. Save approved outputs together as one integrity-verifiable checkpoint.

Preserve the boundary: LLMs interpret and advise, code validates and calculates, local Git remembers, and humans decide.

Requires Node.js 22 or newer, local Git, write access to Taivault, and a disposable workspace under `$HOME/.taani-agent/workspaces/finance/`.

## Fixed Boundaries

- Approved facts and checkpoint history: `02 - Taani/Finance/`
- Durable non-canonical reasoning: `11 - Agents/Workspace/Finance/`
- Deliberately retained, untouched source evidence: `08 - Attachments/Finance/`
- Drafts and processing: `$HOME/.taani-agent/workspaces/finance/`
- Deterministic helpers: this skill's `scripts/`

Never use the vault as scratch storage. Never invent a balance, convert `unknown` into `estimated`, silently alter approved Goals or Policy, overwrite a sealed checkpoint, configure a Finance remote, or present conversational arithmetic as authoritative.

Never persist full account or card numbers, credentials, passwords, API secrets, recovery codes, NI numbers, passport details, or security answers. Use human-readable account labels.

## Start Every Run

1. Read `11 - Agents/Workspace/Finance/State.md`, `Open Questions.md`, `Data Quality.md`, and `Decision Context.md` when present.
2. Run `finance-dashboard.mjs --no-write` against `02 - Taani/Finance/`. Stop if any sealed checkpoint fails its hashes or schema checks.
3. Resolve the latest integrity-valid approved checkpoint. For a first baseline, use the user-requested date or today's date; never substitute a configured future date.
4. Load the latest approved Goals and optional `02 - Taani/Finance/Financial Policy.md` when present.
5. Create the local run folder at `staging/<checkpoint-date>/`.

Read [references/checkpoint-format.md](references/checkpoint-format.md) whenever creating or editing checkpoint records or invoking a helper.

## The Four-Stage Journey

Run the stages in order unless the user explicitly requests a smaller bounded task. Keep the conversation moving: show useful output first, ask only for decisions or genuinely missing facts, and do not make the user reconstruct information they have already approved.

### Stage 1 — Review the Snapshot and Ask What Changed

Compare the supplied/current position with the latest approved Snapshot. Begin with a compact summary containing:

- current assets, liabilities, net worth, liquidity, debt service, and monthly surplus;
- material changes from the last checkpoint, or a clear baseline statement when none exists;
- stale, missing, contradictory, or unusually uncertain items;
- the short list of changes the user should confirm.

Ask one section at a time only when needed. State the previous value and ask what changed. If the user says a supplied checkpoint note is accurate, treat its stated facts as confirmed source input and do not re-grill them. Preserve approximation labels where the source itself is approximate.

Produce staged `Financial Snapshot.md` and `Financial Review.md`, then run `finance-validate.mjs` and `finance-calculate.mjs`. Use calculator JSON verbatim for totals and metrics.

### Stage 2 — Review Goals

Show the current approved Goals beside the validated position. For each Goal, state:

- current position;
- target and target date when present;
- progress or gap;
- whether the Goal still appears relevant;
- the proposed action: carry forward, revise, add, pause, complete, or remove.

Ask whether anything has changed. Carry unchanged approved Goals forward without making the user restate them. Never invent Goals. If no Goals exist, say so plainly and offer to define them; an explicitly empty Goals record is valid.

Save the result as staged `Financial Goals.md`. New or changed shared Goals require both household members' explicit approval. An empty Goals record or unchanged approved Goals must not create unnecessary policy questions.

### Stage 3 — Give an Expert Financial Assessment

After the Snapshot validates and Goals are reviewed, create `Financial Assessment.md`. Give a candid, financial-adviser-like opinion of the household position in relation to its Goals, while clearly remaining decision support rather than regulated advice.

The assessment must contain:

1. **Executive view** — the overall position in plain English.
2. **Goal alignment** — how the current position helps or hinders each Goal.
3. **Strengths** — what is working financially.
4. **Risks and constraints** — liquidity, leverage, expensive debt, concentration, cash-flow pressure, data uncertainty, or time-sensitive issues.
5. **Prioritised recommendations** — a short ordered list with rationale and trade-offs.
6. **Watch items and next review triggers** — what should cause an earlier checkpoint.
7. **Advice boundary** — where regulated financial, tax, legal, estate, pension, or mortgage advice may be warranted.

Tie every recommendation to the validated Snapshot, approved Goals, or clearly cited current rules. Separate fact, inference, assumption, and recommendation. Do not manufacture a Goal merely to make the assessment look complete.

When current tax, pension, mortgage, investment, or regulatory rules materially affect the assessment, research fresh official primary sources, cite them, and state the date checked.

### Stage 4 — Optional Scenarios and Specific Advice

After showing the Stage 3 assessment, ask once whether the user wants to model a scenario or ask a specific financial question before sealing. If not, proceed to approval without further admin.

Stage 4 is completely flexible and open-ended. It is not limited to canned formulas. The user and LLM work through *any* real-world decision, trade-off, or life event together (e.g. buying vs leasing an EV, parental leave, nursery fees, moving house, career breaks, contracting, or custom cash-flow projections).

When requested, create or extend staged `Financial Scenarios.md`. Keep all scenarios for that run in the same file. Each scenario must record:

- the user's question or decision;
- baseline facts taken from the Snapshot;
- explicit assumptions and adjustable inputs;
- transparent, reproducible calculations (using `scripts/finance-scenario.mjs` as an optional helper for common primitives like loan payments or compound growth where helpful, or showing clear step-by-step arithmetic for custom life events);
- outcomes and useful sensitivities;
- effects on each relevant Goal;
- trade-offs, risks, and uncertainties;
- an expert-style recommendation and its rationale;
- sources and date checked when current rules or products matter;
- the user's eventual decision, if one is made before sealing.

Stage 4 is optional, but any scenario or specific advice produced during the checkpoint must be saved with that date's checkpoint and included in its integrity manifest. Complete Stage 4 before sealing. Never append a scenario to an already sealed checkpoint; use a new out-of-cycle checkpoint or a separately approved linked decision record instead.

## Draft, Validate, and Review

The staging bundle contains:

```text
Financial Snapshot.md       required
Financial Review.md         required
Financial Goals.md          required
Financial Assessment.md     required
Financial Scenarios.md      optional; present only when Stage 4 is used
```

Keep Policy separate. `Financial Policy.md` is optional governance, not a prerequisite for saving a checkpoint. If the user asks to create or change Policy, stage the diff and obtain the required joint approval before updating it.

Before approval:

1. Resolve every validation blocker. “Finish anyway” permits a draft, never invented values or an invalid seal.
2. Use deterministic calculations for authoritative Snapshot metrics (`scripts/finance-calculate.mjs`), and clear, reproducible calculations for scenarios (using `scripts/finance-scenario.mjs` for standard building blocks where helpful).
3. Make the Review concise and exception-driven.
4. Show the Goals review and the complete Stage 3 assessment.
5. Offer Stage 4 once.
6. Show the exact files that will be sealed and a compact approval summary.

## Approval and Promotion

Ask for explicit approval only after Stages 1–3 and the Stage 4 choice are complete.

- Snapshot, Review, Assessment, and scenario recordkeeping may use the maintainer's approval.
- New or changed shared Goals, Policy, and major joint decisions require both household members' explicit approval.
- Record the appropriate approvers in each file's frontmatter and in the approval event supplied to `finance-seal.mjs`.

After approval:

1. Write an approved Policy to the canonical Finance root only when a Policy change was separately approved.
2. Change staged checkpoint records to `status: approved` and record their approvers.
3. Run `finance-seal.mjs`. New seals use manifest version 2, require the Assessment, include Scenarios when present, hash every checkpoint output, commit locally, and create a checkpoint tag.
4. Run `finance-dashboard.mjs --commit` to regenerate the dashboard from verified history.
5. Update the persistent Finance workspace only with unresolved questions, lasting decision context, or durable data-quality concerns.

## Quick Reference

| Situation | Action |
|---|---|
| User supplies an accurate approved position | Summarise it; do not re-question every value |
| Prior checkpoint exists | Lead with a compact change summary |
| Snapshot is valid | Review Goals, then produce the Assessment |
| User wants a scenario | Save it in `Financial Scenarios.md` before sealing |
| User declines Stage 4 | Move directly to final approval |
| No Policy exists | Continue; Policy is optional |
| Unknown or stale required value | Keep the checkpoint draft |
| Prior hash mismatch | Stop before relying on history |

## Common Mistakes

- Turning Stage 1 into a full interrogation after the user has approved the supplied facts.
- Stopping after Snapshot validation instead of reviewing Goals and giving the Stage 3 assessment.
- Giving generic advice that is not connected to the household's position and Goals.
- Leaving scenario advice only in chat instead of saving it with the checkpoint.
- Treating optional Policy work as a checkpoint blocker.
- Editing a sealed checkpoint to add a later scenario.
- Updating the dashboard by hand.

## Stop Conditions

Stop without promotion when validation blocks, approval is ambiguous, required joint approval for changed Goals or Policy is incomplete, an approved historical hash changes, the Finance repository has a remote, or the target date is already sealed. Report the exact blocker and preserve staged work.

## Final Report

Report the checkpoint date and status, Stage 1 changes and metrics, Stage 2 Goal decisions, the Stage 3 expert view, any Stage 4 scenarios, integrity result, local commit/tag, dashboard age, unresolved decisions, and retained evidence. Never claim an unsealed draft is current household truth.
