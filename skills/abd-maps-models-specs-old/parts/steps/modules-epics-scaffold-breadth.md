# Modules and epics scaffold (K-read breadth)

## Your role

You are a **domain modeler** and a **story mapper**. In this step **you** figure out the **foundational model** of the system and the **epics and stories** that can **realize** those foundational components. **You** also build a working sense of **what other modules, epics, and downstream work** will **use or depend on** those foundational pieces — so **you** are not modeling in a vacuum.

Everything below is **what you must do** to finish this step.

---

**Where this sits:** **`parts/process.md`** — **Stage 2: Map and Model**, process table **row 5 — Modules and Epics** (this document: **modules/epics scaffold (breadth)** / K-read breadth). **Row 4 — Foundational mechanisms** (foundational spine) must be done first (**`parts/steps/built/modules-epics-foundational-spine.md`**). That pass gives **you** the **concept-first spine**; in breadth **you** substantiate and expand **`concepts[]`** — **you do not** substitute epic lists for understanding.

## What you must achieve (non-negotiable)

**Your main success** is a **refined set of modules and epics**, **domain concepts**, and **stories** developed enough to cover the **foundational, cross-cutting mechanisms** of the solution. **You must** finish able to **(1)** **go deeper into detailed design later** without inventing structure from scratch, and **(2)** **see where dependencies run** between areas of the model. **Do not** sub-optimize on a thin set of concepts — a model that looks small but **conceals** what still must be named, owned, and connected, so **you** lose track of what to flesh out next.

### Overarching outcome (what this step is for)

**Recording.** You persist the outcome in **`map-model-spec.json`**. Per module/epic pair:

- You **cite** **`module.concepts[]`**: names, **`owns`** + **`owns_chunk`**, **`chunk_ids`** / evidence, **`evidence_stage`**, **`extends`**, optional **`properties`[] / `operations`[]** with **`chunk`**
- You **define** **`module.depends_on`** for provider/consumer relationships
- You **align** epics and **`confirming_stories`** with that model

**§2** is the field checklist — not a second workflow.

**Foundational object model.**

- You **grow** each pair’s **`module.concepts[]`**
- You **anchor** claims to chunks
- You **layer** base → categories → implementations
- You promote **`evidence_stage`** toward **`scaffolded`** only where **full reads** substantiate the claims
- You **edit** concepts **before** epics

**Module dependencies.**

- You make **wiring visible**
- You define **`module.depends_on`** between provider and consumer modules
- You define **concept-to-concept** shape (**`extends`**, **owns**, cross-cutting notes)
- You connect **foundational** material to **extensions** and **categorization** — not hidden in story titles alone

**Validation through epics and stories.**

- You **prove** the model with **epics** and **`confirming_stories`**
- You **align** **`epic.statement`** and story vocabulary to **`concepts[].name`** (**bold names**, **`statement_chunk`**, chunk-tied wording)
- You **edit** concepts first, epics second
- You **lock** concept names and story strings together (**`scaffold-concept-story-name-alignment`**) — **no** story nouns without **`concepts[]`** rows

**Split work (brief).**

- You **split** work into consecutive **ranges** on the breadth-sorted id list (**sub-agents** or **batches**) when **breadth reads** are **many**
- You **merge** returned **patches** into **one** JSON (union **`chunk_ids`**, reconcile **`depends_on`**, dedupe questions) — see step **4** in **§1** for **parent** merge
- You **may** route by module/epic pair after ids are chosen

**Verification (tools) vs. modeling (the actual work).**

- **The work:** You **read** chunks and **edit** **`map-model-spec.json`** (**§1**) — concepts, epics, **`depends_on`**, chunk ties. That is what this step is **for**.
- **The checks:** **§4** scanners and **`build_chunk_index.py`** **catch** mistakes in that JSON (missing refs, duplicates, epic/story rules, index freshness). **Run them after you edit**; they **do not** read the corpus for you or decide the model.

---

## 1. What you must do (in order)

**You** follow **one** ordered list below. **You** use **§2** as the field checklist while **you** execute steps **8–12** (concepts through **`depends_on`**).

1. **Context** — **You** resolve **`context_path`** → **`context_index.json`**.
   - **You** set **N** = **`forward_index`** size
   - **You** set **K** = round(0.3×N), band ⌊0.28N⌋–⌈0.32N⌉ (if N &lt; 10, at least max(1, round(0.3×N)))
   - **You do not** store K, N, or a frozen chunk manifest in the spec

2. **Open the spec** — **You** open **`map-model-spec.json`** (foundational spine **already** present).

3. **Choose breadth reads** — **You** lexically sort chunk ids on **`forward_index`**.
   - **You** set **K** = max(1, round(0.3×N))
   - **You** pick **K** ids **spread** from first to last of the sorted list (stratified breadth — not one cluster)
   - **You** keep chosen ids in **session notes / tally**, not in JSON

4. **Optional: batches / sub-agents** — When **K** is large, **you** assign consecutive **ranges** of the sorted list to batches or sub-agents.
   - **You** collect **patches** from each batch (`modules_and_epics`, `open_questions`, `chunk_ids` buckets)
   - **You** (**parent**) **merge** into **one** JSON: union **`chunk_ids`**, reconcile **`depends_on`**, dedupe questions
   - **You may** route by module/epic pair after ids are chosen

5. **Interactive AI** — **You** read chunks and **you** edit **`map-model-spec.json`** directly (optionally with an assistant). **You** need **no** Python driver for reading/editing.

6. **Full-read pass** — **You** open **`chunks/<id>.md`** for chosen ids. **You** count **+1** only after a **full** read (**mandatory** full reads — **no** skim); **you** **stop** at **K**. When **you** split work, **you** follow step **4**.

7. **While reading** — **You** note mechanisms, actors, ownership, cross-area ties.
   - **You** map nouns to **new or existing `concepts[]`** (preferred) or **`open_questions`** / cross-cutting notes
   - **You never** map **only** to a story title

8. **Concepts first (primary)** — For each module/epic pair, **you** expand **`module.concepts[]`**. **You** satisfy **§2** domain (breadth):
   - **You** chunk-anchor every claim
   - **You** advance **`evidence_stage`**: **hypothesis → scaffolded** when **K** reads substantiate
   - **You** use **`concept.extends`** for is-a; **`properties`[] / `operations`[]** with **`chunk`** for has-a
   - **You** apply **concept layering** (base → categories → implementations)
   - **You** apply **verb/noun** module/epic/story rules **after** the concept set for the pair is honest

9. **Epics and confirming stories (secondary)**
   - **You** use **Verb Noun** epic names
   - **You** write **`statement`** with **`**Concept**`** matching **`concepts[].name`**; **`statement_chunk`**
   - **You** add optional **`pre_condition`** + **`pre_condition_chunk`**
   - **You** write **`confirming_stories`** for **every** behavior needed to **validate foundational concepts** for that epic — **as many names as required**, no upper limit; **do not** treat “two” as a default or stopping point — **using** object nouns that already appear in **`concepts[].name`**
   - If **you** need a distinct noun: **you** add the concept row in step **8**, **then** **you** name the story

10. **Concept–story name alignment** — **You** make **`concepts[].name`** and story strings (**`epic.statement`** bold names, **`confirming_stories[]`** object nouns) **match 100%** — **`scaffold-concept-story-name-alignment`**, **non-negotiable**. **Default fix:** **you** add **`concepts[]`** rows + chunks.

11. **Track chunks** — **You** record per pair in **`chunk_ids.identified` / `provisional` / `ambiguous`**.

12. **`module.depends_on`** — For each consumer module, **you** add **`depends_on`** (**`module-depends-on.md`**). **You** resolve duplicates (**`no-duplicates.md`**) first.

13. **You must** generate **`map-model-spec.md`** from **`parts/templates/map-model-spec.md.template.md`**.

14. **Scaffold scanners** — **You** run four commands (**§4**); **you** fix until **PASS**.

15. **`build_chunk_index.py`** — **You** run `python scripts/build_chunk_index.py` (config defaults or `--input` / `--output`); **you** keep **`mms-chunk-index.json`** current.

16. **Human handoff** — **You** complete the **§5** checklist.

**Rules:** **You do not** embed a pre-written **K** chunk-id list inside JSON. **You** take domain + story detail from **§2** and the baked **Rules**.

---

## 2. Reference: per-pair JSON shape (not a second workflow)

**You use** this while **you** edit **`map-model-spec.json`** in steps **8–12** in **§1**. Full narrative specs: **`parts/domain.md`**, **`parts/story-map.md`**.

*Domain (breadth JSON) — what you must satisfy:*

- **Layering:** **you** structure base → subtypes → variants (**`parts/domain.md`** *What goes in* + **`concept-layering-scaffold`** rule)
  - **is-a:** **`concept.extends`** = parent **`name`**
  - **has-a:** **`properties`[] / `operations`[]** with **`chunk`** per asserted field (**`parts/domain.md`** — *Composition vs extends* under scaffold extensions table)
- **`module.depends_on`:** **you** list providers from each consumer module (**`parts/domain.md`** + rule **`module-depends-on`**)
- **`evidence_stage`:** **you** promote to **`scaffolded`** when **K** reads substantiate the **owns** / properties / operations **you** add (**`parts/domain.md`** — *map-model-spec.json* table)

*Story map (breadth JSON) — what you must satisfy:*

- **Epic** **`name`**: Verb Noun
- **`statement`**: scope line with **`**Concept**`** for each domain noun **you** use (**`parts/story-map.md`** — *Epic* row + *Domain Grounding*)
- Optional **`epic.pre_condition`** + **`pre_condition_chunk`** when **you** assert shared given-state (**`parts/story-map.md`** — *Pre-Condition*)
- **`confirming_stories`**: one or **more** story names — as many as needed for concept validation, not a fixed pair; **you** keep names aligned with **`concepts[].name`** (**`parts/story-map.md`** — *Domain Grounding*)

**Concept layering — what you must do**

**You** structure concepts **base → categories → implementations** (see **`concept-layering-scaffold`**):

1. **Base / root** — Umbrella for the area.
2. **Categories / subtypes** — Partitions under the base.
3. **Implementations** — Concrete variants; **you** defer exhaustiveness to **concept classes and stories** unless **K** already names them.

**Evidence (core — matches `chunks_must_be_referenced`)**

- **Concept anchor (required):** **you** supply non-empty **`chunk_ids`** *or* **`chunk_evidence`** with **`chunk_id`** on each row.
- **Cite only what you claim:** **`module.description`** → **`description_chunk`**; **`concept.owns`** → **`owns_chunk`**; **properties[]** / **operations[]** → **`chunk`**; **`epic.statement`** → **`statement_chunk`**; **`epic.pre_condition`** → **`pre_condition_chunk`**.

**`evidence_stage` (on each concept)**

- **`hypothesis`** — From foundational spine or not yet substantiated by **K**.
- **`scaffolded`** — **You** substantiate during **K** reads in this step.
- **`deepened`** — After concept classes and stories (optional in JSON until then).

**Module**

- **name**, **`foundational`**, **description** + **`description_chunk`**
- **`depends_on`** (your step 12)
- **concepts** with cited **`owns`**, optional **`extends`**, optional **`properties`[] / `operations`[]** (each with **`chunk`**) per the domain excerpt above

**Epic**

- **Verb Noun** **name**
- **statement** + **chunk**; actors; optional **pre_condition** + chunk
- **confirming_stories** (≥ 1, **you** list **all** names needed to validate concepts — often **more** than two) per the story-map excerpt above

**Chunk buckets** — **you** use **identified** / **provisional** / **ambiguous** per pair.

**When unfinished** — **you** mark **`[defer]`**, **`[uncertain]`**, **`[cross-cutting]`** as before.

---

## 3. Templates (what you fill in)

**Sketch (per pair) — you mirror this shape in JSON**

```
module.name (+ foundational: true|false)
  depends_on: [...]   ← after step 12
  description (+ description_chunk if present)
  concepts: name, evidence_stage (hypothesis | scaffolded | deepened)
    chunk_ids and/or chunk_evidence
    optional: extends (parent concept name), owns (+ owns_chunk), properties[] (+ chunk), operations[] (+ chunk), foundational?: true
epic: name (Verb Noun), statement (+ statement_chunk), actors, pre_condition (+ chunk if present),
      confirming_stories: ≥1 names (as many as needed), all justified
pair chunk_ids: { identified, provisional, ambiguous }
```

**`map-model-spec.json`** (shape — illustrative)

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Module Name",
        "foundational": true,
        "description": "One sentence.",
        "description_chunk": "chunk_id",
        "depends_on": [
          {
            "dependent_concepts": ["ConceptA"],
            "module": "Other Module",
            "provides_concepts": ["BaseType"],
            "reason": "Uses shared base type; cite chunks in narrative or evidence."
          }
        ],
        "concepts": [
          {
            "name": "ConceptName",
            "foundational": true,
            "evidence_stage": "scaffolded",
            "chunk_ids": ["chunk_id_1"],
            "owns": "One sentence on what this concept owns.",
            "owns_chunk": "chunk_id",
            "properties": [
              { "definition": "Number rank", "chunk": "chunk_id" }
            ],
            "operations": [
              { "definition": "resolve() → Degree", "chunk": "chunk_id" }
            ]
          },
          {
            "name": "SubtypeConcept",
            "extends": "ConceptName",
            "evidence_stage": "scaffolded",
            "chunk_ids": ["chunk_id_subtype"],
            "owns": "Subtype-specific ownership sentence.",
            "owns_chunk": "chunk_id_subtype"
          },
          {
            "name": "LeanConcept",
            "evidence_stage": "hypothesis",
            "chunk_evidence": [
              { "chunk_id": "chunk_id_a", "evidence_type": "context", "note": "Introduces term; defer detailed owns to concept classes and stories." }
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
        "confirming_stories": ["Verb Noun One", "Verb Noun Two", "Verb Noun Three"]
      },
      "chunk_ids": {
        "identified": ["chunk_id"],
        "provisional": [],
        "ambiguous": []
      }
    }
  ],
  "open_questions": [],
  "cross_cutting_notes": ""
}
```

**`map-model-spec.md`** (optional but recommended) — **`parts/templates/map-model-spec.md.template.md`**.

---

## 4. After you write the JSON

**You run:**

```bash
python scripts/scanners/chunks_must_be_referenced.py --input <path-to-map-model-spec.json>
python scripts/scanners/no_duplicates.py --input <path>
python scripts/scanners/epic_requires_confirming_stories.py --input <path>
python scripts/scanners/no_junk_concepts.py --input <path>
```

**You** fix until **PASS**. **Then you run:**

```bash
python scripts/build_chunk_index.py
```

Detail: **`rules/`** (baked into **`parts/steps/built/modules-epics-scaffold-breadth.md`**).

---

## 5. What you must verify with a human

1. **You** confirm the foundational spine is still visible; **`hypothesis` → `scaffolded`** promotions make sense.
2. **You** confirm major material areas are represented after **K** reads.
3. **You** confirm module/epic names follow **noun / Verb Noun**; **`depends_on`** reflects real relationships.
4. **You** confirm concepts are chunk-anchored; confirming-story nouns align with concept names (or **`open_questions`** explain mismatches).
5. **You** confirm **`confirming_stories`** are complete per epic — not capped at two.
