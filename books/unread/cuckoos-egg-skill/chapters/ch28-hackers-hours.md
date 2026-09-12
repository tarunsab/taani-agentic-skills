# Chapter 28: The Hacker's Hours

## Core Idea

Stoll counts 135 sessions and separates weekday behavior from weekend behavior, finding a regular pattern: the hacker often works around midday in California time and begins much earlier on weekends. The schedule fits someone operating in a different time zone, particularly Europe, but it cannot by itself distinguish a person from a programmed process or a traveler. The timing becomes valuable because it helps coordinate scarce tracing resources and later supports the Germany hypothesis. A habit that looks incidental to the attacker becomes a measurable feature once Stoll records it consistently.

## Frameworks Introduced

- Temporal profiling
- Behavioral baseline
- Resource scheduling

## Key Concepts

- 135 sessions
- Weekday window
- Weekend window
- Time zone
- Session duration

## Mental Models

- Time as a location clue
- Routine as a fingerprint

## Anti-patterns

- Infer identity from work hours alone
- Collect timestamps without comparing weekdays and weekends

## Worked Example

The session count is more useful than a single late-night connection because it exposes a repeated schedule. Stoll compares the hours with likely local time abroad and combines the result with latency and German network traces. The chapter demonstrates a low-cost investigative tool: careful aggregation can turn a pile of logs into a profile.

## Key Takeaways

- Aggregate events before interpreting them.
- Compare behavior under different calendar conditions.
- Use timing to prioritize observation, not to claim identity.

## Connects To

- Ch 17 — Echo
- Ch 29 — Across the Atlantic
- Ch 33 — Closing Circle
