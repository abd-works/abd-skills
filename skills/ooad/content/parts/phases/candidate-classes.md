# Candidate classes

**Skill:** abd-ooad — **Phase-id:** `candidate-classes` (Stage 1 — Scaffold, p2).

**Upstream:** `nouns-verbs-rules-and-states` (p1) — nouns, verbs, rules, and states have been extracted per module into `domain-noun-verb.md` and `term-registry.md`.

**What this phase does:** Group the extracted nouns and verbs into class-like clusters. Each cluster becomes a named stub. No DDD stereotypes yet — no Entity, ValueObject, Policy, Event. Just: what naturally travels together? What talks to what? English only, no types, no syntax.

The goal is a set of named candidates that the CRC pass (p4) can reason about. Clustering too fine is better than clustering too coarse — you can merge later; missing a cluster means missing a class.

---

## What you produce

For each cluster:

- A named stub in `domain-model.md` under the correct anchor module — plain name, no stereotype yet: `ClassName`
- A row in `term-registry.md` with Target set to the stub name and a `Sibling Candidate` or `High Confidence Anchor` note explaining why these terms travel together
- A `Tension` note for any cluster whose boundary is unclear

No separate list file. The model and registry are the single source of truth.

When the project keeps a class diagram for the slice, update it after the markdown matches (**visual twin**).

---

## How to cluster

Work module by module (as identified in the domain scan). For each module:

1. Lay out the nouns from `term-registry.md` for that module
2. Ask: which of these always appear together in the source? Which share the same verbs? Which are meaningless without each other?
3. Group them — one name per group, chosen from the strongest noun in the cluster
4. Verbs that belong exclusively to one cluster become a note on that stub: "owns: authorize, capture, settle"
5. Verbs that cross clusters are cross-cutting — note them in `term-registry.md` as `Tension`

---

## Illustrative shape

Source nouns: Character, HP, AC, bonus, roll, DC, modifier, advantage, disadvantage, player, GM

Clusters:

| Stub name | Terms grouped | Verbs owned |
|-----------|--------------|-------------|
| `Character` | Character, HP, AC | takes damage, heals, levels up |
| `Check` | roll, DC, bonus, modifier, advantage, disadvantage | resolves, succeeds, fails |
| `Actor` | player, GM | controls, narrates |

Each stub → row in `term-registry.md` with grouped terms listed in Notes. Each stub → `ClassName` stub in `domain-model.md`.

---

## term-registry.md

Tag model notes with `[p2]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Sibling Candidate - {{anchor_term}} {{why_related}}` — terms grouped into this cluster
- `High Confidence Anchor - {{why_this_class_is_central}}` — cluster that is clearly a core module class
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — cluster boundary unclear; overlapping terms; competing groupings
- `Follow-up - {{question_or_action}}` — deferred to `thing-vs-data-about-a-thing` (p3)

---

## Action Checklist

- [ ] Every noun from `term-registry.md` for this module appears in exactly one cluster stub.
- [ ] Every cluster has a name and a row in `term-registry.md`.
- [ ] Verbs exclusively owned by one cluster are noted on that stub.
- [ ] Cross-cutting verbs are recorded as `Tension` notes.
- [ ] No stereotypes applied — no Entity, ValueObject, Policy, Event, Process, Role.
- [ ] No typed properties or operations — English descriptions only.
- [ ] `domain-model.md` has a plain `ClassName` stub for each cluster under the correct module.

---

## Prompt

> Work module by module. For each module: lay out the nouns, group what travels together, name each group, note the verbs it owns. No stereotypes, no types — just clusters and names. When a boundary is unclear, name the tension; don't leave terms unplaced.
