---
rule_id: map-model-relationships
---

## Map model: resolved `depends_on` and module edges

**Artifact:** `spec/.../maps-models-specs/map-model-spec.json` (path from workspace `output_dir`; see [`domain-model.md`](../content/parts/library/domain-model.md)).

This rule is **machine-checked** by `scripts/scanners/map_model_relationships.py` when the spec file exists.

**Scope (v1):** Reference integrity — every **`depends_on`** target and **`module.depends_on`** concept/module reference names a **concept** or **module** that exists in the same spec. **Subset sync:** when a concept has **both** properties/operations **and** **`concept.depends_on`**, every class-level peer must also appear on **at least one** property or operation under that concept (no class-only edges). It does **not** prove behavioral correctness, acyclicity, or composition vs aggregation semantics.

**DO**

- Reference peer concepts by the **exact** `concept.name` string used in `modules_and_epics[].module.concepts[]` (including `Base:Extension` combined names when used).
- In **`module.depends_on[]`**, set **`dependent_concepts`**, **`provides_concepts`**, and **`module`** (provider module name) to values that exist in the spec.
- Prefer **`depends_on`** on **properties** and **operations** once collaborators are known (CRC-style); keep optional **`concept.depends_on`** in sync with members if you use both.

**DON'T**

- Point **`depends_on[].concept`** at a string that does not match any declared concept name.
- Point **`module.depends_on`** at unknown module names or concept names.
- Add **`concept.depends_on`** peers that never appear on any property or operation when the concept already has members (scanner fails).

```json
{
  "depends_on": [
    { "concept": "MemoryScope", "relation": "…", "evidence_chunk_id": "blk_…" }
  ]
}
```

```json
{
  "depends_on": [
    {
      "dependent_concepts": ["MemoryFolderFilterBinding"],
      "module": "Conversational memory and retrieval",
      "provides_concepts": ["MemoryScope"],
      "reason": "…"
    }
  ]
}
```
