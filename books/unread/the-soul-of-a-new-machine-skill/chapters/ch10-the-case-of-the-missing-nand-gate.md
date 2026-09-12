# Chapter 10: The Case of the Missing NAND Gate

## Core Idea

This chapter is the book’s clearest debugging case study. The team does not try to prove Eagle correct by exhaustive reasoning—an impossible task for a machine that runs billions of cycles—so it runs increasingly demanding diagnostics and studies the traces produced when a failure occurs. The difficult bug appears only occasionally during Eclipse 21, and the initial suspicion is “noise,” but identical failures on two prototypes and the behavior of the accelerators suggest a logical inconsistency between the Instruction Processor’s cache and the System Cache. A cache can contain a stale copy of an instruction, setting a time bomb far earlier in the diagnostic program than the moment at which the wrong instruction executes. Guyer forms and revises hypotheses; Veres searches forward through a long run and proves that the System Cache issues the invalidation while the IP keeps the old block. The repair is tiny—a delay implemented with an eight-cent NAND gate producing the locally named `NOT YET` signal—but the team then discovers that a test fixture, the IP board on an extender, is causing another failure. The case shows debugging as disciplined search through history, not just intuition: reproduce the failure, instrument the right state, isolate subsystems, distinguish a plausible story from evidence, and rerun prior tests after every repair.

## Frameworks Introduced

- **Exercise rather than prove**: Use demanding, repeated tests to expose incorrect behavior, then repair and retest; full formal certainty is not practical for a complex commercial computer.
- **Trace the time bomb backward and forward**: When the failure occurs later than its cause, capture enough history to locate the state change that made the failure possible; search forward when the instrument cannot see far enough backward.
- **Isolate by changing one dependency**: Remove or relocate a subsystem, such as the I-cache, to narrow the suspects, but treat the intervention itself as a possible confounder.
- **Repair, then regress**: After a fix passes its target diagnostic, rerun tests already passed to ensure the new signal or gate did not create a different failure.

## Key Concepts

- **Diagnostic program**: A deliberately repetitive test that exercises many instructions and data paths.
- **Reliability**: The ability to perform a huge number of operations without an intermittent failure.
- **Accelerator**: Hardware such as the IP or Sys Cache that predicts and retains likely instructions or data to gain speed.
- **I-cache**: The Instruction Processor’s small instruction cache.
- **Time bomb**: A latent state inconsistency that is created early and causes a visible failure much later.
- **Block**: A group of memory locations moved together through cache storage.
- **Tag**: The number identifying a memory block in the cache.
- **JSR and Return**: A jump-and-return sequence that becomes the test’s revealing detour.
- **NAND gate**: A circuit implementing the “not and” function and, here, a timing repair.
- **NOT YET**: Holberger’s plain-language name for the delayed signal added by the repair.
- **Extender**: A frame that lets a board run outside its normal position for debugging, while potentially changing its behavior.

## Mental Models

- Think of caches as **nested mailboxes with duplicate contents**; correctness requires invalidation and replacement to keep copies identical.
- Treat an intermittent failure as a **historical event**, not merely a bad instant.
- Use **hypotheses as probes**: a plausible explanation earns the next measurement, not belief.

## Anti-patterns

- **Calling every intermittent failure noise**: Random noise is one possibility; a repeatable low-frequency pattern can indicate a logic error.
- **Fixing the visible wrong instruction**: The stale cache state is created earlier, so the repair must address the invalidation timing.
- **Trusting a passing isolated board**: The IP on an extender creates a test condition that can itself cause or expose a failure.
- **Stopping at the first green test**: The NAND repair initially coincides with another failure; regression testing is part of the fix.

## Worked Example

Eclipse 21 runs 921 passes overnight on both Coke and Gollum but fails 30 times, which is rare enough to be hard to catch and too regular to dismiss. The failing JSR-and-Return reaches the right address but finds the wrong instruction in the I-cache. Guyer notices that the target instruction has moved between addresses; Veres then records the cache tags across the relevant iterations and sees the System Cache replace tag 21 with tag 45 while the IP retains 21. The IP is receiving a second signal too soon and discarding the new block instead of the old one. A NAND gate delays that signal and creates `NOT YET`; when another diagnostic fails, the team removes the gate, then realizes the IP was on an extender, returns it to its normal frame, and confirms that the new failure disappears without undoing the original repair.

## Key Takeaways

1. Repetition turns a rare failure into evidence only when the team records where it occurs.
2. In a cached system, present behavior can be caused by stale state created much earlier.
3. Small physical fixes can encode a large explanatory model.
4. Test equipment and repair configurations are part of the experiment, not neutral scenery.

## Connects To

- **Chapter 6**: Provides the detailed form of the IP, ATU, cache, and microsequencer interactions.
- **Chapter 7**: Demonstrates the diagnostic discipline and fear taxonomy introduced there.
- **Chapter 8**: Parallels the Microteam’s use of a simulator to shorten and clarify feedback.
- **Chapter 14**: Extends the same method to interrupts, memory boundaries, and final reliability.
- **Chapter 15**: Supports the book’s claim that technical mastery and collective ownership made the project work.
