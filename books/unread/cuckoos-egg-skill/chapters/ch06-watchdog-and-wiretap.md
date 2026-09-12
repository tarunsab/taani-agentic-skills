# Chapter 6: The Watchdog and the Wiretap

## Core Idea

Stoll's home life makes clear that the investigation is consuming more than work hours, while the technical work becomes more systematic. He builds a one-way watchdog on Unix-8 to scan other LBL machines for suspicious accounts and uses printers to observe several Tymnet lines. The intruder again takes Sventek, attempts to reach Unix-8, reads the password file, and logs out; Ron traces the activity toward an Oakland modem. Stoll learns that a remote trace is both a technical and legal operation, because the next step may require a telephone warrant.

## Frameworks Introduced

- Watchdog architecture
- Independent observation
- Technical-legal handoff

## Key Concepts

- Unix-8 moat
- Password file
- Tymnet
- Oakland modem
- Telephone warrant

## Mental Models

- A small trusted island
- The trace as a relay race

## Anti-patterns

- Put the monitor on the same host and trust its logs completely
- Treat legal process as someone else's technical problem

## Worked Example

The watchdog is deliberately one-way: the observation machine looks outward rather than becoming another place the intruder can easily use. When the intruder probes it, Stoll sees both the attacker's persistence and the value of separating the observer from the observed. Ron's Oakland trace then shows why a good local monitor still needs cooperation from network and telephone operators.

## Key Takeaways

- Separate monitoring from the systems being monitored.
- Capture the moment of access, not merely the aftermath.
- Plan the technical and legal next step together.

## Connects To

- Ch 3 — Looking for Footprints
- Ch 13 — Trace Without a Number
- Ch 22 — Phone Number
