# Chapter 27: The Fox and the Hound

## Core Idea

After Thanksgiving, Stoll gives his graphics talk and notices that the hacker returns after a month, confirming that a quiet period did not mean the campaign ended. Mitre's modems are closed, so Stoll's strategy becomes a contest of visibility rather than a direct attempt to force the attacker out: alarms, a pager, and physical connection to the right monitoring point. The “fox and hound” image captures the asymmetry—one side can move through many systems while the other must keep a stable trail. The chapter's practical implication is to design a durable observation loop instead of relying on a single successful chase.

## Frameworks Introduced

- Persistent monitoring loop
- Signal-versus-noise discipline
- Asymmetric pursuit

## Key Concepts

- Thanksgiving gap
- Alarm
- Pager
- Physical tap
- Monitoring station

## Mental Models

- The fox's mobility
- The hound's trail

## Anti-patterns

- Abandon monitoring during a quiet period
- Use alerts without preserving the underlying session data

## Worked Example

The return of the hacker after the Mitre route closes shows why Stoll keeps the Berkeley host instrumented. He does not need to know the motive before acting; he needs a reliable signal that a session is active and enough context to request a trace. The human pager and the physical monitor form a simple loop: detect, confirm, coordinate, and record.

## Key Takeaways

- Design for intermittent activity.
- Keep the observation channel stable while the subject changes routes.
- Separate detection, confirmation, and escalation.

## Connects To

- Ch 18 — Mirror Notebook
- Ch 28 — Hacker's Hours
- Ch 41 — Wrong Nest
