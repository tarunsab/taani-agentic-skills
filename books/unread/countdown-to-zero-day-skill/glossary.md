# Glossary

## Air gap

A separation between a control network and outside networks. It reduces ordinary remote paths but is not magic isolation: engineers, laptops, removable media, maintenance tools, and supply chains can bridge it.

## Attribution

The process of assessing who conducted an intrusion. In the book, attribution combines technical artifacts, target knowledge, operational timing, intelligence reporting, and geopolitical context; none is automatically conclusive.

## Cascade

A staged arrangement of centrifuges and associated gas-flow equipment. The number of stages, centrifuges, valves, pressure sensors, and frequency converters forms a process signature that a tailored payload can use as an eligibility check.

## Command and control (C2)

The infrastructure or peer-to-peer mechanism through which malware receives instructions or sends information. Stuxnet had Internet C2 domains but could also update across local peers; its PLC payload did not require a continuously reachable C2 connection once deployed.

## Digital certificate

A cryptographic credential used to establish software identity and trust. Stuxnet abused stolen legitimate certificates for drivers; Flame abused a Microsoft licensing certificate through an MD5 collision, showing that trust infrastructure itself can become an attack surface.

## Industrial control system (ICS)

The combined computers, networks, controllers, instruments, and engineering tools used to monitor or control a physical process. SCADA and DCS are common ICS patterns; the key security issue is the relationship between digital commands and physical consequences.

## Ladder logic / STL / MC7

PLC programming representations. Stuxnet injected logic into Siemens programs; the book describes analysts translating machine-oriented forms such as STL and MC7 to understand what the controllers would execute.

## Man-in-the-middle deception

Interposing on a control or monitoring path so that commands can be changed and readings can be falsified. Stuxnet used this pattern to hide abnormal PLC behavior and replay a record of normal operation.

## NOBUS

“Nobody But Us,” a policy intuition that a government may retain a vulnerability when it believes only it can exploit it. The book presents this as a fragile assumption because knowledge spreads, software changes, and the defender may be the same society that bears the risk.

## PLC

Programmable logic controller: a rugged computer that executes control logic for machines and processes. Stuxnet looked for particular Siemens S7 families and configurations rather than treating every Windows host as its final target.

## Process safety system

Hardware or logic intended to place a process in a safer state when pressure, vibration, speed, or another condition crosses a limit. The book emphasizes that disabling or deceiving such a layer turns a control manipulation into a potentially destructive physical event.

## Rootkit

Software designed to hide files, processes, drivers, or activity from ordinary operating-system tools. Stuxnet used kernel-level hiding to make its presence and copies harder to inspect.

## Step 7 / WinCC

Siemens engineering and supervisory software used to program or monitor S7 controllers. Stuxnet's unusual specificity to this ecosystem let it distinguish ordinary infected hosts from a potential industrial target.

## Zero-day

An exploitable software flaw for which defenders have had no practical time to patch or build reliable detection. The term also names the market value of such knowledge; the book distinguishes vendor disclosure, criminal trade, and government or contractor acquisition.

## Zero-day market

The overlapping white, black, and gray markets for vulnerability knowledge. Price depends on rarity, ubiquity, reliability, privilege, stealth, and exclusivity, while the social cost of secrecy is distributed to vendors and users.

## Weaponization

Turning access or vulnerability knowledge into a capability that achieves a mission. In this book, weaponization includes target reconnaissance, delivery, process-specific logic, testing, timing, deception, and an intended strategic effect—not merely finding a bug.

## Worm

Malware that propagates from system to system. Stuxnet used several propagation paths to cross organizational and network boundaries, but constrained its destructive payload to a narrow industrial configuration; those are separate properties.
