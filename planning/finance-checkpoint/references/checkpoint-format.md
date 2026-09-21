# Finance Checkpoint Format

Read this reference only while preparing checkpoint files or running the helpers.

## Runtime Paths

Resolve the vault root dynamically:

```bash
VAULT_ROOT="$(git rev-parse --show-toplevel)"
SKILL_ROOT="$VAULT_ROOT/11 - Agents/Workflows/finance-checkpoint"
FINANCE_ROOT="$VAULT_ROOT/02 - Taani/Finance"
WORK_ROOT="$HOME/.taani-agent/workspaces/finance"
CHECKPOINT_DATE="2026-09-21"
```

The local workspace contains `scratch/`, `tmp/`, `cache/`, `raw-processing/`, `staging/`, and `logs/`. Deleting it must not delete approved history, persistent reasoning, retained evidence, or reusable code.

## Canonical Frontmatter

Snapshot:

```yaml
---
type: financial-snapshot
schema_version: 1
as_of: 2027-03-01
currency: GBP
status: draft
approved_by: []
---
```

Review, Goals, Assessment, and optional Scenarios use the same `schema_version`, `as_of`, `status`, and `approved_by`, with these types:

| File | Type | Required |
|---|---|---|
| `Financial Snapshot.md` | `financial-snapshot` | yes |
| `Financial Review.md` | `financial-review` | yes |
| `Financial Goals.md` | `financial-goals` | yes |
| `Financial Assessment.md` | `financial-assessment` | yes |
| `Financial Scenarios.md` | `financial-scenarios` | only when Stage 4 is used |

Policy uses `type: financial-policy`, `schema_version`, `status`, and `approved_by` but is not checkpoint-dated. Policy is optional and is not part of the checkpoint bundle unless separately changed and approved.

## Snapshot Data

Place exactly one JSON object in a `finance-data` fence under `## Snapshot Data`. The schema source is [snapshot-schema-v1.json](snapshot-schema-v1.json).

Collections and money fields:

| Collection | Money field | Required item context |
|---|---|---|
| `income` | `monthly_net` | `id`, `label`, `value_date`, `quality`, `source` |
| `assets` | `value` | context plus `category` |
| `liabilities` | `balance` | context plus `category`, `interest_rate_percent`, `monthly_payment` |
| `recurring_flows` | `amount_monthly` | context plus `direction` and `category` |

Allowed quality values are `confirmed`, `estimated`, `stale`, and `unknown`. Use `null` for the money field and `value_date` of an unknown record. An estimated asset also needs `valuation_date`, `valuation_method`, `method`, and—when uncertainty is material—`range_low`, `range_high`, and `uncertainty_material: true`.

Explicit overrides live in the top-level `overrides` array and record `id`, `item_id`, `reason`, `approved_by`, and `approved_at`. They stay visible but do not suppress unknown/stale seal blockers.

## Goals Data

Place exactly one `finance-data` JSON object under `## Goals Data` with `schema_version`, `as_of`, and `goals`. Each goal contains:

```json
{
  "id": "stable-id",
  "goal": "Human-approved outcome",
  "priority": "high",
  "current_position": "Confirmed current position",
  "target": "Human-approved target",
  "target_date": "2027-12-31",
  "strategy": "Approved intended strategy",
  "status": "on-track"
}
```

Never fill this example with invented household content.

## Review Format

`Financial Review.md` is the compact Stage 1 output. Use these sections when relevant:

- `## Position Summary`
- `## Changes Since Previous Checkpoint`
- `## Data Quality`
- `## Risks and Exceptions`
- `## Open Decisions`

For a first checkpoint, state that it is the baseline and that no historical comparison exists. If the user approves a supplied position note as accurate, do not leave reconfirmation questions for every pasted value.

## Assessment Format

`Financial Assessment.md` is the required Stage 3 output. It is human-readable Markdown and must contain:

- `## Executive View`
- `## Goal Alignment`
- `## Strengths`
- `## Risks and Constraints`
- `## Prioritised Recommendations`
- `## Watch Items and Review Triggers`
- `## Advice Boundary`

Every material conclusion must be traceable to Snapshot metrics, approved Goals, or clearly cited current rules. Mark assumptions and inferences explicitly.

## Scenario Format

Create `Financial Scenarios.md` only when Stage 4 is used. Put every scenario from the run in that one file.

Stage 4 is a flexible, open-ended conversational canvas between the user and LLM. It is not limited to canned formulas. Any life decision, major purchase, career transition, family event, or trade-off can be explored (e.g. buying vs leasing, nursery fees, parental leave, career breaks, contracting vs permanent, property moves, or custom multi-variable projections).

For each scenario, record:

- question or decision;
- baseline facts;
- assumptions and adjustable inputs;
- calculations and outcomes (show transparent step-by-step arithmetic directly in the note, using `finance-scenario.mjs` as an optional helper for common building blocks where helpful);
- sensitivities;
- effect on Goals;
- trade-offs and risks;
- recommendation and rationale;
- sources and date checked when current rules matter;
- decision, if made before sealing.

Complete the scenario file before sealing. A sealed checkpoint is append-only.

## Manifest Versions

- Manifest version 1 checkpoints contain Snapshot, Review, and Goals and remain verifiable for backward compatibility.
- New seals use manifest version 2, which also requires Assessment and hashes optional Scenarios when present.

## Helper Commands

Validate a draft or an approved seal candidate:

```bash
node "$SKILL_ROOT/scripts/finance-validate.mjs" \
  --snapshot "$WORK_ROOT/staging/$CHECKPOINT_DATE/Financial Snapshot.md" \
  --mode draft
```

Calculate authoritative metrics:

```bash
node "$SKILL_ROOT/scripts/finance-calculate.mjs" \
  --snapshot "$WORK_ROOT/staging/$CHECKPOINT_DATE/Financial Snapshot.md"
```

Optional Stage 4 scenario math helpers (for common primitives; custom scenarios can be computed directly in the note):

```bash
# Overpay debt vs invest in ISA/index funds:
node "$SKILL_ROOT/scripts/finance-scenario.mjs" \
  --type overpay-vs-invest --debt-balance 200000 --debt-rate 4.5 --monthly 500 --years 10 --investment-return 7

# Mortgage fixed-rate expiration shock:
node "$SKILL_ROOT/scripts/finance-scenario.mjs" \
  --type mortgage-shock --balance 250000 --term-months 300 --current-rate 2.5 --new-rate 5.5

# Emergency runway and income reduction stress-test:
node "$SKILL_ROOT/scripts/finance-scenario.mjs" \
  --type runway-shock --liquid-assets 50000 --monthly-income 7750 --income-reduction 25 --fixed-costs 2000 --debt-service 2400 --duration 6

# Compound investment accumulation:
node "$SKILL_ROOT/scripts/finance-scenario.mjs" \
  --type compound-growth --principal 10000 --monthly 500 --years 10 --return 7
```

Integrity preflight and dashboard dry run:

```bash
node "$SKILL_ROOT/scripts/finance-dashboard.mjs" \
  --finance-root "$FINANCE_ROOT" \
  --no-write
```

Seal only after the user explicitly approves the exact staged records:

```bash
node "$SKILL_ROOT/scripts/finance-seal.mjs" \
  --staging "$WORK_ROOT/staging/$CHECKPOINT_DATE" \
  --finance-root "$FINANCE_ROOT" \
  --approved-by "PrimaryApprover" \
  --approved-at "2026-09-21T12:00:00Z"
```

Regenerate and locally commit the dashboard:

```bash
node "$SKILL_ROOT/scripts/finance-dashboard.mjs" \
  --finance-root "$FINANCE_ROOT" \
  --commit
```

Use the actual checkpoint date, approval names, and approval timestamp. Do not copy example approvals into a live run.
