# Patterns

These patterns translate the memoir’s recurring mechanisms into lawful defensive practice.

## Verify the caller, not the story

**When to use**: Any unusual request involving access, records, money, code, or account recovery.

**How**: Pause the request, use a known contact route, confirm role and necessity independently, and require a second approver for high-impact actions. Record the decision.

**Trade-offs**: Adds time and friction, but preserves helpful service while reducing the value of confidence, urgency, and jargon.

## Break the information chain

**When to use**: Processes that ask one institution to vouch for another, or that expose sensitive details through several desks.

**How**: Minimize each handoff, give each team only what it needs, validate the requester at every boundary, and detect circular confirmation.

**Trade-offs**: More independent checks can slow onboarding; the benefit is that one plausible story cannot travel unchallenged through the whole organization.

## Correction-lure defense

**When to use**: A caller or visitor points out a small error and offers a seemingly easy fix.

**How**: Treat the correction as a new request. Verify through a trusted channel, avoid reading back internal details, and route changes through the normal workflow.

**Trade-offs**: Some harmless corrections take longer, but the process stops “helpfulness” from becoming disclosure.

## Identity-graph check

**When to use**: Enrollment, account recovery, privilege elevation, employment, licensing, or vendor access.

**How**: Compare independent records across time and context; prefer evidence that was not supplied by the claimant. Recheck after material changes.

**Trade-offs**: Privacy and fairness require data minimization and clear appeal paths. More records are not automatically better if they are copies of one source.

## Traffic-analysis review

**When to use**: A breach or insider-risk investigation where content is unavailable or inappropriate to collect.

**How**: Examine timing, direction, frequency, duration, storage anomalies, and device relationships under proper authority. State confidence, dependencies, and stopping conditions.

**Trade-offs**: Metadata can be revealing and misleading. Limit retention and access, and never treat correlation alone as attribution.

## Early-warning tripwire

**When to use**: A dormant account changes, a familiar access path disappears, an unexpected device appears, or a public story reveals new attention.

**How**: Define alerts, severity thresholds, an independent reviewer, evidence preservation, and response owners before an incident. Use the loop: alert, assess, act.

**Trade-offs**: Too many alerts create fatigue; too few allow a real investigation to mature unseen.

## Layered authorized assessment

**When to use**: Reviewing a system whose risk crosses physical, human, identity, and technical layers.

**How**: Obtain written permission, map the full chain, test one boundary at a time in controlled conditions, protect data, and stop at the agreed limit. Report the weakness and remediation rather than operationalizing the path.

**Trade-offs**: Requires coordination across owners, but it catches failures that a purely technical scan misses.

## Scope-and-stop rule

**When to use**: Penetration testing, red teaming, research, demonstrations, or evidence collection.

**How**: Write systems, accounts, dates, techniques, data rules, contacts, and stop triggers. Establish a rapid way for the owner to pause the work.

**Trade-offs**: A narrow scope may miss a risk, so expand only through explicit approval; the alternative is ambiguity about authorization.

## Trophy-motive threat model

**When to use**: Protecting famous researchers, source repositories, rare datasets, or systems that represent a public challenge.

**How**: Identify symbolic assets, separate them from ordinary accounts, monitor for unusual persistence, and limit knowledge of high-value paths.

**Trade-offs**: Extra controls cost convenience. The memoir suggests that prestige can motivate effort even when money is absent.

## Facts-versus-myth ledger

**When to use**: A security incident is receiving press attention or internal retelling.

**How**: Keep separate fields for direct evidence, witness account, inference, allegation, legal finding, and public claim. Update provenance and uncertainty as facts change.

**Trade-offs**: The ledger feels slower than a simple narrative, but it prevents repetition from becoming false certainty.

## Legacy trust-boundary audit

**When to use**: Old services, implicit host trust, shared accounts, or inherited configurations remain in production.

**How**: Inventory trust relationships, replace location-based assumptions with authentication, reduce privilege, isolate legacy components, and set a retirement date.

**Trade-offs**: Migration may disrupt old workflows; compensating controls should be explicit and temporary rather than silently permanent.

## Capability-to-authorization conversion

**When to use**: Turning deep technical experience into a legitimate security role.

**How**: Pair capability with owner permission, a written scope, evidence handling, a reportable method, and accountability. Explain feasibility without overstating occurrence.

**Trade-offs**: Authorized work is less improvisational, but that constraint is what makes expertise safe and useful.
