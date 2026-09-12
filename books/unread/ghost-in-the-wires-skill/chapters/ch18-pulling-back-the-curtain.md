# Chapter 17: Pulling Back the Curtain

## Core Idea

Mitnick seeks the full set of Pacific Bell dial-up numbers so he will no longer need to ask employees for access one office at a time. He begins with ordinary technical questions, learns who handles the relevant material, and then uses a credible engineering story to make a manager release a large paper list to Alex. The glove-wearing courier is challenged, but he improvises a less suspicious explanation and leaves with the material. The second half of the chapter applies the same chain to Eric: a diverted fax, a rental application, a cell-phone account, and a post-office box gradually connect Eric’s aliases to the FBI. The defensive lesson is about accumulation: each employee shares only a small piece, yet the chain creates a full operational picture.

## Frameworks Introduced

- **Information-chain attack**: Build a sensitive picture from individually ordinary disclosures.
  - When to use: In data-loss and social-engineering reviews.
  - How: Identify which small facts combine into a high-value set and add controls at the joins.
- **Cross-channel triangulation**: Compare independent records—rental, phone, postal, and organizational—to test an identity hypothesis.
  - When to use: In authorized fraud or incident investigation.
  - How: Record provenance, seek corroboration, and avoid treating a chain of weak clues as certainty.

## Key Concepts

- **Dial-up list**: A collection of remote access numbers for central offices.
- **Laundering a fax**: Mitnick’s name for routing a fax through intermediary locations.
- **Identity triangulation**: Linking names through multiple independent records.
- **Operational chain**: A sequence in which each handoff adds capability or context.

## Mental Models

Use “small disclosure, large composition” when measuring data sensitivity. Think of identity as a graph of corroborated relationships, not a single name on a form.

## Anti-patterns

- **Treating each low-sensitivity fact as harmless in isolation**.
- **Assuming an intermediary removes accountability**: Routing a document through another site creates more evidence, not less.
- **Accepting cross-record consistency without source provenance**.

## Worked Example

An employee first reveals where technical problems are handled, a manager provides a paper list, and a courier retrieves it. Separately, Mitnick obtains Eric’s rental application and follows the listed phone account to a Federal Building post-office box. The chain demonstrates why security teams should model combinations of data, not only individual fields.

## Key Takeaways

1. Look for combinations that turn routine facts into privileged access.
2. Add verification at every handoff and intermediary channel.
3. Triangulate identity with independent records and documented provenance.

## Connects To

- **ch04**: The institutional map becomes a multi-stage information chain.
- **ch19**: Call records provide the next layer of identity triangulation.

