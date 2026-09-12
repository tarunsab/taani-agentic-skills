# Chapter 14: You Tap Me, I Tap You

## Core Idea

During a drive to Las Vegas, Mitnick investigates the strange tone associated with the monitoring boxes and continues probing Pacific Bell’s internal procedures. The chapter also contains a road-rage episode in which he uses institutional access to identify and confront another driver, revealing how quickly a technical capability can become personal retaliation. He learns that the surveillance setup covers all three of his father’s lines and that the equipment’s safeguards were poorly maintained, allowing him and Lewis to listen to other intercepts. Mitnick experiences the exchange as a contest—if investigators are listening to him, he will listen to them—but the symmetry is false because the lawful status and consequences of each side differ. The chapter’s defensive value lies in its warnings about default settings, compartmentation, and the danger of treating surveillance as a game.

## Frameworks Introduced

- **Reciprocal-surveillance trap**: A watched person may respond by watching the watchers, escalating both sides.
  - When to use: When an incident response begins to resemble a contest of pride.
  - How: Preserve legal authority, separate investigation from retaliation, and use independent oversight.
- **Default-control failure**: A system’s protection is nominal if a factory or shared default remains unchanged.
  - When to use: In every deployment and security review.
  - How: Change defaults, make each installation unique, and test whether access is logged and bounded.

## Key Concepts

- **SAS shoe**: A physical connection method described in the memoir as avoiding an audible signal.
- **Default PIN**: A manufacturer-supplied secret left unchanged by the operator.
- **Security box**: A device used to monitor or test a phone line.
- **Retaliatory curiosity**: Looking at another person’s data because they are investigating you.

## Mental Models

Use “same action, different authority”: listening, testing, or tracing must be judged by mandate and scope, not by whether the other side did something similar. Treat every default as a temporary bootstrap value, never as a control.

## Anti-patterns

- **Responding to surveillance with unauthorized surveillance**: Reciprocity does not create permission.
- **Leaving manufacturer defaults in production**: A control known to insiders is not a secret.
- **Using privileged access to settle anger**: The road-rage call shows how personal emotion can redirect a general capability.

## Worked Example

Mitnick discovers that the monitoring boxes use a shared default and that he can reach other surveillance activity. He and Lewis listen for entertainment and identify targets, including a federal judge. The episode shows why unique initialization, access logging, and separation of duties are necessary, and why a penetration test must stop at proof of exposure.

## Key Takeaways

1. Change defaults and make each security device independently configured.
2. Separate authorized monitoring from retaliatory access.
3. When a test proves a control can be bypassed, preserve evidence and stop.

## Connects To

- **ch14**: Routine technician work exposes the surveillance workflow.
- **ch16**: The contest logic shapes how Mitnick evaluates Eric.

