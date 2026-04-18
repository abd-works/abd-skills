# Refine names — illustrative thread

**Phase ID:** `refine-names`

**Skill:** abd-ooad — **Stage F** — **ubiquitous language** alignment. *(Optional payments-themed example below; substitute your domain.)*

**Upstream:** `validate-with-scenarios.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Renames and preserved terms → term-registry.md

> Tag notes on the class model with `[s1-p19]` — see `templates/domain model template.md` for the full tag table.

All rename decisions and terms-to-preserve belong in `term-registry.md` Notes. Use Notes labels (see **`library/term-capture`** for the full label list).

Common Notes labels added at this phase:

- `Renamed - {{old_name}} → {{new_name}} {{reason}}` — every rename from weak/generic to domain-specific
- `Promoted - {{from_target}} → {{to_target}} {{reason}}` — when a rename also changes a term's target (e.g., property promoted to class)
- `Follow-up - {{question_or_action}}` — names deferred pending spec or team alignment

Terms from spec that must be preserved verbatim (e.g., `idempotency key`, `3DS`, `MoR`, `partial capture`, `settlement`) get a row in `term-registry.md` confirming the canonical spelling used in events and UI.

---

## Carry forward → `model-in-layers` (optional appendix)

**Layer** the model — **domain vs application vs infra** + optional **ASCII** summary. Not part of default **stages A–F**; run **`generate.py --phase model-in-layers`** when needed. See **`process.md`** appendix.

---

## Continual refinement (this step)

- **Delta:** **ubiquitous language** — rename weak terms (**Processor** → **PaymentOrchestrator**, **PspConnector**, **Payer**, …); keep **events** and **UI** aligned; no duplicate **`**newly added**`** unless a rename introduces a **new** concept line.

---

## Action Checklist

- [ ] Have you replaced all generic or weak names (Manager, Handler, Processor) with specific domain terms?
- [ ] Are all names aligned with the language used in the source material (spec, interviews, wiki)?
- [ ] Have you updated the class diagram to reflect every rename?
- [ ] Have you updated `term-registry.md` with `Renamed` notes for each rename and `Promoted` notes where targets changed?
- [ ] Have you verified that events, UI labels, and API names use the same spelling?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
