# Chapter 25: Correlation

## Core Idea

Stoll logs into Mitre's network and discovers that an internal menu can dial out to Berkeley and other systems without a separate password, making Mitre a plausible launch point. He then examines six months of outgoing phone bills and correlates calls with the times the hacker reached Anniston and other military targets. The result is a list of thousands of calls to defense contractors and bases, too broad to identify a caller but strong enough to show the scale of the stepping-stone's exposure. Correlation turns a confusing stream of traces into a network-level pattern while preserving the warning that correlation is not causation.

## Frameworks Introduced

- Correlation analysis
- Stepping-stone detection
- Historical baseline

## Key Concepts

- Mitre outgoing modems
- UUCP
- Phone bills
- Call correlation
- Defense contractors

## Mental Models

- The bill as a retrospective sensor
- Many weak matches become a pattern

## Anti-patterns

- Treat every correlated call as an attack
- Ignore ordinary infrastructure because it looks administrative

## Worked Example

The Mitre menu and outgoing modem access explain how a remote intruder could enter one system and leave through another. Stoll compares timestamps and destinations rather than searching for a single suspicious number. The phone bills cannot tell him who paid or who typed, but they reveal that a security incident may be distributed across a service provider's ordinary operations.

## Key Takeaways

- Build a time-aligned baseline before labeling anomalies.
- Use historical records to map infrastructure relationships.
- State what correlation can and cannot establish.

## Connects To

- Ch 26 — Trail on the Bill
- Ch 29 — Across the Atlantic
- Ch 44 — Network's Shoemakers
