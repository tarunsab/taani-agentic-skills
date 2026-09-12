# Chapter 20: The Elxsi Trap

## Core Idea

Stoll finds the hacker searching LBL accounting for “Pink Floyd,” which rules out the related Stanford intruder who used a different spelling and reinforces the value of small signatures. The hacker then reaches an Elxsi computer through an open, privileged UUCP account, adds an account, and measures the machine's capabilities. Stoll turns the Elxsi connection into a controlled observation by slowing it enough to keep the session visible and builds a pager so he can respond away from the switchyard. The chapter combines attribution by behavior with a practical lesson in instrumenting a live system without claiming more control than one actually has.

## Frameworks Introduced

- Behavioral fingerprinting
- Controlled slowdown
- Alerting for mobility

## Key Concepts

- Elxsi
- UUCP
- 32-bit system
- 10 MIPS
- Pager

## Mental Models

- The trap as a speed governor
- A remote pager extends the observer

## Anti-patterns

- Assume similar incidents have the same operator
- Let an alert exist without a response path

## Worked Example

The accounting search gives Stoll a clean comparison with Stanford, while the Elxsi account demonstrates the intruder's willingness to exploit trust relationships outside the original Unix cluster. Slowing the session is not presented as a universal defense; it is a temporary way to preserve observation time. The pager solves the human problem around the technical system by allowing Stoll to act when he is not physically beside the monitor.

## Key Takeaways

- Use distinctive behavior to separate similar cases.
- Choose interventions that increase observation without destroying the signal.
- Pair automated alerts with an operator who can interpret them.

## Connects To

- Ch 9 — Trojan Horse
- Ch 27 — Fox and Hound
- Ch 31 — Noise
