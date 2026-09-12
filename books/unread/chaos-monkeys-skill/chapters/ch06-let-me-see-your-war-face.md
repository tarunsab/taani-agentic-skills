---
title: "Let Me See Your War Face"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Two — Pseudorandomness"
source_boundary: "Manual body section, extracted lines 1080–1142"
---

# Chapter 06 — Let Me See Your War Face

## Thesis

Advertising products live inside a measurable auction economy, but the hard
part for a startup is often acquiring and retaining small advertisers rather
than writing the optimization code.

## Core Idea

AdGrok's YC-era product is built around Google AdWords, where an advertiser's
position depends on a bid and an estimate of click quality. The chapter gives
the return-on-ad-spend calculation as a compact way to connect campaign cost to
revenue, while noting that keyword economics vary dramatically: legal and
financial terms can be expensive because a conversion is valuable. GrokBar
tries to expose product-level campaign statistics in a browser interface so a
small business can see keywords, bids, spend, and sales. The engineering task
is tractable, but the market is fragmented: individual small businesses have
low budgets, churn easily, and are expensive to serve one by one. The resulting
lesson is that not every business problem yields to engineering; scalable
distribution, partnerships, and repeatable sales matter as much as the bidding
algorithm.

## Frameworks

- **ROAS discipline:** `(revenue / cost) - 1` forces a campaign discussion to
  include economics rather than clicks alone.
- **SMB distribution problem:** low account value and high churn make direct
  sales a poor scaling path unless a platform or channel aggregates demand.

## Key Concepts

- AdWords auction
- Quality and expected click value
- Return on ad spend
- Long-tail advertiser acquisition
- GrokBar

## Source Examples / Evidence

- The chapter uses an illustrative $1.10 revenue on $0.75 spend to show a 47%
  return before other costs.
- AdGrok faces competitors in ad-management software while discovering that
  the small-business customer base is unstable and costly to reach.

## Distinctions

- **Ad performance vs. company performance:** profitable campaigns do not
  guarantee a profitable software business.
- **Optimization vs. acquisition:** improving bids helps existing users; it
  does not automatically create a scalable customer pipeline.
- **Click volume vs. value:** high-volume keywords may be less valuable than
  lower-volume terms with strong purchase intent.

## Limitations

The arithmetic is a teaching example, not a complete unit-economics model;
gross margin, attribution error, labor, and platform fees are omitted. Google
auction behavior and competitor conditions have changed since the memoir's
period.

## Practical Application

For an ad-tech product, calculate value per customer, acquisition cost, churn,
service load, and payback period before expanding features. Identify whether a
partner can aggregate many advertisers more cheaply than a direct sales team.

## Connections

The product's failure modes connect to the multiple-miracle test in [04 —
Knowing How to Swim](ch04-knowing-how-to-swim.md), while data quality and
targeting return in [28 — Leaping Headlong](ch28-leaping-headlong.md).

## Worked Example

If a shop spends $750 and records $1,100 in attributable revenue, the campaign
shows 47% gross return, but the software company still needs to ask whether it
can acquire that shop for less than the expected contribution margin and keep
it long enough to recover support costs. A reseller platform may be more
valuable than another bidding feature.

## Key Takeaways

- Campaign math is necessary but not sufficient for a business model.
- Small-business software fails when acquisition and service economics do not scale.
- Engineering leverage needs a distribution channel.

