# Chapter 22: The Phone Number

## Core Idea

Martha uses Lexis to find the legal rule that a phone company can trace a call to a customer's own number without the kind of warrant Stoll had assumed was required. With help from a telephone technician, Stoll decodes the trace into the McLean, Virginia area and eventually reaches a modem associated with Mitre. The discovery does not prove that Mitre is the hacker's home; it establishes a plausible stepping-stone and a route that can be investigated. The chapter shows how a nontechnical contribution—legal research by a partner—can unlock a technical investigation stuck at an institutional boundary.

## Frameworks Introduced

- Legal-technical bridge
- Assumption checking
- Stepping-stone hypothesis

## Key Concepts

- Lexis
- 18 U.S.C. §3121
- McLean
- Mitre
- Modem

## Mental Models

- The overlooked rule
- A trace stops at a gateway, not necessarily a culprit

## Anti-patterns

- Assume the warrant requirement without checking
- Treat the first answering modem as the caller

## Worked Example

The legal discovery changes Stoll's mental model of what the telephone company can do, while the technician's decoding turns network identifiers into a geographic lead. Mitre answers the call, but the evidence still allows several explanations: the hacker could be there, could be using a stolen access path, or could be passing through. Stoll therefore moves to correlation and internal network tracing rather than declaring the case solved.

## Key Takeaways

- Ask what legal assumption is actually blocking the next measurement.
- Use domain experts to translate identifiers.
- Treat gateways as hypotheses about the route, not proof of origin.

## Connects To

- Ch 13 — Trace Without a Number
- Ch 23 — Mitre
- Ch 25 — Correlation
