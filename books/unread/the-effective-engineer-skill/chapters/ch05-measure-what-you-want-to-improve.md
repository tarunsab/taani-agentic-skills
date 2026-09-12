# Chapter 5: Measure What You Want to Improve

## Core Idea

Metrics direct attention, shape incentives, reveal regressions, and make competing investments comparable. The right metric is not always the easiest number: Google search quality used long clicks rather than raw clicks, while performance work often needed tail latency such as P95 or P99 rather than an average. Changing the metric can change behavior, so hours, bugs fixed, registered users, or gross traffic may reward activity without improving the desired outcome. Lau recommends metrics that maximize impact, remain actionable and responsive, resist noise, and include the right denominator or cohort. Instrumentation should make the system visible end to end, from user conversion steps to latency layers and error rates. Data integrity is itself a high-leverage concern: missing events, inconsistent definitions, bot traffic, or broken pipelines can make a precise dashboard misleading.

## Frameworks Introduced

- **Behavioral metric selection**: Choose the measure that best represents the outcome users or the business actually value.
  - When to use: Define goals, compare variants, or detect regressions.
  - How: Ask what behavior the metric incentivizes, what it omits, and whether it is actionable.
- **Responsive and robust metrics**: Seek useful feedback quickly without mistaking noise for change.
  - When to use: Balance experimentation speed with decision confidence.
  - How: Pair a responsive leading metric with robust supporting measures.
- **Instrumentation as flight instruments**: Make important system states observable before operating at scale.
  - When to use: Launch, optimize, or operate a complex service.
  - How: Instrument the funnel, latency layers, errors, capacity, and user outcomes.
- **Metric integrity check**: Treat the measurement pipeline as a system that needs tests and cross-validation.
  - When to use: A metric changes unexpectedly or drives a consequential decision.
  - How: Inspect logs, definitions, event loss, alternate directions, and anomalous segments.

## Key Concepts

- **Long click**: Search behavior suggesting that a result satisfied the user for a meaningful period.
- **Tail latency**: High-percentile response time experienced by the slowest or most affected requests.
- **Vanity metric**: A large or impressive number that does not identify an actionable causal lever.
- **Ratcheting**: Repeatedly lowering a performance threshold as the system improves.
- **Economic denominator**: A ratio’s denominator that connects activity to a meaningful economic or user outcome.

## Mental Models

- Ask “What behavior will this number reward?” before setting a target.
- Use totals to understand scale, but use rates, cohorts, and distributions to understand change.
- Treat an unexplained metric anomaly as an investigation, not an instant success.

## Anti-patterns

- **Optimizing click-through alone**: More clicks can coexist with worse satisfaction or short visits.
- **Averages that hide tails**: A good mean can conceal severe latency for a vulnerable group.
- **Counting fixes**: Rewarding bugs fixed can incentivize easy bug creation rather than fewer defects.
- **Unverified dashboards**: A clean visualization cannot repair missing or inconsistent data.

## Worked Example

The book contrasts a raw search click with the longer visit that suggests the result was useful, and contrasts registered users with active or cohort-based behavior. It also cites a performance ratchet at Box: once a threshold improves, regressions past the new threshold are not accepted. In the HealthCare.gov example, instrumentation exposed slow loads and high error rates, allowing the team to reduce both rather than relying on launch impressions. These examples show that measurement is a decision system, not a reporting decoration. A metric must be interpreted with supporting measures and checked for data quality before it becomes an incentive.

## Limitations and Boundaries

Every metric is a proxy, so even a carefully chosen one can miss user value, long-term effects, or harms outside the measured surface. Correlation does not establish causality, and a statistically stable number can still be the wrong basis for a product decision. More instrumentation creates maintenance and privacy responsibilities that must be handled under current organizational policies. The source’s latency and scale figures are useful intuition for its era, not guarantees for today’s hardware or workloads.

## Practical Application

Write a metric contract before launching an experiment: desired behavior, primary outcome, denominator or cohort, guardrails, and data-quality checks. Inspect the distribution, not only the average, and pair a fast signal with a slower robust measure when the decision is consequential. Test a sample end to end from event generation through dashboard display, then investigate anomalies from more than one direction. After setting a target, review what behavior the target is actually producing.

## Key Takeaways

1. Pick metrics for the behavior and outcome you want.
2. Use rates, cohorts, distributions, and denominators where totals mislead.
3. Measure tail performance when users experience tail behavior.
4. Instrument before you need to debug or optimize.
5. Pair responsive signals with robust checks.
6. Test the integrity of the logging and analytics pipeline.

## Connects To

- Chapter 1 uses metrics to test whether leverage is real.
- Chapter 4 depends on dashboards, alerts, and rollback signals.
- Chapter 6 uses outcome metrics to evaluate experiments.
- Chapter 7 uses measurable milestones to replace vague status.
