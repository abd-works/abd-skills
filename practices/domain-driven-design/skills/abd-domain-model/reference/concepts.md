# Domain Model — Concepts

For OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes), read [`../../../reference/oo-concepts.md`](../../../reference/oo-concepts.md) in full before proceeding. The sections below cover what is specific to the domain model format.

## The class block format

Each concept gets one `### **ClassName**` block. The block has three zones separated by dashes:

```
### **ClassName**

ClassName(Type, Type)
------
propertyName: Type
	Invariant: declarative constraint
anotherProperty: Type
----
methodName(Type, Type): ReturnType
	CollaboratorType
	Invariant: declarative constraint
anotherMethod(Type): void
```

- **Constructor** — `ClassName(Type, Type)` on the first line. Types only, no parameter names. Include only what is needed to bootstrap a valid object. Omit the constructor line for classes with no constructor (factory, pre-defined instances); begin directly with `------`.
- **`------`** (six dashes) — separates constructor from properties.
- **Properties** — `propertyName: Type`. The name is a camelCase noun from domain vocabulary. The type is a domain type, constrained enum, or typed primitive — never raw `String`.
- **`----`** (four dashes) — separates properties from methods.
- **Methods** — `methodName(Type, Type): ReturnType`. Types only in the parameter list, no parameter names. Use `void` for commands with no return. Use `-` prefix for private methods only; no prefix for public methods.

## Types

Every type must be one of:

- **Domain type** — a class defined elsewhere in the model (`Stage`, `Ticket`, `SkillProgress`).
- **Constrained enum** — a named set of values documented in the decisions section (`DeliveryRole`, `ScopeLevel`, `ExecutionStatus`).
- **Typed primitive** — a named wrapper that communicates intent (`Timestamp`, `FilePath`, `Identifier`, `FreeText`, `PromptText`, `Message`, `SessionId`, `SkillName`).
- **Standard type** — `Boolean`, `Integer` when the domain meaning is self-evident.

Raw `String` is never acceptable. If a property or parameter is a string, determine what kind of string it is and name the type accordingly.

## Collaborators

When a method works with domain types that are not visible in its parameter list or return type, list those types underneath the method, indented, before any invariant:

```
advanceCompletedTickets(): void
	Stage, Ticket
	Invariant: for each ticket in done whose skills are all done — scatter or advance
```

This captures the domain model collaborator information that would otherwise be invisible in a typed signature. Only list types that are genuinely hidden — types already in the params or return are not repeated.

## Invariants

Write each invariant as a single tab-indented line directly under the property or method it constrains: `	Invariant: ...`. Keep it declarative — "must", "cannot", "only if". One line per constraint.

On methods, collaborator lines come first, then invariants.

## Subtypes

Subtypes use `### **ChildClass : ParentClass**` on the heading line. The block lists **only delta members** — properties, methods, and invariants that add to or override the parent. Inherited members are never repeated.

```
### **TeamMember : Agent**

TeamMember(DeliveryRole, WorkRole, AgentDefinition)
------
----
advanceTicketToInProgress(Ticket): BoardPosition
	SkillProgress
	Invariant: only triggers on the first skill start
```

## Value objects and state-carrier classes

When applying a concept to an entity requires state that is unique from the concept itself, introduce a separate **state-carrier class** — do not add that state to the concept or to the entity.

## Collection classes

When a concept owns multiple related objects **and** the collection has unique behavior beyond holding them — such as supersession logic, end-of-turn checks, or add/remove rules — introduce a named collection class that owns that behavior.

## What this format omits (compared to a full domain specification)

- **No `+` prefix** — visibility is not marked; `-` only for private methods.
- **No `<< stereotypes >>`** — no Entity, ValueObject, Service markers.
- **No `<< composition >>` or `<< aggregation >>`** — relationship flavor is omitted.
- **No `List<T>` or `Dictionary<K,V>`** — use the inner domain type only; cardinality is implicit.
- **No `Interaction:` blocks** — no pseudocode walkthroughs.
- **No class descriptions** — no intro paragraphs on individual classes.
- **No `Initialisation:` text** — omit constructor line if no constructor; begin with `------`.
- **No param names in methods** — `method(Type): ReturnType`, not `method(param: Type): ReturnType`.

---

## Code format — `<ka-slug>.<ext>`

Code is the source of truth at model fidelity too. One file per Key Abstraction, named after the KA (`customer.ts`, `cart.ts`, …). The **same file** later evolves to specification fidelity by adding markers and empty invariant/interaction methods in place — a new file is not created (D26).

### Emission target: abstract class

Emit **abstract classes** in the target language.

- TypeScript → `export abstract class KaName { … }`
- Python     → `class KaName(ABC): …`   (`from abc import ABC, abstractmethod`)
- Java       → `public abstract class KaName { … }`

Templates: [`../templates/domain-model.ts`](../templates/domain-model.ts), [`../templates/domain-model.py`](../templates/domain-model.py), [`../templates/domain-model.java`](../templates/domain-model.java).

### What model fidelity carries

Everything the type system can express:

- Constructor with typed parameters
- Properties: `camelCase` name, real type (domain type, constrained enum, typed primitive, or standard type). **No raw `String`.**
- Abstract operations: `camelCase` name, typed parameters, typed return type. `void` for commands.
- Subtypes via `extends` (TS/Java) or class-parent (Python) — **delta members only**.

### What model fidelity omits

Everything on the specification-fidelity list. If you find yourself reaching for any of these, you are drifting up — either commit to specification fidelity or move it out:

- `@stereotype`, `@initialisation`
- `@composition` / `@aggregation` / `@association`
- Empty `@invariant` / `@interaction` methods
- Phase grouping / region banners

### Collaborator hints

Legacy markdown model files carried a `Collaborator:` line under each method listing types that were neither in the params nor return. In code, this information is unnecessary — the operation's body (in concrete implementations) is where those collaborators appear via imports and method calls. At the abstract-class level, only include a `/** Collaborators: A, B, C */` doc comment when it materially aids reading — otherwise drop it.

---

See `../templates/` for the canonical file shape.
