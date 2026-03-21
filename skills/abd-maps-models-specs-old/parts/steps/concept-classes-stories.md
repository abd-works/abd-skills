# Concept Classes and Stories

**This file is the prompt.** **Concept Classes and Stories** (see **[Stage 2](../process.md)**) is **AI-authored**: domain and stories must come from **model reasoning**, not from Python heuristics. Two supported ways to run it:

1. **Interactive** — In chat (or an agent with this skill): bring `map-model-spec.json` and the pair’s chunks; follow **Process Per Module/Epic Pair** (Pass 1–4); edit the spec with file tools.
2. **Chat API (listed script)** — `python scripts/deepen_pair_chat_api.py --spec … --chunks … --pair-index N` — same **chunk batching as [Concept Classification](../process.md)** (`classify_chunks.py`). **No silo:** each **observation** batch gets the **full module** for the pair plus the **epic slice for that run**. **Default:** `--split-threshold-chars` is **0** → **one** whole pair every time (no sharding — minimize complexity). **Only if** compact pair JSON + batches risk blowing model context, set `--split-threshold-chars` to a positive char limit; then shards use **sub_epic** subtrees or **story batches**, plus one **active chunk cluster** per shard. **Synthesis** per shard returns full `module` + `epic`; the driver **grafts** epic subtrees **by scope**. When **several shards** run, each shard is **pinned** to a **sub_epic** path: the driver **nests** that run’s `module` payload under **`sub_modules`** mirroring that path (story batches use the **parent** sub_epic chain), then **merges** by **sub_module** / **concept** name so sibling branches stay separate namespaces; pair-level **`chunk_ids`** are **unioned**. **`deepen_pair_chat_api_run`** records **`run_boundary`** (`single_run` vs `isolated_runs`), **`module_merge_policy`** (`single_pass_replace` vs `isolated_perspectives_merge_sub_epic_sub_modules`), **`epic_root_name`**, per-shard **`run_boundary_tag`** / **`run_boundary_index`**, **`scope_hierarchy`** (epic → sub_epic → nested → optional stories_batch), **`hierarchy_display`**, **`isolated_runs`**, **`reconciliation_hint`**, and **`module_merge_note`** when multiple shards ran. **`--dry-run`** prints planned shards with hierarchy. Requires `OPENAI_API_KEY` (see `conf/.secrets`). See rule **step6-deepen-ai-only-no-merge-scripts**.

Afterward, **code** runs scanners and `build_chunk_index.py` — separate from the deepen pass.

## Non-negotiable: no unofficial merge scripts for this step

**Do not** write or run **ad-hoc** Python to splice / replay / bulk-inject **Concept Classes and Stories** output. **Do not** fabricate domain text in code. The **only** scripted path for this step is **`deepen_pair_chat_api.py`** (chat API end-to-end), same class as **`classify_chunks.py`**. Otherwise **edit the JSON and MD** in session. Re-running a deepen means a **new** API run or a **new** interactive pass — not a private merge replay tool.

---

## Purpose

Take the spec produced by **[Foundational mechanisms](../process.md)** + **[Modules and Epics](../process.md)** (module/epic pairs, initial concepts; chunk evidence per concept and per pair), and **deepen** it **one module/epic pair at a time**. The ordered work is defined only in **Process Per Module/Epic Pair** (Pass 1 → Pass 4): complete harvest and deferral resolution → deepen concepts → deepen stories (with hierarchy) → sync domain and story map. Everything else in this doc (**Core Constraints**, **Flagging**, **What to Produce**, **Rules**) supports or constrains those passes — not a second pipeline.

**Domain and story map stay in sync.** Concepts participate in stories as callers/receivers; state flows through Pre-Condition, Triggering-State, Resulting-State. When you add or revise an interaction, derive or update concepts accordingly. Do not edit one view without the other.

Epics come from context. Keep ~4–9 children per node. Use representative examples to illustrate **structure** (hierarchy, story shape); for **concepts**, Pass 1 adds every evidenced concept from the pair’s chunks — do not cap at representative examples. Derive domain from interactions.

### Domain + story map — relevant excerpts only (full specs: **`parts/domain.md`**, **`parts/story-map.md`**)

*Domain (deepen JSON — Pass 2–3):*

- **`owns`** + **`owns_chunk`** (or equivalent evidence) for every concept you keep; add **`properties`[] / `operations`[]** only with **`chunk`** per field (**`parts/domain.md`** — scaffold / composition).
- **`extends`**: use parent concept **`name`** when the text supports **is-a**; keep **has-a** in properties/operations, not a fake **`extends`** (**`parts/domain.md`** — *Composition vs extends*).
- Advance **`evidence_stage`** toward **`deepened`** when Pass 2–3 substantiate detail beyond **`scaffolded`** (**`parts/domain.md`** — evidence stages table).
- **`concept.foundational`**: tag when the concept spans multiple mechanisms/chunks (**`parts/domain.md`** — *Foundational classes*).

*Story map (deepen JSON — Pass 3–4):*

- **Sub-epics / stories**: **Trigger** (actor + action) and **Response**; ground domain nouns with **`**ConceptName**`** matching **`concepts[].name`** (**`parts/story-map.md`** — *Per Interaction*, *Domain Grounding*).
- **Pre-Condition / Resulting-State** only when chunks evidence them (**`parts/story-map.md`** — *Pre-Condition*, flow fields).
- **Inline Concepts** under epics stay **compact** and **name-aligned** with the module’s **`concepts[]`** (**`parts/story-map.md`** + sync rule **`domain-interaction-sync`**).

*Sync (Pass 4):* Interaction change → concept update and vice versa — already required in **Core Constraints** below; use the excerpts above as the **field-level** checklist against the canonical parts.

---

## Inputs

- `map-model-spec.json` — the evolving output (**Modules and Epics** scaffold; **Concept Classification** AI + code enriched with `chunk_evidence`; this step deepens it)
- Chunks — from context (e.g. `context/chunks/*.md` or index); read only chunks listed for each pair (`chunk_ids.identified`, `chunk_ids.provisional`, `concept.chunk_ids`)
- `open_questions` and `cross_cutting_notes` in map-model-spec.json — resolve or re-flag

---

## Chunk Strategy Per Module/Epic

**Discrete, dedicated passes.** Each module/epic pair is processed in a **single, self-contained pass**. No interleaving. No mixing context from one pair into another. Complete one pair fully — deepen concepts, deepen stories, sync — before starting the next.

**One pass = one pair.** For each pair, run **Pass 1 through Pass 4** in **Process Per Module/Epic Pair** (below) as one self-contained unit before starting the next pair. Operationally:

1. Read from `map-model-spec.json` — `chunk_ids.identified` and `chunk_ids.provisional` for this pair; `concept.chunk_ids` or `concept.chunk_evidence` for each concept. Use **only** those chunks.
2. **Read deferred chunks** — for any `[defer]` in this pair, read the cited chunk and resolve (this begins Pass 1).
3. **Do not re-sample** — use the index. The output already decided what belongs where.
4. **Update `map-model-spec.json`** — write the deepened pair back; do not carry in-memory context to the next pair.

**Process ordering:** Order **`modules_and_epics`** pairs using **`module.depends_on`** (from **[Modules and Epics](../process.md)**): **topological** sort so **provider** modules (those that export `provides_concepts` others need) are deepened **before** dependents. Where the graph has no order constraint, use judgment: core resolution/flow before setup, config, peripheral — but **never** deepen a dependent before its named providers unless `open_questions` documents an explicit exception.

**Isolation:** Prefer focusing each pair in its own stretch of the conversation (or a new chat) so you don’t mix chunks from another pair. Minimum bar: mentally scope to **one pair and its listed chunks** per round of Pass 1–4, write that pair back to the spec, then move on.

---

## Core Constraints

**On domain concepts:**
- A concept earns its place by **owning decisions** or **enforcing rules** — not by appearing as a noun.
- **Derive** properties and operations from interactions and stories; do not invent collaborators or relationships not present in source material.
- When updating interactions: (1) interactions first, (2) derive concepts from interactions, (3) model concepts in OOAD style, (4) add inline Concepts blocks under epics with compact definitions.
- Property types: String, Number, Boolean, List\<T\>, Dictionary\<K,V\>, EnumType {val1, val2}, UniqueID, Instant. Dictionary when items accessed by key; List only when order matters.
- Tag `[foundational]` if the concept appears across multiple chunks and multiple mechanisms.

**On hierarchy:**
- **~4–9 children** per node (epic, sub-epic, story). Does not apply to steps. For stories, count steps as children.
- Epic: ~4–9 sub-epics or stories. Story: ~4–9 steps (total across scenarios). Scenario: ~4–9 steps.
- **DO NOT** create nodes with many more than 9 children — split or regroup.
- **Epics from context** — not from chunk order. Sub-epics group related stories functionally.

**On stories:**
- Every story has **Trigger** (Actor + action) and **Response** (system or other actor). Ground in `**Concept**` where domain concepts participate.
- **Pre-Condition**: Given **Concept** is in state X. Only if evidenced.
- **Failure-Modes**: up to 3. When/Then format. Only if evidenced.
- **Inheritance**: shared steps live at higher level; child inherits. Avoid duplication.

**On domain–story map sync:**
- Concepts participate as callers/receivers in stories. State flows through Pre-Condition, Triggering-State, Resulting-State.
- **DO NOT** edit only the story map and skip the Domain Model. Interaction changes often imply concept changes.
- Example (right): Epic "Make Checks" has inline Concepts: `Check: targetNumber, roll(dice): Result`; `DifficultyClass: value`. After revising an interaction that touches CheckResult, add CheckResult to both.

---

## Flagging

**`[defer]`** — resolved in Step 6 by targeted read. If still unresolved after read, keep in `open_questions` with reason.

**`[uncertain]`** — requires human confirmation. Do not proceed on it without confirmation.

**`[cross-cutting]`** — remains in `cross_cutting_notes` until **[Integrate and Harmonize](../process.md)**. Do not assign to one module yet.

---

## Process Per Module/Epic Pair

These passes are the **single definition** of **Concept Classes and Stories** work for one module/epic pair. **Core Constraints**, **Flagging**, **What to Produce**, and **Rules** elaborate and enforce what you do here — they are not a separate workflow.

### Pass 1 — Resolve deferrals and add missing concepts

**Goal:** The module’s concept list for this pair is **complete** before you deepen anything.

1. **Deferrals** — For each `[defer]` on this pair (or its concepts), read the **cited chunk**. Decide: subtype vs enum (or other resolution). If still unclear, keep in `open_questions` with reason.
2. **Exhaustive concept harvest** — Using **all chunks bound to this pair** (`chunk_ids.identified`, `chunk_ids.provisional`, and every `concept.chunk_ids` for concepts in this module), scan the **full text** of those chunks. Add **every** domain concept the text evidences but that is **not** yet in the module — e.g. named effect types, modifier types, descriptors, named states or outcomes the rules treat as distinct.
3. **No “representative sample” cap for concepts** — If the corpus names or enumerates variants, model them (as concepts or subtypes) with chunk evidence. Representative examples apply to **story shape and hierarchy illustration**, not to hiding evidenced concepts (see Purpose).

### Pass 2 — Deepen concepts

**Goal:** Each concept is a decision-owning model element grounded in chunks.

1. **From chunk evidence only** — Add properties, operations, invariants, and relationships that the chunks support. Derive from evidence; **do not invent** collaborators or mechanics not in the provided text.
2. **`owns`** — Every concept must have `owns`: one sentence on what **decision or rule** it owns (see **Concepts must have owns** under Rules).
3. **`[foundational]`** — Tag when the concept appears across **multiple chunks** and **multiple mechanisms** (aligns with Core Constraints).
4. **Property types** — Use only: String, Number, Boolean, List\<T\>, Dictionary\<K,V\>, EnumType {val1, val2}, UniqueID, Instant. Dictionary when keyed access; List when order matters.

### Pass 3 — Deepen stories

**Goal:** The interaction view matches the domain depth and stays within hierarchy limits.

1. **Trigger / Response** — Every story: `trigger` (Actor + action), `response` (system or other actor). Ground participation in `**Concept**` where domain elements appear.
2. **Optional fields (evidence only)** — `pre_condition` (Given **Concept** in state…), `failure_modes` — **max 3**, When/Then style, only if chunks support them.
3. **Hierarchy** — Keep ~**4–9 children** per epic, sub-epic, or story (steps count as story children). Add `sub_epics` when needed instead of a flat overload of stories.

### Pass 4 — Sync domain and story map

**Goal:** No drift between module and epic.

1. **Coverage** — Every concept in this module appears in **at least one** story (trigger, response, or pre-condition). Every story **references** a concept.
2. **Co-evolution** — If you change an interaction, **update** the domain model (and vice versa). Do not edit only the story map or only the module.

---

## How you run it (chat)

1. **Instructions** — Already in this file (above and below). There is no separate “system prompt” artifact for Step 6.
2. **Context** — Open or @ the current `map-model-spec.json` and the chunk files listed for the pair you’re deepening.
3. **Say which pair** — Name the module and epic you’re working on so the turn stays scoped.
4. **Execute** — Walk Pass 1 → **Pass 1b (gate)** → Pass 2 → Pass 4; emit the deepened module + epic in the shape described under **What to Produce** and **Output**.
5. **Merge** — Apply that result back into the full `map-model-spec.json` by **direct edit** (replace the one `modules_and_epics[i]` object), or by running **`deepen_pair_chat_api.py`** (single shard: replace pair from synthesis; **multiple shards**: nest `module` under **sub_modules** per sub_epic pin, merge, union `chunk_ids`, graft `epic` per scope). **Not** by an unofficial merge script. Then run **Quality Passes** (scanners are code, not chat).

---

## Rules

These rules apply after you have deepened each pair. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Chunks must be referenced (reuse)
*Scanner: `scripts/scanners/chunks_must_be_referenced.py` → Rule: `chunks-must-be-referenced.md`*

**DO** ensure every concept, property, operation, story, trigger, response, pre-condition has chunk evidence.

**DO NOT** populate a field without evidence. Use `[defer]` if evidence exists but was not fully read.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO NOT** have two concepts with the same name within a module. **DO NOT** have two modules with the same name.

---

### Epic requires confirming stories (reuse)
*Scanner: `scripts/scanners/epic_requires_confirming_stories.py` → Rule: `epic-requires-confirming-stories.md`*

**DO** include **as many** story names per epic as needed to validate foundational concepts (often **more** than two). **Do not** treat two as a target. At Step 3, stories have full Trigger/Response; `confirming_stories` is the list of story names.

---

### No junk concepts (reuse)
*Scanner: `scripts/scanners/no_junk_concepts.py` → Rule: `no-junk-concepts.md`*

**DO NOT** use section headers, all-caps labels, proper nouns, instruction phrases as concept names.

---

### Concepts must have owns
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field — one sentence on what decision or rule this concept owns.

**DO NOT** leave a concept with only chunk_ids and no decision ownership.

---

### Stories must have trigger and response
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has `trigger` (Actor + action) and `response` (system or other actor).

**DO NOT** leave a story with only a name. Trigger and response ground the story in domain.

---

### Domain–story map sync
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept in the module participates in at least one story (trigger, response, or pre-condition).

**DO NOT** have orphan concepts — concepts that appear in the domain model but in no story.

---

### Hierarchy sizing (approximately 4–9 children)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range for manageable granularity.

**DO NOT** create nodes with many more than 9 children — split or regroup.

---

### Derive concepts from interactions (AI-only)
*(AI-only — no scanner)*

**DO** derive properties and operations from interactions and stories.

**DO NOT** invent collaborators or relationships not present in source material.

---

### Discover all evidenced concepts (AI-only)
*(AI-only — no scanner)*

**DO** add every domain concept that is evidenced in the pair’s chunks (e.g. every effect type, every modifier type, every descriptor the text defines or names). This is done in **Pass 1** per module/epic pair.

**DO NOT** limit the concept list to "representative examples" — if the text enumerates or names variants, add them as concepts (or as subtypes) with chunk evidence.

---

## What to Produce Per Module/Epic Pair

### Domain view — Module (deepened)

```
name: noun phrase
description: one sentence (chunk: id)

concepts:
  ConceptName [foundational if applicable]
    chunk_ids: [ids]
    owns: one sentence on what decision or rule this concept owns (chunk: id)
    properties:
      - type definition (chunk: id)
    operations:
      - signature (chunk: id)
    invariants:
      - constraint (chunk: id)   ← only if evidenced
    relationships:
      - concept: OtherConcept, role: caller|receiver|state (chunk: id)   ← only if evidenced
```

### Interaction view — Epic (deepened)

```
name: Verb Noun (grounded in **Concept**)
statement: **Actor** does X across **Concept** flows; **System** responds. (chunk: id)
triggering_actor: who starts
responding_actor: who responds
pre_condition: Given **Concept** is X (chunk: id)

sub_epics:   ← optional; add if epic has >9 stories or logical grouping
  - name: Verb Noun
    stories: [story names]

stories:
  - name: Verb Noun
    trigger: **Actor** does X (chunk: id)
    response: **System** does Y (chunk: id)
    pre_condition: Given **Concept** is Z (chunk: id)   ← optional
    failure_modes:   ← optional; max 3
      - when: condition; then: outcome (chunk: id)
    chunk_ids: [ids]
```

---

## Output

After each pair, merge the result into the full spec.

### `map-model-spec.json` (updated)

Same structure as before, with these enrichments:
- Concepts: full properties, operations, invariants, relationships
- Stories: trigger, response, pre_condition, failure_modes
- Sub-epics where needed
- `open_questions` and `cross_cutting_notes` updated (resolved items removed)

### `map-model-spec.md` (updated)

One section per pair, with full concept and story detail.

---

## After Generation — Quality Passes

### Quality pass 1 — Scanners (code)

Run all **[Modules and Epics](../process.md)** scaffold scanners plus **Concept Classes and Stories** scanners:

```
python scripts/scanners/chunks_must_be_referenced.py --input map-model-spec.json
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/epic_requires_confirming_stories.py --input map-model-spec.json
python scripts/scanners/no_junk_concepts.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
```

| Scanner | Rule file | What it checks |
|---|---|---|
| `scripts/scanners/chunks_must_be_referenced.py` | `chunks-must-be-referenced.md` | Every evidence claim cites a chunk |
| `scripts/scanners/no_duplicates.py` | `no-duplicates.md` | No duplicate concept or module names |
| `scripts/scanners/epic_requires_confirming_stories.py` | `epic-requires-confirming-stories.md` | Every epic has ≥1 confirming story name (add more as needed for coverage) |
| `scripts/scanners/no_junk_concepts.py` | `no-junk-concepts.md` | No junk concept names |
| `scripts/scanners/concepts_have_owns.py` | `concepts-must-have-owns.md` | Every concept has `owns` |
| `scripts/scanners/stories_have_trigger_response.py` | `stories-must-have-trigger-response.md` | Every story has trigger and response |
| `scripts/scanners/domain_interaction_sync.py` | `domain-interaction-sync.md` | Every concept in at least one story |
| `scripts/scanners/hierarchy_sizing.py` | `hierarchy-approximately-4-to-9-children.md` | ~4–9 children per node |

### Quality pass 2 — Build chunk index (code)

```
python scripts/build_chunk_index.py --input map-model-spec.json --output mms-chunk-index.json
```

### Quality pass 3 — Adversarial validation (AI)

Re-read output against each rule. Be adversarial:
- Any concept with `owns` that is just restating its name?
- Any story with trigger/response that doesn't reference a concept?
- Any orphan concept?
- Any node with >9 children that wasn't split?
- Any domain change without corresponding interaction change (or vice versa)?

---

## Stop for Review

Present the readable summary and ask:

1. Are concept hierarchies correct? Any missing relationships?
2. Are sub-epic groupings sensible?
3. Are all `[defer]` flags resolved or re-flagged?
4. Does domain and story map stay in sync?
