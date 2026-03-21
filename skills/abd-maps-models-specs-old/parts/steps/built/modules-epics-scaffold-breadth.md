# Modules and epics scaffold (K-read breadth)

## Your role

You are a **domain modeler** and a **story mapper**. In this step **you** figure out the **foundational model** of the system and the **epics and stories** that can **realize** those foundational components. **You** also build a working sense of **what other modules, epics, and downstream work** will **use or depend on** those foundational pieces — so **you** are not modeling in a vacuum.

Everything below is **what you must do** to finish this step.

---

**Where this sits:** This file is the **modules/epics scaffold (breadth)** slice of **`parts/process.md`** (Stage 2 — **Modules and Epics**). **You must** complete the **foundational spine** (**`parts/steps/built/modules-epics-foundational-spine.md`**) first. That pass gives **you** the **concept-first spine**; in breadth **you** substantiate and expand **`concepts[]`** — **you do not** substitute epic lists for understanding.

## What you must achieve (non-negotiable)

**Your main success** is a **refined set of modules and epics**, **domain concepts**, and **stories** developed enough to cover the **foundational, cross-cutting mechanisms** of the solution. **You must** finish able to **(1)** **go deeper into detailed design later** without inventing structure from scratch, and **(2)** **see where dependencies run** between areas of the model. **Do not** sub-optimize on a thin set of concepts — a model that looks small but **conceals** what still must be named, owned, and connected, so **you** lose track of what to flesh out next.

### Overarching outcome (what this step is for)

**Foundational object model.** 
- You **grow** each pair’s **`module.concepts[]`**
- You **anchor** claims to chunks, 
- You **layer** base → categories → implementations
- You promote **`evidence_stage`** toward **`scaffolded`** 

**Module dependencies.** 
- You make **wiring visible**
- You define **`module.depends_on`** between provider and consumer modules
- You define  **concept-to-concept** shape (**`extends`**, **owns**, cross-cutting notes
- You connect **foundational** material to **extensions** and **categorization** So it's not hidden in story titles alone

**Validation through epics and stories.** **Epics** and **`confirming_stories`** **prove** the model: **`epic.statement`** and story vocabulary **must** line up with **`concepts[].name`** (**bold names**, **`statement_chunk`**, chunk-tied wording). **Edit order**: concepts first, epics second; **keep the two locked** (**`scaffold-concept-story-name-alignment`** — no story nouns without **`concepts[]`** rows).

**Split work (brief).** When **K** is large, **sub-agents** or **batches** take **ranges** of the breadth-sorted id list, return **patches**; a **parent** merge reconciles one JSON (union **`chunk_ids`**, reconcile **`depends_on`**, dedupe questions). Optional: route by module/epic pair after ids are chosen.

**Support, not the point:** **K** reads, **§4** scanners, and **`build_chunk_index.py`** **support and verify** the spec.


**Recording.** You persist the outcome in **`map-model-spec.json`**: per module/epic pair, **cited** **`module.concepts[]`** (names, **`owns`** + **`owns_chunk`**, **`chunk_ids`** / evidence, **`evidence_stage`**, **`extends`**, optional **`properties`[] / `operations`[]** with **`chunk`**), **`module.depends_on`** for provider/consumer relationships, and aligned epics / **`confirming_stories`**. **§2** is the field checklist — not a second workflow.

---

## 1. What you must do (in order)

**One** ordered list. **§2** is the field checklist while you execute steps **8–12** (concepts through **`depends_on`**).

1. **Context** — **You** resolve **`context_path`** → **`context_index.json`**. **N** = **`forward_index`** size; **K** = round(0.3×N), band ⌊0.28N⌋–⌈0.32N⌉ (if N &lt; 10, at least max(1, round(0.3×N))). **Do not** store K, N, or a frozen chunk manifest in the spec.

2. **Open the spec** — **`map-model-spec.json`** (already contains foundational spine).

3. **Choose breadth reads** — Lexical sort chunk ids on **`forward_index`**. **K** = max(1, round(0.3×N)). Pick **K** ids **spread** from first to last of the sorted list (stratified breadth — not one cluster). Keep chosen ids in **session notes / tally**, not in JSON.

4. **Optional: batches / sub-agents** — For large **K**, assign consecutive **ranges** of the sorted list; each returns **patches** (`modules_and_epics`, `open_questions`, `chunk_ids` buckets). **Parent** merges (union **`chunk_ids`**, reconcile **`depends_on`**, dedupe questions). Optional: pair-scoped routing after ids are chosen.

5. **Interactive AI** — **You** read chunks and edit **`map-model-spec.json`** directly (optionally with an assistant). **No** Python driver required for reading/editing.

6. **Full-read pass** — Open **`chunks/<id>.md`** for chosen ids. **+1** only after a **full** read (**mandatory** full reads — **no** skim); **stop** at **K**. Use step **4** when splitting work.

7. **While reading** — **You** note mechanisms, actors, ownership, cross-area ties; **you** map nouns to **new or existing `concepts[]`** (preferred) or **`open_questions`** / cross-cutting notes — **never** only to a story title.

8. **Concepts first (primary)** — For each module/epic pair, **you** expand **`module.concepts[]`**. **You** satisfy **§2** domain (breadth): **chunk-anchor** every claim; **`evidence_stage`** **hypothesis → scaffolded** when **K** reads substantiate; **`concept.extends`** for is-a; **`properties`[] / `operations`[]** with **`chunk`** for has-a; **concept layering** (base → categories → implementations); **verb/noun** module/epic/story rules **after** the concept set for the pair is honest.

9. **Epics and confirming stories (secondary)** — **Verb Noun** epic names; **`statement`** with **`**Concept**`** matching **`concepts[].name`**; **`statement_chunk`**; optional **`pre_condition`** + **`pre_condition_chunk`**. **`confirming_stories`**: every behavior **K** justifies — **minimum two**, no artificial cap — **using object nouns that already appear in `concepts[].name`**. If a distinct noun is needed, **you** add the concept row in step **8**, **then** name the story.

10. **Concept–story name alignment** — **`concepts[].name`** and story strings (**`epic.statement`** bold names, **`confirming_stories[]`** object nouns) **match 100%** — **`scaffold-concept-story-name-alignment`**, **non-negotiable**. **Default fix:** add **`concepts[]`** rows + chunks.

11. **Track chunks** — **You** record per pair in **`chunk_ids.identified` / `provisional` / `ambiguous`**.

12. **`module.depends_on`** — For each consumer module, **you** add **`depends_on`** (**`module-depends-on.md`**). **You** resolve duplicates (**`no-duplicates.md`**) first.

13. **Optional** — **`map-model-spec.md`** from **`parts/templates/map-model-spec.md.template.md`**.

14. **Scaffold scanners** — Four commands (**§4**); **you** fix until **PASS**.

15. **`build_chunk_index.py`** — `python scripts/build_chunk_index.py` (config defaults or `--input` / `--output`); keep **`mms-chunk-index.json`** current.

16. **Human handoff** — **§5** checklist.

**Rules:** **Do not** embed a pre-written **K** chunk-id list inside JSON. Domain + story detail: **§2** and baked **Rules**.

---

## 2. Reference: per-pair JSON shape (not a second workflow)

**You use** this while **you** edit **`map-model-spec.json`** in steps **8–12** in **§1**. Full narrative specs: **`parts/domain.md`**, **`parts/story-map.md`**.

*Domain (breadth JSON) — what you must satisfy:*

- **Layering:** **you** structure base → subtypes → variants (**`parts/domain.md`** *What goes in* + **`concept-layering-scaffold`** rule). **You** encode **is-a** with **`concept.extends`** = parent **`name`**; **you** encode **has-a** in **`properties`[] / `operations`[]** with **`chunk`** per asserted field (**`parts/domain.md`** — *Composition vs extends* under scaffold extensions table).
- **`module.depends_on`:** **you** list providers from each consumer module (**`parts/domain.md`** + rule **`module-depends-on`**).
- **`evidence_stage`:** **you** promote to **`scaffolded`** when **K** reads substantiate the **owns** / properties / operations **you** add (**`parts/domain.md`** — *map-model-spec.json* table).

*Story map (breadth JSON) — what you must satisfy:*

- **Epic** **`name`**: Verb Noun; **`statement`**: scope line with **`**Concept**`** for each domain noun **you** use (**`parts/story-map.md`** — *Epic* row + *Domain Grounding*).
- Optional **`epic.pre_condition`** + **`pre_condition_chunk`** when **you** assert shared given-state (**`parts/story-map.md`** — *Pre-Condition*).
- **`confirming_stories`**: all behaviors **K** supports; **you** keep names aligned with **`concepts[].name`** (**`parts/story-map.md`** — *Domain Grounding*).

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

- **name**, **`foundational`**, **description** + **`description_chunk`**, **`depends_on`** (your step 12), **concepts** with cited **`owns`**, optional **`extends`**, optional **`properties`[] / `operations`[]** (each with **`chunk`**) per the domain excerpt above.

**Epic**

- **Verb Noun** **name**; **statement** + **chunk**; actors; optional **pre_condition** + chunk; **confirming_stories** (≥ 2, **you** list all **K** supports) per the story-map excerpt above.

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
      confirming_stories: min 2, all justified names
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


---

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: foundational-spine-and-evidence-stage
phases: [step1]
order: 5
impact: HIGH
---

## Foundational spine and evidence-stage ladder

Before naming modules or epics, establish the **domain spine**: the minimal set of concepts and mechanisms without which the rest of the model cannot be read coherently. In [`parts/process.md`](../../process.md) this is the **Foundational mechanisms** row (Stage 2), separate from **Modules and Epics** (scaffold breadth).

**DO**

- Identify **foundational** concepts: core entities, invariants, and mechanisms that other concepts presuppose. Mark them in JSON with `module.foundational: true` on the module that primarily owns that spine (or split if the spine spans modules — then mark each contributing module).
- Assign every concept an **`evidence_stage`** aligned with [`parts/process.md`](../../process.md) / AGENTS. Start conservative; promote only when chunk evidence supports it.
- Cite chunks from the first substantive claim (`description_chunk`, `owns_chunk`, `chunk_ids` / `chunk_evidence`) — see `chunks-must-be-referenced.md`.

**Evidence-stage ladder (concept-level)**

Use these values on each `concept` (add `open_questions` when the schema or material is unclear):

| Stage | Meaning |
|--------|---------|
| `hypothesis` | **[Foundational mechanisms](../../process.md)** or early **[Modules and Epics](../../process.md)**: named from skim/structure; provisional citations; not yet substantiated by the **K** full-read pass |
| `scaffolded` | **[Modules and Epics](../../process.md)**: substantiated by the orientation / **K** chunk reads — chunk-anchored names and any `owns` / properties / operations you cite there |
| `deepened` | After **[Concept Classes and Stories](../../process.md)** (deepen): full properties/operations/invariants from pair chunks (optional until deepen runs) |

**Human gate**

- If a concept would be promoted to **`scaffolded`** or **`deepened`** but the source is ambiguous, **stop** and record under `open_questions` instead of inventing detail.

**DON'T**

- Collapse foundational spine and **Modules and Epics** into one pass: do not skip the explicit “what is foundational?” pass and jump straight to epic titles.
- Mark `module.foundational: true` for convenience modules (helpers, cross-cutting buckets) without a spine role.


---

---
rule_id: verb-noun-module-epic-story
phases: [step1]
order: 8
impact: HIGH
---

## Verb/noun alignment for modules, epics, and scaffold stories

Naming must match the story-map conventions in `parts/story-map.md` and stay consistent with `parts/domain.md` (modules = bounded contexts; epics = journey; confirming stories = observable outcomes).

**Non-negotiable:** Domain object words in **`epic.statement`** and **`confirming_stories[]`** must use **the exact same strings** as **`concepts[].name`** in that module (**100% match**). See **`scaffold-concept-story-name-alignment`** — not separate from this rule.

**Modules (nouns)**

- **Module names** are **noun phrases** — a bounded context or subsystem (e.g. `Order Fulfillment`, `Policy Engine`).
- Avoid verb-led module titles unless the domain truly names the area that way; prefer the thing being coordinated.

**Epics (verb + noun)**

- **Epic titles** follow **Verb Noun** (or **Verb the Noun**): the user or system **does** something meaningful (e.g. `Place Order`, `Resolve Coverage Conflict`).
- **`epic.statement`** should read as a goal or outcome in the same voice, not a module dump.

**Confirming stories (verb + noun)**

- Each **`confirming_stories[]`** entry is **Verb Noun** — one observable outcome that **confirms** the epic (see `epic-requires-confirming-stories.md`).
- The **object noun** (the domain thing acted on) must be **identical** to a **`concepts[].name`** in that module — **100% string match**, not paraphrase.
- Stories are **not** module names and **not** generic placeholders (`Do work`, `Handle requests`).

**DO**

- Cross-check epic and story titles against `parts/story-map.md` § Epics and § Stories.
- If an epic is noun-only, rewrite to verb+noun or document the exception in `open_questions`.

**DON'T**

- Use the same string for module name, epic title, and story title without a deliberate reason (that usually hides missing decomposition).


---

---
rule_id: concept-layering-scaffold
phases: [step1]
order: 12
impact: HIGH
---

## Concept layering at scaffold (base → categories → implementations)

At **[Modules and Epics](../../process.md)** (scaffold breadth), structure concepts so readers can navigate **general → specific** without mixing levels in one undifferentiated list.

**Layering model**

1. **Base / root** — The umbrella concept for the area (often one per module or sub-area).
2. **Categories / subtypes** — Named partitions or roles under the base (enums, subtypes, or clearly named siblings).
3. **Implementations / specifics** — Concrete variants, policies, or mechanisms that **depend on** the categories.

**Naming**

- Prefer **`SubtypeName : BaseName`** (or equivalent convention already used in this spec) when a concept is a specialization of another — see `classify-variants-before-modeling.md` for variant vs duplicate.

**DO**

- Reflect layering in `concept` names and in **`module.depends_on`** where one module’s concepts presuppose another’s base types (see `module-depends-on.md`).
- Keep **Modules and Epics** scaffold breadth in check: defer exhaustive enumeration of every implementation to **[Concept Classes and Stories](../../process.md)** (deepen) unless chunks already force them.

**DON'T**

- Flatten all domain nouns into a single bucket without parent/variant structure when the source distinguishes them.
- Add implementation-level concepts with no path to a base or category — park in `open_questions` or mark `evidence_stage: hypothesis` until the **K** reads or **Concept Classes and Stories** ground them.


---

---
rule_id: module-depends-on
phases: [step1]
order: 42
impact: MEDIUM
---

## Module dependency shape (`depends_on`)

After modules and their primary concepts are drafted, record **explicit dependencies** between modules so deepen, integrate, and scanners can order work and detect cycles.

**JSON shape (per dependency entry)**

Use this structure (field names may match your existing schema; align with `map-model-spec.json` conventions in the repo):

```json
"depends_on": [
  {
    "dependent_concepts": ["ConceptA", "ConceptB"],
    "module": "Other Module Name",
    "provides_concepts": ["BaseType", "SharedPolicy"],
    "reason": "Short text: why this module needs the other (cite chunk ids in narrative or in linked evidence)."
  }
]
```

**DO**

- List dependencies from **foundational / shared** modules toward **consumers** (the consumer module holds `depends_on` pointing to providers).
- Tie each dependency to **concepts** on both sides — not vague “uses other module.”
- Prefer **acyclic** graphs at scaffold time; if a cycle is real, document it in `open_questions` and justify.

**DON'T**

- Omit `depends_on` when two modules clearly share vocabulary — either merge synonyms in integrate or record the dependency.
- Use `depends_on` as a substitute for **duplicate concepts** — resolve duplicates per `no-duplicates.md` first.


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
rule_id: scaffold-concept-story-name-alignment
phases: [step1]
order: 45
impact: HIGH
---

## Scaffold: concepts and stories match exactly (100%)

**Non-negotiable.** Nothing in this rule is optional.

**Spine and breadth are understood through `concepts[]`, not through epic titles.** This rule complements **`domain-interaction-sync.md`** (later: bolded names in triggers/responses). At **scaffold** time, **`concepts[].name`** and **story text** ( **`epic.statement`** bold names, **`confirming_stories[]`** object nouns) are **one vocabulary**. They must **match 100%** — **the same identifier strings** as in **`concepts[].name`** for every domain object the epic or story names.

- **No synonyms** in story titles when the model uses a canonical **`concepts[].name`**.
- **No drift** (“close enough”, “related term”, informal shorthand).
- **No** domain object in **`confirming_stories`** or **`epic.statement`** that does not appear as **`name`** on a **`concepts[]`** row in that module (add the concept first, or fix the text).

If the source material uses two terms for one thing, resolve via **`classify-variants-before-modeling.md`** and/or record a single canonical **`concepts[].name`** plus an explicit note in **`open_questions`** — **not** two different strings in stories vs JSON.

**DO**

- For each **`**ConceptName**`** in **`epic.statement`**, assert **`ConceptName`** exists in **`module.concepts[].name`** (exact string match).
- For each **`confirming_stories[]`** entry, extract **object noun(s)** that refer to domain things; each must **equal** some **`concepts[].name`** in the same module (or document cross-module reference in **`open_questions`** with the **same** spelling as the owning module’s concept).
- If the story needs a new domain object, **add** **`concepts[]`** first (minimal row + chunk evidence), **then** write the story using **that exact `name`**.
- Run this check **after** epics and confirming stories exist, **before** finalize scanners.

**DON'T**

- Treat story titles or epic statements as free prose unrelated to **`concepts[].name`**.
- Use “matching or related” — **exact match** only, unless **`open_questions`** defines an alias table the whole spec follows.


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
rule_id: classify-variants-before-modeling
phases: [step3]
order: 25
impact: HIGH
---

## Classify variant families before you model them

When the corpus presents a family of variants under one umbrella idea, decide whether the variants share **all** of the same mechanics end-to-end, or only **some** — with real differences in how specific parts work. That choice drives whether you use a type field (enum) on one concept or defer subtypes (inheritance) for a later pass.

- **All mechanics align** — same validation shape, same lifecycle rules, same fulfillment/resolution steps; only labels, codes, or cosmetic fields differ → treat as one concept with a **type property** (`EnumType` on the parent in `map-model-spec.json`).
- **Some mechanics align, others diverge** — e.g., a shared high-level lifecycle, but **different** validation rules, fulfillment paths, settlement steps, or resolution steps between variants → **inheritance / subtype** candidate → flag `[defer]` with the chunk that proves the variants exist. Do not invent parallel subtype concepts until the scaffold pass accepts them.

This is **not** “do they share *a* mechanic?” — many variants share *something* (same noun in the source). The question is whether they share **the full set** of behavioral mechanics; partial overlap with meaningful differences in named aspects is the signal for subtyping.

There is no scanner for this rule. It is enforced by reading chunks and by the Step 6 assessment (type-field-vs-subtype).

**Recurring pattern (not a corner case):**  
Models **constantly** confuse **two levels at once**: (1) sibling variants under an umbrella that are **true extensions** — different end-to-end pipelines — vs (2) **one** of those branches where variants **only** change which data or label the **same** pipeline reads. The first belongs in **subtyping / inheritance**; the second belongs in a **type property** on that branch only. Do not flatten both into a single enum on the umbrella concept.

(Classification only; serialize extensions vs enums however your pipeline defines.)

**DO** run this test whenever you see a list of named variants under one parent idea — when variants first appear in evidence **and** when you name or refine the parent concept in the scaffold. When not all mechanics align (subtype case), record deferral on the parent concept in the scaffold (same shape as any other concept — `owns` may start with `[defer]` until harmonize); deferral is a modeling choice, not only a discovery note.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "PaymentInstruction",
            "owns": "[defer] Split wire vs ACH vs RTP into subtypes after harmonize — see chunk chunk-pay-001",
            "owns_chunk": "chunk-pay-001",
            "chunk_ids": ["chunk-pay-001"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO** use a single concept with an `EnumType` property on the **branch** where **all** mechanics match and only **which data** applies differs. Do not introduce parallel subtype concepts for that branch when the source describes one flow and only a kind flag or coded field changes inputs. Sibling branches that **do** differ in pipeline stay **extensions** of the umbrella — not extra enum literals on the homogeneous branch.

**Example (illustrative — one domain; names are not normative):** umbrella **A** with extensions **B**, **C**, **D** when mechanics diverge; **B** alone carries `EnumType` for variants that share **B**’s pipeline and only switch inputs.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "Attack",
            "owns": "Common attack notion; specialized by StandardAttack, PerceptionAttack, AreaEffectAttack where mechanics diverge",
            "owns_chunk": "chunk-attack-0",
            "chunk_ids": ["chunk-attack-0"]
          },
          {
            "name": "StandardAttack",
            "owns": "Owns hit resolution for ordinary attacks; melee vs ranged shares this pipeline and only selects which defense applies (e.g. parry vs dodge)",
            "owns_chunk": "chunk-attack-standard",
            "chunk_ids": ["chunk-attack-standard"],
            "properties": [
              {
                "definition": "EnumType attack_kind { melee, ranged }",
                "chunk": "chunk-attack-standard"
              }
            ]
          },
          {
            "name": "PerceptionAttack",
            "owns": "Owns resolution when the attack uses perception-based mechanics (differs from standard attack flow)",
            "owns_chunk": "chunk-attack-perception",
            "chunk_ids": ["chunk-attack-perception"]
          },
          {
            "name": "AreaEffectAttack",
            "owns": "Owns resolution for area templates / multiple targets (differs from standard single-target flow)",
            "owns_chunk": "chunk-attack-area",
            "chunk_ids": ["chunk-attack-area"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Model **inheritance / extends** from **Attack** to those three in whatever form your process uses; this rule is about **getting this two-level split right** — it is one of the most common modeling mistakes in the wild.

**DO NOT** put perception and area-effect on the same `EnumType` as melee/ranged on **StandardAttack** when mechanics differ — that collapses **extensions** (different pipelines) into **labels** (same pipeline).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Ledger",
        "concepts": [
          {
            "name": "MoneyAmount",
            "owns": "Owns numeric amount with ISO currency code",
            "owns_chunk": "chunk-fx-01",
            "chunk_ids": ["chunk-fx-01"],
            "properties": [
              {
                "definition": "EnumType currency { USD, EUR, GBP }",
                "chunk": "chunk-fx-01"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** create both an enum and a parallel set of subtype concepts for the same family.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "PaymentInstruction",
            "chunk_ids": ["chunk-01"],
            "properties": [
              {
                "definition": "EnumType rail { wire, ach, rtp }",
                "chunk": "chunk-01"
              }
            ]
          },
          { "name": "WireTransfer", "chunk_ids": ["chunk-01"] },
          { "name": "ACHCredit", "chunk_ids": ["chunk-01"] },
          { "name": "RTPPayment", "chunk_ids": ["chunk-01"] }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** model separate subtype concepts when one aggregate and a single coded field (`status`, channel code, etc.) matches the source.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          { "name": "OrderStatusPending", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusPaid", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusShipped", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusCancelled", "chunk_ids": ["chunk-ord-1"] }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Prefer one concept on the same module:

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Order",
            "chunk_ids": ["chunk-ord-1"],
            "properties": [
              {
                "definition": "EnumType status { pending, paid, shipped, cancelled }",
                "chunk": "chunk-ord-1"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** model subtypes at Step 1 when the skill says to defer — keep a single parent row and `[defer]` in `owns` (see first **DO** example) instead of adding the deferred subtype concepts as full rows until harmonize approves.


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
