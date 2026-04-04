# Domain model

Enduring reference for modules, `concepts[]`, examples, and inheritance.   

See `[content/parts/process.md](../content/parts/process.md)` and `[principles.md](principles.md)`.

---

## Purpose

The **domain model** describes the **state and structure** that the story map refers to. It holds **modules** and **domain concepts**: the things that hold state, get operated on, and participate as callers, receivers, and collaborators in interactions. Every `**Concept`** referenced in the story map **appears** in the domain model so the story tree and model stay aligned.

---

## What goes in the domain model

- **Modules** — A **grouping of tightly related concepts that collaborate around the same mechanism**. Each module has a name and a list of concepts. Each module typically maps to one area (or page) of the class diagram.
- **Domain concepts** — A **domain concept holds state and can be operated on** (equates to a class in OO code). **Concepts participate as callers, receivers, and collaborators in interactions; state is carried in Pre-Condition labels, **Trigger** / **Response** behavior text, and **Examples** tables in the story map (no separate Triggering-State / Resulting-State fields). Each concept has:
  - **Properties** — with types, optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter. **Type selection:** Use `Dictionary<K,V>` when items are accessed by key (name, type, id) — most "has many" relationships where you look up by name. Use `List<T>` only when order matters and items are accessed by position. Default to Dictionary for named domain collections.
  - **Operations** — with optional collaborating concepts and invariants. Interactions in the story map should be reverse-engineerable to operations on the domain model.
  - **Base-Concept** (optional) — parent for inheritance. **Foundational** — tag `[foundational]` for concepts that are the base classes everything else extends from (the stable core).
- **Concept relationships** — When a concept "has" another: **composition** (strong has-a; part cannot exist without whole) or **aggregation** (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.
- **Examples** — At the end of each module, one table per concept, shared scenario linking the module. Scenario column required; qualifier in parentheses after concept name; columns match concept properties.
- **Invariants** — Under the specific property or operation they apply to, not a separate section.

**What does not go in:** Implementation details (APIs, services, databases, UI components, code). No speculation beyond the provided material. Everything at logical/domain level.

---

## Domain model format

### Module

A grouping of tightly related concepts that collaborate around the same mechanism. Name + list of concepts; typically maps to one area (or page) of the class diagram.

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
- examples: at end of module, after all concepts; one table per concept; shared scenario links the module
```

### Domain concept

A domain concept holds state and can be operated on (equates to a class in OO code). Concepts participate as callers, receivers, and collaborators in interactions; state is carried in Pre-Condition labels, **Trigger** / **Response** behavior text, and **Examples** tables.

Heading: `### **Extension** : <BaseConcept if any>` — **Extension** is the subtype; **BaseConcept** is the immediate superclass (omit the `: BaseConcept` part when there is no inheritance).

One-liner description of the purpose of the concept

```
**Extension** : <BaseConcept if any>
- <type> property
      <collaborating concepts if any>
      Invariant: <constraint on this property>
- <type> operation(<param>, ...) → <return>
      <collaborating concepts if any>
      Invariant: <constraint enforced by this operation>
- Interactions: interaction nodes this concept is used by
```

**Marking deltas:** When you **revise** an existing concept in a later pass (Deepen, Integrate, or a follow-up domain-types patch), append **`**newly added**`** on the line **immediately after** any **new** property or operation line so reviewers can see what changed since the previous version. Example:

```
### **Payment**

…

- Money authorizedAmount **newly added**
      Invariant: authorizedAmount >= capturedAmount
- authorize(amount) → Boolean **newly added**
      **ComplianceGate** — precondition
```

(Use the same marker in parallel prose beside `map-model-spec.json` when you maintain a narrative module section; JSON has no standard field for this — rely on git history for `properties[]` / `operations[]` or a short `phase_note` on the spec root if you need machine-visible deltas.)

### Continual refinement — class definition + diagram

Where appropriate, treat each **domain concept** as a **living** definition that you **refine across phases**, not a one-shot dump at promotion time.

| Phase / artifact | What to add | Force the property/operation format? |
|------------------|-------------|--------------------------------------|
| **Terms & mechanisms**, **shaped story map** | Vocabulary, mechanisms, anchors — **no** `concepts[]` yet | **No.** Do not fake classes. Collect **candidates** and **responsibilities** in queue / stories. |
| **Domain types (promote)** | Sparse `concepts[]`, `owns`, evidence | **Partially.** Use formal **heading** (`### **Extension** : **Base**`) and **Interactions** when known; properties/operations **as soon as** evidence supports a typed line. If you only have **responsibility sentences**, keep those in `owns` / narrative until Deepen — **do not** invent parameters. |
| **Variant classification** | Enum vs subtype decisions | **N/A** to line format; constrains **name** (`Base:Extension`) and families. |
| **Deepen** | Evidence, `depends_on`, collaborations on **members** | **Yes, prefer.** Fold responsibilities into **`- <type> property`** and **`- <type> operation(...) → …`**; add **`**newly added**`** on lines first introduced this pass. |
| **Integrate** | Synonyms, drained queue, reconciled edges | **Yes** where stable — final pass on prose **mirror** of JSON. |
| **`map-model-spec.json`** | Source of truth for structure | Keep **properties[]** / **operations[]** aligned with the prose template above; same refinement rules apply in JSON editing. |

**Class diagram:** After material updates to **`map-model-spec.json`**, re-run **`render_map_model_class_diagram.py`** (see [class-diagram-from-spec.md](class-diagram-from-spec.md)) so **`map-model-class-diagram.drawio`** stays the **visual twin** of the continually refined model. Optional: a short **ASCII** sketch in module notes for fast diff in review — not a substitute for the Draw.io artifact.

### Foundational classes

A **foundational class** is a domain concept tagged `[foundational]`. These are the **base classes that everything else extends from** — the stable core that repeats across the system. Later slices add concepts that extend or use foundational classes; the foundational classes themselves remain stable.

There is one domain model, not separate "foundational" and "full" models. The tag distinguishes core classes from extensions.

Example: in a payments system, Account + Transaction + ValidationRule collaborate the same way whether you're processing a wire transfer, ACH, or direct debit. Those three are foundational. Wire, ACH, and direct debit are extensions added in later slices.

### Examples

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

### Guidelines

- Prefer **composition/aggregation** over inheritance (composition = strong has-a; aggregation = weak has-a where whole has no meaning without multiple instances of the same part).
- **Type selection:** Use `Dictionary<K,V>` when items are accessed by key (name, type, id); use `List<T>` only when order/position matters (e.g. turn order, sequential steps). Default to Dictionary for named domain collections.
- Avoid central "service/manager" concepts.
- Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options.

---

## Promotion ledger (`promotion_ledger.json`)

The **promotion ledger** is the audit trail for every candidate extracted during Phase 4 (terms-mechanisms). It lives alongside `map-model-spec.json` in the output directory and is populated during Phase 6 (domain-types).

### Contract

Every entry in `candidate_queue.json` **must** have a corresponding entry in `promotion_ledger.json`. No candidate may be silently ignored.

### Source reading requirement

Before deciding any candidate, the agent **must read source evidence** — not just JSON metadata:

1. **`shaped_story_map.json`** — find every story where the candidate appears in `anchor`, `trigger`, `response`, `steps[]`, or `term_refs`. Read the full story context.
2. **Original chunk `.md` files** — for every `evidence_chunk_id` cited on the candidate, open and read the actual markdown body. Do not make promotion decisions based on chunk IDs or previews alone.
3. **`mechanisms.json`** — find any mechanism whose description names the candidate or whose `realized_by` paths include stories that reference the candidate.

### Decision taxonomy

| Decision | When to use | Action on `map-model-spec.json` |
|---|---|---|
| **`promote`** | Entity holds state, makes decisions, has a distinct lifecycle, or owns a behavioral boundary | Add to `concepts[]` with `owns` sentence, evidence chunks, rationale |
| **`absorb`** | Entity is real but has no independent lifecycle — it is a property or operation on an existing concept | Add as property/operation on the absorbing concept; ledger records which concept absorbed it and why |
| **`merge`** | Identity match — same entity, different names. One name survives; the other becomes a synonym | Keep one concept; add alias to `terms_layer.json`; ledger records merge rationale |
| **`extend`** | Specialization — entity is a subtype with distinct behavior that justifies inheritance (LSP) | Promote child with `Base:Extension` naming and shared `owns`/evidence on subtype; ledger records LSP justification |
| **`defer`** | Insufficient evidence today — but specific trigger for revisiting | Move to deferred section with trigger: "promote when [specific evidence arrives]" |
| **`reject`** | True noise — not a domain entity at all (UI label, implementation detail, etc.) | Ledger records reason; no model change |

### Absorb pathway

When a candidate is **absorbed**, it becomes a property or operation on the absorbing concept rather than a standalone `concepts[]` entry. The ledger entry records:
- `absorbing_concept` — which existing concept took ownership
- `absorbed_as` — `property` or `operation`
- `rationale` — why this entity lacks an independent lifecycle

### Merge pathway

When candidates are **merged**, they are recognized as the same entity with different names. The surviving name keeps its `concepts[]` entry; the alias is added to `terms_layer.json`. The ledger entry records:
- `surviving_name` — the name that persists in the model
- `merged_name` — the alias being collapsed
- `rationale` — what evidence proves identity (same state, same operations, same lifecycle)

### Extend pathway

When a candidate is decided as **`extend`**, it becomes a subtype using `Base:Extension` naming. This decision must be grounded in the Liskov Substitution Principle: the extension has all the behavior of the base **plus** distinct additional behavior that the base does not have. The ledger entry records:
- `base_concept` — the parent type
- `extension_name` — the subtype
- `lsp_justification` — what distinct behavior justifies the subtype (not just a different label)

### Format

```json
{
  "decisions": [
    {
      "candidate": "EntityName",
      "decision": "promote | absorb | merge | extend | defer | reject",
      "rationale": "Evidence-grounded explanation",
      "source_chunks_read": ["blk_xxx", "blk_yyy"],
      "stories_read": ["Story Name 1", "Story Name 2"],
      "mechanisms_checked": ["Mechanism Name"],
      "modeling_kind_composition": {"rule": 2, "definition": 1},
      "action_taken": "Added to concepts[] in Module X / Absorbed as property on ConceptY / etc.",
      "absorbing_concept": "ConceptY (only for absorb)",
      "surviving_name": "EntityA (only for merge)",
      "base_concept": "Base (only for extend)",
      "trigger": "promote when [condition] (only for defer)"
    }
  ]
}
```

---

## `map-model-spec.json` — scaffold extensions

These fields extend the domain view in JSON. Align with `**[foundational]`** in prose and with Phases **4–7** in `[content/parts/process.md](../content/parts/process.md)` (domain types → variants → deepen → integrate)..

Shaped stories live in **`phase3/shaped_story_map.json`** at the root of **`output_dir`** (see [shaped-story-map.md](../phases/shaped-story-map.md)); **`map-model-spec.json`** holds modules and **`concepts[]`** only.

| Field                            | Where          | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `**phase`**                      | root           | Named pipeline **step** from `**content/parts/process.md`** (e.g. domain types, variant classification) — not a numeric id only.                                                                                                                                                                                                                                                                                                                   |
| `**phase_note`**                 | root           | Optional free-text note (status, counters, session notes).                                                                                                                                                                                                                                                                                                                                                                                         |
| `**module.foundational`**        | `module`       | `true` when this row carries the **foundational spine** (3–7 mechanisms); omit or `false` for peripheral modules.                                                                                                                                                                                                                                                                                                                                  |
| `**module.depends_on`**          | `module`       | Array of `{ dependent_concepts, module, provides_concepts, reason }` — consumer → provider (rule **module-depends-on** where scanners enforce it).                                                                                                                                                                                                                                                                                                 |
| `**concept.evidence_stage`**     | each `concept` | `hypothesis` (foundational spine / early scaffold breadth) → `scaffolded` (breadth **K** reads) → `deepened` (concept classes and stories).                                                                                                                                                                                                                                                                                                        |
| `**concept.foundational`**       | each `concept` | `true` for stable core types that repeat across mechanisms (same intent as `**[foundational]`** in prose).                                                                                                                                                                                                                                                                                                                                         |
| `**concept.name`** (inheritance) | each `concept` | **No separate `extends` field.** Encode **is-a** in `**name`** only, as `**Base:Extension`** (immediate superclass **:** subtype) — the same pair as prose `### **Extension** : **Base`**, packed into one string (e.g. `"Check:SkillCheck"`). Root concepts use a single name with no colon (e.g. `"Check"`). Parent and child must still resolve in `**modules_and_epics`**; use `**depends_on**` / `**open_questions**` for cross-module edges. |


**Inheritance in JSON vs markdown**


| Markdown (Domain concept heading) | `map-model-spec.json`        |
| --------------------------------- | ---------------------------- |
| `### **SkillCheck** : **Check`**  | `"name": "Check:SkillCheck"` |
| `### **Check`** (no parent)       | `"name": "Check"`            |


**Composition vs inheritance in `name`:** “has-a” (properties referencing other concepts) stays in `**properties[]` / `operations[]`** with collaborating types. “is-a” subtype layering uses `**Base:Extension`** in `**name`** (not a second field) plus shared `**owns`** / evidence on the subtype.

Epic and confirming-story naming: see `[story-map.md](story-map.md)`; module naming stays **noun phrase**, epic/story **Verb Noun** (verb-noun rule). `**concepts[].name`** and domain words in `**epic.statement`** / `**confirming_stories`** must match **exactly (100%)** — rule **scaffold-concept-story-name-alignment** where enforced.

### Relationships between concepts — plan and checks

**Primary (automated):** Rule **`map-model-relationships`** with scanner **`scripts/scanners/map_model_relationships.py`** runs in the **`build.py`** pipeline when **`map-model-spec.json`** exists. It enforces **reference integrity**: every **`depends_on[].concept`** names a declared **`concept.name`**; every **`module.depends_on`** entry references existing **module** names and **concept** names in **`dependent_concepts`** / **`provides_concepts`**. It does **not** check acyclicity or semantic relation types — only resolution. See **`[map-model-relationships-plan.md](map-model-relationships-plan.md)`** and **`[../../rules/map-model-relationships.md](../../rules/map-model-relationships.md)`**.

#### Where to attach `depends_on` (pre- vs post-property)

| Situation | Guidance |
|-----------|----------|
| **Before** properties/operations exist | **Concept-level** `depends_on` alone is OK as a scaffold. |
| **After** properties and/or operations are filled in | **Authoritative** collaborations belong on **`properties[]` / `operations[]`** `depends_on` (who collaborates on which field or behavior). |
| **Optional class-level** `depends_on` | Allowed as a **diagram summary** only if every peer also appears on **at least one** property or operation under that concept (**subset sync** — enforced by the scanner when members exist). |

#### Optional product patterns (non-normative)

Workspace specs may use extra concepts for RAG-style systems: e.g. **hub source tree** vs **chat UI** aggregates, **scope filters** from hub folders, **conversion → chunk → vector** artifacts, **folder-level pipeline rollup** from per-file stages. Name and module layout are **product-specific**; the skill only requires resolved names and the **`depends_on`** rules above.

**Optional:** Narrative **scenario walkthroughs** ([`scenario-walkthrough-template.md`](scenario-walkthrough-template.md)) and sidecar **`scenario_walkthroughs.json`** beside **`map-model-spec.json`** stress-test collaborations against **`shaped_story_map.json`**; they do **not** replace structural validation.

---

## Example 1: Concept and Example Table

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

---

## Example  2: Domain model for country-specific payment

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

---

## Validation checklist

- Format: `**Extension** : <Base Concept if any>` when there is inheritance; otherwise a single concept name (see `**Base:Extension**` in `map-model-spec.json` above)
- **Continual refinement:** phased updates to the same concepts; **`**newly added**`** on new member lines when you want explicit deltas; class diagram re-rendered when `map-model-spec.json` changes materially (see [class-diagram-from-spec.md](class-diagram-from-spec.md))
- Module has examples: one table per concept, shared scenario, `===` separator
- Properties, operations, collaborating concepts listed
- Each concept referenced via `**Concept**` in story map must exist here (see `[story-map.md](story-map.md)`)
- Invariants under specific property/operation they apply to
- No implementation details (APIs, services, databases, UI components, code)
- No speculation beyond the provided material
- Everything at logical/domain level

