# Chapter 47: The Dictionary

## Core Idea

Stoll notices that the hacker can try many passwords because Unix's one-way password transformation makes verification cheap, and Bob Morris explains how a dictionary attack precomputes common words and tests them against the stored values. The lesson is not that encryption is broken, but that a weak human-chosen secret can be guessed offline when an attacker obtains the transformed password file. Stoll concludes that stronger passwords must avoid ordinary words, while the agencies' reluctance to disclose vulnerabilities shows that a local fix does not automatically improve the wider ecosystem. The chapter connects the specific incident to a general security principle: credential strength is part of system design, not merely user etiquette.

## Frameworks Introduced

- Dictionary-attack model
- Offline verification risk
- Credential policy

## Key Concepts

- One-way transformation
- Password file
- Dictionary word
- Bob Morris
- Credential disclosure

## Mental Models

- Cheap testing beats clever guessing
- A password file as a capability amplifier

## Anti-patterns

- Assume one-way storage makes weak passwords safe
- Treat a password rule as sufficient without considering usability and disclosure

## Worked Example

The attacker is observed trying names and common choices, while Morris supplies the broader mechanism that explains why such guesses scale. Stoll changes his own practices and warns that agencies often hide the existence of holes instead of coordinating a fix. The source's practical point is about attack economics: once the transformed password file is available, familiar words are not much of a barrier.

## Key Takeaways

- Use passwords that are not predictable dictionary words.
- Protect transformed credential files as sensitive capabilities.
- Pair local credential changes with disclosure and remediation across dependent systems.

## Connects To

- Ch 2 — Super-User Threat
- Ch 9 — Trojan Horse
- Ch 50 — Last Holes
