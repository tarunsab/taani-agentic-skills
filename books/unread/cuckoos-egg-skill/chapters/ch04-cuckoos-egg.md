# Chapter 4: The Cuckoo's Egg

## Core Idea

The printout reveals that the intruder is using Sventek's stolen credentials and exploiting a flaw in the Gnu-Emacs move-mail path to replace a privileged system program. When the operating system runs the altered program, the intruder becomes super-user, reads mail, watches active users, kills Stoll's monitor, and copies credentials for trusted systems. The “cuckoo's egg” image names a hostile program placed inside a legitimate system so that the system itself hatches the intruder's privilege. The chapter also establishes a crucial investigative tension: closing the vulnerability protects the host, but doing so immediately may destroy the only window into a larger campaign.

## Frameworks Introduced

- Privilege-escalation chain
- Cuckoo's-egg metaphor
- Window-versus-containment trade-off

## Key Concepts

- Stolen credentials
- Gnu-Emacs flaw
- Privileged program
- Super-user transition
- Trusted network

## Mental Models

- A parasite using the host's own lifecycle
- Visibility versus containment

## Anti-patterns

- Assume the attacker must remain at user privilege
- Patch or close the host without preserving evidence

## Worked Example

The intruder's sequence is compact: enter with a stolen account, alter a program that the system will later execute, gain super-user authority, and restore the original program to reduce suspicion. Stoll can see the sequence because the printer captures commands as they happen. The result is not a complete explanation of the intruder's goal, but it is strong evidence that the system has been used as a stepping-stone rather than merely browsed.

## Key Takeaways

- Model compromise as a chain of state changes, not a single event.
- Treat privileged program replacement as a system-integrity failure.
- Balance containment against the evidentiary value of continued observation.

## Connects To

- Ch 5 — Keep the Doors Open
- Ch 16 — Research, Not Revenge
- Ch 50 — Last Holes
