# Refine names — illustrative thread

**Phase ID:** `refine-names`

**Skill:** abd-ooad — **Stage F** — **ubiquitous language** alignment. *(Optional payments-themed example below; substitute your domain.)*

**Upstream:** `validate-with-scenarios.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Renames (candidates)

| Weak / vague | Stronger (payments) |
|----------------|---------------------|
| Processor / Handler | **PaymentOrchestrator** (use case), **PspConnector** (port) |
| User | **Payer** / **Merchant** / **Actor** (audit) |
| Status (string soup) | **PaymentState** enum + **RefundState** |
| Data / Info | **FeeBreakdown**, **AuthorizationResult** (VOs) |
| Thing | **Payment**, **Refund**, **AuditEntry** |

---

## Terms from spec to preserve

- **Idempotency key**, **3DS**, **MoR**, **partial capture**, **settlement** — **glossary** in team wiki; model uses **same** spellings in **events** and **UI**.

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
- [ ] Have you updated `term-registry.md` with the new canonical names and removed old entries?
- [ ] Have you verified that events, UI labels, and API names use the same spelling?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
