# Invariants in the model — payments example

**Skill:** abd-ooad — **Step 8:** rules live where they can be **enforced**, not only in docs/UI.

**Upstream:** `garbled-payments-spec.md`, `relationships-and-cardinality.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## From spec → enforced behavior

| Rule (text) | Enforce on |
|-------------|------------|
| No double-charge for same idempotency intent | **`Payment.initiate`** — return existing aggregate or reject duplicate **successful** outcome. |
| Sanctioned country: block **before** method selection | **`ComplianceGate`** + **`Payment`** refuses `recordMethodSelection` if payer blocked (or earlier gate). |
| Partial capture only if rail supports | **`Payment.capture`** checks **connector capability** (policy/config). |
| Refund reason codes required | **`Refund.request`** — rejects missing **ReasonCode** when policy says required. |
| `payment.settled` before warehouse pick (physical) | **Event ordering** — **`Payment.settle`** emits event; fulfillment BC subscribes — invariant is **cross-BC** contract test, not one method on Payment. |
| Append-only audit | **`AuditEntry`** immutable; no `update`. |

---

## Example guard clauses (conceptual)

- `capture(amount)` — `amount ≤ authorizedRemainder`; state in `{AUTHORIZED, PARTIALLY_CAPTURED}`; rail allows partial.
- `settle()` — state allows settlement; fraud/compliance flags satisfied (if modeled).
- `requestRefund(amount)` — `sum(prior refunds) + amount ≤ captured`.

---

## Conflicts in spec (explicit debt)

- **Idempotency TTL 24h vs 72h** — invariant uses **configured** TTL until product decides.
- **Digital vs physical emit timing** — **not** solvable inside Payment alone; **policy flag** or **event choreography** document.

---

## Carry forward → Step 9

Watch **Payment** for bloat as more rules arrive — split policies if needed.

---

## Continual refinement (this step)

- **Delta:** **invariants** tied to **`Payment.initiate`**, **`capture`**, **`settle`**, **`Refund.request`**, append-only **AuditEntry** — add **`Invariant:`** lines under the matching **property** / **operation** in the spec (see [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md)); mark **`**newly added**`** when first attaching each invariant to a member line.

---

## Action Checklist

- [ ] Have you identified at least one invariant per major aggregate?
- [ ] Is each invariant expressed as a condition that must always be true, not a procedure?
- [ ] Are all invariants attached to the relevant `property` or `operation` line in the spec?
- [ ] Have you documented open decisions (e.g. configurable TTLs) where invariants are not yet fully defined?
- [ ] Have you noted carry-forward items to Step 9 (watch for bloat)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
