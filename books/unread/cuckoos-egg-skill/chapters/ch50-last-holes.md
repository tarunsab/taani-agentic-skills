# Chapter 50: The Last Holes

## Core Idea

The hacker returns to an editor vulnerability that Berkeley has patched, so Stoll deliberately leaves a different path available long enough to observe how the attacker adapts. The SDINET decoy becomes a rich target: the hacker tries default accounts, reads defense-contractor material, and searches for network addresses and password files at several hosts. The same pattern appears again—the systems involved are technically sophisticated or security-adjacent, yet their maintenance paths and default credentials are weak. Stoll's goal is not to maximize the hacker's access; it is to learn the remaining route while closing everything that no longer yields useful evidence.

## Frameworks Introduced

- Selective patching
- Canary account
- Attack-surface inventory

## Key Concepts

- Editor vulnerability
- SDINET defaults
- Unisys contractor
- Ingres
- Network address file

## Mental Models

- One controlled hole among closed holes
- Security weakness at the maintenance edge

## Anti-patterns

- Leave every known hole open for convenience
- Patch one host and assume the route is gone everywhere

## Worked Example

The patched editor hole blocks the old path, but the attacker practices and continues through other systems. Stoll enriches the decoy so that the next session reveals both interest and route, then records which hosts still expose useful information. The chapter's boundary is clear: controlled observation may justify one carefully scoped opening, while ordinary production vulnerabilities should be repaired.

## Key Takeaways

- Close known weaknesses except for an explicitly bounded observation path.
- Inventory defaults and maintenance interfaces across the route.
- Use decoys to reveal targeting while protecting real data.

## Connects To

- Ch 4 — Cuckoo's Egg
- Ch 37 — Field Service Account
- Ch 51 — Last Session
