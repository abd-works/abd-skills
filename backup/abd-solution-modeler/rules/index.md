# Rules by AI Phase

Rules declare their phase in frontmatter (`phases: [synthesis]`) or via filename (`phase-topic`). Cross-phase rules have no phase prefix and are included in all phases.

| Phase | Rule prefix | # Rules | Notes |
| ----- | ----------- | ------- | ----- |
| synthesis | synthesis-* | ~10 | Hierarchy, speculation, subtypes, property types, model instances |
| structure | structure-* | ~9 | Single source of truth, composition, caller-receiver, interaction patterns, inheritance |
| behavior | behavior-* | ~8 | Atomic operations, traverse-from-root, thin orchestration, steps |
| variation | variation-* | ~8 | Shared behavior base, invariants, decompose variants, inheritance |
| consolidate | consolidate-* | ~13 | Integrate concepts, concept roles, anemia critique, examples, scaffold |
| assess, finalize | consolidate | Same as consolidate | Use consolidate rules |

## Cross-phase rules

(No phase prefix; included in all phases that have rules.)

- derive-from-source
- domain-mechanics-not-toc
- domain-subtypes-vs-enum
- outcome-oriented-language
- story-granularity
- story-small-and-testable
- verb-noun-format

## Code phases (no rules)

`configure_concept_extraction_parameters` — calibration; no rules (prompt describes calibration).

`normalize`, `concept_index`, `evidence_extraction`, `evidence_index` — code phases; no rule loading.
