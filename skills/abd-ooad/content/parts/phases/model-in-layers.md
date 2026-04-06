# Model in layers — payments example

**Skill:** abd-ooad — **Step 20:** four layers + **where** payments artifacts sit.

**Upstream:** entire chain from `nouns-verbs-rules-and-states.md` through `refine-names.md`.

See **`SKILL.md` → Model in layers (four layers)** and **ASCII class diagrams**.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Layer map (payments)

| Layer | Contents (this exercise) |
|-------|---------------------------|
| **Domain** | **Payment**, **Refund**, **PaymentMethod** (contract), **Money**, **FeeBreakdown**, **PaymentState**, **FailureKind**, **invariants**, **domain events** (`PaymentSettled`, …). |
| **Application** | **InitiatePayment**, **CapturePayment**, **HandlePspWebhook**, **RequestRefund** — orchestration; **ComplianceGate**, **IdempotencyStore** **ports**. |
| **Infrastructure** | **StripeConnector**, **WebhookParser**, **AuditRepository**, **IdempotencyRedis** — adapters. |
| **Presentation / API** | REST **DTOs**, **redirect URLs**, **not** domain entities. |

---

## ASCII — core domain (compact)

```
<<interface>> PspConnector
        ^
        | ..|>  (implements)
  StripeConnector

Payment ----* Refund
Payment ..> PaymentMethod : uses snapshot
Payment ..> Money : amounts
[Application] InitiatePayment ..> Payment : loads/saves
InitiatePayment ..> PspConnector : calls
```

**Dependency rule:** Domain **does not** reference **Stripe**; **Application** wires **ports**.

---

## Done (battle-test)

You have walked **garbled** payments from **nouns/verbs** through **layers** — ready to compare with **`SKILL.md`** steps 1–20 and to **challenge** any team diagram that skips **invariants** or **boundaries**.

---

## Continual refinement (this step)

- **Delta:** **layer map** + ASCII — domain **concepts** vs **application** use cases vs **infra** adapters; dependency rule (**Domain** does not reference **Stripe**) matches **Integrate** / diagram boundaries. Re-render **`map-model-class-diagram.drawio`** when the promoted spec changes.

---

## Action Checklist

- [ ] Have you produced a layer map (domain / application / infrastructure) for your model?
- [ ] Does every class sit in exactly one layer with a clear rationale?
- [ ] Have you verified the dependency rule — domain classes do not reference infrastructure types?
- [ ] Have you re-rendered `map-model-class-diagram.drawio` to reflect the layered spec?
- [ ] Is the model ready for scenario validation (Step 18)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
