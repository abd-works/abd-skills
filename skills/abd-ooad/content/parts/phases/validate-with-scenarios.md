# Validate with scenarios — payments example

**Skill:** abd-ooad — **Step 18:** walk instances; find **gaps** and **absurdities**.

**Upstream:** `model-state-transitions.md`, `what-changes-together.md`.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Scenarios (abbrev)

1. **Happy path card** — Initiate → select card → authorize → capture → settle → event emitted; audit trail length ≥ N.
2. **Sanctioned payer** — Browse OK; **before** method selection → **blocked**; no charge; **FailureKind** / compliance reason.
3. **Idempotency replay** — Same key within TTL → **same** Payment id and outcome; after TTL → **reject** or **new** per policy.
4. **Partial capture** — Rail allows → second capture; sum ≤ authorized; **Refund** capped at captured.
5. **Partial capture disallowed** — Second capture **rejected** with clear invariant.
6. **Webhook arrives late** — **Idempotent** application to aggregate; no double settle.
7. **Physical goods** — **No** pick until **settled** (cross-BC assertion or integration test).
8. **Refund after partial capture** — Refund ≤ captured; multiple refunds sum correctly.

---

## Gaps to fix in model or backlog

- **Dispute** lifecycle — only **referenced**; full model **out of scope** here.
- **Crypto** — stub **PaymentMethod** or flag until requirements firm.

---

## Carry forward → Step 19

**Refine names** for lingering **Processor**/ambiguous terms.

---

## Continual refinement (this step)

- **Delta:** scenario walk — gaps (**Dispute**, **crypto**) become backlog or **`**newly added**`** members when you add them to the formal model.

---

## Action Checklist

- [ ] Have you walked at least one happy-path scenario end-to-end through the model?
- [ ] Have you walked at least one failure / edge-case scenario (e.g., sanctions, partial capture, idempotency replay)?
- [ ] Did every scenario step map to at least one class responsibility in the model?
- [ ] Have you logged any gaps or missing responsibilities as explicit debt with a clear follow-up?
- [ ] Have you noted carry-forward items to Step 19 (refine names)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
