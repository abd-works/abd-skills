---
name: object-model
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

Before proceeding, read [`common/oo-concepts.md`](../../common/oo-concepts.md) **carefully and in full**. The sections below cover what is specific to this level of fidelity: typed notation and relationship flavors.

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
- **Variable names must use domain language** — `roll`, `margin`, `throwingDistanceMeasure`, not `r`, `temp`, `measureA`. Trace the right name up the chain: CRC → domain sketch → ubiquitous language → source references.

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

## Build

1. **Assess the starting point.** If a CRC model exists in the file, use it as the primary input — it is the richest source. If not, work from domain knowledge, a domain sketch, or any available source describing the classes and their behavior.
2. **Identify classes.** From the CRC (if present) or from domain knowledge, list every class that needs a typed block, including subtypes and collection classes.
3. **Decompose responsibilities.** For each class, look at its responsibilities (from CRC "Responsible for" lines, behavior bullets, or domain knowledge). Ask: *does this require the class to hold something (→ property), do something (→ operation), or both?* Route each responsibility before writing anything.
4. **Write properties and operations.** For responsibilities routed to state, write `+ propertyName: Type`. For responsibilities routed to action, write `+ methodName(param: Type): ReturnType`. Group related members into clusters separated by `----`; place operations after the properties they act on within the same cluster.
5. **Determine object initialisation.** For each class, scan its properties and ask: *how does each value or reference arrive?* Choose constructor injection, internal initialisation, factory method, or factory object — see `### Object initialisation` above. Record the chosen approach as constructor signatures or factory operation signatures.
6. **Derive relationships.** For each class, identify its collaborators (from CRC collaborator columns if present, or from domain knowledge). Ask: *is the parent defined by its children (aggregation), does the child depend on the parent to exist (composition), or are both sides independent (association)?* Mark composition and aggregation with a stereotype on the property (`<< composition >>`, `<< aggregation >>`). Leave plain associations unannotated.
7. **Add invariant lines.** Identify lifecycle guards and always-true rules (from CRC `invariants:` fields if present, or from domain knowledge). Write each as a tab-indented `Invariant: ...` line directly under the member it constrains.
8. **Add interaction blocks.** For each operation, ask: does this have inherent complexity — multiple internal steps, coordinated collaborators, or branching behavior not captured by the signature and invariants? If yes, write a tab-indented `Interaction:` block tracing the step-chain. CRC collaborators not mapped to parameters are a useful signal. See `### Interactions` above.
9. **Handle inheritance.** For each subtype, use `ChildClass : ParentClass` on the heading line and write only delta members — see `### Inheritance` above. Mark each class with its stereotype (`<< Entity >>`, `<< ValueObject >>`, or other as appropriate) — see `### Entities and Value Objects` below.
10. **Format.** Use `----` to separate clusters within a class and `-----` to separate whole classes. Follow `templates/domain-model-scaffold.md` for placeholder shapes and heading conventions.
11. **Bump state.** Change the YAML front-matter from `state: crc` to `state: domain-model`.

## Templates

`templates/domain-model-scaffold.md`

## Validate

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
- Every variable name inside an `Interaction:` block uses domain language drawn from the ubiquitous language, domain sketch, or CRC. Generic placeholders (`measureA`, `result`, `temp`, single letters) are not acceptable. When the right name is unclear, trace up: CRC → domain sketch → ubiquitous language → source references.
- Walkthrough scenarios (if present) can still be stepped with the new typed names (spot-check at least one).
- The YAML front-matter reads `state: domain-model`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: No technical terms in member names

**Scanner:** Manual review

Property names and operation names must use domain language vocabulary. Technical implementation terms are forbidden.

#### DO NOT use these terms (or their variants) in member names:

- `flag` → use a domain phrase like `is ongoing`
- `boolean`, `bool` → use the domain state name
- `list`, `array`, `collection` → introduce a named collection class instead
- `type` as a bare noun → use a qualified domain noun
- `status` as a bare noun → qualify it: `active status`, `activation status`

#### DO

- Derive the noun or verb from the domain behavior that inspired the member.

  **Example (pass):** Behavior says "penalises a character according to a game modifier" → property is `+ gameModifier: Modifier`, not `+ modifier` or `+ penalty`.

  **Example (pass):** Behavior says "may be ongoing for a target character" → property is `+ isOngoing: Boolean`, not `+ ongoingFlag`.

### Rule: Domain vocabulary matches inspiring behavior

**Scanner:** Manual review

Each member name must use vocabulary recognisably tight to the domain behavior that inspired it. A reader who sees the member name should be able to connect it to the behavior without explanation.

#### DO

- Use the key noun or verb from the behavior description.

  **Example (pass):** Behavior: "carries imposed conditions" → property `+ imposedConditions: ImposedConditions`.

#### DO NOT

- Use a generic name that could apply to any class.

  **Example (fail):** Behavior says "enforces penalties only when active" but operation is named `+ apply(): void` — too vague.

- Rename a domain term to a technical synonym.

  **Example (fail):** Behavior says "imposing source" but property is named `+ originRef: Source`.

### Rule: Introduce a state-carrier class when application requires unique state

**Scanner:** Manual review

When applying a concept to an entity requires state that is unique per application — state that varies per entity or over time — introduce a separate state-carrier class. Do not add that state to the original concept or to the entity.

#### DO

- Introduce a state-carrier class when the applied state is distinct from the concept's definition.

  **Example (pass):** `Condition` holds its label, modifier, and supersession relationships. `ImposedCondition` holds active/inactive status, suppressing condition, and source — state unique to each application on a specific character.

#### DO NOT

- Add per-application state directly to the value object.

  **Example (fail):** Adding `+ activeStatus: Boolean` to `Condition` — this varies per character and per imposition, not per condition type.

### Rule: Introduce a collection class when the collection has unique behavior

**Scanner:** Manual review

When a class owns multiple related objects and managing that collection requires unique behavior — supersession logic, ordering, constraint enforcement — introduce a named collection class that owns that behavior.

#### DO

- Give the collection class the management operations and invariants.

  **Example (pass):** `ImposedConditions` owns `+ applyCondition(condition: Condition, source: Source): void` with supersession invariants. `Character` simply holds `+ imposedConditions: ImposedConditions`.

#### DO NOT

- Put collection management behavior directly on the owning entity.

  **Example (fail):** `Character` owns `+ applyCondition(...)` with all supersession logic — the character becomes bloated with condition-management concerns.

### Rule: A class is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not own a responsibility for receiving it. Only the actor that performs the action owns the operation. If behavior describes something happening *to* a class, find the acting class and place the operation there.

#### DO

- Place the operation on the class that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. `Character` owns `+ makeResistanceCheck(effect: PowerEffect): CheckResult`. `PowerEffect` owns `+ resistanceTrait: Trait` (declaring how it is resisted) — not a `resist()` operation.

#### DO NOT

- Give a class an operation that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):** `PowerEffect` has `+ resist(check: ResistanceCheck): void` — the effect does not resist itself.

### Rule: Explicit chain of responsibility — no nebulous behavior

**Scanner:** Manual review

When behavior implies a chain of actors or steps, every actor in that chain must be traceable to a typed property or operation with explicit relationships. Nothing may be left implied.

#### DO

- Trace each step in the chain to a named member with explicit parameters and collaborating types.

  **Example (pass):** Behavior: "may be ongoing — requires a resistance check at end of each target's turn."
  ```
  OngoingEffects
  + ongoingTargets: List<Character>
  + triggerResistanceChecks(turn: Turn): void
  	Invariant: check triggered at end of each ongoing target's turn
  ```

#### DO NOT

- Write a property that implies downstream action without naming the class that owns that action.

  **Example (fail):** `PowerEffect` has `+ isOngoing: Boolean` with no corresponding operation or class owning the end-of-turn check trigger.

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

- A class with only stateless responsibilities may have zero properties — that is valid. Only add a property when a responsibility requires the class to hold state.

  **Example (pass):** A CRC class with three verb-phrase responsibilities (all stateless operations) produces a domain-model block with zero properties and three operation signatures — correct.

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

### Rule: Relationships are marked on properties, not as separate lines

Composition and aggregation are marked with a stereotype directly on the property that holds the reference. Association is the default and needs no annotation. Explicit relationship lines (`*composes*`, `*aggregates*`, `*associates*`) are forbidden. Explicit cardinality notation (`[1..1 → 1..*]`) is forbidden — cardinality is implied by the property type (single type = 1..1; `List<T>` = one-to-many) or made explicit via an invariant.

#### DO

- Mark composition and aggregation with a stereotype on the property.

  **Example (pass):**
  ```
  + << composition >> stages: List<DifficultyStage>   ← child has no identity without parent
  + << aggregation >> helpers: List<Check>            ← parent groups children
  + linkedTrait: Trait                                ← plain association; no stereotype
  ```

- Use an invariant when a cardinality constraint needs to be stated explicitly.

  **Example (pass):**
  ```
  + << composition >> stages: List<DifficultyStage>
  	Invariant: at least one stage required
  ```

#### DO NOT

- Write a separate relationship line.

  **Example (fail):**
  ```
  Order *composes* OrderLine  [1..1 → 1..*]    ← separate line; forbidden
  ```

- Add a stereotype to a plain association.

  **Example (fail):**
  ```
  + << association >> customer: Customer    ← association is the default; no annotation needed
  ```

- Write explicit cardinality notation outside an invariant.

  **Example (fail):**
  ```
  + stages: List<DifficultyStage>  [1..*]    ← cardinality belongs in an Invariant: line, not inline
  ```

### Rule: Subtype blocks contain only delta members

A subtype class block must contain only what the subtype adds or overrides. Passing means no inherited properties, operations, or relationships are repeated in the subtype block. Failing means the subtype duplicates members already present on the parent.

#### DO

- Write only delta members — properties, operations, and relationships that are new or overridden.

  **Example (pass):**
  ```
  CreditCardPayment : Payment
  + authorizationCode: String
  + authorize(gateway: PaymentGateway): void
  ```

- Leave the subtype block empty of any member already on the base class.

#### DO NOT

- Repeat a parent property or operation in the subtype.

  **Example (fail):**
  ```
  CreditCardPayment : Payment
  + amount: Money              ← already on Payment
  + authorizationCode: String
  ```

### Rule: Every class has an object initialisation decision recorded

Every class block must show how its objects are initialised — at minimum one constructor signature, factory method signature, or an explicit note that initialisation is internal. Passing means the reader can tell how a valid instance is created. Failing means a class has properties and operations but no indication of how it is brought into existence.

#### DO

- Write at least one constructor or factory signature for every class.

  **Example (pass):**
  ```
  + Order(customer: Customer, items: List<OrderLine>)
  ```

- When initialisation is internal (composition owner creates it), note it explicitly.

  **Example (pass):**
  ```
  // initialised internally by Airplane
  ```

#### DO NOT

- Leave a class with properties but no initialisation entry.

  **Example (fail):** Class `Order` has `+ totalPrice: Money` and `+ status: OrderStatus` but no constructor or factory — the reader cannot tell how a valid `Order` is created.

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
<!-- execute_rules:bundle_rules:end -->
