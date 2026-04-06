# Refine names — payments example

**Skill:** abd-ooad — **Step 19:** **ubiquitous language** alignment.

**Upstream:** `validate-with-scenarios.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

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

## Carry forward → Step 20

**Layer** the model — **domain vs application vs infra** + optional **ASCII** summary.

---

## Continual refinement (this step)

- **Delta:** **ubiquitous language** — rename weak terms (**Processor** → **PaymentOrchestrator**, **PspConnector**, **Payer**, …); keep **events** and **UI** aligned; no duplicate **`**newly added**`** unless a rename introduces a **new** concept line.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
