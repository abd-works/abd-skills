# Watch for bloated classes — payments example

**Skill:** abd-ooad — **Step 9:** danger signals for **Payment** growing into a god object.

**Upstream:** `invariants-in-the-model.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Signs to monitor on `Payment`

| Signal | In this domain |
|--------|----------------|
| Unrelated property clusters | Mixing **redirect URLs**, **dispute scores**, **marketing campaign ids** with core money state. |
| Methods touching different clusters | `calculateTax()`, `reserveInventory()`, `emailReceipt()` on **Payment**. |
| Many `if (methodKind == …)` | Long-term: **strategy** per rail (Step 12–13); short-term acceptable with debt noted. |
| Name smell | **`PaymentProcessor`**, **`PaymentManager`** — likely hiding services. |

---

## Splits if bloat appears

| Extract | Responsibility |
|---------|----------------|
| **PricingQuoteService** (app) | FX display, fee quotes — **inputs** to Payment, not fields forever. |
| **RedirectSession** VO + adapter | 3DS / bank login — keep **Payment** to `awaitingRedirect` + correlation id. |
| **RefundPolicy** | Eligibility windows, reason-code matrix. |
| **SettlementNotifier** | Emitting events — or stay **domain events** from Payment if thin. |

**Payment** should stay: **one payment attempt’s truth**, rail outcomes, settlement emission.

---

## Carry forward → Step 10

Ask whether **“user”** / **payer** / **admin** are one abstraction or **smashed roles**.

---

## Continual refinement (this step)

- **Delta:** **signals and extract paths** (pricing, redirect, refund policy, notifier) — mostly narrative; new **types** introduced here get **`**newly added**`** on their first **property** / **operation** lines when promoted.

---

## Action Checklist

- [ ] Have you identified any class with more than two distinct responsibilities?
- [ ] Have you identified any class that contains both state management and policy enforcement?
- [ ] Have you proposed concrete extractions (new types) for each bloat signal found?
- [ ] Have you logged any deferral as explicit design debt with a rationale?
- [ ] Have you noted carry-forward items to Step 10 (smashed abstractions)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
