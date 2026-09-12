# Chapter 3: Looking for Footprints

## Core Idea

Roy Kerth asks Stoll for evidence that the suspicious activity is real, so Stoll turns the computer center into an observation site. He explains the difference between LBL's open, unclassified research network and nearby classified environments, then follows the login's 1200-baud signature through the switchyard. Because the route can be hidden in ordinary network traffic, he connects old printers and monitors to every relevant line and watches for the characteristic long printout. The astronomy analogy matters: when a signal is faint, collect repeated observations, record the conditions, and separate what the data shows from what the observer merely suspects.

## Frameworks Introduced

- Distributed monitoring
- Astronomical observation method
- Evidence before inference

## Key Concepts

- 1200-baud line
- Switchyard
- Printer monitor
- Dial-in trace
- Network footprint

## Mental Models

- The computer center as observatory
- Redundancy creates visibility

## Anti-patterns

- Rely on a single log or a single screen
- Close the system before learning how the intrusion works

## Worked Example

Stoll's improvised monitoring station catches an unusually long output on one of the lines, which gives him a live view of the intruder rather than a retrospective account. The observation does not identify the person, but it does show that the activity is active, remote, and worth instrumenting further. The physical awkwardness of printers, wires, and a switchyard is part of the lesson: visibility often requires deliberately placing sensors where the system is least elegant.

## Key Takeaways

- Instrument the boundary where traffic becomes observable.
- Collect repeated, time-linked observations before building a theory.
- Use independent evidence channels when an attacker may alter local records.

## Connects To

- Ch 6 — Watchdog and Wiretap
- Ch 17 — Echo
- Ch 31 — Noise
