# Chapter 6: Flying Upside Down

## Core Idea

This chapter makes the project’s implicit rules visible. At Data General, nothing happens unless a team pushes it, and a group competing for a new product must also compete for support groups, prototypes, software, and executive attention. West’s one-year schedule is not a forecast; it is a commitment designed to create motion and demonstrate determination, even though everyone knows it is close to impossible. “Signing up” turns that schedule into a personal promise, while the hinted reward is the right to play again rather than guaranteed cash. West and his lieutenants accept multiple risks at once: inexperienced engineers, a single PAL supplier, a design assembled before all specifications are settled, and a product that must be cheap, fast, reliable, and compatible. The design process looks chaotic because hardware and microcode negotiate continuously, but sparse formal structure is partly replaced by trust, local ownership, and quick decisions. The chapter closes by showing an instruction move through Eagle’s layers, making clear that “mind games” and speed are purchased with complexity, anxiety, and no single person’s complete control.

## Frameworks Introduced

- **Competition for resources**: Use when a new product has to earn help inside a company; make the value of the idea legible to support groups and create enough urgency that they choose to participate.
- **What’s-the-earliest-date-by-which-you-can’t-prove-you-won’t-be-finished scheduling**: Use as a forcing device when delay itself is the main threat; treat the date as a self-imposed source of motion, not as evidence that the work is under control.
- **Flying upside down**: Take several bounded risks when the ordinary, fully protected path cannot reach the market in time; tie each risk to a concrete advantage and monitor its failure mode.
- **Trust after signing up**: Give a committed expert a substantial responsibility and let the person choose the implementation rather than decomposing the work into dull, easily monitored fragments.
- **No bells and whistles**: Keep the product inside explicit cost, speed, compatibility, and manufacturing constraints.

## Key Concepts

- **Competition for resources**: Internal rivalry over the people, tools, and support required to build a product.
- **Support group**: Another department, such as Software or Diagnostics, whose cooperation determines whether the machine can ship.
- **Escape valve**: Carl Carman’s policy allowing engineers to leave without reprisal when the pressure becomes too great.
- **PAL**: A new programmable logic chip selected for speed and flexibility despite having only one likely supplier.
- **Quick-and-dirty**: A fast implementation that works well enough for the commercial objective.
- **Trust**: A management choice to rely on a signed-up engineer’s responsibility instead of micromanaging every step.
- **Booth’s algorithm**: The multiplication procedure Jon Blau studies while preparing Eagle’s arithmetic microcode.
- **Instruction Processor / IP**: The part that predicts, fetches, and decodes instructions ahead of execution.
- **Address Translation Unit / ATU**: The part that maps program addresses to locations in the machine’s memory.
- **System Cache**: Fast storage that keeps likely instructions and data close to the processor.
- **Crock**: A subtle, damaging flaw in a design or implementation.

## Mental Models

- Treat a schedule as a **behavioral instrument** when the team has accepted it as a commitment; do not treat it as a probabilistic estimate.
- Think of a computer instruction as a **relay race through abstractions**: user program, IP, ATU, cache, microsequencer, ALU, and back again.
- Use **local ownership with global constraints** when no manager can hold the whole design in working memory.

## Anti-patterns

- **Pretending an impossible date is a normal plan**: The schedule can generate motion, but it also creates anxiety and masks real slippage.
- **Assuming competition supplies cooperation automatically**: Support groups have their own priorities; a project still has to earn their time.
- **Optimizing a local part without the whole machine**: Hardware and microcode repeatedly trade work across the boundary, so a “finished” component may not be useful in isolation.
- **Replacing all structure with heroics**: Trust works here because named people own technical areas and negotiate interfaces; it is not the absence of structure.

## Worked Example

Blau traces a `WSEQ`—Skip On Equal—through Eagle. The user program’s instruction is fetched and decoded by the IP, which identifies the microprogram and the values to compare. The Microsequencer emits 75-bit microinstructions on successive clock ticks; the ALU subtracts one value from the other and reports whether the result is zero. If the values differ, the microprogram ends and the IP fetches the next instruction; if they match, a final microinstruction tells the IP to skip one instruction and continue with the following one. The example is a small branch, but implementing it requires coordination among the same boards and control signals that make the full machine fast.

## Key Takeaways

1. Internal competition can create entrepreneurship, but it also makes support a political resource.
2. Extreme schedules work as commitments only when people act as if they matter.
3. Trust transfers control downward; it does not remove the need for interfaces, tests, or ownership.
4. Speed increases the number of interactions that later debugging must explain.

## Connects To

- **Chapter 3**: Extends signing up from recruitment into day-to-day labor.
- **Chapter 7**: Shows why the same speed and trust make debugging frightening.
- **Chapter 8**: Follows the parallel hardware–microcode work and the need for a simulator.
- **Chapter 10**: Supplies the IP/cache vocabulary used in the missing-gate investigation.
- **Chapter 14**: Tests whether the schedule and design can survive final reliability gates.
