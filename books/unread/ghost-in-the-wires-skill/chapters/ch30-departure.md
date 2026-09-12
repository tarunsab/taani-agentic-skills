# Chapter 29: Departure

## Core Idea

Mitnick discovers that a Colorado Supernet administrator has found logs linking Novell activity to his accounts and has shared them with the FBI. He tries to redirect the investigation with a bogus log, but the discovery convinces him that Denver is no longer safe. The chapter explains why his concealment strategy depends on watching administrators, storage systems, and outside contacts at the same time; any one of those channels can expose the pattern. It also records a law-enforcement meeting in which companies struggle to explain why someone would collect source code if not for profit, reinforcing the memoir’s criticism of a narrow threat model. Departure is therefore both a tactical move and a reminder that hiding creates a continual workload that eventually fails.

## Frameworks Introduced

- **Cover-compromise threshold**: Leave when independent evidence shows the surrounding system has connected the activity to the person.
  - When to use: Defensively, to define incident-severity escalation.
  - How: Correlate logs, identity clues, and human reports; do not wait for a single conclusive artifact.
- **Red-herring response**: Attempt to misdirect an investigation after detection.
  - When to use: As an incident-response threat model, not a recommended practice.
  - How: Preserve originals, detect altered records, and restrict who can create or modify logs.

## Key Concepts

- **Colorado Supernet**: The Denver network Mitnick uses for storage and access.
- **Login record**: Metadata tying an account to time and source.
- **Red herring**: Misleading information intended to redirect attention.
- **Threat model**: An explanation of who might act, why, and how.

## Mental Models

Use “independent hints compound”: a log, a source network, and a suspicious account can be decisive together. Think of concealment as a system with growing maintenance cost.

## Anti-patterns

- **Allowing users to alter the logs used to investigate them**.
- **Assuming no financial motive means no serious threat**.
- **Waiting for proof from one source before acting on converging evidence**.

## Worked Example

An administrator shares login records showing activity from Novell’s network and Colorado Supernet. Mitnick notices the email, confirms the recipient is an FBI agent, and sends a misleading log. The episode demonstrates why immutable logs, independent collection, and correlation across systems are essential.

## Key Takeaways

1. Define compromise thresholds from multiple signals.
2. Protect logs from the subjects they describe.
3. Model nonfinancial motives explicitly.

## Connects To

- **ch28**: Monitoring of source-code activity exposes the trophy hunt.
- **ch31**: A vulnerable cover leads to a sudden decision at lunch.

