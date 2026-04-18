# Scenario validation

**Skill:** abd-ooad — **Phase-id:** `scenario-validation` (Stage 4 — Behaviour, p11).

**Upstream:** `state-and-lifecycle` (p10) — lifecycle defined; invariants attached; domain events named.

**What this phase does:** Walk real scenarios through the model. Each scenario step must map to a class responsibility. If it does not, the model has a gap. This phase is the verification gate — it does not add new design, it exposes what is missing.

---

## How to walk a scenario

Pick a scenario (happy path first, then edge cases). For each step:

1. **Identify which class receives the call** — which operation handles this step?
2. **Check the guard** — does the operation have the invariant to handle the input?
3. **Check the state** — is the entity in the right state for this transition?
4. **Check the output** — does the operation return or emit what the next step needs?
5. **If any check fails** → record a `Scenario Gap` note; fix the model before continuing

---

## Scenario coverage

Walk at minimum:

- One happy-path scenario end-to-end
- One failure scenario (rejection, guard triggered, illegal transition)
- One idempotency or replay scenario (if the domain has retry behaviour)
- One cross-BC scenario (cross-boundary event subscription or contract)

Each scenario step must have a named class and operation. Steps that float without an owner are model gaps.

---

## What gaps mean

A gap always means one of:
- A missing operation on an existing class
- A missing class entirely
- A responsibility assigned to the wrong class
- An invariant that was not defined in p9

Fix the gap in the model immediately — update `domain-model.md` and `term-registry.md`. Do not accumulate gaps; the model is wrong until they are resolved.

---

## term-registry.md

Tag all model notes with `[p11]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Scenario Gap - {{scenario}} exposes: {{missing_responsibility_or_operation}}` — a step had no matching class responsibility
- `Invariant - {{rule_that_must_always_hold}}` — new invariant surfaced by walking an edge case
- `Follow-up - {{question_or_action}}` — gap deferred; awaiting product decision or out-of-scope

---

## Action Checklist

- [ ] At least one happy-path scenario walked end-to-end.
- [ ] At least one failure / edge-case scenario walked.
- [ ] Every scenario step mapped to a class and operation.
- [ ] Every unmapped step recorded as `Scenario Gap` in `term-registry.md`.
- [ ] All gaps fixed in `domain-model.md` immediately (or explicitly deferred with `Follow-up`).
- [ ] New invariants surfaced by edge cases attached to the model.

---

## Prompt

> Walk each scenario step by step. At each step, name the class and the operation. If you cannot name both, the model has a gap. Fix it before moving on. Do not finish scenario validation with unresolved gaps — either resolve them in the model or record them explicitly as deferred with a reason.
