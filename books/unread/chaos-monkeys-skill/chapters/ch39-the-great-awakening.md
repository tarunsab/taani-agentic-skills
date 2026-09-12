---
title: "The Great Awakening"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Three — Move Fast and Break Things"
source_boundary: "Manual body section, extracted lines 2822–2902"
---

# Chapter 39 — The Great Awakening

## Thesis

The high-value advertising problem is identity resolution: connecting a person,
device, browsing event, customer record, and purchase while preserving enough
control over data to make the connection useful and safe.

## Core Idea

Advertising begins with name-calling—assigning keys such as a postal address,
device identifier, or retargeting cookie—then trying to join those keys across
surfaces. A retailer may see browsing, a mobile action, and a later store
purchase as separate events unless an identity bridge attributes them to one
person. Data brokers and onboarding firms maintain offline and CRM segments,
while Facebook and Google act like highly efficient post offices that can route
messages once an audience is identified. Facebook Custom Audiences can match
uploaded identifiers to platform users, and the author presents high match
rates as evidence of the value of the bridge. The company studies demand-side
platforms, data suppliers, and identity providers because outside ad-tech
expertise is necessary to build a real targeting system. The chapter's central
distinction is that Facebook's social graph is not automatically the best
commercial dataset; the join between real-world intent and a reachable user is
the valuable infrastructure.

## Frameworks

- **Identity graph:** nodes are identifiers and events; edges are evidence that
  two records refer to the same user or household.
- **Attribution bridge:** ad exposure → recognized identity → action → matched
  outcome; each join needs a confidence and a privacy boundary.

## Key Concepts

- Identity resolution
- Data onboarding
- Custom Audiences
- First- and third-party data
- Demand-side platform
- Offline attribution

## Source Examples / Evidence

- The chapter uses a Target-like sequence in which browsing, mobile behavior,
  and a store purchase become measurable only after an identity join.
- It surveys brokers and ad-tech companies such as Acxiom, Experian, Epsilon,
  MediaMath, Turn, BlueKai, and DSPs as parts of the ecosystem.

## Distinctions

- **Identifier vs. identity:** a cookie or device ID is a key, not proof of a
  human, household, or intent.
- **First-party vs. third-party data:** data collected in a direct relationship
  differs in provenance, permission, and reliability from purchased segments.
- **Targeting vs. attribution:** choosing whom to reach is distinct from proving
  that exposure caused an outcome.

## Limitations

The data-broker landscape, identifiers, match rates, and policy environment have
changed substantially since the period described. Identity matching can create
false joins and serious privacy harm; the chapter's business enthusiasm should
be balanced by consent, minimization, security, and fairness requirements.

## Practical Application

Document every identity edge: source, permission, match confidence, retention,
allowed use, and deletion path. Test incrementality with holdouts rather than
assuming that a successful match proves causal advertising value.

## Connections

The human-attention market in [03 — The Human Attention Exchange](ch03-the-human-attention-exchange.md)
provides the economic context, while implementation conflict appears in [40 —
Barbarians at the Gates](ch40-barbarians-at-the-gates.md).

## Worked Example

An advertiser uploads hashed emails and wants to retarget customers across
devices. The platform should report match quality without exposing raw data,
limit use to the stated purpose, and compare retargeted conversions with a
holdout group. The join creates reach; the experiment establishes value.

## Key Takeaways

- Identity resolution is the connective tissue of modern ad measurement.
- A match is not a person and an attribution is not causation.
- Commercially useful data often comes from mundane transactions, not intimate posts.

