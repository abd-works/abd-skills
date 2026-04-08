# Prefer composition — illustrative thread

**Phase ID:** `prefer-composition`

**Skill:** abd-ooad — **Stage D** — **has-a** over **is-a** for variability. *(Example uses a payment aggregate; substitute your domain.)*

**Upstream:** `abstract-classes-and-interfaces.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Composed parts (payments)

| Part | Role |
|------|------|
| **Payment** aggregate | Lifecycle, invariants, domain events. |
| **PaymentMethod** (ref or VO) | What customer chose — **immutable** snapshot after confirm. |
| **FeeBreakdown** VO | Snapshot at quote time. |
| **PspConnector** (injected port) | **Does not** live inside aggregate as concrete class — **application** calls port after loading aggregate. |
| **ComplianceGate** | Pre-check — **composed** into use case, not inherited. |
| **IdempotencyStore** | Port — **composed** into initiate flow. |

---

## Why not inherit “StripePayment”

- **PSP** swaps per **merchant config** or **routing** — **strategy object** or **factory**, not subclass of Payment.

---

## Carry forward → `model-state-transitions`

Model **state transitions** explicitly on the aggregate (e.g. **Payment** / **Refund** in this example).

---

## Continual refinement (this step)

- **Delta:** **composed parts** table — **ComplianceGate**, **IdempotencyStore**, **PspConnector** as **collaborators** on use cases / **Interactions**, not fields on **Payment**; **`**newly added**`** when those collaboration edges first appear on a concept.

---

## Action Checklist

- [ ] Have you identified any place where inheritance was used for code reuse rather than behavioral substitution?
- [ ] Have you replaced those cases with composition (strategy, collaborator, or dependency injection)?
- [ ] Are all composed parts documented as collaborators on the relevant use cases / interactions in the spec?
- [ ] Have you updated the class diagram to reflect composition relationships?
- [ ] Have you noted carry-forward items to Step 14 (state transitions)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
