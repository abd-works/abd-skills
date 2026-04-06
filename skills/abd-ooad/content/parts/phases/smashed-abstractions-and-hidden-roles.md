# Smashed abstractions and hidden roles — payments example

**Skill:** abd-ooad — **Step 10:** one noun, several **real** roles.

**Upstream:** `garbled-payments-spec.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## “User” in payments prose

| Mention | Actual role |
|---------|-------------|
| Buyer / payer | Pays; subject to sanctions, 3DS. |
| Merchant | Receives funds; MoR question for disputes. |
| Admin | Region checkbox, product matrix, crypto pilot. |
| Support | Failure → message + log category. |
| “Platform” vs “Risk” | **Owns dispute** — org conflict, not one **User** subtype. |

**Single `User` class** would blur **permissions**, **money flow**, and **config**.

---

## Outcomes (payments)

- **Identity**: **Account** / **PartyId** in IAM BC — **not** modeled fully here.
- **This BC**: **`payerRef`**, **`merchantRef`**, **`actor`** on audit (`user` vs `system` vs `psp_webhook`) — **references + audit**, not rich user graphs.
- **Admin actions** → **configuration** rows or **admin audit** with actor id — optional **AdminAction** log, not `Admin` entity inside payments core.

---

## Carry forward → Step 11

Use **inheritance** only if **PaymentMethod** subtypes share substitutable **authorize/capture** behavior (see next file).

---

## Continual refinement (this step)

- **Delta:** **role separation** — **`payerRef`**, **`merchantRef`**, **`actor`** on audit vs monolithic **User**; refine **Interactions** and collaborator lists when serializing to the spec.

---

## Action Checklist

- [ ] Have you identified any class that serves multiple distinct roles in different contexts?
- [ ] Have you separated smashed abstractions into explicit roles with their own names and responsibilities?
- [ ] Have you checked for hidden roles disguised as generic names (User, Actor, Person)?
- [ ] Have you updated the spec with `payerRef`, `merchantRef`, or equivalent references in place of rich user graphs?
- [ ] Have you noted carry-forward items to Step 11 (inheritance)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
