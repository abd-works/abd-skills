# Model state transitions — payments example

**Skill:** abd-ooad — **Step 14:** illegal transitions are **unrepresentable** or **rejected**.

**Upstream:** `invariants-in-the-model.md`, `prefer-composition.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

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

## Action Checklist

- [ ] Have you defined all valid lifecycle states for every stateful entity?
- [ ] Have you documented every allowed transition and every illegal transition?
- [ ] Is each transition guarded by an `Invariant:` line attached to the relevant operation?
- [ ] Have you verified that domain events are emitted on all significant state transitions?
- [ ] Have you updated the class diagram to reflect state and guard information?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
