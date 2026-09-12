# Chapter 6: Green And Pissed

## Core Idea

The Madison period turns id’s technical experiments into the recognizable Wolfenstein formula. The team works in a cold apartment, lives in crunch, and keeps testing whether texture mapping, sound, secret rooms, and speed can coexist on ordinary PCs. Carmack’s Catacomb 3-D and later Wolfenstein work make walls feel solid through raycasting and texture mapping while leaving floors and ceilings simple enough to preserve frame rate. Romero pushes for bodies, searching, hidden rooms, and a more playful physical space; Carmack initially rejects push walls as an ugly hack, then accepts them when the design value—secrets and discovery—outweighs the implementation cost. The resulting game combines violent feedback, jokes, music, mod potential, and a shareware episode that reaches far beyond the team’s original audience. Wolfenstein’s success creates money, celebrity, controversy, and a new expectation that id must make an even larger leap. The chapter closes with Carmack’s growing desire to build demons and deeper 3-D while Romero still wants the design to carry more of the player’s experience.

## Frameworks Introduced

The core framework is **protect speed, then add meaning at the edges**. Carmack removes slow searching and expensive surfaces from the main loop, while Romero uses secrets, sound, blood, and humor to make the fast loop emotionally legible. A second framework is “accept the hack when it serves the player”: the push wall begins as an implementation compromise but becomes a signature of exploration. The chapter also shows how a technical platform can be licensed, ported, and modified into an ecosystem—Super Nintendo, Shadowcaster, and Noah’s Ark all extend the engine in different directions. Apply this by naming the non-negotiable sensation, then judging every feature by whether it strengthens that sensation enough to justify its cost.

## Key Concepts

- **Texture mapping** — place image detail on rendered walls so a sparse scene feels more physical.
- **Fast-action loop** — movement, aiming, feedback, and enemy response must remain immediate.
- **Push-wall hack** — secret passages make a technical trick serve exploration and discovery.
- **Sound as embodiment** — music, weapon sounds, German voices, and monster cues make space feel active.
- **Mod and port ecosystem** — the engine’s value expands through player changes and licensed versions.
- **Doom premise** — demons versus technology becomes the next design/engine target after Wolfenstein.

## Mental Models

Model Wolfenstein as a stack: Carmack’s renderer supplies speed, Romero’s tools make spaces, Adrian’s art makes threats readable, and sound gives actions weight. Model feature triage by asking whether a feature increases the signal of the core loop or only increases the specification. A “hack” is not automatically technical debt if it creates a durable player affordance; it is debt when it adds complexity without changing the experience. Finally, success expands the constraint set: after Wolfenstein, the team must manage audience expectation, legal scrutiny, and a larger commercial surface.

## Anti-patterns

- Preserving a technically elegant implementation after it has become a barrier to meaningful play.
- Adding gore, secrets, or spectacle without protecting speed and readability.
- Treating a successful engine as a complete product rather than a platform that needs design.
- Accepting crunch as proof of commitment instead of a cost that can degrade judgment and relationships.

## Worked Example

The push-wall dispute demonstrates how design can revise an engine-first decision. Carmack thinks hidden moving walls are an ugly special case and initially tells Romero to forget them. Romero keeps arguing because the secret room changes what players do: they search, remember spaces, share discoveries, and feel that the maze has depth beyond shooting. Once the team sees that the feature supports exploration without destroying the speed loop, it is kept and becomes part of the game’s identity. The same logic governs texture mapping and sound: each addition is justified by how it changes perception, not by how impressive its implementation sounds. The lesson is to let the player-visible consequence decide whether a shortcut is worth the engineering cost.

## Key Takeaways

- Keep the action loop fast enough that every later layer can be felt.
- Let a technically inelegant feature survive when it creates a strong player behavior.
- Treat sound, secrets, humor, and feedback as part of immersion, not decoration.
- Expect success to create new organizational and cultural constraints.

## Connects To

- **Ch 05, More Fun Than Real Life** — Hovertank and Keen Dreams supply the earlier approximation experiments.
- **Ch 07, Spear Of Destiny** — Wolfenstein turns the formula into a public launch and fan phenomenon.
- **Ch 08, Summon The Demons** — the next game narrows the formula while increasing engine ambition.
- **Ch 10, The Doom Generation** — modding and open data turn the engine into player infrastructure.

