# Chapter 5: Keep the Doors Open

## Core Idea

Roy asks what the intruder can do, and Stoll realizes that the known flaw is only the beginning. Even if the obvious hole is closed, the attacker may have altered programs, planted a logic bomb, or created another path back in, while shutting the system would erase the best evidence. Stoll therefore chooses a monitored trap: keep the relevant access open long enough to understand the intruder and warn other sites. The decision is ethically uncomfortable because the laboratory is accepting local risk in order to learn about a wider threat.

## Frameworks Introduced

- Containment-versus-observation decision
- Known flaw versus unknown persistence
- Local risk / wider responsibility

## Key Concepts

- Logic bomb
- Backdoor
- Monitored trap
- Evidence window
- Operational risk

## Mental Models

- A compromised host as a watchtower
- Security work under incomplete knowledge

## Anti-patterns

- Treat patching the first hole as the end of the incident
- Assume the safest local choice is automatically the safest social choice

## Worked Example

Stoll does not claim that leaving a door open is universally correct. He keeps the choice bounded by monitors, watches for the intruder, and understands that the arrangement can fail if the attacker damages the lab. This is the chapter's practical pattern: make an explicit risk decision, define the information it is meant to obtain, and maintain a way to stop the experiment.

## Key Takeaways

- Name the trade-off before acting.
- Keep an observation experiment bounded and reversible where possible.
- Share warnings with affected system managers instead of treating the case as private property.

## Connects To

- Ch 21 — Responsible
- Ch 27 — Fox and Hound
- Ch 45 — Case for Staying Open
