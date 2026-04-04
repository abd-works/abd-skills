Battle-test for **abd-ooad**:

- Input: **`examples/garbled-payments-spec.md`**
- Step-style outputs are named after the step (not “step 1” …). Full sequence under **`examples/`**:

1. `nouns-verbs-rules-and-states.md`
2. `raw-candidate-list.md`
3. `thing-vs-data-about-a-thing.md`
4. `responsibilities-before-operations.md`
5. `add-properties-semantically-tight.md`
6. `turn-verbs-into-operations.md`
7. `relationships-and-cardinality.md`
8. `invariants-in-the-model.md`
9. `watch-for-bloated-classes.md`
10. `smashed-abstractions-and-hidden-roles.md`
11. `inheritance-when-behavior-generalizes.md`
12. `abstract-classes-and-interfaces.md`
13. `prefer-composition.md`
14. `model-state-transitions.md`
15. `iterative-refinement.md`
16. `tension-as-a-signal.md`
17. `what-changes-together.md`
18. `validate-with-scenarios.md`
19. `refine-names.md`
20. `model-in-layers.md`

See **`SKILL.md`** (end) for the same table with **`examples/`** prefixes.

**Continual refinement:** Each step file (except the raw **`garbled-payments-spec.md`**) links to **abd-maps-models-specs** [`domain-model.md`](../abd-maps-models-specs/content/parts/library/domain-model.md) and ends with **`## Continual refinement (this step)`** — formal **property** / **operation** lines from Step 5 onward, with **`**newly added**`** on deltas first introduced in that file.

**Prompt:** Each step file also ends with **`## Prompt`** — **validate and fix when you find problems** (e.g. bloat, weak boundaries, missing invariants); do not advance on a broken model without fixing or recording debt.
