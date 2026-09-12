# Chapter 9: The Kevin Mitnick Discount Plan

## Core Idea

After a period of apparent reform, Mitnick tests whether a cellular phone can be made to appear associated with someone else’s subscriber identity. The technical premise matters less than the method: he chooses a noisy public setting, researches the manufacturer, uses a plausible internal role, and turns a routine support interaction into access to a powerful configuration change. The successful demonstration gives him what he calls invisibility, but it also reveals relapse in real time; he wonders whether the act was a one-off or a return to hacking. The chapter’s practical lesson is that security depends on both technical binding and human authorization. If support staff can change identity-linked settings based on a convincing story, the system’s accounting and traceability can be defeated without breaking the cryptography of the network.

## Frameworks Introduced

- **Context-supported pretext**: A believable environment, role, and technical detail reinforce one another.
  - When to use: Defensively, when evaluating call-center and vendor-support workflows.
  - How: Verify identity out of band, limit sensitive changes, and log the requester and approver.
- **Relapse signal**: A successful challenge immediately restores the emotional reward of the old activity.
  - When to use: When someone is trying to stop a compulsive or prohibited behavior.
  - How: Treat the first “just to see if it works” act as a warning and change access to the trigger.

## Key Concepts

- **ESN**: Electronic serial number associated with a cellular handset.
- **MIN**: Mobile identity number used with the phone’s subscriber record.
- **Cloning**: Making a device appear associated with another subscriber identity.
- **Invisibility**: Mitnick’s subjective sense that tracing would point elsewhere.

## Mental Models

Use “identity binding” to ask whether device, subscriber, person, and transaction are tied together by independent evidence. Use “first success is the risk point”: a successful test can be more reinforcing than a failed attempt.

## Anti-patterns

- **Allowing support staff to change identity-linked attributes from a phone call alone**.
- **Treating a controlled demonstration as harmless when it affects a real subscriber**.
- **Ignoring the emotional meaning of a relapse**: The question is not only what changed technically, but what reward returned.

## Worked Example

Mitnick calls a phone manufacturer from the Consumer Electronics Show so the background noise supports his claimed location. He reaches an engineer, obtains help with a handset configuration, and confirms the result by placing a call. He does not use the access for purchases, but the method still creates risk for another customer and undermines billing and traceability. The correct defensive response is stronger caller verification and dual approval for identity changes.

## Key Takeaways

1. Bind identity changes to independent verification and approval.
2. Treat a successful “harmless” test as a relapse and control signal.
3. Evaluate traceability across the whole transaction chain.

## Connects To

- **ch11**: The renewed appetite for challenge draws Mitnick toward Eric Heinz.
- **ch39**: Authorization converts controlled demonstrations into professional assessments.

