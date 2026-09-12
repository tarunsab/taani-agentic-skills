# Chapter 37: The Field Service Account

## Core Idea

The hacker reaches an Air Force Systems Command VAX/VMS system through a default field-service account and receives broad system privileges, then disables accounting, explores thousands of files, and locks himself out by mishandling password expiration. Days later the account is re-enabled, and the hacker adds a former colonel's account with a new privileged password, exposing how quickly a repaired boundary can be reopened. Stoll warns the Air Force and learns that the intruder selects operationally meaningful documents rather than indiscriminately reading everything. German traces move through RCA, satellite links, Karlsruhe, and Hannover, tying the local incident to the international route.

## Frameworks Introduced

- Default-account failure
- Privilege persistence
- Operational targeting

## Key Concepts

- VMS system privilege
- Field/service account
- Password expiration
- Air Force Systems Command
- RCA trace

## Mental Models

- A maintenance account as a master key
- The attacker curates a collection

## Anti-patterns

- Leave vendor or maintenance accounts at defaults
- Assume a locked account remains closed after a routine re-enable

## Worked Example

The first VMS session demonstrates how a forgotten maintenance credential can grant more than the operator intended. The later reactivation demonstrates that a system can be vulnerable again even after a suspicious account is noticed. Stoll's review of the selected files supports a sharper conclusion about intent: the hacker is looking for specific military information, not merely testing every file.

## Key Takeaways

- Inventory and protect maintenance accounts.
- Audit every re-enable and privilege change.
- Distinguish file selection from mere directory traversal when assessing intent.

## Connects To

- Ch 8 — First Military Target
- Ch 43 — German Clues
- Ch 50 — Last Holes
