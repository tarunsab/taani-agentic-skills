# Chapter 28: Trophy Hunter

## Core Idea

Mitnick describes hacking as entertainment and source code as a trophy whose value comes from the difficulty of obtaining it. He targets Novell, Nokia, NEC, and other manufacturers, using a mixture of technical weaknesses, internal telephone calls, helpful employees, and storage on compromised systems. The chapter repeatedly shows that the technical path is only one part of the system: developers and administrators are persuaded to move information, while monitoring programs and email eventually reveal that the FBI and system administrators are watching. The “trophy” motive explains why financial gain is not a sufficient model for threat assessment; the challenge, status, and learning can be the reward. Defensively, the chapter calls for protecting intellectual property, monitoring unusual source access, and responding to the human pathway as seriously as the software flaw.

## Frameworks Introduced

- **Trophy motive**: The target’s symbolic value and difficulty sustain repeated escalation.
  - When to use: In threat modeling where no obvious financial motive exists.
  - How: Monitor behavior, access patterns, and interest in proprietary internals, not only transactions.
- **Human–technical compound path**: Technical access and social persuasion reinforce each other.
  - When to use: In source-code and product-security reviews.
  - How: Require approval for unusual transfers, isolate development systems, and correlate logs with calls and account changes.

## Key Concepts

- **Source-code trophy**: Proprietary implementation material valued as proof of mastery.
- **Development cluster**: Systems used by engineers to build or share product code.
- **Backdoor**: An unauthorized alternate path into a system; included here as a risk category.
- **Monitoring program**: Software used by administrators or investigators to observe activity.
- **“Ivan Boesky thinking”**: Assuming unauthorized access must be motivated by money.

## Mental Models

Use “curiosity is a motive” when modeling threats. Think of source protection as a graph problem: code, developer accounts, build systems, storage, and transfer paths all matter.

## Anti-patterns

- **Looking only for theft or financial gain**.
- **Protecting the central repository while leaving developer workflows weak**.
- **Ignoring alerts because the attacker appears to be collecting rather than damaging**.

## Worked Example

Mitnick gets source from several cellular manufacturers, then notices an email saying files have appeared on a monitored Los Angeles site. He investigates the monitoring and realizes that administrators and federal agents are observing the systems used for storage. The source-specific defensive lesson is to detect the entire path from developer account to transfer destination and to alert on bulk or unusual access.

## Key Takeaways

1. Include challenge, status, and curiosity in threat models.
2. Correlate human requests with source-code and account activity.
3. Treat collection-only behavior as a serious incident.

## Connects To

- **ch09**: The trophy idea begins with DEC source code.
- **ch33**: A technical triumph becomes the trigger for the final pursuit.

