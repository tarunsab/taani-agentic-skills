# Chapter 52: The Search

## Core Idea

German police coordinate with the Bundespost and the FBI, then search Focus Computer GmbH and an apartment in Hannover, seizing more than eighty disks and copying material for the investigation. Stoll patches the original privilege flaw, expires passwords, and adds traps, while the FBI tells him not to contact the suspect or publicize the case. He begins writing a scientific paper because the investigation has produced a reproducible account of network behavior, evidence handling, and institutional response. The search converts a long technical observation into legal action, but it does not by itself answer every question about collaborators, buyers, or motive.

## Frameworks Introduced

- Technical-to-legal handoff
- Post-incident hardening
- Scientific write-up

## Key Concepts

- Focus Computer GmbH
- Hannover apartment
- Disks
- Password expiration
- Evidence copy

## Mental Models

- The handoff packet
- Hardening after observation

## Anti-patterns

- Contact the suspect directly after identification
- Assume seizure resolves attribution and policy questions

## Worked Example

The German search is possible because the network trace, account evidence, and U.S.-German communication have been assembled into an actionable case. Stoll then closes the original route and changes credentials, acknowledging that the observation phase is over. Writing the paper preserves the method so the case can teach more than the identities of those arrested.

## Key Takeaways

- Preserve a complete handoff from technical records to legal action.
- Harden systems immediately after the observation phase ends.
- Publish the generalizable method only through an appropriate review and disclosure process.

## Connects To

- Ch 35 — German Search Warrant
- Ch 54 — Publishing
- Ch 55 — Markus Hess
