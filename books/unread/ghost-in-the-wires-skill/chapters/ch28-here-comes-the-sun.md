# Chapter 27: Here Comes the Sun

## Core Idea

At the Denver law firm, Mitnick uses legitimate job duties to learn the organization’s systems while maintaining unauthorized activity in parallel. His work includes operations, scripts, administration, Internet connectivity, and two-factor authentication, so he understands both the controls and the surrounding workflows. He also turns the firm’s phone-billing system into an early-warning mechanism for calls to law-enforcement offices, illustrating how a trusted internal role can be repurposed for personal surveillance. The chapter contains a telling reciprocal moment: Mitnick catches a coworker looking at payroll, but recognizes that he can object only because he was watching the coworker. The practical lesson is to separate administrative access, monitoring, and personal curiosity through least privilege and independent review.

## Frameworks Introduced

- **Role-to-access drift**: Legitimate job access gradually becomes a platform for unrelated observation or control.
  - When to use: In insider-risk and privileged-access reviews.
  - How: Scope duties, log use, review unusual queries, and remove access when the role changes.
- **Monitoring reciprocity**: A watcher may also be watched, creating a conflict when monitoring is personal.
  - When to use: When administrators can inspect others’ activity.
  - How: Use transparent policies, separation of duties, and audit review.

## Key Concepts

- **SecurID**: A two-factor authentication product used at the firm.
- **Early-warning script**: A script that alerts on calls to selected numbers.
- **Privileged access**: Access granted because of a job role.
- **Least privilege**: Give only the access required for current duties.

## Mental Models

Use “legitimate role, illegitimate purpose” as a core insider-risk test. Treat monitoring capability as a sensitive privilege that needs oversight of the monitor itself.

## Anti-patterns

- **Assuming authorized access means authorized use**.
- **Letting one administrator control access, logs, and review**.
- **Using a security tool as a private alarm system**.

## Worked Example

Mitnick’s responsibility for telephone billing lets him write a script that pages him when calls reach FBI or U.S. Attorney offices. He later sees a coworker viewing payroll and notices the irony that his own surveillance made the discovery possible. A defensible design would restrict query scope, alert on unusual access, and have an independent reviewer inspect both users.

## Key Takeaways

1. Review purpose and context, not only whether access was technically allowed.
2. Separate administration from monitoring and audit.
3. Apply least privilege to information about employees as well as systems.

## Connects To

- **ch23**: Early-warning systems become central to Mitnick’s response.
- **ch29**: Internal access enables trophy-oriented source-code hunting.

