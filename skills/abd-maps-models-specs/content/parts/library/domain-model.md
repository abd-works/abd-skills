# Domain model

Enduring reference for **modules**, **`concepts[]`**, examples, and inheritance. **Process** follows Phases 0–8 in [`content/parts/process.md`](../content/parts/process.md) and [`docs/principles-and-rules.md`](principles-and-rules.md).

---

## Purpose

The **domain model** describes the **state and structure** that the story map refers to. It holds **modules** and **domain concepts**: the things that hold state, get operated on, and participate as callers, receivers, and collaborators in interactions. Every `**Concept**` referenced in the story map **appears** in the domain model so the story tree and model stay aligned.

---

## What goes in the domain model

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

## Domain model format (prose)

### Module

A grouping of tightly related concepts that collaborate around the same mechanism. Name + list of concepts; typically maps to one area (or page) of the class diagram.

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
- examples: at end of module, after all concepts; one table per concept; shared scenario links the module
```

### Domain concept

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

## `map-model-spec.json` — scaffold extensions

These fields extend the domain view in JSON. Align with **`[foundational]`** in prose and with Phases **4–7** in [`content/parts/process.md`](../content/parts/process.md) (domain types → variants → deepen → integrate). Older pipelines used separate `parts/steps/*` files; **this skill** encodes spine/breadth in **process + automation + scanners** on `map-model-spec`.

| Field | Where | Purpose |
|--------|--------|---------|
| **`phase`** | root | Named pipeline **step** from **`content/parts/process.md`** (e.g. domain types, variant classification) — not a numeric id only. |
| **`phase_note`** | root | Optional free-text note (status, counters, session notes). |
| **`module.foundational`** | `module` | `true` when this row carries the **foundational spine** (3–7 mechanisms); omit or `false` for peripheral modules. |
| **`module.depends_on`** | `module` | Array of `{ dependent_concepts, module, provides_concepts, reason }` — consumer → provider (rule **module-depends-on** where scanners enforce it). |
| **`concept.evidence_stage`** | each `concept` | `hypothesis` (foundational spine / early scaffold breadth) → `scaffolded` (breadth **K** reads) → `deepened` (concept classes and stories). |
| **`concept.foundational`** | each `concept` | `true` for stable core types that repeat across mechanisms (same intent as **`[foundational]`** in prose). |
| **`concept.extends`** | each `concept` | Optional string: **immediate superclass** concept name. Maps prose **`### **Child** : Parent**`** — the parent named after the colon. **Omit** (or `null`) for root/base concepts in a hierarchy. Parent must exist elsewhere in **`modules_and_epics`** (any module); **`no-duplicates`** keeps names unique. If inheritance is real but parent lives in another module, still set **`extends`** and ensure **`depends_on`** / **`open_questions`** reflect the cross-module edge. |

**Inheritance in JSON vs markdown**

| Markdown (`docs/domain-model.md` — Domain Concept) | `map-model-spec.json` |
|-----------------------------------------------|------------------------|
| `### **SkillCheck** : **Check**` | `"name": "SkillCheck", "extends": "Check"` |
| `### **Check**` (no parent named) | no **`extends`** field (root for that branch) |

**Composition vs extends:** “has-a” (properties referencing other concepts) stays in **`properties[]` / `operations[]`** with collaborating types. “is-a” subtype layering uses **`extends`** plus shared **`owns`** / evidence on the child.

Epic and confirming-story naming: see [`story-map-narrative.md`](story-map-narrative.md); module naming stays **noun phrase**, epic/story **Verb Noun** (verb-noun rule). **`concepts[].name`** and domain words in **`epic.statement`** / **`confirming_stories`** must match **exactly (100%)** — rule **scaffold-concept-story-name-alignment** where enforced.

---

## Example — connected concepts with tables

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

## Example — domain model for country-specific payment

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

- [ ] Format: `**Concept** : <Base Concept if any>`
- [ ] Module has examples: one table per concept, shared scenario, `===` separator
- [ ] Properties, operations, collaborating concepts listed
- [ ] Each concept referenced via `**Concept**` in story map must exist here (see [`story-map-narrative.md`](story-map-narrative.md))
- [ ] Invariants under specific property/operation they apply to
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level
