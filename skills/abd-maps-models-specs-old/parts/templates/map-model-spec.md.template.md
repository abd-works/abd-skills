# Parameterized template — `map-model-spec.md`

Use this **exact layout** whenever you produce or refresh **`map-model-spec.md`**. Copy the structure below into the workspace artifact and **replace every `{{…}}`** with values from **`map-model-spec.json`** at the same paths. No code generator is required—this file is the contract.

**Vocabulary:** Domain sections follow **`parts/domain.md`**. Story sections follow **`parts/story-map.md`**. Headings are **demoted one level** inside the combined document so there is only one `#` title (see table).

---

## JSON → placeholders (root)

| Placeholder | JSON path |
|-------------|-----------|
| `{{phase}}` | `phase` |
| `{{phase_note}}` | `phase_note` |
| `{{source_corpus}}` | `source_corpus` |
| `{{context_index}}` | `context_index` |
| `{{N_chunks}}` | `N_chunks` |
| `{{open_questions}}` | `open_questions` — list; if empty write `*None.*` |
| `{{cross_cutting_notes}}` | `cross_cutting_notes` — if empty write `*None.*` |

---

## JSON → placeholders (each pair `modules_and_epics[i]`)

| Placeholder | JSON path |
|-------------|-----------|
| `{{pair_index}}` | `i + 1` (1-based) |
| Module block | `modules_and_epics[i].module` |
| Epic block | `modules_and_epics[i].epic` |
| Buckets | `modules_and_epics[i].chunk_ids` |

**Module:** `name`, `foundational`, `description`, `description_chunk`, `depends_on` (optional array), `concepts[]`.

**Each concept:** `name`, `foundational`, `evidence_stage`, `chunk_ids`, `chunk_evidence` (optional), `owns`, `owns_chunk`, `properties` (optional), `operations` (optional).

**Epic:** `name`, `statement`, `statement_chunk`, `triggering_actor`, `responding_actor`, `pre_condition`, `pre_condition_chunk` (optional), `confirming_stories[]`.

**Optional fields:** If missing, use `—` for table cells, omit optional bullets, or write *Not present.*

---

## Heading level shift (single document)

| Reference doc | Standalone | In `map-model-spec.md` |
|---------------|------------|-------------------------|
| `domain.md` | `## Module: …` | `### Module: …` under **Domain model** |
| `story-map.md` | `# Epic: …` | `### Epic: …` under **Story map** |

One `# Map model spec` for the whole file. Each JSON pair is one `##` section.

---

## Template — top matter (once)

Fill from root JSON keys; keep the table and headings.

```markdown
# Map model spec — {{source_corpus}}

_Human-readable twin of `map-model-spec.json`. When the JSON changes, rewrite this file using **`parts/templates/map-model-spec.md.template.md`**._

## Document metadata

| Field | Value |
|-------|--------|
| Phase | {{phase}} |
| Source corpus | {{source_corpus}} |
| Context index | {{context_index}} |
| N chunks | {{N_chunks}} |
| Phase note | {{phase_note}} |

## Open questions

{{open_questions_bullets_or_None}}

## Cross-cutting notes

{{cross_cutting_notes_or_None}}

---
```

---

## Template — one block per `modules_and_epics[]` entry

Repeat the whole block for each pair, in array order.

```markdown
## {{pair_index}}. {{module.name}} · {{epic.name}}

### Domain model

_Shape: `parts/domain.md` (module + **Concept** headings, citations from JSON)._

### Module: {{module.name}}

- **Foundational (module):** {{module.foundational true/false}}
- **Description:** {{module.description}} — *chunk:* `{{module.description_chunk}}`
- **Depends on:** {{depends_on_bullets_each_entry_in_module.depends_on_or_dash}}
- **Concepts:** {{list_concept_names_with_bold_markdown e.g. **Rank**, **MeasurementTable**}}

#### **{{concept.name}}**

- **Evidence stage:** {{concept.evidence_stage}}
- **Foundational (concept):** {{concept.foundational true/false/—}}
- **Chunk ids:** {{backtick_join concept.chunk_ids}}
- **Chunk evidence:** {{optional_bullets_from_chunk_evidence_or_—}}
- **Owns:** {{concept.owns}} — *chunk:* `{{concept.owns_chunk}}`
- **Properties:** {{optional_bullets_definition_plus_chunk_or_—}}
- **Operations:** {{optional_bullets_definition_plus_chunk_or_—}}

_(Repeat the `#### **{{concept.name}}**` subsection for every concept in `module.concepts`.)_

### Story map

_Shape: `parts/story-map.md` (epic interaction; Scenario/Step blocks appear in later phases when JSON has them)._

### Epic: {{epic.name}} ({{epic.statement_short_for_heading}})

Use the full `epic.statement` in the heading if it is short; if long, use a shortened parenthetical and keep the full statement on the next line.

**Full statement:** {{epic.statement}} — *chunk:* `{{epic.statement_chunk}}`

- **Pre-Condition:** {{epic.pre_condition_or_—}} — *chunk:* `{{epic.pre_condition_chunk_or_—}}`
- **Trigger**
  - **Triggering-Actor:** {{epic.triggering_actor}}
  - **Behavior (When):** _(derive from statement / corpus; at scaffold may mirror the statement)_
- **Response**
  - **Responding-Actor:** {{epic.responding_actor}}
  - **Behavior (Then):** _(derive from statement / corpus; at scaffold may mirror the statement)_
- **Confirming stories (scaffold):**
  1. {{confirming_stories[0]}}
  2. {{confirming_stories[1]}}
  3. _(etc.)_

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | {{backtick_join chunk_ids.identified}} |
| provisional | {{backtick_join chunk_ids.provisional}} |
| ambiguous | {{backtick_join chunk_ids.ambiguous}} |

---
```

---

## Conventions

- **Concept names** in the domain section should match **`**Name**`** usage in the epic **statement** where they refer to the same thing.
- **`depends_on`:** For each object in `module.depends_on`, emit a bullet: dependent concepts, providing module, provided concepts, reason (all from JSON).
- **`chunk_evidence`:** For each `{ chunk_id, evidence_type, note }`, emit `- \`chunk_id\` (*type*): note`.
- **`properties` / `operations`:** `- {{definition}} — *chunk:* \`{{chunk}}\``
