# Chapter 13: A Trace Without a Number

## Core Idea

The three-week support deadline forces Stoll to pursue a live trace through Tymnet, Pacific Bell, AT&T, Virginia, and federal authorities. The route narrows to a McLean, Virginia area number, but the investigators still lack the legal authority and technical certainty needed to identify the caller. The chapter makes the chain of custody visible: each operator can provide a different segment of the path, and a break in any segment stalls the whole result. Stoll's frustration is tempered by the recognition that a trace is a cooperative measurement, not a magic button.

## Frameworks Introduced

- Trace-chain coordination
- Deadline-driven investigation
- Technical uncertainty

## Key Concepts

- Tymnet
- 703 area code
- McLean
- Federal warrant
- Trace chain

## Mental Models

- The relay race
- A narrowing cone of uncertainty

## Anti-patterns

- Treat a network trace as a single vendor's responsibility
- Confuse a geographic region with a confirmed origin

## Worked Example

Stoll can obtain a near-live location because several organizations pass information quickly, but the number is not yet enough to support a search. The case therefore sits between engineering and law: the signal is real, while the action it might justify is constrained. The practical pattern is to label every handoff and its confidence rather than compressing the whole route into one unsupported claim.

## Key Takeaways

- Record who produced each segment of a trace.
- Track uncertainty at every handoff.
- Use deadlines to prioritize the next discriminating measurement, not to overstate confidence.

## Connects To

- Ch 22 — Phone Number
- Ch 24 — McLean Connection
- Ch 39 — FBI's Towel
