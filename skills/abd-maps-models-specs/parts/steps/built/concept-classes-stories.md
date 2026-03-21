# Concept Classes and Stories

**This file is the prompt.** **Concept Classes and Stories** (see **[Stage 2](../../process.md)**) is **AI-authored**: domain and stories must come from **model reasoning**, not from Python heuristics. Two supported ways to run it:

1. **Interactive** — In chat (or an agent with this skill): bring `map-model-spec.json` and the pair’s chunks; follow **Process Per Module/Epic Pair** (Pass 1–4); edit the spec with file tools.
2. **Chat API (listed script)** — `python scripts/deepen_pair_chat_api.py --spec … --chunks … --pair-index N` — same **chunk batching as [Concept Classification](../../process.md)** (`classify_chunks.py`). **No silo:** each **observation** batch gets the **full module** for the pair plus the **epic slice for that run**. **Default:** `--split-threshold-chars` is **0** → **one** whole pair every time (no sharding — minimize complexity). **Only if** compact pair JSON + batches risk blowing model context, set `--split-threshold-chars` to a positive char limit; then shards use **sub_epic** subtrees or **story batches**, plus one **active chunk cluster** per shard. **Synthesis** per shard returns full `module` + `epic`; the driver **grafts** epic subtrees **by scope**. When **several shards** run, each shard is **pinned** to a **sub_epic** path: the driver **nests** that run’s `module` payload under **`sub_modules`** mirroring that path (story batches use the **parent** sub_epic chain), then **merges** by **sub_module** / **concept** name so sibling branches stay separate namespaces; pair-level **`chunk_ids`** are **unioned**. **`deepen_pair_chat_api_run`** records **`run_boundary`** (`single_run` vs `isolated_runs`), **`module_merge_policy`** (`single_pass_replace` vs `isolated_perspectives_merge_sub_epic_sub_modules`), **`epic_root_name`**, per-shard **`run_boundary_tag`** / **`run_boundary_index`**, **`scope_hierarchy`** (epic → sub_epic → nested → optional stories_batch), **`hierarchy_display`**, **`isolated_runs`**, **`reconciliation_hint`**, and **`module_merge_note`** when multiple shards ran. **`--dry-run`** prints planned shards with hierarchy. Requires `OPENAI_API_KEY` (see `conf/.secrets`). See rule **step6-deepen-ai-only-no-merge-scripts**.

Afterward, **code** runs scanners and `build_chunk_index.py` — separate from the deepen pass.

## Non-negotiable: no unofficial merge scripts for this step

**Do not** write or run **ad-hoc** Python to splice / replay / bulk-inject **Concept Classes and Stories** output. **Do not** fabricate domain text in code. The **only** scripted path for this step is **`deepen_pair_chat_api.py`** (chat API end-to-end), same class as **`classify_chunks.py`**. Otherwise **edit the JSON and MD** in session. Re-running a deepen means a **new** API run or a **new** interactive pass — not a private merge replay tool.

---

## Purpose

Take the spec produced by **[Foundational mechanisms](../../process.md)** + **[Modules and Epics](../../process.md)** (module/epic pairs, initial concepts; chunk evidence per concept and per pair), and **deepen** it **one module/epic pair at a time**. The ordered work is defined only in **Process Per Module/Epic Pair** (Pass 1 → Pass 4): complete harvest and deferral resolution → deepen concepts → deepen stories (with hierarchy) → sync domain and story map. Everything else in this doc (**Core Constraints**, **Flagging**, **What to Produce**, **Rules**) supports or constrains those passes — not a second pipeline.

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

**Process ordering:** Order **`modules_and_epics`** pairs using **`module.depends_on`** (from **[Modules and Epics](../../process.md)**): **topological** sort so **provider** modules (those that export `provides_concepts` others need) are deepened **before** dependents. Where the graph has no order constraint, use judgment: core resolution/flow before setup, config, peripheral — but **never** deepen a dependent before its named providers unless `open_questions` documents an explicit exception.

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

**`[cross-cutting]`** — remains in `cross_cutting_notes` until **[Integrate and Harmonize](../../process.md)**. Do not assign to one module yet.

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

Run all **[Modules and Epics](../../process.md)** scaffold scanners plus **Concept Classes and Stories** scanners:

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


---

## Rules (baked in)

Apply these rules when producing output for this step.

# Step 6 — Deepen AI-only (no merge scripts)



**Binding process rule.** Violating this is a process failure, not a style preference.



## Required (pick one path)



- **Path A — Chat / agent session:** Read the pair’s chunks and `map-model-spec.json`, run Pass 1–4 reasoning, and **edit** `map-model-spec.json` and `map-model-spec.md` directly (patch sections, or equivalent).

- **Path B — Listed chat API driver:** Run **`scripts/deepen_pair_chat_api.py`** (same class of tool as `classify_chunks.py`). It batches this pair’s chunks using the **same token budgeting as Step 5** (~8k tokens of chunk text per batch, oversize chunks alone). **Context model:** each **observation** call includes the **full** current shard: always the **entire** `module` for the pair plus the **epic slice** for that run (whole pair when under size limit; otherwise a **sub_epic** subtree, or a **story batch** under a node if still too large — `--split-threshold-chars`, default 120000 compact JSON chars; `0` disables splitting). **Synthesis** returns **one** JSON object per shard with **complete** `module` and `epic` for that scope. **Single shard:** replace the stored pair from synthesis. **Multiple shards:** each run is **pinned** to a **sub_epic** path; the driver **nests** that synthesis **`module`** under **`sub_modules`** mirroring that path (story batches → parent sub_epic chain), then **merges** by **`sub_modules`** / **concept** name; pair **`chunk_ids`** are **unioned**; **`epic`** is **grafted** by scope. **`deepen_pair_chat_api_run`** records **`run_boundary`**: **`single_run`** vs **`isolated_runs`**, **`module_merge_policy`**, **`isolated_runs[]`** with per-shard **`run_boundary_tag`** (**`single_run`** / **`isolated_run`**) and **`run_boundary_index`**, **`epic_root_name`**, **`scope_hierarchy`** (ordered **epic → sub_epic → … → stories_batch**), **`hierarchy_display`** (same chain as one string), plus **`reconciliation_hint`** and **`module_merge_note`** when multiple shards ran so a later **Integrate/Harmonize** (or dedicated reconciliation) step knows how much cross-run stitching may be needed. The JSON shard payload’s **`deepen_shard_scope`** mirrors that hierarchy. Use **`--dry-run`** to print the planned shards without calling the API. Re-run a deepen by running the script again or Path A again — not ad-hoc merge helpers.



## Forbidden



- **Any unofficial** one-off **script** whose **purpose** is to programmatically **merge, splice, bulk-inject, or regenerate** Step 6 content **without** going through the chat API for authoring (e.g. `step6_pairs_*.py` replay merges, idempotent JSON splices that **fabricate** domain text in code).

- **Path B is not optional glue:** If you use code for Step 6, it must be **`deepen_pair_chat_api.py`** (or future listed equivalents in `AGENTS.md`), not a new private merge script.



## Allowed code



- **`classify_chunks.py`** (Step 5) — chat API + deterministic merge of **model-returned** chunk evidence.

- **`deepen_pair_chat_api.py`** (Step 6, optional) — chat API + apply **model-returned** `module`/`epic` (single shard: replace pair; multi-shard: **sub_module** shells per sub_epic pin, merge, union `chunk_ids`, graft `epic`).

- **`build_chunk_index.py`**, **scanners** — indexes and validation after the spec is updated.



## Rationale



Step 6 is defined as an **AI pass** over evidence and the spec. Merge scripts hide reasoning, rot when the schema shifts, and train agents to be lazy. **Do the fucking work** every time.


---

---
rule_id: foundation-coverage-before-deepen
phases: [step6]
order: 18
impact: HIGH
---

## Foundation coverage gate before Pass 2 (deepen)

After **Pass 1** (taxonomy / structure / dependency check on the JSON) and **before** pair ordering and **Pass 2 (deepen)**, verify that the **foundational spine** is **covered** by the planned deepen pairs.

**DO**

- List every concept that is still **`hypothesis`** (or missing `evidence_stage`) under a **`module.foundational: true`** module, plus any concept that **`depends_on`** marks as **provider** for others.
- Ensure each such concept appears in **at least one** deepen pair’s scope (module + epic subtree), or explicitly defer with `open_questions` and a reason. Prefer providers at **`scaffolded`** before you deepen dependents.
- Order pairs so **providers** (modules/concepts that others **`depends_on`**) are **deepened before** dependents when possible — same ordering principle as `module-depends-on.md`.

**DON'T**

- Start deepen on peripheral modules while a **core** foundational concept still has only `inferred` stage and no pair assigned.
- Treat Pass 1 as complete if **`depends_on`** is empty but cross-module concept names clearly overlap — reconcile or record dependencies first.


---

---
rule_id: chunks-must-be-referenced
phases: [step1]
order: 10
scanner: scripts/scanners/chunks_must_be_referenced.py
impact: HIGH
---

## All evidence claims must cite a chunk

Every field that makes an evidence claim must include a chunk reference. An uncited claim is speculation — it cannot be verified, cannot be navigated in later steps, and cannot be included in the reverse index.

The scanner (`scripts/scanners/chunks_must_be_referenced.py`) highlights missing citations. It does not determine whether a missing citation is a genuine gap or a false positive — that judgment belongs to the AI in the adversarial validation pass.

**DO** cite a chunk on every evidence-bearing field:

- `module.description_chunk` — the chunk that evidenced the module description
- `concept.owns_chunk` — the chunk that evidenced what this concept owns
- `concept.chunk_ids` (or `chunk_evidence` with `chunk_id`) — non-empty where the concept is evidenced
- `property.chunk` — the chunk that evidenced this property (paired with `definition`)
- `operation.chunk` — the chunk that evidenced this operation (paired with `definition`)
- `epic.statement_chunk` — the chunk that evidenced the epic statement
- `epic.pre_condition_chunk` — the chunk that evidenced the pre-condition (when `pre_condition` is populated)

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "description": "Originate and release customer payment instructions.",
        "description_chunk": "chunk-mod-pay-1",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns whether a payment instruction is allowed against daily and per-transaction limits",
            "owns_chunk": "chunk-4410b",
            "chunk_ids": ["chunk-4410b", "chunk-4410c"],
            "properties": [
              {
                "definition": "Number dailyLimit",
                "chunk": "chunk-4410b"
              }
            ],
            "operations": [
              {
                "definition": "evaluate(instruction: PaymentInstruction) -> Decision",
                "chunk": "chunk-4410c"
              }
            ]
          }
        ]
      },
      "epic": {
        "name": "Wire transfers",
        "statement": "**Customer** initiates **WireTransfer**; **System** validates limits before release.",
        "statement_chunk": "chunk-09bc",
        "pre_condition": "**Customer** session is authenticated.",
        "pre_condition_chunk": "chunk-09bc"
      }
    }
  ]
}
```

**DO NOT** populate any of these fields without a chunk citation. If you cannot cite a chunk, either leave the field blank or add a `[defer]` flag with the chunk that shows the thing exists but was not fully read.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns whether a payment instruction is allowed against daily and per-transaction limits",
            "chunk_ids": ["chunk-4410b"]
          }
        ]
      },
      "epic": { "name": "Placeholder" }
    }
  ]
}
```

`owns` is set but `owns_chunk` is missing — violation.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Provisioning",
        "description": "Install and activate customer circuits from service orders."
      },
      "epic": { "name": "Placeholder" }
    }
  ]
}
```

`description` is set but `description_chunk` is missing — violation.

Do not cite a nearby chunk “by proximity” when the corpus does not support the claim — use `[defer]` in the owning text and a real chunk id that proves the gap is documented.


---

---
rule_id: no-duplicates
phases: [step1, step2, step3, step5]
order: 15
scanner: scripts/scanners/no_duplicates.py
impact: HIGH
---

## No duplicate names at the same scope

The same name must not appear twice among siblings at the same level: duplicate module names, duplicate concept names within a module, duplicate epic names at the same parent, duplicate story names under the same epic or sub-epic.

The scanner (`scripts/scanners/no_duplicates.py`) flags collisions.

**DO** use distinct names or merge duplicates into one entry with combined evidence.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": { "name": "Settlement", "stories": [] }
    }
  ]
}
```

```json
{
  "name": "Retail",
  "concepts": [
    {
      "name": "Cart",
      "owns": "Owns line items before checkout",
      "owns_chunk": "chunk-a",
      "chunk_ids": ["chunk-a"]
    },
    {
      "name": "Promotion",
      "owns": "Owns discount rules",
      "owns_chunk": "chunk-b",
      "chunk_ids": ["chunk-b"]
    }
  ]
}
```

**DO NOT** repeat the same module name in `modules_and_epics[]`.

```json
{
  "modules_and_epics": [
    { "module": { "name": "Retail", "concepts": [] }, "epic": { "name": "A", "stories": [] } },
    { "module": { "name": "Retail", "concepts": [] }, "epic": { "name": "B", "stories": [] } }
  ]
}
```

**DO NOT** repeat concept names within one module.

```json
{
  "name": "Retail",
  "concepts": [
    {
      "name": "Cart",
      "owns": "Owns line items",
      "owns_chunk": "chunk-a",
      "chunk_ids": ["chunk-a"]
    },
    {
      "name": "Cart",
      "owns": "Owns totals display",
      "owns_chunk": "chunk-c",
      "chunk_ids": ["chunk-c"]
    }
  ]
}
```

**DO NOT** repeat story names under the same parent.

```json
{
  "name": "Checkout",
  "stories": [
    { "name": "Apply tax", "trigger": "…", "response": "…" },
    { "name": "Apply tax", "trigger": "…", "response": "…" }
  ]
}
```


---

---
rule_id: epic-requires-confirming-stories
phases: [step1]
order: 25
scanner: scripts/scanners/epic_requires_confirming_stories.py
impact: HIGH
---

## Every epic needs confirming stories

An `epic.statement` makes a behavioral claim. At least one story under that epic (directly or via `sub_epics`) must **confirm** that claim — its `trigger` / `response` should exercise the same actors and domain concepts named in the statement.

**How many names in `confirming_stories[]`:** As **many as required** so the **foundational concepts** that epic is responsible for are **validated** in story form — not a default of two, not a ceiling. Add story names until coverage is honest; the mechanical scanner only checks **at least one** non-empty name so the list is never empty.

**Scaffold JSON (`confirming_stories[]` on the epic):** Domain nouns in those strings must **`concepts[].name`** **exactly** (100% match) — **`scaffold-concept-story-name-alignment`**. Non-negotiable alongside this rule.

The scanner (`scripts/scanners/epic_requires_confirming_stories.py`) checks overlap between bolded terms in the statement and each story's trigger/response.

**DO** align story text with the epic statement so concepts and actors reappear.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire release",
        "statement": "**Customer** submits **WireTransfer**; **System** runs **LimitChecker** before **SettlementBatch**.",
        "statement_chunk": "chunk-w1",
        "stories": [
          {
            "name": "Happy path limits pass",
            "trigger": "**Customer** submits **WireTransfer** for amount within limits",
            "response": "**System** runs **LimitChecker**, approves, and enqueues **SettlementBatch**"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Retail promotions",
        "statement": "**Cashier** adds **LineItem** to **Cart**; **System** applies **Promotion** rules.",
        "statement_chunk": "chunk-r1",
        "sub_epics": [
          {
            "name": "Stacking",
            "stories": [
              {
                "name": "Second promo on same cart",
                "trigger": "**Cashier** adds a second **Promotion** to **Cart** with multiple **LineItem** rows",
                "response": "**System** recomputes discounts per stacking policy"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

**DO NOT** leave an epic with only unrelated stories — no shared bolded concepts with the statement.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire release",
        "statement": "**Customer** submits **WireTransfer**; **System** runs **LimitChecker**.",
        "statement_chunk": "chunk-w1",
        "stories": [
          {
            "name": "Password reset email",
            "trigger": "**Customer** requests password reset",
            "response": "**System** sends email token"
          }
        ]
      }
    }
  ]
}
```

No overlap with **WireTransfer** or **LimitChecker** — violation.

**DO NOT** use a generic story that never names the epic's domain concepts.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Combat", "concepts": [] },
      "epic": {
        "name": "Combat resolution",
        "statement": "**Player** rolls **Attack** against **ArmorClass**.",
        "statement_chunk": "chunk-srd-1",
        "stories": [
          {
            "name": "Session start",
            "trigger": "**Player** joins table",
            "response": "**System** shows welcome screen"
          }
        ]
      }
    }
  ]
}
```

No **Attack** or **ArmorClass** in stories — violation.


---

---
rule_id: no-junk-concepts
phases: [step2, step3, step5]
order: 30
scanner: scripts/scanners/no_junk_concepts.py
impact: HIGH
---

## No junk concepts

A concept is junk if it is a synonym of another concept, a UI label with no decision ownership, a database table name mistaken for domain meaning, or a passive noun with no rules.

The scanner (`scripts/scanners/no_junk_concepts.py`) flags likely junk. Borderline cases are resolved in assessment.

**DO** merge synonyms into one concept with `aliases` (or one canonical name and evidence that ties alternate terms to the same chunk).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "ShoppingCart",
            "aliases": ["Basket", "Cart"],
            "owns": "Owns line items and running totals before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "InventoryReservation",
            "owns": "Owns whether stock is held for an order line and for how long",
            "owns_chunk": "chunk-retail-inv-2",
            "chunk_ids": ["chunk-retail-inv-2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** introduce parallel concepts for the same decision with only naming drift.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "ShoppingCart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
          },
          {
            "name": "Basket",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Two concepts, same `owns` and same chunks — junk duplicate.

**DO NOT** model passive containers as concepts when they carry no rules.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Ops",
        "concepts": [
          {
            "name": "OrderHeaderRow",
            "owns": "Row in the orders table",
            "owns_chunk": "chunk-db-99",
            "chunk_ids": ["chunk-db-99"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Table shape is not domain ownership — fold into `Order` or drop.

**DO NOT** invent concepts for every UI string.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "UI",
        "concepts": [
          {
            "name": "SubmitButton",
            "owns": "The button the user clicks",
            "owns_chunk": "chunk-mockup-1",
            "chunk_ids": ["chunk-mockup-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

UI chrome is not a domain concept unless the source assigns it explicit behavioral rules.


---

---
rule_id: concepts-must-have-owns
phases: [step2, step3, step5]
order: 20
scanner: scripts/scanners/concepts_have_owns.py
impact: HIGH
---

## Every concept must have decision ownership

The scanner (`scripts/scanners/concepts_have_owns.py`) flags concepts that violate this rule. Borderline wording is resolved in assessment.

**DO** ensure every concept has an `owns` field — one sentence stating what **decision or rule** this concept owns (not a restatement of the name, not vague marketing text).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PriceBook",
            "owns": "Owns which list price applies for a SKU in a channel and effective date range",
            "owns_chunk": "chunk-retail-12",
            "chunk_ids": ["chunk-retail-12"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "owns": "Owns the target number an attack roll must meet or beat to hit",
            "owns_chunk": "chunk-srd-combat-3",
            "chunk_ids": ["chunk-srd-combat-3"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Telco",
        "concepts": [
          {
            "name": "ServiceOrder",
            "owns": "Owns lifecycle state transitions for install or repair orders until closed",
            "owns_chunk": "chunk-telco-ord-1",
            "chunk_ids": ["chunk-telco-ord-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** leave a concept with only `chunk_ids` and no decision ownership. A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun in the source.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PriceBook",
            "chunk_ids": ["chunk-retail-12"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** set `owns` to the concept name or other non-decision text.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "owns": "ArmorClass",
            "owns_chunk": "chunk-srd-combat-3",
            "chunk_ids": ["chunk-srd-combat-3"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```


---

---
rule_id: stories-must-have-trigger-response
phases: [step1]
order: 20
scanner: scripts/scanners/stories_have_trigger_response.py
impact: HIGH
---

## Stories must express actor → system interaction

A story is not a feature title alone. It is a minimal interaction: something an actor does (trigger) and how the system responds (response). Without both, the story cannot be validated, traced to evidence, or tested.

The scanner (`scripts/scanners/stories_have_trigger_response.py`) checks that `trigger` and `response` are populated and non-trivial.

**DO** write `trigger` and `response` as sentences. Use `**Actor**` / `**System**` and `**Concept**` bolding where domain concepts participate, matching how they appear under `epic.stories[]` or `epic.sub_epics[].stories[]` in `map-model-spec.json`.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Checkout",
        "stories": [
          {
            "name": "Price basket with promotions",
            "trigger": "**Cashier** adds **LineItem** rows to **Cart**",
            "response": "**System** applies **Promotion** rules and refreshes **Cart** totals"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire",
        "stories": [
          {
            "name": "Submit wire transfer",
            "trigger": "**Customer** submits **WireTransfer** instruction",
            "response": "**System** runs **LimitChecker** and queues **SettlementBatch** when allowed"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Combat", "concepts": [] },
      "epic": {
        "name": "Attacks",
        "stories": [
          {
            "name": "Resolve attack",
            "trigger": "**Player** declares **Attack** against **Creature**",
            "response": "**System** compares the roll to **ArmorClass** and applies **Damage** on a hit"
          }
        ]
      }
    }
  ]
}
```

**DO NOT** leave `trigger` or `response` empty, or fill them with titles only.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Checkout",
        "stories": [{ "name": "Checkout" }]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire",
        "stories": [
          {
            "name": "Wire transfer",
            "trigger": "User stuff",
            "response": "It works"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Combat", "concepts": [] },
      "epic": {
        "name": "Combat",
        "stories": [
          {
            "name": "Combat",
            "trigger": "Combat",
            "response": "Resolved"
          }
        ]
      }
    }
  ]
}
```


---

---
rule_id: domain-interaction-sync
phases: [step1, step2, step3, step5]
order: 40
scanner: scripts/scanners/domain_interaction_sync.py
impact: HIGH
---

## Domain names in stories must match concepts

Stories use `**Concept**` bolding to name domain participants. Those names must resolve to concepts in the module — or the story cannot be traced to the model.

The scanner (`scripts/scanners/domain_interaction_sync.py`) checks that bolded names in `epic.statement`, `epic.pre_condition`, and each story's `trigger` / `response` exist as concept names (or aliases) under the paired module.

**DO** use the same spelling and casing as `module.concepts[].name` (or list the term under `aliases`).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items and running totals before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          },
          {
            "name": "Promotion",
            "owns": "Owns which discount rules apply to a cart line",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": {
        "name": "Apply promotions",
        "statement": "**Cashier** adds rows to **Cart**; **System** evaluates **Promotion** rules.",
        "statement_chunk": "chunk-r1",
        "stories": [
          {
            "name": "Stacking rules",
            "trigger": "**Cashier** adds a second **Promotion** to **Cart**",
            "response": "**System** applies stacking policy and refreshes **Cart** totals"
          }
        ]
      }
    }
  ]
}
```

**DO NOT** bold names that do not exist on concepts (unless they are actors like **Customer** — actors are not required to be concepts).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": {
        "name": "Apply promotions",
        "statement": "**System** evaluates **PromoEngine** against **Cart**.",
        "statement_chunk": "chunk-r1",
        "stories": []
      }
    }
  ]
}
```

`PromoEngine` is bolded but no concept (or alias) — violation.

**DO NOT** rename concepts in stories without updating `concepts[]` (or aliases).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "aliases": [],
            "owns": "Owns the target number to hit",
            "owns_chunk": "chunk-srd-1",
            "chunk_ids": ["chunk-srd-1"]
          }
        ]
      },
      "epic": {
        "name": "Resolve hits",
        "statement": "**System** compares roll to **AC**.",
        "statement_chunk": "chunk-srd-1",
        "stories": []
      }
    }
  ]
}
```

`AC` is not `ArmorClass` and is not listed under `aliases` — violation.

Fix in scaffold (alias) or story text:

```json
{
  "name": "ArmorClass",
  "aliases": ["AC"],
  "owns": "Owns the target number to hit",
  "owns_chunk": "chunk-srd-1",
  "chunk_ids": ["chunk-srd-1"]
}
```


---

---
rule_id: hierarchy-approximately-4-to-9-children
phases: [step1]
order: 30
scanner: scripts/scanners/hierarchy_sizing.py
impact: MEDIUM
---

## Epic tree sizing (4–9 children per level)

The story map should be navigable: neither a flat pile nor an over-nested hairball. Target roughly **4–9** children at each level (`epic.sub_epics`, `sub_epic.stories`, or `epic.stories` when there are no sub-epics).

The scanner (`scripts/scanners/hierarchy_sizing.py`) warns when a node has fewer than 4 or more than 9 children. It does not block the pipeline — judgment belongs to assessment.

**DO** group related stories under sub-epics so each level stays in range.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Retail checkout",
        "sub_epics": [
          {
            "name": "Cart and pricing",
            "stories": [
              { "name": "Add line", "trigger": "…", "response": "…" },
              { "name": "Apply promo", "trigger": "…", "response": "…" },
              { "name": "Recalculate tax", "trigger": "…", "response": "…" },
              { "name": "Hold for manager", "trigger": "…", "response": "…" }
            ]
          },
          {
            "name": "Payment capture",
            "stories": [
              { "name": "Card auth", "trigger": "…", "response": "…" },
              { "name": "Partial auth", "trigger": "…", "response": "…" },
              { "name": "Decline path", "trigger": "…", "response": "…" },
              { "name": "Receipt", "trigger": "…", "response": "…" }
            ]
          }
        ]
      }
    }
  ]
}
```

**DO NOT** put twenty-five sibling stories directly under one epic with no sub-epics.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Fulfillment", "concepts": [] },
      "epic": {
        "name": "Order fulfillment",
        "stories": [
          { "name": "Story 01", "trigger": "…", "response": "…" },
          { "name": "Story 02", "trigger": "…", "response": "…" },
          { "name": "Story 03", "trigger": "…", "response": "…" },
          { "name": "Story 04", "trigger": "…", "response": "…" },
          { "name": "Story 05", "trigger": "…", "response": "…" },
          { "name": "Story 06", "trigger": "…", "response": "…" },
          { "name": "Story 07", "trigger": "…", "response": "…" },
          { "name": "Story 08", "trigger": "…", "response": "…" },
          { "name": "Story 09", "trigger": "…", "response": "…" },
          { "name": "Story 10", "trigger": "…", "response": "…" },
          { "name": "Story 11", "trigger": "…", "response": "…" },
          { "name": "Story 12", "trigger": "…", "response": "…" }
        ]
      }
    }
  ]
}
```

Twelve direct children — scanner warns (too wide).

**DO NOT** nest single-child chains (`A → B → C` each with one child) unless the corpus truly decomposes that way — flatten or merge.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Example", "concepts": [] },
      "epic": {
        "name": "Level A",
        "sub_epics": [
          {
            "name": "Level B",
            "sub_epics": [
              {
                "name": "Level C",
                "stories": [{ "name": "Only story", "trigger": "…", "response": "…" }]
              }
            ]
          }
        ]
      }
    }
  ]
}
```

Deep single-child chain — scanner warns.


---
