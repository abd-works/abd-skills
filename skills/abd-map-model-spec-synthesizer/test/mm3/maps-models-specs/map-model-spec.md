# Step 1 — Discover Modules and Epics

## Purpose

Orient yourself in the corpus. Discover the major areas of the domain and produce a paired list of **modules** (domain view) and **epics** (interaction view). Every field you populate must be supported by a chunk you read. If you have no chunk, leave the field blank or use a flag.

This is orientation, not modeling. Concepts get sketched — not designed. The epic confirms that the module has real interactions — but stories are a sanity check, not the deliverable. The structure you produce here is the scaffold that Steps 2 and 3 will fill in.

---

## Inputs

- `context/context_chunks.json`

---

## Sampling Strategy

Read **30% of chunks** spread evenly: divide into thirds (beginning, middle, end), read 10% from each third. Do not read sequentially from the start.

---

## Core Constraints

These are the fundamental principles that govern everything you produce. Read them before you read a single chunk.

**On domain concepts:**
- A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun.
- Only name a concept if a chunk shows it doing something: making a decision, enforcing a rule, holding state that matters.
- Tag `[foundational]` if the concept appears across multiple chunks and multiple mechanisms — it is a stable core everything else depends on.
- `chunk_ids` on a concept = chunks where this concept is the **primary subject**. Property-level `chunk` = the specific chunk that evidenced that property. Both are distinct and both matter.

**On modules:**
- A module groups concepts that collaborate around the same mechanism.
- Module boundaries come from mechanical evidence — what things do together — not from document structure or chapter layout.

**On epics:**
- An epic is the interaction-side name for a module's functional area.
- Epic names are verb-noun, grounded in at least one `**Concept**` from the paired module.
- The epic statement describes scope — the broad flows the epic encompasses — not a single interaction.
- 2–3 story names confirm the epic is real and coherent. Stories are a sanity check. You are not trying to enumerate or detail them.

---

## Flagging Incomplete Understanding

When you cannot fully resolve something from the chunks you read, flag it explicitly. Never leave a gap unflagged — an unflagged gap is invisible to Step 2.

**`[defer]`** — evidence exists that this thing exists, but not enough to model it yet. Record the chunk. Step 2 will do a targeted read.

**`[uncertain]`** — evidence exists but the boundary or ownership is unclear. State the question explicitly. Requires human confirmation before Step 2 proceeds on it.

**`[cross-cutting]`** — this concept or mechanic appears in multiple modules. Do not assign it to one module yet. List all modules it touches.

`[defer]` and `[uncertain]` items collect in `open_questions` in the JSON output. `[cross-cutting]` items collect in `cross_cutting_notes`.

---

## Orient First, Then Classify

**Pass 1 — Read without classifying.** What are the major mechanisms? What are actors doing, and to what? What enforces rules? What has lifecycle? What cross-cuts everything?

**Pass 2 — Name pairs.** One module/epic pair per distinct area. Test: does the module have at least one concept that owns a real decision and has chunk evidence? Can you name 2 stories that confirm the epic is real?

**Pass 3 — Index evidence.** Assign chunk_ids to everything you named. Anything with no chunk goes to provisional or gets flagged.

---

## Rules

These rules apply after you have oriented yourself. Rules with a scanner are mechanically enforced in Pass 1. Rules without a scanner are enforced in the adversarial validation pass (Pass 3).

Full rule files: `test/experiment/rules/`

---

### Mechanics from evidence, not document structure
*(AI-only — no scanner)*

**DO** derive modules and epics from mechanics you observe — what things do, what decisions they enforce, what resolution patterns they follow.

**DO NOT** name a module after a chapter title, section header, or ToC entry.

- Wrong: Module "Chapter 3: Abilities". Right: Module "Character Traits" — because Abilities, Skills, and Defenses share the same PP cost and PL constraint mechanic.

---

### All concepts must have chunk evidence
*Scanner: `scan_chunks_must_be_referenced.py` → Rule: `chunks-must-be-referenced.md`*

**DO** ensure every concept has at least one `chunk_id`. **DO** cite a chunk on every property, operation, `owns`, module description, and epic statement.

**DO NOT** name a concept or populate a field without chunk evidence. Use `[defer]` if evidence exists but was not fully read.

---

### No junk concept names
*Scanner: `scan_no_junk_concepts.py` → Rule: `no-junk-concepts.md`*

**DO NOT** use section headers, all-caps document labels, proper nouns, instruction phrases, or truncations as concept names.

Reject: "THE BASICS", "POWERS", "Paragon", "Speedster", "Choose One", "Insub".

**DO** name concepts as domain nouns that hold state or own decisions: "Check", "Ability", "PowerLevel", "Condition".

---

### No duplicates
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO NOT** have two concepts with the same name within a module. **DO NOT** have two modules with the same name across the output.

---

### No speculation — flag instead
*(AI-only — no scanner)*

**DO NOT** invent mechanics not present in chunks you read. **DO** use `[defer]`, `[uncertain]`, or `[cross-cutting]` flags. An unflagged gap is a silent error.

- Right: `ExtraEffort [defer] — chunk: 4cd63373be61`
- Wrong: Populating properties from prior knowledge without a chunk citation.

---

### Classify variants before modeling
*(AI-only — no scanner → Rule: `classify-variants-before-modeling.md`)*

When you encounter variant families, classify them — do not model them yet.

- Different mechanics per variant → subtype candidate → flag `[defer]`
- Same mechanic, different label → enum → `EnumType {val1, val2}` on parent concept

**DO NOT** create subtype concepts or hierarchy entries at Step 1.

---

### Verb-noun format for epics and story names
*(AI-only — no scanner)*

**DO** name epics and confirming stories as verb-noun. Actor NOT in the name. Active, base verb form.

- Right: "Resolve Check", "Build Character", "Apply Effect"
- Wrong: "Check Resolution", "Character Building", "Player Resolves Check"

---

### Epics must have confirming stories
*Scanner: `scan_epic_requires_confirming_stories.py` → Rule: `epic-requires-confirming-stories.md`*

**DO** include at least 2 story names in `confirming_stories` per epic. Stories confirm the epic is real — they are not the deliverable.

**DO** name a confirming story only if it describes a complete, independently testable behavior with an observable outcome.

- Wrong: "Serialize Character to JSON", "Calculate PP total"
- Right: "Validate Character Sheet", "Build Power Array"

---

## What to Produce Per Module/Epic Pair

### Domain view — Module

```
name: noun phrase
description: one sentence — what mechanism this area centers on (chunk: id)

concepts:
  ConceptName [foundational if applicable]
    chunk_ids: [ids where this concept is the primary subject]
    owns: one sentence on what decision or rule this concept owns (chunk: id)
    properties:
      - type definition (chunk: id)   ← only if evidenced
    operations:
      - signature (chunk: id)          ← only if evidenced
```

Property types: String, Number, Boolean, List\<T\>, Dictionary\<K,V\>, EnumType {val1, val2}, UniqueID, Instant.
Dictionary\<K,V\> when items accessed by key. List\<T\> only when order matters.

### Interaction view — Epic

```
name: Verb Noun (grounded in **Concept**)
statement: **Actor** does X across **Concept** flows; **System** responds. (chunk: id)
triggering_actor: who starts
responding_actor: who responds
pre_condition: Given **Concept** is X (chunk: id)   ← only if evidenced

confirming_stories: ["Verb Noun", "Verb Noun"]   ← names only; confirms epic is real
```

Story names only. No trigger/response, no chunk required per story. If you have a story chunk, record it in the module's `chunk_ids.provisional` bucket.

---

## Chunk Indexing

Index as you discover — not deferred. Three buckets per module/epic pair:
- **identified** — chunk clearly belongs here; also cited inline on the field it supports
- **provisional** — chunk seems related but the specific concept or story is not yet clear
- **ambiguous** — chunk may belong here or to another module

---

## Output

Two files, then run the index script. Step 1 creates `output.json`; Step 2 deepens it; Step 3 canonicalizes it.

### `test/experiment/output.json`

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Module Name",
        "description": "One sentence.",
        "description_chunk": "chunk_id",
        "concepts": [
          {
            "name": "ConceptName",
            "foundational": true,
            "chunk_ids": ["chunk_id_1", "chunk_id_2"],
            "owns": "One sentence on what this concept owns.",
            "owns_chunk": "chunk_id",
            "properties": [
              { "definition": "Number rank", "chunk": "chunk_id" }
            ],
            "operations": [
              { "definition": "resolve() → Degree", "chunk": "chunk_id" }
            ]
          }
        ]
      },
      "epic": {
        "name": "Verb Noun",
        "statement": "**Actor** does X across **Concept** flows; **System** responds.",
        "statement_chunk": "chunk_id",
        "triggering_actor": "Player",
        "responding_actor": "System",
        "pre_condition": "Given **Concept** is in state X",
        "pre_condition_chunk": "chunk_id",
        "confirming_stories": ["Verb Noun One", "Verb Noun Two"]
      },
      "chunk_ids": {
        "identified": ["chunk_id"],
        "provisional": ["chunk_id"],
        "ambiguous": ["chunk_id"]
      }
    }
  ],
  "open_questions": [],
  "cross_cutting_notes": ""
}
```

### `test/experiment/readable.md`

One section per pair:

```markdown
## Module: Name | Epic: Verb Noun

**Module:** Description. (chunk: id)

**Concepts:**
- **ConceptName** [foundational] — Owns: what it decides. (chunk: id)
  - chunk_ids: [id1, id2]
  - Number rank (chunk: id)
  - resolve() → Degree (chunk: id)

**Epic:** Statement (chunk: id)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Concept** is X (chunk: id)
- Confirming stories: Verb Noun One, Verb Noun Two

**Chunk index:** identified: [ids] | provisional: [ids] | ambiguous: [ids]
```

---

## After Generation — Three Quality Passes

### Pass 1 — Scanners (code)

Run all four scanners immediately after writing the JSON output. Each scanner corresponds to one rule file in `test/experiment/rules/`. Scanners highlight gaps — the AI determines whether each violation is a genuine gap, false positive, or needs a `[defer]` flag.

```
python test/experiment/scripts/scan_chunks_must_be_referenced.py --input test/experiment/output.json
python test/experiment/scripts/scan_no_duplicates.py --input test/experiment/output.json
python test/experiment/scripts/scan_epic_requires_confirming_stories.py --input test/experiment/output.json
python test/experiment/scripts/scan_no_junk_concepts.py --input test/experiment/output.json
```

| Scanner | Rule file | What it checks |
|---|---|---|
| `scan_chunks_must_be_referenced.py` | `chunks-must-be-referenced.md` | Every evidence claim cites a chunk |
| `scan_no_duplicates.py` | `no-duplicates.md` | No duplicate concept or module names |
| `scan_epic_requires_confirming_stories.py` | `epic-requires-confirming-stories.md` | Every epic has at least 2 confirming story names |
| `scan_no_junk_concepts.py` | `no-junk-concepts.md` | No section headers, proper nouns, or instruction phrases as concept names |

Review each violation. Fix, flag `[defer]`, or document as false positive. Re-run until all scanners report `PASS`.

### Pass 1b — Update junk config (AI)

After running the scanners, if you encountered section headers, chapter labels, or proper nouns (character/setting names) while reading chunks that are not already in `junk_config.json`, add them now:

- `test/mm3/solution/generated/junk_config.json` — solution-specific junk terms
- Add to `section_headers` for ToC labels and chapter names found in this corpus
- Add to `proper_nouns` for character names, setting names, organization names
- Add to `additional_junk` for anything else that is clearly not a domain concept

The scanner will pick these up on the next run. This file is cumulative — add to it, never remove unless confirmed false positive.

### Pass 2 — Build chunk index (code)

```
python test/experiment/scripts/build_chunk_index.py --input test/experiment/output.json --output test/experiment/chunk-index.json
```

### Pass 3 — Adversarial validation (AI)

Re-read `output.json` against each rule as a checklist. Be adversarial — look for violations the scanner cannot catch:

- Any module name derived from a chapter title or ToC entry?
- Any concept name that is a section header, proper noun, or single common word?
- Any concept with `owns` that is just restating its name rather than declaring a decision?
- Any `[defer]` gap that should have been flagged but wasn't?
- Any confirming story that is an implementation step rather than a testable behavior?
- Any enum decision that should be a subtype candidate (or vice versa)?

Report each violation with: rule name, location in JSON, proposed fix. Fix all violations. Re-read until clean.

---

## Stop for Review

Present the readable summary (`readable.md`) and ask:

1. Does this list capture all major areas of the corpus?
2. Are any module/epic pairs wrong or misnamed?
3. Are any pairs missing?
4. Are any concept candidates data bags with no real decision ownership?
5. Any areas where you had no chunk evidence and guessed rather than flagged?
6. Are any `[defer]` flags wrong — should they be modeled now?
