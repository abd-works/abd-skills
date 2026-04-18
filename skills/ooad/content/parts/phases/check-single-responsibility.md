# Check — single responsibility

**Skill:** abd-ooad — **Validator-id:** `check-single-responsibility`.

**When to run:** After `properties-methods-and-relationships` (p5) and after `design-bounded-contexts` (p8). Can also be applied at end of **Stage 2 — Model** or **Stage 3 — DDD patterns** when a class looks suspicious.

**What this validator does:** Ask, for each class: does this class have more than one reason to change? If yes, it is carrying more than one responsibility. Split it.

---

## The test

For each class:

> *If requirement set A changes, does this class change?*
> *If requirement set B (unrelated to A) also changes, does this class change?*

If both answers are yes — the class has two reasons to change and needs to be split.

---

## Common bloat signals

- Unrelated property clusters on the same class (e.g., payment state + pricing logic + notification config)
- Methods that touch different responsibility areas (e.g., `authorizePayment` and `sendReceiptEmail` on the same class)
- Long conditional chains switching on a kind or type field (each branch is probably a separate class)
- Name smells: `*Manager`, `*Processor`, `*Handler`, `*Service` that covers too much ground
- Class grows with every new feature from different domains

---

## Outcome

For each bloat signal found:

- Propose a concrete extraction — name the new class and what moves to it
- Record a `Bloat Signal` note in `term-registry.md`
- Update `domain-model.md` if the split is applied now; record as `Follow-up` if deferred

This validator does not add design — it confirms that existing design is clean.

---

## term-registry.md notes at this validator

- `Bloat Signal - {{what_clusters_are_mixed}} suggest: {{extract}}` — class mixes unrelated responsibility clusters
- `Role Separation - {{merged_role}} splits into: {{role_a}}, {{role_b}}` — class serves multiple distinct roles
- `Follow-up - {{question_or_action}}` — deferred split; design debt explicitly recorded

---

## Checklist

- [ ] Every class checked against the single-reason-to-change test.
- [ ] Bloat signals named and recorded in `term-registry.md`.
- [ ] Concrete extractions proposed for every bloat signal.
- [ ] Applied extractions updated in `domain-model.md`.
- [ ] Deferred extractions recorded as explicit `Follow-up` with reason.
