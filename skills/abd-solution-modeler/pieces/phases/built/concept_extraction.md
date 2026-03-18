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

# Phase 3 — Concept Extraction

**Actor:** AI + Code loop

## Purpose

Run code extraction with `extraction_config.json` (from Phase 2), evaluate signal quality, and **loop back to Phase 2** when signals fail. Outputs `concept_signals/concept_signals.json`.

**Principle:** AI calibrates (Phase 2), code extracts (Phase 3), AI evaluates. When extraction is wrong, go back to Phase 2 — adjust `extraction_config.json`, then run Phase 3 again. Loop between Phase 2 and Phase 3 until all 12 signals pass.

## Trigger

concept extraction, concept signals, term candidates, definition candidates, run extraction

## Inputs

- `context/context_chunks.json` — normalized chunks from Phase 1
- `generated/extraction_config.json` — from Phase 2 (configure_concept_extraction_parameters)

## Signal Reference (for Phase 2 and evaluation)

Phase 2 uses these signal definitions when calibrating. Phase 3 uses the evaluation checklist below. Full details:

This phase runs as **three separate AI prompts**, each focused on a group of related signals. Each scan reads the same chunk sample but looks for different things.

---

### Scan A — Structure Calibration

**Signals:** 1 (TF weights), 2 (definition patterns), 6 (table mining), 7 (enumeration patterns)

**What the AI looks at:** How is this document formatted? What structural cues carry concept signal?

**For each signal, observe and propose:**

#### Signal 1 — TF Weights

*Summary:* Weight terms by where they appear (heading, table, definition, etc.). High-weighted terms surface before the AI guesses them.

Look at where concepts appear in the document structure.

- Are headings concept names (high weight) or just chapter titles (lower weight)?
- Are bold terms domain concepts or emphasis?
- Are tables core rule definitions (high weight) or just formatting?
- Are list items led by concept names?

**Defaults to adjust:**

```json
"tf_weights": {
  "heading": 5,
  "table_header": 4,
  "definition_sentence": 3,
  "capitalized_noun": 2,
  "regular": 1,
  "bold_term": 3,
  "list_item_lead": 2
}
```

#### Signal 2 — Definition Patterns

*Summary:* Rulebooks and specs use explicit definition patterns (X is a..., X represents...). One of the highest-signal concept extractors.

Look at how this corpus defines things. Not just "X is a..." — what syntax does it actually use?

- Does it use "X is a..."? "X represents..."? "X: a type of..."?
- Does it use behavioral definitions? "X alters Y", "X imposes Y", "X resists Y"?
- Are behavioral patterns more revealing than static "is a" definitions?

**Defaults to adjust:**

```json
"definition_patterns": [
  "^([A-Z][a-zA-Z ]+) (is|represents|refers to|describes|means)\\s+"
]
```

Add domain-specific patterns you observe. Rank them — which patterns produce the strongest concept signal in this corpus?

#### Signal 6 — Table Mining

*Summary:* Tables contain enormous signal. Extract table name, column headers, row labels → clean domain vocabularies.

Look at how tables are used.

- Are tables markdown (`|...|`) or HTML?
- Do headers contain concept names or just column labels like "Name", "Value"?
- Are row labels concepts?

**Defaults to adjust:**

```json
"table_mining": {
  "header_pattern": "^\\s*\\|([^|]+)\\|",
  "concept_columns": ["header", "row_label"],
  "ignore_patterns": ["page", "chapter", "table of contents"]
}
```

#### Signal 7 — Enumeration Patterns

*Summary:* Patterns like "types of X include", "X may be" reveal parent concepts and children (e.g., Condition + Dazed, Stunned, Paralyzed).

Look at how this corpus lists variants or types.

- "Effects include: Damage, Affliction..."
- "The following modifiers apply:"
- "Available options: X, Y, Z"

**Defaults to adjust:**

```json
"enumeration_patterns": [
  "types of ([A-Z][a-zA-Z ]+) include",
  "([A-Z][a-zA-Z ]+) may be",
  "([A-Z][a-zA-Z ]+) categories are",
  "([A-Z][a-zA-Z ]+) can be one of",
  "forms of ([A-Z][a-zA-Z ]+)"
]
```

Add domain-specific enumeration syntax you observe.

**Scan A output:** `tf_weights`, `definition_patterns`, `table_mining`, `enumeration_patterns` fields.

---

### Scan B — Behavior Calibration

**Signals:** 3 (dependency verbs), 4 (noun phrase mining), 8 (contrast patterns), 9 (actor detection), 12 (verb interaction)

**What the AI looks at:** What happens in this domain and who does it? What verbs and noun structures carry behavioral signal?

**For each signal, observe and propose:**

#### Signal 3 — Dependency Verbs

*Summary:* Subject→verb→object patterns (Attack targets Defense, Character uses Power). Produces concept candidates through behavior, not just noun frequency.

Look at what verbs express relationships between concepts.

- Domain-specific relationship verbs: "resists", "imposes", "grants", "inflicts"?
- Business verbs: "approves", "submits", "escalates"?
- API verbs: "returns", "accepts", "validates"?

**Defaults to adjust:**

```json
"dependency_verbs": [
  "has", "have", "contains", "includes", "uses", "requires",
  "applies", "targets", "modifies", "affects"
]
```

Add domain-specific verbs. Remove generic ones that produce noise in this corpus.

#### Signal 4 — Noun Phrase Mining

*Summary:* Extract noun phrases (attack check, damage effect, character condition). Cluster to derive core nouns.

Look at how concepts are expressed as phrases.

- Single nouns ("Attack") or compound phrases ("Area Effect Attack", "Damage Resistance Check")?
- What's the typical phrase length?
- What's a reasonable minimum frequency to filter noise?

**Defaults to adjust:**

```json
"np_mining": {
  "min_frequency": 2,
  "max_words": 4,
  "prioritize_compound": true
}
```

#### Signal 8 — Contrast Patterns

*Summary:* When text compares things (Unlike X, Y does...), both X and Y are strong concept indicators, often siblings.

Look at how this corpus compares or contrasts concepts.

- "Unlike X, Y does..."
- "X differs from Y in..."
- Domain-specific comparison language?

**Defaults to adjust:**

```json
"contrast_patterns": [
  "unlike ([A-Z][a-zA-Z ]+),\\s+([A-Z][a-zA-Z ]+)",
  "([A-Z][a-zA-Z ]+) differs from ([A-Z][a-zA-Z ]+)",
  "while ([A-Z][a-zA-Z ]+).*,\\s+([A-Z][a-zA-Z ]+)",
  "in contrast to ([A-Z][a-zA-Z ]+)",
  "as opposed to ([A-Z][a-zA-Z ]+)"
]
```

#### Signal 9 — Actor Detection

*Summary:* Entities that initiate or trigger actions (Triggering-Actor / Responding-Actor). *Not* every concept that appears as the subject of a verb — those are covered by dependency (Signal 3) and verb-interaction (Signal 12) signals.

- Who are the actors in this domain? (character, player, system, gamemaster?)
- What verbs do actors use? (rolls, selects, activates, submits?)

**Defaults to adjust:**

```json
"actor_detection": {
  "actor_verbs": ["rolls", "selects", "chooses", "determines", "decides", "assigns", "activates", "initiates", "creates", "submits"],
  "known_actors": [],
  "actor_noun_pattern": "(character|player|user|system|gamemaster|admin|manager|operator)"
}
```

Replace defaults with domain-specific actors and verbs.

#### Signal 12 — Verb Interaction

*Summary:* The strongest signal. Verbs applied to nouns repeatedly (attack targets defense, effect causes condition). Concepts in many verb structures are almost always real domain objects.

Look at what action verbs recur with domain nouns.

- What are the key domain action verbs?
- Which generic verbs should be excluded because they produce noise? (e.g., "check", "roll" might be too generic in a rulebook)
- What verb patterns express rules?

**Defaults to adjust:**

```json
"verb_interaction": {
  "min_verb_frequency": 3,
  "verb_patterns": [],
  "exclude_verbs": ["is", "are", "was", "were", "has", "have", "can", "may", "should", "would", "could"],
  "prioritize_domain_verbs": true
}
```

**Scan B output:** `dependency_verbs`, `np_mining`, `contrast_patterns`, `actor_detection`, `verb_interaction` fields.

---

### Scan C — Tuning Review

**Signals:** 5 (co-occurrence), 10 (topic modeling), 11 (centrality) + noise filters

**What the AI looks at:** Corpus-level characteristics — size, density, structure. These signals are code-computed; the AI just picks reasonable parameters.

#### Signal 5 — Co-occurrence

*Summary:* Build co-occurrence matrix (term A appears near term B). Highest-degree nodes are often core domain concepts.

- How large are the chunks? (chunk-level window or sentence-level?)
- How tightly co-located are concepts?

**Defaults to adjust:**

```json
"cooccurrence": {
  "window_size": "chunk",
  "min_count": 2,
  "max_edges": 300
}
```

#### Signal 10 — Topic Modeling

*Summary:* Cluster chunks by topic. Extract representative nouns from each cluster. Domain modules emerge automatically.

- How many distinct topic areas does the corpus cover?
- What domain-specific words appear everywhere but carry no concept signal? (these are domain stop words)

**Defaults to adjust:**

```json
"topic_modeling": {
  "n_clusters": 8,
  "min_cluster_size": 3,
  "stop_words": ["the", "a", "an", "is", "are", "was", "were", "be", "been", "being"],
  "domain_stop_words": []
}
```

#### Signal 11 — Centrality

*Summary:* After building the term/relationship graph, run degree/PageRank/betweenness. Top nodes are usually foundation concepts.

- Is the domain tightly connected (use betweenness) or hub-and-spoke (use degree)?

**Defaults to adjust:**

```json
"centrality": {
  "metric": "degree",
  "top_n": 20,
  "threshold": 0.02
}
```

#### Noise Filters

*Summary:* Exclude chunks that carry no concept signal (chapter headers, title page, section separators, flavor text).

- What repeated junk appears in chunks? Chapter headers, title page text, section separators, flavor text?

**Defaults to adjust:**

```json
"noise_filters": [
  "table of contents", "appendix", "index", "license",
  "copyright", "acknowledgments", "foreword", "preface"
]
```

**Scan C output:** `cooccurrence`, `topic_modeling`, `centrality`, `noise_filters` fields.

---

## Outputs

- `concept_signals/concept_signals.json` — extracted signals

## Loop: Phase 2 ↔ Phase 3

Phase 3 runs extraction and evaluation. When signals fail, **go back to Phase 2** to adjust config, then run Phase 3 again. Loop until all 12 pass.

**CRITICAL: AI MUST verify.** Phase 3 is not complete until Step 2 (evaluate with subagent) has been run. Do not skip evaluation — extraction output often contains junk (pronouns, headers, generic verbs). The evaluation catches this and drives config fixes.

### Step 1 — Run extraction

Run: `python scripts/extract_concepts.py -i <context_chunks.json> -o <concept_signals_dir> -c <extraction_config.json>`

If extraction crashes (regex error, missing capture group), **go to Phase 2** — fix the offending pattern in `extraction_config.json`, then run Phase 3 again.

### Step 2 — Evaluate with subagent

Launch a subagent to read `concept_signals/concept_signals.json` and run this checklist:

| # | Signal | Check | Fail threshold |
|---|--------|-------|----------------|
| 1 | tf_weights | Term count reasonable for corpus size | < 50 terms |
| 2 | definition_patterns | Definitions are real concepts, not pronouns/headers | > 50% junk |
| 3 | dependency_verbs | Dependency count reflects domain verb richness | < 200 in a rule-heavy corpus |
| 4 | np_mining | Noun phrases are domain-relevant, not structural junk | > 30% structural headers |
| 5 | cooccurrence | Edge count non-trivial | < 100 edges |
| 6 | table_mining | Tables found if corpus has tables | 0 when corpus has tables |
| 7 | enumeration_patterns | Enumerations found for type/subtype structures | < 20 in a rich domain |
| 8 | contrast_patterns | Non-zero if corpus compares concepts | 0 when corpus uses "unlike/whereas" |
| 9 | actor_detection | Actors are real actors, not section headers | > 30% junk actors |
| 10 | topic_modeling | Clusters map to real domain areas | Clusters are generic words |
| 11 | centrality | Top-ranked concepts are real domain concepts | Top 5 are structural junk |
| 12 | verb_interaction | Domain verbs dominate, not generic verbs | Top verbs are "make/get/take" |

The subagent should read a sample of actual signal entries (not just counts) and report:
- PASS/FAIL per signal with reason
- For each FAIL: what config change would fix it

### Step 3 — If any FAIL: go back to Phase 2

**Do not fix config from Phase 3.** For each FAIL, run **Phase 2 (configure_concept_extraction_parameters)** again. Adjust the relevant section in `extraction_config.json` based on the subagent's suggestions. Then run Phase 3 again.

### Step 4 — Stop condition

Stop when all 12 signals pass or when remaining failures are inherent to the corpus (e.g. no tables exist to mine).

## Run

```bash
python scripts/pipeline.py generate concept_extraction
```


---

# Domain Model Format

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

## Domain Model Rules (15)

Apply these rules when producing the domain model output for this phase.

---
title: Hierarchy from evidence, not invention
impact: HIGH
---

## Build concept_hierarchy from evidence

**DO** derive parent-child relationships from evidence in `registries.actions` and concept `performs`/`receives`:
- **Shared mechanics** — concepts that share the same resolution, cost, or validation role (e.g. Wire Transfer, ACH, Card Payment all resolve as Payment; Checking, Savings, Money Market → Account) → Child → Parent
- **Shared protocol** — concepts that participate in the same workflow, lifecycle, or parent's collection → introduce a common base
- **Subtype patterns** — when evidence describes different rules, formulas, or state transitions for variants → model as Child : Parent

**DO** scan actions for each concept: subject, object, predicate, raw. Look for:
- Co-occurrence (concepts that appear together as subject/object)
- Shared terminology (term_ids, chunk_ids overlap)
- Domain language (e.g. "Transaction", "Account", "Payment", "Fee", "Product", "Order" in raw text)

**DO** build a **comprehensive** hierarchy. With hundreds of concepts, expect many parent types: Transaction, Account, Payment, Fee, Product, Order, Customer, etc. Each parent should have all its subtypes listed.

**DO NOT** infer hierarchy from chapter titles, section headers, or ToC alone. Read the raw action text to confirm different mechanics.

**DO NOT** leave hierarchy sparse. If you have 10+ concepts that share mechanics (e.g. Wire Transfer, ACH, Card Payment → Payment; Checking, Savings → Account), add them. If you have Transaction subtypes beyond Purchase/Refund/Chargeback, add them.

**Related rules:** [concept_synthesis-subtypes-first-class](concept_synthesis-subtypes-first-class.md), [variation-base-inheritance](variation-base-inheritance.md), [domain-mechanics-not-toc](domain-mechanics-not-toc.md), [refined-integrate-concepts](refined-integrate-concepts.md).


---

---
title: Model Instances, Not Smashed Properties
impact: HIGH
---

## Model Instances, Not Smashed Properties

**DO** consider when a concept is best represented as instances/examples (objects in diagram) vs smashing it into a property or method.

**DO** model context with tables as one or more concepts with relationships.

**DO** model instances and examples explicitly when structure matters.

**DO NOT** smash complex objects with multiple concepts into a single property or method.


---

---
title: Domain Model — Standard Types for Properties
impact: HIGH
---

## Standard Types for Properties

**DO** use standard types for Properties when defining concepts:

| Type | Use when | Example |
|------|----------|---------|
| **String** | Text, names, labels | `Customer.name`, `Product.sku` |
| **Number** | Quantities, amounts, counts | `Cart.total`, `LineItem.quantity` |
| **Boolean** | Yes/no, flags | `Order.isPaid`, `Cart.isEmpty` |
| **List** | Ordered collection | `Cart.lineItems` (List of LineItem) |
| **Dictionary** | Key-value mapping | `Product.attributes`, `Config.settings` |
| **UniqueID** | Identifier, reference | `Order.customerId`, `LineItem.productId` |
| **Instant** | Point in time (ISO 8601) | `Order.createdAt`, `Payment.processedAt` |

| **EnumType** | Fixed set of valid values | `ModifierType type {bonus, penalty}`, `ActionType action_type {standard, move, free, reaction}` |

Use `List<T>` or `Dictionary<K,V>` when element types matter.

**DO** use a named enum type when a property has a constrained set of valid values. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** use `String` with parenthetical options (e.g., `String type (bonus/penalty)`). Strings imply free-form text; constrained options are a distinct type.

- Example (wrong): `String type (bonus/penalty)`, `String attack_type (close/ranged)`.
- Example (right): `ModifierType type {bonus, penalty}`, `AttackType attack_type {close, ranged}`.


---

---
title: Speculation and assumptions
impact: HIGH
---

## Speculation and assumptions

**DO** state an assumption when something is unclear.
- Example (right): "Assumption: Shipping Address is provided before checkout"; "Assumption: Loyalty points not in scope".

**DO NOT** speculate beyond the provided material or invent mechanics when unclear.
- Example (wrong): Story "Apply loyalty points at checkout" when context never mentions loyalty. Right: Omit, or state "Assumption: Loyalty points not in scope."


---

---
title: Subtypes as first-class concepts
impact: HIGH
---

## Subtypes as first-class concepts

**DO** give each subtype its own `### **SubtypeName** : Parent` section with its own properties, operations, collaborators, and composition. Subtypes inherit from parent but have distinct mechanics — model those mechanics explicitly.

**DO** ground each subtype's definition in evidence. Scan `actions.json` and `terms.json` for the subtype name (e.g. Purchase, Refund, Chargeback) and derive properties/operations from what the evidence says that subtype does.

**DO NOT** list subtypes only in a parent's `Subtypes:` line without creating first-class sections for them.

**DO NOT** collapse subtypes that have distinct rules (e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, reversal) into a single parent definition.

- Example (wrong): `### **Transaction**` with `Subtypes: Purchase, Refund, Chargeback` and no separate sections for Purchase, Refund, Chargeback.
- Example (right): `### **Transaction**` plus `### **Purchase** : Transaction`, `### **Refund** : Transaction`, `### **Chargeback** : Transaction`, etc., each with its own properties, operations, and collaborators.


---

---
title: Subtypes vs enum — verify before modeling
impact: HIGH
---

## Subtypes vs enum — verify before modeling

**DO** before creating a subtype section: verify actions.json and terms.json show different mechanics for that subtype. Different properties, operations, or resolution paths = subtype. Same logic, different label = enum on parent.

**DO** use `EnumType property_name {value1, value2}` when the evidence shows same behavior across variants. Do not create subtype sections for enum-like variation.

**DO NOT** create subtype sections from concept_hierarchy without evidence check. If concept_guidance listed Purchase, Refund, Chargeback as Transaction subtypes but the evidence treats them identically (same validation, same settlement flow), convert to `TransactionType type {purchase, refund, chargeback}` on Transaction.

**DO NOT** have both a type enum and mirroring subtypes. If Transaction has `TransactionType type {purchase, refund, chargeback}`, do not also create Purchase, Refund, Chargeback as subtypes.

- Example (right): Transaction has Purchase, Refund, Chargeback as subtypes — evidence shows Purchase has forward-payment validation, Refund has reversal rules and original-required check, Chargeback has issuer workflow. Each has distinct mechanics.
- Example (wrong): Transaction has Purchase, Return, Exchange as subtypes when the rules only categorize by label. Right: Transaction with `TransactionType type {purchase, return, exchange}`.


---

---
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---

---
title: Mechanics from evidence, not table of contents
impact: HIGH
---

## Mechanics from evidence, not table of contents

**DO** read evidence chunks for mechanical depth. For each candidate subtype, scan actions.json and terms.json for that name. Derive properties, operations, and collaborators from what the evidence says that variant does. A subtype is justified when the evidence describes different rules, formulas, state transitions, or interaction patterns.

**DO** verify each subtype has its own trigger, conditions, or resolution path in the source. Different mechanics = subtype. Same mechanics with different label = enum.

**DO NOT** infer subtypes from chapter titles, section headers, or bullet lists without reading the actual rule text. A table of contents that lists "Volume Discount, Loyalty Reward, Bundle Offer" under Promotions does not make them subtypes — only the rules for each do.

**DO NOT** create subtypes from variation axes or category lists when each item shares the same resolution logic. "Transaction types: Purchase, Return, Exchange" in a summary is a categorization; read the rules to see if each resolves differently.

- Example (wrong): Source has section "Transaction Types" with Purchase, Return, Exchange. You list those as subtypes. But the ToC categories are wrong — the mechanics show different resolution types (e.g. forward payment vs reversal vs disputed reversal). Right: Read the rules. Derive subtypes from resolution mechanics, not from ToC labels.
- Example (wrong): Source lists "Payment Methods: Credit Card, Bank Transfer, Invoice" and you model each as a subtype because they use different rails. But the mechanics are identical — same flow, different input. Right: PaymentMethod with `method_type {credit_card, bank_transfer, invoice}` — data field, not subtypes. Same mechanics with different input = variable, not subtype.


---

---
title: Subtypes vs enum — distinct mechanics required
impact: HIGH
---

## Subtypes vs enum — distinct mechanics required

**DO** use subtype when the evidence shows different properties, operations, or resolution mechanics for each variant. A subtype is a concept when it has its own rules — different validation, different settlement, different formulas, different state transitions.

**DO** use enum (or type property) when variants share the same logic and differ only by label. Same behavior, different data = enum. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** derive subtypes from table of contents or section headers alone. Verify each subtype has distinct mechanics in the evidence (actions.json, terms.json, context chunks). If the source only lists names under a category without different rules per name, it's an enum.

**DO NOT** create both a parent "Type" or "Category" enum and subtypes that mirror it. Example (wrong): Transaction has `TransactionType type {purchase, refund, chargeback}` AND subtypes Purchase, Refund, Chargeback. Use one representation: either enum or subtypes with genuinely different mechanics.

- Example (right — subtype): Transaction subtypes Purchase, Refund, Chargeback — each has different validation, settlement, and reversal rules. Purchase: forward payment, creates obligation. Refund: reversal, requires original. Chargeback: disputed reversal, involves issuer. Each gets its own concept.
- Example (right — enum): Order has `OrderStatus status {pending, shipped, delivered}` — same state machine, different state. Or: LineItem has `ItemType type {product, service, subscription}` — same line-item logic, different label.
- Example (wrong): Transaction types Purchase, Return, Exchange as Transaction subtypes when the rules treat them the same way and only categorize by label. Right: `TransactionType type {purchase, return, exchange}` on Transaction.
- Example (wrong): Subtypes inferred from a bullet list "Promotions: Volume Discount, Loyalty Reward, Bundle Offer..." without reading whether each has different mechanics. Right: Read the actual rule text; if Volume Discount has tier-based calc, Loyalty Reward has points logic, Bundle has bundle rules, they're subtypes. If they're just names under a category, enum.


---

---
title: Hierarchy from evidence, not invention
impact: HIGH
---

## Build concept_hierarchy from evidence

**DO** derive parent-child relationships from evidence in `registries.actions` and concept `performs`/`receives`:
- **Shared mechanics** — concepts that share the same resolution, cost, or validation role (e.g. Wire Transfer, ACH, Card Payment all resolve as Payment; Checking, Savings, Money Market → Account) → Child → Parent
- **Shared protocol** — concepts that participate in the same workflow, lifecycle, or parent's collection → introduce a common base
- **Subtype patterns** — when evidence describes different rules, formulas, or state transitions for variants → model as Child : Parent

**DO** scan actions for each concept: subject, object, predicate, raw. Look for:
- Co-occurrence (concepts that appear together as subject/object)
- Shared terminology (term_ids, chunk_ids overlap)
- Domain language (e.g. "Transaction", "Account", "Payment", "Fee", "Product", "Order" in raw text)

**DO** build a **comprehensive** hierarchy. With hundreds of concepts, expect many parent types: Transaction, Account, Payment, Fee, Product, Order, Customer, etc. Each parent should have all its subtypes listed.

**DO NOT** infer hierarchy from chapter titles, section headers, or ToC alone. Read the raw action text to confirm different mechanics.

**DO NOT** leave hierarchy sparse. If you have 10+ concepts that share mechanics (e.g. Wire Transfer, ACH, Card Payment → Payment; Checking, Savings → Account), add them. If you have Transaction subtypes beyond Purchase/Refund/Chargeback, add them.

**Related rules:** [concept-model-subtypes-first-class](concept-model-subtypes-first-class.md), [variation-base-inheritance](variation-base-inheritance.md), [domain-mechanics-not-toc](domain-mechanics-not-toc.md), [refined-integrate-concepts](refined-integrate-concepts.md).


---

---
title: Model Instances, Not Smashed Properties
impact: HIGH
---

## Model Instances, Not Smashed Properties

**DO** consider when a concept is best represented as instances/examples (objects in diagram) vs smashing it into a property or method.

**DO** model context with tables as one or more concepts with relationships.

**DO** model instances and examples explicitly when structure matters.

**DO NOT** smash complex objects with multiple concepts into a single property or method.


---

---
title: Domain Model — Standard Types for Properties
impact: HIGH
---

## Standard Types for Properties

**DO** use standard types for Properties when defining concepts:

| Type | Use when | Example |
|------|----------|---------|
| **String** | Text, names, labels | `Customer.name`, `Product.sku` |
| **Number** | Quantities, amounts, counts | `Cart.total`, `LineItem.quantity` |
| **Boolean** | Yes/no, flags | `Order.isPaid`, `Cart.isEmpty` |
| **List** | Ordered collection | `Cart.lineItems` (List of LineItem) |
| **Dictionary** | Key-value mapping | `Product.attributes`, `Config.settings` |
| **UniqueID** | Identifier, reference | `Order.customerId`, `LineItem.productId` |
| **Instant** | Point in time (ISO 8601) | `Order.createdAt`, `Payment.processedAt` |

| **EnumType** | Fixed set of valid values | `ModifierType type {bonus, penalty}`, `ActionType action_type {standard, move, free, reaction}` |

Use `List<T>` or `Dictionary<K,V>` when element types matter.

**DO** use a named enum type when a property has a constrained set of valid values. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** use `String` with parenthetical options (e.g., `String type (bonus/penalty)`). Strings imply free-form text; constrained options are a distinct type.

- Example (wrong): `String type (bonus/penalty)`, `String attack_type (close/ranged)`.
- Example (right): `ModifierType type {bonus, penalty}`, `AttackType attack_type {close, ranged}`.


---

---
title: Speculation and assumptions
impact: HIGH
---

## Speculation and assumptions

**DO** state an assumption when something is unclear.
- Example (right): "Assumption: Shipping Address is provided before checkout"; "Assumption: Loyalty points not in scope".

**DO NOT** speculate beyond the provided material or invent mechanics when unclear.
- Example (wrong): Story "Apply loyalty points at checkout" when context never mentions loyalty. Right: Omit, or state "Assumption: Loyalty points not in scope."


---

---
title: Subtypes as first-class concepts
impact: HIGH
---

## Subtypes as first-class concepts

**DO** give each subtype its own `### **SubtypeName** : Parent` section with its own properties, operations, collaborators, and composition. Subtypes inherit from parent but have distinct mechanics — model those mechanics explicitly.

**DO** ground each subtype's definition in evidence. Scan `actions.json` and `terms.json` for the subtype name (e.g. Purchase, Refund, Chargeback) and derive properties/operations from what the evidence says that subtype does.

**DO NOT** list subtypes only in a parent's `Subtypes:` line without creating first-class sections for them.

**DO NOT** collapse subtypes that have distinct rules (e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, reversal) into a single parent definition.

- Example (wrong): `### **Transaction**` with `Subtypes: Purchase, Refund, Chargeback` and no separate sections for Purchase, Refund, Chargeback.
- Example (right): `### **Transaction**` plus `### **Purchase** : Transaction`, `### **Refund** : Transaction`, `### **Chargeback** : Transaction`, etc., each with its own properties, operations, and collaborators.


---

---
title: Subtypes vs enum — verify before modeling
impact: HIGH
---

## Subtypes vs enum — verify before modeling

**DO** before creating a subtype section: verify actions.json and terms.json show different mechanics for that subtype. Different properties, operations, or resolution paths = subtype. Same logic, different label = enum on parent.

**DO** use `EnumType property_name {value1, value2}` when the evidence shows same behavior across variants. Do not create subtype sections for enum-like variation.

**DO NOT** create subtype sections from concept_hierarchy without evidence check. If concept_guidance listed Purchase, Refund, Chargeback as Transaction subtypes but the evidence treats them identically (same validation, same settlement flow), convert to `TransactionType type {purchase, refund, chargeback}` on Transaction.

**DO NOT** have both a type enum and mirroring subtypes. If Transaction has `TransactionType type {purchase, refund, chargeback}`, do not also create Purchase, Refund, Chargeback as subtypes.

- Example (right): Transaction has Purchase, Refund, Chargeback as subtypes — evidence shows Purchase has forward-payment validation, Refund has reversal rules and original-required check, Chargeback has issuer workflow. Each has distinct mechanics.
- Example (wrong): Transaction has Purchase, Return, Exchange as subtypes when the rules only categorize by label. Right: Transaction with `TransactionType type {purchase, return, exchange}`.


---



## Interaction Tree Rules (6)

Apply these rules when producing the interaction tree output for this phase.

---
title: Verb-noun format
impact: HIGH
order: 1
---

## Verb-noun format

Use verb-noun format for epic/story/step names and steps. Actor documented separately. Use active voice, base verb forms, and business language for all interaction text. Use behavioral language — describe what happens, not how it's implemented. Use domain concepts in steps (Given/When/Then) — not UI labels. Applies to all nodes (epic, story, step, scenario), including steps in or out of scenarios.
**DO** use Actor → verb noun [qualifiers]. Actor is documented separately, NOT in the name.
- Names: "Places Order" (actor: Customer); "Validates Payment" (actor: System); "Process Order Payment".
- **Step format** — strategy may specify When/Then (strict) or vanilla (verb-noun). Show both:
  - **When/Then:** `When **User** browses countries; Then **System** displays list of **Country** options`.
  - **Vanilla:** `User submits form`, `System validates payment`, `Select item from list`.
- Use base verb forms (infinitive/imperative): "Select Tokens", "Group Minions", "Process Payment".
- Use behavioral terms: "When user enters name; Then system saves character information" (not "system writes to JSON").
- Use domain concepts in steps: "User selects **Country**", "User enters **PaymentDetails**" (not "User clicks dropdown", "User fills form field").

**DO NOT** include actor in name, use noun-only, gerunds, or third-person singular.
**DO NOT** use technical implementation terms (config, json, api, sql, class, method). Use behavioral language instead.
- Wrong: "Customer Places Order" (actor in name). Right: "Places Order" (actor: Customer).
- Wrong: "Order submission", "Payment processing", "Form validation" (noun-only). Right: "Submit order", "Process payment", "Validate form".
- Wrong: "Submitting order", "Selects item", "Displays confirmation" (gerund/third-person). Right: "Submit order", "Select item", "Display confirmation".
- Wrong: "Then system saves to JSON file", "Then system parses XML", "Then system executes SQL query" (technical). Right: "Then system saves configuration data", "Then system processes data", "Then system retrieves data".
- Wrong: "User clicks dropdown", "User fills form field", "User submits button" (UI). Right: "User selects **Country**", "User enters **PaymentDetails**", "User submits payment".


---

---
title: Outcome-oriented language
impact: HIGH
order: 2
---

## Outcome-oriented language

Use outcome-oriented language over mechanism-oriented language. Focus on what is created or achieved, not how it's shown or communicated.

**DO** use verbs that describe artifacts and outcomes — name concepts by what they ARE or CREATE.
- Example (right): "System → displays power activation animation" (not "Visualizing Power Activation"); "System → provides combat outcome feedback" (not "Showing Combat Results"); "System → displays hit indicators" (not "Displaying Hit Information").

**DO NOT** use generic communication or mechanism verbs.
- Example (wrong): "Visualizing Power Activation", "Showing Combat Results", "Displaying Hit Information", "Presenting Configuration Options".
- Wrong: "Showing results", "Displaying information", "Visualizing data", "Presenting options", "Providing settings", "Enabling features", "Allowing access".


---

---
title: Hierarchy — approximately 4 to 9 children
impact: MEDIUM
order: 3
---

## Hierarchy — approximately 4 to 9 children

Any node (epic, story, scenario) has approximately 4–9 children. Does not apply to steps. For stories, count **steps** as children (not scenarios).
**DO** keep child count in the 4–9 range for manageable granularity.
- Epic: ~4–9 sub-epics or stories.
- Story: ~4–9 steps (total across scenarios; scenarios are containers, not counted).
- Scenario: ~4–9 steps.

**DO NOT** create nodes with many more than 9 children — split or regroup.
- Wrong: Epic with 15 stories (split into sub-epics).
- Wrong: Story with 12 steps (consider splitting story or grouping steps into scenarios).


---

---
title: Hierarchy — approximately 4 to 9 children
impact: MEDIUM
order: 3
---

## Hierarchy — approximately 4 to 9 children

Any node (epic, story, scenario) has approximately 4–9 children. Does not apply to steps. For stories, count **steps** as children (not scenarios).
**DO** keep child count in the 4–9 range for manageable granularity.
- Epic: ~4–9 sub-epics or stories.
- Story: ~4–9 steps (total across scenarios; scenarios are containers, not counted).
- Scenario: ~4–9 steps.

**DO NOT** create nodes with many more than 9 children — split or regroup.
- Wrong: Epic with 15 stories (split into sub-epics).
- Wrong: Story with 12 steps (consider splitting story or grouping steps into scenarios).


---

---
title: Story granularity
impact: MEDIUM-HIGH
order: 4
---

## Story granularity

**DO** break down by distinct requirements areas, distinct concept structure, or workflow steps; sufficient stories to capture rule detail.
- Example (right): Story "View Product Details", Story "Make Payment" (each has distinct logic). Story "Drive Bike", Story "Drive Car" (concept structure differs).

**DO NOT** collapse large rule sections into one story.
- Example (wrong): Story "All combat effects" or "All attack types" when the context has dozens of distinct rules. Right: Story "Apply damage effect", Story "Apply condition effect", Story "Resolve melee attack", etc.


---

---
title: Small and testable
impact: HIGH
order: 5
---

## Small and testable

Stories must be testable as complete interactions and deliverable independently. Story = testable outcome; Step = implementation detail.

**DO** create stories that can be tested and delivered independently.
- Example (right): "Customer → places order" (testable: order created, payment processed).
- Story = User/system outcome (testable independently with clear acceptance criteria).
- Step = Implementation detail (not testable alone, verified as part of parent story test).

**DO NOT** create stories too small to test meaningfully or make implementation steps into stories.
- Example (wrong): "Add order button" (can't test without full order flow); "Display error message" (can't test without validation context).
- Wrong: "Convert Diagram to StoryGraph Format", "Serialize Components to JSON", "Calculate Component Positions" (implementation steps, not testable alone).


---



## Extraction Config Rules (10)

Apply these rules when producing extraction_config.json for this phase.

---
phases: [concept_synthesis]
order: 10
---

## Merge alias concepts into canonical

**DO** merge alias concepts into their canonical using `concept_guidance.concept_aliases`. If concept_aliases has "Account": ["ACCT"], then concepts must NOT contain both "ACCT" and "Account" as separate entries.

**DO NOT** leave abbreviation concepts (ACCT, REV, CUST, SKU, etc.) as separate concepts when concept_aliases maps them to a canonical.


---

---
phases: [concept_synthesis]
order: 20
---

## No extraction artifacts as concepts

**DO NOT** leave extraction artifacts as separate concepts: "All Transactions", "All Orders", "Rev", "Cust", "Compli", "Transac", "COST PER ITEM An".

**DO** merge "All X" → "X", truncations → full form, fragments → cleaned form.


---

---
phases: [concept_synthesis]
order: 30
---

## No nonsense concepts

**DO NOT** leave non-words, typos, proper nouns, or garbage as concepts. Remove: Smith, Choose, Choose One, Although, Because, McDonald, Acme Corp.

**DO** remove instruction phrases mistaken for concepts ("Choose", "Select One" from rule text).


---

---
phases: [concept_synthesis]
order: 40
---

## No section headers as concepts

**DO NOT** leave section headers, ToC labels, or structural categories as concepts. Remove: BALANCE SHEET, INCOME STATEMENT, CHECKOUT, PRODUCT CATALOG, COST PER ITEM, THE BASICS, SERVICE TIERS.

**DO** remove concepts that are structural labels rather than domain entities.


---

---
phases: [concept_synthesis]
order: 50
---

## Merge singular/plural variants

**DO** merge singular/plural variants into one canonical (usually singular). Do NOT leave both "Account" and "Accounts", "Order" and "Orders", "Customer" and "Customers" as separate concepts.


---

---
phases: [concept_synthesis]
order: 60
---

## Actions reference valid concepts

**DO** ensure every action's subject and object (when non-empty) reference a concept in the concepts dict. Orphan references (subject/object not in concepts) indicate merged/removed concepts whose actions were not updated.


---

---
phases: [concept_synthesis]
order: 70
---

## All concepts have evidence

**DO** ensure each concept has at least one of: term_ids, chunk_ids, performs, receives. Concepts with no evidence are noise and should be removed.


---

---
phases: [concept_synthesis]
order: 80
---

## Concept names are valid domain terms

**DO NOT** use single instruction verbs (Choose, Apply, Because) or article+noun fragments ("A Transaction", "The Balance") as concept names.

**DO** use domain nouns or noun phrases (Account, Order, Subscription, Customer).


---

---
phases: [concept_synthesis]
order: 90
---

## concept_hierarchy derived from evidence

**DO** build concept_hierarchy from evidence (shared mechanics, co-occurrence in actions, subtype patterns). Parent and child names must exist in concepts.

**DO NOT** infer hierarchy from chapter titles or ToC alone.


---

---
phases: [concept_synthesis]
order: 95
---

## performs/receives match actions registry

**DO** ensure each concept's performs list contains only act_ids where that concept is subject; receives only act_ids where that concept is object. After merge/remove, rebuild performs/receives from actions.


---

