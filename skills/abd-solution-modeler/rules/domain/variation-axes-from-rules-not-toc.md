---
title: Variation axes from rules, not table of contents
impact: HIGH
---

## Variation axes from rules, not table of contents

### What a variation axis is

A **variation axis** is a dimension along which the domain's *mechanics* differ — different rules, different resolution, different triggers, different state transitions. Switching from one value to another on a real axis changes *how things work*.

### What is NOT a variation axis

**Variable values are not variation axes.** When the source lists values for a single variable (e.g. payment method: credit card, bank transfer, invoice; order status: pending, shipped, delivered; customer tier: gold, silver, bronze), those are just different values the same variable can take. The *mechanism* is the same — only the input changes. Listing them as a variation axis adds noise and means nothing for extraction.

**ToC and headers are not evidence.** Table of contents, section headers, and bullet lists name things; they do not prove distinct mechanics. You must read the actual rule text before adding an axis.

### How to justify a variation axis

1. **Read the rules** — For each candidate axis, scan context chunks for the rules that govern each variant: triggers, conditions, resolution, state transitions.
2. **Mechanical difference test** — Does switching from variant A to variant B change the *rules* that apply? If yes, it may be a variation axis. If it only changes which value a variable has (same rules, different input), it is not.
3. **Avoid collapsing** — When the source describes many named variants, each with distinct rules, do not collapse them into one superficial axis. Either list the mechanically distinct variants or treat the area as an epic.

### High-complexity areas

When the source describes many named variants, each with its own rules, that area is likely an epic — not a single variation axis. Model as concepts and stories, not as one axis with an enum of values.

### Examples (from unrelated domains)

- **Wrong:** Axis = "payment method (credit card, bank transfer, invoice)" — same settlement flow, different input. Variable values, not a mechanical dimension.
- **Wrong:** Axis = "order status (pending, shipped, delivered)" — same state machine, different state. Variable values.
- **Wrong:** Axis copied from ToC or headers without reading rule text.
- **Right:** Axis documents a dimension where variants have different mechanics — e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, and reversal rules. You have read the rules and can state what differs.
