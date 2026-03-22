---
rule_id: story-map-before-domain-types
phase_files:
  - story-map.md
  - domain-types.md
---

## Behavioral story map before sparse domain types

**Process:** Phase **3** (behavioral story map) **before** Phase **4** (`concepts[]` promotion). See [`process.md`](../content/parts/process.md) and [`why-story-mapping-first.md`](../content/parts/library/why-story-mapping-first.md).

If types land first, stories drift toward **nouns that already exist in `concepts[]`**, and alignment becomes **string-matching**, not **capability**. This pipeline orders **actor → behavior → anchor** in the story map **before** promotion decisions.

At **story-map**, you produce `phase3/mm3_story_map.json` with **behavioral** stories—not a type checklist. See [`behavioral-story-map.md`](../content/parts/library/behavioral-story-map.md).

At **domain-types**, promotion to `concepts[]` uses **explicit accept/reject** rationale against the **candidate queue** and the story map. You do **not** mint types because a heading matched a string; you mint them where **distinct behavioral contracts** are justified.

Older “step” numbering mixed story and type work. Here, **phase filenames** (`story-map.md` vs `domain-types.md`) are the source of truth—not “step3” labels from another skill.

**DO**

- Complete `mm3_story_map.json` with actors, behavioral stories, and evidence **before** promoting `concepts[]`.

```json
{
  "phase": "story_map",
  "stories": [{ "name": "Customer places order", "evidence_chunk_ids": ["chunk-01"] }]
}
```

**DON'T**

- Seed **`concepts[]`** from a spreadsheet of nouns **first**, then write stories that only restate those type names.

```json
{
  "phase": "domain_types",
  "concepts": [{ "name": "OrderAggregate" }],
  "story_map": "written later to match"
}
```

Types-first **without** a prior behavioral map—**violation** of this pipeline’s order.
