# Domain model Markdown

The **domain model** is the project’s **authoritative description of domain structure**: the classes, responsibilities, relationships, and rules that mirror how the problem space actually behaves. You use it to keep **specification, scenarios, and diagrams aligned** so implementation choices stay traceable to domain truth, not to convenience or technology. The model must stay **domain-oriented** (behavior and language from the source material), **cohesive and honest** (clear boundaries, names that mean what they say), and shaped by **SOLID** and related OO discipline — **single responsibility**, **open/closed** and **Liskov**-safe generalizations where inheritance exists, **interface segregation** at boundaries, **dependency inversion** toward abstractions — plus **preferring composition over inheritance** unless generalization is real. It is not a dumping ground for services, frameworks, or UI; those belong outside this layer. 

**Implementation must reflect this model in running code** — same classes, responsibilities, and rules — **not a parallel story told only at analysis or design altitude** — including **crane analysis** and other **design-level abstractions** (logical-only layers, shelf diagrams, conceptual boxes) **that divorce the documented domain from real types and behavior in the repository.**

## One canonical model, two views - markdown and drawio diagram

The **domain model** is **one** primary Markdown file in the workspace (naming convention **`*-domain-model.md`**) and one class diagram (**`*-domain-model.drawio`**) that stay paired as **visual twins** — update Markdown first, then render or hand-sync the diagram (see **class-diagrams**, **using-diagram-cli**).

**Pipeline stages refine the same artifacts.** **Phases** iterate over **the same** `*-domain-model.md` and `*-domain-model.drawio`.

Use **`*[Sn · phase-id]*`** in class **Notes** (from **process.md**) to record *when* something was introduced or changed.

Structure templates: **`templates/domain model template.md`**, **`templates/domain model template.drawio`**.

---

## What goes in the domain model

- **Modules** — A **grouping of tightly related classes that collaborate around the same mechanism**. Each module has a name and a list of classes. Each module typically maps to one area (or page) of the class diagram.
- **Domain classes** — A **domain class holds state and can be operated on** (the modeling unit that becomes a class in OO code). Classes participate as callers, receivers, and collaborators in scenarios and collaborations. Each class has:
  - **Properties** — with types, optional collaborating classes and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter. **Type selection:** Use `Dictionary<K,V>` when items are accessed by key (name, type, id) — most “has many” relationships where you look up by name. Use `List<T>` only when order matters and items are accessed by position. Default to Dictionary for named domain collections.
  - **Operations** — with optional collaborating classes and invariants. Behaviors in scenarios should be traceable to operations on the domain model.
  - **Base class** (optional) — parent for inheritance. **Foundational** — tag `[foundational]` for classes that are the base types everything else extends from (the stable core).
- **Class relationships** — When a class “has” another: **composition** (strong has-a; part cannot exist without whole) or **aggregation** (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock). Prefer composition/aggregation over inheritance.
- **Examples** — At the end of each module, one table per class, shared scenario linking the module. Scenario column required; qualifier in parentheses after class name; columns match class properties.
- **Invariants** — Under the specific property or operation they apply to, not a separate section.

---

## Guidelines
- Prefer **composition/aggregation** over inheritance (composition = strong has-a; aggregation = weak has-a where the whole has no meaning without multiple instances of the same part).
- Avoid central "service/manager" concepts.
- Avoid tech details (APIs, services, databases, UI components). No speculation beyond the provided material. Everything at logical/domain level.

## **newly added**

During execution of a phase place **newly added** at end of line to mark a class, property, or operation that first appears in **that phase** of document creation — useful when showing how the **same** model file grows over time.

Remove **newly added** markers that were added during previous phases.

## Introducing typed members

During **Stage 1 scaffold** (for example from **`nouns-verbs-rules-and-states`** through **`thing-vs-data-about-a-thing`**), informal bullets for candidates, responsibilities, and collaborators are enough.

After you introduce **typed** members (typically from **`properties-methods-and-relationships`** onward), prefer **typed** members in the spec. Earlier passes may stay informal (bullets and prose) in the same file. 

### Typed Guidelines
- Write members in the formal style: `- <Type> propertyName` and `operationName(...) → ReturnType`.
- Use `Dictionary<K,V>` when items are accessed by key (name, type, id); use `List<T>` only when order/position matters (e.g. turn order, sequential steps). Default to Dictionary for named domain collections.
- Use `EnumType name along with a related EnumType Definition in the model` for constrained options — not `String` with parenthetical options.

---

## Subtype headings and invariant placement

When you introduce substitutable specializations, use an **explicit subtype heading** so the hierarchy is visible in the spec and on the diagram. Attach **invariants** to the **property or operation** they constrain, not in a separate inventory.
