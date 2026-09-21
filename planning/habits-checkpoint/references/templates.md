# Habits Workspace Templates & Schemas

Canonical templates for use across Markdown vaults.

## 1. Habit Experiment Template (`09 - Templates/Habit Experiment.md`)

```markdown
---
parent: "[[04 - Areas/Habits/Active Habit Experiments|Active Habit Experiments]]"
type: habit-experiment
experiment_id: "H###"
phase: active
approved_date: YYYY-MM-DD
start_date: YYYY-MM-DD
review_date: YYYY-MM-DD
result:
tags:
  - habits
  - experiment
---
# {{Experiment title}}

## Origin and Promotion
- Proposal: [[11 - Agents/Workspace/Habits/Experiments/{{proposal-slug}}|{{proposal-title}}]]
- Approval decision: [[11 - Agents/Logs/Decisions and Corrections#{{Anchor}}|Promotion Decision]]
- Changes from proposal:

## Identity and Outcome
- Identity I am reinforcing:
- Desired outcome:
- Identity area:

## Behaviour
- Observable behaviour:
- Frequency or target:
- Cue:
- Implementation intention or habit stack:
- Craving or expected benefit:
- Two-minute version:

## Four Laws and Environment
### Make it obvious
### Make it attractive
### Make it easy
### Make it satisfying

**Atomic Habits mechanism:**

## Tracking and Recovery
- Tracking method:
- Recovery rule: If I miss once, I return at the next available opportunity; I do not let one miss become a new pattern.

## Review
- Review date:
- Evidence:
- Result:
- Next decision:
```

## 2. Habit Weekly Review Template (`09 - Templates/Habit Weekly Review.md`)

```markdown
---
parent: "[[04 - Areas/Habits/00 - Habits Index|Habits Index]]"
tags:
  - habits
  - review
week: YYYY-Www
date: YYYY-MM-DD
source_app:
export_start:
export_end:
---
# Habit Review — {{YYYY-Www}}

## Evidence
Link to active experiment notes under `04 - Areas/Habits/Experiments/`, daily tracking data from [[04 - Areas/Habits/Daily Habit Tracking|Daily Habit Tracking]], and any intentionally retained raw source evidence. Do not copy large source sections into this review.

## What Repeated

## Where the Habit Loop Failed First
- Cue:
- Craving:
- Response:
- Reward:

## Interpretation

## One System Adjustment
**Atomic Habits mechanism:**

## Next Experiment or Adjustment

## Recovery After Lapses

## Confidence
- Level: high / medium / low
- Why:
```

## 3. Daily Habit Tracking Note (`04 - Areas/Habits/Daily Habit Tracking.md`)

```markdown
---
parent: "[[04 - Areas/Habits/00 - Habits Index|Habits Index]]"
tags:
  - habits
  - tracking
  - dashboard
---
# Daily Habit Tracking

Central tracking scratchpad for all active habit experiments. Record daily check-ins here. At the end of each review cycle, the AI archives this data into `04 - Areas/Habits/Reviews/` and prepares this tracker for the next period.

## Active Habits to Track Today

```dataview
TABLE experiment_id, phase, start_date, review_date
FROM "04 - Areas/Habits/Experiments"
WHERE phase = "active"
SORT review_date ASC
```

## Daily Check-In Grid

> [!TIP] The Two-Minute Rule & Never Miss Twice
> If time or energy is low, do the two-minute gateway version to cast a vote for your identity. If you miss a day, treat it as friction data and prioritize showing up the next day. Never miss twice.

| Active Habit | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Total | Notes / Friction Observed |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
|  | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | 0/7 |  |
```
