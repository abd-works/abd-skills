---
rule_id: classify-variants-before-modeling
phases: [step1]
order: 50
impact: HIGH
---

## Classify variant families before modeling them

When you encounter a family of variants in the corpus (types of effects, categories of advantages, kinds of skills), you must classify them before deciding how to represent them. Do not create subtype concepts, subtype sections, or hierarchy entries at Step 1.

There is no scanner for this rule. The classification requires reading chunks to assess mechanics — a scanner cannot determine whether variants have different mechanics or just different labels. This rule is enforced in the adversarial validation pass.

**Test — apply this before naming any variant as a concept:**

- Variants have **different mechanics** (different resolution, different rules, different cost formula, different lifecycle) → subtype candidate → flag `[defer]` with the chunk that shows the variants exist. Do not create the subtypes yet.
- Variants share **the same mechanic** with different labels or data → enum → use `EnumType {val1, val2, ...}` as a property on the parent concept.

**DO** apply this test whenever you see a list of named variants under a parent concept.

**DO NOT** create subtype concepts at Step 1. If a subtype candidate exists, record it as a `[defer]` flag.

**DO NOT** create both an enum and mirroring subtype candidates for the same family. Pick one representation.

- Subtype candidate example: Effect variants (Affliction, Damage, Healing) each have distinct resolution mechanics. Output: `[defer] Effect subtypes — chunk: d4cad3e10e05`. Do not create Affliction, Damage, or Healing as concepts.
- Enum example: Ability score names (Strength, Stamina, Agility...) share identical mechanics — same cost, same modifier formula. Output: `EnumType name {Strength, Stamina, Agility, Dexterity, Fighting, Intellect, Awareness, Presence}` as a property on the Ability concept.
