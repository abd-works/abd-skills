<!--
  AGENTS.md — GENERATED FILE. Do not edit by hand.
  Assembled from: parts/*.md and parts/steps/built/*.md (see scripts/build_agents.py).
  Regenerate: python scripts/build.py  (from skills/abd-maps-models-specs)
-->

> **Generated document.** This file is built from `parts/` and `parts/steps/built/`. Edit step sources under `parts/steps/<name>.md` or top-level parts, run `python scripts/build.py`, then use this file as the agent instruction bundle.

---

# Process — Maps-Models-Specs

Pipeline: Context → Foundational spine → Modules/epics scaffold (breadth) → Classify → Deepen → Integrate → Evidence → Structure → Finalize.

**Core principle:** Discover taxonomy layer by layer, top-down, with evidence indexed as you go. Each pipeline step is a separate AI or code pass. Scanners enforce structure mechanically. AI resolves violations — scanners never propose fixes.

**Prerequisites:** Stage 1 — source documents (PDF, DOCX, PPTX, etc.). Stage 2+ — `context_index.json` and `chunks/*.md` under **`context_path`** from `solution.conf` (default `<output_dir>/context`).

**Config:** `skill-config.json` must set **`solution_workspace`** (workspace root with **`solution.conf`**). In `solution.conf`, **`output_dir`** holds map-model-spec.\*, mms-chunk-index.json, evidence/, summary.md, relationships.md, generated/; **`context_path`** holds context_index.json and chunks/. See `conf/README.md`. Scripts fail if workspace is missing or invalid.

**Two parallel artifacts produced at every pipeline step:**

- **Domain model** — modules, concepts, properties, operations (what things are and own)
- **Story map** — epics, sub-epics, stories, acceptance criteria, specifications, examples (what actors do and what changes)

These are two views of the same coin and must be produced simultaneously. **Epics matter for scope and flow, but they are empty if they do not verify the domain** — every epic **`statement`** and **`confirming_stories`** name must **ground in `concepts[].name`** and **chunks**; otherwise the story map is labels without a model underneath.

**Output files (under `output_dir`; single evolving spec):**

- `map-model-spec.json` — forward index (foundational spine; modules/epics scaffold breadth; classify; deepen; integrate; evidence; structure and finalize — see Stage 2–3 tables below)
- `map-model-spec.md` — human-readable summary (**layout:** fill from JSON using **`parts/templates/map-model-spec.md.template.md`**)
- `mms-chunk-index.json` — reverse index (chunk_id → concepts, epics, stories, modules). **Code-only:** run `build_chunk_index.py` after **Modules and Epics**, **Concept Classes and Stories**, or **Integrate and Harmonize** — each has a **Build chunk index** row in the Stage 2 table (**5a**, **7a**, **8a**). AI steps do not run it.
- **Concept Classification (code)** (row **6a**) also writes **`summary.md`**, **`relationships.md`** (same directory as the spec, unless a script overrides).

**Step specs** (same pattern as solution modeler `pieces/phases/`): Clean instructions live in `parts/steps/<name>.md`. **Agents use the built files** in `parts/steps/built/<name>.md` (base + rules baked in). Do not edit `built/` by hand. After changing a step or any rule, run `python scripts/build.py` (or `build_agents.py`).

---

## Stage 1: Extract Context


| #   | Step        | Initiator    | Script                        | What it does                                                   | Coverage       | Ref                   | Inputs           | Outputs                         |
| --- | ----------- | ------------ | ----------------------------- | -------------------------------------------------------------- | -------------- | --------------------- | ---------------- | ------------------------------- |
| 1   | **Convert** | Human → Code | convert_to_markdown.py        | Source → markdown                                              | Creates corpus | [context](parts/context.md) | Source folder    | markdown                        |
| 2   | **Analyze** | AI           | discover_context_structure.py | Analyze markdown → markers for headers, tables, sections, TOC, | —              | [context](parts/context.md) | markdown         | solution.conf                   |
| 3   | **Parse, curate, chunk, index** | Code | parse_and_curate.py | Parse → **curate** (classify, exclude) → chunk → index          | —              | [context](parts/context.md) | markdown         | chunks/*.md, context_index.json |

**Curate note:** Curate is **not** a separate script step. The script parse_and_curate.py does all of: parse markdown to blocks; **curate** (classify evidence_type, assign document_region, exclude noise and out-of-scope sections); purpose-built chunking and merge; write chunks and context_index.json. Excluded blocks are listed in context_index.json under `excluded` and are not written to chunks.


---

## Stage 2: Map and Model (rows 4–8)

Rows **4** and **5** are **two separate AI passes** (foundational spine vs. modules/epics scaffold breadth), not two halves of one pass.

| #   | Step                              | Actor | Script                                    | What it does                                                                                                                  | Coverage               | Ref                                                   | Inputs                                    | Outputs                                           |
| --- | --------------------------------- | ----- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| 4   | **Foundational mechanisms**       | AI    | —                                         | **Before** chunk-heavy scaffold work: from `context_index.json` + document headings/TOC, identify **3–7 foundational mechanisms**. **Spine = `concepts[]` per area** (named domain objects/mechanisms + citations), not module/epic labels alone; epics/`confirming_stories` ground in **`concepts[].name`**. Write **`modules_and_epics`** rows (`foundational`, `evidence_stage: hypothesis` on concepts); attach provisional citations; **human checkpoint** — then run **Modules and Epics** (row 5). | Skim / structure       | [modules-epics-foundational-spine (built)](parts/steps/built/modules-epics-foundational-spine.md) | context (index + corpus skim)             | map-model-spec.json                               |
| 5   | **Modules and Epics**             | AI    | —                                         | **After** foundational spine gate: orientation pass; **full-read ~30%** of corpus (**K ≈ round(0.3N)** chunks, breadth); expand **`modules_and_epics`** with cited candidates, epics/stories, layering, per-module **`depends_on`**; scanners; hand off for review. Advance `evidence_stage` toward **`scaffolded`** where chunks substantiate. **`confirming_stories`:** add **as many** names as needed to validate foundational concepts — **not** a default of two. Use interactive AI (optionally **batches / sub-agents** per [modules-epics-scaffold-breadth](parts/steps/built/modules-epics-scaffold-breadth.md)). | ~K full reads          | [modules-epics-scaffold-breadth (built)](parts/steps/built/modules-epics-scaffold-breadth.md) | context/, map-model-spec.json             | map-model-spec.json, map-model-spec.md            |
| 5a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | map-model-spec.json                       | mms-chunk-index.json                              |
| 6   | **Concept Classification**        | AI    | classify_chunks.py (Pass 1)               | AI reads chunks (or configured %); extracts concepts and relationships                                                        | All chunks             | [concept-classification (built)](parts/steps/built/concept-classification.md)   | map-model-spec.json, context/             | map-model-spec.json                               |
| 6a  | **Concept Classification (code)** | Code  | classify_chunks.py (Pass 2); summarize.py | Code scans chunks; extracts concepts and relationships, merges gaps with AI pass; summarize.py → summary.md, relationships.md | All chunks             | [concept-classification (built)](parts/steps/built/concept-classification.md)   | map-model-spec.json                       | map-model-spec.json, summary.md, relationships.md |
| 7   | **Concept Classes and Stories**   | AI    | —                                         | Deepen classes/stories per module/epic; resolve [defer] tags                                                                  | Chunks per Module/Epic | [concept-classes-stories (built)](parts/steps/built/concept-classes-stories.md) | map-model-spec.json, context/             | map-model-spec.json                               |
| 7a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | map-model-spec.json                       | mms-chunk-index.json                              |
| 8   | **Integrate and Harmonize**       | AI    | —                                         | Unify naming; wire cross-module; resolve [cross-cutting]; finalize subtypes                                                   | —                      | [integrate-harmonize (built)](parts/steps/built/integrate-harmonize.md)         | map-model-spec.json, mms-chunk-index.json | map-model-spec.json                               |
| 8a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | map-model-spec.json                       | mms-chunk-index.json                              |


---

## Stage 3: Specification


| #   | Step          | Actor | Script                | What it does                                                                   | Coverage   | Ref                       | Inputs                         | Outputs             |
| --- | ------------- | ----- | --------------------- | ------------------------------------------------------------------------------ | ---------- | ------------------------- | ------------------------------ | ------------------- |
| 9   | **Evidence**  | Code  | TBD (not implemented) | Mine complete context for actions, decisions, states, relationships            | All chunks | [evidence (built)](parts/steps/built/evidence.md)   | map-model-spec.json, context/  | evidence/*.json     |
| 10  | **Structure** | AI    | —                     | Finalize Map & model and build steps, scenarios, examples from evidence        | —          | [structure (built)](parts/steps/built/structure.md) | map-model-spec.json, evidence/ | map-model-spec.json |
| 11  | **Finalize**  | AI    | —                     | Assign operations; link behaviors; split by subtype; fix anti-patterns; assess | —          | [finalize (built)](parts/steps/built/finalize.md)   | map-model-spec.json            | map-model-spec.json |


**Built step specs (agents):** [context](parts/context.md), [modules-epics-foundational-spine](parts/steps/built/modules-epics-foundational-spine.md), [modules-epics-scaffold-breadth](parts/steps/built/modules-epics-scaffold-breadth.md), [concept-classification](parts/steps/built/concept-classification.md), [concept-classes-stories](parts/steps/built/concept-classes-stories.md), [integrate-harmonize](parts/steps/built/integrate-harmonize.md), [evidence](parts/steps/built/evidence.md), [structure](parts/steps/built/structure.md), [finalize](parts/steps/built/finalize.md). Edit **`parts/steps/<name>.md`**, then **`python scripts/build.py`** (regenerates `parts/steps/built/` and `AGENTS.md`).

---

# Domain Model

## Purpose

The **domain model** describes the **state and structure** that the story map refers to. It holds **modules** and **domain concepts**: the things that hold state, get operated on, and participate as callers, receivers, and collaborators in interactions. Every `**Concept**` referenced in the story map must exist in the domain model — no drift between tree and model.

## What goes in the Domain Model

- **Modules** — A **grouping of tightly related concepts that collaborate around the same mechanism**. Each module has a name and a list of concepts. Each module typically maps to one area (or page) of the class diagram.
- **Domain concepts** — A **domain concept holds state and can be operated on** (equates to a class in OO code). **Concepts participate as callers, receivers, and collaborators in interactions; state flows through Pre-Condition, Triggering-State, and Resulting-State** in the story map. Each concept has:
  - **Properties** — with types, optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter. **Type selection:** Use `Dictionary<K,V>` when items are accessed by key (name, type, id) — most "has many" relationships where you look up by name. Use `List<T>` only when order matters and items are accessed by position. Default to Dictionary for named domain collections.
  - **Operations** — with optional collaborating concepts and invariants. Interactions in the story map should be reverse-engineerable to operations on the domain model.
  - **Base-Concept** (optional) — parent for inheritance. **Foundational** — tag `[foundational]` for concepts that are the base classes everything else extends from (the stable core).
- **Concept relationships** — When a concept "has" another: **composition** (strong has-a; part cannot exist without whole) or **aggregation** (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.
- **Examples** — At the end of each module, one table per concept, shared scenario linking the module. Scenario column required; qualifier in parentheses after concept name; columns match concept properties.
- **Invariants** — Under the specific property or operation they apply to, not a separate section.

**What does not go in:** Implementation details (APIs, services, databases, UI components, code). No speculation beyond the provided material. Everything at logical/domain level.

---

# Domain Model Format

## Module

A grouping of tightly related concepts that collaborate around the same mechanism. Name + list of concepts; typically maps to one area (or page) of the class diagram.

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
- examples: at end of module, after all concepts; one table per concept; shared scenario links the module
```

## Domain Concept

A domain concept holds state and can be operated on (equates to a class in OO code). Concepts participate as callers, receivers, and collaborators in interactions; state flows through Pre-Condition, Triggering-State, and Resulting-State.

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

### Foundational classes

A **foundational class** is a domain concept tagged `[foundational]`. These are the **base classes that everything else extends from** — the stable core that repeats across the system. Later slices add concepts that extend or use foundational classes; the foundational classes themselves remain stable.

There is one domain model, not separate "foundational" and "full" models. The tag distinguishes core classes from extensions.

Example: in a payments system, Account + Transaction + ValidationRule collaborate the same way whether you're processing a wire transfer, ACH, or direct debit. Those three are foundational. Wire, ACH, and direct debit are extensions added in later slices.

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

- Prefer **composition/aggregation** over inheritance (composition = strong has-a; aggregation = weak has-a where whole has no meaning without multiple instances of the same part).
- **Type selection:** Use `Dictionary<K,V>` when items are accessed by key (name, type, id); use `List<T>` only when order/position matters (e.g. turn order, sequential steps). Default to Dictionary for named domain collections.
- Avoid central "service/manager" concepts.
- Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options.

## map-model-spec.json — scaffold extensions (foundational spine + breadth)

These fields extend the domain view in JSON (see **`parts/process.md`** and **`parts/steps/modules-epics-foundational-spine.md`** / **`parts/steps/modules-epics-scaffold-breadth.md`**). They align markdown **`[foundational]`** tags with machine-readable structure.

| Field | Where | Purpose |
|--------|--------|---------|
| **`phase`** | root | Named pipeline **step** from **`parts/process.md`** (e.g. **`Modules and Epics`**, **`Concept Classification`**) — not a numeric id. |
| **`phase_note`** | root | Optional free-text note (status, counters, session notes). |
| **`module.foundational`** | `module` | `true` when this row carries the **foundational spine** (3–7 mechanisms); omit or `false` for peripheral modules. |
| **`module.depends_on`** | `module` | Array of `{ dependent_concepts, module, provides_concepts, reason }` — consumer → provider (see rule **`module-depends-on`**). |
| **`concept.evidence_stage`** | each `concept` | `hypothesis` (foundational spine / early scaffold breadth) → `scaffolded` (breadth **K** reads) → `deepened` (concept classes and stories). |
| **`concept.foundational`** | each `concept` | `true` for stable core types that repeat across mechanisms (same intent as **`[foundational]`** in prose). |
| **`concept.extends`** | each `concept` | Optional string: **immediate superclass** concept name. Maps prose **`### **Child** : Parent**`** — the parent named after the colon. **Omit** (or `null`) for root/base concepts in a hierarchy. Parent must exist elsewhere in **`modules_and_epics`** (any module); **`no-duplicates`** keeps names unique. If inheritance is real but parent lives in another module, still set **`extends`** and ensure **`depends_on`** / **`open_questions`** reflect the cross-module edge. |

**Inheritance in JSON vs markdown**

| Markdown (`parts/domain.md` — Domain Concept) | `map-model-spec.json` |
|-----------------------------------------------|------------------------|
| `### **SkillCheck** : **Check**` | `"name": "SkillCheck", "extends": "Check"` |
| `### **Check**` (no parent named) | no **`extends`** field (root for that branch) |

**Composition vs extends:** “has-a” (properties referencing other concepts) stays in **`properties[]` / `operations[]`** with collaborating types. “is-a” subtype layering uses **`extends`** plus shared **`owns`** / evidence on the child.

Epic and confirming-story naming still follow **`parts/story-map.md`**; module naming stays **noun phrase**, epic/story **Verb Noun** (rule **`verb-noun-module-epic-story`**). **`concepts[].name`** and domain words in **`epic.statement`** / **`confirming_stories`** must match **exactly (100%)** — rule **`scaffold-concept-story-name-alignment`**; non-negotiable.

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

## Example — Domain model for country-specific payment

A single module with several concepts that collaborate around payment by country and type (e.g. wire, ACH). Structure only; examples tables would follow the same format as above.

```
## Module: Payment
- concepts — **Country**, **PaymentType**, **UserPaymentAccess**, **PaymentDetails**, **User**, **Session**, **PaymentTypeFieldTypes**

### **Country**
- String country_code
- String country_name
- lookup(code) → **Country**
- list_available() → List<**Country**>

### **PaymentType**
- String payment_type {wire, ach, …}
- List<**PaymentTypeFieldTypes**> fields
- get_fields_for_type(payment_type) → fields
- validate_availability_for_country(**Country**, payment_type) → Boolean

### **UserPaymentAccess**
- String user_name
- **Country** country
- **PaymentType** payment_type
- Boolean available
- check(**User**, **Country**, **PaymentType**) → Boolean

### **PaymentDetails**
- **PaymentType** payment_type
- Number amount
- String currency
- String beneficiary_id
- String swift_code | routing_number, account_number (type-specific)
- validate() → Boolean
- submit() → result

### **User**
- String user_name
- String user_role
- has_session() → Boolean
- has_access(**Country**, **PaymentType**) → Boolean

### **Session**
- String session_id
- Instant expires_at
- is_active() → Boolean
- extend() → void

### **PaymentTypeFieldTypes**
- String payment_type
- List<String> fields
- get_fields(payment_type) → List<String>
```

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

# Story Map (Interaction Tree)

A **story map** is a hierarchy of **interactions**. An **interaction** is a single meaningful exchange between two actors that results in either retrieval of state or a change of state.

## Purpose

The story map captures **who does what, in what order, under what conditions**. It is the user- and value-facing view: epics group capabilities, stories are the smallest independently deliverable, testable behaviors, and steps are atomic interactions. Every epic, story, scenario, and step is grounded in domain language via `**Concept**`; every such concept must exist in the domain model.

**Epics are important** (scope, actors, grouping) **but meaningless if they do not verify the domain** — an epic that does not **name and exercise** real **`concepts[]`** (same spelling as the domain model) and **evidence** is organizational noise, not design.

## What goes in the Story Map

**The interaction (unit):** Each node is an interaction with: **Name** (verb-noun or subject-qualifier); **Statement** (one-sentence trigger and response; use `**Concept**` in the statement). **Pre-Condition** — label only; what must be true before the interaction; state qualifies through the label; use `**Concept**`. **Trigger** — Triggering-Actor, Behavior (label), Triggering-State (state that qualifies the interaction; e.g. selecting an option of a certain type); labels reference domain concepts; examples live on the interaction. **Response** — Responding-Actor, Behavior (label), Resulting-State (state that results); labels reference domain concepts; examples live on the interaction. **Examples** — collection of tables at the interaction level; one per concept referenced in labels; Pre-Condition, Trigger, and Response reference these through their labels. **Failure-Modes** — up to three; how the exchange can fail (rule/state based only). **Constraints** — zero or more; qualitative instructions on how the interaction is shaped; may be a sentence, a file reference, or (commonly) a markdown file; constraints are inherited from parent to child. **Children** — child interactions.

**State** qualifies an interaction through its **label** — a description of the condition. The interaction's **Examples** (tables) live on the interaction; labels reference the domain concepts that correspond to those tables.

**Node hierarchy:**
- **Epic** — Can nest: epic children (sub-epics) or story children. Names typically verb-noun. **Statement:** describes the *scope* of the epic (broad flows it encompasses), not a single interaction.
- **Sub-Epic** — An epic whose parent is an epic; logical grouping of related stories; a feature area, not a behavior itself.
- **Story** — The **backbone** of the map. Smallest unit of testable value that is independently deliverable. Has a triggering actor, a responding actor, and produces observable state change; if it has no actor and no state change, it is not a story. **Statement:** one trigger and response. Everything below the story (scenarios, steps, examples) **belongs to the story**. Epic and sub-epic exist to **group stories**; they are organizational structure, not the primary unit of value.
- **Scenario** — Groups steps; optional container for a story. Names describe the primary conditions tested (e.g. success path, failure path). Split scenarios when pre-conditions differ, success vs failure paths, or different branches.
- **Step** — Atomic interaction within a scenario; one action by one actor. **Statement:** often When (Trigger) and Then (Response). Identify separate steps when: explicit action-reaction, actor or response changes, or when enumerating permutations (validation paths, branches, edge cases).

**Name and statement (all nodes):** Use active verb language. Short name first, longer statement in brackets. Format: `Node: Short Name (Longer statement.)` — e.g. `Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays list of **Country** options.)`

**Domain grounding:** Every epic, story, scenario, and step must be grounded in domain language. Use `**Concept**` in labels (name, statement, pre-condition, trigger, response). Avoid generic terms — use `**Country**`, `**PaymentType**`, not "country" or "payment type". Concepts are placed at the level where they apply to all descendants. Every `**Concept**` must exist in the domain model as **`concepts[].name`** with the **identical spelling** — **100% match**, **non-negotiable**. No drift, no synonyms in story text when the model has fixed a canonical name.

**Inheritance:** Child nodes inherit from parents (actors, pre-condition, examples, domain concepts, constraints). Use `[brackets]` for inherited values (e.g. `Triggering-Actor: [User]`, `Examples: [Logged In User, Active Session]`) so readers see what applies. Never use `Pre-Condition: [inherited]` alone — always include the label. Put shared concepts at epic level; story-specific concepts at story level.

---

# Story Map Format

## Hierarchy

Each node is an interaction. Epic → Sub-Epic (or Epic) → Story → Scenario → Step. Epics can nest (epic children = sub-epics).

| Node | Meaning | Heading |
| ----- | ----- | ----- |
| Epic | Large domain capability — a major area of the system. Groups stories; statement = scope (broad flows), not a single interaction. | `# Epic: <name> (<statement>)` |
| Sub-Epic | An epic whose parent is an epic; logical grouping of related stories — a feature area, not a behavior itself. | `## Epic: <name> (<statement>)` |
| Story | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. Statement = one trigger and response. | `### Story: <name> (<statement>)` |
| Scenario | Condition-specific grouping of steps within a story (e.g. success path, failure path). Names describe conditions tested. | `#### Scenario: <name>` |
| Step | Atomic interaction — one action by one actor. When/Then: Trigger as When, Response as Then. | `- Step N: <name> (When/Then <statement>)` |

## Per Interaction

- **Pre-Condition** — label only; what must be true before. Use Given/And for steps. State qualifies through the label; use `**Concept**`. Examples live on the interaction.
- **Trigger** — **Triggering-Actor** (who starts), **Behavior** (label; use When/And for steps), **Triggering-State** (state that qualifies the interaction). Labels reference domain concepts; examples live on the interaction.
- **Response** — **Responding-Actor** (who responds), **Behavior** (label; use Then/And for steps), **Resulting-State** (state that results). Labels reference domain concepts; examples live on the interaction.
- **Examples** — tables at the interaction level; one per concept referenced in labels. Pre-Condition, Trigger, and Response reference these through their labels.
- **Failure-Modes** — bullet list, max 3; rule/state based only (no infrastructure failures).
- **Constraints** — zero or more; qualitative instructions; sentence, file ref, or markdown ref; inherited from parent to child.
- **Domain concepts** — Use `**Concept**` in labels; every concept must exist in the domain model.

### Step format

- **When/Then** — Trigger as When, Response as Then (e.g. `When **User** browses countries; Then **System** displays list of **Country** options`).
- **Vanilla steps** — verb-noun short labels (e.g. `User submits form`, `System validates payment`).

Strategy or scope specifies which format applies.


### Commonly Generated Fields Per Node

| Node | Commonly Generated | Case-by-Case |
|------|--------------------|--------------|
| Epic | Triggering-Actor, Responding-Actor, Name, Pre-Condition | Constraints |
| Story | Trigger, Response, Name, Examples, Pre-Condition, Failure-Modes | Constraints |
| Scenario | Trigger, Response, Pre-Condition, Examples | |
| Step | Trigger, Response, Examples | Constraints (when step-specific) |

## Domain Grounding

Use `**Concept**` in labels (name, statement, pre-condition, trigger, response). Place concepts at the level where they apply to all descendants. Avoid generic terms — use `**Country**`, `**PaymentType**`, not "country" or "payment type". Every concept must exist in the domain model; **spelling must match `concepts[].name` exactly (100%)** — **non-negotiable** (rule **`scaffold-concept-story-name-alignment`** at scaffold). No drift.

**Scaffold JSON (`confirming_stories[]` on an epic):** Include **as many** story **names** as you need so foundational concepts for that epic are exercised — there is **no** “stop at two” rule; two was never a ceiling, only a bad habit.

## Inheritance

Attributes from a parent node are inherited by child nodes. Use **brackets** for inherited values so readers see what applies: `Triggering-Actor: [User]`, `Responding-Actor: [System]`, `Examples: [Logged In User, Active Session]`. Unbracketed values are defined on the node. If the parent changes, update bracketed values in children.

**Commonly inherited:**
- **Story from Epic:** Triggering-Actor, Responding-Actor, Pre-Condition, Examples (by name), domain concepts.
- **Scenario from Story:** Often nothing needs to be stated explicitly (inherited applies).
- **Step from Story:** Triggering-Actor, Responding-Actor (e.g. [User], [System]). Exception: when a step is system-triggered, that step may override Triggering-Actor.

**Rule:** Put shared concepts at the epic level; add story-specific concepts only at the story level. Only put something at a level if it applies to every descendant.

## Example Tables

Tables **live on the interaction**. One table per concept referenced in Pre-Condition, Trigger, or Response labels. Tables should align with examples in the domain model (same scenario prefix, same columns where applicable).

**Naming:** Name tables by state or condition — "Selected Country", "Approved Payment", "User Payment Type Access" — not generic labels like "Payment" or "Country". When multiple tables for the same concept appear in one step, add a qualifier in parentheses (e.g. `Selected PaymentType (selected, not available for country)`). When inherited, list those names: `Examples: [Logged In User, Active Session, User Payment Type Access]`.

```
ConceptName (qualifier):
| scenario | field1 | field2 |
|----------|--------|--------|
| success  | val1   | val2   |

===
AnotherConcept (qualifier):
| scenario | field1 |
|----------|--------|
| success  | val1   |
```

- **Scenario column** required; use kebab-case (e.g. `success`, `invalid-payment-details`, `payment-type-not-available`)
- **Separator:** `===` between tables; no blank lines between tables
- **Header:** Tables require a header separator row (`|---|---|`)
- **Inherited:** `Examples: [Table Name 1, Table Name 2]`

## Validation Checklist

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- [ ] Trigger: sub-bullets Triggering-Actor, Behavior, Triggering-State (labels reference **Concept**)
- [ ] Response: sub-bullets Responding-Actor, Behavior, Resulting-State (labels reference **Concept**)

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Trigger and Response with [inherited] when from parent

**Example tables**
- [ ] Tables live on the interaction; one per concept referenced in labels
- [ ] Names by state/condition (e.g. Selected Country, Approved Payment); qualifier in parentheses when needed
- [ ] Scenario column required; kebab-case
- [ ] Each table: label, header row, separator row, data rows; `===` between tables

**Hierarchy**
- [ ] Epic → Epic/Story → Scenario → Step
- [ ] Each node touches at least one domain concept via `**Concept**`

---

# Stage 1 — Extract Context

**Prerequisites:** (1) `skill-config.json` sets **required** `solution_workspace` and that directory contains `solution.conf` (see `conf/README.md`). (2) Source documents (PDF, DOCX, PPTX, XLSX, HTML, etc.) in a folder under that workspace (or passed explicitly to scripts).

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

Before naming modules or epics, establish the **domain spine**: the minimal set of concepts and mechanisms without which the rest of the model cannot be read coherently. In [`parts/process.md`](parts/process.md) this is the **Foundational mechanisms** row (Stage 2), separate from **Modules and Epics** (scaffold breadth).

**DO**

- Identify **foundational** concepts: core entities, invariants, and mechanisms that other concepts presuppose. Mark them in JSON with `module.foundational: true` on the module that primarily owns that spine (or split if the spine spans modules — then mark each contributing module).
- Assign every concept an **`evidence_stage`** aligned with [`parts/process.md`](parts/process.md) / AGENTS. Start conservative; promote only when chunk evidence supports it.
- Cite chunks from the first substantive claim (`description_chunk`, `owns_chunk`, `chunk_ids` / `chunk_evidence`) — see `chunks-must-be-referenced.md`.

**Evidence-stage ladder (concept-level)**

Use these values on each `concept` (add `open_questions` when the schema or material is unclear):

| Stage | Meaning |
|--------|---------|
| `hypothesis` | **[Foundational mechanisms](parts/process.md)** or early **[Modules and Epics](parts/process.md)**: named from skim/structure; provisional citations; not yet substantiated by the **K** full-read pass |
| `scaffolded` | **[Modules and Epics](parts/process.md)**: substantiated by the orientation / **K** chunk reads — chunk-anchored names and any `owns` / properties / operations you cite there |
| `deepened` | After **[Concept Classes and Stories](parts/process.md)** (deepen): full properties/operations/invariants from pair chunks (optional until deepen runs) |

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

---

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

Before naming modules or epics, establish the **domain spine**: the minimal set of concepts and mechanisms without which the rest of the model cannot be read coherently. In [`parts/process.md`](parts/process.md) this is the **Foundational mechanisms** row (Stage 2), separate from **Modules and Epics** (scaffold breadth).

**DO**

- Identify **foundational** concepts: core entities, invariants, and mechanisms that other concepts presuppose. Mark them in JSON with `module.foundational: true` on the module that primarily owns that spine (or split if the spine spans modules — then mark each contributing module).
- Assign every concept an **`evidence_stage`** aligned with [`parts/process.md`](parts/process.md) / AGENTS. Start conservative; promote only when chunk evidence supports it.
- Cite chunks from the first substantive claim (`description_chunk`, `owns_chunk`, `chunk_ids` / `chunk_evidence`) — see `chunks-must-be-referenced.md`.

**Evidence-stage ladder (concept-level)**

Use these values on each `concept` (add `open_questions` when the schema or material is unclear):

| Stage | Meaning |
|--------|---------|
| `hypothesis` | **[Foundational mechanisms](parts/process.md)** or early **[Modules and Epics](parts/process.md)**: named from skim/structure; provisional citations; not yet substantiated by the **K** full-read pass |
| `scaffolded` | **[Modules and Epics](parts/process.md)**: substantiated by the orientation / **K** chunk reads — chunk-anchored names and any `owns` / properties / operations you cite there |
| `deepened` | After **[Concept Classes and Stories](parts/process.md)** (deepen): full properties/operations/invariants from pair chunks (optional until deepen runs) |

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

At **[Modules and Epics](parts/process.md)** (scaffold breadth), structure concepts so readers can navigate **general → specific** without mixing levels in one undifferentiated list.

**Layering model**

1. **Base / root** — The umbrella concept for the area (often one per module or sub-area).
2. **Categories / subtypes** — Named partitions or roles under the base (enums, subtypes, or clearly named siblings).
3. **Implementations / specifics** — Concrete variants, policies, or mechanisms that **depend on** the categories.

**Naming**

- Prefer **`SubtypeName : BaseName`** (or equivalent convention already used in this spec) when a concept is a specialization of another — see `classify-variants-before-modeling.md` for variant vs duplicate.

**DO**

- Reflect layering in `concept` names and in **`module.depends_on`** where one module’s concepts presuppose another’s base types (see `module-depends-on.md`).
- Keep **Modules and Epics** scaffold breadth in check: defer exhaustive enumeration of every implementation to **[Concept Classes and Stories](parts/process.md)** (deepen) unless chunks already force them.

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

# Concept Classification

Pipeline placement: **[Concept Classification](parts/process.md)** (Stage 2 — AI + code rows **6** and **6a**).

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
- **Classification (AI):** AI reads every chunk (or configured %), extracts concepts and relationships
- **Classification (code):** Code scanner runs on full text with concept list from the AI pass; merges gaps (catches concepts in text the AI didn't see when chunk-pct < 100%). Then `summarize.py` → `summary.md`, `relationships.md`

**Outputs:** `map-model-spec.json` (updated with evidence), `summary.md`, `relationships.md`

---

## Why so many subtypes are "missing" (Pass 1 coarse-grained)

Pass 1 asks the AI to label each chunk with **primary_concepts** (concept name + module + evidence_type). The model tends to return **coarse** names: e.g. "Effect", "Modifier", "Advantage" rather than every power effect (Damage, Weaken, Healing, …), every advantage type, or every modifier type. So you get a limited set of unique concept names (e.g. 80) that are high-level. The finer-grained subtypes are either lumped under one concept or never named as first-class concepts.

---

## Will **[Concept Classes and Stories](parts/process.md)** find them?

**Sometimes.** **Concept Classes and Stories** **deepens** the concepts you already have and **Pass 1** re-harvests from the pair’s chunks — so **new** names can appear when the classification pass was coarse. The **default** is still: classification broadens coverage across the corpus; **Concept Classes and Stories** **must not** skip **Pass 1** harvest to “only deepen what exists.” If dozens of variants exist only in unclassified chunks, **Concept Classification** coverage matters most.

---

## Design: module-level evidence → then find them

**Your approach is right.** Put evidence at the **module** level (which chunks belong to this module), and have a **later** step read those chunks and discover the subtypes (all power effects, all advantage types, all modifiers).

- **What we have today:** Evidence is attached to **(module, concept)**. We also have **chunk_ids.identified** and **chunk_ids.provisional** per module/epic pair — i.e. the set of chunks that belong to that module. So we already have a module-level view of which chunks are in scope.
- **What’s missing:** A dedicated pass that says: “For this module, read its chunks and extract all subtype concept names (e.g. every effect type, every advantage type, every modifier).” That could be:
  - a new sub-step (e.g. “Discover subtypes from module chunks”), or
  - a variant of **Concept Classes and Stories** (e.g. “Pass 0: from module chunks, discover and add subtype concepts; then deepen as now”).

So: **we didn’t “miss” them forever** — we just didn’t ask Pass 1 to enumerate every subtype. The way to get them is to use the module-level chunk sets we already have and add a discovery step that finds the subtypes. No need to re-run Pass 1 for that; the evidence is already at the module level in `chunk_ids` and in the concept-level evidence for the coarse concepts (Effect, Modifier, Advantage). A later pass can use that to propose and attach finer-grained concepts.

---

## Regression: fewer concepts after "better context extraction" changes

If you used to get **many more** concepts and now get a much smaller set (e.g. ~80), something in the pipeline or inputs changed. **Concept Classes and Stories** **Pass 1** can add missing names from pair chunks, but it does not replace a weak **Concept Classification** corpus pass. So the fix is to find why **Concept Classification** Pass 1 is now returning fewer/different names.

**What drives concept count in Pass 1:**

1. **Seed spec (map-model-spec.json)** — `build_module_context(spec)` sends the AI: for each module, name + description + list of concept names. The **initial** concept list the AI sees is whatever is in the spec when you run **Concept Classification**. If that spec was minimal (e.g. **[Modules and Epics](parts/process.md)** with 30% sample → few concepts), the AI can still add more but may stay coarser. If the spec used to be richer (e.g. from a previous full run or hand-curated list), the AI had more hints and could produce more names.
2. **Chunk content** — The AI gets batches of chunks; each chunk's text is sliced by `chunk_pct` (default 100%). If chunks now have **less text** (e.g. YAML front matter stripped and the body is shorter, or chunking splits more finely), the model sees less evidence per chunk and may name fewer concepts.
3. **Chunk source** — **Concept Classification** loads from either `context_index.json` + `chunks/*.md` (strip YAML, use body) or legacy `context_chunks.json`. If you switched from one to the other, chunk count, order, or content may differ.
4. **chunk_pct** — If you run with `--chunk-pct 50` or `25`, the AI only sees the first part of each chunk; the rest is invisible to Pass 1.

**Checklist to compare before vs now:**

- [ ] **Spec at Concept Classification start** — How many concept names are in the spec when you invoke classify_chunks? If you used to run with a spec that already had many concepts (e.g. from a previous run), that primed the AI. If you now run with a fresh **[Modules and Epics](parts/process.md)** output, that could explain fewer.
- [ ] **Chunk path** — Same `--chunks` as before? (e.g. legacy context_chunks.json vs context_index + chunks/*.md)
- [ ] **Chunk count and sample** — Same number of chunks? For a few chunk IDs, compare length of text sent to the AI (after stripping). Shorter or different text per chunk can reduce discovery.
- [ ] **chunk_pct** — Same value (e.g. 100%)?
- [ ] **Step 3 (parse_and_curate)** — Did "better context extraction" change chunk boundaries, front matter vs body, or exclusions? That would change what the classifier sees.

**Quick diagnostic:** Before the AI pass, log the first 500 chars of `module_context` and the first chunk's full text length. Compare to any saved log or old run to see if inputs (seed concepts + chunk content) are smaller or different.


**At 100%, there is no truncation of chunk text.** The code sends exactly `text[:int(len(text) * chunk_pct/100)]`; when `chunk_pct` is 100, that is the full string. Every chunk’s full text is sent to the AI.

**What the “average length” is used for:** The script samples ~10% of chunks at the configured `chunk_pct`, computes average *sent* size (chars → tokens via `CHARS_PER_TOKEN`), then sets **batch size** so that each batch aims for ~8,000 tokens of chunk text. So “average” is used only to decide *how many chunks per API call*, not to truncate. Oversized chunks (raw length &gt; 15,000 chars) get their own single-chunk batch so one huge chunk doesn’t blow the prompt.

**“Buffer on top of average”:** There is no separate step that “adds a buffer so we never truncate.” We don’t need one for chunk content: at 100% we never cut chunk text. The only way content is shortened is when `chunk_pct` &lt; 100 (e.g. 50% or 25%). So for a run at 100% (e.g. mm3 with `chunk_pct: 100` in run_log.json), **no truncation of input happened**. If you ever want an extra safety (e.g. use 90th percentile + buffer to set a more conservative batch size so total prompt stays well under model context), that could be added; today we rely on the 8k-token target and the 15k-char oversize rule.


---

## Rules (baked in)

Apply these rules when producing output for this step.

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

# Concept Classes and Stories

**This file is the prompt.** **Concept Classes and Stories** (see **[Stage 2](parts/process.md)**) is **AI-authored**: domain and stories must come from **model reasoning**, not from Python heuristics. Two supported ways to run it:

1. **Interactive** — In chat (or an agent with this skill): bring `map-model-spec.json` and the pair’s chunks; follow **Process Per Module/Epic Pair** (Pass 1–4); edit the spec with file tools.
2. **Chat API (listed script)** — `python scripts/deepen_pair_chat_api.py --spec … --chunks … --pair-index N` — same **chunk batching as [Concept Classification](parts/process.md)** (`classify_chunks.py`). **No silo:** each **observation** batch gets the **full module** for the pair plus the **epic slice for that run**. **Default:** `--split-threshold-chars` is **0** → **one** whole pair every time (no sharding — minimize complexity). **Only if** compact pair JSON + batches risk blowing model context, set `--split-threshold-chars` to a positive char limit; then shards use **sub_epic** subtrees or **story batches**, plus one **active chunk cluster** per shard. **Synthesis** per shard returns full `module` + `epic`; the driver **grafts** epic subtrees **by scope**. When **several shards** run, each shard is **pinned** to a **sub_epic** path: the driver **nests** that run’s `module` payload under **`sub_modules`** mirroring that path (story batches use the **parent** sub_epic chain), then **merges** by **sub_module** / **concept** name so sibling branches stay separate namespaces; pair-level **`chunk_ids`** are **unioned**. **`deepen_pair_chat_api_run`** records **`run_boundary`** (`single_run` vs `isolated_runs`), **`module_merge_policy`** (`single_pass_replace` vs `isolated_perspectives_merge_sub_epic_sub_modules`), **`epic_root_name`**, per-shard **`run_boundary_tag`** / **`run_boundary_index`**, **`scope_hierarchy`** (epic → sub_epic → nested → optional stories_batch), **`hierarchy_display`**, **`isolated_runs`**, **`reconciliation_hint`**, and **`module_merge_note`** when multiple shards ran. **`--dry-run`** prints planned shards with hierarchy. Requires `OPENAI_API_KEY` (see `conf/.secrets`). See rule **step6-deepen-ai-only-no-merge-scripts**.

Afterward, **code** runs scanners and `build_chunk_index.py` — separate from the deepen pass.

## Non-negotiable: no unofficial merge scripts for this step

**Do not** write or run **ad-hoc** Python to splice / replay / bulk-inject **Concept Classes and Stories** output. **Do not** fabricate domain text in code. The **only** scripted path for this step is **`deepen_pair_chat_api.py`** (chat API end-to-end), same class as **`classify_chunks.py`**. Otherwise **edit the JSON and MD** in session. Re-running a deepen means a **new** API run or a **new** interactive pass — not a private merge replay tool.

---

## Purpose

Take the spec produced by **[Foundational mechanisms](parts/process.md)** + **[Modules and Epics](parts/process.md)** (module/epic pairs, initial concepts; chunk evidence per concept and per pair), and **deepen** it **one module/epic pair at a time**. The ordered work is defined only in **Process Per Module/Epic Pair** (Pass 1 → Pass 4): complete harvest and deferral resolution → deepen concepts → deepen stories (with hierarchy) → sync domain and story map. Everything else in this doc (**Core Constraints**, **Flagging**, **What to Produce**, **Rules**) supports or constrains those passes — not a second pipeline.

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

**Process ordering:** Order **`modules_and_epics`** pairs using **`module.depends_on`** (from **[Modules and Epics](parts/process.md)**): **topological** sort so **provider** modules (those that export `provides_concepts` others need) are deepened **before** dependents. Where the graph has no order constraint, use judgment: core resolution/flow before setup, config, peripheral — but **never** deepen a dependent before its named providers unless `open_questions` documents an explicit exception.

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

**`[cross-cutting]`** — remains in `cross_cutting_notes` until **[Integrate and Harmonize](parts/process.md)**. Do not assign to one module yet.

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

Run all **[Modules and Epics](parts/process.md)** scaffold scanners plus **Concept Classes and Stories** scanners:

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

---

# Integrate and Harmonize

## Purpose

Unify naming, wire cross-module relationships, resolve `[cross-cutting]` items, and finalize subtypes/enums. Produces a clean, consistent scaffold ready for evidence extraction.

### Domain + story map — relevant excerpts only (full specs: **`parts/domain.md`**, **`parts/story-map.md`**)

*Domain (integrate pass):*

- **Synonym merge:** one **`concepts[].name`**; **union** **`chunk_ids`** / **`chunk_evidence`**; if a merged concept had **`extends`**, ensure the parent **`name`** still exists or repoint **`extends`** after renames (**`parts/domain.md`** — naming + scaffold extensions).
- **Cross-module wiring:** **`depends_on`**, **`provides_concepts`**, and any **`relationships`** stay consistent with **`parts/domain.md`** module boundaries; new shared concepts get **`owns`** + evidence (**`concepts-must-have-owns`**).
- **Subtypes / enums:** align **`extends`** trees and **`EnumType {…}`** property types with finalized decisions (**`parts/domain.md`** — property types).

*Story map (integrate pass):*

- After **moving or renaming** a concept, scan epics/sub-epics/stories: every **`**Concept**`** reference must match a surviving **`concepts[].name`** in the right module (**`parts/story-map.md`** — *Domain Grounding*; scanner **`domain-interaction-sync`**).
- **Hierarchy 4–9** still holds after regrouping (**`parts/story-map.md`** — *Hierarchy* + **`hierarchy-approximately-4-to-9-children`**).

---

## Inputs

- `map-model-spec.json` — deepened output from **[Concept Classes and Stories](parts/process.md)** (Stage 2)
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
*Scanner: `scripts/scanners/cross_cutting_resolved.py` → Rule: `cross-cutting-resolved.md`*

**DO** resolve every item in `cross_cutting_notes` — assign to a primary module, create a shared module, or document in `open_questions` if human input is needed.

**DO NOT** leave unresolved `[cross-cutting]` items. The scaffold must be clean before evidence extraction.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept names remain unique within their module after unification. **DO** ensure module names remain unique across the output.

**DO NOT** introduce duplicates when unifying synonyms — merge into one concept with combined chunk_ids.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story after cross-module wiring.

**DO NOT** break sync when assigning cross-cutting concepts — update stories to reference the concept in its new home.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range. Subtype additions must not violate hierarchy sizing.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept (including new subtypes) has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story retains trigger and response after canonicalization.

---

### Subtypes and enums finalized (AI-only)
*(AI-only — no scanner)*

**DO** resolve all deferred subtype/enum decisions. Create subtype concepts or apply `EnumType {val1, val2}` consistently.

**DO NOT** leave `[defer]` for subtype/enum in the output. **Integrate and Harmonize** must resolve them — no deferred structural decisions in the integrated scaffold.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/cross_cutting_resolved.py --input map-model-spec.json
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
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

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: cross-cutting-resolved
phases: [step5]
order: 50
scanner: scripts/scanners/cross_cutting_resolved.py
impact: HIGH
---

## Cross-cutting concerns must be resolved or explicitly deferred

When the same concept name appears in multiple modules, or when evidence shows shared infrastructure (logging, auth, notifications), document how it is handled — either assign a **home module** with `cross_cutting_notes`, or leave `cross_cutting_notes` empty only when the scanner finds **no** cross-cutting pattern to flag.

The scanner (`scripts/scanners/cross_cutting_resolved.py`) treats **non-empty** `cross_cutting_notes` as a violation until assessment marks the concern handled. Empty notes pass.

**DO** keep `cross_cutting_notes` empty when concepts are cleanly scoped and names do not collide across modules.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": {
        "name": "Payments",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "SettlementBatch",
            "owns": "Owns batching and cut-off times for release",
            "owns_chunk": "chunk-p1",
            "chunk_ids": ["chunk-p1"]
          }
        ]
      },
      "epic": { "name": "Settlement", "stories": [] }
    }
  ]
}
```

**DO** document the resolution in `cross_cutting_notes` when you intentionally share a concept — then clear or update notes in assessment once home module and boundaries are agreed.

```json
{
  "name": "Retail",
  "cross_cutting_notes": "Customer identity: home module is IAM; Retail stores only customerId foreign key — see IAM.CustomerAccount.",
  "concepts": []
}
```

**DO NOT** leave stale placeholder text in `cross_cutting_notes` through final delivery — the scanner flags non-empty notes.

```json
{
  "name": "Retail",
  "cross_cutting_notes": "TODO: figure out auth",
  "concepts": []
}
```

Non-empty — violation until resolved in assessment.

**DO NOT** duplicate the same concept name in two modules without notes.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "CustomerAccount",
            "owns": "Owns cart preferences",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": {
        "name": "IAM",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "CustomerAccount",
            "owns": "Owns credentials and sessions",
            "owns_chunk": "chunk-i1",
            "chunk_ids": ["chunk-i1"]
          }
        ]
      },
      "epic": { "name": "Login", "stories": [] }
    }
  ]
}
```

Same concept name, two modules, empty `cross_cutting_notes` — scanner may flag; assessment must rename, merge, or document.


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

# Evidence

## Purpose

Extract structured evidence from the codebase (or corpus) guided by the concept list in `map-model-spec.json`. Evidence feeds into **[Structure](parts/process.md)** (Stage 3) for full model construction.

**Status:** The extractor script is not yet implemented. The process below describes the intended behavior. Until implemented, evidence files must be produced manually or by an external tool; scanners validate the output.

---

## Inputs

- `map-model-spec.json` — canonical scaffold with concept list
- Source corpus (code, docs, or context directory: `context_index.json` + `chunks/*.md`)

---

## Corpus Scope

**Scan the full corpus.** **Evidence** is code-based extraction across **all chunks** in the context directory (`chunks/*.md`). Do not limit to chunks indexed in mms-chunk-index.json. This step is where corpus coverage expands beyond the **~30%** sampled in **[Modules and Epics](parts/process.md)** (scaffold breadth). For each concept in the scaffold, search the entire corpus for evidence.

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

These rules apply to the evidence extraction output. **Evidence** is code-based; scanners validate the evidence files before **Structure**.

Full rule files: `rules/`

---

### Evidence files exist
*Scanner: `scripts/scanners/evidence_files_exist.py` → Rule: `evidence-files-exist.md`*

**DO** produce all four evidence files: `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`.

**DO NOT** skip a file — **Structure** expects all four. Empty `{}` or `{"concepts": {}}` is valid when no evidence found.

---

### Evidence references scaffold concepts only
*Scanner: `scripts/scanners/evidence_scaffold_refs.py` → Rule: `evidence-scaffold-refs.md`*

**DO** ensure every concept_id (or concept key) in evidence files exists in the scaffold (`map-model-spec.json`).

**DO NOT** invent concepts in evidence — extract only for concepts already in the canonical scaffold.

---

### Evidence schema valid
*Scanner: `scripts/scanners/evidence_schema.py` → Rule: `evidence-schema-valid.md`*

**DO** produce valid JSON. Each file should have a structure that maps concepts to evidence entries (e.g. `{"ConceptName": [...]}` or `{"concepts": {"ConceptName": [...]}}`).

**DO NOT** produce malformed JSON or files that cannot be parsed by **Structure**.

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

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: evidence-scaffold-refs
phases: [step4]
order: 10
scanner: scripts/scanners/evidence_scaffold_refs.py
impact: HIGH
---

## Evidence must reference only scaffold concepts

Extraction is guided by the canonical concept list in `map-model-spec.json`. Evidence files attach chunks and claims to those concept keys. Keys that are not in the scaffold break Step 5 and invalidate traceability.

The scanner (`scripts/scanners/evidence_scaffold_refs.py`) flags concept IDs in evidence files that do not exist in the scaffold.

**DO** ensure every concept key in `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, and `evidence/relationships.json` exists under some `module.concepts[].name` in `map-model-spec.json` (exact spelling).

Scaffold (`map-model-spec.json`):

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "WireTransfer",
            "owns": "Owns customer-initiated wire instruction validation and release",
            "owns_chunk": "chunk-pay-1",
            "chunk_ids": ["chunk-pay-1"]
          }
        ]
      },
      "epic": { "name": "Wire release", "stories": [] }
    }
  ]
}
```

Evidence (`evidence/actions.json`) — top-level keys match concept names:

```json
{
  "WireTransfer": [
    {
      "action": "Customer submits instruction",
      "chunk_ids": ["chunk-pay-1"]
    }
  ]
}
```

Same scaffold, nested `concepts` shape (also accepted by the scanner):

```json
{
  "concepts": {
    "WireTransfer": [
      { "action": "Customer submits instruction", "chunk_ids": ["chunk-pay-1"] }
    ]
  }
}
```

**DO** add the concept to the scaffold in Step 3 (or an explicit intermediate pass) before attaching evidence under that key.

**DO NOT** add evidence for concepts not in the scaffold “because the PDF mentions them” — extend the scaffold first, or file under the nearest existing parent with `[defer]` in the scaffold text.

Scaffold has only `WireTransfer`, but evidence introduces extra keys:

```json
{
  "WireTransfer": [],
  "ACHCredit": [],
  "LimtChecker": []
}
```

`ACHCredit` and `LimtChecker` are not in `module.concepts[].name` — scanner reports orphan keys. (`LimtChecker` is also a typo for `LimitChecker`.)

**DO NOT** use a different naming convention in evidence than in the scaffold.

Scaffold:

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns limit evaluation for payment instructions",
            "owns_chunk": "chunk-lim-1",
            "chunk_ids": ["chunk-lim-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Evidence:

```json
{
  "limit_checker": []
}
```

Key `limit_checker` does not match `LimitChecker` — violation.

The scaffold is the namespace; evidence is annotations on that namespace — not the driver of new concept names without a scaffold update.


---

---
rule_id: evidence-files-exist
phases: [step4]
order: 5
scanner: scripts/scanners/evidence_files_exist.py
impact: HIGH
---

## All four evidence files must exist

Step 4 produces structured evidence for downstream structure and assessment. Step 5 expects a complete set of files. A missing file usually means extraction stopped early or a path was wrong.

The scanner (`scripts/scanners/evidence_files_exist.py`) checks that all four files exist.

**DO** produce these paths under `evidence/`:

- `evidence/actions.json`
- `evidence/decisions.json`
- `evidence/states.json`
- `evidence/relationships.json`

**DO** use empty but valid JSON when a category has nothing to say:

`evidence/relationships.json`:

```json
{}
```

`evidence/decisions.json`:

```json
{}
```

`evidence/states.json`:

```json
{
  "concepts": {}
}
```

`evidence/actions.json`:

```json
{}
```

(Adjust empty shape to match your pipeline’s convention; each file must still parse as JSON.)

**DO NOT** skip a file because “we had no relationships”. Create the file with empty content.

**DO NOT** rename files or invent parallel names — automation depends on fixed paths.

Invalid handoff — only one file on disk:

```
evidence/
  actions.json
```

Missing: `decisions.json`, `states.json`, `relationships.json`.

Wrong contract:

```
evidence/
  actions.json
  actions_v2.json
```

Use the four canonical filenames only.


---

---
rule_id: evidence-schema-valid
phases: [step4]
order: 15
scanner: scripts/scanners/evidence_schema.py
impact: MEDIUM
---

## Evidence files must be valid JSON

Step 5 reads evidence files programmatically. Malformed JSON blocks the structure phase.

The scanner (`scripts/scanners/evidence_schema.py`) validates that each evidence file parses as valid JSON.

**DO** produce valid JSON. Use `python -m json.tool evidence/actions.json` or `python -c "import json; json.load(open('evidence/actions.json'))"` before handoff.

**DO** match the expected shape: an object with concept keys or a `concepts` object mapping concept names to evidence arrays — follow the schema your pipeline documents.

`evidence/actions.json` (valid):

```json
{
  "WireTransfer": [
    {
      "action": "Customer submits instruction",
      "chunk_ids": ["chunk-pay-1"]
    }
  ]
}
```

UTF-8 encoding; no paste artifacts inside strings.

**DO NOT** produce truncated files (copy-paste cut mid-string).

**DO NOT** use JSON5, trailing commas, or comments inside `.json` unless your toolchain explicitly supports them.

Not valid JSON (do not save this inside a `.json` file):

```
{'WireTransfer': []}
```

Not valid JSON:

```
{
  "WireTransfer": [
    {
      "action": "Incomplete
    }
  ]
}
```

Not valid JSON:

```
{
  "WireTransfer": [],
  // TODO: add ACH
}
```

Markdown fenced code pasted into the `.json` file itself — the file on disk must be raw JSON only.


---

---

# Structure

## Purpose

AI builds the full model from the canonical scaffold plus evidence. Properties, operations, inheritance, stories, and steps are populated from `map-model-spec.json` and `evidence/`.

---

## Inputs

- `map-model-spec.json` — canonical scaffold from **[Integrate and Harmonize](parts/process.md)** (Stage 2)
- `evidence/` — actions.json, decisions.json, states.json, relationships.json

---

## Process

AI step. Read the scaffold and evidence. For each module/epic pair:

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

**DO NOT** ignore evidence — **Structure** merges scaffold with evidence. Empty evidence for a concept is acceptable; populated evidence must be reflected.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept and module names remain unique.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

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

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: no-anemia
phases: [step2, step3, step5]
order: 35
scanner: null
impact: MEDIUM
---

## No anemic concepts (manual / assessment)

An anemic concept is a named bucket with no properties, no operations, and a vague `owns` — it does not carry enough structure to validate or implement.

There is **no automated scanner** for this rule in this package. Apply it during adversarial validation and assessment.

**DO** give each concept at least one property or operation when the source supports it, and make `owns` state a specific decision.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Promotion",
            "owns": "Owns which discount rules apply to a cart line and in what order",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"],
            "properties": [
              { "definition": "String code", "chunk": "chunk-r2" },
              {
                "definition": "EnumType stackPolicy { exclusive, additive }",
                "chunk": "chunk-r2"
              }
            ],
            "operations": [
              {
                "definition": "apply(cart: Cart, line: LineItem) -> MoneyAmount",
                "chunk": "chunk-r2"
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

**DO NOT** leave a concept as only a name and generic owns.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Promotion",
            "owns": "Handles promotions",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

No properties, no operations, vague owns — anemic.

**DO NOT** split one cohesive rule across three empty shells.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PromotionRules",
            "owns": "Rules",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          },
          {
            "name": "PromotionEngine",
            "owns": "Engine",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          },
          {
            "name": "PromotionResult",
            "owns": "Result",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Three names, no structure — fold into one concept or add real properties/operations.


---

---
rule_id: no-over-centralization
phases: [step2, step3, step5]
order: 36
scanner: null
impact: MEDIUM
---

## No god object (manual / assessment)

A god object owns every decision in the domain — dozens of unrelated properties and operations on one concept, with other concepts reduced to dumb data holders.

There is **no automated scanner** for this rule in this package. Apply it during adversarial validation and assessment.

**DO** distribute ownership so each concept owns a coherent slice of decisions.

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
            "chunk_ids": ["chunk-r1"],
            "properties": [
              { "definition": "List<LineItem> lines", "chunk": "chunk-r1" }
            ],
            "operations": [
              {
                "definition": "addLine(sku: String, qty: Number) -> void",
                "chunk": "chunk-r1"
              }
            ]
          },
          {
            "name": "TaxCalculator",
            "owns": "Owns jurisdiction rules and tax lines for a cart",
            "owns_chunk": "chunk-r3",
            "chunk_ids": ["chunk-r3"],
            "operations": [
              {
                "definition": "compute(cart: Cart) -> List<TaxLine>",
                "chunk": "chunk-r3"
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

**DO NOT** pile unrelated domains onto one concept.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "OrderSystem",
            "owns": "Owns cart, tax, payment, shipping, inventory, promotions, and user profiles",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"],
            "properties": [
              { "definition": "List<LineItem> lines", "chunk": "chunk-r1" },
              { "definition": "MoneyAmount tax", "chunk": "chunk-r1" },
              { "definition": "String cardToken", "chunk": "chunk-r1" },
              { "definition": "String trackingNumber", "chunk": "chunk-r1" },
              { "definition": "Number stockOnHand", "chunk": "chunk-r1" }
            ],
            "operations": [
              { "definition": "checkout() -> void", "chunk": "chunk-r1" },
              { "definition": "ship() -> void", "chunk": "chunk-r1" },
              { "definition": "chargeCard() -> void", "chunk": "chunk-r1" }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Single concept absorbing cart, tax, payment, shipping, inventory — god object.

**DO NOT** make every other concept an empty DTO while one concept holds all behavior — split by bounded context from the corpus.


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

# Finalize

## Purpose

AI steps: behavior, variation, consolidate, assess, finalize. Produce the validated map-model-spec.

---

## Inputs

- `map-model-spec.json` — structured output from **[Structure](parts/process.md)** (Stage 3)

---

## Activities

1. **Behavior** — Assign operations to concepts. Link behaviors to steps. Group steps into scenarios.

2. **Variation** — Split stories by subtype when mechanics differ. Add failure modes where evidenced.

3. **Consolidate** — Fix anti-patterns (anemia, over-centralization). Add examples where appropriate.

4. **Assess** — Produce assessment: consistency, coverage, completeness, type-field-vs-subtype. Flag gaps.

5. **Finalize** — Apply assessment fixes. Produce validated `map-model-spec.json`.

---

## Rules

These rules apply after finalization. All structural rules from earlier steps still apply. **Finalize** adds final-quality checks.

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

Run the same scanners as **[Concept Classes and Stories](parts/process.md)** (and scaffold scanners as needed). The final output must pass all structural checks:

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


---

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: assessment-complete
phases: [step6]
order: 30
impact: HIGH
---

## Assessment must be produced and applied

**[Finalize](parts/process.md)** (Stage 3) includes an **Assess** activity. There is **no scanner** for this rule — the AI (or human reviewer) must perform it and record the outcome. Skipping assessment ships contradictions: enum/subtype mistakes, orphan concepts, and story/domain drift.

**DO** produce an assessment artifact (for example `assessment.json` next to `map-model-spec.json`, or a section your repo documents) that explicitly records decisions and follow-ups.

```json
{
  "assessment_version": "1",
  "map_model_spec_path": "map-model-spec.json",
  "resolved": [
    {
      "topic": "type_field_vs_subtype",
      "decision": "Merge WireTransfer, ACHCredit, RTPPayment into PaymentInstruction with EnumType rail { wire, ach, rtp }",
      "chunk_ids": ["chunk-pay-001"]
    },
    {
      "topic": "domain_interaction_sync",
      "decision": "Story used **SKU**; scaffold had Product only — stories updated to **Product**",
      "chunk_ids": ["chunk-retail-12"]
    }
  ],
  "known_gaps": []
}
```

**DO** apply fixes before declaring `map-model-spec.json` final, or record open gaps in `known_gaps`:

```json
{
  "assessment_version": "1",
  "map_model_spec_path": "map-model-spec.json",
  "resolved": [],
  "known_gaps": [
    {
      "id": "gap-01",
      "description": "Two concepts both named like spell slot — merge deferred to next harmonize",
      "chunk_ids": ["chunk-srd-magic-2"]
    }
  ]
}
```

**DO NOT** skip assessment because “the JSON validates”.

**DO NOT** treat linter green as model correct — scanners catch syntax and heuristics, not semantic truth.

Chat-only resolution with no saved artifact — no audit trail:

```
(Conversation only: "merged RTP into PaymentInstruction" — assessment.json not updated)
```

Cosmetic JSON edits with empty assessment:

```json
{
  "assessment_version": "1",
  "resolved": [],
  "known_gaps": []
}
```

No entries in `resolved` despite substantive model changes — insufficient assessment record.


---

