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

This skill exists so you **do not start "building a solution"** while people are thinking about **a different problem**, **a different customer**, or **a different definition of success**. 

This skill makes an **opportunity** explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that **downstream build and delivery work** is based on a shared model. This skill captures this alignment as an **opportunity model**, in the form of a **opportunity canvas**.

Every part of the canvas is also a candidate **assumption** — beliefs about customers, value, and capability that teams often make explicit, turn into falsifiable statements, and run through a lightweight validation path **outside** this skill (see **abd-simple-validated-learning**). This skill’s job is to **surface** that uncertainty in the model; *who* confirms or refutes *what* *by when* is planned and run by the team in whatever **workflow** or **working agreement** they use to track those checks.

## When to use this skill

Load this skill when any of the following apply:

- A **new or restarted initiative** is ambiguous and/or complex: sponsors, product, and engineering would not agree on problems, users, solutions, effort, etc
- You want to **co-create a common model** that aligns multiple stakeholders on the opportunity: **why this matters** → **who** → **what we might do** → **how we'd know** → **what we're assuming**, so the **next** workshops (mapping, prioritisation, delivery) are not arguing past each other.

- The opportunity is **large enough to have multiple moving parts**: multiple customer segments with different needs, competing solution directions, several key partners or resource constraints, and a business case that only holds if several of those pieces align. When the canvas rows would each be non-trivial to fill, the canvas is earning its keep by forcing that complexity into the open before build starts.

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

Once the canvas is filled, teams **often** move the assumptions into a small backlog of experiments and cycle learnings back into the canvas. 

A common **approach** is to **treat the canvas as living**: decide what to check next, gather evidence, update the bet—so the model does not **freeze** while the world is still unknown. Use **abd-simple-validated-learning** when you want to **mine** assumptions, phrase hypotheses, prioritise tests, and structure the **plan–test–learn** loop.
---

## Core concepts

### The Opportunity Canvas
**The Opportunity** is the handle for the whole opportunuty — a short name that captures *this* problem–outcome story in plain language. State the Unique Value Proposition, a summary of the customer problems being addressed and how they eill be addressed. Every other part of the model on the canvas exists to justify or qualify this one statement. 
The eight section titles and their guiding questions are fixed across workshops. The table below is the reference — do not add rows or rephrase the questions.

Elements in a sections can be grouped into a one to many relationship, informal "columns" - where it makes sense for larger opportunities.

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

These sections are often connected formally or informally into *clusters* of problems, users, features, increments, metrics, activities etc

**Customer Problems** names the segments and their unique requirements — the people or roles who experience the pain, and what they specifically need that the current situation does not deliver. This row anchors the whole canvas: if Solution Features cannot trace back to at least one named segment here, the solution is solving a private hypothesis, not a stated problem. Good customer problems name a consequence — what happens if this need goes unmet. *Examples: customer segments, buyer vs user distinction, early adopters, targeted market size.*

**Solution Features** states the major features of the solution. It should read as a direct answer to Customer Problems — the features exist because of those requirements, not because they seemed interesting. A UVP without a named customer pain is not yet a value proposition. *Examples: top 3 problems or opportunities addressed, gains and pains resolved, key game features, new behaviours replacing manual processes, other functionality.*

**Increments of Value** describes how value will reach customer segments in sequence — the minimum valuable increment first, then the next meaningful increment(s), then the broader rollout. It bridges Solution Features to Key Activities and Resources by forcing the team to commit to which slice ships first, rather than treating the full feature set as a single delivery event. *Examples: increments that enable learning, risk avoidance, or direct value delivery.*

**Key Metrics of Success** names the observable signals that will tell the organisation how the product is doing. Each metric should be measurable — a percentage, count, time, or rate — tied where possible to a segment or timeframe. These signals close the loop with Revenue Drivers and Cost Drivers: if the metrics do not move, the business case does not hold.

**Revenue Drivers** answers what customers or the organisation are *really* willing to pay for — not the price, but the value exchange. It should be honest about whether value is captured as direct revenue, cost avoidance, retention, or regulatory compliance. Vague optimism here is usually a signal that Customer Problems need more precision. *Examples: pricing model, potential sales volume, revenue uplift.*

**Key Activities and Resources** lists what the product requires to be built, run, and supported — the activities and the people and process capabilities that make them possible. It is the operational foundation of Increments of Value: if an increment cannot be supported by what is listed here, the delivery order assumption is fragile. *Examples: systems and departments involved, internal and external assets, existing vs new assets required, path to customer, channels.*

**Key Partners** names the external organisations or suppliers the bet depends on — vendors, platforms, channels, or specialist providers without whom a key activity cannot happen. If a partner is load-bearing and absent from this row, they are an undeclared assumption that should be named as one.

**Cost Drivers** identifies the most significant costs inherent in the product — not a budget line, but the structural sources of cost such as integration work, support load, licensing, test environments, and compliance overhead. Together with Revenue Drivers and Key Metrics of Success it closes the business case: the organisation can see what it is paying, what it expects in return, and how it will know. *Examples: hardware and software costs, new build vs ongoing operations.*

**Alternatives** captures multiple credible paths forward as distinct clusters (e.g., columns), each representing an option such as "do nothing," "buy a product," "build using XXX platform," "Focus on Customer YYYY". These alternatives are modelled to make it easier to evaluate wich option makes sense. By noting which options were considered (not just the favoured build), the canvas surfaces key assumptions underlying the decision — options be verified against each other, especially early on in kifecycle of the opportunity.


### Assumptions
**Assumptions** are approached from the perspective that incorrect elements on of the Canvas will derail the value proposition of the Opportunity.  Teams use a validated learning approach to confirm or refute beliefs, and update the canvas as they learn — keeping evidence and learning visible. 

Plan - what to test, smallest useful check, owner, and date; 
Learn - what we took away and how the bet or canvas updates; 
Validate - run the check and collect evidence to confirm or refute the belief.

Mine the opportunity canvas for assumptions by connecting elements across sections into falsifiable statements of the form — *we believe X will Y* — any row can generate assumptions: segment size from Customer Problems, adoption rates from Increments of Value, partner cooperation from Key Partners, willingness to pay from Revenue Drivers. Better to name them here than let them hide in code.

A useful lens for triage is the three **risk-driven hypothesis types**: **Impact**, **Economics**, and **Feasibility**. Each type maps to a cluster of canvas sections that together test a distinct kind of uncertainty.

- **Impact** — *Will users do what we want, and love doing it?* We assume a **Customer** has a **Problem** that can be solved by a **Solution Feature** well enough that they will change their behaviour.
- **Economics** — *Will we achieve the financial outcome?* We assume an **Increment of Value** will generate enough **Revenue** that it justifies its **Cost Drivers** — the effort, investment, and ongoing expense of building and running it.
- **Feasibility** — *Can we build it the right way?* We assume a **Solution Feature** is achievable given the **Key Activities and Resources** and **Partners** available — the team has, or can acquire.

When creating assumptions, label each with its type — Impact, Economics, or Feasibility — so the team can see at a glance whether one risk area is over-represented or ignored, and can sequence experiments to cover all three before committing to build. Usethe *We assume <x will y>* format for each assumption.

Use the **abd-simple-validated-learning** skill to turn these assumptions into hypothesis that go through the **plan, validate, and learn** process. 

---

## Build

**Goal:** Produce an opportunity model in the form of a canvas; where every section has real depth. You should be able to connect **across** all of the elements—so the model hangs together, not as isolated rows. **Assumptions** should be falsifiable, with a **validate by** line (*who* / *what* / *when*) where the engagement can commit — detailed experiment design and the rest of the **validation workflow** live under **abd-simple-validated-learning**, not here.

### 1. Prepare inputs

Collect **specific** raw material before touching the template — vague prep produces weak canvases:

- **Stakeholder context and perspectives**: who the key voices are (sponsor, product, engineering, domain, ops), what each cares about, and what decision this canvas is feeding (budget, pilot scope, kill/continue, vendor shortlist).
- **Existing pain**: incidents, tickets, customer or staff quotes, contract clauses, regulatory dates, numbers already being tracked.
- **Alternatives already on the table**: competing approaches, incumbent solutions, or the "do nothing / manual process" option.
- **Known disagreements**: where stakeholders diverge on problem statement, customer segment, or definition of success — surface these in the canvas, do not paper over them.

### 2. Fill each section with intent

Work in canvas order the first time (top to bottom); refine in passes. Every section must be filled — **Opportunity**, **Customer Problems**, **Solution Features**, **Increments of Value**, **Key Metrics of Success**, **Revenue Drivers**, **Key Activities and Resources**, **Key Partners**, and **Cost Drivers**. Refer to the Core Concepts section for what each section means and what good looks like.

Once the eight sections are filled, mine the completed canvas for **Assumptions** and add them as a separate block below the canvas — not as a ninth row.

### 3. Trace the spine

From Solution Features and Increments of Value back to Customer Problems: every "what we build / ship" should speak to a named segment and requirement.

From Key Metrics of Success, Revenue Drivers, and Cost Drivers: the numbers or signals should show why the org would proceed and how it will know.

Each Assumption should be traceable to a test the *team* can **schedule and own** in their own **validation workflow** (this skill does not run that workflow for them).

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
### Rule: All canvas sections are filled and connect into a coherent narrative

**Scanner:** Manual review

A canvas passes when every section — **Customer Problems**, **Solution Features**, **Increments of Value**, **Key Metrics of Success**, **Revenue Drivers**, **Key Activities and Resources**, **Key Partners**, and **Cost Drivers** — contains real content, and the sections hang together as a single coherent story. **Assumptions** are a separate block added after the canvas is complete — they are not a ninth section of the canvas. Failing means any canvas section is empty or placeholder, or the sections read as independent lists that could belong to different canvases entirely.

#### DO

- Fill every section and write each one as a response to the sections it depends on, so a reader can follow the chain from Customer Problems through to Cost Drivers without the narrative breaking.

  **Example (pass):** Customer Problems names coordinator scheduling pain; Solution Features describes the features that address that pain; Increments sequences which segment gets value first; Key Activities names the integration work those increments require; Revenue Drivers names the retention and call-reduction value captured; Cost Drivers names the integration and support costs — every section is about the same bet and references the same customer and solution.

#### DO NOT

- Leave any section empty, placeholder, or deferred without a stated reason.

  **Example (fail):** `KEY_PARTNERS:` with no content, or `COST_DRIVERS: TBD` — empty sections hide load-bearing dependencies or costs that are part of the bet.

- Fill sections independently so they describe different scopes or audiences without connecting to the same customer problem and solution.

  **Example (fail):** Customer Problems mentions dealer coordinators; Solution Features describes a consumer mobile app; Increments references an internal analytics dashboard — a reviewer cannot trace a single narrative from start to finish.

**Source:** Agile by Design Opportunity Canvas — all-sections coverage and coherent model requirement.

### Rule: Alternatives are documented as substantially different columns

**Scanner:** Manual review

When alternatives are present on the canvas, each one passes when it is structured as a distinct column that represents a meaningfully different path — a different customer focus, build approach, buy option, or do-nothing scenario — not a minor variation of the main case. Failing means an alternative column is only a tweak on the same solution (different technology, different timeline) rather than a genuinely different strategic option.

#### DO

- Document each alternative as a column whose content in at least one key section differs substantially from the main case — different segment focus, different solution approach, different business model, or no build at all.

  **Example (pass):** Main case column: build a self-service scheduling platform for dealer coordinators. Alternative column: integrate with an existing third-party SaaS scheduling tool, different Key Activities (integration vs build), different Cost Drivers (licensing vs engineering), different Increments of Value (configuration milestones vs feature releases).

#### DO NOT

- Add an alternative column that only changes a technology choice or delivery detail while keeping the same customer, problem, solution shape, and business case.

  **Example (fail):** Alternative column that swaps React for Angular in Solution Features while all other sections mirror the main case — this is an implementation variant, not a strategic alternative worth modelling.

**Source:** Agile by Design Opportunity Canvas — Alternatives as canvas columns.

### Rule: Assumptions connect canvas elements and are stated as beliefs that could be wrong

**Scanner:** Manual review

A well-formed assumption passes when it names at least multiple connected canvas elements across sections and expresses a belief that could be disproved — not a plan, a task, or a statement of fact. Failing means an assumption is a solution idea restated as certainty, or it floats free of the canvas with no traceable connection to a section's content.

#### DO

- Name the canvas section(s) the assumption connects, and state the belief as something that could turn out to be false.

  **Example (pass):** `ASSUMPTION: (Impact) We believe dealer coordinators (Customer Problems) will adopt the self-service reschedule feature (Solution Features) rather than calling support.`

#### DO NOT

- State an assumption with no reference to any canvas section.

  **Example (fail):** `ASSUMPTION: Users will love it.` — no segment named, no canvas section referenced, not falsifiable.

#### DO

- Label the assumption type — **Impact**, **Economics**, or **Feasibility** — to show which canvas cluster it comes from.

  **Example (pass):** `ASSUMPTION: (Economics) We assume the SMB pricing in Revenue Drivers will exceed the integration and support costs in Cost Drivers within 12 months.`

#### DO NOT

- Write an assumption that describes a delivery step or plan rather than a belief that could be wrong.

  **Example (fail):** `ASSUMPTION: We will run a pilot in Q2.` — this is a task, not a belief about the opportunity that could fail.

**Source:** Agile by Design opportunity canvas and validated learning practices.

### Rule: Increments of Value names a minimum valuable increment

**Scanner:** Manual review

The **Increments of Value** section passes when it identifies a first increment that is smaller than the full solution — something the team could ship and learn from — and states which customer segment receives that value first. Failing means the section treats the full feature set as a single delivery event, uses vague language with no specificity about what ships first, or lists features rather than increments.

#### DO

- Name the minimum valuable increment explicitly and state who it reaches first.

  **Example (pass):** `INCREMENTS_OF_VALUE: (1) Live bay calendar for dealer coordinators — minimum increment, validates core scheduling visibility; (2) Push notification on booking change for fleet managers; (3) Dealer-facing reschedule self-service flow.`

#### DO NOT

- Describe all features as one delivery without naming a minimum or an ordering.

  **Example (fail):** `INCREMENTS_OF_VALUE: Full scheduling platform with calendar, notifications, and self-service reschedule` — this is a scope description, not a sequenced increment plan.

- Use a vague phrase that does not commit to a slice.

  **Example (fail):** `INCREMENTS_OF_VALUE: Digital solution for dealers` — no minimum, no segment, no ordering.

**Source:** Agile by Design Opportunity Canvas — Increments of Value section.

### Rule: Key Metrics of Success are measurable signals

**Scanner:** Manual review

The **Key Metrics of Success** section passes when each metric is expressed as something observable and countable — a rate, percentage, count, time, or threshold — not a feeling, a direction, or a vague goal. Failing means the section lists outcomes that cannot be measured without agreeing on a definition first, or uses aspirational language with no signal the team could actually track.

#### DO

- Express each metric as a measurable signal with enough specificity that the team could evaluate whether it has been reached.

  **Example (pass):** `KEY_METRICS_OF_SUCCESS: Inbound reschedule calls per dealer per week drops by at least 40% within 60 days of go-live; dealer coordinator satisfaction score (CSAT) on booking process ≥ 4.2/5 by end of pilot.`

#### DO NOT

- Use aspirational language that cannot be observed or measured from any data source.

  **Example (fail):** `KEY_METRICS_OF_SUCCESS: Improved dealer experience, better scheduling, growth` — none of these are measurable without a separate definition conversation.

- Use a single word or phrase that names a topic rather than a signal.

  **Example (fail):** `KEY_METRICS_OF_SUCCESS: Success` or `KEY_METRICS_OF_SUCCESS: Customer satisfaction` — these are categories, not metrics.

**Source:** Agile by Design Opportunity Canvas — Key Metrics of Success section.

### Rule: Opportunity states the UVP connecting customer, problem, and solution

**Scanner:** Manual review

The `OPPORTUNITY:` field passes when it contains a **Unique Value Proposition** — a statement that connects the customer segment to the problem they have and the solution that addresses it. All three elements must be present: who the customer is, what problem or need is being addressed, and what the solution does for them. Failing means the field is a project label, a technology direction, or a solution description with no named customer or problem.

#### DO

- Write the Opportunity as a UVP that names the customer, states the problem or need, and describes how the solution addresses it.

  **Example (pass):** `OPPORTUNITY: Dealer service coordinators lose time and credibility managing reschedules across three disconnected systems — a unified scheduling view with real-time bay status and push notifications gives coordinators confidence and reduces inbound reschedule calls by 40%.`

#### DO NOT

- Use a project codename, programme title, or technology direction without the customer, problem, and solution.

  **Example (fail):** `OPPORTUNITY: Project Phoenix` — no customer, no problem, no solution value stated.

- Describe only the solution with no customer or problem context.

  **Example (fail):** `OPPORTUNITY: A real-time scheduling platform with calendar integration and notifications` — solution-only, no segment named, no problem connected.

**Source:** Agile by Design Opportunity Canvas — Opportunity field and UVP framing.

### Rule: Solution Features spine traces to Customer Problems with a UVP

**Scanner:** Manual review

The canvas passes the spine check when **Solution Features** states a Unique Value Proposition and its major features can each be traced to at least one named segment or problem in **Customer Problems** — and every named segment in Customer Problems is addressed by at least one feature. Failing means features appear with no stated problem, a named segment has no solution addressing their need, or Solution Features is a feature list with no UVP.

#### DO

- Include a UVP in Solution Features and write each feature so it is clear which problem or segment from Customer Problems it addresses.

  **Example (pass):** `SOLUTION_FEATURES: UVP — a booking slot the dealer can rely on. Live bay calendar (addresses: coordinator need for real-time bay visibility — Customer Problems row 1); push notification on change (addresses: fleet manager need for booking confirmation — Customer Problems row 2).`

#### DO NOT

- List features in Solution Features with no UVP and no link to a Customer Problems segment or requirement.

  **Example (fail):** `SOLUTION_FEATURES: Calendar view, notification system, reporting dashboard.` — no UVP, no problem linked, no segment referenced.

- Name a customer segment in Customer Problems and leave it without any coverage in Solution Features.

  **Example (fail):** `CUSTOMER_PROBLEMS: Fleet managers — need bulk booking confirmation` with no feature for fleet managers in Solution Features — the segment is named but the solution ignores them.

**Source:** Agile by Design Opportunity Canvas — Customer Problems and Solution Features spine.
<!-- execute_rules:bundle_rules:end -->
