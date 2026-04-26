# abd-answers retrieval input — abd-simple-validated-learning

**Scope:** This skill is grounded in the same ABD **Opportunity / Idea Canvas** training extension as **abd-opportunity-canvas** — **Validated Learning Kanban**, **uncertainty → experiment** pattern, and the **full assumption / risk checklist** (slides 12–14 in the *canvas* deck). Full deck context: **`../../abd-opportunity-canvas/reference/opportunity-canvas-source-materials.md`** §5, verbatim extract **`../../abd-opportunity-canvas/reference/canvas-pptx-extract.md`**.

**RAG (optional):** `npm run rag:query` from the **abd-answers** agent root with queries such as `validated learning kanban opportunity canvas`, `uncertainty backlog`, `assumption test opportunity` — use **`--folders "01 Agile Practices"`** when the index supports it. If quota blocks RAG, use the **Kept chunks** below (sourced from the on-disk extract).

## Kept chunks (verbatim)

### Kept chunk 1

- **Source location:** `../../abd-opportunity-canvas/reference/canvas-pptx-extract.md` (slides 12–13) — *canvas.pptx* / equivalent training path under Agile Practices
- **Relevance:** `procedure` — bridge from **Idea Canvas** to **Validated Learning Kanban**; **Plan / Validation / Learning**; stand-ups to coordinate validation
- **Query:** (manual extract)

```
The team collaborates on the Idea Canvas to identify uncertainty that is validated on a "Validated Learning Kanban Board"

Validation Backlog by common area
Plan
Validation
Learning

### Notes:
We used Kanban has a the mechanism to coordinating our validation activities

Stand ups occurred on a daily basis with team from IT, Marketing, Product, Legal, Security
```

### Kept chunk 2

- **Source location:** `../../abd-opportunity-canvas/reference/canvas-pptx-extract.md` (slide 13)
- **Relevance:** `example` — uncertainty → small experiment → validate reaction; **Uncertainty Backlog**
- **Query:** (manual extract)

```
Create a Validated Learning Kanban to test assumptions; leverage learnings to refine the Opportunity Canvas

We Don't Know
which of our customers are interested in a
Consolidated Bill, 

Therefore we will manually create Consolidated Bills send to a small cohort of each of our segments, then validate the reaction…
Learn
Validate

Plan

Uncertainty Backlog
```

### Kept chunk 3

- **Source location:** `../../abd-opportunity-canvas/reference/canvas-pptx-extract.md` (slide 14, excerpt)
- **Relevance:** `rule` / `procedure` — **multi-area** checklist: Problem/Solution fit, Capability/Market, Technology, Delivery, Other  
- **Query:** (manual extract)

```
Are there uncertainties or risks associated with the items on your backlog? 
Problem / Solution Fit
Do the Customer Segments consider this their top pain point(s)
Does our Opportunity (set of capabilities) address our Customer Segment's top problems? 
…
Capability / Market Fit
Does the Opportunity identify a unique value proposition in comparison to current competitors or existing alternatives?
…
Technology Feasibility
Is the solution technically feasible? What are the riskiest / uncertain parts of the architecture?
…
Delivery Feasibility
Which parts of my product depend on the ability of our Key Partners? Internal Key Resources?
…
Other Feasibility
Are there any Legal, Compliance or Regulatory impacts based on Opportunity?
…
```

*(Full list of questions is in the same file; the agent may read the file for the complete checklist.)*

## Summary table (non-verbatim)

| Topic | Use in this skill |
| --- | --- |
| **Kanban** | **Plan** → **Validation** → **Learning**; backlog **by area**; refine **Opportunity Canvas** with learnings |
| **Example pattern** | *We don't know X* → *therefore* small experiment → validate → update backlog/canvas |
| **Checklist** | Scan **all** main risk types so fragile beliefs are not only on the “obvious” rows |

## Coverage and run log

| Run | Command / note | Result |
| --- | --- | --- |
| 1 | Manual extract from `canvas-pptx-extract.md` (2026-04-26) | Chunks 1–3 above |
