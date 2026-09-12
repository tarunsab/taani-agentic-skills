# Chapter 7: The Physics Problem

## Core Idea

Dave and the district attorney help Stoll understand the evidence, while a phone technician explains that the visible login behavior is characteristic of AT&T Unix rather than Berkeley Unix. The chapter gives a compact account of password protection: Unix stores a one-way transformed value, so a verifier can test a candidate without retaining the original password. Stoll then describes his astronomer's discipline—record observations, use physical constraints, and label the difference between proof and speculation. This discipline keeps the investigation from collapsing into a story built from the first plausible trace.

## Frameworks Introduced

- Physics-style inference
- One-way password verification
- Proof versus speculation

## Key Concepts

- Encrypted password file
- Trapdoor transformation
- AT&T Unix
- Audit trail
- Physical constraint

## Mental Models

- The lab as an experiment
- Every trace as a measurement with error

## Anti-patterns

- Treat a plausible location as a proven identity
- Confuse password verification with recoverable plaintext

## Worked Example

The Oakland trace is useful because it narrows the path, but the software evidence still has to be interpreted carefully. Stoll records the exact behavior, asks what kinds of systems could produce it, and changes important passwords while the case continues. The chapter's method is portable: make an observation, list competing explanations, and use the next measurement to discriminate among them.

## Key Takeaways

- Write down what the evidence directly establishes.
- Use system behavior as a constraint on hypotheses.
- Change exposed credentials while preserving enough observation to continue safely.

## Connects To

- Ch 1 — Seventy-Five-Cent Mystery
- Ch 17 — Echo
- Ch 32 — Profile
