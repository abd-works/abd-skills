# Opportunity Canvas — Concepts

## What is an opportunity canvas?

An opportunity canvas is a tool for **gaining shared understanding** of the key components required to realise an opportunity successfully. It helps a team get started, align on the vision, and quickly organise around the key risks, unknowns, and assumptions that need to be validated. The canvas makes assumptions — and the activity required to validate them — **explicit**, so the team has an accelerated path through uncertainty rather than absorbing it silently into a roadmap or backlog.

The canvas is a **product hypothesis model** — not a feature list, but a structured claim that connects **Customer Problems** to the **Solution Features** that address them, to the **Increments of Value** that deliver them, to the **Key Metrics of Success** that prove they worked, and to the **Revenue Drivers**, **Cost Drivers**, **Key Activities and Resources**, and **Key Partners** that make the business case real. This holistic picture forces the team to see whether the parts of the opportunity actually fit together before any of them are committed to build.

Once the canvas is filled, teams **often** move the assumptions into a small backlog of experiments and cycle learnings back into the canvas.

A common **approach** is to **treat the canvas as living**: decide what to check next, gather evidence, update the bet — so the model does not **freeze** while the world is still unknown. Use **abd-simple-validated-learning** when you want to **mine** assumptions, phrase hypotheses, prioritise tests, and structure the **plan–test–learn** loop.

---

## The Opportunity Canvas

**The Opportunity** is the handle for the whole opportunity — a short name that captures *this* problem–outcome story in plain language. State the Unique Value Proposition, a summary of the customer problems being addressed and how they will be addressed. Every other part of the model on the canvas exists to justify or qualify this one statement. The eight section titles and their guiding questions are fixed across workshops. The table below is the reference — do not add rows or rephrase the questions.

Elements in a section can be grouped into a one-to-many relationship, informal "columns" — where it makes sense for larger opportunities.

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

These sections are often connected formally or informally into *clusters* of problems, users, features, increments, metrics, activities, etc.

---

## Section definitions

**Customer Problems** names the segments and their unique requirements — the people or roles who experience the pain, and what they specifically need that the current situation does not deliver. This row anchors the whole canvas: if Solution Features cannot trace back to at least one named segment here, the solution is solving a private hypothesis, not a stated problem. Good customer problems name a consequence — what happens if this need goes unmet.

**Solution Features** states the major features of the solution. It should read as a direct answer to Customer Problems — the features exist because of those requirements, not because they seemed interesting. A UVP without a named customer pain is not yet a value proposition.

**Increments of Value** describes how value will reach customer segments in sequence — the minimum valuable increment first, then the next meaningful increment(s), then the broader rollout. It bridges Solution Features to Key Activities and Resources by forcing the team to commit to which slice ships first, rather than treating the full feature set as a single delivery event.

**Key Metrics of Success** names the observable signals that will tell the organisation how the product is doing. Each metric should be measurable — a percentage, count, time, or rate — tied where possible to a segment or timeframe. These signals close the loop with Revenue Drivers and Cost Drivers: if the metrics do not move, the business case does not hold.

**Revenue Drivers** answers what customers or the organisation are *really* willing to pay for — not the price, but the value exchange. It should be honest about whether value is captured as direct revenue, cost avoidance, retention, or regulatory compliance. Vague optimism here is usually a signal that Customer Problems need more precision.

**Key Activities and Resources** lists what the product requires to be built, run, and supported — the activities and the people and process capabilities that make them possible. It is the operational foundation of Increments of Value: if an increment cannot be supported by what is listed here, the delivery order assumption is fragile.

**Key Partners** names the external organisations or suppliers the bet depends on — vendors, platforms, channels, or specialist providers without whom a key activity cannot happen. If a partner is load-bearing and absent from this row, they are an undeclared assumption that should be named as one.

**Cost Drivers** identifies the most significant costs inherent in the product — not a budget line, but the structural sources of cost such as integration work, support load, licensing, test environments, and compliance overhead. Together with Revenue Drivers and Key Metrics of Success it closes the business case: the organisation can see what it is paying, what it expects in return, and how it will know.

**Alternatives** captures multiple credible paths forward as distinct clusters (e.g., columns), each representing an option such as "do nothing," "buy a product," "build using XXX platform," "focus on Customer YYYY". These alternatives are modelled to make it easier to evaluate which option makes sense. By noting which options were considered (not just the favoured build), the canvas surfaces key assumptions underlying the decision — options can be verified against each other, especially early in the lifecycle of the opportunity.

---

## Assumptions

**Assumptions** are approached from the perspective that incorrect elements on the Canvas will derail the value proposition of the Opportunity. Teams use a validated learning approach to confirm or refute beliefs, and update the canvas as they learn — keeping evidence and learning visible. The shared Plan / Validate / Learn loop is defined once in [`../../../reference/validated-learning.md`](../../../reference/validated-learning.md).

Mine the opportunity canvas for assumptions by connecting elements across sections into falsifiable statements of the form — *we believe X will Y* — any row can generate assumptions: segment size from Customer Problems, adoption rates from Increments of Value, partner cooperation from Key Partners, willingness to pay from Revenue Drivers. Better to name them here than let them hide in code.

A useful lens for triage is the three **risk-driven hypothesis types**: **Impact**, **Economics**, and **Feasibility**. Each type maps to a cluster of canvas sections that together test a distinct kind of uncertainty.

- **Impact** — *Will users do what we want, and love doing it?* We assume a **Customer** has a **Problem** that can be solved by a **Solution Feature** well enough that they will change their behaviour.
- **Economics** — *Will we achieve the financial outcome?* We assume an **Increment of Value** will generate enough **Revenue** that it justifies its **Cost Drivers** — the effort, investment, and ongoing expense of building and running it.
- **Feasibility** — *Can we build it the right way?* We assume a **Solution Feature** is achievable given the **Key Activities and Resources** and **Partners** available — the team has, or can acquire.

When creating assumptions, label each with its type — Impact, Economics, or Feasibility — so the team can see at a glance whether one risk area is over-represented or ignored, and can sequence experiments to cover all three before committing to build. Use the *We assume <x will y>* format for each assumption.

Use the **abd-simple-validated-learning** skill to turn these assumptions into hypotheses that go through the **plan, validate, and learn** process.

---

## Build method

**Goal:** Produce an opportunity model in the form of a canvas where every section has real depth. You should be able to connect **across** all of the elements — so the model hangs together, not as isolated rows. **Assumptions** should be falsifiable, with a **validate by** line (*who* / *what* / *when*) where the engagement can commit — detailed experiment design and the rest of the **validation workflow** live under **abd-simple-validated-learning**, not here.

### 1. Prepare inputs

Collect **specific** raw material before touching the template — vague prep produces weak canvases:

- **Stakeholder context and perspectives**: who the key voices are (sponsor, product, engineering, domain, ops), what each cares about, and what decision this canvas is feeding.
- **Existing pain**: incidents, tickets, customer or staff quotes, contract clauses, regulatory dates, numbers already being tracked.
- **Alternatives already on the table**: competing approaches, incumbent solutions, or the "do nothing / manual process" option.
- **Known disagreements**: where stakeholders diverge on problem statement, customer segment, or definition of success — surface these in the canvas, do not paper over them.

### 2. Fill each section with intent

Work in canvas order the first time (top to bottom); refine in passes. Every section must be filled — **Opportunity**, **Customer Problems**, **Solution Features**, **Increments of Value**, **Key Metrics of Success**, **Revenue Drivers**, **Key Activities and Resources**, **Key Partners**, and **Cost Drivers**. Once the eight sections are filled, mine the completed canvas for **Assumptions** and add them as a separate block below the canvas — not as a ninth row.

### 3. Trace the spine

From Solution Features and Increments of Value back to Customer Problems: every "what we build / ship" should speak to a named segment and requirement. From Key Metrics of Success, Revenue Drivers, and Cost Drivers: the numbers or signals should show why the org would proceed and how it will know. Each Assumption should be traceable to a test the *team* can **schedule and own** in their own **validation workflow**.

### 4. Ensure parity

The table canvas (`opportunity-canvas.md`) and the section canvas / plain-text (`opportunity-canvas-sections.md`, `opportunity-canvas.txt`) must carry the same Opportunity, same row coverage, and the same Assumptions with the same validate-by intent. No drift between files.
