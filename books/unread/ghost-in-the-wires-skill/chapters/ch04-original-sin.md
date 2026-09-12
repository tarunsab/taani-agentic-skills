# Chapter 3: Original Sin

## Core Idea

Mitnick’s first sustained information-gathering experiments target the California DMV and other institutional records. He discovers that a large organization can be navigated by learning its internal phone structure, vocabulary, escalation paths, and the assumptions employees make about callers. One of his recurring observations is that asking for sensitive data directly provokes suspicion, while presenting a nearly correct detail can invite the employee to correct it. The chapter also contains an early warning about overconfidence: a visit to UCLA ends with detention and the discovery of his equipment, even though the university does not file charges. Repeated escapes from immediate consequences convince him that he is “untouchable,” a belief that becomes more dangerous than any single technique.

## Frameworks Introduced

- **Institutional map**: Understand departments, phone routes, terminology, and authority relationships before assessing a request.
  - When to use: Defensively, when reviewing how an outsider could navigate a service organization.
  - How: Document the legitimate workflow, identify what is verified at each handoff, and remove assumptions that a caller already belongs.
- **Correction lure**: Offer a plausible but incorrect detail so the other person supplies the accurate one.
  - When to use: In awareness training as a recognizable social-engineering tell.
  - How: Treat unsolicited corrections of sensitive information as a trigger for independent verification.

## Key Concepts

- **Requester code**: A claimed authorization value used by an institution to control access.
- **Internal number**: A phone route whose apparent location can create false confidence.
- **Information reconnaissance**: Collecting organizational facts before making a sensitive request.
- **False invulnerability**: Belief formed when repeated risky behavior produces no immediate punishment.

## Mental Models

Use “trust transfer” to see how a caller borrows credibility from a department, title, or phone route. Use “near miss as evidence” in the opposite direction: an escape should trigger control improvement, not confidence that the system is safe.

## Anti-patterns

- **Treating internal routing as identity proof**: A caller can learn or imitate the route.
- **Using a lucky correction as validation**: A cooperative employee may be wrong, and a successful ruse may still be logged.
- **Reading non-prosecution as permission**: Institutional restraint does not authorize repetition.

## Worked Example

When a public-facing employee hints that law-enforcement requests use another number, Mitnick calls the police station and obtains that number by claiming to be another agency. He then uses an invented requester value and lets the employee correct it. The episode demonstrates a chain of small disclosures rather than one dramatic breach, and it gives defenders a concrete training scenario: every handoff needs independent verification.

## Key Takeaways

1. Map workflows from the defender’s perspective and remove implicit trust at handoffs.
2. Treat “almost right” claims about sensitive data as suspicious.
3. Never let repeated near misses become evidence that a risky activity is harmless.

## Connects To

- **ch05**: The same institutional trust enables physical access to COSMOS.
- **ch18**: Traffic analysis later turns scattered records into an organizational map.

