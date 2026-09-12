# Chapter 11: Robbing the Dead

## Core Idea

The first warrant-supported trace reaches through AT&T toward Virginia and New Jersey, but the line drops before the investigators can identify the endpoint. Reviewing the session afterward, Stoll finds that the intruder used several abandoned accounts, became super-user, erased or changed credentials, and probed Air Force systems. “Robbing the dead” describes the exploitation of dormant accounts whose owners no longer notice or report misuse. The chapter shows why a trace can fail operationally while still producing strong after-session evidence about persistence and account selection.

## Frameworks Introduced

- Dormant-account exploitation
- Post-session reconstruction
- Trace fragility

## Key Concepts

- Abandoned account
- Password change
- Credential cleanup
- Virginia route
- Air Force probe

## Mental Models

- The dead account as an unlocked door
- The failed live trace, successful forensic trace

## Anti-patterns

- Assume unused accounts are harmless
- Judge a trace only by whether it names a street address

## Worked Example

The live telephone trace breaks, but the Berkeley logs show a pattern: the intruder shifts among accounts and leaves some of them unusable. That pattern is more informative than any single failed call because it reveals a repeatable strategy for extending access. Stoll's review turns an operational disappointment into an account-hygiene lesson.

## Key Takeaways

- Audit and retire dormant accounts.
- Preserve post-session state changes as evidence.
- Measure an investigation by the quality of the model it improves, not only by immediate attribution.

## Connects To

- Ch 19 — Benson and Hedges
- Ch 25 — Correlation
- Ch 47 — Dictionary
