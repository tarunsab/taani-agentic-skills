---
title: "Speed Is a Feature"
book: "Chaos Monkeys"
author: "Antonio García Martínez"
part: "Part Two — Pseudorandomness"
source_boundary: "Manual body section, extracted lines 1186–1235"
---

# Chapter 08 — Speed Is a Feature

## Thesis

In an early startup, attention is a form of distribution and shipping quickly
can create more learning and leverage than polishing an incomplete product.

## Core Idea

AdGrok's first public prototype is embarrassing: it barely works, lives on a
local development server, and fails during a short demo. Instead of treating
the failure as a verdict, the team uses a provocative essay about New York
technology and Goldman Sachs to attract attention. Timed for Hacker News, the
post reaches the front page, overloads a single AWS instance, and forces the
team to clone the blog across machines while thousands of people arrive. The
episode shows that a startup's packaging and distribution can temporarily
outperform its product, creating users, press, and investor interest before the
software is mature. The title's speed is therefore double-edged: rapid action
creates options and evidence, but it also creates operational debt and public
exposure. The "chaos monkey" image captures a broader idea of disruption that
tests the resilience of established systems, including the human systems around
them.

## Frameworks

- **Attention before perfection:** use a sharp, honest wedge to attract a
  relevant audience, then convert attention into product learning.
- **Resilience by forced failure:** expose infrastructure to unexpected failure
  so the team learns before a larger audience discovers it.

## Key Concepts

- Viral distribution
- Hacker News launch dynamics
- AWS scaling
- Chaos monkey testing
- Product packaging and PR

## Source Examples / Evidence

- A Scoble tweet and Hacker News ranking drive a sudden traffic spike that
  takes down the initial single-instance deployment.
- The engineers copy the blog to multiple Amazon machines and recover enough
  service to capture signups and press interest.

## Distinctions

- **Attention vs. retention:** a viral post can create a spike without proving
  durable product use.
- **Speed vs. carelessness:** moving fast is valuable when paired with a rapid
  recovery loop, not when failures are ignored.
- **System testing vs. social disruption:** technical chaos testing has a
  bounded purpose; disruption in human systems carries moral costs.

## Limitations

The chapter celebrates provocative writing and does not quantify how many
visitors became paying customers. Viral reach is highly path-dependent and may
not generalize to a quieter or trust-sensitive product.

## Practical Application

Design a launch with a small but real audience, a traffic-failure plan, and a
conversion event that produces learning. Before seeking virality, ensure the
team can observe, recover, and communicate when capacity is exceeded.

## Connections

Launch decay is formalized in [16 — Launching!](ch16-launching.md), and
experimentation culture reappears in [33 — Are We Savages or What?](ch33-are-we-savages-or-what.md).

## Worked Example

A developer tool publishes a technically opinionated benchmark that attracts
ten times expected traffic. The team keeps the post live, adds capacity,
records the failure, and asks every new visitor to run one reproducible test.
The attention becomes useful only if the spike yields qualified users and
evidence about the product's real value.

## Key Takeaways

- Distribution is part of product development.
- Public failure can become leverage when recovery is fast and visible.
- Chaos is useful as a test only when its blast radius is understood.

