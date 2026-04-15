---
rule_id: story-map-before-domain-types
---

## Shaped story map before sparse domain types

**Process:** Phase **3** (shaped story map) **before** Phase **4** (`concepts[]` promotion). See [`process.md`](../content/parts/process.md) and [`story-map.md`](../content/parts/library/story-map.md#why-story-mapping-before-domain-types) (ordering rationale + interaction tree).

If types land first, stories drift toward **nouns that already exist in `concepts[]`**, and alignment becomes **string-matching**, not **capability**. This pipeline orders **actor → behavior → anchor** in the story map **before** promotion decisions.

At **shaped-story-map** (phase bundle), you produce **`shaped_story_map.json`** at the root of **`output_dir`** with **actor–behavior** stories—not a type checklist. See [`shaped-story-map.md`](../content/parts/phases/shaped-story-map.md).

At **domain-types**, promotion to `concepts[]` uses **explicit accept/reject** rationale against the **candidate queue** and the story map. You do **not** mint types because a heading matched a string; you mint them where **distinct behavioral contracts** are justified.

Older “step” numbering mixed story and type work. Here, **phase filenames** (`shaped-story-map.md` vs `domain-types.md`) are the source of truth—not “step3” labels from another skill.

**DO**

- Complete **`shaped_story_map.json`** with actors, stories, and evidence **before** promoting sparse `concepts[]` beyond the scaffold.

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

Types-first **without** a prior shaped story map—**violation** of this pipeline’s order.
