# Process — Maps-Models-Specs

Pipeline: Context → Discover → Classify → Deepen → Canonicalize → Evidence → Structure → Finalize.

**Core principle:** Discover taxonomy layer by layer, top-down, with evidence indexed as you go. Each step is a separate AI or code pass. Scanners enforce structure mechanically. AI resolves violations — scanners never propose fixes.

**Prerequisites:** Stage 1 — source documents (PDF, DOCX, PPTX, etc.). Stage 2+ — `context/context_index.json` and `context/chunks/*.md` from Stage 1.

**Two parallel artifacts produced at every step:**

- **Domain model** — modules, concepts, properties, operations (what things are and own)
- **Story map** — epics, sub-epics, stories, acceptance criteria, specifications, examples (what actors do and what changes)

These are two views of the same coin and must be produced simultaneously.

**Output files (single evolving document):**

- `map-model-spec.json` — forward index (Step 4 creates; Steps 5/5a classify; Step 6 deepens; Step 7 canonicalizes; Step 9 structures; Step 10 finalizes)
- `map-model-spec.md` — human-readable summary
- `mms-chunk-index.json` — reverse index (chunk_id → concepts, epics, stories, modules). **Code-only:** `build_chunk_index.py` reads map-model-spec.json and produces this derived artifact. Steps 4a, 6a, 7a run it after 4, 6, 7 whenever the spec changes. The AI steps do not invoke it — it is a separate step.

---

## Stage 1: Extract Context


| #   | Step        | Initiator    | Script                        | What it does                                                   | Coverage       | Ref                   | Outputs                         |
| --- | ----------- | ------------ | ----------------------------- | -------------------------------------------------------------- | -------------- | --------------------- | ------------------------------- |
| 1   | **Convert** | Human → Code | convert_to_markdown.py        | Source → markdown                                              | Creates corpus | [context](parts/context.md) | markdown                        |
| 2   | **Analyze** | AI           | discover_context_structure.py | Analyze markdown → markers for headers, tables, sections, TOC, | —              | [context](parts/context.md) | solution.conf                   |
| 3   | **Parse, curate, chunk, index** | Code | parse_and_curate.py | Parse → **curate** (classify, exclude) → chunk → index          | —              | [context](parts/context.md) | chunks/*.md, context_index.json |

**Step 3 — curate is not a separate step.** The script parse_and_curate.py does all of: parse markdown to blocks; **curate** (classify evidence_type, assign document_region, exclude noise and out-of-scope sections); purpose-built chunking and merge; write chunks and context_index.json. Excluded blocks are listed in context_index.json under `excluded` and are not written to chunks.


---

## Stage 2: Map and Model (Steps 4–7)


| #   | Step                              | Actor | Script                                    | What it does                                                                                                                  | Coverage               | Ref                                                   | Outputs                                           |
| --- | --------------------------------- | ----- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------- | ------------------------------------------------- |
| 4   | **Modules and Epics**             | AI    | —                                         | Orient on context taxonomy; discover module/epic pairs; sketch modules and concept classes; 2–3 story names per epic          | 30% sampled            | [modules-epics](parts/modules-epics.md)                     | map-model-spec.json, map-model-spec.md            |
| 4a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |
| 5   | **Concept Classification**        | AI    | classify_chunks.py (Pass 1)               | AI reads chunks (or configured %); extracts concepts and relationships                                                        | All chunks             | [concept-classification](parts/concept-classification.md)   | map-model-spec.json                               |
| 5a  | **Concept Classification (code)** | Code  | classify_chunks.py (Pass 2); summarize.py | Code scans chunks; extracts concepts and relationships, merges gaps with AI pass; summarize.py → summary.md, relationships.md | All chunks             | [concept-classification](parts/concept-classification.md)   | map-model-spec.json, summary.md, relationships.md |
| 6   | **Concept Classes and Stories**   | AI    | —                                         | Deepen classes/stories per module/epic; resolve [defer] tags                                                                  | Chunks per Module/Epic | [concept-classes-stories](parts/concept-classes-stories.md) | map-model-spec.json                               |
| 6a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |
| 7   | **Integrate and Harmonize**       | AI    | —                                         | Unify naming; wire cross-module; resolve [cross-cutting]; finalize subtypes                                                   | —                      | [integrate-harmonize](parts/integrate-harmonize.md)         | map-model-spec.json                               |
| 7a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |


---

## Stage 3: Specification


| #   | Step          | Actor | Script                | What it does                                                                   | Coverage   | Ref                       | Outputs             |
| --- | ------------- | ----- | --------------------- | ------------------------------------------------------------------------------ | ---------- | ------------------------- | ------------------- |
| 8   | **Evidence**  | Code  | TBD (not implemented) | Mine complete context for actions, decisions, states, relationships            | All chunks | [evidence](parts/evidence.md)   | evidence/*.json     |
| 9   | **Structure** | AI    | —                     | Finalize Map & model and build steps, scenarios, examples from evidence        | —          | [structure](parts/structure.md) | map-model-spec.json |
| 10  | **Finalize**  | AI    | —                     | Assign operations; link behaviors; split by subtype; fix anti-patterns; assess | —          | [finalize](parts/finalize.md)   | map-model-spec.json |


---

## Config (solution modeler pattern)

**Skill config** `conf/abd-config.json` — one key:

- `solution_workspace` — path to workspace root (e.g. `mm3`). When set, all paths resolve relative to workspace.

**Workspace config** `<workspace>/solution.conf` — paths relative to workspace root:

- `output_dir` — where map-model-spec.json, evidence/, mms-chunk-index.json live (default: `solution` or e.g. `maps-models-specs`)
- `context_path` — where chunks/ and context_index.json live (default: `output_dir/context`)

When no workspace is configured, scripts fall back to skill root (flat layout).

## Workspace Layout

**With workspace (e.g. mm3):**

```
mm3/
├── solution.conf          # output_dir, context_path
├── maps-models-specs/     # output_dir
│   ├── summary.md        # from summarize.py (Step 5a)
│   ├── relationships.md  # from summarize.py (Step 5a)
│   ├── context/          # chunks/*.md, context_index.json
│   ├── generated/        # junk_config.json
│   ├── evidence/         # actions.json, decisions.json, ...
│   ├── map-model-spec.json
│   ├── map-model-spec.md
│   └── mms-chunk-index.json
```

**Flat (no workspace):**

```
abd-maps-models-specs/
├── conf/abd-config.json   # optional: solution_workspace
├── parts/, rules/, scripts/
├── context/               # chunks/*.md (content), context_index.json (metadata + indexes)
├── evidence/
├── map-model-spec.json
├── map-model-spec.md
└── mms-chunk-index.json
```

---

## Operational flow

Per-step details: [context](parts/context.md), [modules-epics](parts/modules-epics.md), [concept-classification](parts/concept-classification.md), [concept-classes-stories](parts/concept-classes-stories.md), [integrate-harmonize](parts/integrate-harmonize.md), [evidence](parts/evidence.md), [structure](parts/structure.md), [finalize](parts/finalize.md).


| Step | Actor        | Script                                    | Inputs                                    | Outputs                                           |
| ---- | ------------ | ----------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| 1    | Human → Code | convert_to_markdown.py                    | Source folder                             | markdown                                          |
| 2    | AI           | discover_context_structure.py             | markdown                                  | solution.conf                                     |
| 3    | Code         | parse_and_curate.py                       | markdown                                  | chunks/*.md, context_index.json                   |
| 4    | AI           | —                                         | context/                                  | map-model-spec.json                               |
| 4a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 5    | AI           | classify_chunks.py (Pass 1)               | map-model-spec.json, context/             | map-model-spec.json                               |
| 5a   | Code         | classify_chunks.py (Pass 2); summarize.py | map-model-spec.json                       | map-model-spec.json, summary.md, relationships.md |
| 6    | AI           | —                                         | map-model-spec.json, context/             | map-model-spec.json                               |
| 6a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 7    | AI           | —                                         | map-model-spec.json, mms-chunk-index.json | map-model-spec.json                               |
| 7a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 8    | Code         | TBD (not implemented)                     | map-model-spec.json, context/             | evidence/*.json                                   |
| 9    | AI           | —                                         | map-model-spec.json, evidence/            | map-model-spec.json                               |
| 10   | AI           | —                                         | map-model-spec.json                       | map-model-spec.json                               |


### File dependency graph

```
source docs
       │
       ▼
   STAGE 1 (Code) — Steps 1–3
   convert → [discover_context_structure] → parse_and_curate
       │
       ▼
context_index.json + chunks/*.md
       │
       ├──────────────────────────────────────────────────────────────────┐
       │                                                                   │
       ▼                                                                   ▼
   STEP 4 (AI)                                                    STEP 5 (AI)
   Shape modules/epics                                            classify_chunks Pass 1
   samples 30%                                                            │
       │                                                                   │
       ▼                                                                   ▼
map-model-spec.json ◄───────────────────────────────────────────── STEP 5a (Code)
       │                    (writes evidence directly)                    classify_chunks Pass 2 + summarize
       │                                                                   │
       ├──────────────────────────────────────────────────────────────────▼
       │                                              summary.md, relationships.md
       │                                                                   │
       ▼                                                                   ▼
                                                                    STEP 6 (AI)
                                                                    Concept classes and stories
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (deepened)
       │                                                                   │
       │                                                                   ▼
       │                                                      build_chunk_index.py
       │                                                                   │
       │                                                                   ▼
       │                                                      mms-chunk-index.json
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 7 (AI)
       │                                                         Integrate and harmonize
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (canonical)
       │                                                                   │
       │                                                                   ├─────────────────────┐
       │                                                                   │                     │
       │                                                                   ▼                     ▼
       │                                                         STEP 8 (Code)            build_chunk_index.py
       │                                                         evidence extraction            │
       │                                                                   │                     ▼
       │                                                                   ▼              mms-chunk-index.json
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 9 (AI)
       │                                                         Structure
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 10 (AI)
       │                                                         Finalize
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (final)
```

---

# Domain Model Format

## Module

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
- examples: at end of module, after all concepts; one table per concept; shared scenario links the module
```

## Domain Concept

Heading: `### **ConceptName** : <BaseConcept if any>`
One-liner description of the purpose of the concept

```
**ConceptName** : <BaseConcept if any>
- <type> property
      <collaborating concepts if any>
      Invariant: <constraint on this property>
- <type> operation(<param>, ...) → <return>
      <collaborating concepts if any>
      Invariant: <constraint enforced by this operation>
- Interactions: interaction nodes this concept is used by
```

## Examples

**## Examples** (at end of module, after all concepts — one table per concept, shared scenario links all):
```
ConceptName (qualifier):
| scenario | property1 | property2 |
|----------|-----------|-----------|
| module-scenario.phase | val1 | val2 |
===
AnotherConcept (qualifier):
| scenario | property1 |
|----------|-----------|
| module-scenario.phase | val1 |
```

- One scenario prefix for the module (e.g. `monthly-operations`); sub-phases allowed (e.g. `monthly-operations.after-payroll`)
- Qualifier in parentheses after concept name
- Scenario column required; kebab-case
- Columns match concept property names
- `===` separator between tables

### Invariants

Place invariants under the specific property or operation they apply to — not as a separate section. Format: `Invariant: <constraint>`.

```
- Number balance
      Invariant: balance >= 0
- debit(amount) → Boolean
      Invariant: amount <= balance
```

## Guidelines

- Prefer **composition** over inheritance
- Use `Dictionary<K,V>` when items are keyed
- Use `List<T>` only when ordering matters
- Avoid central "service/manager" concepts
- Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options

## Example — Connected Concepts with Tables

Account holds funds; transactions record deposits and withdrawals. The balance is what's available.

```
## Module: Accounts
- concepts — **Account**, **Transaction**

### **Account**

Holds funds. You deposit (credit) or withdraw (debit). Balance is what you have available.

- String name
- List<**Transaction**> transactions
      **Transaction** — history of deposits and withdrawals
- balance() → Number
      current available funds
- debit(amount) → Boolean
      withdraws funds; fails if insufficient
      **Transaction** — adds a withdrawal record
- credit(amount) → void
      deposits funds
      **Transaction** — adds a deposit record

- Interactions: Debit Account, Credit Account

### **Transaction**

A deposit or withdrawal. Belongs to an account.

- **Account** account
      **Account** — which account this affects
- Number amount
- String type {debit, credit}

- Interactions:  Debit Account, Credit Account

### examples

Account (selected):
| scenario                             | name            | balance  |
|--------------------------------------|-----------------|----------|
| monthly-operations.main-checking     | Main Checking   | 3247.50  |
| monthly-operations.main-checking-od  | Main Checking   | 42.00    |
| monthly-operations.savings           | Savings         | 500.00   |
===
Transaction (recorded):
| scenario                             | account         | amount   | type   |
|--------------------------------------|-----------------|----------|--------|
| monthly-operations.main-checking     | Main Checking   | 2400.00  | credit |
| monthly-operations.main-checking     | Main Checking   | 1000.00  | credit |
| monthly-operations.main-checking     | Main Checking   | 142.50   | debit  |
| monthly-operations.main-checking     | Main Checking   | 10.00    | debit  |
| monthly-operations.main-checking-od  | Main Checking   | 500.00   | credit |
| monthly-operations.main-checking-od  | Main Checking   | 458.00   | debit  |
| monthly-operations.savings           | Savings         | 500.00   | credit |
```

One scenario per account. Balance = sum of transactions (credits − debits) for that account in that scenario. Main Checking: 3247.50 = 2400 + 1000 − 142.50 − 10. Overdraft: 42 = 500 − 458. Savings: 500 = 500.

## Validation Checklist

- [ ] Format: `**Concept** : <Base Concept if any>`
- [ ] Module has examples: one table per concept, shared scenario, `===` separator
- [ ] Properties, operations, collaborating concepts listed
- [ ] Each concept referenced via `**Concept**` in story map must exist here
- [ ] Invariants under specific property/operation they apply to
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level

---

# Story Map Format

## Hierarchy

Epic → Sub-Epic → Story → Scenario → Step

| Node | Meaning | Heading |
| ----- | ----- | ----- |
| Epic | Large domain capability — a major area of the system | `# Epic: <name> (<statement>)` |
| Sub-Epic | Logical grouping of related stories — a feature area, not a behavior itself | `## Epic: <name> (<statement>)` |
| Story | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. | `### Story: <name> (<statement>)` |
| Scenario | A condition-specific grouping of steps within a story (e.g. success path, failure path) | `#### Scenario: <name>` |
| Step | A single atomic interaction — one action by one actor | `- Step N: <name> (When/Then <statement>)` |

## Per Interaction

- **Trigger** — Triggering-Actor, Behavior
- **Response** — Responding-Actor, Behavior
- **Pre-Condition** — label only (Given/And)
- **Failure-Modes** — bullet list, max 3; rule/state based only (no infrastructure failures)
- **Domain Concepts** - Domain Concepts related to Interaction, must exist in the domain model
- **Examples** — tables per concept


### Commonly Generated Fields Per Node

| Node | Commonly Generated | Case-by-Case |
|------|--------------------|--------------|
| Epic | Triggering-Actor, Responding-Actor, Name, Pre-Condition | Constraints |
| Story | Trigger, Response, Name, Examples, Pre-Condition, Failure-Modes | Constraints |
| Scenario | Trigger, Response, Pre-Condition, Examples | |
| Step | Trigger, Response, Examples | Constraints (when step-specific) |

## Domain Grounding

Use `**Concept**` in labels. Every concept must exist in Domain Model.

## Inheritance

Parent → child; use `[brackets]` for inherited values (e.g. `Triggering-Actor: [User]`).

## Example Tables

Tables live on the interaction. One per concept referenced in labels, should be identical to examples in the domain model

```
ConceptName (qualifier):
| scenario | field1 | field2 |
|----------|--------|--------|
| success  | val1   | val2   |

AnotherConcept (qualifier):
| scenario | field1 |
|----------|--------|
| success  | val1   |
```

- Qualifier in parentheses after concept name
- Scenario column required; use kebab-case (e.g. `success`, `invalid-details`)
- `===` separator between tables
- Inherited examples: `Examples: [Table Name 1, Table Name 2]`

## Validation Checklist

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- [ ] Trigger: sub-bullets Triggering-Actor, Behavior
- [ ] Response: sub-bullets Responding-Actor, Behavior

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Trigger and Response with [inherited] when from parent

**Example tables**
- [ ] Qualifier in parentheses: `ConceptName (qualifier):`
- [ ] Scenario column required; kebab-case
- [ ] Each table: label, header row, separator row, data rows

**Hierarchy**
- [ ] Epic → Epic/Story → Scenario → Step
- [ ] Each node touches at least one domain concept via `**Concept**`

---

# Stage 1 — Extract Context

**Prerequisite:** Source documents (PDF, DOCX, PPTX, XLSX, HTML, etc.) in a folder.

## Purpose

Convert source documents to markdown, discover structure, parse into structural blocks, curate (classify, exclude, split), and produce `chunks/*.md` (content) and `context_index.json` (metadata + indexes) for Stage 2 onward. This stage creates the corpus that the rest of the pipeline consumes.

**Scope:** Parser / extractor / filterer only. No orchestration, layered memory, or branching.

**Planning:** See [docs/plan-context-curation.md](../docs/plan-context-curation.md) for strategy, decisions, and exact deliverables.

---

## Steps (by initiator)

| Step | Initiator | What it does |
|------|-----------|--------------|
| **1. Convert** | Human → Code | Source files (PDF, DOCX, PPTX, etc.) → markdown |
| **2. Discovery** | AI | Analyze markdown; identify how tables, headers, sections, document-shape regions manifest; output patterns to `context_curation` |
| **3. Parse and Curate** | Code | Document-shape detection → parse → **curate** (classify + exclude) → purpose-built chunking → per-chunk metadata → write chunks/*.md and context_index.json |

**Step 3** includes: document-shape pre-pass, block parsing, **curate** (classification with richer taxonomy; exclusion of noise headings, structural headings, out-of-scope sections, below-min chunks), purpose-built chunking, multi-purpose split, per-chunk metadata, and writing outputs. There is no separate “curate” step—curate is done inside this step.

---

## Exact deliverables

1. **Document-shape detection** — Pre-pass tags regions (front matter, TOC, rules, examples, glossary, appendix, legal).
2. **Richer taxonomy** — evidence_type: domain-rule, mechanic, actor-action, definition, state-change, variation/exception, example, flavor, table, mention, metadata/noise.
3. **Purpose-built chunking** — Definitions small; rules medium; tables row-aware; examples separate. `min_chunk` filters out tiny fragments (e.g. single table cells, orphan bullets). `merge_table_like` merges consecutive short paragraph blocks (PDF-converted tables) into cohesive table chunks. `merge_header_with_next` prepends short all-caps header lines (e.g. TRADE-OFFS) into the following content block instead of excluding them. `merge_definition_runs` merges consecutive short definition blocks (e.g. Parry & Toughness, Fortitude & Will) and skips trivial separators (single bullets) between them.
4. **Multi-purpose split** — Split when block has more than one dominant purpose.
5. **Per-chunk metadata** — candidate_concepts, actors, actions, state_terms, decision_terms, noise_score, modeling_priority, retrieval_tags.
6. **Output schema** — chunks/*.md (content: YAML front matter + markdown); context_index.json (single consolidated index: metadata + refs, forward + reverse indexes).

---

## Classification: Heuristic vs Config-based

**Heuristic (code):** Rules hardcoded in Python. E.g. `structural_type == 'table'` → `evidence_type = 'table'`. No config.

**Config-based:** Rules read from `solution.conf` → `context_curation`. E.g. `document_region_keywords`, `noise_heading_keywords`, `definition_cues`, `example_cues`, `chunking`. User can customize without editing code.

We use both: structural rules are heuristic; keyword/cue matching and chunking rules are config-based.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `convert_to_markdown.py` | Convert PDF, DOCX, PPTX, XLSX, HTML, etc. to markdown. Requires `pip install "markitdown[all]"`. |
| `discover_context_structure.py` | AI pass over markdown; outputs document_region_keywords, chunking rules, cues to `context_curation`. Run after convert, before parse_and_curate. |
| `parse_and_curate.py` | Document-shape detection; parse → blocks; classify (richer taxonomy); purpose-built chunking + multi-purpose split; per-chunk metadata; write chunks/*.md and context_index.json. |

---

## Usage

**1. Convert source folder to markdown**

```bash
python scripts/convert_to_markdown.py --path <source_folder> [--output <output_folder>]
```

**2. Discovery (optional AI pass)**

```bash
python scripts/discover_context_structure.py --path <markdown_folder>
```

Populates `context_curation` in solution.conf. Run after convert, before parse_and_curate.

**3. Parse and curate**

```bash
python scripts/parse_and_curate.py --path <markdown_folder> [--output <context_folder>]
```

When `--output` is omitted, writes to `context_path` from solution.conf (default: `output_dir/context`).

---

## Prompt for study: when assisting with Extract Context

When the user asks you to **extract context** (or to run Convert / Discovery / Parse and Curate for context):

1. **Ask why if they don’t say.** If the user does not state the purpose or scope of the extraction (e.g. “for character creation only”, “for the combat chapter”, “for domain modeling”), ask: *What is this context for? Which parts of the source do you actually need?* Use the answer to guide what to keep or drop.

2. **Review the source and call out unhelpful sections.** After you see the document(s) or markdown (e.g. table of contents, chapter list, section headers), go through the context and explicitly say which sections you think **will not be helpful** for their stated purpose. For example: “I don’t think these sections are going to be helpful for [purpose]: [list sections]. They’re [reason: out of scope / reference-only / setting fluff / legal / etc.].”

3. **Suggest removing them.** Propose removing those sections (or whole chapters) from the corpus—at conversion time (e.g. strip chapters or ranges when converting to markdown) or via config (e.g. `out_of_scope_section_keywords`) so they never become chunks.

4. **Get approval before removing.** Do not remove or strip content until the user approves. Summarize what you propose to remove and ask: “Do you want to drop these from the context?” Only then apply the change (re-convert with strip, edit markdown, or update solution.conf).

---

## Output Format

**chunks/{chunk_id}.md** — one file per chunk. YAML front matter + markdown body. IDE indexable, human readable.

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

**context_index.json** — single consolidated index. Metadata + refs only; no full text. Content lives in chunks/*.md.

```json
{
  "manifest": {
    "sources": ["HeroesHandbook"],
    "section_counts": {"Chapter 3": 12, "Chapter 4": 8},
    "evidence_type_counts": {"definition": 45, "domain-rule": 120, "example": 30},
    "total_chunks": 195,
    "excluded_count": 22
  },
  "forward_index": {
    "blk_00042": {
      "source": "HeroesHandbook",
      "section_path": ["Chapter 3", "Abilities", "Ability Ranks"],
      "document_region": "rules",
      "structural_type": "paragraph",
      "evidence_type": "domain-rule",
      "start_line": 145,
      "end_line": 152,
      "candidate_concepts": ["Ability", "Rank"],
      "actors": [],
      "actions": ["apply", "modify"],
      "state_terms": [],
      "decision_terms": [],
      "noise_score": 0.1,
      "modeling_priority": 0.8,
      "retrieval_tags": ["abilities", "ranks"]
    }
  },
  "concept_seeds": [{"concept": "Ability", "count": 45}, {"concept": "Rank", "count": 32}],
  "reverse_indexes": {
    "by_concept": {"Ability": ["blk_00042", "blk_00043"], "Rank": ["blk_00042", "blk_00051"]},
    "by_evidence_type": {"domain-rule": ["blk_00042", "blk_00043"], "definition": ["blk_00001", ...]}
  },
  "excluded": [{"block_id": "...", "section_path": [...], "reason": "noise", "evidence_type": "metadata/noise", "text_preview": "..."}]
}
```

**Content lookup:** Index → filter/search → get chunk_ids → read `chunks/{chunk_id}.md` for text. No duplication.

---

## Config (solution.conf)

`context_curation` is populated by the AI discovery pass (Step 2). Example schema:

```json
{
  "output_dir": "maps-models-specs",
  "context_path": "maps-models-specs/context",
  "context_curation": {
    "document_region_keywords": {
      "front_matter": ["---", "title:", "author:"],
      "toc": ["table of contents", "contents"],
      "rules": ["rules", "mechanics", "how it works"],
      "examples": ["examples", "for example", "sample"],
      "glossary": ["glossary", "definitions"],
      "appendix": ["appendix", "appendices"],
      "legal": ["copyright", "license", "terms"]
    },
    "noise_heading_keywords": ["table of contents", "index", "glossary"],
    "definition_cues": ["refers to", "is a", "means", ":"],
    "example_cues": ["for example", "for instance", "such as", "e.g."],
    "chunking": {
      "definition": {"max_words": 80, "min_words": 10},
      "rule": {"max_words": 200, "min_words": 20},
      "table": {"row_aware": true},
      "example": {"max_words": 150, "min_words": 15, "priority": 0.5},
      "min_chunk": {"min_words": 2, "min_chars": 15},
      "merge_table_like": {"enabled": true, "max_cell_chars": 50, "min_run_length": 2},
      "merge_header_with_next": {"enabled": true, "max_header_chars": 60},
      "merge_definition_runs": {"enabled": true, "max_words_per_block": 80, "max_merged_words": 250, "min_run_length": 2, "skip_trivial_separators": true}
    },
    "multi_purpose_split": true
  }
}
```

---

## Workspace Layout

After Stage 1 (Steps 1–3):

```
maps-models-specs/
├── context/
│   ├── chunks/           # Content: one .md per chunk (YAML front matter + markdown)
│   │   ├── blk_00042.md
│   │   ├── blk_00043.md
│   │   └── ...
│   └── context_index.json   # Metadata + forward/reverse indexes (no full text)
```

---

## Prerequisite for Stage 2

Stage 2 (Discover) requires `context_index.json` and `chunks/*.md` in the context folder.

---

# Step 4 — Modules and Epics

## Purpose

Orient yourself in the corpus. Discover the major areas of the domain and produce a paired list of **modules** (domain view) and **epics** (interaction view). Every field you populate must be supported by a chunk you read. If you have no chunk, leave the field blank or use a flag.

This is orientation, not modeling. Concepts get sketched — not designed. The epic confirms that the module has real interactions — but stories are a sanity check, not the deliverable. The structure you produce here is the scaffold that Steps 5 and 6 will fill in.

---

## Inputs

- **Context:** Resolve from config. When `conf/abd-config.json` has `solution_workspace`, use `workspace/solution.conf` → `context_path` (default: `output_dir/context`). In that directory use **`context_index.json`** (metadata and indexes) and **`chunks/*.md`** (content). Chunk IDs and their order for sampling come from the keys of **`forward_index`** in `context_index.json`. When no workspace, use `context/context_index.json` and `context/chunks/*.md` at skill root.

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

When you cannot fully resolve something from the chunks you read, flag it explicitly. Never leave a gap unflagged — an unflagged gap is invisible to Step 6.

**`[defer]`** — evidence exists that this thing exists, but not enough to model it yet. Record the chunk. Step 6 will do a targeted read.

**`[uncertain]`** — evidence exists but the boundary or ownership is unclear. State the question explicitly. Requires human confirmation before Step 6 proceeds on it.

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

Full rule files: `rules/`

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

**DO NOT** create subtype concepts or hierarchy entries at Step 2.

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

Two files, then run the index script. Step 4 creates `map-model-spec.json`; Step 6 deepens it; Step 7 canonicalizes it.

### `map-model-spec.json`

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

### `map-model-spec.md`

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

Run all four scanners immediately after writing the JSON output. Each scanner corresponds to one rule file in `rules/`. Scanners highlight gaps — the AI determines whether each violation is a genuine gap, false positive, or needs a `[defer]` flag.

```
python scripts/scanners/chunks_must_be_referenced.py --input map-model-spec.json
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/epic_requires_confirming_stories.py --input map-model-spec.json
python scripts/scanners/no_junk_concepts.py --input map-model-spec.json
```

| Scanner | Rule file | What it checks |
|---|---|---|
| `scan_chunks_must_be_referenced.py` | `chunks-must-be-referenced.md` | Every evidence claim cites a chunk |
| `scan_no_duplicates.py` | `no-duplicates.md` | No duplicate concept or module names |
| `scan_epic_requires_confirming_stories.py` | `epic-requires-confirming-stories.md` | Every epic has at least 2 confirming story names |
| `scan_no_junk_concepts.py` | `no-junk-concepts.md` | No section headers, proper nouns, or instruction phrases as concept names |

Review each violation. Fix, flag `[defer]`, or document as false positive. Re-run until all scanners report `PASS`.

### Pass 1b — Update junk config (AI)

After running the scanners, if you encountered section headers, chapter labels, or proper nouns (character/setting names) while reading chunks that are not already in the junk config, add them now:

- Solution-specific junk terms
- Add to `section_headers` for ToC labels and chapter names found in this corpus
- Add to `proper_nouns` for character names, setting names, organization names
- Add to `additional_junk` for anything else that is clearly not a domain concept

Junk config location: workspace `generated/junk_config.json` or `mms-junk-config.json` next to map-model-spec. The scanner will pick these up on the next run. This file is cumulative — add to it, never remove unless confirmed false positive.

### Pass 2 — Build chunk index (code)

```
python scripts/build_chunk_index.py
```

Defaults use config when workspace is set. Override with `--input` and `--output` if needed.

### Pass 3 — Adversarial validation (AI)

Re-read `map-model-spec.json` against each rule as a checklist. Be adversarial — look for violations the scanner cannot catch:

- Any module name derived from a chapter title or ToC entry?
- Any concept name that is a section header, proper noun, or single common word?
- Any concept with `owns` that is just restating its name rather than declaring a decision?
- Any `[defer]` gap that should have been flagged but wasn't?
- Any confirming story that is an implementation step rather than a testable behavior?
- Any enum decision that should be a subtype candidate (or vice versa)?

Report each violation with: rule name, location in JSON, proposed fix. Fix all violations. Re-read until clean.

---

## Stop for Review

Present the readable summary (`map-model-spec.md`) and ask:

1. Does this list capture all major areas of the corpus?
2. Are any module/epic pairs wrong or misnamed?
3. Are any pairs missing?
4. Are any concept candidates data bags with no real decision ownership?
5. Any areas where you had no chunk evidence and guessed rather than flagged?
6. Are any `[defer]` flags wrong — should they be modeled now?

---

# Steps 5 & 5a — Concept Classification

Read every chunk in the corpus and extract domain evidence. For each chunk, the scan records:
- Which domain concepts it evidences, with evidence type (definition, rule, example, table, mention) and optional note
- Which cross-module relationships it establishes between concepts, with the specific mechanic that justifies each relationship

**Evidence is written directly to map-model-spec.json** — no separate index files. The spec gains:
- `concept.chunk_evidence`: `[{chunk_id, evidence_type, note}, ...]` per concept
- `concept.chunk_ids`: derived from chunk_evidence
- `chunk_ids.identified` / `chunk_ids.provisional` per module/epic pair
- `cross_module_relationships` at top level

**Configuration** — present to user and confirm:
- Chunk text: 100% (default) | 50% | 25%
- Model: gpt-4o-mini (default) | gpt-4o

**How it works:**
- **Step 5 (AI):** AI reads every chunk (or configured %), extracts concepts and relationships
- **Step 5a (Code):** Code scanner runs on full text with concept list from Step 5; merges gaps (catches concepts in text the AI didn't see when chunk-pct < 100%). Then `summarize.py` → `summary.md`, `relationships.md`

**Outputs:** `map-model-spec.json` (updated with evidence), `summary.md`, `relationships.md`

---

# Step 6 — Concept Classes and Stories

## Purpose

Take the module/epic pairs from Step 4 and deepen them. For each module/epic pair: (1) deepen concepts with full properties, operations, invariants; (2) deepen stories to Trigger, Response, Pre-Condition, Failure-Modes; (3) add hierarchy (sub-epics, concept relationships); (4) resolve all `[defer]` flags via targeted chunk reads.

**Domain and story map stay in sync.** Concepts participate in stories as callers/receivers; state flows through Pre-Condition, Triggering-State, Resulting-State. When you add or revise an interaction, derive or update concepts accordingly. Do not edit one view without the other.

Epics come from context. Keep ~4–9 children per node. Use representative examples to illustrate structure; do not enumerate every variant. Derive domain from interactions.

---

## Inputs

- `map-model-spec.json` — the evolving output (Step 4 created it; Step 5 enriched it with chunk_evidence; Step 6 deepens it)
- `context/context_chunks.json` — full corpus; read only chunks listed for each pair (`chunk_ids.identified`, `chunk_ids.provisional`, `concept.chunk_ids`)
- `open_questions` and `cross_cutting_notes` in map-model-spec.json — resolve or re-flag

---

## Chunk Strategy Per Module/Epic

**Discrete, dedicated passes.** Each module/epic pair is processed in a **single, self-contained pass**. No interleaving. No mixing context from one pair into another. Complete one pair fully — deepen concepts, deepen stories, sync — before starting the next.

**One pass = one pair.** For each pass:

1. Read from `map-model-spec.json` — `chunk_ids.identified` and `chunk_ids.provisional` for this pair; `concept.chunk_ids` or `concept.chunk_evidence` for each concept. Use these chunks.
2. **Read deferred chunks** — for any `[defer]` item in this pair, read the cited chunk and resolve
3. **Do not re-sample** — use the index. The output already decided what belongs where.
4. **Update map-model-spec.json** — write the deepened pair back into map-model-spec.json. Do not carry forward in-memory context to the next pass.

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

**On domain–story map sync:**
- Concepts participate as callers/receivers in stories. State flows through Pre-Condition, Triggering-State, Resulting-State.
- **DO NOT** edit only the story map and skip the Domain Model. Interaction changes often imply concept changes.
- Example (right): Epic "Make Checks" has inline Concepts: `Check: targetNumber, roll(dice): Result`; `DifficultyClass: value`. After revising an interaction that touches CheckResult, add CheckResult to both.

---

## Flagging

**`[defer]`** — resolved in Step 6 by targeted read. If still unresolved after read, keep in `open_questions` with reason.

**`[uncertain]`** — requires human confirmation. Do not proceed on it without confirmation.

**`[cross-cutting]`** — remains in `cross_cutting_notes` until Step 7. Do not assign to one module yet.

---

## Process Per Module/Epic Pair

**Pass 1 — Resolve deferrals.** For each `[defer]` in this pair, read the cited chunk. Decide: subtype vs enum.

**Pass 2 — Deepen concepts.** From interactions and stories: add properties, operations, invariants. Derive from evidence; do not invent.

**Pass 3 — Deepen stories.** Add Trigger, Response, Pre-Condition, Failure-Modes. Ground in `**Concept**`. Group into sub-epics if needed (~4–9 children).

**Pass 4 — Sync.** Ensure every concept in the module appears in at least one story. Ensure every story references a concept. Update domain model if interaction changes.

---

## Rules

These rules apply after you have deepened each pair. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Chunks must be referenced (reuse)
*Scanner: `scanners/chunks_must_be_referenced.py` → Rule: `chunks-must-be-referenced.md`*

**DO** ensure every concept, property, operation, story, trigger, response, pre-condition has chunk evidence.

**DO NOT** populate a field without evidence. Use `[defer]` if evidence exists but was not fully read.

---

### No duplicates (reuse)
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO NOT** have two concepts with the same name within a module. **DO NOT** have two modules with the same name.

---

### Epic requires confirming stories (reuse)
*Scanner: `scanners/epic_requires_confirming_stories.py` → Rule: `epic-requires-confirming-stories.md`*

**DO** include at least 2 story names per epic. At Step 3, stories have full Trigger/Response; confirming_stories is the list of story names.

---

### No junk concepts (reuse)
*Scanner: `scanners/no_junk_concepts.py` → Rule: `no-junk-concepts.md`*

**DO NOT** use section headers, all-caps labels, proper nouns, instruction phrases as concept names.

---

### Concepts must have owns
*Scanner: `scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field — one sentence on what decision or rule this concept owns.

**DO NOT** leave a concept with only chunk_ids and no decision ownership.

---

### Stories must have trigger and response
*Scanner: `scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has `trigger` (Actor + action) and `response` (system or other actor).

**DO NOT** leave a story with only a name. Trigger and response ground the story in domain.

---

### Domain–story map sync
*Scanner: `scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept in the module participates in at least one story (trigger, response, or pre-condition).

**DO NOT** have orphan concepts — concepts that appear in the domain model but in no story.

---

### Hierarchy sizing (approximately 4–9 children)
*Scanner: `scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

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

### `map-model-spec.json` (updated)

Same shape as before, but with:
- Concepts: full properties, operations, invariants, relationships
- Stories: trigger, response, pre_condition, failure_modes
- Sub-epics where needed
- `open_questions` and `cross_cutting_notes` updated (resolved items removed)

### `map-model-spec.md` (updated)

One section per pair, with full concept and story detail.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

Run all Step 4 scanners plus Step 6 scanners:

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
| `scanners/chunks_must_be_referenced.py` | `chunks-must-be-referenced.md` | Every evidence claim cites a chunk |
| `scanners/no_duplicates.py` | `no-duplicates.md` | No duplicate concept or module names |
| `scanners/epic_requires_confirming_stories.py` | `epic-requires-confirming-stories.md` | Every epic has ≥2 stories |
| `scanners/no_junk_concepts.py` | `no-junk-concepts.md` | No junk concept names |
| `scanners/concepts_have_owns.py` | `concepts-must-have-owns.md` | Every concept has `owns` |
| `scanners/stories_have_trigger_response.py` | `stories-must-have-trigger-response.md` | Every story has trigger and response |
| `scanners/domain_interaction_sync.py` | `domain-interaction-sync.md` | Every concept in at least one story |
| `scanners/hierarchy_sizing.py` | `hierarchy-approximately-4-to-9-children.md` | ~4–9 children per node |

### Pass 2 — Build chunk index (code)

```
python scripts/build_chunk_index.py --input map-model-spec.json --output mms-chunk-index.json
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
4. Does domain and story map stay in sync?

---

# Step 7 — Integrate and Harmonize

## Purpose

Unify naming, wire cross-module relationships, resolve `[cross-cutting]` items, and finalize subtypes/enums. Produces a clean, consistent scaffold ready for evidence extraction.

---

## Inputs

- `map-model-spec.json` — deepened output from Step 6
- `mms-chunk-index.json` — reverse chunk index

---

## Tasks

1. **Unify naming** — Resolve synonyms, standardize terminology across modules. Ensure concept names are consistent where they refer to the same thing.

2. **Wire cross-module relationships** — For each `[cross-cutting]` item in `cross_cutting_notes`: assign to a primary module or create a shared module; add explicit `relationships` between concepts across modules.

3. **Resolve [cross-cutting]** — Move resolved items out of `cross_cutting_notes`. Document decisions in `open_questions` if human input was needed.

4. **Finalize subtypes and enums** — For deferred subtype candidates: create subtype concepts or confirm enum. For enum decisions: ensure `EnumType {val1, val2}` is applied consistently.

---

## Rules

These rules apply after canonicalization. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Cross-cutting resolved
*Scanner: `scan_cross_cutting_resolved.py` → Rule: `cross-cutting-resolved.md`*

**DO** resolve every item in `cross_cutting_notes` — assign to a primary module, create a shared module, or document in `open_questions` if human input is needed.

**DO NOT** leave unresolved `[cross-cutting]` items. The scaffold must be clean before evidence extraction.

---

### No duplicates (reuse)
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept names remain unique within their module after unification. **DO** ensure module names remain unique across the output.

**DO NOT** introduce duplicates when unifying synonyms — merge into one concept with combined chunk_ids.

---

### Domain–story map sync (reuse)
*Scanner: `scan_domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story after cross-module wiring.

**DO NOT** break sync when assigning cross-cutting concepts — update stories to reference the concept in its new home.

---

### Hierarchy sizing (reuse)
*Scanner: `scan_hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range. Subtype additions must not violate hierarchy sizing.

---

### Concepts must have owns (reuse)
*Scanner: `scan_concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept (including new subtypes) has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scan_stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story retains trigger and response after canonicalization.

---

### Subtypes and enums finalized (AI-only)
*(AI-only — no scanner)*

**DO** resolve all deferred subtype/enum decisions. Create subtype concepts or apply `EnumType {val1, val2}` consistently.

**DO NOT** leave `[defer]` for subtype/enum in the output. Step 5 produces the canonical scaffold — no deferred structural decisions.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scan_cross_cutting_resolved.py --input map-model-spec.json
python scripts/scan_no_duplicates.py --input map-model-spec.json
python scripts/scan_domain_interaction_sync.py --input map-model-spec.json
python scripts/scan_hierarchy_sizing.py --input map-model-spec.json
python scripts/scan_concepts_have_owns.py --input map-model-spec.json
python scripts/scan_stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Build chunk index (code)

If structure changed:

```
python scripts/build_chunk_index.py --input map-model-spec.json --output mms-chunk-index.json
```

### Pass 3 — Adversarial validation (AI)

- Any cross-cutting item left unresolved?
- Any synonym unification that merged distinct concepts?
- Any subtype that should have been an enum (or vice versa)?
- Any cross-module relationship missing or incorrect?

---

## Output

- `map-model-spec.json` — updated with unified names, cross-module relationships, resolved cross-cutting items, finalized subtypes/enums
- `mms-chunk-index.json` — updated if structure changed (re-run `build_chunk_index.py`)

---

# Step 8 — Evidence

## Purpose

Extract structured evidence from the codebase (or corpus) guided by the concept list in `map-model-spec.json`. Evidence feeds into Step 9 for full model construction.

**Status:** The extractor script is not yet implemented. The process below describes the intended behavior. Until implemented, evidence files must be produced manually or by an external tool; scanners validate the output.

---

## Inputs

- `map-model-spec.json` — canonical scaffold with concept list
- Source corpus (code, docs, or context directory: `context_index.json` + `chunks/*.md`)

---

## Corpus Scope

**Scan the full corpus.** Step 8 is code-based extraction across **all chunks** in the context directory (`chunks/*.md`). Do not limit to chunks indexed in mms-chunk-index.json. This step is where corpus coverage expands beyond the 30% sampled in Step 4. For each concept in the scaffold, search the entire corpus for evidence.

---

## Process

Code-based extraction. For each concept in the scaffold:

1. **Actions** — Identify operations, methods, or behaviors that the concept participates in.
2. **Decisions** — Identify decision points, branching logic, or rule enforcement.
3. **States** — Identify state transitions, properties, or lifecycle phases.
4. **Relationships** — Identify collaborators, callers, receivers, containment.

Extraction is guided by the concept list — do not invent concepts; extract evidence for concepts already in the scaffold.

---

## Rules

These rules apply to the evidence extraction output. Step 6 is code-based; scanners validate the evidence files before Step 7.

Full rule files: `rules/`

---

### Evidence files exist
*Scanner: `scan_evidence_files_exist.py` → Rule: `evidence-files-exist.md`*

**DO** produce all four evidence files: `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`.

**DO NOT** skip a file — Step 7 expects all four. Empty `{}` or `{"concepts": {}}` is valid when no evidence found.

---

### Evidence references scaffold concepts only
*Scanner: `scan_evidence_scaffold_refs.py` → Rule: `evidence-scaffold-refs.md`*

**DO** ensure every concept_id (or concept key) in evidence files exists in the scaffold (`map-model-spec.json`).

**DO NOT** invent concepts in evidence — extract only for concepts already in the canonical scaffold.

---

### Evidence schema valid
*Scanner: `scan_evidence_schema.py` → Rule: `evidence-schema-valid.md`*

**DO** produce valid JSON. Each file should have a structure that maps concepts to evidence entries (e.g. `{"ConceptName": [...]}` or `{"concepts": {"ConceptName": [...]}}`).

**DO NOT** produce malformed JSON or files that cannot be parsed by Step 7.

---

## After Extraction — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/evidence_files_exist.py
python scripts/scanners/evidence_scaffold_refs.py
python scripts/scanners/evidence_schema.py
```

Review each violation. Fix extraction logic. Re-run until all scanners report PASS.

---

## Output

- `evidence/actions.json` — actions per concept
- `evidence/decisions.json` — decisions per concept
- `evidence/states.json` — states and transitions per concept
- `evidence/relationships.json` — cross-concept relationships

---

# Step 9 — Structure

## Purpose

AI builds the full model from the canonical scaffold plus evidence. Properties, operations, inheritance, stories, and steps are populated from `map-model-spec.json` and `evidence/`.

---

## Inputs

- `map-model-spec.json` — canonical scaffold from Step 7
- `evidence/` — actions.json, decisions.json, states.json, relationships.json

---

## Process

AI phase. Read the scaffold and evidence. For each module/epic pair:

1. **Domain model** — Populate properties, operations, invariants from evidence. Assign types. Add inheritance where subtypes are finalized.
2. **Story map** — Populate stories with Trigger, Response, Pre-Condition, Failure-Modes. Add scenarios and steps. Ground in `**Concept**`.
3. **Sync** — Ensure every concept participates in at least one story. Ensure every story references concepts.

---

## Rules

These rules apply after structuring. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Use evidence where available (AI-only)
*(AI-only — no scanner)*

**DO** populate properties, operations, and invariants from `evidence/` when evidence exists for a concept.

**DO NOT** ignore evidence — Step 7 merges scaffold with evidence. Empty evidence for a concept is acceptable; populated evidence must be reflected.

---

### No duplicates (reuse)
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept and module names remain unique.

---

### Domain–story map sync (reuse)
*Scanner: `scan_domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story.

---

### Hierarchy sizing (reuse)
*Scanner: `scan_hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range.

---

### Concepts must have owns (reuse)
*Scanner: `scan_concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scan_stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has trigger and response.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Adversarial validation (AI)

- Any evidence ignored when it should have been used?
- Any property or operation invented without evidence?
- Any concept with evidence that has no properties/operations populated?

---

## Output

- `map-model-spec.json` — structured (full domain model + story map)

---

# Step 10 — Finalize

## Purpose

AI phases: behavior, variation, consolidate, assess, finalize. Produce the validated map-model-spec.

---

## Inputs

- `map-model-spec.json` — structured output from Step 9

---

## Phases

1. **Behavior** — Assign operations to concepts. Link behaviors to steps. Group steps into scenarios.

2. **Variation** — Split stories by subtype when mechanics differ. Add failure modes where evidenced.

3. **Consolidate** — Fix anti-patterns (anemia, over-centralization). Add examples where appropriate.

4. **Assess** — Produce assessment: consistency, coverage, completeness, type-field-vs-subtype. Flag gaps.

5. **Finalize** — Apply assessment fixes. Produce validated `map-model-spec.json`.

---

## Rules

These rules apply after finalization. All structural rules from earlier steps still apply. Step 7 adds final-quality checks.

Full rule files: `rules/`

---

### No anemia (AI-only)
*(AI-only — no scanner)*

**DO** ensure concepts that own decisions have operations that enact those decisions. Avoid anemic concepts — data bags with no behavior.

**DO NOT** leave concepts with only properties and no operations when the domain clearly implies behavior.

---

### No over-centralization (AI-only)
*(AI-only — no scanner)*

**DO** distribute responsibility across concepts. Prefer composition over a single "manager" or "service" concept.

**DO NOT** create a central concept that does everything — spread operations to the concepts that own the decisions.

---

### Assessment complete (AI-only)
*(AI-only — no scanner)*

**DO** produce an assessment covering: consistency (naming, types), coverage (all concepts in stories), completeness (no [defer] left), type-field-vs-subtype (correct representation).

**DO NOT** skip assessment. Document gaps and apply fixes before declaring final.

---

### All structural rules (reuse)

Run the same scanners as Step 6. The final output must pass all structural checks:

```
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

Run all structural scanners. Fix violations.

### Pass 2 — Adversarial validation (AI)

- Any anemic concepts?
- Any over-centralized design?
- Assessment complete? All gaps documented and addressed?

---

## Output

- `map-model-spec.json` — final, validated
- `map-model-spec.md` — readable summary (optional)

