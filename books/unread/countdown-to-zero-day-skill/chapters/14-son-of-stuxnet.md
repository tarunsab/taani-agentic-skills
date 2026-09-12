# Chapter 14: Son of Stuxnet

## Thesis

Duqu showed that the Stuxnet episode was not only about one destructive payload; it also revealed a family of reconnaissance and espionage tools designed to prepare future operations. CrySyS Lab researcher Boldizsár Bencsáth found a signed, encrypted infection at a Hungarian company and recognized overlaps in encryption, driver behavior, and platform design. Symantec named it Duqu after its `~DQ` files and found a remote-access and information-stealing framework rather than a PLC saboteur. The chapter demonstrates how researchers infer relationship from shared engineering choices while resisting the stronger claim that two tools necessarily have the same authors or mission.

## Mechanism and source evidence

Duqu used a kernel driver, keylogging, document and design-file theft, encrypted communications, proxy infrastructure, and modular downloads. Its targets included strategic manufacturers and organizations linked to Iran, and the stolen material included AutoCAD and industrial-network designs that could support later targeting. Unlike Stuxnet, it did not autonomously spread broadly; it relied on manual delivery and removed itself after a configurable period. Kaspersky found a shared “Tilde-d” platform and similar development habits, while the CrySyS report, victim identity, and possible NetLock certificate connection remained partly anonymized or inferential.

## Distinctions and limitations

Reconnaissance is not sabotage, and a tool that prepares an operation may be used by a different team from the one that writes the destructive payload. Shared code, encryption, file naming, or development style can establish a relationship hypothesis but not a state attribution. The source also mentions a possible “Stars” connection through an image-carried keylogger, but does not establish it. Public visibility increased after researchers learned from Stuxnet, yet the operators' cleanup and modularity left important gaps.

## Practical use

Defenders should treat design files, administrator credentials, network diagrams, and engineering-laptop activity as high-value reconnaissance indicators even when no process change is observed. Hunt for unexpected signed drivers, short-lived modular backdoors, encrypted outbound traffic, and access to CAD or control-system documentation. Limit the blast radius of engineering knowledge through least privilege and compartmentalized repositories. During attribution, compare technical lineage with target selection and operations, but publish confidence and uncertainty separately.

## Connections

Duqu explains how attackers could learn about a control network before deploying a Stuxnet-like payload, a possibility raised in Chapter 11. Its shared platform and specialized teams connect to Chapter 15's Flame/Gauss analysis and Chapter 19's discussion of techniques diffusing into criminal tools. It also reinforces the evidence ladder introduced in the root skill: observed overlap is stronger than a filename clue but weaker than proof of common authorship.
