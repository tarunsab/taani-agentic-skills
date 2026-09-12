# Chapter 2: The Super-User Threat

## Core Idea

The second chapter explains why a seemingly ordinary Unix account can become a laboratory-wide risk. Stoll distinguishes user-level access from super-user or root access, which can read protected files, alter programs, change accounts, and erase evidence. LBL's open scientific culture and Livermore's isolated classified environment create different exposure profiles, but neither culture makes privileged compromise impossible. The practical implication is that a security investigation must ask not only what data was viewed, but whether the intruder could change the system that records and enforces trust.

## Frameworks Introduced

- Privilege boundary
- Open-versus-isolated exposure
- Hacker/cracker distinction

## Key Concepts

- Super-user
- Root
- Protected file
- Open guest account
- Accounting trail

## Mental Models

- A normal account as a foothold
- Privilege as a change in the rules

## Anti-patterns

- Equate an open research account with harmless access
- Focus on stolen files while ignoring altered system programs

## Worked Example

Stoll's concern is not that every guest login is malicious. It is that a weak boundary can let an outsider move from reading public material to controlling the operating system. Once that happens, ordinary logs and password files may no longer be trustworthy, so the investigation has to preserve independent observations while it studies the compromised host.

## Key Takeaways

- Map what each privilege level permits before judging the incident.
- Assume a privileged intruder can tamper with both defenses and evidence.
- Compare the security boundary with the mission of the system it protects.

## Connects To

- Ch 4 — Cuckoo's Egg
- Ch 9 — Trojan Horse
- Ch 47 — Dictionary
