<!-- Prompt bundle: process + domain + story-map + context + one built step. Assembled by scripts/get_prompt_bundle.py via build_agents.assemble_prompt_bundle -->



---

## process.md

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

## domain.md

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

## story-map.md

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

## context.md

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

## concept-classification.md

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
