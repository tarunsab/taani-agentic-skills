---
title: "Leaping Headlong"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Three — Move Fast and Break Things"
source_boundary: "Manual body section, extracted lines 2359–2387"
---

# Chapter 28 — Leaping Headlong

## Thesis

Product management creates speed by making reversible trade-offs and measuring
the result, while good experiments can reveal that abundant data has no
commercial signal.

## Core Idea

The chapter opens with topic extraction: a system maps text such as a sports
reference to a semantic category that can support ad targeting. The author
mediates a debate over whether to preserve old interest keywords or introduce a
hashtag-like supertopic, choosing a compatibility layer that can ship in weeks.
This is the book's practical version of bias for action: avoid a perfect
taxonomy when a reversible feature can generate evidence. A dashboard tracking
spend by target type makes the economic feedback visible and embodies the rule
that organizations tend to create what they measure. Project Chorizo then tests
posts, messages, links, check-ins, and other user inputs and finds no meaningful
performance improvement, demonstrating that richer data is not automatically
more predictive or valuable.

## Frameworks

- **Compatibility-first launch:** preserve existing behavior while adding a new
  mechanism so adoption and learning can begin without a full migration.
- **Signal audit:** test each data source against an outcome metric rather than
  assuming volume, intimacy, or novelty creates value.

## Key Concepts

- Topic extraction
- Semantic targeting
- Bias for action
- Product dashboard
- Project Chorizo

## Source Examples / Evidence

- Interest keywords and new hashtag-style supertopics are combined rather than
  forcing an abrupt switch.
- Testing many Facebook data inputs fails to improve advertising performance in
  a material way.

## Distinctions

- **Data richness vs. predictive signal:** more fields can add noise or cost
  without improving targeting.
- **Reversible speed vs. reckless launch:** a narrow, compatible change limits
  blast radius and creates a learning loop.
- **Metric visibility vs. metric truth:** a dashboard directs attention but can
  encode the wrong economic question.

## Limitations

The source does not provide the full experimental design or statistical power
behind Project Chorizo. Results from one platform, cohort, and period should not
be generalized to every future use of social data.

## Practical Application

For a new data feature, specify the incremental outcome, test cohort, baseline,
cost, and stopping rule. Ship the smallest compatibility-preserving version
that can falsify the value hypothesis.

## Connections

Data quality is tested at scale in [29 — One Shot, One Kill](ch29-one-shot-one-kill.md),
and the identity data that does prove valuable appears in [39 — The Great
Awakening](ch39-the-great-awakening.md).

## Worked Example

A platform wants to use private messages for ad targeting because the data is
more personal. A controlled experiment compares that signal with existing
interest categories, protects privacy boundaries, and measures incremental
conversion. If performance does not improve, the data should not be retained or
exposed merely because it is available.

## Key Takeaways

- Ship reversible compatibility layers when they accelerate learning.
- Make the metric answer the economic question, not just the data question.
- The most intimate data can still be commercially useless.

