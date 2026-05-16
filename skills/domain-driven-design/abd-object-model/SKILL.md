---
name: object-model
catalog_garden_order: 6
description: >-
  Build a typed object model for a module. A CRC model makes it faster but is
  not required. Use when a module needs a typed domain surface before writing
  production code, or when a module has reached state: crc.
---
# object-model

## Purpose

Build a typed object model for a module. When a CRC model exists it is the primary input — the skill converts that behavioral model into a typed domain surface with far less effort. Without a CRC the skill can still produce an object model directly from domain knowledge.

## When to use

- The team knows what each class is responsible for and needs to formalise those responsibilities as typed properties and method signatures.
- You need to see explicit types, operation signatures, and ownership relationships before writing production code.
- Collaborators between classes need to become typed, directional relationships with ownership semantics made explicit.

## Core concepts

Before proceeding, read [`common/oo-concepts.md`](../common/oo-concepts.md) **carefully and in full**. The sections below cover what is specific to this level of fidelity: typed notation and relationship flavors.

### Properties

Write each property as `+ propertyName: Type`. Type it where the domain makes the type obvious (`String`, `Boolean`, `Money`, `List<Item>`, etc.); leave it untyped only when the domain is genuinely ambiguous. Typed constants and enum-like value sets (`UPPER_CASE` names) are grouped under a named constant block.

### Operations

Write each operation as `+ methodName(param: Type): ReturnType`. Parameters come from the information the method needs but does not already hold as a property; the return type reflects what the caller expects back. Keep signatures at the domain level: no infrastructure, no UI, no framework types. Omit the return type only when the operation is genuinely void.

Use `+` for public operations that external collaborators call. Use `-` for private helpers that are only called internally by the class itself — extracted sub-logic, tie-breakers, guard checks, etc.

**When the right name is unclear, name it after the invariant.** If an operation's invariant says "incoming supersedes existing", the operation is `incomingSupersedes`. The invariant is already the correct domain statement — the name should match it directly rather than inventing a separate label.

```
- incomingSupersedes(existing: ImposedCondition, incoming: Condition): Boolean
	Invariant: if incoming supersedes existing — remove existing, return true; if existing supersedes incoming — return false
```

### Object initialisation

For every class, determine how its objects are initialised. Choose from the following approaches based on scenario and context:

**Constructor injection** — pass a dependency in when the class references but does not own it (association), or when a required value must be present for the object to be valid. Write as `+ ClassName(param: Type, ...)`. Include only what is needed to bootstrap a fully valid object; never leave an object half-initialised. Write multiple constructors when different valid bootstrap configurations exist in the domain.

```
+ Ability(character: Character, rank: Integer)
+ Ability(character: Character, rank: Integer, extras: List<Extra>)
```

**Internal initialisation** — create or derive it inside the class when the class owns the thing (composition) or when the value is derived from properties the object already holds. The caller should not be responsible for assembling parts the class owns. An airplane assembles its own engines; it does not receive them as constructor arguments.

**Factory method** — use a static factory *on the class itself* when construction is complex, can fail gracefully, or needs to return different subtypes based on input. The factory method replaces `new` for callers — it is a named static operation on the class.

```
+ Payment.create(type: PaymentType): Payment   → returns CreditCardPayment or BankTransferPayment
```

> **Do not confuse:** if another class produces instances of this class by calling `new ClassName(...)`, that is normal construction — the class still shows its constructor. The fact that `Check.resolve()` creates a `CheckResult` via `new CheckResult(...)` does not make `CheckResult` a factory-method class; it just has a constructor that `Check` calls.

**Factory object** — delegate construction entirely to a separate domain object when the assembly logic is itself a domain concern, when multiple unrelated callers need the same complex build, or when the assembled object requires coordinating many collaborators the caller should not know about.

```
CharacterBuilder → produces a fully loaded Character with abilities, skills, and powers
```


### Relationships

The three questions in `oo-concepts.md` (`## Relationships`) determine the dependency nature. At this level of fidelity, each answer maps to a named type of relationship:

- **Aggregation** — the parent exists to collect or group its children; the parent has no identity without them (a flock, an army, a server cluster).
- **Composition** — the child has no identity without the parent; the parent owns the child's lifecycle (airplane wings, a car's steering wheel).
- **Association** — both sides have independent lifecycles.

**Association is the default** — no annotation needed. Mark composition and aggregation directly on the property with a stereotype; no separate relationship line is required.

```
+ << composition >> stages: List<DifficultyStage>   ← ownership is on the property
+ linkedTrait: Trait                                 ← plain association; no stereotype
```

The property type already implies cardinality direction: a single type is 1..1; `List<T>` or `Dictionary<K,T>` is one-to-many. Use an invariant on the property when the cardinality constraint needs to be made explicit (e.g. "at least one stage required"). Do not write separate `*composes*`, `*aggregates*`, or `*associates*` relationship lines — the stereotype and property type together carry the full picture.

### Collections

When a class holds multiple instances of another class, type the property using one of two generic forms:

- **`List<ClassName>`** — an ordered or unordered set where you iterate or process all members. Use when the caller works through the whole set or picks by position. No key needed.
- **`Dictionary<KeyType, ClassName>`** — a keyed set where you need to look up a specific member directly. Use when the caller retrieves by a known identifier (id, name, code) and traversing the whole set would be wasteful.

```
+ appliedConditions: List<ImposedCondition>       ← iterate all when no behavior; use when collection is simple
+ abilitiesByName: Dictionary<String, Ability>    ← look up by name directly
```

The name of the property should reflect the domain collection concept, not the data structure — `appliedConditions`, not `conditionList`. When the collection itself has unique behavior (supersession logic, ordering rules, add/remove constraints), introduce a named collection class that owns that behavior rather than holding a raw `List` or `Dictionary` directly on the parent class.

```
+ << composition >> imposedConditions: ImposedConditions   ← named collection class: owns supersession logic
```

### Inheritance

Use `ChildClass : ParentClass` on the class heading. The child block contains only delta members — typed properties, operations, and relationships that add or override the parent. Inherited members are never repeated — see `## Inheritance and subtypes` in `oo-concepts.md` for the delta rule.

```
ChildClass : ParentClass
+ addedProperty: Type
+ overriddenMethod(param: Type): ReturnType
```

Mark each class with its stereotype on the heading — see `### Entities and Value Objects` below.

### Invariants

Write each invariant as a single tab-indented line directly under the property or operation it constrains: `	Invariant: ...`. Keep it declarative — "must", "cannot", "only if". One line per constraint; long lifecycle prose stays in the CRC content above.

### Interactions

When an operation has inherent complexity or interesting interactions — it coordinates multiple collaborators, produces a result through a chain of internal steps, or branches in a way not captured by the signature and invariants alone — write a tab-indented `Interaction:` block directly after the operation's invariants. Each step is a flat, non-nested pseudocode line using the scenario-walkthrough notation.

CRC collaborators that did not map to operation parameters are a useful signal: they are likely accessed internally, and the step-chain should be made explicit so that behavior is not lost.

**When to omit:** Simple delegations with a single step, pure queries that return a property directly, or operations whose entire behavior is self-evident from the return type and invariants alone.

**Design smell — invariants without interactions:** If an operation carries several invariants but no `Interaction:` block, that is almost always wrong. Invariants state *what must be true*; they cannot replace the step-chain that *makes it true*. Many invariants signal that the operation is doing real work internally — that work must be made explicit in an `Interaction:` block.

**Extract complex sub-logic into named operations.** An `Interaction:` block is not pseudocode — it traces the key collaborations. When a branch or calculation is non-trivial, give it a name, extract it as a separate operation, and describe its rule as an invariant. Call that operation from the interaction instead of spelling out every line.

```
+ resolve(): CheckResult
	Interaction:
		...
		if activeResult.margin != 0: return activeResult
		return resolveTie(activeResult: activeResult, opposingResult: opposingResult)
- resolveTie(activeResult: CheckResult, opposingResult: CheckResult): CheckResult
	Invariant: higher rank bonus wins; if ranks are equal, d20 decides (1–10 active wins, 11–20 opposing wins)
```

> **Visibility:** extracted helper operations that are only called internally use `-` (private). Public operations that callers invoke use `+`.

```
+ resolve(): CheckResult
	Invariant: shape is always rollTotal vs dc.value; subtypes vary only how total or DC is produced
	Interaction:
		roll: Integer = d20.roll()
		total: Integer = trait.rank + roll + circumstanceModifier.value
		success: Boolean = total >= dc.value
		result: CheckResult = new CheckResult(roll: roll, rollTotal: total, isSuccess: success, check: this)
		return result
```

**Format rules:**
- `	Interaction:` is tab-indented under the operation, same level as `Invariant:`
- Each step inside is a further-indented flat line — **no nesting**
- Use typed pseudocode: `variableName: Type = expression`
- Method calls: `object.method(param: value)`
- Construction: `variable: Type = new ClassName(param: Type)`
- Return: `return variable` or `return variable: actual_value`
- Comments for logic not yet decomposed: `// degree logic`
- **Variable names must use domain language** — `roll`, `margin`, `throwingDistanceMeasure`, not `r`, `temp`, `measureA`. Trace the right name up the chain: CRC → Ubiquitous Language → ubiquitous language → source references.

### Entities and Value Objects

Domain objects carry one of several stereotypes depending on their role. The two most common are Entity and Value Object — classify each domain object before writing its members, because the kind determines immutability rules, how equality works, and how objects are initialised. Other stereotypes exist (`<< Service >>`, `<< Factory >>`, `<< Repository >>`, `<< Domain Event >>`, boundary types, etc.) and are applied when the class clearly plays that role.

**Entity** — an object distinguished by identity, not by its attributes. Two entities with identical attributes are still different things. An entity has a continuous lifecycle: it is created, changes over time, and eventually ends. The model must define what it means for two instances to be the same entity.

Mark with `<< Entity >>`.

```
Character  << Entity >>       ← two characters with the same name are different people
Order  << Entity >>           ← two orders placed by the same customer are different orders
```

**Value Object** — an object defined entirely by its attributes, with no meaningful identity of its own. Two value objects with the same attributes are interchangeable — they *are* the same thing. Value objects are immutable: never modify one in place; replace it with a new instance that has the updated values. Operations on a value object return new instances and have no side effects.

Mark with `<< ValueObject >>`.

```
Rank  << ValueObject >>       ← Rank(5) and Rank(5) are the same rank; replace, don't mutate
Money  << ValueObject >>      ← $10 is $10 regardless of which Money instance holds it
DifficultyClass  << ValueObject >>
```

**The deciding question for Entity vs Value Object:** *Does this thing need to be tracked as an individual over time, or does only the combination of its values matter?* If tracking individual identity matters — use Entity. If only the values matter — use Value Object.

> *Source: Evans, Domain-Driven Design Reference (2015) — Entities and Value Objects patterns.*


---


Shared reference for all abd-domain-driven-design skills. This file owns the OO theory. Each skill owns its own notation and format.

---

### What is a class

> **Applies from: ubiquitous language stage and beyond (ubiquitous language → CRC → object-model).**

A class is a named domain idea that earns its own identity because it has at least one of: **distinct identity**, **state**, **behavior**, **structure**, or **interactions** that cannot be collapsed into a property, instance, or type property of something else.

A class knows things (**state**) and does things (**behavior**). Those two dimensions — together with the relationships it maintains and the invariants that constrain it — are what a class IS at every level of fidelity. The notation changes across the pipeline; this definition does not.

A term that is only a data value on another class is a **property**. A term that varies only by label across identical behavior is a **type property**. A term that is one concrete member of a known set is an **instance**. A term that adds distinct behavior to a base is a **subtype**. Only when none of those fit does something deserve its own class.

Each skill records a class in its own form:
- **ubiquitous-language** — a named concept block with intent, behaviors, and collaborations in plain English.
- **CRC** — a `#### **ClassName**` block with responsibility and collaborator columns.
- **Object-model** — a typed class block with properties, operation signatures, relationships, and invariants.

---

### Decomposing responsibilities

> **Applies from: CRC stage and beyond (CRC → object-model → ...).** Do not use this section at ubiquitous language level — there are no typed properties or operations at that stage.

A responsibility is either something a class **holds** (state) or something it **does** (behaviour) — or both. Classify each responsibility before deciding how to represent it:

- **Property** — the class must remember something across calls. Named as a **noun phrase**: *remaining budget*, *active status*, *target character*.
- **Operation** — the class must perform an action or compute a result; it may be entirely stateless. Named as a **verb phrase**: *calculate shipping cost*, *apply condition*, *resolve check*.
- **Both** — the class holds state **and** exposes an action that works with it.

Never assume every responsibility implies a property, and never assume every responsibility implies an operation. Ask for each one: *hold something, do something, or both?*

---

### Relationships

> **Applies from: CRC stage and beyond (CRC → object-model).** At ubiquitous language level, dependencies are captured as plain-English collaboration sentences only — no formal relationship modeling.

A relationship describes how two domain classes depend on each other. Before recording a relationship, answer three questions:

1. **Does one class own the other's lifecycle?** — The other cannot exist without the first. If the owning class is gone, so is the owned one.
2. **Does one class exist to collect or group the other?** — The collecting class has no meaningful identity without its members. Remove all members and the collector is empty of purpose.
3. **Are both sides independent?** — Each can exist and be meaningful without the other.

These questions determine the nature of the dependency. Each skill records the answer in its own notation — plain-English collaborations at ubiquitous language level, named collaborators at CRC level, typed flavors with cardinality at object-model level.

A relationship also has **direction**: the class that depends on, uses, or navigates to the other is the navigating end. Be explicit about which side initiates the dependency.

---

### Inheritance and subtypes

> **Applies from: ubiquitous language stage and beyond (ubiquitous language → CRC → object-model).**

#### Base class and subtype

A **base class** (also called a parent or superclass) defines the common identity, state, and behavior shared by a family of related things. It owns everything that is true of every member of that family — the responsibilities, rules, and collaborations that do not change regardless of which specific variant you are dealing with.

A **subtype** (also called a child class or subclass) is a specialisation of the base. It *is a kind of* the base — everything the base defines applies to it — but it adds or overrides behavior that is specific to it alone. The subtype does not restate what it inherits; it only describes the delta.

**Inheritance** is the mechanism that connects them. The subtype inherits all of the base's identity and behavior automatically. The base never knows about its subtypes; the subtypes always know about their base.

A family can have many subtypes, each specialising the base in a different direction. Subtypes can themselves be bases for further subtypes — but depth should reflect real behavioral distinctions in the domain, not structural tidiness.

#### Liskov Substitution rule

**Anywhere the base is used, a subtype must work correctly in its place.** If swapping in a subtype breaks or weakens a rule the base guarantees, the subtype is not a true specialisation — it is a different thing that happens to share some behavior.

In practice: a subtype may *add* behavior and *strengthen* constraints, but it must never *remove* behavior or *weaken* a guarantee the base makes. If you find yourself writing a subtype that overrides a base operation to do nothing, throw an error, or return a narrower result than the base promises, stop — that is a modeling error, not a subtype.

#### When to use a subtype, type property, or instance

When a term looks like "a thing is a kind of another thing," three modeling options exist:

**Subtype** — the specialised thing adds **behavior the base does not have**. Each subtype does something differently enough that you need to describe it separately. Use this when the distinction changes **what the thing does**, not just what data it carries. Example: an *international shipment* is a type of *shipment* — it introduces customs filing and duty handling that a domestic shipment does not have.

**Type property (constrained list)** — the thing varies by **category**, but every category follows the **same behavior**. The difference is purely which label from a known list applies. Use this when you could swap one label for another and the behavior description would not change. Example: a *notification* has a *notification priority type* drawn from (*low*, *normal*, *urgent*) — every notification still has a recipient, still carries a message, still follows the same delivery and read-receipt rules. The *notification priority type* tells you how soon it surfaces, not how it behaves differently.

**Instance** — the thing is one **concrete member** of a parent concept, distinguished only by its **specific data values**. Many instances exist side by side and they all work the same way — each just carries different numbers or names. Use this when listing them out would produce rows that repeat the same structure with different fill. Example: *bronze*, *silver*, *gold* are all instances of *membership tier* — each names a specific discount rate and benefit set, but they all follow the same upgrade, renewal, and expiry rules that Membership Tier defines.

A common modeling journey begins with treating domain elements as *instances* or *type properties*, and as understanding of behavior differences grows, promotes them into subtypes.

**Example — Evolving a Payment System Domain Model:**

- **Early model (Instances or Type properties):**
  - Model *Payment* as a concept.
  - Each *payment* instance carries data like channel (e.g., "credit card", "bank transfer"), transaction amount, reference id, etc.
  - All payments go through the same core behaviors: *initiate payment*, *set channel*, *approve transaction limit*.

- **Transition point:**
  - As behaviors diverge (e.g., approval workflow or fraud checks differ by channel), notice that some payment types must satisfy additional steps or rules.
  - Subtle differences in fulfillment or submission arise: submitting a bank transfer may require different fields or succeed asynchronously, while a credit card might authorize instantly.

- **Evolved model (Subtypes):**
  - Define subtypes such as `CreditCardPayment`, `BankTransferPayment`, each *is a type of* `Payment`.
  - Each subtype describes behaviors *only* where they differ — `CreditCardPayment` enforces an online authorization step; `BankTransferPayment` requires reference code validation and may be fulfilled later.
  - Shared behaviors (initiate, submit) stay on the base `Payment`.
  - Now *type* drives both *attached data* and *behavior*.

> When a domain element's *type* alters not only the data needed but also the sequence of steps or the rules followed, it's time to promote from type-property instances to true subtypes with their own behaviors.

#### The delta rule

A subtype carries **only what it adds or overrides**. Inherited responsibilities are not repeated at any level of fidelity — ubiquitous-language, CRC, or object model. If the parent owns a responsibility, the subtype block is silent on it.

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]object-model.md
```

**File name:** Default to `object-model.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `object-model.md` and `<name>-object-model.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-object-model.md`.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output already lives in a folder, write next to it.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**.

The file is **not** an in-place enrichment of the CRC file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Consistent shape (used by every DDD phase skill)

```
## **{{KAName}}**

[Optional 1–2 sentence intro]

### **{{ka_name as a Class}}** << Stereotype >>      ← MUST appear first; matches the KA
+ Constructor(param: Type)
------
+ property: Type
	Invariant: rule
+ << composition >> ownedProperty: Type
----
+ operation(param: Type): ReturnType
	Invariant: rule
	Interaction:
		variable: Type = expression
		return variable

### **{{another Class}} : {{BaseClass}}** << Stereotype >>
+ deltaProperty: Type
+ overriddenOperation(param: Type): ReturnType

### references                                       ← one per KA, peer to classes
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made                                   ← one per KA, peer to classes
- decision rationale
```

The Boundary Domain is one flat group with shared `### references` and `### decisions made`.

---

## Build

1. **Read the prerequisite file.** If a `<deliverables-folder>/<name>-crc.md` exists, use it as the primary input — it is the richest source. If not, work from `<name>-ubiquitous-language.md` or any available source describing the classes and their behavior.
2. **Identify classes.** From the CRC (if present) or domain knowledge, list every class that needs a typed block, including subtypes and collection classes. Group them under their `## **KA**` from the prior phase.
3. **Decompose responsibilities.** For each class, look at its responsibilities. Ask: *does this require the class to hold something (→ property), do something (→ operation), or both?* Route each responsibility before writing anything.
4. **Write the typed class blocks.** Under `# Core Domain`, for each KA from the prior phase:
   - `## **KAName**` heading.
   - `### **ka_name_as_a_Class** << Stereotype >>` — the KA's own class, listed FIRST, with constructor, properties, operations, invariants, and `Interaction:` blocks.
   - `### **another Class** << Stereotype >>` for each grouped concept. Subtypes use `### **ChildClass : BaseClass** << Stereotype >>` and carry only deltas.
   - `### references` listing all Refs for classes in this KA, with fenced ```source``` blocks.
   - `### decisions made` listing object-model judgments (constructor injection vs internal init vs factory; relationship flavor; Entity vs Value Object; collaborator-omission decisions; lifecycle observations).
5. **Determine object initialisation.** For each class, scan its properties and choose constructor injection, internal initialisation, factory method, or factory object — see `### Object initialisation`.
6. **Derive relationships.** Mark composition and aggregation with a stereotype on the property (`<< composition >>`, `<< aggregation >>`). Leave plain associations unannotated.
7. **Add invariant lines.** Each as a tab-indented `Invariant: ...` line directly under the member it constrains.
8. **Add interaction blocks.** For each operation with inherent complexity, write a tab-indented `Interaction:` block tracing the step-chain. CRC collaborators not mapped to parameters are a useful signal.
9. **Set the state marker** to `domain-model`.
10. **Write the file** to `<deliverables-folder>/<name>-object-model.md`. Use `----` for clusters within a class and follow `templates/domain-model-scaffold.md` for placeholder shapes.

## Templates

`templates/domain-model-scaffold.md`

## Validate

- **Per-phase output file.** The file is named `<name>-object-model.md`. No prior or later phase content lives in it.
- **Every KA has a class that names it.** Every `## **KA**` heading is followed by a `### **Class** << Stereotype >>` whose name matches the KA itself, listed first.
- **No sub-headings under classes.** Class member blocks live directly under each `### **Class**` heading. No `#### Object Model`, `#### References`, or `#### Decisions made` sub-sections.
- **References per KA with verbatim source blocks.** One `### references` per KA, every `**Ref —**` followed by a fenced ```source``` block of verbatim text.
- **Decisions per KA.** One `### decisions made` per KA listing object-model judgment calls.
- Every class has a typed block. A class with only stateless behavior may have zero properties — that is valid.
- Every property is typed and justified by a domain responsibility that requires stored state.
- Every operation is a fully typed signature — `+ methodName(param: Type): ReturnType` — with no untyped parameters or missing return types.
- Every class has object initialisation using a combination of decisions — constructor, internal initialisation, factory method, or factory object.
- Every composition or aggregation property carries a `<< composition >>` or `<< aggregation >>` stereotype. Plain association properties have no stereotype.
- Every subtype block contains only delta members — no inherited properties, operations, or relationships are repeated.
- Every invariant is a single tab-indented declarative constraint under the member it constrains — none are invented beyond what the domain supports.
- Every operation with inherent complexity or interesting interactions has an `Interaction:` block. Operations that are simple delegations or whose behavior is self-evident from the return type and invariants may omit it.
- No operation carries multiple invariants without an `Interaction:` block. Several invariants signal that real internal work is happening — that work must be made explicit.
- Every CRC collaborator for a responsibility is accounted for — either as a parameter, return type, property type, or a step in the `Interaction:` block. No collaborator is silently dropped. Intentional exclusions are recorded as decisions.
- Every variable name inside an `Interaction:` block uses domain language drawn from the ubiquitous language, Ubiquitous Language, or CRC. Generic placeholders (`measureA`, `result`, `temp`, single letters) are not acceptable. When the right name is unclear, trace up: CRC → Ubiquitous Language → ubiquitous language → source references.
- Walkthrough scenarios (if present) can still be stepped with the new typed names (spot-check at least one).
- The YAML front-matter reads `state: domain-model`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The object-model skill writes a self-contained file at `<deliverables-folder>/<name>-object-model.md`. It does **not** enrich the prior phase's file in place. The output uses the consistent flat heading shape every DDD phase skill shares: `## **KA** → ### **Class** (with class members directly under) → ### references → ### decisions made`.

#### DO

- Write the file to `<deliverables-folder>/<name>-object-model.md`.

  **Example (pass):** `domain/paw-place-object-model.md`.

- Place class members (constructor, properties, operations, invariants, interactions) directly under each `### **Class**` heading.

#### DO NOT

- Add typed class blocks as a sub-section inside the prior phase's file.

  **Example (fail):** Edit `paw-place-crc.md` to insert typed class blocks — that is in-place enrichment which produces unrecoverable heading drift.

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a class that names the KA itself

**Scanner:** AI review

Every `## **KA**` heading must be followed by a `### **Class** << Stereotype >>` whose name matches the KA itself, listed **first** under the KA, with its full typed block (constructor, properties, operations, invariants, interactions). The KA's own class carries the abstraction's behavior, identity, and invariants.

#### DO

- List the KA's own class first under the `## **KA**` heading.

  **Example (pass):**
  ```
  ## **Check**

  ### **Check** << Entity >>           ← first; matches the KA
  + Check(trait: Trait, dc: DifficultyClass)
  ------
  + trait: Trait
  + dc: DifficultyClass
  ----
  + resolve(): CheckResult
      Interaction:
          ...

  ### **DifficultyClass** << ValueObject >>
  + value: Integer
  ```

#### DO NOT

- Skip the KA's own class.

  **Example (fail):**
  ```
  ## **Check**

  ### **DifficultyClass** << ValueObject >>     ← subordinate first; missing ### **Check**
  ```

**Source:** Correction — engagement repo (paw-place); KA's own term must be the most important class modeled.

### Rule: All CRC collaborators are accounted for in the typed member

**Scanner:** Manual review

Every collaborator listed for a CRC responsibility must appear somewhere in the corresponding typed property or operation. A collaborator may be accounted for as:

1. A **parameter** to the operation
2. The **return type** of the operation
3. A **type** on the property
4. A step in the **`Interaction:`** block

If a collaborator appears nowhere in 1–4, it has been silently dropped. That is a modeling gap — either the collaborator belongs in the signature, the property type, or the interaction, or a deliberate decision to exclude it must be recorded.

#### DO

- Account for every collaborator in the parameter list, return type, or interaction.

  **Example (pass):** CRC responsibility: `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result`

  None of these are parameters on `+ resolve(): CheckResult`. They are all internal. Every one must appear in the `Interaction:` block:
  ```
  + resolve(): CheckResult
      Invariant: shape is always rollTotal vs dc.value
      Interaction:
          roll: Integer = d20.roll()                              ← D20 accounted for
          total: Integer = trait.rank + roll + circumstanceModifier.value   ← Trait, CircumstanceModifier
          success: Boolean = total >= dc.value                   ← DifficultyClass (dc)
          margin: Integer = total - dc.value
          result: CheckResult = new CheckResult(...)             ← CheckResult
          return result
  ```

- Account for a collaborator as a property type when the responsibility becomes a property.

  **Example (pass):** CRC responsibility: `difficulty ladder | Difficulty Ladder` becomes `+ difficultyLadder: DifficultyLadder` — collaborator is the property type.

#### DO NOT

- Drop a collaborator silently.

  **Example (fail):** CRC responsibility `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result` becomes:
  ```
  + resolve(): CheckResult
  ```
  with no `Interaction:` block — D20, Trait, CircumstanceModifier, and DifficultyClass are all unaccounted for.

- Assume a collaborator is "obvious" and omit it from the model.

  **Example (fail):** Interaction traces `d20.roll()` but never references `trait.rank` or `dc.value` — Trait and DifficultyClass are dropped.

#### When a collaborator is intentionally excluded

Record it as a decision: state which collaborator is excluded and why (e.g., "D20 is an internal implementation detail not exposed at this fidelity level"). Without an explicit decision, any missing collaborator is a gap.

**Source:** Engagement convention (object-model skill).

### Rule: Dependency magnet — split unrelated business concerns

**Scanner:** Manual review

A class whose **properties, operations, and typed relationships** span **multiple unrelated business concerns** acts as a **dependency magnet**: unrelated domain areas converge on one type, which makes the model brittle and couples changes that should be independent. At object-model fidelity, the smell shows up as member clusters that do not share a coherent story — disparate collaborators, unrelated invariants, or operations that read like a cross-cutting checklist. Split by moving coherent groups to focused classes or collaborators (align with any CRC split; if CRC already separated concerns, the typed blocks should mirror that separation).

#### DO

- Group members by concern; if one class mixes unrelated areas (for example catalog + billing + notifications), extract types so each class has one coherent responsibility thread. Collaborators and `Interaction:` blocks should tell one story per class.

  **Example (pass):** `Order` exposes coordination; `OrderPricing`, `Shipment`, `PaymentAuthorization` own their operations and properties instead of overloading `Order` with every detail.

#### DO NOT

- Leave one class as a hub for unrelated domains with no structural boundary.

  **Example (fail):** A single class exposes tax calculation, email dispatch, inventory validation, and PDF generation — each with different collaborator types and no domain reason for them to share one type.

**Source:** Engagement convention (object-model skill).

### Rule: Explicit chain of responsibility — no nebulous operations

**Scanner:** Manual review

When a typed operation implies a chain of actors or steps, every actor in that chain must be traceable to a typed property or operation with explicit parameters in the object model. Nothing may be left implied or nebulous. "May" and "requires" language in a behavior must be fully modeled as typed members.

#### DO

- Trace each step in the implied chain to a named typed operation or property.

  **Example (pass):** Behavior: "may be ongoing for a target character: requires a resistance check at the end of each of the target's turns until ended."

  This implies: someone tracks which characters are ongoing targets, and someone triggers end-of-turn resistance checks. The object model must reflect both:
  ```
  PowerEffect : Trait
  + << aggregation >> ongoingTargets: List<Character>
  + resist(effect: PowerEffect, check: Check): void    ← on OngoingEffects, not PowerEffect
      Invariant: resistance check made at end of each of the character's turns while effect is active
  ```

  **Example (pass):** Behavior: "supersedes a less severe condition from the same source — removing the lesser."

  This implies: someone knows the supersession hierarchy, and someone performs the removal. Both must appear — `+ supersedes: Condition` on `Condition` and `+ applyCondition(...)` with the supersession invariant on `ImposedConditions`.

#### DO NOT

- Write a property and leave the downstream action it implies without an owning operation.

  **Example (fail):**
  ```
  PowerEffect
  + ongoingTargets: List<Character>   ← who triggers the end-of-turn resistance check? No operation owns it.
  ```

- Leave "may" or "requires" language from a behavior with an incomplete typed chain.

  **Example (fail):** Behavior says "requires a resistance check at end of each turn" but no operation for triggering that check appears anywhere in the model.

- Leave an implied collaborator out of the operation signature.

  **Example (fail):**
  ```
  + resist(check: Check): void   ← missing the PowerEffect parameter; which effect is being resisted?
  ```

**Source:** Engagement convention (object-model skill). Adapted from class-responsibility-collaborator/rules/explicit-chain-of-responsibility.md.

### Rule: Extract complex sub-logic to a named operation

**Scanner:** Manual review

An `Interaction:` block traces the key collaborations of an operation — it is not pseudocode. When a branch or calculation inside an interaction is non-trivial, extract it into a named operation with an invariant describing the rule. Call that operation from the interaction instead of expanding every line inline.

#### DO NOT

Spell out multi-step branching logic inside an interaction block.

```
+ resolve(): CheckResult
	Interaction:
		...
		if activeResult.margin != 0: return activeResult
		// exact tie: higher rank bonus wins
		if trait.rank.value > opposingTrait.rank.value: return activeResult
		if opposingTrait.rank.value > trait.rank.value: return opposingResult
		// rank tie: d20 decides (1–10 active wins, 11–20 opposing wins)
		tieBreak: Integer = new D20().roll()
		activeWins: Boolean = tieBreak <= 10
		return activeWins ? activeResult : opposingResult
```

The tie-breaking procedure is a domain rule in its own right. Burying it inside the interaction makes both operations harder to read and obscures the rule.

#### DO

Give the sub-logic a domain name, extract it as a separate operation, and describe the rule as its invariant. Call it from the interaction.

```
+ resolve(): CheckResult
	Interaction:
		...
		if activeResult.margin != 0: return activeResult
		return resolveTie(activeResult: activeResult, opposingResult: opposingResult)
- resolveTie(activeResult: CheckResult, opposingResult: CheckResult): CheckResult
	Invariant: higher rank bonus wins; if ranks are equal, d20 decides (1–10 active wins, 11–20 opposing wins)
```

The interaction stays high-level. The tie-breaking rule is declared precisely where it lives and is independently readable.

#### Guidance

- If you find yourself writing more than two or three conditional branches inside a single `Interaction:` block, that is a signal to extract.
- The extracted operation's invariant replaces the inline comments — it is the authoritative statement of the rule.
- The name of the extracted operation should come from domain language, not from implementation vocabulary (`resolveTie`, not `handleTieCase` or `processTieBreaker`).

### Rule: Interaction variable names use domain language

**Scanner:** Manual review

Variable names inside an `Interaction:` block must use domain language drawn from the ubiquitous language, Ubiquitous Language, or CRC — not generic technical placeholders. If a name is ambiguous, trace up the chain: CRC responsibility → Ubiquitous Language → ubiquitous language → source references.

#### DO

- Name variables after the domain concept they represent.

  **Example (pass):** Resolving a check:
  ```
  roll: Integer = d20.roll()
  total: Integer = trait.rank + roll + circumstanceModifier.value
  success: Boolean = total >= dc.value
  margin: Integer = total - dc.value
  result: CheckResult = new CheckResult(rollTotal: total, dc: dc, isSuccess: success, margin: margin)
  ```

  **Example (pass):** Converting ranks to measures and back:
  ```
  throwingDistanceMeasure: Number = Measurement.lookup(rank: strengthRank, type: THROWING_DISTANCE).value
  massMeasure: Number = Measurement.lookup(rank: massRank, type: THROWING_DISTANCE).value
  combined: Number = throwingDistanceMeasure - massMeasure
  throwingDistanceRank: Rank = Measurement.rankFor(measure: combined, type: THROWING_DISTANCE)
  return throwingDistanceRank
  ```

#### DO NOT

- Use generic placeholders that could mean anything.

  **Example (fail):**
  ```
  measureA: Number = Measurement.lookup(rank: this, type: type).value
  measureB: Number = Measurement.lookup(rank: other, type: type).value
  ```
  `measureA` and `measureB` say nothing about what is being measured. Name them after the domain quantities: `strengthMeasure`, `massMeasure`, `travelDistanceMeasure`, etc.

- Use single-letter names, index names, or temp/result/data patterns.

  **Example (fail):**
  ```
  r: Integer = d20.roll()
  t: Integer = trait.rank + r
  res: CheckResult = getResult(t)
  ```

#### When names are unclear

Trace up the chain:
1. Check the CRC responsibility name and its collaborator names
2. Check the Ubiquitous Language description of the behavior
3. Check the ubiquitous language definition
4. Check the source references

The right name is almost always already in the source material.

**Source:** Engagement convention (object-model skill).

### Rule: Invariant lines trace to CRC invariants or always-true rules

Every `Invariant: ...` line under a member must be sourced from the CRC `invariants:` field of the corresponding concept. Passing means each invariant is short, tab-indented under the member it constrains, and traceable to the CRC block. Failing means an invariant is invented, placed outside a member context, or contradicts the CRC source.

#### DO

- Write each invariant as a single tab-indented line directly under the property or operation it constrains, sourced from the CRC `invariants:` field.

  **Example (pass):**
  ```
  + remainingBudget: Money
  	Invariant: remainingBudget ≥ 0 (from: "budget must never go negative")
  ```

- Keep invariants declarative — "must", "cannot", "only if" — matching the CRC phrasing.

  **Example (pass):**
  ```
  + ship(destination: Address): void
  	Invariant: cannot ship unless paymentCleared is true
  ```

#### DO NOT

- Invent an invariant that has no corresponding CRC `invariants:` line.

  **Example (fail):**
  ```
  + quantity: Integer
  	Invariant: quantity must be a prime number   ← no CRC source
  ```

- Place an invariant as a free-standing line outside any member context.

  **Example (fail):**
  ```
  Invariant: total must match sum of line items
  + totalPrice: Money                             ← invariant floats above, not under a member
  ```

- Write multi-line prose instead of a single declarative constraint.

  **Example (fail):**
  ```
  + status: OrderStatus
  	Invariant: When the order transitions from pending to confirmed
  	           the system must verify that all line items are in stock
  	           ← too long; split into atomic invariants or keep prose in CRC
  ```

### Rule: Invariants without interactions

**Scanner:** Manual review

An operation that carries multiple invariants must also carry an `Interaction:` block. Invariants declare *what must be true* — they cannot replace the step-chain that *makes it true*. Several invariants are a reliable signal that the operation is performing real internal work; that work must be made explicit.

#### DO NOT

Write multiple invariants with no interaction block.

```
+ resolve(): CheckResult
	Invariant: shape is always rollTotal vs dc.value
	Invariant: subtypes vary only how total or DC is produced
	Invariant: natural 20 always yields a critical success
```

These constraints hint at internal calculations (rolling a die, summing a total, comparing to DC) that are nowhere shown. A reader cannot tell how the result is produced.

#### DO

Follow every multi-invariant operation with an `Interaction:` block that shows the steps that satisfy those invariants.

```
+ resolve(): CheckResult
	Invariant: shape is always rollTotal vs dc.value; subtypes vary only how total or DC is produced
	Interaction:
		roll: Integer = d20.roll()
		total: Integer = trait.rank + roll + circumstanceModifier.value
		success: Boolean = total >= dc.value
		margin: Integer = total - dc.value
		result: CheckResult = new CheckResult(rollTotal: total, dc: dc, isSuccess: success, margin: margin)
		return result
```

Now the invariants are backed by visible steps — the reader can see exactly how `rollTotal`, `dc`, and `isSuccess` are produced.

#### Guidance

- A single invariant on a simple setter or guard is fine without an interaction block.
- Two or more invariants — especially ones describing how values are derived or compared — require an `Interaction:` block.
- When in doubt: if the invariants collectively describe a *process*, the process belongs in `Interaction:`.

### Rule: Name operations after their invariant

**Scanner:** Manual review

When the right name for an operation is unclear, name it after the invariant. The invariant is already the correct domain statement of what the operation does — the name should match it directly rather than inventing a separate abstract label.

#### DO NOT

Invent a name that describes *how* the operation works or uses vague process words.

```
- applySupersession(...)
- handleSameSourceConflict(...)
- incomingIsBlocked(...)
```

These names either describe internal mechanics or encode the answer from the wrong perspective. A reader cannot tell what the operation asserts.

#### DO

Read the invariant and use its subject-verb as the name.

Invariant: *"if incoming supersedes existing — remove existing, return true"*

```
- incomingSupersedes(existing: ImposedCondition, incoming: Condition): Boolean
	Invariant: if incoming supersedes existing — remove existing, return true; if existing supersedes incoming — return false
```

The name *is* the invariant's claim. The invariant then fills in the detail.

#### Guidance

- This applies especially to private Boolean helpers — they answer a yes/no question about a domain rule. Name the question from the domain, not from the implementation.
- The invariant should not repeat the name verbatim — it adds precision (edge cases, side effects, return value meaning).
- If the invariant is still hard to summarise in a name, that is a signal the invariant itself needs to be sharpened first.

### Rule: Operations use typed signatures tracing to CRC verbs

Every operation must be written as a typed method signature — `methodName(param: Type): ReturnType` — and must trace to a CRC responsibility verb phrase. Passing means the signature is complete and the source verb phrase is identifiable. Failing means the operation lacks types, uses prose instead of a signature, or has no CRC verb-phrase origin.

#### DO

- Write each operation as `+ methodName(param: Type): ReturnType`, derived from a CRC "Responsible for" verb phrase.

  **Example (pass):**
  ```
  CRC — Responsible for: calculating shipping cost based on weight and destination

  Domain-model block:
  + calculateShippingCost(weight: Weight, destination: Address): Money
  ```

- Omit the return type only when the operation is genuinely void (a command with no meaningful return).

  **Example (pass):**
  ```
  + cancelOrder(reason: String): void
  ```

#### DO NOT

- Write an operation as plain prose without a typed signature.

  **Example (fail):**
  ```
  + calculates the shipping cost     ← prose, not a signature
  ```

- Add an operation that does not trace to any CRC responsibility verb phrase.

  **Example (fail):**
  ```
  CRC — (no mention of "archiving")

  Domain-model block:
  + archiveRecord(id: RecordId): void   ← invented, no CRC source
  ```

- Leave parameters or return types untyped when the domain makes the type obvious.

  **Example (fail):**
  ```
  + calculateShippingCost(weight, destination)   ← missing types
  ```

### Rule: Every property traces to a CRC responsibility

Every property in a domain-model block must be justified by a "Responsible for" line in the corresponding CRC class. Passing means each property answers the question *what must this class remember to fulfil that responsibility?* Failing means a property appears with no CRC backing, or a CRC responsibility that implies stored state has no matching property.

#### DO

- Derive each property from a specific "Responsible for" line and type it where the domain makes the type obvious.

  **Example (pass):**
  ```
  CRC — Responsible for: tracking the total price of the order

  Domain-model block:
  + totalPrice: Money
  ```

- Include at least one property for every CRC class that owns domain behavior.

  **Example (pass):** A CRC class with three "Responsible for" lines produces a domain-model block with three or more properties, each traceable to one of those lines.

#### DO NOT

- Add a property that has no corresponding CRC responsibility.

  **Example (fail):**
  ```
  CRC — (no mention of "color")

  Domain-model block:
  + color: String       ← invented, not sourced from CRC
  ```

- Leave a CRC class that holds state without any domain-model properties.

  **Example (fail):** A CRC class is "Responsible for: maintaining the remaining budget" but its domain-model block has zero properties — the stored state was never surfaced.

### Rule: A class is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not need an operation to receive it. Only the class that performs the action owns the operation. If a typed operation describes something happening *to* a class, find the acting class and place the operation there instead.

#### DO

- Place the operation on the class that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. `OngoingEffects` owns `+ resist(effect: PowerEffect, check: Check): void`. `PowerEffect` owns `+ resistanceTrait: Trait` (declaring how it is resisted) — not a `resist` operation.

  **Example (pass):** A condition is applied to a character. `ImposedConditions` owns `+ applyCondition(source: ConditionSource, condition: Condition): void`. `Character` does not own `+ receiveCondition(...)`.

#### DO NOT

- Give a class an operation that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):**
  ```
  PowerEffect
  + resist(check: Check): void   ← the effect does not resist itself; the character makes the check
  ```

  **Example (fail):**
  ```
  Character
  + receiveCondition(condition: Condition): void   ← Character does not receive; ImposedConditions applies
  ```

  **Example (fail):**
  ```
  Condition
  + imposeOn(character: Character): void   ← Condition doesn't impose itself; PowerEffect does through ImposedConditions
  ```

#### Clarification

A class *may* have a property that describes what is used to act upon it. This is not the same as an operation to be acted upon.

  **Example (pass):**
  ```
  PowerEffect
  + resistanceTrait: Trait   ← declares which trait a character uses to resist; the effect is not doing the resisting
  ```

**Source:** Engagement convention (object-model skill). Adapted from class-responsibility-collaborator/rules/receiver-not-responsible-for-receiving.md.

### Rule: Relationships have two named ends and cardinality

Every relationship in a domain-model block must name both ends and state cardinality (`1..1`, `0..1`, `1..*`, `0..*`). Direction must match the CRC collaborator that sourced it. Passing means both ends, cardinality, and direction are present and traceable. Failing means an end is unnamed, cardinality is missing, or the direction contradicts the CRC collaborator line.

#### DO

- State both class names, the relationship kind (composition or association), and cardinality on both ends.

  **Example (pass):**
  ```
  Order *composes* OrderLine  [1..1 → 1..*]
  ```

- Derive direction from the CRC collaborator entry — the class that lists the collaborator is the navigating end.

  **Example (pass):**
  ```
  CRC — Order collaborates with OrderLine
  → Order navigates to OrderLine, not the reverse
  ```

#### DO NOT

- Write a relationship with only one end named.

  **Example (fail):**
  ```
  *composes* OrderLine  [1..*]    ← owning end missing
  ```

- Omit cardinality entirely.

  **Example (fail):**
  ```
  Order *associates* Customer     ← no cardinality on either end
  ```

- Reverse the direction from what the CRC collaborator line states.

  **Example (fail):**
  ```
  CRC — Order collaborates with Customer
  Relationship written as: Customer *associates* Order  ← direction flipped
  ```

### Rule: State marker is domain-model

After this skill runs, the module file's YAML front matter must contain `state: domain-model`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: domain-model`.

  **Example (pass):**
  ```
  ---
  state: domain-model
  ---
  ```

#### DO NOT

- Leave the state at `crc` (the previous step).

  **Example (fail):**
  ```
  ---
  state: crc
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

### Rule: Subtypes use ClassName : ParentClass on the heading line

**Scanner:** Manual review

When a class is a specialization of another, its object-model heading must use `#### **ClassName : ParentClass**` notation. The block states only delta members — typed properties, operations, and invariants that the subtype adds or overrides beyond the parent. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate inherited members.

#### DO

- Use `#### **ClassName : ParentClass**` on the heading line for subtypes.

  **Example (pass):**
  ```
  #### **OpposedCheck : Check**

  + resolve(opposing: Check): CheckResult
      Invariant: both sides resolve as standard Checks; higher result wins
  ```

- State only delta members — typed properties and operations the subtype adds or overrides beyond the parent.

  **Example (pass):** Parent `Check` owns `+ resolve(): CheckResult`; subtype `OpposedCheck : Check` overrides it with the opposing-check signature and adds its own invariants. No parent members are repeated.

#### DO NOT

- Use the Ubiquitous Language English heading form in object-model headings.

  **Example (fail):** `#### **Opposed Check** *(is a type of Check)*` — use `: ParentClass` in the heading, not the sketch's English form.

- Use code-style syntax from the implementation language.

  **Example (fail):** `class OpposedCheck extends Check` or `OpposedCheck(Check)` — the domain model uses its own notation, not a language keyword.

- Repeat inherited members in the subtype block.

  **Example (fail):**
  ```
  #### **OpposedCheck : Check**

  + trait: Trait                      ← inherited from Check; do not repeat
  + dc: DifficultyClass               ← inherited from Check; do not repeat
  + resolve(opposing: Check): CheckResult
  ```

**Source:** Engagement convention (object-model skill). Adapted from class-responsibility-collaborator/rules/subtype-uses-child-parent.md.
<!-- execute_rules:bundle_rules:end -->
