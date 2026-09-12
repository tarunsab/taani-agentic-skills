# Patterns

## Start with the Small Anomaly
**When to use**: An accounting, timing, or identity mismatch is unexplained but reproducible.
**How**: Preserve the observation, test the smallest change that can discriminate among explanations, and record what happens next.
**Trade-offs**: The clue may look trivial and the investigation may take time, but it avoids building a case on drama.
Stoll's seventy-five-cent mismatch exposes the Hunter account, and removing that account produces the Sventek login. The discrepancy is not proof of motive; it is a high-value lead because it can be checked. This pattern works when the anomaly is preserved before the system is normalized.

## Build an Independent Watchdog
**When to use**: The observed host or its logs may be altered by a privileged intruder.
**How**: Put observation outside the host's ordinary trust boundary, collect repeated session evidence, and keep a human confirmation path.
**Trade-offs**: External equipment is awkward and adds operational work, but it preserves visibility when local evidence is suspect.
Stoll's Unix-8 moat, printers, pager, and switchyard monitors make the attack observable without relying on the compromised machine alone. A watchdog is a sensor, not a complete response system; it still needs interpretation and escalation.

## Model the Privilege Chain
**When to use**: An incident crosses from account use into system modification.
**How**: Record the sequence from credential use to program alteration, privilege gain, persistence, and cleanup.
**Trade-offs**: The model explains mechanism better than a label such as “hacking,” but it can miss actions performed outside the monitored host.
The cuckoo's egg is a compact example: a stolen account becomes a path to a privileged program, which gives the intruder root and access to protected material. Mapping the chain reveals where to patch and what evidence may have been tampered with.

## Separate Route, Target, Identity, and Motive
**When to use**: A trace feels persuasive but attribution is still incomplete.
**How**: State what the evidence says about the network path, the systems touched, the person or process involved, and the reason for acting as four different claims.
**Trade-offs**: The explanation stays cautious and can feel unsatisfying, but it resists false certainty.
Stoll can identify Germany as part of the route before he can name Markus Hess, and he can observe SDI searches before he can prove espionage. The separation lets new evidence strengthen one claim without silently upgrading all the others.

## Use a Bounded Decoy
**When to use**: You need a longer or more informative session, and real sensitive material is not appropriate bait.
**How**: Create plausible synthetic material, restrict it from ordinary users, define the observation window, obtain approval, and monitor the result.
**Trade-offs**: A decoy can reveal behavior and create a callback, but it consumes effort and can mislead the investigator if it is too theatrical.
Operation Showerhead succeeds because the documents are bureaucratic and the goal is explicit: keep the hacker connected long enough for a trace. It is an experiment, not a general license to leave weaknesses open or plant real secrets.

## Verify Before Escalating
**When to use**: An alarm could be caused by instrumentation, maintenance, or unrelated activity.
**How**: Confirm the live session and its context before waking external partners, then preserve the false positive in the log.
**Trade-offs**: Verification costs time, but a false alarm can damage cooperation and credibility.
Stoll's electrical false alarm teaches this directly. The same rule improves both incident response and scientific observation.

## Correlate Historical Records
**When to use**: No single trace identifies the source, but many records cover the same time range.
**How**: Align timestamps, destinations, account use, and route identifiers against a baseline, then state what the correlation cannot prove.
**Trade-offs**: Historical correlation reveals stepping-stones and scope, but it can produce many innocent matches.
Mitre's phone bills show repeated calls to defense-related systems, helping identify infrastructure rather than a person. The method is strongest when combined with live traces and behavioral differences.

## Distinguish Probe from Compromise
**When to use**: A log contains guessed accounts, directory searches, privilege changes, or data transfers.
**How**: Classify each event as attempted access, successful access, privilege gain, or retrieval, and preserve the uncertainty between them.
**Trade-offs**: The resulting report is less dramatic, but it is more defensible and more useful for remediation.
Stoll sees the hacker try dozens of military systems, yet many reject the guesses. Counting all of them as breaches would overstate the case and obscure the systems that actually need urgent repair.

## Patch with the Mission in Mind
**When to use**: A host is compromised but continued observation may expose other systems or people.
**How**: Compare immediate containment, evidence value, safety consequences, and campaign redirection; choose a bounded action and revisit it.
**Trade-offs**: Staying open can preserve a trace but creates local risk, while closing can protect one host but make the wider threat invisible.
Stoll keeps LBL open under monitoring, closes routes such as Mitre's modems, and later hardens the system after the search. The correct action depends on the host's mission and the information still needed.

## Publish the Generalizable Lesson
**When to use**: A case has produced evidence and methods that others need, but sensitive operational details remain.
**How**: Separate reproducible method from protected data, use review, and prepare an accurate account before publicity forces improvisation.
**Trade-offs**: Publication can improve defense and accountability while exposing the investigator and changing future attacker behavior.
Stoll's paper and press conference transform a personal chase into a case study. The German leak shows why responsible preparation matters even when the timing is no longer fully controlled.
