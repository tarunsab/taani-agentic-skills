# Patterns

These patterns translate the book’s frameworks into repeatable operating moves. They are heuristics, not substitutes for project-specific evidence.

## Run a leverage audit

**When to use:** A team has many plausible tasks and limited time. **How:** Name the goal, list the recurring cost or downstream reach of each candidate, and ask whether the work reduces time, increases output, or moves to a higher-leverage activity. Prefer investments whose benefit reaches future tasks or other people, then check the result with an outcome metric. **Trade-offs:** Long-horizon work may be harder to prove and can crowd out immediate delivery, while a fast task may be necessary even when it does not compound.

## Keep one backlog and a small WIP limit

**When to use:** Commitments are scattered or many projects are half-started. **How:** Capture work in one trusted backlog, select a small current set, and serialize projects where possible. Review daily for the next action, weekly for stale commitments, and monthly for direction; protect maker blocks from avoidable interruptions. **Trade-offs:** Some parallelism is necessary for dependencies or team capacity, but visible WIP makes the switching cost explicit.

## Build a tight delivery loop

**When to use:** A change takes too long to compile, test, deploy, observe, or reverse. **How:** Shrink batches, run checks in parallel, use canaries and dashboards, and make rollback routine. For debugging, create the smallest reproducible state and automate repeated setup after the workflow proves recurring. **Trade-offs:** The loop requires investment in tests, observability, and release discipline; speed without safeguards increases blast radius.

## Write a metric contract

**When to use:** A team is about to set a target or compare alternatives. **How:** Define the desired behavior, primary metric, denominator or cohort, supporting guardrails, and data-quality checks before optimizing. Pair a responsive signal with a robust one, and use distributions when averages hide the tail. **Trade-offs:** More instrumentation adds work, but a wrong metric can direct much more work toward the wrong outcome.

## Validate the riskiest assumption first

**When to use:** A project has uncertain demand, architecture, performance, or usability. **How:** State a hypothesis and what would count as good, bad, or inconclusive evidence, then choose a prototype, fake door, interview, staged rollout, or A/B test that can change the decision cheaply. Stop or redirect when evidence rejects the premise. **Trade-offs:** Early experiments can be noisy or unrepresentative, so match method and scale to the decision rather than overgeneralizing.

## Estimate with ranges and milestones

**When to use:** A project is novel, cross-team, or vulnerable to integration risk. **How:** Decompose work, include coordination and interruptions, give confidence ranges, and define a concrete goal with measurable milestones. Move high-variance unknowns and end-to-end scaffolding early, then revise the plan from actuals. **Trade-offs:** Ranges can feel less decisive than a date, but false precision hides scope choices and makes slippage arrive later.

## Use a pragmatic quality budget

**When to use:** Quality work competes with learning speed or feature delivery. **How:** Raise review, testing, and abstraction investment where failure is costly, code is central, or reuse is proven. Add a focused regression test before changing fragile behavior and pay technical-debt interest in high-churn areas. **Trade-offs:** Under-investment creates compounding friction, while blanket perfectionism delays useful evidence and can overfit an immature design.

## Make operations simple, loud, and retryable

**When to use:** A service has recurring manual work or difficult incidents. **How:** Remove unnecessary technologies, validate inputs and invariants, automate mechanics, and design batches to be idempotent or reentrant. Maintain recovery playbooks and rehearse important failure modes. **Trade-offs:** Simplicity may defer capability and automation can amplify mistakes, so preserve human decision points and safeguards.

## Multiply the team

**When to use:** An individual owner, slow onboarding path, or hiring bottleneck limits team capacity. **How:** Improve high-signal hiring, give new hires a mentor and a small shippable starter task, rotate ownership, document decisions, and review code across boundaries. Measure whether people ramp, operate, and make decisions without the original owner. **Trade-offs:** Teaching and interviewing consume immediate time, but the return compounds through team output and personal freedom from bottlenecks.

## Turn failures into collective wisdom

**When to use:** An outage, launch, or project contains lessons that should outlive the participants. **How:** Hold a blameless debrief, reconstruct evidence, use Five Whys to seek root causes, choose prevention or recovery actions, and publish the runbook or lesson. Revisit whether the project met its goal and metric, not just whether it launched. **Trade-offs:** Reflection is emotionally and calendar-expensive, but skipping it repeats mistakes and loses knowledge when people move teams.

