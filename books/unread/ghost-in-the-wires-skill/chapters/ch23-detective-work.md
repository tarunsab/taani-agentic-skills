# Chapter 22: Detective Work

## Core Idea

Mitnick tries to learn who is paying Eric by using bank procedures, a supposed internal colleague, and the account name Joseph Wernle. The bank’s daily codes appear protective, but the workflow lets him create a relationship, return after the employee leaves, and pressure a coworker to reveal a value that should have been independently verified. He then follows Wernle through account balances, employer information, tax records, utility service, and a pager identifier, gradually building a story about the alias. The chapter culminates when a line-monitoring attempt reveals Eric speaking with FBI agent Ken McGuire about evidence for a search warrant, after which Mitnick begins an emergency cleanup. The practical lesson is that investigations need both data discipline and a stop rule; otherwise each new clue justifies another privacy violation.

## Frameworks Introduced

- **Layered identity investigation**: Test a person through financial, employment, residential, and communication records.
  - When to use: Only in an authorized inquiry with a defined question.
  - How: Minimize fields, record provenance, corroborate, and protect unrelated people.
- **Workflow pressure attack**: Exploit a colleague’s desire to finish a task when the original requester is unavailable.
  - When to use: As a call-center awareness scenario.
  - How: Require a known callback, manager confirmation, and transaction-specific approval.

## Key Concepts

- **Reverse social engineering**: A staged first contact that makes a later request appear to be a routine continuation.
- **Daily verification code**: A shared secret rotated by date.
- **Wernle**: The alias Mitnick investigates as a possible cover identity.
- **Cleanup mode**: Mitnick’s attempt to remove evidence after hearing about a warrant.

## Mental Models

Use “convenience creates the bypass”: a control can be defeated by the workflow built around it. Think of an investigation as a hypothesis ledger with explicit “enough evidence” criteria.

## Anti-patterns

- **Allowing a coworker’s name to stand in for authentication**.
- **Expanding from one record to a person’s whole life without necessity**.
- **Treating a revealing conversation as permission to continue the intrusion**.

## Worked Example

Mitnick persuades one employee to become a plausible predecessor and another to continue the supposed task, then uses the resulting access to identify Wernle’s bank and employer. Later, the evidence chain links Wernle’s alias to a series of records and to a call with McGuire. The lesson for defenders is to make every new request stand on its own, even when the caller supplies a believable history.

## Key Takeaways

1. Authenticate each transaction, not just the relationship around it.
2. Define data minimization and stopping rules before an investigation begins.
3. Preserve the legal boundary when the target appears to be investigating you.

## Connects To

- **ch20**: Reverse social engineering supplies the banking method.
- **ch24**: Early-warning data turns suspicion into a physical response.

