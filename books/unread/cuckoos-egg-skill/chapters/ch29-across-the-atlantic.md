# Chapter 29: Across the Atlantic

## Core Idea

Stoll separates weekday and weekend traces, searches network discussions for related incidents, and finally watches a live connection travel through an international carrier and satellite route. The path adds roughly six thousand miles and exposes the attacker probing CIA, ICBM, NORAD, White Sands, and many other military systems, often failing at default credentials but continuing methodically. Steve White explains that packet networks create virtual circuits whose identifiers change as the route crosses national systems, so the trace requires specialists who understand each layer. The chapter expands the investigation from a Berkeley incident into a global infrastructure problem without claiming that every scanned system was successfully compromised.

## Frameworks Introduced

- Layered network tracing
- Virtual-circuit reasoning
- Target-set analysis

## Key Concepts

- International carrier
- Westar satellite
- Virtual circuit
- NORAD
- White Sands

## Mental Models

- The route as a nested map
- Breadth of probing versus depth of compromise

## Anti-patterns

- Count every probe as a successful breach
- Assume one network identifier stays meaningful across carriers

## Worked Example

The live trace is compelling because it aligns route evidence, time-zone behavior, and the hacker's repeated military searches. Yet many targets reject the guessed credentials, so Stoll records the difference between trying a door and entering the building. Steve's explanation lets him follow the connection through international network layers rather than treating the satellite hop as the endpoint.

## Key Takeaways

- Trace each layer with the operator who understands it.
- Distinguish probing, access, privilege, and data retrieval.
- Use route changes as evidence about infrastructure, not automatically about people.

## Connects To

- Ch 30 — Germany
- Ch 31 — Noise
- Ch 42 — Net
