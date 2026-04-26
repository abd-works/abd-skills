---
name: abd-opportunity-canvas
catalog_garden_tier: practice
catalog_garden_order: 16
catalogue_one_liner: >-
  Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build.
description: >-
  Frame a candidate opportunity, align stakeholders on a shared bet, and make assumptions explicit before committing to build.
---
Manual: [Practice manual](./manual/index.html)

# abd-opportunity-canvas

## Purpose

This skill exists so you **do not start "building a solution"** while people are thinking about **a different problem**, **a different customer**, or **a different definition of success**. It makes a **candidate opportunity** explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that **downstream build and delivery work** points at the **same** bet instead of at private mental models. Every row is also an **assumption surface**: beliefs about customers, value, and capability that can be made explicit, grounded into falsifiable hypotheses, and scheduled as validated learning experiments — so the uncertainty the canvas surfaces is **tracked and worked off**, not silently absorbed into code.

## When to use this skill

Load this skill when any of the following apply:

- A **new or restarted initiative** is still fuzzy: sponsors, product, and engineering would not give you the **same two-sentence** summary of the problem and the bet.

- You need **one artifact** that links **why this matters** → **who** → **what we might do** → **how we'd know** → **what we're assuming**, so the **next** workshops (mapping, prioritisation, delivery) are not arguing past each other.
- You need to **co-create a common model** that aligns multiple stakeholders on the opportunity.
- The opportunity is **large enough to have moving parts**: multiple customer segments with different needs, competing solution directions, several key partners or resource constraints, and a business case that only holds if several of those pieces align. When the canvas rows would each be non-trivial to fill, the canvas is earning its keep by forcing that complexity into the open before build starts.

Use the Opportunity Canvas when an opportunity is likeley to tranlsate to an *initiative*. 

For smaller *features* 
 - if you want to understand how organizational goals translate to user behavior, and / prioritize explore what feature could enable that beavior consider **impact mapping** instead
 - if you want to compare well scoped features where it is reasonable to calculate economic benefit consider using  **cost of delay** instead

## Agent Instructions

1. **Templates**

  Generate the Opportunity Canvas using the following templates:

   | Template | What to produce |
   | -------- | ---------------- |
   | `templates/opportunity-canvas.md` | **Table** canvas: one markdown table row per ABD section, columns for individual items. `OPPORTUNITY:`, `ALTERNATIVES:`, and `ASSUMPTION:` fields sit outside the table. Use for at-a-glance layout and workshop walls. |
   | `templates/opportunity-canvas-sections.md` | **Section** canvas: for each ABD row, a heading + verbatim guiding questions + a `PREFIX:` answer line (`CUSTOMER_PROBLEMS:` … `COST_DRIVERS:`, plus `OPPORTUNITY:`, `ALTERNATIVES:`, `ASSUMPTION:`). Use when prose depth is needed. |
   | `templates/opportunity-canvas.txt` | Plain-text parity with the section `.md` — same sections, same prefix lines, same content for the same engagement. |

2. **Rules**

   After generating, review each bundled rule (**DO** / **DO NOT** / examples) against the saved outputs.

---

## What is an opportunity canvas?

An opportunity canvas is a tool for **gaining shared understanding** of the key components required to realise an opportunity successfully. It helps a team get started, align on the vision, and quickly organise around the key risks, unknowns, and assumptions that need to be validated. The canvas makes assumptions — and the activity required to validate them — **explicit**, so the team has an accelerated path through uncertainty rather than absorbing it silently into a roadmap or backlog.

The canvas is a **product hypothesis model** — not a feature list, but a structured claim that connects **Customer Problems** to the **Solution Features** that address them, to the **Increments of Value** that deliver them, to the **Key Metrics of Success** that prove they worked, and to the **Revenue Drivers**, **Cost Drivers**, **Key Activities and Resources**, and **Key Partners** that make the business case real. This holistic picture forces the team to see whether the parts of the opportunity actually fit together before any of them are committed to build.

Once the canvas is filled, the assumptions that surface in each area can be validated using a Plan → Validate → Learn approach. The team works through the uncertainty represented on the canvas through a backlog of small experiments, and what it learns cycles back to refine the model. The canvas is not a one-time artifact — it is a living model of the bet.

### Canonical ABD Opportunity Canvas (eight rows)

The eight section titles and their guiding questions are fixed across workshops. The table below is the reference — do not add rows or rephrase the questions.

| **Section** | **Guiding questions** |
|-------------|------------------------|
| **Customer Problems** | What are our key customer segments and what are the unique requirements of each customer segment? |
| **Solution Features** | What is our Unique Value Proposition to our Customer Segments? What customer problem are we solving? What are the major features of our solution? |
| **Increments Of Value** | What are the increments of value we will deliver to our Customer Segments? What is the minimum valuable increment? In what order will value reach each segment? |
| **Key Metrics of Success** | What are the key metrics that will tell us how our product is doing? |
| **Revenue Drivers** | For what value are our Customers really willing to pay? |
| **Key Activities and Resources** | What Key Activities does our Product Require (e.g. to Build, to Support, etc.)? What Key Resources [People] and Capabilities [Process] does our Product leverage? |
| **Key Partners** | Who are our Key Partners? Who are our key Suppliers? |
| **Cost Drivers** | What are the most important costs drivers inherent in our Product? |

---

## Core concepts

**The Opportunity** is the handle for the whole bet — a short name that captures *this* problem–outcome story in plain language. The name should make clear who is affected and what moving the needle looks like. Every other part of the model on the canvas exists to justify or qualify this one statement.


**Customer Problems** names the segments and their unique requirements — the people or roles who experience the pain, and what they specifically need that the current situation does not deliver. This row anchors the whole canvas: if Solution Features cannot trace back to at least one named segment here, the solution is solving a private hypothesis, not a stated problem. Good customer problems name a consequence — what happens if this need goes unmet.

**Solution Features** states the Unique Value Proposition, the specific customer problem being addressed, and the major features of the solution. It should read as a direct answer to Customer Problems — the features exist because of those requirements, not because they seemed interesting. A UVP without a named customer pain is not yet a value proposition.

**Increments of Value** describes how value will reach customer segments in sequence — the minimum valuable increment first, then the next meaningful step, then the broader rollout. It bridges Solution Features to Key Activities and Resources by forcing the team to commit to which slice ships first, rather than treating the full feature set as a single delivery event.

**Key Metrics of Success** names the observable signals that will tell the organisation how the product is doing. Each metric should be measurable — a percentage, count, time, or rate — tied where possible to a segment or timeframe. These signals close the loop with Revenue Drivers and Cost Drivers: if the metrics do not move, the business case does not hold.

**Revenue Drivers** answers what customers or the organisation are *really* willing to pay for — not the price, but the value exchange. It should be honest about whether value is captured as direct revenue, cost avoidance, retention, or regulatory compliance. Vague optimism here is usually a signal that Customer Problems need more precision.

**Key Activities and Resources** lists what the product requires to be built, run, and supported — the activities and the people and process capabilities that make them possible. It is the operational foundation of Increments of Value: if an increment cannot be supported by what is listed here, the delivery order assumption is fragile.

**Key Partners** names the external organisations or suppliers the bet depends on — vendors, platforms, channels, or specialist providers without whom a key activity cannot happen. If a partner is load-bearing and absent from this row, they are an undeclared assumption that should be named as one.

**Cost Drivers** identifies the most significant costs inherent in the product — not a budget line, but the structural sources of cost such as integration work, support load, licensing, test environments, and compliance overhead. Together with Revenue Drivers and Key Metrics of Success it closes the business case: the organisation can see what it is paying, what it expects in return, and how it will know.

**Alternatives** forces the canvas to acknowledge that a choice was made. Name at least one credible path that is not the favoured build — do nothing, buy a product, partner, narrow scope, or defer. Without alternatives the canvas presents a recommendation disguised as an analysis. Alternatives also surface assumptions: if the favoured option is claimed to be better than an alternative, that claim can usually be tested.

**Assumptions** hold the fragile beliefs that, if wrong, would change the recommendation. Each assumption should be falsifiable — *we believe X will Y* — paired with a validation path that names who does what by when to confirm or refute it. The canvas surfaces uncertainty; a Validated Learning Kanban (Plan → Build → Measure → Learn) is how the team works it off. Any row can generate assumptions — segment size from Customer Problems, adoption rates from Increments of Value, partner cooperation from Key Partners, willingness to pay from Revenue Drivers. Better to name them here than let them hide in code.

### Validated Learning Kanban

Once the canvas is filled, uncertainty does not stay on the page — it moves into a **Validated Learning Kanban** with three stages: Plan, Validate, and Learn. Each assumption becomes a small, scheduled experiment that the team can run before committing to full build. A multi-area checklist covers the main risk categories — problem/solution fit, capability and market fit, technology, delivery, and regulatory or commercial constraints — so the team can scan for fragile beliefs across the whole canvas, not just the obvious ones.

---

## Build

**Goal:** Produce a serious canvas where every row does real work. You should be able to trace from Solution Features and Increments of Value back to Customer Problems, and from Key Metrics of Success, Revenue Drivers, and Cost Drivers to a coherent business story. Every Assumption should have a scheduled validate-by test.

### 1. Prepare inputs

Collect **specific** raw material before touching the template — vague prep produces weak canvases:

- **Who is in the room** (sponsor, product, engineering, domain, ops) and **what decision** this canvas feeds (budget, pilot scope, kill/continue, vendor shortlist).
- **Existing pain**: incidents, tickets, quotes from customers or staff, contract clauses, regulatory dates, numbers already tracked.
- **Competitive or internal alternatives** already on the table (including "manual process for another year").
- **Top disagreements** in the group: problem statement, customer segment, or success metric — write them down; the canvas should surface them, not hide them.

### 2. Fill each section with intent

Work in canvas order the first time (top to bottom); refine in passes. For each section, pass this bar:

| Section | What "not a joke" looks like | Weak (rewrite) |
| --- | --- | --- |
| **Opportunity** | Names the **bet** in plain language (outcome + who), not a project label. | "Project Phoenix", "Digital transformation." |
| **Customer Problems** | **Segments** and **unique requirements** per segment (consequence if unmet). | "Everyone", "stakeholders." |
| **Solution Features** | **UVP**, which **customer problem**, **major features** — tied to those segments. | Feature list with no UVP or problem. |
| **Increments of Value** | **Minimum valuable increment** and delivery order per segment. | Vague "digital." |
| **Key Metrics of Success** | **Observable** measures of product/org success (ideally timebound or threshold). | "Success." |
| **Revenue Drivers** | For **what value** customers (or other parties) **really** pay — aligned to segments. | Unpriced optimism. |
| **Key Activities and Resources** | **Activities** to build/support; **people** and **process** capability required. | "The team will do it." |
| **Key Partners** | **Partners** and **suppliers** the bet depends on. | Empty if partners are load-bearing. |
| **Cost Drivers** | **Important costs** in the product/system. | Only headcount, no other drivers. |
| **Alternatives** | At least one **credible** path that is not "our favourite build." | Empty. |
| **Assumptions** | **Falsifiable** belief with a **validate by** clause — who/what/when. | Opinion with no check. |

Add more Assumption lines if the bet is fragile; each gets a validate-by where possible.

### 3. Trace the spine

From Solution Features and Increments of Value back to Customer Problems: every "what we build / ship" should speak to a named segment and requirement.

From Key Metrics of Success, Revenue Drivers, and Cost Drivers: the numbers or signals should show why the org would proceed and how it will know.

Each Assumption ties to a test the team can schedule on the Validated Learning Kanban.

### 4. Ensure parity

The table canvas (`opportunity-canvas.md`) and the section canvas / plain-text (`opportunity-canvas-sections.md`, `opportunity-canvas.txt`) must carry the same Opportunity, same row coverage, and the same Assumptions with the same validate-by intent. No drift between files.

### 5. Rule pass

Read the bundled rules against both files; fix failures.

---

## Validate

**Goal:** Act as a reviewer — would another facilitator trust this canvas to drive the next learning conversation?

- **Sponsor and product** — Can see clear Customer Problems and Solution Features, and a business case through Key Metrics of Success, Revenue Drivers, and Cost Drivers.
- **Engineering and design** — Can see Key Activities and Resources, Key Partners, and testable Assumptions with validate-by clauses.
- **Parity** — Table and section/text files match for the same engagement; no extra row or Assumption in one file only.
- **Honest bar** — Do not claim this practice requires steps or wording that this page and the bundled rules do not actually set.

Re-run a rule pass if any of the above fail.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- execute_rules:bundle_rules:end -->
