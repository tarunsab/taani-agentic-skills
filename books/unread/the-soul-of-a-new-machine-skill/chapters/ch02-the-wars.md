# Chapter 2: The Wars

## Core Idea

The “wars” begin with Data General’s need to answer DEC’s VAX 11/780, a 32-bit supermini that threatened to make the company look technologically behind. West secretly examines a VAX, not to copy its circuits, but to count its boards and chips, estimate its manufacturing cost, and reassure himself that DEC’s complexity is not unbeatable. The technical issue is the size of logical-address space: 16 bits yield roughly 65,000 directly addressable compartments, while 32 bits yield about 4.3 billion, and customers increasingly want the larger space. Organizational politics then turns that need into a contest between FHP, moved to North Carolina, and EGO, a Westborough design that uses a mode bit to behave as both a 16-bit Eclipse and a 32-bit machine. EGO is cancelled after an internal fight, leaving Westborough depressed, but the cancellation also clarifies what a surviving project must do: preserve Eclipse software compatibility without a mode bit. West gathers the technical ideas and begins promoting Eagle as a fast, compatible “insurance” machine, keeping the project quiet enough to live while making it exciting enough to recruit its builders.

## Frameworks Introduced

- **Software compatibility as installed-base leverage**: Use when a new system must attract existing customers; preserving working programs lowers switching costs and gives customers a path from old machines to new ones.
  - How: Identify what customers cannot afford to recreate, preserve the old behavior, and add the new capability alongside it.
- **Insurance positioning**: Use when formal sponsorship is weak and a direct challenge would provoke resistance; describe the initiative as protection against another plan failing while quietly building a real alternative.
- **Mode-bit constraint**: A mode bit can make one box behave like two architectures, but it adds product-line and implementation complexity; de Castro’s “no mode bit” forces a single compatible design.

## Key Concepts

- **32-bit**: A computer organization that handles information in 32-bit packets and can directly express a far larger address space.
- **Logical-address space**: The set of uniquely named storage compartments a machine can address.
- **VAX 11/780**: DEC’s influential 32-bit supermini and the immediate competitive threat to Data General.
- **FHP / Fountainhead Project**: The large 32-bit project transferred from Westborough to North Carolina.
- **EGO**: Westborough’s proposed two-mode machine, named as a counterpoint to FHP.
- **Mode bit**: A control choice that switches the machine between two operating modes or architectural identities.
- **Backward compatibility**: The ability of a newer machine to run software written for an older one.
- **Cultural compatibility**: A looser resemblance to an older product line that does not guarantee old programs will run.
- **Canard**: In the group’s vocabulary, a false or wrongheaded notion, often attributed to another group.
- **Kludge**: A design assembled in an inelegant, makeshift way; an especially severe insult among the engineers.

## Mental Models

- Think of address bits as **telephone digits**: more bits create more unique numbers, but only matter if the storage and software can use them.
- Treat compatibility as a **customer lock-in and escape problem**: old software is valuable, and abandoning it makes a market survey likely.
- Use **strategic ambiguity** when an initiative needs cover, but remember that the people doing the work may not know the real stakes.

## Anti-patterns

- **Reverse engineering for imitation**: West’s inspection is bounded fact-finding about cost and complexity, not a plan to reproduce VAX board by board.
- **Technical victory without organizational viability**: EGO may be admired by its designers, yet the company’s investment in North Carolina and the size of FHP determine what can survive.
- **Treating compatibility as cosmetic**: A machine that merely resembles its predecessor does not preserve the customer’s existing software investment.

## Worked Example

The address-space problem gives the war a concrete shape. A 16-bit address has 2^16 possible values, about 65,000 storage locations; a 32-bit address has 2^32, roughly 4.3 billion. EGO tries to provide both worlds by switching modes, but its designers are pursuing a separate and politically vulnerable architecture. After EGO is cancelled, West asks what customers actually need and learns that a 32-bit machine must also retain Eclipse software. Eagle becomes the compromise with a strategic purpose: one compatible machine, no mode bit, a short schedule, and enough performance to challenge VAX without announcing an internal challenge to North Carolina.

## Key Takeaways

1. Competitive urgency becomes useful only when translated into a specific technical and customer requirement.
2. Compatibility preserves installed value, but it constrains architectural freedom.
3. A backup narrative can create room for a real project inside a political organization.

## Connects To

- **Chapter 1**: Explains why falling behind a new product class threatens Data General’s growth.
- **Chapter 4**: Follows the “no mode bit” constraint into Wallach’s architecture.
- **Chapter 6**: Shows how the political situation becomes the group’s rules for resources, schedules, and risk.
- **Chapter 15**: Revisits whether Eagle was designed by management, West, or the engineers themselves.
