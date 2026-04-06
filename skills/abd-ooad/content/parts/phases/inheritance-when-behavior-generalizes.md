# Inheritance when behavior generalizes — payments example

**Skill:** abd-ooad — **Step 11:** subtype only when **substitutable** behavior differs.

**Upstream:** `turn-verbs-into-operations.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Candidate hierarchy

**PaymentMethod** (abstract or interface) — **authorize**, **capture**, **supportsPartialCapture** — **if** each rail implements differently **and** callers use polymorphism.

| Subtype | Justified when |
|---------|------------------|
| **CardMethod** | 3DS, network tokens — extra **redirect** flow. |
| **BankTransferMethod** | Different settlement timing; no “capture” in card sense. |
| **WalletMethod** | Balance vs card rails. |

**Avoid** subclass explosion for **every** PSP brand if behavior is **adapter**-level (Stripe vs Adyen) — that’s **composition** (connector), not inheritance from **PaymentMethod**.

---

## Rule of thumb (payments)

- **Inherit** from **PaymentMethod** when **domain** distinguishes **how** the customer pays (card vs bank vs wallet).
- **Compose** **PspConnector** when **infrastructure** differs (same card semantics, different API).

---

## Carry forward → Step 12

Formalize **abstract class vs interface** for **PaymentMethod** and **ports** for PSP.

---

## Continual refinement (this step)

- **Delta:** **PaymentMethod** family (**CardMethod**, **BankTransferMethod**, **WalletMethod**) as substitutable subtypes — add subtype concept headings per [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (`### **Subtype** : **PaymentMethod**`) with **`**newly added**`** on subtype **operation** lines when first introduced.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
