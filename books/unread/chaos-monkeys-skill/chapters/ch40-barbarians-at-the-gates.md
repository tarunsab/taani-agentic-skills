---
title: "Barbarians at the Gates"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Three — Move Fast and Break Things"
source_boundary: "Manual body section, extracted lines 2903–2955"
---

# Chapter 40 — Barbarians at the Gates

## Thesis

Facebook's path to serious advertising requires opening its wall to outside
data and real-time exchanges, but the organization must first understand and
politically approve technology that threatens its information advantage.

## Core Idea

The chapter presents Facebook Ads as technically backward compared with the
outside programmatic market while still earning significant revenue through
scale. The proposed remedies are Custom Audiences, which joins uploaded
identifiers to Facebook users, and Facebook Exchange, a real-time system that
lets outside demand-side platforms bid on Facebook impressions. FBX would
require new data stores, APIs, auction timing, creative handling, statistics,
monitoring, partner integrations, and sales enablement; it is a parallel ads
system rather than a small feature. Zach Coelius serves as the credible outside
voice who translates programmatic advertising for engineers and executives,
turning an obscure opportunity into a compelling internal narrative. Five weeks
later the author has only three engineers and a $100 million revenue promise,
so the product's strategic ambition and its execution resources are radically
misaligned. The chapter therefore shows how a platform can need “barbarians” to
bring outside practice inside while still trying to control the gate.

## Frameworks

- **Open-wall strategy:** connect external data and bidders through controlled
  interfaces instead of rebuilding every function internally.
- **Revenue-for-resources bargain:** secure scarce engineering capacity by
  tying a product to a measurable near-term financial commitment.

## Key Concepts

- Custom Audiences
- Facebook Exchange
- Demand-side platform
- Real-time bidding
- Partner integration
- Revenue commitment

## Source Examples / Evidence

- Facebook Ads is compared unfavorably with earlier outside ad-tech systems in
  targeting and attribution despite its large revenue base.
- A one-hour presentation by Zach Coelius persuades senior Ads leaders of the
  scale and technical logic of programmatic buying.

## Distinctions

- **New feature vs. parallel system:** FBX must handle external network calls,
  bidding, data, creative, reporting, and operational health independently.
- **Revenue size vs. technology maturity:** billions in revenue can coexist with
  a weak underlying stack when distribution is powerful.
- **Internal champion vs. institutional support:** a persuasive pitch can win a
  decision while leaving the team under-resourced.

## Limitations

The chapter's technology comparison is the author's expert judgment at a
particular moment. Five-week delivery and $100 million targets are historical
constraints, not a general planning standard; modern privacy and platform rules
may prohibit analogous data flows.

## Practical Application

When proposing a platform opening, enumerate the technical, privacy, partner,
sales, and accounting surfaces required for launch. Secure explicit resources,
owners, and a staged revenue hypothesis rather than relying on executive
enthusiasm.

## Connections

Identity joining is developed in [39 — The Great Awakening](ch39-the-great-awakening.md),
while execution latency and the eventual conflict are shown in [43 — Flash
Boys](ch43-flash-boys.md) and [44 — Full Frontal Facebook](ch44-full-frontal-facebook.md).

## Worked Example

A social platform wants external retailers to bid on its impressions. The first
plan should specify pseudonymous identity, request latency, data leakage
controls, creative constraints, reporting truth, partner certification, and a
kill switch. A five-week prototype can test the critical path; it cannot hide
the remaining operational program.

## Key Takeaways

- Opening a platform is an organizational and accounting change as well as a technical one.
- Outside specialists can translate an external market into internal action.
- Revenue promises do not replace staffing and governance.

