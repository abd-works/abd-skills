# abd-solution-modeler

Transforms raw context into a validated OO domain model and interaction tree. Pipeline: Guidance → Sketch → Refine.

---

## Context Preparation

Use **abd-context-to-memory** before Phase 1 if source is documents:

- `index_memory.py --path <source_folder>` — convert, chunk, embed
- Output: `chunk_index.json` (required for evidence extraction)
- Path: `skills/abd-context-to-memory`

**Config:** Set `chunk_index_path` or `context_path` in `skill-config.json`. Or pass `--chunk-index PATH` / `--context-path PATH` when running the pipeline.

---

# Process

Pipeline: Context → Model → Assess. `pipeline.py` orchestrates all phases.

- Code phases — run scripts directly (normalize, concept_index, evidence_extraction, evidence_index)
- AI phases — **the AI does the work** (concept_synthesis, structure, behavior, variation, consolidate, assess, finalize). Do NOT write scripts for AI phases. Read inputs, reason, produce output directly.
- `generate <phase>` — prints built phase spec from `phases/built/` (phase instructions + baked-in rules)
- `scan <phase>` — runs programmatic scanners against generated output
- `validate <phase>` — prints rules for adversarial AI validation pass

**Workspace layout** (relative to `output_dir`):

- `context/` — context_chunks.json
- `concept_signals/` — concept_signals.json, concept_signals.md (12-signal output + markdown render)
- `evidence/` — terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_index.json
- `generated/` — extraction_config.json, hypothesis.json, hypothesis.md, solution_model.json, assessment.json
- `generated/domain/` — legacy .md outputs, solution_model.drawio

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.

---

## Stage 1: Context and Evidence (Phases 1–7)


| #   | Phase                                       | Actor | What it does                                                                                                      | Ref                                                                                                   | Outputs                                                                       |
| --- | ------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | **Normalize**                               | Code  | Chunk and clean raw source into uniform text segments.                                                            | [normalize.md](phases/built/normalize.md)                                                             | context_chunks.json                                                           |
| 2   | **Configure concept extraction parameters** | AI    | Calibrate weights, patterns, thresholds for 12 evidence-signal techniques (3 scans: structure, behavior, tuning). | [configure_concept_extraction_parameters.md](phases/built/configure_concept_extraction_parameters.md) | extraction_config.json                                                        |
| 3   | **Concept Extraction**                      | Code  | Run extraction using config; produce concept signals. Loop to Phase 2 if signals fail.                            | [concept_extraction.md](phases/built/concept_extraction.md)                                           | concept_signals.json, concept_signals.md                                      |
| 4   | **Concept Index**                           | Code  | Merge signals into hypothesis (concept index) with chunk_ids per concept.                                         | [concept_index.md](phases/built/concept_index.md)                                                     | hypothesis.json, hypothesis.md                                                |
| 5   | **Concept Synthesis**                       | AI    | Curate concepts (merge/split/kill), build hierarchy, allocate evidence.                                           | [concept_synthesis.md](phases/built/concept_synthesis.md)                                             | hypothesis.json (refined)                                                     |
| 6   | **Evidence extraction**                     | Code  | Mine chunks for actions, decisions, states, relationships, terms; guided by hypothesis.                           | [evidence_extraction.md](phases/built/evidence_extraction.md)                                         | evidence/*.json (terms, actions, decisions, states, relationships, modifiers) |
| 7   | **Evidence Index**                          | Code  | Aggregate evidence into concept-anchored index.                                                                   | [evidence_index.md](phases/built/evidence_index.md)                                                   | evidence_index.json                                                           |


---

## Stage 2: Model (Phases 8–11)

From Phase 8 onward, a single artifact: `solution_model.json` (concepts, behaviors, interaction_tree, evidence_refs).


| #   | Phase            | Actor | What it does                                                                                          | Ref                                           | Outputs                |
| --- | ---------------- | ----- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------- |
| 8   | **Structure**    | AI    | Build first solution_model from hypothesis + evidence index: properties, inheritance, stories, steps. | [structure.md](phases/built/structure.md)     | solution_model.json v1 |
| 9   | **Behavior**     | AI    | Assign operations, link behaviors to steps, group steps into scenarios.                               | [behavior.md](phases/built/behavior.md)       | solution_model.json v2 |
| 10  | **Variation**    | AI    | Split stories by subtype when mechanics differ; add failure modes.                                    | [variation.md](phases/built/variation.md)     | solution_model.json v3 |
| 11  | **Consolidate**  | AI    | Fix anti-patterns (anemia, over-centralization); add examples.                                        | [consolidate.md](phases/built/consolidate.md) | solution_model.json v4 |


---

## Stage 3: Assess (Phases 12–13)


| #   | Phase        | Actor    | What it does                                                                          | Ref                                     | Outputs                   |
| --- | ------------ | -------- | ------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------- |
| 12  | **Assess**   | AI+Human | Produce model assessment: consistency, coverage, completeness, type-field-vs-subtype. | [assess.md](phases/built/assess.md)     | assessment.json           |
| 13  | **Finalize** | AI       | Apply assessment fixes; produce validated model.                                      | [finalize.md](phases/built/finalize.md) | solution_model.json final |

---

# Critical Quality Steps

**These steps MUST be followed for every AI phase. No exceptions.**

---

## DO NOT write scripts for AI phases

**AI phases = the AI does the work.** You read the inputs, reason about them, and produce the output directly.

**DO** read the inputs (hypothesis.json, evidence/, context chunks), analyze them, and edit/write the output files yourself.

**DO NOT** write a Python (or other) script to "run" the phase. Do not create `synthesize_concepts.py`, `build_structure.py`, or similar. The pipeline has no script runners for AI phases — by design. Writing a script delegates the cognitive work to code; the AI must perform it.

Wrong: "I'll create a script that merges concepts and builds hierarchy."
Right: "I'll read the hypothesis and actions, curate concepts, build the hierarchy from evidence, and write the refined hypothesis.json."

---

## Step 0 — Deep Scan of Evidence and Conceptual Guidance (REQUIRED FIRST)

Before generating any output, you MUST:

1. **Do a deep scan of the evidence** — Read all files in `evidence/` (terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_graph.json). Understand every concept, every action, every decision, every state.
2. **Do a deep examination of the conceptual guidance** — Read `concept_guidance.md` and `concept_guidance.json`. Examine ALL concepts. Understand the nuance at a very detailed level.
3. **Verify understanding** — Before writing, confirm you can articulate: What are the key mechanisms? What are the subtypes and their distinct data/behavior? What variations exist? What constraints apply?

Do not proceed to generation until you have done this deep scan. Shallow or partial understanding produces shallow, broken models.

---

## Three-Stage Process (MUST follow for every AI step)

Each AI phase uses three validation layers. All three are required.

**Layer 1 — Generate with rules.** Phase spec + accumulated rules are included in the generation instructions. Follow DO/DO NOT guidance while producing output. Rules are guidance — produce natural output that complies.

**Layer 2 — Scan.** After generation, run `pipeline.py scan <phase>`. Scanners check structural violations mechanically (naming, child counts, concept sync, property types). Fix reported violations before proceeding.

**Layer 3 — Validate.** After scanners, run `pipeline.py validate <phase>`. This prints all applicable rules. AI re-reads generated output against the rules AND the completeness checklists. For each rule: does the output comply with the spirit, not just the letter? Report violations with rule name, location, proposed fix. Fix all violations. Re-validate until clean.

**This layer is critical.** Be adversarial. Take a contrarian stance. A scanner says "all clear" but the AI reviewing the rules sees that 3 operations on a concept all make decisions that belong to other concepts.

---

## AI Behavior Per Layer

| Layer           | Behavior                                                                            |
| --------------- | ----------------------------------------------------------------------------------- |
| Step 0          | Deep scan evidence + concept_guidance; verify understanding before generating       |
| Generation      | Pay strict attention to rules naturally while producing output                      |
| Scanner fixes   | Fix reported violations mechanically; re-run until clean                            |
| Validation pass | Adversarial checklist review — each rule is a checklist item; report ALL violations |

---

## Corrections Format

When recording corrections:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be
- **Scanner or rule:** (if applicable) Name of scanner or rule that caught the error
- **Likely source:** (if known) One of: code issue | prompt issue | rule priority | rule guidance quality

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

Account holds funds; transactions record deposits and withdrawals. The balance is what’s available.

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
- [ ] Each concept referenced via `**Concept**` in interaction tree must exist here
- [ ] Invariants under specific property/operation they apply to
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level

---

# Interaction Tree Format

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

## DrawIO Diagram Rendering

DrawIO class diagrams are generated from domain model `.md` files in `generated/domain/`.

- **Mandatory** — auto-generated after `finalize`
- **Optional** — append `render-diagram` to any `generate` command

```bash
python scripts/pipeline.py generate finalize render-diagram
python scripts/pipeline.py generate structure render-diagram
python scripts/pipeline.py drawio  # standalone, from latest solution model
```

Output: `generated/domain/<phase>.drawio` (alongside the source `.md` file).

---

## Scripts

```bash
python scripts/pipeline.py generate <phase>                  # Layer 1: phase spec + rules
python scripts/pipeline.py generate <phase> render-diagram   # Layer 1 + DrawIO
python scripts/pipeline.py scan <phase>                      # Layer 2: run scanners
python scripts/pipeline.py validate <phase>                  # Layer 3: rules + checklist for AI pass
python scripts/pipeline.py drawio [<phase>]                  # DrawIO from domain model
python scripts/pipeline.py pipeline                          # Run all phases (use --stop <phase>)
```

**Assemble AGENTS.md from pieces:**

```bash
python scripts/assemble_agents.py
```

