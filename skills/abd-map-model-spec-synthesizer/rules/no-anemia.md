---
rule_id: no-anemia
phases: [step6]
order: 20
impact: MEDIUM
---

## Concepts That Own Decisions Must Have Operations

An anemic concept is a data bag — properties only, no behavior. When a concept owns a decision or enforces a rule, it should have operations that enact that behavior.

There is no scanner for this rule. It requires domain judgment — the AI assesses whether each concept's `owns` implies operations that are missing.

**DO** ensure concepts with `owns` have corresponding operations. The concept that "Decides degree of success from d20 + modifier vs DC" should have an operation like `roll() → Degree` or `resolve() → Result`.

**DO NOT** leave concepts as pure data when the domain clearly implies behavior. If the concept owns a decision, it needs an operation to perform it.

- Right: Check has `owns: "Decides degree..."` and `operations: ["roll() → Degree"]`
- Wrong: Check has `owns: "Decides degree..."` but only `properties: [...]` and no operations
