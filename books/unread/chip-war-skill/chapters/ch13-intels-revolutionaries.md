# Chapter 13: Intel’s Revolutionaries

## Core Idea

Bob Noyce and Gordon Moore left Fairchild in 1968 to create Intel, betting that the number of transistors sold would become enormous even if each one became cheap. Intel’s first product, DRAM, replaced magnetic-core memory by storing bits in transistor-and-capacitor cells that could be fabricated rather than hand-woven. The company’s success depended on design, manufacturing, and a willingness to pursue a market that did not yet exist at scale. Intel’s founders also embodied the spinout culture that made Silicon Valley renew itself. Their decision turned integrated electronics from a promising product into a company organized around continuous density and cost improvements.

## Frameworks Introduced

- **DRAM cell**: pair a transistor with a capacitor, refreshing the charge repeatedly to store a bit.
  - When to use: when dense, low-cost temporary memory is needed.
  - How: fabricate the storage elements on silicon and use repeated refresh to compensate for leakage.
- **Volume-before-margin**: pursue a vast market for a cheap component rather than a small market for an expensive one.
  - When to use: when adoption can expand with lower unit cost.

## Key Concepts

- **Intel**: Noyce and Moore’s company, initially built around memory and later microprocessors.
- **DRAM**: dynamic random-access memory for temporary data storage.
- **Magnetic core memory**: older memory made from magnetized rings and wires.
- **Transistor density**: number of switches placed in a given chip area.

## Mental Models

- Think of memory as a manufacturing problem as much as an architecture problem.
- Use “cheap enough to become infrastructure” when evaluating a component market.

## Anti-patterns

- **Confusing first product with enduring identity**: Intel’s later survival required abandoning DRAM.
- **Treating density as the only metric**: yields, price, and market adoption determined commercial success.

## Worked Example

Intel adapted Robert Dennard’s transistor-capacitor idea into a dense DRAM chip, replacing the hand-assembled rings of magnetic core memory. The same logic that made the cell physically smaller also made the memory market scalable.

## Key Takeaways

1. Component markets can become enormous when cost falls fast enough.
2. Memory design and manufacturing yield must be optimized together.
3. Preserve the option to change identity when the market changes.

## Connects To

- **Ch 22**: Intel later abandons the DRAM identity it created.
- **Ch 33**: x86 becomes a moat around Intel’s replacement business.
