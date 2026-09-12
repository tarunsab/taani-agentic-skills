# Patterns

These are recurring practices extracted from the narrative, not a formal management system. Apply them with the book’s counterevidence about exhaustion, secrecy, supply risk, and commercialization.

## Frame a risky initiative as insurance

**When to use:** A useful project lacks enough formal sponsorship to win an immediate organizational contest.

**How:** Present the initiative as protection against a rival path failing, while giving the builders a more energizing internal reason to care. The external frame can secure attention without forcing a public fight before the design has evidence. Pair it with a clear success case, because insurance that never becomes a product can consume resources without reducing risk.

**Trade-offs:** The frame creates room to work but can hide the project’s true stakes from participants and support groups. It also encourages need-to-know management, so disclose any constraint that changes technical or ethical decisions.

## Give signed-up people consequential ownership

**When to use:** A complex project requires judgment distributed across many boards, layers, or interfaces.

**How:** Ask whether a person is genuinely willing to take on the difficult work, then give them a whole responsibility with a visible connection to the system. Trust the owner’s technical choices, review evidence at the right interfaces, and make it possible to ask what is really happening without taking the work back.

**Trade-offs:** Ownership creates learning and intrinsic motivation, but “signing up” can become unpaid overtime enforced by peer norms. Pair responsibility with an escape valve, realistic support, and explicit limits on what the person is expected to sacrifice.

## Use the earliest date that cannot yet be disproved

**When to use:** A team needs a forcing function before the design and support dependencies are fully known.

**How:** Choose a date far enough out to sound possible but close enough to make motion unavoidable; then move design, hardware, simulation, documentation, and supplier conversations forward in parallel. Treat the date as a game that generates action, not as evidence that the machine will actually be ready.

**Trade-offs:** A moving target can prevent analysis paralysis, but repeated missed promises burn credibility and shift uncertainty onto exhausted finishers. Replace optimism with evidence as the release approaches.

## Design for the product’s bottleneck

**When to use:** A new system must beat an incumbent under hard cost, board-count, compatibility, or schedule constraints.

**How:** State the non-negotiables, choose the smallest implementation that can meet them, and reject features until the core one-board or one-path solution is clear. Use “quick-and-dirty” for a bounded tactic, then test the shortcut in the integrated system.

**Trade-offs:** Scope discipline can create a commercially right product sooner, but it may sacrifice elegance, numerical features, or future flexibility. Record what was omitted so a later team does not mistake the product boundary for a technical impossibility.

## Distribute control through shared interfaces

**When to use:** One manager cannot understand every microinstruction, board interaction, supplier dependency, and downstream handoff.

**How:** Let authority travel with expertise: architecture to the architect, hardware to the hardware leader, microcode organization to the microcode leader, and concrete implementation to the person closest to it. Keep the distributed system coherent with shared vocabularies such as UINST, visible interfaces, cross-checks, and a common product goal.

**Trade-offs:** Distribution increases speed and ownership, but local decisions can contradict one another or leave integration work invisible. Name the integrator and test the joins, not just the components.

## Turn rare failures into historical evidence

**When to use:** A complex machine fails intermittently and exhaustive proof is impractical.

**How:** Reproduce the failure with demanding diagnostics, instrument the state that could explain it, and trace backward or forward until a state change is found. Remove one dependency to narrow the search, but treat the intervention and test fixture as possible confounders. After a repair, rerun the earlier suite and the long-run workload.

**Trade-offs:** The method is slower than guessing but produces evidence that survives argument. A small fix can still expose a second failure, as the NAND-gate repair and extender-frame episode show.

## Win the next pinball game

**When to use:** A project has many obstacles and scarce shared resources, so an all-or-nothing goal is demoralizing.

**How:** Make the next win concrete—free a computer, clear a diagnostic barrier, complete a board, or secure a supplier path—then preserve the capacity to play again. A leader can buffer politics and save resources for the next product while the team concentrates on the current ball.

**Trade-offs:** Local wins sustain momentum, but resource theater can become a substitute for fixing allocation. Keep the team informed about risks, especially supplier failure, and do not let “another game” conceal the need for rest or fair access.

## Judge craft by conditions as well as output

**When to use:** A technically successful project relied on unusual autonomy, pressure, secrecy, or long hours.

**How:** Ask who could make consequential choices, who could see the result in the whole, and what the work did to people’s health, relationships, and future options. Preserve the parts that create meaning—responsibility, difficulty, peer recognition, and visible accomplishment—while designing guardrails for the costs.

**Trade-offs:** The pattern explains why money and praise do not fully motivate craft, but it can be misused to romanticize exploitation. A good result does not retroactively make every working condition good.

## Release by evidence and handoff

**When to use:** A prototype is mostly working and pressure is shifting from invention to shipment.

**How:** Define release gates such as long-run reliability, real software workloads, benchmark targets, documentation, manufacturing readiness, and a downstream owner. Test the exact configuration customers will receive, record physical and software conditions, and transfer responsibility explicitly.

**Trade-offs:** Gates make readiness legible but can tempt managers to celebrate a green result while unfinished support work remains. Keep “passes this test” separate from “belongs in the field.”

## Preserve collective authorship

**When to use:** A product launch or postmortem is likely to simplify a team effort into one leader, title, or marketing name.

**How:** Keep an attribution stack that includes the organizational environment, opportunity, framing, architecture, implementation, debugging, integration, documentation, and handoff. Explain the product’s public promise separately from the history of how the system was made.

**Trade-offs:** Layered credit is more accurate but less convenient for press, patents, and promotion. Without it, the people who supplied the glue and the judgment disappear from the record.
