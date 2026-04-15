# Step 1 — Discover Modules and Epics (v3)

## Purpose

Orient yourself in the corpus. Discover the major areas of the domain and produce a paired list of **modules** (domain view) and **epics** (interaction view). Every field you populate must be supported by a chunk you read. If you have no chunk, leave the field blank.

This is orientation, not modeling. Concepts get sketched — not designed. Stories get named — not detailed. The structure you produce here is the scaffold that Steps 2 and 3 will fill in.

---

## Inputs

- `context/context_chunks.json`

---

## Sampling Strategy

Read **30% of chunks** spread evenly: divide into thirds (beginning, middle, end), read 10% from each third. Do not read sequentially from the start.

---

## Core Constraints (apply throughout)

**On domain concepts:**
- Do not go from nouns to classes. A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun.
- Only name a concept if a chunk shows it doing something: making a decision, enforcing a rule, holding state that matters, or participating in a resolution.
- Tag a concept `[foundational]` if it appears across multiple chunks and multiple mechanisms — it is a stable core that everything else depends on.

**On epics and stories:**
- Epic and story names are verb-noun. Active, base verb form. Actor is NOT in the name.
  - Right: "Resolve Check", "Build Character", "Apply Effect"
  - Wrong: "Check Resolution", "Character Building", "Player Resolves Check"
- Every epic name must reference at least one concept from its paired module using `**Concept**` notation.
- A story is the smallest independently testable behavior — it has an actor, an action, and an observable outcome. "Serialize to JSON" is not a story. "Apply Damage Effect" is.
- At this step, stories get a name and a one-line trigger + response only. No triggering-state, resulting-state, failure-modes, or steps yet.

---

## What to Produce Per Module/Epic Pair

### Domain view — Module

**Name:** noun phrase

**Description:** one sentence — what mechanism this area centers on. Evidence: cite chunk_id.

**Concept candidates:** only concepts evidenced by chunks you read. For each:

```
**ConceptName** [foundational if applicable]
- <property: type> — chunk: id  (only if evidenced)
- <operation()> — chunk: id  (only if evidenced)
- Owns: one sentence on what decision or rule this concept owns — chunk: id
```

Property types: String, Number, Boolean, List\<T\>, Dictionary\<K,V\>, EnumType {val1, val2}, UniqueID, Instant.  
Use Dictionary\<K,V\> when items are accessed by key. Use List\<T\> only when order matters.  
Leave property/operation lines blank if you have no chunk evidence for them. A concept with only a name and an "Owns" sentence is fine at this step.

**`chunk_ids`** — every concept has a `chunk_ids` list. This is the set of chunks where **this concept is the primary subject** of the text. Rules:
- Include the `owns_chunk`
- Include any chunk cited on a property or operation **where this concept is the focus of that chunk** — not where it is merely mentioned as a collaborator
- Do NOT include chunks that are primarily about another concept and only reference this one in passing — those stay on the property citation only
- Deduplicate
- This list is used to build the reverse index (chunk → concepts) so Step 2 knows exactly which chunks to read for each concept

### Interaction view — Epic

**Name:** verb-noun. `**Concept**` grounded.

**Statement:** scope of the epic — the broad flows it encompasses, not a single story. Format: `**Actor** does X across **Concept** flows; **System** responds with **Outcome**.` — chunk: id

**Triggering-Actor:** who starts interactions in this epic

**Responding-Actor:** who responds (typically System)

**Pre-Condition:** what must be true before any story in this epic can run. Given/And format. Reference concepts. Only include if a chunk supports it — chunk: id

**Stories:** 3–7 per epic. For each story:
```
Story: Verb Noun — chunk: id
- Trigger: **Actor** does X with **Concept**
- Response: **System** does Y → **Outcome**
```
Only populate trigger/response if a chunk shows the interaction. Name-only is acceptable if you identified the story but haven't read its detail chunk.

---

## Chunk Indexing

Index chunks as you discover them — do not defer. Three buckets per pair:

- **identified** — chunk clearly belongs here; also cited inline on the field it supports
- **provisional** — chunk seems related but specific concept/story not yet clear
- **ambiguous** — chunk may belong here or to another module

---

## Flagging Incomplete Understanding

When you encounter something you cannot fully name or resolve from the chunks you read, flag it explicitly rather than leaving it blank or guessing.

Use these markers inline on any concept, property, story, or module boundary:

**`[defer]`** — evidence exists that this thing exists, but not enough to model it yet. Record the chunk that shows it. Step 2 will do a targeted read.
Example: `Effect subtypes [defer] — chunk: 2b9b77a24290`

**`[uncertain]`** — evidence exists but the boundary or ownership is unclear. State the question explicitly. Requires human confirmation before Step 2 proceeds on it.
Example: `Skills [uncertain] — sub-module of Character Traits or separate? chunk: 94d3158e4b6b`

**`[cross-cutting]`** — this concept or mechanic appears in multiple modules. Do not assign it to one module yet. List all the modules it touches.
Example: `PowerLevel [cross-cutting] — Character (budget) + Powers (cap enforcement)`

**Rules:**
- `[defer]` and `[uncertain]` items appear in the `open_questions` array in the JSON output
- `[cross-cutting]` items appear in `cross_cutting_notes`
- Never omit a flag to keep output clean — an unflagged gap is invisible to Step 2

---

## Orient First, Then Classify

**Pass 1 — Read without classifying.** What are the major mechanisms? What are actors doing and to what? What enforces rules? What has lifecycle? What cross-cuts everything?

**Pass 2 — Name pairs.** One module/epic pair per distinct area. Test: does the module have at least one concept that owns a real decision? Does the epic have at least one story a developer could build and test independently?

**Pass 3 — Index evidence.** Assign chunk_ids to everything you named. Anything with no chunk goes to provisional.

---

## Output

Two files:

### `test/experiment/step1-output-v2.json`

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
            "owns": "One sentence on what decision or rule this concept owns.",
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
        "stories": [
          {
            "name": "Verb Noun",
            "chunk": "chunk_id",
            "trigger": "**Actor** does X with **Concept**",
            "response": "**System** does Y → **Outcome**"
          }
        ]
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

### `test/experiment/step1-readable-v2.md`

One section per pair. Format:

```markdown
## Module: Name | Epic: Verb Noun

**Module:** Description. (chunk: id)

**Concepts:**
- **ConceptName** [foundational] — Owns: what it decides. (chunk: id)
  - Number rank (chunk: id)
  - resolve() → Degree (chunk: id)

**Epic:** Statement (chunk: id)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Concept** is X (chunk: id)

**Stories:**
- Story: Verb Noun (chunk: id)
  - Trigger: **Actor** does X with **Concept**
  - Response: **System** does Y → **Outcome**

**Chunk index:** identified: [ids] | provisional: [ids] | ambiguous: [ids]
```

---

## Stop for Review

After writing both files, stop. Present the readable summary. Ask:

1. Does this list capture all major areas of the corpus?
2. Are any pairs wrong or misnamed?
3. Are any pairs missing?
4. Are any concept candidates data bags with no real decision ownership?
5. Any areas where you had no chunk evidence and guessed?
