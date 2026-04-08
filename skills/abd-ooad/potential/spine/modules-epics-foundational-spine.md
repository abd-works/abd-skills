# Foundational mechanisms (spine)

## Your role

You are a **domain modeler** and a **story mapper**. In this step **you** run a **quick pass** (no full chunk reads yet) to answer: **what are the foundational concepts** of this domain, and **how do epics and stories prove that those concepts are the right backbone?** **You** model those concepts **minimally** — enough to name them, anchor them to evidence, and say what they own when **you** assert it — then **you** write epics and confirming stories that **only** use those names. That **validates** the spine: if the story drifts to new nouns, **you** add those nouns to **`concepts[]`** (minimal, cited, hypothesis), not as orphan titles.

Module labels and epic titles **without** honest **`concepts[]`** rows are **decoration**, not a spine.

Everything below is **what you must do** to finish this step.

## What “spine” means (read this first)
**The spine is not a list of module titles and epics.** You **understand** the domain’s backbone through **`module.concepts[]`**: the named things the story will refer to (**stateful domain objects / mechanisms**), each with at least a **chunk anchor** and usually **`owns`** + **`owns_chunk`** when you assert what it owns. **Module name + epic name without an honest concept row is not a spine** — it is decoration. Epics matter for scope, but **they are meaningless if they do not verify the domain** — **`epic.statement`** must use **`**ConceptName**`** spelling that matches **`concepts[].name`** and cite **`statement_chunk`**. Epics and **`confirming_stories`** exist to **name flows over those concept names** (see **`parts/story-map.md`** *Domain Grounding*). If a confirming story implies a distinct noun, that noun **belongs in `concepts[]`** in this row (minimal, cited, **`hypothesis`**), not as orphan story text.

**Where this sits:** This is the **foundational spine** slice of **`parts/process.md`** — **before** the **modules/epics scaffold (breadth)** step (see **Built step specs**). Breadth is where **you** full-read a sample of chunks, deepen **`concepts[]`**, add **`depends_on`**, and run **`build_chunk_index.py`**. **You do none of that here.**

**What you must name:** **3–7 foundational mechanisms** without which the domain cannot be read coherently. **You** produce a **minimal, cited** `modules_and_epics` scaffold with **`evidence_stage: hypothesis`** on concepts and a **human checkpoint** before breadth work.

**What you must produce:** **`map-model-spec.json`** with **`modules_and_epics`** rows carrying **`module.foundational: true`** for spine areas; **lean `concepts[]` per `domain.md`** (this is the spine); **`evidence_stage: hypothesis`**; provisional **`chunk_ids`** / **`chunk_evidence`**; matching epics with **≥ 2** **`confirming_stories`** whose object nouns align with **`concepts[].name`**; four **scaffold scanners** **PASS**. Optional **`map-model-spec.md`**. **Do not** run **`build_chunk_index.py`** here — that belongs to the **modules/epics scaffold (breadth)** step after scaffold expansion.

**How you work here:** **You** skim **`context_index.json`**, document titles, TOC, and **titles** of chunks only (not counted toward **K**). **Domain + story shape for this step** — only the parts that apply here — are in **§2** (before templates). Core evidence rule: **you** only assert what **you** cite. See baked **Rules**.

1. **Context** — **You** resolve **`context_path`** from **`skill-config.json`** → **`solution_workspace`** → that workspace’s **`solution.conf`**. **You** open **`context_index.json`**. **You** record **N** = number of keys in **`forward_index`** (the breadth step uses **N** later to size its reads; **you** are **not** doing that sampling here).

2. **Open or create the spec** — **`output_dir`** from **`solution.conf`** → **`map-model-spec.json`**. **You** create the file if needed. **You** set **`workflow_step`** / **`workflow_note`** (or your pipeline’s equivalent) so this pass is clearly **foundational spine** work.

3. **Skim to find mechanisms** — **You** skim **`context_index.json`**, document titles, the table of contents, and **chunk titles** (not full reads). From that, **you** pick **3–7** **foundational mechanisms**: areas without which the rest of the domain does not read coherently.

4. **For each mechanism, concepts first, then epic** — For each area, **you** add or extend one **`modules_and_epics`** row with **`module.foundational`: `true`**.

   - **Concepts:** **You** add **lean `concepts[]`** rows: **`name`**, **`evidence_stage`: `hypothesis`**, at least one **chunk anchor** (**`chunk_ids`** and/or **`chunk_evidence`**). Where **you** assert what a concept **owns**, **you** add **`owns`** + **`owns_chunk`**. (Shape and optional **`extends`**: **§2**.)
   - **Epic:** **Only after** those names exist, **you** add the **epic** (**Verb Noun** **`name`**): **`statement`** whose bold **`**Concept**`** spellings **match `concepts[].name`**, plus **`statement_chunk`**; actors; **≥ 2** **`confirming_stories`** whose **object nouns** are already concept names in **this** row. If a story needs another noun, **you** add that concept first — not a free-floating story string.

5. **Human checkpoint** — **You** stop for review. **Do not** start **modules/epics scaffold (breadth)** until this passes.

6. **Optional** — **You** may render **`map-model-spec.md`** from **`parts/templates/map-model-spec.md.template.md`**.

7. **Scanners** — **You** run the four commands in **§4**; **you** fix until **PASS**.

8. **What you do *not* do here** — **Do not** run **`python scripts/build_chunk_index.py`**; that belongs to **breadth** after **you** expand the scaffold.

---

## 2. What each module/epic pair must contain at foundational spine

**Domain + story map — relevant excerpts only** (full specs: **`parts/domain.md`**, **`parts/story-map.md`**)

*Domain (spine-level JSON):*

- **Module** = one mechanism / bounded area; **concepts** = stateful things the story will refer to (**`parts/domain.md`** — *What goes in the Domain Model* → Modules, Domain concepts).
- Each concept: **`name`**, **`evidence_stage`**, and a **chunk anchor**; when you assert what it *owns*, add **`owns`** + **`owns_chunk`**. If a concept is clearly a **subtype** of another named concept in the spec, set **`extends`** to that parent’s **`name`** (same file as **`### **Child** : **Parent**`** in domain prose — **`parts/domain.md`** → *map-model-spec.json — scaffold extensions*).
- Tag stable spine types with **`concept.foundational`: true** where that matches “base of the mechanism” (**`parts/domain.md`** — *Foundational classes*). Skip **`properties`[] / `operations`[]** here unless each field has a **`chunk`** (defer to breadth / deepen).

*Story map (spine-level JSON):*

- **Epic `name`** = **Verb Noun** (**`parts/story-map.md`** — *Hierarchy* / epic row).
- **`statement`** = epic **scope** in one flow: name every domain thing with **`**ConceptName**`** spelling that matches **`concepts[].name`** (**`parts/story-map.md`** — *Domain Grounding*).
- **`triggering_actor`** / **`responding_actor`** = who initiates / who responds (**`parts/story-map.md`** — *Per Interaction* → Trigger / Response actors).
- **`confirming_stories`**: short **Verb Noun** outcomes; object words should **match concept names** in the same row (**`parts/story-map.md`** — *Domain Grounding*: no drift).

**Evidence (matches `chunks_must_be_referenced`)**

- **Concept anchor:** non-empty **`chunk_ids`** *or* **`chunk_evidence`** with **`chunk_id`** per row.
- **Cite claims:** **`module.description`** → **`description_chunk`**; **`concept.owns`** → **`owns_chunk`**; **`epic.statement`** → **`statement_chunk`**; properties/operations only if you add them with **`chunk`**.

**`evidence_stage`**

- At foundational spine, concepts are typically **`hypothesis`** until **K** reads in the scaffold breadth pass substantiate (**`scaffolded`**).

**Module**

- **name**, **`foundational`: `true`** on spine rows, **description** + **`description_chunk`** when asserting.
- **concepts** — **name**, **`evidence_stage`**, **`chunk_ids`** / **`chunk_evidence`**, optional **owns** (+ **`owns_chunk`**). **`depends_on`** is usually **scaffold breadth** once structure stabilizes.

**Epic**

- **Verb Noun** **name**; **statement** + **`statement_chunk`**; **triggering_actor** / **responding_actor**; **≥ 2** **`confirming_stories`**.

**Chunk buckets**

- **identified** / **provisional** / **ambiguous** — populate as far as you can from skim-level evidence.

**Deferrals**

- **`[defer]`**, **`open_questions`**, **`[cross-cutting]`** as needed.

---

## 3. Templates

**Sketch (per pair) — foundational spine**

```
module.name, foundational: true
  description (+ description_chunk)
  concepts: name, evidence_stage: hypothesis
    chunk_ids and/or chunk_evidence
    optional: owns (+ owns_chunk)
epic: Verb Noun, statement (+ statement_chunk), actors,
      confirming_stories: ≥1 (add more as needed for concept coverage)
pair chunk_ids: { identified, provisional, ambiguous }
```

**`map-model-spec.json`** (illustrative — same shape as scaffold breadth; at foundational spine prefer **`hypothesis`** and lean fields)

```json
{
  "workflow_step": "foundational_spine",
  "modules_and_epics": [
    {
      "module": {
        "name": "Module Name",
        "foundational": true,
        "description": "One sentence.",
        "description_chunk": "chunk_id",
        "concepts": [
          {
            "name": "ConceptName",
            "foundational": true,
            "evidence_stage": "hypothesis",
            "chunk_ids": ["chunk_id_1"],
            "owns": "One sentence on what this concept owns.",
            "owns_chunk": "chunk_id"
          }
        ]
      },
      "epic": {
        "name": "Verb Noun",
        "statement": "**Actor** does X across **Concept** flows.",
        "statement_chunk": "chunk_id",
        "triggering_actor": "Player",
        "responding_actor": "System",
        "confirming_stories": ["Verb Noun One", "Verb Noun Two"]
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

**`map-model-spec.md`** (optional) — **`parts/templates/map-model-spec.md.template.md`**.

---

## 4. After you write the JSON

From skill root, with `--input` set to your **`map-model-spec.json`**, **you run:**

```bash
python scripts/scanners/chunks_must_be_referenced.py --input <path-to-map-model-spec.json>
python scripts/scanners/no_duplicates.py --input <path>
python scripts/scanners/epic_requires_confirming_stories.py --input <path>
python scripts/scanners/no_junk_concepts.py --input <path>
```

**You** fix until **PASS**. Detail: **`rules/`** (baked into **`parts/steps/built/modules-epics-foundational-spine.md`**).

---

## 5. What you must verify with a human (foundational spine)

1. **You** confirm the spine is visible: **3–7** mechanisms, **`module.foundational`** and **`hypothesis`** make sense.
2. **You** confirm every row is chunk-anchored; epics have **≥ 2** confirming stories.
3. **You** confirm names follow **noun module / Verb Noun epic** (see rules).
4. **You** confirm **`concepts[].name`** and domain words in **`epic.statement`** / **`confirming_stories`** **match exactly (100%)** — rule **`scaffold-concept-story-name-alignment`**; **non-negotiable**.

When **you** and the reviewer approve, **you** proceed to the **modules/epics scaffold (breadth)** step (**`parts/process.md`**).
