---
title: "Ads Five-Oh"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Three — Move Fast and Break Things"
source_boundary: "Manual body section, extracted lines 2448–2489"
---

# Chapter 31 — Ads Five-Oh

## Thesis

Advertising safety works as a layered operational system: automated detection,
human review, user feedback, and escalation must cooperate because adversaries
adapt to any single filter.

## Core Idea

Facebook's early ad units are small and visually limited, but the review burden
is large because advertisers can submit obscene, fraudulent, or misleading
creative at scale. The Ads Review and Quality team combines human moderation
with machine-learning detectors, user negative feedback, and MOSI-style labels
that can send an ad back for review. Fuzzy image matching helps catch repeated
or slightly altered versions of prohibited material, while copy patterns such
as implausible free offers can act as fraud signals. The chapter also shows the
political side of safety: a quarterly meeting turns invisible operational work
into a presentation, and even the choice of demonstration images can create a
gender or taste dispute. Security protects a large share of the Internet yet
rarely receives credit until a failure makes it visible.

## Frameworks

- **Layered defense:** combine automated precision, human judgment, user
  reports, and re-review rather than expecting one classifier to be complete.
- **Adversarial feedback loop:** every enforcement rule teaches bad actors how
  to evade it, so detection and review must evolve continuously.

## Key Concepts

- Ads Review and Quality
- Machine-learning moderation
- MOSI labels
- Fuzzy image matching
- Operational security

## Source Examples / Evidence

- User feedback and machine labels trigger additional review of questionable
  ads, with image similarity used to detect evasion.
- A demonstration involving obscene imagery and the team's trophy display shows
  how moderation work intersects with executive presentation and culture.

## Distinctions

- **Detection vs. adjudication:** a model can flag an ad; a human or policy
  system may still need to decide what action is justified.
- **Fraud signal vs. proof:** suspicious copy raises risk but is not itself a
  complete finding.
- **Security success vs. visibility:** preventing abuse produces little public
  evidence compared with responding to a breach.

## Limitations

The chapter is historical and anecdotal; it does not provide classifier error
rates, appeal outcomes, or a complete policy framework. Moderation standards
and platform responsibilities evolve, so the examples should not be treated as
current policy.

## Practical Application

Design enforcement with a clear policy, a fast automated screen, human review
for uncertain cases, user feedback, appeal paths, and an adversarial test set.
Measure false positives, false negatives, time to action, and repeat evasion.

## Connections

The scale and economic pressure behind safety appear in [29 — One Shot, One
Kill](ch29-one-shot-one-kill.md), while data governance is examined in [32 —
The Narcissism of Privacy](ch32-the-narcissism-of-privacy.md).

## Worked Example

A platform sees a wave of fake giveaway ads. It blocks known image hashes,
scores suspicious language, routes high-risk accounts to human review, and
lets users report misses. A weekly sample of accepted and rejected ads tests
whether the system is merely shifting fraud into a new format.

## Key Takeaways

- Safety is an operating system, not a single model.
- User feedback can be a production sensor.
- Invisible prevention still needs metrics and executive support.

