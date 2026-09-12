# Chapter 4 — Swatting at Mosquitoes

## Core Idea

The F-117's first production aircraft exposed a new class of problems: small manufacturing imperfections could erase the radar advantage of the whole design. Rich uses the “mosquitoes” image for these seemingly minor defects and shows that production quality, maintenance, security, documentation, and user training were part of the stealth technology itself. The first aircraft were treated as learning instruments rather than a clean handoff from engineering to an anonymous factory. That approach made production slow and expensive, but it created a feedback loop in which each aircraft taught the team how to build the next one.

## Frameworks Introduced

- Put operators and builders together from the first production units.
- Treat access panels, fasteners, paint, and tools as mission-critical interfaces.
- Use simple physical controls to prevent recurring defects.
- Measure learning rate honestly instead of comparing unlike factories.
- Let quality authority interrupt progress when the system is at risk.

## Key Concepts

Major Al Whitley and his crew chiefs worked alongside the people who built the first F-117s. The arrangement made maintenance discoveries immediately visible to the designers and gave operators confidence that their feedback mattered. “Buttering” the aircraft meant replacing or filling access-panel material so that an indentation did not become a radar reflector. A production tail that fluttered off during testing revealed that the initial tail was too small and flexible; the fix was a design and manufacturing lesson, not a reason to blame a single worker.

The learning curve was steep. Lockheed produced only a few aircraft over several months while conventional manufacturers could build many more, yet the memoir attributes the difference to training, inspection, supervision, motivation, and shortages as much as to the geometry. New workers also created foreign-object-debris risk, so the team audited tools and parts, used pocketless clothing, locked and tagged material, and stopped work for cleaning. These controls were costly, but the cost of repairs, security violations, and schedule disruption was higher.

Rich describes a clash with OSHA and a growing population of auditors. Progress payments were cut when records were missing, even though some documents had been destroyed under security procedures and the destruction itself had not been logged in the expected way. The episode demonstrates that security and compliance can create contradictory evidence requirements. A fast team still needs a small, durable record system that proves what happened without exposing more than necessary.

## Mental Models

### The first production units are field experiments

Do not pretend that an aircraft, medical device, or complex software release becomes mature when the prototype label disappears. Treat the first small batch as an instrumented learning cohort. Preserve detailed records, keep builders close to users, and make changes easy enough to incorporate without hiding defects.

### Critical defects can be physically small

The “mosquito” is a defect whose dimensions are tiny but whose consequence is system-wide. A useful review asks not “is this part small?” but “can this part disrupt the dominant mission mechanism?” This is why the memoir makes heat shields, surface finish, tail flutter, tools, and loose hardware feel as important as the headline design.

## Worked Example (Study)

The successful first F-117 flight on June 18, 1981 followed a production process full of small corrections. The aircraft was not a perfect Mercedes; it was a mission-focused system whose team identified the critical performance and signature risks and kept solving them. The successful flight therefore validates a disciplined learning loop more than a claim that the initial design was complete.

## Distinctions and Limitations

The memoir's quality culture depends on unusually close access to the customer and on leaders willing to tolerate short-term inefficiency. Pocketless coveralls and stop-work cleaning are not universal solutions; they are examples of making a failure mode visible and expensive enough to control. Rich's account also presents the team as unusually cohesive, so readers should test whether their own workforce, supplier base, and regulatory obligations can support the same cadence.

## Practical Use

For a first production batch, define a learning charter: what will be measured, who sees defects, how operators report them, and what evidence can trigger a design change. Track defects by mission consequence rather than by part count. Build a minimal audit trail that reconciles security, quality, and payment requirements before the project enters production.

## Connects To

- [Chapter 3 — The Silver Bullet](ch03-the-silver-bullet.md): the contract and design trades that production must honor.
- [Chapter 16 — Drawing the Right Conclusions](ch16-drawing-the-right-conclusions.md): cost, paperwork, and lifecycle lessons.
- [Patterns](../patterns.md): “Use customer operators as design input” and “Keep design and production in the same conversation.”

## Key Takeaways

- Production quality is part of the technical invention when small defects destroy the mission advantage.
- Early users and builders should form one learning system.
- Security and compliance need evidence designs that are simple enough to survive real operations.
- A slow first batch can be rational if it increases knowledge and reduces later rework.

