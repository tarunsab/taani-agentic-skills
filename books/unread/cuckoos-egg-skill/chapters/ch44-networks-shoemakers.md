# Chapter 44: The Network's Shoemakers

## Core Idea

German officials, U.S. agencies, and military system managers struggle to coordinate while Stoll creates more fake SDI material to keep the investigation alive. The hacker uses default access on a BBN Butterfly VAX, creates privileged accounts, and reaches Rochester to steal integrated-circuit designs, confirming that the campaign is not limited to military keywords. German investigators report that the route involves a company and many people, not just a single anonymous university terminal, and characterize the activity as harmful rather than benign exploration. The “shoemakers' children” image captures the irony that organizations building secure systems often leave their own administrative paths poorly protected.

## Frameworks Introduced

- Defense-in-depth failure
- Organizational exposure mapping
- Decoy enrichment

## Key Concepts

- BBN Butterfly
- Rochester
- Integrated-circuit designs
- Company route
- Default access

## Mental Models

- The shoemaker's children
- A network made of neglected edges

## Anti-patterns

- Assume a security contractor is secure by reputation
- Treat one compromised host as the whole campaign

## Worked Example

The intruder follows a chain of easy accounts through a system associated with networking research and ends at valuable chip designs. Stoll's fake files continue to occupy the attacker, but the real target demonstrates the cost of weak boundaries at every link. The German report broadens the model from “one hacker at a university” to a networked group or business context without yet resolving each participant's role.

## Key Takeaways

- Audit the administrative edges of security-sensitive organizations.
- Trace the whole route, including service providers and contractors.
- Separate the operator who enters a system from every person who may benefit from the data.

## Connects To

- Ch 25 — Correlation
- Ch 45 — Case for Staying Open
- Ch 55 — Markus Hess
