# Object Model — Concepts

For OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes), read [`../../../reference/oo-concepts.md`](../../../reference/oo-concepts.md) in full before proceeding. The sections below cover what is specific to object-model fidelity: typed notation and relationship flavors.

## Properties

Write each property as `+ propertyName: Type`. Type it where the domain makes the type obvious (`String`, `Boolean`, `Money`, `List<Item>`, etc.); leave it untyped only when the domain is genuinely ambiguous. Typed constants and enum-like value sets (`UPPER_CASE` names) are grouped under a named constant block.

## Operations

Write each operation as `+ methodName(param: Type): ReturnType`. Parameters come from the information the method needs but does not already hold as a property; the return type reflects what the caller expects back. Keep signatures at the domain level: no infrastructure, no UI, no framework types. Omit the return type only when the operation is genuinely void.

Use `+` for public operations that external collaborators call. Use `-` for private helpers that are only called internally by the class itself — extracted sub-logic, tie-breakers, guard checks, etc.

**When the right name is unclear, name it after the invariant.** If an operation's invariant says "incoming supersedes existing", the operation is `incomingSupersedes`. The invariant is already the correct domain statement — the name should match it directly rather than inventing a separate label.

## Object initialisation

For every class, determine how its objects are initialised. Choose from the following approaches based on scenario and context:

**Constructor injection** — pass a dependency in when the class references but does not own it (association), or when a required value must be present for the object to be valid. Write as `+ ClassName(param: Type, ...)`. Include only what is needed to bootstrap a fully valid object; never leave an object half-initialised. Write multiple constructors when different valid bootstrap configurations exist in the domain.

**Internal initialisation** — create or derive it inside the class when the class owns the thing (composition) or when the value is derived from properties the object already holds. The caller should not be responsible for assembling parts the class owns.

**Factory method** — use a static factory *on the class itself* when construction is complex, can fail gracefully, or needs to return different subtypes based on input. The factory method replaces `new` for callers — it is a named static operation on the class.

**Factory object** — delegate construction entirely to a separate domain object when the assembly logic is itself a domain concern, when multiple unrelated callers need the same complex build, or when the assembled object requires coordinating many collaborators the caller should not know about.

## Relationships

The three questions in `oo-concepts.md` (`## Relationships`) determine the dependency nature. At this level of fidelity, each answer maps to a named type of relationship:

- **Aggregation** — the parent exists to collect or group its children; the parent has no identity without them.
- **Composition** — the child has no identity without the parent; the parent owns the child's lifecycle.
- **Association** — both sides have independent lifecycles.

**Association is the default** — no annotation needed. Mark composition and aggregation directly on the property with a stereotype; no separate relationship line is required.

```
+ << composition >> stages: List<DifficultyStage>   ← ownership is on the property
+ linkedTrait: Trait                                 ← plain association; no stereotype
```

The property type already implies cardinality direction: a single type is 1..1; `List<T>` or `Dictionary<K,T>` is one-to-many. Use an invariant on the property when the cardinality constraint needs to be made explicit.

## Collections

When a class holds multiple instances of another class, type the property using one of two generic forms:

- **`List<ClassName>`** — an ordered or unordered set where you iterate or process all members. No key needed.
- **`Dictionary<KeyType, ClassName>`** — a keyed set where you need to look up a specific member directly.

The name of the property should reflect the domain collection concept, not the data structure — `appliedConditions`, not `conditionList`. When the collection itself has unique behavior, introduce a named collection class.

## Inheritance

Use `ChildClass : ParentClass` on the class heading. The child block contains only delta members — typed properties, operations, and relationships that add or override the parent. Inherited members are never repeated.

Mark each class with its stereotype on the heading — see `### Entities and Value Objects` below.

## Invariants

Write each invariant as a single tab-indented line directly under the property or operation it constrains: `	Invariant: ...`. Keep it declarative — "must", "cannot", "only if". One line per constraint.

## Interactions

When an operation has inherent complexity or interesting interactions — it coordinates multiple collaborators, produces a result through a chain of internal steps, or branches in a way not captured by the signature and invariants alone — write a tab-indented `Interaction:` block directly after the operation's invariants. Each step is a flat, non-nested pseudocode line using the scenario-walkthrough notation.

**When to omit:** Simple delegations with a single step, pure queries that return a property directly, or operations whose entire behavior is self-evident from the return type and invariants alone.

**Design smell — invariants without interactions:** If an operation carries several invariants but no `Interaction:` block, that is almost always wrong. Invariants state *what must be true*; they cannot replace the step-chain that *makes it true*.

**Extract complex sub-logic into named operations.** An `Interaction:` block is not pseudocode — it traces the key collaborations. When a branch or calculation is non-trivial, give it a name, extract it as a separate operation, and describe its rule as an invariant.

**Format rules:**
- `	Interaction:` is tab-indented under the operation, same level as `Invariant:`
- Each step inside is a further-indented flat line — **no nesting**
- Use typed pseudocode: `variableName: Type = expression`
- Method calls: `object.method(param: value)`
- Construction: `variable: Type = new ClassName(param: Type)`
- Return: `return variable`
- **Variable names must use domain language** — `roll`, `margin`, `throwingDistanceMeasure`, not `r`, `temp`, `measureA`. Trace the right name up the chain: CRC → Ubiquitous Language → source references.

## Entities and Value Objects

Domain objects carry one of several stereotypes depending on their role. The two most common are Entity and Value Object.

**Entity** — an object distinguished by identity, not by its attributes. Two entities with identical attributes are still different things. An entity has a continuous lifecycle: it is created, changes over time, and eventually ends. Mark with `<< Entity >>`.

**Value Object** — an object defined entirely by its attributes, with no meaningful identity of its own. Two value objects with the same attributes are interchangeable. Value objects are immutable: never modify one in place; replace it with a new instance. Mark with `<< ValueObject >>`.

**The deciding question:** *Does this thing need to be tracked as an individual over time, or does only the combination of its values matter?*

Other stereotypes exist (`<< Service >>`, `<< Factory >>`, `<< Repository >>`, `<< Domain Event >>`, boundary types, etc.) and are applied when the class clearly plays that role.

---

## Consistent shape

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
