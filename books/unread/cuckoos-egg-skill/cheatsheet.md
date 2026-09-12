# Cheatsheet

## First response

| If you see | Decide |
|---|---|
| A small unexplained mismatch | Preserve it, reproduce it, and record what changes after a controlled test. |
| A login under a real user's name | Treat the name as a credential, not an identity. |
| Privileged program or account changes | Assume local logs and protections may be compromised; add independent observation. |
| A live alarm | Confirm the session before escalating. |

## Keep claims separate

1. **Route** — Where did the connection pass?
2. **Target** — What system or data did it touch?
3. **Access** — Was it a probe, successful login, privilege gain, or transfer?
4. **Identity** — Person, program, or still unknown?
5. **Motive** — What does the selection suggest, and what remains speculation?

## Choose the next measurement

- Need a longer session? Use a bounded, synthetic, plausible decoy.
- Need the caller's location? Coordinate network, carrier, telephone, and legal handoffs.
- Need campaign scope? Correlate historical bills, timestamps, accounts, and targets.
- Need to distinguish actors? Compare spelling, schedule, tools, errors, targets, and route behavior.
- Need to protect a safety-critical host? Containment outranks curiosity; do not wait for classified or monetary loss.

## Patch / observe trade-off

| Situation | Default judgment |
|---|---|
| Known production weakness, no unique evidence value | Patch and rotate credentials. |
| Compromised host is the only view of a wider campaign | Keep a narrowly bounded observation path only with approval, monitoring, and a stop condition. |
| Stepping-stone is shut down | Expect route migration; check adjacent systems and do not call it resolution. |
| Investigation is handed to police | Preserve the technical handoff, then harden the observed systems. |

## Fast tells

- Reused credentials across dormant accounts suggest one operator or a small group.
- Default maintenance accounts are high-impact doors.
- Repeated target keywords reveal interest, not automatically successful theft.
- A time-zone pattern is a location clue, not an identity.
- A common exploit can link systems without linking actors.
- A trustworthy logbook can be the difference between an anecdote and a case.
