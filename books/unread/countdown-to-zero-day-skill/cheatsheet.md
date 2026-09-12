# Cheatsheet

## One-page thesis

Stuxnet mattered because it joined a sophisticated Windows intrusion to a narrowly selected industrial process, changed controller behavior, deceived operators, and demonstrated that binary commands could damage physical machinery. Its engineering success did not settle its strategic success. The operation may have delayed Iran's enrichment effort, but it did not end it; the malware escaped its intended environment, revealed techniques others could reuse, weakened trust in shared infrastructure, and helped normalize destructive cyber operations between states.

## Fast diagnostic questions

1. What physical process is controlled, and what failure state is dangerous?
2. Which assets are enterprise IT, engineering, supervisory, PLC, safety, or field devices?
3. What bridges an otherwise isolated control environment?
4. Can the same software write commands and falsify read-back data?
5. What exact configuration would make the payload eligible to run?
6. Which observations are direct, and which are inference or anonymous reporting?
7. What are the plausible non-malicious explanations for the physical symptoms?
8. Can operators stop, isolate, or safely reconstitute the process?
9. What happens to certificates, update trust, and other shared defenses if the operation is exposed?
10. Who benefits from secrecy, and who carries the risk if the capability leaks or is copied?

## Stuxnet in six layers

| Layer | Study question | Defensive analogue |
| --- | --- | --- |
| Delivery | How did code cross organizational or network boundaries? | Control removable media, engineering laptops, supplier access, and project-file exchange. |
| Persistence | How did it survive and hide? | Inspect drivers, signatures, boot persistence, hidden files, and clean-room baselines. |
| Eligibility | What exact system and process had to be present? | Inventory PLC models, cards, firmware, logic, recipes, and safety dependencies. |
| Manipulation | What did it change in the engineering/control path? | Compare authorized logic, software binaries, controller checksums, and change records. |
| Deception | How could operators see normal data during abnormal operation? | Validate telemetry through independent sensors and out-of-band process checks. |
| Outcome | What physical, operational, and strategic effect followed? | Track safe shutdown, recovery, production, delay, disclosure, and copycat risk. |

## Evidence language

- **The file contains / the report records:** direct observation.
- **This is consistent with:** a supported reconstruction, not proof.
- **The source reports / an unnamed official said:** attributed reporting.
- **The public record does not establish:** an explicit fidelity limit.

## Governance checklist

- Is the vulnerability also present in domestic, allied, or widely used systems?
- Is the capability unique, controllable, recallable, and safe if it spreads?
- Has the target's civilian and third-party infrastructure been mapped?
- What legal authority and proportionality analysis apply?
- What is the disclosure and remediation plan if the operation is exposed?
- What independent review can test whether the benefit outweighed the systemic risk?

## Safe application

Use this framework for historical study, defensive architecture, tabletop exercises, incident response, and policy analysis. Keep demonstrations in toy or simulated environments; do not reproduce exploit chains, PLC sabotage logic, credential theft, persistence methods, or operational target-selection procedures.
