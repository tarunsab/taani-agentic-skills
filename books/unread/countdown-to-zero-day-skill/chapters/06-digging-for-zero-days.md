# Chapter 6: Digging for Zero Days

## Thesis

Stuxnet's unusual reach came from a portfolio of propagation methods rather than a single lucky exploit. During a weekend analysis, O'Murchu found a second Windows zero-day involving keyboard handling and then a printer-spooler flaw; together with the shortcut vulnerability and another previously unknown flaw, the code carried four zero-days. It also spread through Step 7 project files, network shares, peer-to-peer updates, old vulnerabilities, and human movement across removable media. The chapter shows that the attack was engineered around the practical problem of crossing an air gap, but that the same redundancy made collateral infection likely.

## Mechanism and source evidence

Stuxnet could use USB Autorun, the print spooler, a Step 7 project-file feature, a hard-coded Siemens account, local network shares, and the older MS08-067 vulnerability, in addition to its other paths. It logged roughly 100 bytes per infection, including an address, domain, and timestamp, allowing researchers to reconstruct an early chain through five Iranian industrial companies: Foolad Technique, Behpajooh, Neda Industrial Group, CGJ/Control Gostar Jahed, and Kala. More than 100,000 machines in roughly 100 countries were infected, while Behpajooh accounted for a particularly large share of one observed set. The code's 2009 update became more aggressive than the earlier version, suggesting an operational need to improve delivery or compensate for lost access.

## Distinctions and limitations

Air-gapped does not mean unreachable; it means the bridge is different. The book distinguishes a zero-day from older public vulnerabilities, and a propagation path from the PLC conditions that activate sabotage. Some vulnerabilities had appeared in earlier tools or public discussions, so “zero-day” status may depend on who knew what and when. The company names came from malware logs and public investigation, not a complete official account of each firm's relationship to Natanz or its operators.

## Practical use

Defensive review should enumerate every path into an engineering environment, including project files, maintenance laptops, USB drives, network shares, vendor credentials, and old protocol stacks. Use allowlists and scanning for removable media, but also audit the social workflow that carries files between networks. Preserve infection timestamps and graph relationships without assuming the first infected company is the final target. Redundancy in an attacker’s delivery portfolio is a signal to test several controls together; patching one exploit is not equivalent to closing the route.

## Connections

The chapter operationalizes Chapter 4's separation of spread and payload and leads to Chapter 7's question of how such zero-days are acquired. The gateway-company pattern connects to Chapter 17's infection timeline and Chapter 15's contrasting targeted spread of Flame. Its collateral-infection lesson becomes central in Chapters 18 and 19, where controllability and blowback determine whether Stuxnet should be called a success.
