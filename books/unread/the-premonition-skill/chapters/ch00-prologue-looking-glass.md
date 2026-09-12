# Prologue: The Looking Glass

**Contents position**: Prologue | **Part**: Part I

## Core Idea

Bob Glass’s agent-based model turns a population into interacting entities whose movements and contact rules can be inspected. Laura Glass recognizes that the red dots are behaving like infection and pushes the model beyond a toy by adding social networks, incubation, asymptomatic transmission, immunity, death, and age-specific contact patterns. Their most important insight is not a prediction about one epidemic but a way to see transmission as a network problem: people who make many contacts may matter more than people who are most likely to die. When they allocate a scarce flu vaccine to young people, the model shows that protecting transmitters can indirectly protect older people who are more vulnerable to death. The model also reproduces broad features of the 1957–58 pandemic, which gives the simple abstraction credibility without turning it into a perfect representation. The prologue therefore establishes the book’s recurring method: make an inspectable model, use it to expose a neglected leverage point, then test the implication against history and reality.

## Frameworks Introduced

- **Agent-based modeling**: Represent individuals, schedules, contacts, and state changes, then let the system’s behavior emerge.
  - When to use: When aggregate averages hide who transmits, who is exposed, or where an intervention acts.
  - How: Define actors and interaction rules; add only the disease and social variables needed for the question; compare interventions.
- **Transmission-node targeting**: Protect or remove the people who connect many others, even when they are not the people most likely to die.
  - When to use: When a scarce intervention must reduce spread as well as individual risk.
  - How: Map contact patterns, identify high-contact groups, and test whether reducing their transmission protects the wider network.

## Key Concepts

- **Useful abstraction**: A simplified representation judged by whether it helps solve a problem.
- **Social network**: The pattern of relationships and repeated contacts through which a pathogen can move.
- **Incubation period**: Time infected but not yet infectious or symptomatic.
- **Asymptomatic transmission**: Spread by people who do not show symptoms.
- **Network removal**: Taking a person out of active contacts through immunity, isolation, or death.
- **Science as engineering**: Learning the system in order to intervene in it.

## Mental Models

- Use **colored dots** when you need to explain a system’s mechanism to people who cannot follow its mathematics.
- Think of vaccination as both **individual protection** and **network editing**.
- Ask whether the model’s answer changes when you vary the assumptions that matter most.

## Worked Example

The first model let people infect one another whenever they passed, which Laura correctly saw as unrealistic. She and Bob surveyed hundreds of people about hugs, shared seats, proximity, and time spent together, then used those data to make age groups and social networks more realistic. The model tested a flu-like pathogen and compared vaccination strategies. Giving the vaccine to young people removed their ability to transmit, and the older people never received the disease in the simulation. The example demonstrates how a child’s objection about realism can improve a model and change the intervention question from “Who dies?” to “Who spreads?”

## Distinctions & Limits

The Glass model is crude by design: it omits college students and other social behaviors, and its infection probabilities are assumptions rather than direct observations. Its value is not that it reproduces every individual event; it is that it makes hidden causal structure visible and generates a question experts can test. The state science-fair result is evidence that the model captured something useful, not proof that every policy conclusion is universal. A model can also mislead if its contact map, compliance assumptions, or pathogen properties are wrong. Keep the abstraction inspectable and use it to direct fieldwork.

## Anti-patterns

- **Treating the model as the world**: Output is conditional on rules and assumptions.
- **Protecting only the most vulnerable individuals**: Mortality risk and transmission leverage can point to different groups.
- **Adding complexity without a decision**: Detail is useful only when it improves the problem being solved.

## Key Takeaways

1. Start with the smallest model that can answer the decision question.
2. Make contacts and delays explicit.
3. Test interventions on transmission structure, not only on mortality categories.
4. Use surprising output to decide what to measure next.

## Connects To

- **Ch 3 — The Pandemic Thinker**: Glass’s model becomes evidence for federal pandemic planning.
- **Ch 4 — Stopping the Unstoppable**: School closure appears as a nonlinear leverage point.
- **Ch 10 — The Bug in the System**: Genomic data later reveal the real network behind the dots.
