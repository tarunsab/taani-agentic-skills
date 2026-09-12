# Chapter 35: Game Over

## Core Idea

By February 1995, a joint effort involving federal officials, private organizations, journalists, and Shimomura is closing in on Mitnick. The memoir describes an unusually blurred boundary between public investigation and a private technical expert who receives confidential information and assists the pursuit. A storage anomaly on the Well reveals files connected to Shimomura, while cellular monitoring and voice recognition narrow the search to Raleigh. The chapter’s operational lesson is not to reproduce those methods but to understand how disparate clues become powerful when combined. It also raises a governance lesson: extraordinary investigative arrangements need clear legal authority, documented roles, and independent oversight.

## Frameworks Introduced

- **Triangulated geolocation**: Time, device signals, account artifacts, and human recognition can converge on a location.
  - When to use: In incident response with proper legal process.
  - How: Corroborate independent sources and record confidence rather than treating one signal as decisive.
- **Public-private boundary review**: A private expert assisting an official investigation can create legal and accountability risk.
  - When to use: In investigations, managed security services, and evidence handling.
  - How: Define authority, access, retention, disclosure, and review before work begins.
- **Anomaly-led investigation**: A routine capacity or account alert can expose an unrelated compromise.

## Key Concepts

- **Clue fusion**: Combining weak, independent signals into a stronger assessment.
- **De facto government agent**: A private actor whose practical role may resemble official investigative work.
- **Voice recognition**: Human identification used as one input in a larger evidence chain.

## Mental Models

Use an evidence graph with source, collection authority, timestamp, reliability, and dependence. Independent clues deserve more weight than multiple reports copied from one original claim.

## Anti-patterns

- Giving a private investigator broad access without written scope and oversight.
- Treating a capacity alert as proof of who created the files.
- Combining signals without preserving their legal and evidentiary provenance.

## Worked Example

An incident team sees an unexpected storage spike, finds files addressed to a sensitive account, and correlates a later device signal with a recognized voice. Each clue is incomplete; together they justify a carefully authorized next step. The report should still distinguish correlation, identification, and legal conclusions.

## Key Takeaways

1. Weak signals become powerful when independent and properly correlated.
2. Private expertise does not remove the need for public authority and oversight.
3. Operational success and legal legitimacy are separate questions.

## Connects To

- **ch19**: Traffic analysis turns metadata into behavioral inference.
- **ch37**: A surveillance net can still fail at the final identification step.
