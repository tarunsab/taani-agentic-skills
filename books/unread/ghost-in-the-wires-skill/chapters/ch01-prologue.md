# Prologue: From Intrusion to Penetration Test

## Core Idea

The prologue presents a physical and technical penetration test as a chain of ordinary weaknesses rather than a single magical break-in. A tester uses reconnaissance, social trust, physical access, local privilege, remote access, and poorly protected administrative material to demonstrate how a company’s layers can fail together. The important lesson is systemic: a locked door, an access card, an administrator account, and encrypted customer data do not provide meaningful protection if people routinely bypass procedures or leave the decryption path available to broad administrative access. Mitnick contrasts this scenario with his earlier crimes to establish the memoir’s central ethical distinction: the techniques may resemble one another, but a commissioned test has a bounded purpose and gives the owner a chance to repair the gaps. Read the chapter as a defensive anatomy of trust, defaults, privilege, and detection—not as an instruction set for unauthorized access.

## Frameworks Introduced

- **Layered weakness chain**: Small failures compound across physical, human, host, network, and data layers.
  - When to use: When reviewing whether a security control is actually resilient.
  - How: Test each layer and then test the transitions between layers; a control is weak if the next layer silently trusts its result.
- **Authorization boundary**: The same capability is legitimate only when the owner has explicitly scoped and approved the work.
  - When to use: Before any security assessment or demonstration.
  - How: Confirm written permission, targets, dates, allowed techniques, evidence handling, and stop conditions.

## Key Concepts

- **Tailgating**: Entering behind an authorized person because courtesy overrides the access rule.
- **Privilege escalation**: Moving from a limited foothold to broader control.
- **Remote access Trojan**: Malware that gives an outside operator persistent control; here it is evidence of a compromise, not a recommended tool.
- **Password hash**: A transformed password value that can still become useful if protections are weak.
- **Defense in depth**: Multiple independent controls whose failure does not automatically expose the whole environment.

## Mental Models

Think in chains, not walls: ask what each control assumes about the previous one. Use the “authorized adversary” model to expose real paths while preserving scope and evidence.

## Anti-patterns

- **Trusting appearance or courtesy as identity proof**: A badge, uniform, or confident manner is not authentication.
- **Leaving privileged paths and encryption keys broadly reachable**: Encryption does not help if the key is stored where every administrator can retrieve it.
- **Testing without scope**: An unauthorized proof of capability becomes a new incident.

## Worked Example

The prologue’s commissioned assessment moves from a building entrance to an IT office, then to a workstation, administrative access, domain-wide account material, and a protected transaction database. The tester stops short of using customer numbers and reports the chain to the client. The value is not the specific tools; it is the evidence that physical access, weak internal trust, privileged accounts, and key management must be reviewed together.

## Key Takeaways

1. Review the transitions between controls, not only each control in isolation.
2. Treat human courtesy, defaults, and administrative convenience as attack surface.
3. Establish authorization and evidence boundaries before testing.

## Connects To

- **ch00**: Wozniak’s motive–impact–authorization distinction becomes concrete.
- **ch39**: The memoir closes by naming authorization as the professional dividing line.

