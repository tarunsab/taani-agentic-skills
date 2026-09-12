# Chapter 31: The Noise

## Core Idea

The hacker returns through Germany, probes more military systems, reaches super-user on some hosts, and attempts to copy network programs and credentials. Stoll realizes the attacker is not tied to one route and uses a small source of deliberate noise to interfere with a transfer long enough to protect the observation. The intervention is tactical and limited: it buys time but does not eliminate the vulnerability or identify the person. The chapter also reinforces that a campaign can be broad in target count while remaining selective about what it copies.

## Frameworks Introduced

- Selective interference
- Route redundancy
- Target-versus-payload distinction

## Key Concepts

- Kermit transfer
- Noise
- Rlogin/telnet programs
- Milnet
- Alternate phone route

## Mental Models

- The observer's controlled perturbation
- A campaign with fallback paths

## Anti-patterns

- Assume the observed route is the only route
- Use an intervention that destroys the evidence you still need

## Worked Example

Stoll notices that the hacker is trying to take useful network software, not merely browse military names. He introduces noise through the observed connection to make the transfer less reliable, then watches for the attacker's response. When another telephone route appears, the disruption demonstrates both the value and the limit of local control.

## Key Takeaways

- Protect the highest-value artifact first.
- Make interventions reversible or measurable.
- Expect a persistent actor to have alternate paths.

## Connects To

- Ch 9 — Trojan Horse
- Ch 17 — Echo
- Ch 29 — Across the Atlantic
