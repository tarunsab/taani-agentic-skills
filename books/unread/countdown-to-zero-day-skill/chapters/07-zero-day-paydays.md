# Chapter 7: Zero-Day Paydays

## Thesis

Zero-day vulnerabilities sit in competing markets with different incentives. The white market rewards disclosure and patching; the criminal market monetizes access, credentials, or botnets; the gray market lets governments, defense contractors, and law-enforcement buyers purchase exploits without telling vendors. The chapter's central policy question is not simply what an exploit costs, but who benefits while it remains secret and who bears the risk if the flaw is independently discovered or the capability leaks. Stuxnet's four zero-days make that abstract market concrete.

## Mechanism and source evidence

The source describes prices rising with rarity, software ubiquity, reliability, privilege, stealth, and exclusivity: browser, Windows, Flash, Mac, and iOS exploits could command tens or hundreds of thousands of dollars, while public bug bounties were often much smaller. It profiles brokers such as The Grugq, researchers such as Charlie Miller, and firms such as Endgame and VUPEN that packaged access or exploit research for government and security customers. Critics including Christopher Soghoian argued that buyers could be robbed, blackmailed, or copied, while Wassenaar discussions showed how difficult it is to classify and control dual-use knowledge. The examples do not prove who purchased Stuxnet's vulnerabilities; they demonstrate that a capable operator could acquire them through a real incentive structure.

## Distinctions and limitations

The white, black, and gray categories overlap in practice, and the source does not reduce every researcher or buyer to a moral type. A government may have legitimate intelligence reasons to retain a flaw, but secrecy also withholds remediation from the government’s own citizens and allies. Export controls may regulate transactions without eliminating underground trade or domestic stockpiles. Market prices are historical examples, not stable quotations, and the value of an exploit depends on the target and the buyer's mission.

## Practical use

Organizations should assume that software vulnerabilities can have buyers other than the vendor and should invest in layered mitigation rather than relying on disclosure alone. Policymakers evaluating retention should model discovery probability, reuse across domestic systems, patch delay, vendor trust, and the cost of emergency response. Security teams can use the “who benefits?” test to surface hidden incentives in procurement and disclosure decisions. The safe lesson is not to hunt or trade exploits, but to understand why a vulnerability may remain unreported and how to reduce dependence on a single defensive layer.

## Connections

This chapter explains how Stuxnet could combine rare vulnerabilities with older public flaws, and it leads directly to Chapter 12's vulnerability-equities dilemma. It also reinforces the book's difference between technical sophistication and governance maturity: a state can buy extraordinary access without having a transparent process for handling the resulting risk. Chapter 19 extends that market concern into an arms race in which government-funded techniques diffuse into crimeware.
