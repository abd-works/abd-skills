# Step 2 — Deepen Concepts and Stories Per Module/Epic

## Purpose

Take the module/epic pairs from Step 1 and deepen them. For each module/epic pair: (1) deepen concepts with full properties, operations, invariants; (2) deepen stories to Trigger, Response, Pre-Condition, Failure-Modes; (3) add hierarchy (sub-epics, concept relationships); (4) resolve all `[defer]` flags via targeted chunk reads.

**Domain and interaction stay in sync.** Concepts participate in stories as callers/receivers; state flows through Pre-Condition, Triggering-State, Resulting-State. When you add or revise an interaction, derive or update concepts accordingly. Do not edit one view without the other.

Epics come from context. Keep ~4–9 children per node. Use representative examples to illustrate structure; do not enumerate every variant. Derive domain from interactions.

---

## Inputs

- `output.json` — the evolving output (Step 1 created it; Step 2 deepens it)
- `chunk-index.json` — reverse index: which chunks to read per module/epic
- `context/context_chunks.json` — full corpus; read only chunks listed in the index for each pair
- `open_questions` and `cross_cutting_notes` in output.json — resolve or re-flag

---

## Chunk Strategy Per Module/Epic

**Discrete, dedicated passes.** Each module/epic pair is processed in a **single, self-contained pass**. No interleaving. No mixing context from one pair into another. Complete one pair fully — deepen concepts, deepen stories, sync — before starting the next.

**One pass = one pair.** For each pass:

1. **Read identified chunks** — from `chunk_ids.identified` in output.json for this pair only
2. **Read provisional chunks** — from `chunk_ids.provisional` in output.json for this pair only; these often hold story or concept detail
3. **Read deferred chunks** — for any `[defer]` item in this pair, read the cited chunk and resolve
4. **Do not re-sample** — use the index. The output already decided what belongs where.
5. **Update output.json** — write the deepened pair back into output.json. Do not carry forward in-memory context to the next pass.

**Process ordering:** Process module/epic pairs by importance to core mechanics. Core resolution/flow first; setup, config, peripheral last.

**Enforcement:** When running in an environment that supports it, invoke a sub-agent or fresh session per pair to guarantee context isolation. If not, treat each pass as a distinct invocation: load only the pair and its chunks; produce only that pair's deepened output; then start the next pair from the aggregate so far.

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

**On domain–interaction sync:**
- Concepts participate as callers/receivers in stories. State flows through Pre-Condition, Triggering-State, Resulting-State.
- **DO NOT** edit only the Interaction Tree and skip the Domain Model. Interaction changes often imply concept changes.
- Example (right): Epic "Make Checks" has inline Concepts: `Check: targetNumber, roll(dice): Result`; `DifficultyClass: value`. After revising an interaction that touches CheckResult, add CheckResult to both.

---

## Flagging

**`[defer]`** — resolved in Step 2 by targeted read. If still unresolved after read, keep in `open_questions` with reason.

**`[uncertain]`** — requires human confirmation. Do not proceed on it without confirmation.

**`[cross-cutting]`** — remains in `cross_cutting_notes` until Step 3. Do not assign to one module yet.

---

## Process Per Module/Epic Pair

**Pass 1 — Resolve deferrals.** For each `[defer]` in this pair, read the cited chunk. Decide: subtype vs enum.

**Pass 2 — Deepen concepts.** From interactions and stories: add properties, operations, invariants. Derive from evidence; do not invent.

**Pass 3 — Deepen stories.** Add Trigger, Response, Pre-Condition, Failure-Modes. Ground in `**Concept**`. Group into sub-epics if needed (~4–9 children).

**Pass 4 — Sync.** Ensure every concept in the module appears in at least one story. Ensure every story references a concept. Update domain model if interaction changes.

---

## Rules

These rules apply after you have deepened each pair. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `test/experiment/rules/`

---

### Chunks must be referenced (reuse)
*Scanner: `scan_chunks_must_be_referenced.py` → Rule: `chunks-must-be-referenced.md`*

**DO** ensure every concept, property, operation, story, trigger, response, pre-condition has chunk evidence.

**DO NOT** populate a field without evidence. Use `[defer]` if evidence exists but was not fully read.

---

### No duplicates (reuse)
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO NOT** have two concepts with the same name within a module. **DO NOT** have two modules with the same name.

---

### Epic requires confirming stories (reuse)
*Scanner: `scan_epic_requires_confirming_stories.py` → Rule: `epic-requires-confirming-stories.md`*

**DO** include at least 2 story names per epic. At Step 2, stories have full Trigger/Response; confirming_stories is the list of story names.

---

### No junk concepts (reuse)
*Scanner: `scan_no_junk_concepts.py` → Rule: `no-junk-concepts.md`*

**DO NOT** use section headers, all-caps labels, proper nouns, instruction phrases as concept names.

---

### Concepts must have owns
*Scanner: `scan_concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field — one sentence on what decision or rule this concept owns.

**DO NOT** leave a concept with only chunk_ids and no decision ownership.

---

### Stories must have trigger and response
*Scanner: `scan_stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has `trigger` (Actor + action) and `response` (system or other actor).

**DO NOT** leave a story with only a name. Trigger and response ground the story in domain.

---

### Domain–interaction sync
*Scanner: `scan_domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept in the module participates in at least one story (trigger, response, or pre-condition).

**DO NOT** have orphan concepts — concepts that appear in the domain model but in no story.

---

### Hierarchy sizing (approximately 4–9 children)
*Scanner: `scan_hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range for manageable granularity.

**DO NOT** create nodes with many more than 9 children — split or regroup.

---

### Derive concepts from interactions (AI-only)
*(AI-only — no scanner)*

**DO** derive properties and operations from interactions and stories.

**DO NOT** invent collaborators or relationships not present in source material.

---

### Representative examples, not enumeration (AI-only)
*(AI-only — no scanner)*

**DO** use representative examples that illustrate the structure.

**DO NOT** enumerate every possible variant. Classify; defer subtype modeling if needed.

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

### `test/experiment/output.json` (updated)

Same shape as before, but with:
- Concepts: full properties, operations, invariants, relationships
- Stories: trigger, response, pre_condition, failure_modes
- Sub-epics where needed
- `open_questions` and `cross_cutting_notes` updated (resolved items removed)

### `test/experiment/readable.md` (updated)

One section per pair, with full concept and story detail.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

Run all Step 1 scanners plus Step 2 scanners:

```
python test/experiment/scripts/scan_chunks_must_be_referenced.py --input test/experiment/output.json
python test/experiment/scripts/scan_no_duplicates.py --input test/experiment/output.json
python test/experiment/scripts/scan_epic_requires_confirming_stories.py --input test/experiment/output.json
python test/experiment/scripts/scan_no_junk_concepts.py --input test/experiment/output.json
python test/experiment/scripts/scan_concepts_have_owns.py --input test/experiment/output.json
python test/experiment/scripts/scan_stories_have_trigger_response.py --input test/experiment/output.json
python test/experiment/scripts/scan_domain_interaction_sync.py --input test/experiment/output.json
python test/experiment/scripts/scan_hierarchy_sizing.py --input test/experiment/output.json
```

| Scanner | Rule file | What it checks |
|---|---|---|
| `scan_chunks_must_be_referenced.py` | `chunks-must-be-referenced.md` | Every evidence claim cites a chunk |
| `scan_no_duplicates.py` | `no-duplicates.md` | No duplicate concept or module names |
| `scan_epic_requires_confirming_stories.py` | `epic-requires-confirming-stories.md` | Every epic has ≥2 stories |
| `scan_no_junk_concepts.py` | `no-junk-concepts.md` | No junk concept names |
| `scan_concepts_have_owns.py` | `concepts-must-have-owns.md` | Every concept has `owns` |
| `scan_stories_have_trigger_response.py` | `stories-must-have-trigger-response.md` | Every story has trigger and response |
| `scan_domain_interaction_sync.py` | `domain-interaction-sync.md` | Every concept in at least one story |
| `scan_hierarchy_sizing.py` | `hierarchy-approximately-4-to-9-children.md` | ~4–9 children per node |

### Pass 2 — Build chunk index (code)

```
python test/experiment/scripts/build_chunk_index.py --input test/experiment/output.json --output test/experiment/chunk-index.json
```

### Pass 3 — Adversarial validation (AI)

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
4. Does domain and interaction stay in sync?
