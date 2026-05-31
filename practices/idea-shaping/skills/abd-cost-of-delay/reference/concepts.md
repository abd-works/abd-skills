# Cost of Delay — Concepts

## Cost of Delay

The value an organisation does **not** receive for every time period an item is not yet in market. Expressed as dollars (or equivalent) per month or per week. It reframes prioritization from "how much does this cost to build?" to "how much does it cost us to **wait to build it**?"

## Value Type

Every item generates value through one of four mechanisms. The type shapes the formula you use to estimate Cost of Delay:

| Value Type | What it means | Formula pattern |
| --- | --- | --- |
| **Increase Revenue** | New or expanded sales | Market size × transaction value × likelihood × volume |
| **Protect Revenue** | Sustain current revenue against threats | Likelihood of threat × events/month × cost per event |
| **Reduce Cost** | Lower costs we are currently incurring | Cost reduction/event × events × likelihood of benefit |
| **Avoid Cost** | Prevent costs we do not yet incur but may | Cost avoidance/event × events |

## Urgency Profile

How fast value decays over time — the shape of the curve:

| Profile | Characteristic | Example |
| --- | --- | --- |
| **Expedite** | High and immediate impact; major loss if not addressed now | "Customer data is exposed until we fix this" |
| **Fixed Date** | Value drops to zero past a specific date | "Campaign must launch before Black Friday" |
| **Standard** | Shallow but immediate; incremental value over time | "More paying customers if they can subscribe online" |
| **Intangible** | No immediate impact; builds future capability | "Local delivery capability gives us autonomy to move at market speed" |

## CD3 — Cost of Delay Divided by Duration

The scheduling decision formula:

```
CD3 = Cost of Delay (per period) / Duration (lead time to deliver)
```

Rank by **highest CD3 first**. This maximises total value delivered for a given time window with fixed resources, and naturally encourages breaking work into smaller batches (smaller duration → higher CD3).

## The method

**Inputs required:** Each candidate item needs a **lead time estimate** (how long to deliver to market) and optionally a **delay time estimate** (how much of that lead time is waiting, not working). These come from outside this skill — from team knowledge, flow metrics, or a delivery planning practice.

1. **Scan context for items and isolate each one.** Read the supplied context (backlog, story map, canvas, brief, conversation) and identify every distinct feature, epic, or initiative. When there is more than one item, treat each independently — do not blend assumptions across items. List what you found and cite where in context each item came from.

2. **Check for lead time.** Each item needs a lead time (duration) estimate. If the context supplies it, cite where. If not, **ask the user** — do not invent a duration. You cannot calculate CD3 without it.

3. **Classify value type and urgency profile per item.** For each item independently, select one value type (Increase Revenue / Protect Revenue / Reduce Cost / Avoid Cost) and one urgency profile (Expedite / Fixed Date / Standard / Intangible). Cite which part of the context led to the classification — quote the phrase, metric, or constraint that justifies it.

4. **Build a value model and estimate Cost of Delay per item.** For each item independently, mine the context for numbers, constraints, and claims that feed the formula. Every assumption must cite its source: quote from context if available, mark as "team estimate" or "SWAG" if not. Use Reach × Frequency × Likelihood × Unit Value or the formula matching the value type. Express CoD as **$ per period** (month or week — be consistent across items). Document each assumption with factor, unit, confidence, and source citation.

5. **Calculate CD3 per item.** CD3 = Cost of Delay / Duration. Show the arithmetic.

6. **Rank by CD3 and produce the revenue vs opportunity-cost table.** Order all items highest CD3 first.

7. **Answer "what if we reorder?"** When the user asks (or when items are close in CD3), show both orderings side by side with a comparison summary showing total revenue, total opportunity cost, and the saving vs the worst order.

## Assumptions and validation

Every CoD canvas labels assumptions with confidence (Strong / Reasonable / Uncertain). Assumptions marked **Uncertain** are candidates for validation — beliefs that could be wrong and would change the CoD materially if they are. This skill surfaces them with confidence labels so the team can decide what to test. The shared Plan / Validate / Learn loop is defined once in [`../../../reference/validated-learning.md`](../../../reference/validated-learning.md); use **abd-simple-validated-learning** to take Uncertain assumptions through it.

## Neighbours

- `abd-thin-slicing` handles increment ordering after items are scored.
- `abd-delivery-planning` provides the pipeline context where this skill fits as stage 5 (Value Estimation).
- `abd-simple-validated-learning` turns assumptions flagged here into a prioritised validation backlog with hypothesis format, owners, and Plan / Validate / Learn.
