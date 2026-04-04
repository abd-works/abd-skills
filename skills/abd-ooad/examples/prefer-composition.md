# Prefer composition — payments example

**Skill:** abd-ooad — **Step 13:** **has-a** over **is-a** for variability.

**Upstream:** `abstract-classes-and-interfaces.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

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

## Carry forward → Step 14

Model **state transitions** explicitly on **Payment** (and **Refund**).

---

## Continual refinement (this step)

- **Delta:** **composed parts** table — **ComplianceGate**, **IdempotencyStore**, **PspConnector** as **collaborators** on use cases / **Interactions**, not fields on **Payment**; **`**newly added**`** when those collaboration edges first appear on a concept.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
