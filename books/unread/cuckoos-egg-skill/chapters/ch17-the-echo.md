# Chapter 17: The Echo

## Core Idea

Stoll uses the timing of an acknowledgement to estimate how far away the intruder might be, borrowing an astronomical technique for a network measurement. His first calculation is wrong because intermediate network nodes add delay, but comparisons across routes eventually make a distance of roughly six thousand miles plausible. The important result is methodological: a timestamp can be useful only when the system's internal delays and routing behavior are modeled. The echo does not identify a person, yet it challenges the earlier Oakland and Virginia stories and supports the possibility of an international path.

## Frameworks Introduced

- Round-trip timing
- Calibration by comparison
- Modeling intermediate delay

## Key Concepts

- Acknowledgement timing
- Network node delay
- Six-thousand-mile estimate
- Route comparison
- Distance inference

## Mental Models

- The network as a telescope
- Measurement error as part of the signal

## Anti-patterns

- Convert latency directly into geographic distance
- Discard a useful method because its first estimate is wrong

## Worked Example

Stoll compares a known or plausible route with the suspicious route rather than trusting one raw delay. The first moon-like estimate fails when node processing time is included, and the correction is itself evidence about the network. This is a model-repair example: the measurement survives, but the simplistic interpretation does not.

## Key Takeaways

- Calibrate timing with comparison routes.
- Name hidden delays before converting time into distance.
- Use wrong estimates to improve the model rather than to defend the conclusion.

## Connects To

- Ch 7 — Physics Problem
- Ch 29 — Across the Atlantic
- Ch 31 — Noise
