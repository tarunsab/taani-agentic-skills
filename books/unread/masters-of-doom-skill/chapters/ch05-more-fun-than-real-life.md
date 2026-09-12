# Chapter 5: More Fun Than Real Life

## Core Idea

This chapter links Carmack’s private Dungeons & Dragons campaign to the public problem of building a convincing game world. His carefully maintained glossary, dangerous artifacts, persistent characters, and willingness to let a world die show how rules can give imagination consequences; play feels meaningful when choices have stable effects. At id, the same desire for immersion drives Carmack from Commander Keen and Rescue Rover toward fast-action first-person 3-D. Hovertank uses raycasting, limited polygons, and scaled sprites to create a quick, imperfect illusion of depth, while Keen Dreams layers cached backgrounds and foregrounds to fake parallax. The team keeps adapting the representation to what the hardware can sustain rather than waiting for a complete simulation. A parallel business conflict appears when Mark Rein’s retail instincts and Apogee’s episodic shareware formula pull in different directions. The chapter’s central limit is that technical progress, retail opportunity, and creative tone can all be correct locally while still leaving the team divided about what the company is making.

## Frameworks Introduced

The first framework is **persistent rules create agency**: a world becomes compelling when its constraints are remembered and the player’s actions matter inside them. The second is approximation as engineering strategy; raycasting and layered caches do not simulate every surface, but they protect speed and the player’s sense of presence. The third is a pipeline of escalating experiments: use a small game to prove a rendering idea, then reuse the idea in a more expressive product. The chapter also establishes the engine/play seam as an asset, provided design and technology keep communicating. Apply it by identifying the sensation that must survive the approximation, not by assuming visual completeness is the goal.

## Key Concepts

- **Persistent campaign** — Carmack’s D&D world uses rules, memory, and consequences to make play feel consequential.
- **Raycasting** — project lines to find wall slices, then scale sprites to produce fast pseudo-3-D.
- **Hovertank** — an ugly but important proof that a PC could support fast first-person action.
- **Parallax illusion** — cache separate layers and move them at different rates to suggest depth.
- **Pipeline reuse** — carry a tested engine or technique into the next design problem.
- **Retail/shareware tension** — retail legitimacy and episodic control optimize different business goals.

## Mental Models

Think of immersion as a contract between perception and rules. The player does not need a physically complete world if movement, feedback, and consequences consistently support the imagined space. Think of Carmack’s engine work as a sequence of controlled lies: omit, cache, simplify, and scale, but never break the speed or response that makes the lie convincing. Think of a development pipeline as a ladder, not a single leap; Hovertank can be valuable even when it is not the final commercial form.

## Anti-patterns

- Pursuing full simulation when a narrower illusion would make the core action better.
- Calling a technical demo a finished experience without testing what players actually feel.
- Treating a successful distribution channel as the only legitimate path.
- Adding business or team structure faster than the product’s roles and incentives can absorb.

## Worked Example

Hovertank is a useful constraint-first case. Carmack wants a first-person game that moves quickly, but the PC cannot afford a fully modeled world with modern polygonal rendering. He uses raycasting to determine the visible wall strips, limits the geometry, and scales sprites for objects, accepting visual roughness in exchange for responsiveness. The result is not as pretty as a later game, yet it establishes the sensation of moving through a dangerous space and even preserves environmental traces such as lingering blood. Keen Dreams applies a related idea to side-scrolling: separate layers and caches create depth without rendering a complete 3-D scene. In both cases, the practical question is not “is the simulation complete?” but “does the approximation preserve the player’s intended action?”

## Key Takeaways

- Rules and consequences can make an artificial world feel real.
- Approximation is powerful when it protects the core sensation.
- Small technical experiments should be treated as steps in a reusable pipeline.
- Business and creative alignment must be revisited as the audience and channel change.

## Connects To

- **Ch 02, The Rocket Scientist** — the Holodeck ambition gives the engine experiments their long horizon.
- **Ch 06, Green And Pissed** — texture mapping and raycasting become a complete fast-action formula.
- **Ch 09, The Coolest Game** — BSP extends the same visibility-first optimization to Quake.
- **Ch 16, Persistent World** — persistent rules return as the basis for online worlds.

