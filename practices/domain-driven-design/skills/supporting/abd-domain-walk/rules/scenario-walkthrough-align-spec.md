---
rule_id: scenario-walkthrough-align-spec
---

**See also:** [`content/parts/library/walkthrough-semantic-alignment.md`](../content/parts/library/walkthrough-semantic-alignment.md) (index vs narrative, optional scanners).

## Scenario walkthrough: names align with `map-model-spec`

**When** you document a scenario walkthrough (prose or sidecar), **concept and module names** used in object-flow text **must match** **`concept.name`** and **`module.name`** in **`map-model-spec.json`** for the integrated slice — no shadow synonyms unless Integrate has recorded a merge.

**DO**

- Use the same spelling as in the spec for every named concept in the walk.

**DON'T**

- Introduce alternate labels for the same concept without a synonym row in the candidate queue or spec.
