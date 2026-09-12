# Chapter 9: The Trojan Horse

## Core Idea

The intruder installs a deceptive login program that displays a familiar prompt and stores credentials typed into it, creating a second way to steal access. Stoll slows and observes the connection, while Dave notices that the software behavior fits AT&T Unix and that the intruder is using Kermit as a general transfer tool. The technical lesson is that a user-visible interface can be a trap even when the underlying account appears ordinary. Stoll also begins to think of operating-system diversity as a kind of software genetic diversity: different implementations can prevent one flaw from spreading everywhere.

## Frameworks Introduced

- Trojan-horse pattern
- Interface deception
- Software diversity

## Key Concepts

- False login prompt
- Credential capture
- Kermit
- AT&T Unix
- Operating-system diversity

## Mental Models

- The familiar doorway as camouflage
- Diversity as containment

## Anti-patterns

- Trust a prompt because it looks normal
- Standardize every host so one exploit transfers unchanged

## Worked Example

The false login program matters because it attacks the operator's expectation rather than only a technical boundary. Stoll's monitors expose the sequence, but they do not make the trap harmless; a user who types a real credential could lose access elsewhere. The chapter's defensive implication is to verify the path and to avoid making every system depend on an identical trust assumption.

## Key Takeaways

- Verify authentication paths, not just account names.
- Treat cross-system credential reuse as a force multiplier.
- Use heterogeneity deliberately where it reduces correlated failure.

## Connects To

- Ch 4 — Cuckoo's Egg
- Ch 20 — Elxsi Trap
- Ch 47 — Dictionary
