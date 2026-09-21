export function knownSnapshot(overrides = {}) {
  return {
    schema_version: 1,
    as_of: "2027-03-01",
    currency: "GBP",
    household_members: ["Alex", "Sam"],
    income: [
      {
        id: "household-employment",
        label: "Household employment income",
        monthly_net: 8000,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Household confirmation",
      },
    ],
    assets: [
      {
        id: "joint-cash",
        label: "Joint cash",
        category: "cash",
        value: 30000,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "isa",
        label: "ISA",
        category: "investment",
        value: 70000,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "pensions",
        label: "Pensions",
        category: "pension",
        value: 120000,
        value_date: "2027-02-15",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "home",
        label: "Home",
        category: "property",
        value: 330000,
        value_date: "2027-01-15",
        valuation_date: "2027-01-15",
        valuation_method: "Comparable local sales",
        method: "Estimated from comparable sales",
        range_low: 310000,
        range_high: 350000,
        uncertainty_material: true,
        quality: "estimated",
        source: "Synthetic test fixture",
      },
      {
        id: "car",
        label: "Car",
        category: "vehicle",
        value: 20000,
        value_date: "2027-01-15",
        valuation_date: "2027-01-15",
        valuation_method: "Dealer listings",
        method: "Estimated from dealer listings",
        range_low: 18000,
        range_high: 22000,
        uncertainty_material: true,
        quality: "estimated",
        source: "Synthetic test fixture",
      },
    ],
    liabilities: [
      {
        id: "mortgage",
        label: "Mortgage",
        category: "mortgage",
        balance: 300000,
        interest_rate_percent: 4.5,
        monthly_payment: 1800,
        secured_asset_id: "home",
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "car-loan",
        label: "Car loan",
        category: "loan",
        balance: 15000,
        interest_rate_percent: 0,
        monthly_payment: 400,
        secured_asset_id: "car",
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "credit-card",
        label: "Credit card",
        category: "credit-card",
        balance: 6000,
        interest_rate_percent: 19.9,
        monthly_payment: 200,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
    ],
    recurring_flows: [
      {
        id: "fixed-costs",
        label: "Fixed household costs",
        direction: "expense",
        category: "fixed",
        amount_monthly: 2000,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
      {
        id: "variable-costs",
        label: "Variable household costs",
        direction: "expense",
        category: "variable",
        amount_monthly: 850,
        value_date: "2027-03-01",
        quality: "confirmed",
        source: "Synthetic test fixture",
      },
    ],
    overrides: [],
    ...overrides,
  };
}

export function renderSnapshotMarkdown(snapshot = knownSnapshot(), frontmatter = {}) {
  const metadata = {
    type: "financial-snapshot",
    schema_version: snapshot.schema_version,
    as_of: snapshot.as_of,
    currency: snapshot.currency,
    status: "draft",
    approved_by: [],
    ...frontmatter,
  };
  const approvalLines = metadata.approved_by.length
    ? `approved_by:\n${metadata.approved_by.map((name) => `  - ${name}`).join("\n")}`
    : "approved_by: []";
  return `---
type: ${metadata.type}
schema_version: ${metadata.schema_version}
as_of: ${metadata.as_of}
currency: ${metadata.currency}
status: ${metadata.status}
${approvalLines}
---
# Financial Snapshot

## Snapshot Data

\`\`\`finance-data
${JSON.stringify(snapshot, null, 2)}
\`\`\`
`;
}

export function renderReviewMarkdown({ asOf = "2027-03-01", approvedBy = ["Alex", "Sam"] } = {}) {
  return `---
type: financial-review
schema_version: 1
as_of: ${asOf}
status: approved
approved_by:
${approvedBy.map((name) => `  - ${name}`).join("\n")}
---
# Financial Review

This is the baseline checkpoint. No historical comparison exists.

## Open Decisions

- Confirm the next review date.
`;
}

export function renderGoalsMarkdown({ asOf = "2027-03-01", approvedBy = ["Alex", "Sam"] } = {}) {
  return `---
type: financial-goals
schema_version: 1
as_of: ${asOf}
status: approved
approved_by:
${approvedBy.map((name) => `  - ${name}`).join("\n")}
---
# Financial Goals

## Goals Data

\`\`\`finance-data
${JSON.stringify({
    schema_version: 1,
    as_of: asOf,
    goals: [
      {
        id: "maintain-buffer",
        goal: "Maintain the confirmed liquidity buffer",
        priority: "high",
        current_position: "Synthetic test fixture",
        target: "Synthetic test target",
        target_date: "2027-12-31",
        strategy: "Review quarterly",
        status: "on-track",
      },
    ],
  }, null, 2)}
\`\`\`
`;
}

export function renderAssessmentMarkdown({ asOf = "2027-03-01", approvedBy = ["Alex"] } = {}) {
  return `---
type: financial-assessment
schema_version: 1
as_of: ${asOf}
status: approved
approved_by:
${approvedBy.map((name) => `  - ${name}`).join("\n")}
---
# Financial Assessment

## Expert View

The household position is assessed against the approved Goals using the validated Snapshot metrics.

## Goal Alignment

- Maintain the confirmed liquidity buffer: on track.

## Priorities

1. Protect liquidity.
2. Address expensive debt before discretionary investing.

## Boundaries

This is decision support, not regulated financial advice.
`;
}

export function renderScenariosMarkdown({ asOf = "2027-03-01", approvedBy = ["Alex"] } = {}) {
  return `---
type: financial-scenarios
schema_version: 1
as_of: ${asOf}
status: approved
approved_by:
${approvedBy.map((name) => `  - ${name}`).join("\n")}
---
# Financial Scenarios

## Scenario: Accelerated debt repayment

- Question: What changes if £500 per month is redirected to expensive debt?
- Assumptions: Current income and recurring spending remain unchanged.
- Outcome: The scenario is retained with the checkpoint for later review.
- Recommendation: Compare the interest saved with the effect on liquidity before deciding.
`;
}

export function renderPolicyMarkdown({ approvedBy = ["Alex", "Sam"] } = {}) {
  return `---
type: financial-policy
schema_version: 1
status: approved
approved_by:
${approvedBy.map((name) => `  - ${name}`).join("\n")}
---
# Household Financial Policy

## Priorities

Synthetic test policy approved by the synthetic household.
`;
}
