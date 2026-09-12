---
title: "The Narcissism of Privacy"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Three — Move Fast and Break Things"
source_boundary: "Manual body section, extracted lines 2490–2562"
---

# Chapter 32 — The Narcissism of Privacy

## Thesis

Privacy risk and advertising value are related but not identical: the most
embarrassing personal information may be commercially useless, while mundane
purchase and browsing signals can be highly valuable and operationally risky.

## Core Idea

The author describes Facebook Ads as a routing system in which advertisers
choose targeting and Facebook supplies access to users without simply handing
over the underlying data. Privacy debates, legal audits, and product deadlines
create pressure to know exactly what is active in production rather than trust
an informal assurance. In one New Zealand test-bed incident, he checks the
production database, removes a forbidden targeting configuration, and verifies
the result with dashboards under oversight. The chapter contrasts public fear
of intimate content with the data that actually improves advertising:
identifiers, purchases, browsing, devices, and customer records that link an ad
to a transaction. It also describes a privacy referendum with weak participation
and an ignored outcome, illustrating the gap between a formal process and a
policy that can guide later products.

## Frameworks

- **Data-value/risk matrix:** classify data by commercial lift, sensitivity,
  identifiability, access, retention, and misuse consequence.
- **Trust-but-verify production check:** combine policy interpretation,
  database inspection, controlled remediation, and post-change monitoring.

## Key Concepts

- Targeting versus data transfer
- Personally identifiable information
- Privacy audit
- Production configuration
- Purchase-intent data

## Source Examples / Evidence

- The author does not rely solely on an engineer's statement that restricted
  targeting is inactive; he inspects production and removes the setting.
- The chapter distinguishes creepy personal content from browsing, purchase,
  CRM, and device data that can improve ad performance.

## Distinctions

- **Privacy sensitivity vs. monetization value:** a detail can be intimate but
  not predictive of a purchase.
- **Using data to target vs. selling data:** a platform can keep user-level data
  inside its system while allowing advertisers to select an audience.
- **Policy existence vs. policy control:** a vote, document, or promise matters
  only if it changes production behavior.

## Limitations

The account reflects a historical product and legal environment and does not
provide a complete view of the audit, user consent, or affected jurisdictions.
The author's claim about commercial uselessness is a context-specific
generalization, not a reason to dismiss privacy harm.

## Practical Application

For every targeting feature, document data origin, purpose, access path,
retention, user expectation, legal basis, and kill switch. Test the live system,
not only code or documentation, and log who can change a sensitive setting.

## Connections

The failed experiments on social data appear in [28 — Leaping Headlong](ch28-leaping-headlong.md),
while identity joining and data brokers appear in [39 — The Great Awakening](ch39-the-great-awakening.md).

## Worked Example

A product team proposes using a user's private text to improve ad relevance.
The data-value/risk matrix may show high sensitivity, uncertain incremental
lift, and substantial trust cost. A safer test may use consented purchase data,
aggregate cohorts, and a production kill switch before any user-level rollout.

## Key Takeaways

- “Creepy” and “valuable” are separate assessments.
- Production verification matters more than verbal reassurance.
- Privacy controls must be designed into the data path and the operating process.

