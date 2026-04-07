# Tension as a signal — payments example

**Skill:** abd-ooad — **Step 16:** discomfort → **design choice** or **explicit debt**.

**Upstream:** `garbled-payments-spec.md`, `iterative-refinement.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Tensions → responses

| Tension | Signal | Response |
|---------|--------|----------|
| Risk owns dispute vs Support | **Two orgs**, one noun “dispute” | **Dispute** aggregate in **risk BC**; Support **reads** or **opens ticket** — link by id. |
| Digital ship on auth vs physical on settle | **Different fulfillment triggers** | **Policy** per **product type** — **not** one rule inside Payment. |
| Local vs global product matrix | **Same UI**, different **constraints** | **RegionProfile** + **catalog** refs — **composition** at checkout. |
| Sanctions “before method” vs “before money moves” | **Two compliance checkpoints** | **Gate A** (browse) vs **Gate B** (capture) — name both in model narrative. |

---

## Carry forward → Step 17

**Cohesion:** what **changes together** for **Payment** vs **catalog** vs **fulfillment**?

---

## Continual refinement (this step)

- **Delta:** tension → **boundary** or **explicit debt**; update **modules** / **Interactions** in the spec when a tension resolves into a new concept or BC handoff.

---

## Action Checklist

- [ ] Have you reviewed all tensions logged since Step 1 and resolved or escalated each one?
- [ ] Does each resolved tension either produce a new concept boundary or an explicit debt entry?
- [ ] Have you updated the spec modules / Interactions for any tension that resolved into a new concept?
- [ ] Have you noted carry-forward items to Step 17 (cohesion / what changes together)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
