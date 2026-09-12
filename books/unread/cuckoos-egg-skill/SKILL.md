---
name: cuckoos-egg-skill
description: "Knowledge base from \"Cuckoo's Egg\" by Clifford Stoll. Use when studying or applying the book's lessons on incident observation, network tracing, privilege, evidence, responsibility, and computer security."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Cuckoo's Egg
**Author**: Clifford Stoll | **Source**: EPUB text extraction | **Chapters**: 56 + Epilogue | **Mode**: text / study | **Generated**: 2026-09-12

## How to Use This Skill

- Without arguments, load the core frameworks below.
- With a topic, read the relevant chapter file and supporting index.
- With a chapter number, open its linked note in chapters/.
- Use glossary.md for terms, patterns.md for reusable investigative patterns, and cheatsheet.md for decisions.

This is a study-oriented knowledge base, not a reproduction of the book. The chapter files carry the explanatory detail; the master file is intentionally compact.

## Core Frameworks & Mental Models

**Start with the small anomaly.** Use a reproducible discrepancy as a lead even when its immediate value is tiny. Stoll's seventy-five-cent mismatch exposes the Hunter account, and the next login turns bookkeeping into a security investigation. The anomaly is not proof of motive; it is valuable because it can be checked and because the response to a controlled change may reveal the next state.

**Observe outside the trust boundary.** When a privileged intruder can alter programs, accounts, and logs, the observed host cannot be the only witness. Stoll builds watchdogs, printers, pagers, and physical monitoring around the compromised machines. Independent observation is awkward and incomplete, but it preserves a signal when local evidence is suspect.

**Model the privilege chain.** Describe compromise as a sequence: stolen credential, program alteration, privilege gain, protected access, persistence, and cleanup. The cuckoo's egg metaphor captures a hostile program using the legitimate system's own lifecycle to hatch elevated authority. This model identifies both repair points and evidence that may no longer be trustworthy.

**Separate route, target, access, identity, and motive.** A German network path is not a named person; a military keyword is not proof that data was copied; a common exploit is not proof of a common actor. Stoll keeps these claims distinct and strengthens them with independent observations such as timing, account choices, typing errors, physical mail, and local traces. This prevents an attractive theory from silently becoming a fact.

**Use bounded decoys to buy information.** Operation Showerhead uses synthetic, bureaucratic SDINET documents to keep the intruder reading long enough for a manual telephone trace. The decoy is an experiment with approval, restricted content, monitoring, and a purpose-specific stop condition. Plausibility makes it useful; real secrets or theatrical bait would change the risk and the signal.

**Treat trust as an externality.** A network connects institutions that have different missions, thresholds, and legal powers. Closing one route may protect a host while moving the attacker elsewhere, and ignoring a nonmonetary incident may leave a shared system unsafe. Stoll's responsibility is therefore wider than his job description, but it remains bounded by evidence, safety, and cooperation.

**Balance security with mission and usability.** The book rejects both careless openness and a fantasy of perfect isolation. Password rules, patches, compartmentalization, monitoring, and disclosure all carry costs, and the right choice depends on what the system does and what evidence remains to collect. Protecting openness requires making trust failures observable and repairable.

## Chapter Index

| # | Title | Key frameworks |
|---|---|---|
| [1](chapters/ch01-seventy-five-cent-mystery.md) | The Seventy-Five-Cent Mystery | Anomaly as lead, Reproducible observation |
| [2](chapters/ch02-super-user-threat.md) | The Super-User Threat | Privilege boundary, Open-versus-isolated exposure |
| [3](chapters/ch03-looking-for-footprints.md) | Looking for Footprints | Distributed monitoring, Astronomical observation method |
| [4](chapters/ch04-cuckoos-egg.md) | The Cuckoo's Egg | Privilege-escalation chain, Cuckoo's-egg metaphor |
| [5](chapters/ch05-keep-the-doors-open.md) | Keep the Doors Open | Containment-versus-observation decision, Known flaw versus unknown persistence |
| [6](chapters/ch06-watchdog-and-wiretap.md) | The Watchdog and the Wiretap | Watchdog architecture, Independent observation |
| [7](chapters/ch07-physics-problem.md) | The Physics Problem | Physics-style inference, One-way password verification |
| [8](chapters/ch08-first-military-target.md) | The First Military Target | Escalation by impact, Network-versus-telephone visibility |
| [9](chapters/ch09-trojan-horse.md) | The Trojan Horse | Trojan-horse pattern, Interface deception |
| [10](chapters/ch10-library-stakeout.md) | The Library Stakeout | Hypothesis testing, Physical corroboration |
| [11](chapters/ch11-robbing-the-dead.md) | Robbing the Dead | Dormant-account exploitation, Post-session reconstruction |
| [12](chapters/ch12-network-neighborhood.md) | The Network Neighborhood | Network topology as context, Mission-versus-means distinction |
| [13](chapters/ch13-trace-without-a-number.md) | A Trace Without a Number | Trace-chain coordination, Deadline-driven investigation |
| [14](chapters/ch14-calling-the-spooks.md) | Calling the Spooks | Cross-domain escalation, Clue-to-contact mapping |
| [15](chapters/ch15-spooks-visit.md) | The Spooks Visit | Compartmentalization, Trust boundary |
| [16](chapters/ch16-research-not-revenge.md) | Research, Not Revenge | Research framing, System boundary mapping |
| [17](chapters/ch17-the-echo.md) | The Echo | Round-trip timing, Calibration by comparison |
| [18](chapters/ch18-mirror-notebook.md) | The Mirror Notebook | Behavioral baseline, Discreet decoy |
| [19](chapters/ch19-benson-and-hedges.md) | Benson and Hedges | Password reuse as signature, Clue aggregation |
| [20](chapters/ch20-elxsi-trap.md) | The Elxsi Trap | Behavioral fingerprinting, Controlled slowdown |
| [21](chapters/ch21-responsible.md) | Responsible | Responsibility beyond mandate, Shared-infrastructure model |
| [22](chapters/ch22-phone-number.md) | The Phone Number | Legal-technical bridge, Assumption checking |
| [23](chapters/ch23-mitre.md) | Mitre | Independent corroboration, Gateway-versus-origin distinction |
| [24](chapters/ch24-mclean-connection.md) | The McLean Connection | Triangulation, Independent case comparison |
| [25](chapters/ch25-correlation.md) | Correlation | Correlation analysis, Stepping-stone detection |
| [26](chapters/ch26-trail-on-the-bill.md) | The Trail on the Bill | Parallel obligations, Infrastructure intervention |
| [27](chapters/ch27-fox-and-hound.md) | The Fox and the Hound | Persistent monitoring loop, Signal-versus-noise discipline |
| [28](chapters/ch28-hackers-hours.md) | The Hacker's Hours | Temporal profiling, Behavioral baseline |
| [29](chapters/ch29-across-the-atlantic.md) | Across the Atlantic | Layered network tracing, Virtual-circuit reasoning |
| [30](chapters/ch30-germany.md) | Germany | Progressive localization, Multi-signal attribution |
| [31](chapters/ch31-the-noise.md) | The Noise | Selective interference, Route redundancy |
| [32](chapters/ch32-the-profile.md) | The Profile | Behavioral profiling, Adversarial questioning |
| [33](chapters/ch33-closing-circle.md) | Closing the Circle | Cross-site corroboration, Distributed detection gap |
| [34](chapters/ch34-operation-showerhead.md) | Operation Showerhead | Decoy information environment, Time-on-target extension |
| [35](chapters/ch35-german-search-warrant.md) | The German Search Warrant | International legal handoff, Contemporaneous documentation |
| [36](chapters/ch36-new-years-day.md) | New Year's Day | Impact-based escalation, Evidence loss through instrumentation failure |
| [37](chapters/ch37-field-service-account.md) | The Field Service Account | Default-account failure, Privilege persistence |
| [38](chapters/ch38-medical-computer.md) | The Medical Computer | Containment by controlled failure, Safety-critical context |
| [39](chapters/ch39-fbis-towel.md) | The FBI's Towel | Bailiwick failure, Institutional escalation |
| [40](chapters/ch40-bait.md) | Bait | Time-extension bait, Plausible decoy design |
| [41](chapters/ch41-wrong-nest.md) | The Wrong Nest | Bounded authorization, Decoy iteration |
| [42](chapters/ch42-the-net.md) | The Net | Converging trace, Distributed exposure |
| [43](chapters/ch43-german-clues.md) | The German Clues | Cross-site pattern matching, Default-account audit |
| [44](chapters/ch44-networks-shoemakers.md) | The Network's Shoemakers | Defense-in-depth failure, Organizational exposure mapping |
| [45](chapters/ch45-case-for-staying-open.md) | The Case for Staying Open | Risk-based decision, Documented-case method |
| [46](chapters/ch46-political-boundaries.md) | Political Boundaries | Ethical boundary setting, Controlled-interest experiment |
| [47](chapters/ch47-the-dictionary.md) | The Dictionary | Dictionary-attack model, Offline verification risk |
| [48](chapters/ch48-human-adversary.md) | The Human Adversary | Human-adversary model, Compartmentalization |
| [49](chapters/ch49-the-letter.md) | The Letter | Canary document, Physical-digital corroboration |
| [50](chapters/ch50-last-holes.md) | The Last Holes | Selective patching, Canary account |
| [51](chapters/ch51-last-session.md) | The Last Session | Case separation, Breadcrumb decoy |
| [52](chapters/ch52-the-search.md) | The Search | Technical-to-legal handoff, Post-incident hardening |
| [53](chapters/ch53-chaos-club.md) | The Chaos Club | Vulnerability disclosure, Case differentiation |
| [54](chapters/ch54-publishing.md) | Publishing | Responsible disclosure, Peer review |
| [55](chapters/ch55-markus-hess.md) | Markus Hess | Attribution reconstruction, Collaborator-role separation |
| [56](chapters/ch56-returning-to-astronomy.md) | Returning to Astronomy | Security trade-off model, Responsibility through attention |
| [Epilogue](chapters/epilogue.md) | After the Hunt | Life after incident, Recurring-threat awareness |

## Topic Index

- **Anomaly and accounting** → Ch 1, Ch 7
- **Attribution and profiling** → Ch 19, Ch 28, Ch 30, Ch 32, Ch 55
- **Decoys and canaries** → Ch 34, Ch 40, Ch 41, Ch 49
- **Evidence and logbooks** → Ch 3, Ch 7, Ch 35, Ch 52, Ch 54
- **International tracing** → Ch 13, Ch 22, Ch 29, Ch 30, Ch 33, Ch 42
- **Passwords and credentials** → Ch 2, Ch 9, Ch 11, Ch 19, Ch 37, Ch 47
- **Privilege and system integrity** → Ch 4, Ch 16, Ch 37, Ch 38, Ch 50
- **Responsibility and institutions** → Ch 5, Ch 12, Ch 21, Ch 39, Ch 45, Ch 48
- **Safety-critical systems** → Ch 36, Ch 37, Ch 38
- **Trust, openness, and disclosure** → Ch 21, Ch 45, Ch 53, Ch 54, Ch 56

## Supporting Files

- [glossary.md](glossary.md) — alphabetized terms and definitions
- [patterns.md](patterns.md) — source-grounded investigative patterns
- [cheatsheet.md](cheatsheet.md) — compact decision rules and trade-offs

## Scope & Limits

This private skill covers Clifford Stoll's *Cuckoo's Egg* as synthesized study notes from one EPUB. The source structure supports 56 numbered chapters and an Epilogue; no separate prologue was present. The extracted text contains about 116.7K words, and 71 EPUB images were omitted by the text extraction, so image-only material is not represented. Chapter titles here are descriptive labels because the source navigation exposed chapter numbers rather than a complete title list. The notes preserve the narrative's defensive and investigative lessons without reproducing the book text or providing operational instructions for unauthorized access.
