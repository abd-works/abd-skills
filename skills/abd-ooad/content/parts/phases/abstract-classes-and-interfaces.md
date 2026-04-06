# Abstract classes and interfaces — payments example

**Skill:** abd-ooad — **Step 12:** **state + shared impl** vs **pure contract**.

**Upstream:** `inheritance-when-behavior-generalizes.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Suggested split

| Construct | Use in payments |
|-----------|-----------------|
| **`interface PspConnector`** | `authorize`, `capture`, `refund`, `parseWebhook` — **implementations** per PSP; **mock** in tests. |
| **`interface PaymentMethod`** (or abstract base) | Domain-facing **selection** + **capabilities**; optional **default** helpers in abstract class if shared. |
| **`abstract class Payment`** | Rare — prefer **one** aggregate **Payment** with **state machine**; avoid subclass per status (**use state enum**, not `AuthorizedPayment extends Payment`). |

---

## Anti-pattern here

- **`class StripePayment extends Payment`** — **no**; **Payment** is one type; **Stripe** is **connector**.

---

## Carry forward → Step 13

**Prefer composition:** **Payment** holds **PaymentMethod** ref + **PspConnector** injected at application layer.

---

## Continual refinement (this step)

- **Delta:** **`interface PspConnector`**, **`PaymentMethod`** contract vs **abstract** base — port **operations** (**authorize**, **capture**, **refund**, **parseWebhook**) **`**newly added**`** on the interface concept when first captured in **`map-model-spec.json`**.

---

## Action Checklist

- [ ] Have you identified every place where a port / plug-point is needed for external or swappable infrastructure?
- [ ] Is each port defined as an interface (not an abstract class) when it has no shared implementation?
- [ ] Have you defined all abstract base classes with shared domain behaviour and at least one abstract operation?
- [ ] Have you verified that no concrete domain class directly depends on infrastructure types?
- [ ] Have you noted carry-forward items to Step 13 (prefer composition)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
