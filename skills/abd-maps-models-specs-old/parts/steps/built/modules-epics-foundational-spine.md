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

1. **Context** — **You** resolve **`context_path`** from **`conf/abd-config.json`** → **`solution_workspace`** → that workspace’s **`solution.conf`**. **You** open **`context_index.json`**. **You** record **N** = number of keys in **`forward_index`** (the breadth step uses **N** later to size its reads; **you** are **not** doing that sampling here).

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
