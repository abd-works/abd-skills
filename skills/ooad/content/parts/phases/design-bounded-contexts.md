# Design bounded contexts

**Skill:** abd-ooad — **Phase-id:** `design-bounded-contexts` (Stage 3 — DDD patterns, p8).

**Upstream:** `classify-stereotypes` (p7) — every class has a stereotype and aggregate candidates are flagged.

**What this phase does:** Name and align **bounded contexts** (DDD strategic design): linguistic boundaries where a single ubiquitous language holds, and where models may diverge legitimately across seams. Within each context, confirm **aggregate** boundaries by asking what must change **atomically** under one business operation. This is the final structural decision before behaviour rules (`invariants` onward). The answer determines which classes sit inside an aggregate, which reference a root by ID only, and where context boundaries (and integration seams) sit.

---

## Bounded context first

For each major area of the domain:

1. **Name the context** — one short phrase (e.g. *Billing*, *Inventory*, *Campaign authoring*).
2. **List what must stay linguistically consistent** inside it — shared terms that must not mean different things.
3. **Mark seams** — where another context consumes this model (events, queries, anti-corruption layer). Do not merge distinct contexts for implementation convenience.

---

## Aggregates inside a context

For each aggregate candidate from p7:

1. **Name a realistic operation** on the aggregate root (e.g. `Payment.capture`, `Order.submit`).
2. **Walk the object graph** — which child entities and VOs must be updated in the **same** transaction?
3. **Confirm the boundary** — everything inside belongs to one aggregate; everything outside references the root by ID.
4. **Check for bloat signals**: if more than 5–7 objects change together routinely, the boundary is probably too wide.

Objects that must stay consistent together belong in the same aggregate. Objects whose consistency is eventual (cross-context, separate transactions) belong outside.

---

## Bloat signal

If an aggregate boundary spans objects that change in different business contexts, it is too wide. Signs:

- Many classes change together but for *different reasons*
- Two distinct domain concepts share a root for convenience
- The aggregate grows with every new feature

When you see this, name the `Tension` and split the boundary — do not merge for transaction convenience.

---

## Cohesion and module boundaries

Classes that always change together belong in the same module **within** a bounded context. Classes that change for different reasons may belong in separate contexts or separate aggregates. Update `domain-model.md` module groupings if this analysis reveals a better boundary.

---

## term-registry.md

Tag all model notes with `[p8]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Cohesion Group - {{group_name}} changes with: {{related_classes}}` — confirmed aggregate or co-change cluster
- `Bounded Context - {{context_name}}` — named context; lists core terms and seams
- `Classified - Aggregate Root {{reason}}` — root confirmed; boundary defined
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — boundary too wide; competing groupings; bloat signal
- `Follow-up - {{question_or_action}}` — deferred to architecture (e.g. cross-context contract testing)

---

## Action Checklist

- [ ] Every major area has a **bounded context** name and a clear seam where another context integrates.
- [ ] Every Aggregate candidate has a confirmed boundary with named members.
- [ ] Every class inside an aggregate boundary is there for the same business operation.
- [ ] Every cross-aggregate reference is by root ID only — no embedded child from another aggregate.
- [ ] Module groupings in `domain-model.md` updated if cohesion analysis revealed better boundaries.
- [ ] Bloat signals named as `Tension` notes with a split recommendation.
- [ ] `term-registry.md` updated with `Cohesion Group`, `Bounded Context`, and `Classified - Aggregate Root` notes as applicable.

---

## Prompt

> For each bounded context, walk aggregate candidates through a real operation. List what changes atomically. If everything on the list belongs to one business reason, the aggregate holds. If not, split it. Name context seams explicitly — ambiguity there becomes integration debt later.
