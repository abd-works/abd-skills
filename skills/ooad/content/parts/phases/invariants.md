# Invariants

**Skill:** abd-ooad — **Phase-id:** `invariants` (Stage 4 — Behaviour, p9).

**Upstream:** `design-bounded-contexts` (p8) — bounded contexts and aggregate boundaries are confirmed; every class has a stereotype, properties, operations, and relationships.

**What this phase does:** Identify and attach the rules that must always be true within an aggregate. An invariant is a condition the aggregate enforces — not a procedure, not a validation checklist. If the invariant is violated, the operation is rejected.

---

## What is an invariant

An invariant is a **domain constraint that must always hold inside the aggregate boundary**.

- It is enforced by a guard clause on an operation
- It cannot be delegated to a service or caller — the aggregate itself ensures it
- It is expressed as a condition, not a procedure: "sum(refunds) ≤ captured" not "check refund amount before saving"

---

## How to identify invariants

For each aggregate:

1. **Read the spec** — look for rules that use language like "must", "cannot", "only if", "never", "always"
2. **Walk operations** — for each operation, ask: what must be true *before* this runs? What must be true *after*?
3. **Check state transitions** — what transitions are illegal? The guard enforcing that is an invariant
4. **Look for cross-object rules** — if a rule spans two classes in the same aggregate, it lives on the root

---

## Attaching invariants to the model

For each invariant:

- Write it as an `Invariant:` annotation on the relevant property or operation in `domain-model.md`
- Example: `Invariant: amount ≤ authorizedRemainder`
- Example: `Invariant: state in {AUTHORIZED, PARTIALLY_CAPTURED} before capture`
- Cross-BC invariants (e.g., "settled before pick") are cross-boundary contracts — record as `Follow-up` for integration test scope

---

## term-registry.md

Tag all model notes with `[p9]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Invariant - {{rule_that_must_always_hold}}` — the enforced condition and which operation or property carries it
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — configurable rules, cross-BC constraints, spec conflicts on rule boundaries
- `Follow-up - {{question_or_action}}` — invariant deferred; awaiting product or architecture decision

---

## Action Checklist

- [ ] At least one invariant identified per aggregate.
- [ ] Every invariant is expressed as a condition, not a procedure.
- [ ] Every invariant is attached to the specific operation or property it guards in `domain-model.md`.
- [ ] Cross-BC invariants recorded as `Follow-up` with integration test scope.
- [ ] Spec conflicts on rule boundaries recorded as `Tension` notes.
- [ ] `term-registry.md` updated with `Invariant`, `Tension`, and `Follow-up` notes.

---

## Prompt

> For each aggregate, read the spec and walk the operations. Find the conditions that must always hold. Express them as conditions — not procedures. Attach them to the model. If a rule crosses a BC boundary, record it and flag it for integration testing.
