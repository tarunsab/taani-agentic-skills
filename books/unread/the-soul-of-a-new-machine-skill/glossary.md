# Glossary

Terms below are defined in the sense used by Tracy Kidder’s account of Data General’s Eagle project. Some are technical terms; others name the project’s social rules or recurring images.

## A–E

- **Adventure** — A large software workload used late in the project as a test of the complete machine, not merely of an isolated board.
- **ALU** — Arithmetic-logic unit; the processor section that performs operations such as addition and subtraction. Eagle’s one-board ALU is a central example of performance gained through feature sacrifice.
- **ATU** — Address Translation Unit; part of the path that maps a program’s address before instruction and cache activity proceed.
- **Canards** — The chapter title for stories or attributions that circulate, perhaps elegantly, but simplify a collective event too much.
- **Coke / Gollum** — Prototype machines used for testing. Their different memory-board configurations show why a result belongs to a specific configuration.
- **Eagle** — Data General’s new 32-bit computer, developed by the West-led group under pressure to be fast, compatible, inexpensive, and shippable.
- **Eclipse** — Data General’s earlier computer family and the culture surrounding it. Eagle had to be compatible with Eclipse software and peripherals while competing with the VAX.
- **EGO / FHP** — Competing internal project identities in the struggle around the VAX-era product direction; the names mark organizational politics as well as technical alternatives.

## F–M

- **I-cache** — Instruction cache in the Instruction Processor. It stores recently used instruction blocks and becomes the site of the missing-NAND-gate failure.
- **IP** — Instruction Processor; the part of Eagle that prefetches, decodes, and executes instructions, working with translation and cache hardware.
- **MPR** — Multiprogramming Reliability test. Its long-run failures in the last crunch demonstrate that passing isolated tests is not the same as release readiness.
- **Microcode** — Low-level control instructions that sequence the hardware. Eagle’s microinstructions are 75 bits wide; the Microteam organizes them through microverbs and a shared UINST vocabulary.
- **Microkids / Microteam** — The young programmers and their group working on Eagle’s microcode. Their play, pranks, and distributed ownership are part of the project’s technical culture.
- **Micromachines** — The title’s image for the microcode subsystems and the people who build them: small control structures nested inside the larger computer.

## N–R

- **NAND gate** — A logic gate whose timing is used to delay a cache-control signal in the rare Eclipse 21 failure. The repair is small, but its placement follows a long trace of evidence.
- **NOVA** — Data General’s earlier minicomputer line. Its large boards and commercial success establish the company’s starting point and the growth pressure around Eagle.
- **PAL** — Programmable array logic device used in Eagle’s implementation. Dependence on a single supplier becomes a deliberate schedule and supply risk.
- **Pinball** — The project’s metaphor for winning one challenge in order to earn the next game. It names both a resource strategy and a motivational promise of future meaningful work.
- **Quick-and-dirty** — A preference for the simplest working solution that meets the product’s constraints. It is a judgment about scope and timing, not a license to skip evidence.
- **Rasala** — Hardware leader associated with dogged implementation, debugging, and the final “last two percent.” His work exposes the difference between a design that exists and a product that survives tests.
- **Rings and segments** — Eagle’s address-space organization: three bits can select eight segments and eight rings. The scheme supports a large 32-bit space while preserving compatibility and protection ideas.

## S–W

- **Signing up** — Voluntary commitment to the difficult project, including its schedule and long hours. The book treats it as both a source of meaning and a route to peer pressure and burnout.
- **Sys Cache** — System-level cache holding instruction or data blocks alongside the I-cache. Correctness depends on replacement and invalidation signals keeping the copies coherent.
- **UINST** — Shared dictionary and grammar for microcode. Holland uses it to organize hundreds of instructions and prevent local microverb choices from contradicting one another.
- **VAX** — Digital Equipment Corporation’s competing 32-bit computer. Its cost, complexity, speed, and compatibility influence Eagle’s architecture and sales case.
- **WSEQ** — The micro-sequencer, which advances through Eagle’s 75-bit microinstructions and controls branches, skips, and ALU operations.
- **West, Tom** — Project leader who frames Eagle as insurance and a challenge, delegates whole responsibilities, protects the group from organizational noise, and later becomes the focus of attribution debates.
- **“Flying upside down”** — West’s image for deliberately taking a large, controlled risk when the ordinary route cannot win: compressed schedule, small team, new components, and parallel work.

## Distinctions to Preserve

- **Architecture vs. implementation** — Architecture specifies the programmer-visible and system-level contract; implementation chooses the circuitry and sequencing that realize it.
- **Compatibility vs. identity** — Eagle must behave like an Eclipse where customers depend on it, while still being a new and faster product.
- **Trust vs. absence** — Giving someone a whole responsibility can be trust; withholding context or support can instead be abandonment.
- **Speed vs. readiness** — A benchmark advantage matters only alongside reliability, documentation, manufacturing, software, and handoff.
- **Freedom vs. voluntariness** — Engineers have real choice over difficult work, but organizational norms can make refusal costly.
