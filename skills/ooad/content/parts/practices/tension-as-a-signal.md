# Tension as a signal — payments example

**Skill:** abd-ooad — **Step 16:** discomfort → **design choice** or **explicit debt**.

**Upstream:** `garbled-payments-spec.md`, `iterative-refinement.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Tensions → term-registry.md

> Tag notes on the class model with `[s1-p16]` — see `templates/domain model template.md` for the full tag table.

All tension analysis — signal, response, and resolution status — belongs in `term-registry.md` Notes, not in a separate table. Use Notes labels (see **`library/term-capture`** for the full label list).

Common Notes labels added at this phase:

- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — the core tension; update or close the entry when resolved
- `Renamed - {{old_name}} → {{new_name}} {{reason}}` — when a tension resolves by renaming or splitting a concept
- `Follow-up - {{question_or_action}}` — unresolved tensions deferred to architecture or product

**Every tension log entry is a term row update, not a separate document.**

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
- [ ] Have you updated `term-registry.md` Notes with `Tension` entries for each signal and their resolution status?
- [ ] Have you noted carry-forward items to Step 17 (cohesion / what changes together)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
