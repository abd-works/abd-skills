# Model state transitions — payments example

**Skill:** abd-ooad — **Step 14:** illegal transitions are **unrepresentable** or **rejected**.

**Upstream:** `invariants-in-the-model.md`, `prefer-composition.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Payment — states (from spec + consolidation)

`INITIATED` → `METHOD_SELECTED` → `PENDING_REDIRECT` (optional) → `AUTHORIZED` → `CAPTURED` / `PARTIALLY_CAPTURED` → `SETTLED`  
Branches: `FAILED` (terminal), `CANCELLED` (if allowed).

**Refund** (separate aggregate or child): `REQUESTED` → `COMPLETED` / `FAILED`.

---

## Illegal (reject in operation)

| From | To | Why illegal |
|------|-----|-------------|
| `SETTLED` | `AUTHORIZED` | Time doesn’t run backward. |
| `FAILED` | anything except new attempt | New attempt = **new** Payment or new **idempotency** scope. |
| `INITIATED` | `SETTLED` | Skip rails. |

---

## Events vs state

- **`payment.settled`** emitted **on** transition to `SETTLED` — **Warehouse** / digital fulfillment subscribe.
- **Webhook** handlers map external status → **command** on aggregate — **not** direct field set from HTTP.

---

## Carry forward → Step 15

**Re-read** spec for missed contradictions (TTL, MoR, digital vs physical).

---

## Continual refinement (this step)

- **Delta:** **PaymentState** / **RefundState** transition sets and **illegal** edges — attach **`Invariant:`** under **`state`** or under **operation** lines that guard transitions; **`**newly added**`** when first stating each guard in formal form.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
