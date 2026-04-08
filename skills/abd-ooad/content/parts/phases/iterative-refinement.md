# Iterative refinement — payments example

**Skill:** abd-ooad — **Step 15:** second pass on **garbled** spec.

**Upstream:** all prior step files + `garbled-payments-spec.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Action Checklist

- [ ] Have you re-read the source material against the current model from the beginning?
- [ ] Have you resolved contradictions between the spec and the model?
- [ ] Have you updated class names, responsibilities, or relationships found to be inaccurate?
- [ ] Have you logged any open questions or unresolvable contradictions as explicit design debt with a clear follow-up?
- [ ] Have you updated the term registry with any name or classification changes?
- [ ] Have you updated the class diagram to reflect all refinements from this pass?

---

## Re-read checklist (payments)

| Question | Action |
|----------|--------|
| Idempotency 24h vs 72h? | Flag **config** parameter; document **open decision**. |
| MoR for disputes? | **Out of core Payment** — **MerchantAccount** BC or note. |
| Partial capture “if rail supports” | **Connector capability** + **Payment.capture** guard. |
| Crypto pilot | **Feature flag** or **PaymentMethod** subtype — don’t pollute core until stable. |
| B2B “invoice” | New **use case** or **PaymentKind** — revisit **Step 2** nouns if added late. |

---

## Model updates from refinement

- Add **`FailureKind`** enum if support taxonomy stabilizes.
- Split **redirect** concerns if **3DS** and **bank login** diverge further.

---

## Carry forward → Step 16

Treat **tensions** (org conflict, timing conflict) as **signals** for boundaries or options.

---

## Continual refinement (this step)

- **Delta:** second pass — **`FailureKind`**, redirect split, config knobs; add **`**newly added**`** only on **new** properties/operations/invariants introduced during this pass.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
