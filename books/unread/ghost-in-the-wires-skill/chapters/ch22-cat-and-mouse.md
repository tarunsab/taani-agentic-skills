# Chapter 21: Cat and Mouse

## Core Idea

Mitnick joins Terry Hardy, Lewis, and Teltec investigators in targeting Pacific Bell security personnel, turning the “cat and mouse” metaphor into a working identity. A line-monitoring stunt gives them access to a security investigator’s voicemail and becomes a way for Mitnick to prove his usefulness to Teltec. The chapter also shows the operational danger of shared access: a technician can be induced to place a connection on a sensitive line, while the people using the connection treat the result as a game. Mitnick’s work for Teltec sometimes helps locate missing people or assets, but the same environment also asks him to examine law-enforcement targets. The distinction between legitimate investigation and retaliatory curiosity becomes harder to maintain as the participants praise one another’s cleverness.

## Frameworks Introduced

- **Cat-and-mouse escalation**: Each side observes, adapts, and raises the stakes in response to the other.
  - When to use: In adversarial security exercises.
  - How: Define authority, objective, stop conditions, and a neutral referee before the contest begins.
- **Proof-by-demonstration**: A person tries to establish credibility by showing access to a target or secret.
  - When to use: In authorized assessments or vendor demonstrations.
  - How: Use synthetic or client-approved data; never prove capability by exposing a real person’s account.

## Key Concepts

- **SAS shoe**: A line-connection method described in the source as difficult for the target to notice.
- **Voicemail target**: A person whose messages become an information source.
- **Teltec Investigations**: The private-investigation workplace that employs Mitnick.
- **Cat-and-mouse game**: Reciprocal adaptation between pursuer and evader.

## Mental Models

Use “a proof can be an incident”: demonstrating access to a real account creates harm even if no files are changed. Think of adversarial work as a game only when an independent party controls the rules.

## Anti-patterns

- **Proving skill on a real person’s voicemail**.
- **Letting the target define the scope by asking for more**.
- **Assuming a private-investigation job makes every technique lawful**.

## Worked Example

Mitnick and Terry target a Pacific Bell security investigator’s voicemail and infer the access code from the tones of a live call. They repeat the process against another investigator and check messages after hours. The source-specific defensive lesson is to enforce unique authentication, alert on anomalous access, and keep investigators from using privileged channels for personal experiments.

## Key Takeaways

1. A demonstration on a live account is not a safe proof of concept.
2. Separate authorized investigation from adversarial retaliation.
3. Put an independent scope owner between competing teams.

## Connects To

- **ch15**: The reciprocal-surveillance logic becomes a social game.
- **ch23**: The search for Eric expands into financial and investigative records.

