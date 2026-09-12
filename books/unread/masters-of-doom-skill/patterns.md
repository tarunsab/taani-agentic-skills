# Patterns

## Complementary seam

- **When:** A small team must combine specialized skills under severe time or hardware limits.
- **How:** Give engine, tools/play, art, design, and operations distinct owners, then keep the interfaces concrete through shared builds and direct feedback. The early id team works because each person can move quickly inside a clear seam.
- **Trade-offs:** Specialization accelerates output but becomes a fault line when the shared direction is unclear or one owner dismisses another kind of expertise (Ch 03–06, 12).

## Constraint-first breakthrough

- **When:** The desired experience is blocked by a platform or performance limit.
- **How:** Identify the bottleneck, redesign the representation around it, and protect the player-visible loop. Adaptive tile refresh, raycasting, cached layers, BSP visibility, and simplified geometry all follow this pattern.
- **Trade-offs:** The workaround can create a new genre, but it may also exclude story, atmosphere, or features that do not fit the optimized loop (Ch 03, 05–06, 09, 12).

## Bounded first taste

- **When:** Discovery and payment are harder than production.
- **How:** Release a compact, high-value slice that is easy to copy or download, then charge for the continuation. Commander Keen and Wolfenstein made the first episode do the selling.
- **Trade-offs:** The first slice must stand alone while creating appetite; order handling, piracy, and partner relationships become the next bottlenecks (Ch 03–04, 07, 10, 13).

## Player-as-builder loop

- **When:** A stable core can support content beyond the original team’s capacity.
- **How:** Separate data from code, expose editing tools, and let players exchange levels or rule changes. Doom’s WADs, DEU, and DeHackEd turned usage into creation and community.
- **Trade-offs:** Openness increases immersion and longevity but brings legal ambiguity, support costs, quality variance, and loss of control (Ch 06–07, 10, 13).

## Innovate, optimize, jettison

- **When:** A project has more ideas than it can finish.
- **How:** Explore a bold possibility, test it against the core experience, keep the part that raises the signal, and deliberately discard the rest. Doom’s development repeatedly cuts story or features when they threaten speed, while still recovering push walls when secrets become essential.
- **Trade-offs:** Ruthless focus protects shipping; applied without empathy it erases contributors and can make the product feel repetitive (Ch 06, 08–09, 12).

## Finish-and-distribute

- **When:** The product is viable but the team is tempted by the next idea or by publicity.
- **How:** Freeze the promise, close bugs, choose a channel, and make access easy. Carmack’s small-team discipline contrasts with Romero’s public projections and later Ion Storm delays.
- **Trade-offs:** Shipping is a strategic advantage, but a narrow definition of “done” can underinvest in story, polish, or organizational health (Ch 07, 12, 14–16).

## Visible myth, invisible work

- **When:** A community wants a face, a story, or a movement around the product.
- **How:** Use authentic artifacts—updates, tournaments, creator access, and memorable language—to make the work legible. Romero becomes the public front of id while Carmack’s logs make progress concrete.
- **Trade-offs:** Myth compounds attention but also creates entitlement, backlash, and a dangerous gap between the persona’s promises and the team’s actual capacity (Ch 00, 07, 10–14).

## Small-team ceiling

- **When:** A project’s uncertainty is high and communication cost is more dangerous than labor shortage.
- **How:** Keep the core small, add people only for a clear ownership gap, and make coordination work explicit. Carmack’s experience is that a team can become slower after problems are split too finely.
- **Trade-offs:** Smallness preserves coherence but concentrates power, knowledge, and failure; the Quake and Ion Storm stories show that autonomy without management is not freedom for everyone (Ch 11–15).

## Culture as product infrastructure

- **When:** A game’s value depends on repeated play with other people.
- **How:** Build the social affordance into the artifact—deathmatch, hosted play, clans, mod exchange, or persistent worlds—and observe what players make of it.
- **Trade-offs:** The community can outgrow the original design and become the strongest distribution engine, but controversy and governance arrive with it (Ch 09–16).
