# Chapter 20: Reverse Sting

## Core Idea

Mitnick presents the DMV as a rich information source and then extends the search through banking and tax records. He uses reverse social engineering: first creating a relationship or plausible pending request, then returning as a coworker who needs the earlier employee’s information to complete the task. The method works because employees want to help one another and do not want to block a colleague’s work, while the daily verification codes are treated as procedural theater rather than as a real identity check. Mitnick eventually links the supposed Eric/Wernle identity to an employer, bank activity, and tax records, yet the resulting picture remains partly speculative. The chapter is a defensive blueprint for redesigning verification: a process must authenticate the person, the request, the destination, and the authority independently.

## Frameworks Introduced

- **Reverse social engineering**: Establish a plausible interaction first, then use the expected follow-up to obtain access or information.
  - When to use: As an awareness scenario for call centers, banks, and government offices.
  - How: Treat unplanned callbacks, coworker references, and “we already discussed this” claims as new requests requiring fresh verification.
- **Code-of-the-day weakness**: A rotating code fails when employees can be socially induced to reveal it.
  - When to use: When reviewing shared-secret procedures.
  - How: Replace verbal secrets with strong identity binding, transaction limits, and independent approval.

## Key Concepts

- **Soundex**: The DMV term Mitnick says was used for a driver’s-license image request.
- **Daily code**: A rotating internal verification value.
- **Signature card**: A bank record associated with an account holder.
- **Integrated Data Retrieval System (IDRS)**: The IRS system referenced in the memoir.
- **Reverse social engineering**: A staged interaction that makes later access appear like routine follow-up.

## Mental Models

Use “verification must survive the second call”: a prior conversation should not authenticate a new caller. Think of a secret as weak when the process makes employees responsible for revealing it.

## Anti-patterns

- **Accepting a colleague’s name as approval**.
- **Letting urgency, hierarchy, or fear of blocking work override verification**.
- **Treating a rotating code as strong authentication when it is shared verbally**.

## Worked Example

Mitnick first speaks with a bank employee as a prospective customer, learns when she will be away, and later calls as a colleague who needs to continue the earlier task. When challenged for a daily code, he pressures the employee by saying the information cannot be sent without it, then exploits confusion among code labels. The defensive version is simple: a callback to a known number and a second approver must be independent of the original conversation.

## Key Takeaways

1. A previous interaction does not authenticate a later caller.
2. Replace shared verbal secrets with independent identity and transaction controls.
3. Keep financial and government-record investigations within lawful scope and data minimization.

## Connects To

- **ch04**: The correction lure and institutional map support the same social-engineering pattern.
- **ch22**: The investigation moves from data collection to direct surveillance of a security investigator.

