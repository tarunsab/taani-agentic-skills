# Chapter 14: The Last Crunch

## Core Idea

The final stretch turns Eagle’s heroic schedule into a sequence of release gates whose evidence is harder to obtain as the obvious bugs disappear. Carman asks for a finish date, but Rasala refuses another confident promise: April, May, June, and the end of September have all passed, and credibility is running out. The team celebrates too early with awards, then works through a narrowing set of failures, including address-boundary behavior, hard interrupts, Adventure crashes, and the Multiprogramming Reliability test. Benchmarking adds another discomfort: Eagle must sacrifice double precision to beat the VAX’s single-precision speed, and the first numbers are not good enough. Physical details remain causal—heat, sockets, extender frames, memory-board configurations, and a shaken ALU can create or expose faults—so “software finished” or “logic correct” is never the whole release claim. When Adventure finally runs for twelve hours and the Whetstone result beats the VAX, the machine is still not simply done; documentation, software, manufacturing, and a last low-level flakiness problem remain before the handoff. The chapter’s discipline is therefore evidence matched to the shipped configuration, followed by explicit transfer to the next group.

## Frameworks Introduced

- **Release gates**: Define concrete tests that must pass before responsibility moves downstream; use full-night or long-run tests when intermittent faults are the risk.
- **Actual-workload evidence**: A benchmark or diagnostic that resembles real use can reveal interactions that isolated board tests miss.
- **Configuration-matched testing**: A result belongs to the exact hardware frame, memory complement, socket condition, and software image under test; changing the setup changes the experiment.
- **Finishers and handoff**: The last two percent needs people who can integrate, document, and transfer the system, not only the original specialists.

## Key Concepts

- **Eclipse and Eagle Multiprogramming Reliability (MPR)**: A demanding reliability test for running multiple programs.
- **Adventure**: A real software workload used as a practical test of the complete machine.
- **Whetstone**: A benchmark used to compare Eagle’s numerical performance with the VAX.
- **Interrupt**: A signal that requires the processor to suspend or redirect its current work.
- **Address boundary**: A point where the machine’s mapping or memory configuration can expose an off-by-one or missing-resource error.
- **Flakey**: An intermittent, hard-to-reproduce fault that resists a simple binary diagnosis.
- **ECO**: An engineering change order used to record and implement a hardware revision.

## Mental Models

- Treat release as a **funnel**: broad subsystem tests reduce the search space, but the remaining failures become more integrated and therefore more expensive to interpret.
- Treat the test setup as part of the system: **machine + configuration + workload + instrument** is the unit of evidence.
- Distinguish **green test** from **release-ready**. A test can pass while documents, manufacturing, downstream software, or a final intermittent fault still block shipment.

## Anti-patterns

- **Promising dates to relieve pressure**: A schedule that cannot survive evidence damages trust and makes the next estimate less useful.
- **Celebrating a milestone as completion**: Awards and preliminary benchmarks can lift morale, but they do not replace MPR, real workloads, and handoff.
- **Ignoring physical causality**: A hot lab, bad socket, extender, or missing memory board can masquerade as a logic or software bug.
- **Testing the ideal configuration**: Results from Coke do not automatically apply to Gollum, and a board outside its frame may not behave like the shipped machine.

## Worked Example

In September, a hard interrupt failure interacts with a block/page boundary: Coke has two memory boards, Gollum one, and the address system lets Gollum fall off the end until the team adds a board. Adventure then fails because the disk is roached, while MPR fails every four hours; after repeated work the full Adventure run succeeds on October 4 and Whetstone measures about ten percent faster than the VAX in single precision, roughly twice the fastest Eclipse. A low-level failure remains, and Carman can provoke it by shaking the ALU on an extender; replacing sockets removes the symptom, showing that mechanical state belongs in the diagnosis. Even after Gallifrey moves to Software, Rasala is tired and empty because the operational work of documentation, manufacturing, and transfer is still part of finishing.

## Key Takeaways

1. A late schedule is credible only when it is tied to tests and known remaining work.
2. Integrated workloads expose failures that component-level tests cannot predict.
3. Physical configuration and test fixtures can be causal variables, not background details.
4. A release is a transfer of responsibility, not merely the moment a benchmark turns green.

## Connects To

- **Chapter 7**: Develops Rasala’s “last two percent” into the full release struggle.
- **Chapter 10**: Reuses trace-and-regression debugging for rare failures and small physical repairs.
- **Chapter 11**: Shows how the project’s schedule and compromises continue to shape people after a subsystem works.
- **Chapter 13**: Converts the question of what technology will do into the immediate question of whether the product can be trusted.
- **Epilogue**: Completes the public handoff that this chapter prepares technically and emotionally.
