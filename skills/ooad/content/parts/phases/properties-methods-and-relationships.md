# Properties, methods and relationships

**Skill:** abd-ooad — **Phase-id:** `properties-methods-and-relationships` (Stage 2 — Model, p5).

**Upstream:** `responsibilities-and-collaborators` (p4) — each class has a responsibility sentence, exclusions, and named collaborators; English only.

**What this phase does:** Convert responsibility statements into first-class model members in one ordered pass: **properties first, then operations that exercise them, then relationships and cardinality between classes.** These three sub-steps happen in sequence within the same phase — they inform each other and must not be done in isolation.

---

## Pass 1 — Properties

Every property answers: *What must this object know to fulfil its responsibility?*

Rules:
- Name properties contextually (`authorizedMoney` not `amount` when partial capture matters)
- If a property recurs across many operations, it is likely a value object — extract it
- Remove anything that is UI, infrastructure, or application-layer concern
- No types yet if the domain type is still uncertain — write the English description, type comes when clear

For each class: update `domain-model.md` with properties. Add a `Classified - Property` note to `term-registry.md` for each property introduced. Tag notes `[p5]`.

---

## Pass 2 — Operations

Every operation answers: *What must this object do, and who calls it?*

Rules:
- Map verbs from `nouns-verbs-rules-and-states` (p1) and `responsibilities-and-collaborators` (p4) to owning classes
- Challenge each verb: does it belong on a domain object or an application service?
- Application-layer verbs (orchestrate, call HTTP, render) must be moved out now
- Each surviving operation appears as a method signature on the class: `methodName(param: Type): ReturnType`

For each operation: update `domain-model.md`. Add a `Classified - Operation` note to `term-registry.md`. Tag notes `[p5]`.

---

## Pass 3 — Relationships and cardinality

Every relationship answers: *How do these objects refer to each other, and who owns whom?*

Rules:
- Decide composition vs association: if the child only exists inside the parent, it is composition; if it has independent identity, it is association
- Cardinality: record `1..1`, `1..*`, `0..*` for each end
- Cross-BC references (e.g. `OrderId`, `PayerId`) are references, not embedded aggregates — confirm this explicitly
- Use ASCII notation from `class-diagrams` in the library: `----|>`, `..|>`, `*---`, `o---`, `- - ->`

For each relationship: update `domain-model.md`. Add a `Classified` note to `term-registry.md` confirming relationship type. Tag notes `[p5]`.

---

## term-registry.md

Tag all model notes with `[p5]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Classified - Property {{reason}}` — noun resolves to a property on a class
- `Classified - Operation {{reason}}` — verb confirmed as a domain operation
- `Classified - Composition {{reason}}` — child lives inside parent; lifecycle bound
- `Classified - Association {{reason}}` — independent identity; cross-reference
- `Promoted - Property → Class {{reason}}` — property promoted to its own class (e.g. `Money` extracted from raw `amount`)
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — ownership unclear; competing boundaries
- `Follow-up - {{question_or_action}}` — deferred to `inherit-interface-or-compose` (p6)

**Any new VO, aggregate, or operation introduced in this phase gets a term row or row update.**

---

## Action Checklist

- [ ] Every class has typed properties derived from its p4 responsibility statement.
- [ ] Every property is semantically tight — the object needs it to fulfil its responsibility.
- [ ] UI, infrastructure, and application-layer properties removed.
- [ ] Every domain verb from p1 and p4 is mapped to an owning class or application service.
- [ ] Application-layer verbs moved out — not on domain objects.
- [ ] Every surviving operation is a formal method signature on the class.
- [ ] Every class pair that interacts has an explicit relationship type and cardinality.
- [ ] Cross-BC references confirmed as references, not embedded aggregates.
- [ ] `term-registry.md` updated with `Classified`, `Promoted`, and `Tension` notes.

---

## Prompt

> Work in order: properties, then operations, then relationships. Do not skip to operations before properties are solid — operations depend on knowing what the object holds. When ownership of an operation or relationship is unclear, name the tension and resolve it before moving on.
