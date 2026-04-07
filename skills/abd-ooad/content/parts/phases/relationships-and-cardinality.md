# Relationships and cardinality — payments example

**Skill:** abd-ooad — **Step 7:** structure + containment strength.

**Upstream:** `turn-verbs-into-operations.md`, `add-properties-semantically-tight.md`.

Use ASCII glyphs from **`SKILL.md` → ASCII class diagrams — notation** (`----|>`, `..|>`, `*---`, `o---`, `- - ->`).

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Narrative relationships

- **Order** (external BC) **1 — 0..*** **Payment** — retry / multiple attempts possible for same order (idempotency distinguishes “same” vs new attempt).
- **Payment** **1 — 0..*** **Refund** — several partial refunds over time.
- **Payment** **1 — 1..*** **AuditEntry** (or events) — every transition logged (append-only).
- **Merchant** (ref) **1 — *** **Payment** — many payments per merchant (via `merchantRef`).
- **Payer** (ref) **1 — *** **Payment**.

---

## Composition vs association

| End | Strength | Rationale |
|-----|------------|-----------|
| **Payment** *—* **FeeBreakdown** / **Money** snapshots | **Composition** (VO inside aggregate) | No standalone “fee” entity; dies with payment context for that attempt. |
| **Payment** — **Refund** | **Association** (strong ref) | Refund has identity; may be queried independently; lifecycle linked but not embedded value. |
| **Payment** — **Order** | **Association** (id only) | Order lives elsewhere. |

---

## ASCII sketch

```
<<external>>
Order
  1 ------------------ * Payment
                           |
                           | 1
                           *
                        Refund

Payment *-------- AuditEntry    (or events *-------- projection)
  (append-only facts; composition if AuditEntry only exists as child row)
```

**Dependency** (dashed):

```
PaymentOrchestrator - - - -> ComplianceGate
PaymentOrchestrator - - - -> PspAdapter
```

---

## Carry forward → Step 8

Encode **invariants** on **Payment** / **Refund** operations (sanctions, partial capture, settlement before fulfillment consumers).

---

## Continual refinement (this step)

- **Delta:** **associations and cardinality** (**Order** ↔ **Payment**, **Payment** ↔ **Refund**, **Payment** ↔ **AuditEntry**, composition vs association) — document in **Concept relationships** / diagram; **`**newly added**`** on new relationship edges when mirroring to **`map-model-spec.json`**.

---

## Action Checklist

- [ ] Have you defined the relationship type (composition, aggregation, association, dependency) for every pair?
- [ ] Have you recorded cardinality (1..1, 1..*, 0..*) for each relationship?
- [ ] Have you verified that composition correctly models ownership and lifecycle dependency?
- [ ] Have you updated the class diagram with all relationships and cardinalities?
- [ ] Have you noted carry-forward items to Step 8 (invariants)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
