---
rule_id: concept-layering-scaffold
phases: [step1]
order: 12
impact: HIGH
---

## Concept layering at scaffold (base → categories → implementations)

At **[Modules and Epics](../parts/process.md)** (scaffold breadth), structure concepts so readers can navigate **general → specific** without mixing levels in one undifferentiated list.

**Layering model**

1. **Base / root** — The umbrella concept for the area (often one per module or sub-area).
2. **Categories / subtypes** — Named partitions or roles under the base (enums, subtypes, or clearly named siblings).
3. **Implementations / specifics** — Concrete variants, policies, or mechanisms that **depend on** the categories.

**Naming**

- Prefer **`SubtypeName : BaseName`** (or equivalent convention already used in this spec) when a concept is a specialization of another — see `classify-variants-before-modeling.md` for variant vs duplicate.

**DO**

- Reflect layering in `concept` names and in **`module.depends_on`** where one module’s concepts presuppose another’s base types (see `module-depends-on.md`).
- Keep **Modules and Epics** scaffold breadth in check: defer exhaustive enumeration of every implementation to **[Concept Classes and Stories](../parts/process.md)** (deepen) unless chunks already force them.

**DON'T**

- Flatten all domain nouns into a single bucket without parent/variant structure when the source distinguishes them.
- Add implementation-level concepts with no path to a base or category — park in `open_questions` or mark `evidence_stage: hypothesis` until the **K** reads or **Concept Classes and Stories** ground them.
