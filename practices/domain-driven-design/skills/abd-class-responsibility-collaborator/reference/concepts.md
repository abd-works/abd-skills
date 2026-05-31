# Class Responsibility Collaborator — Concepts

For OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes), read [`../../../reference/oo-concepts.md`](../../../reference/oo-concepts.md) in full before proceeding. The sections below cover only what is specific to the CRC format.

## The CRC block format

Each concept gets one `#### **ConceptName**` block. Responsibilities are listed as rows in a two-column table separated by `|`: the left column names the responsibility, the right column names collaborators.

```markdown
#### **ConceptName**
responsibility name         | Collaborator, Another Collaborator
another responsibility      | Collaborator
                            |   invariant: declarative constraint that must always hold
```

- **Left column** — the responsibility name. Use a **noun phrase** for state (something the concept holds or carries) and a **verb phrase** for behaviour (something the concept does). Use domain language vocabulary from the behavior bullet that inspired it — not bare nouns, not technical terms.
- **Right column** — comma-separated collaborator class names, or a value description in parentheses for primitive/enum values.
- **Invariants** — indented continuation rows `|   invariant:` under the responsibility they constrain.
- **`|` separators** — align consistently within each block.

## Subtypes

Subtypes use `#### **ConceptName : BaseConcept**` on the heading line. The block lists **only delta responsibilities** — what the subtype adds or overrides. Inherited responsibilities are not repeated — see `## Inheritance and subtypes` in `oo-concepts.md` for the delta rule.

```markdown
#### **ConceptName : BaseConcept**
added responsibility        | Collaborator
                            |   invariant: constraint specific to this subtype
```

## Value objects and state-carrier classes

When applying a concept to an entity requires state that is unique from the concept itself, introduce a separate **state-carrier class** — do not add that state to the concept or to the entity.

- **`Condition`** is a value object: its values are *dazed*, *stunned*, etc. It holds the label, modifier, and supersession relationships that are the same for every character.
- **`Imposed Condition`** is a state-carrier class: it manages the state required to impose a condition on a specific character — active/inactive status, suppressing condition, source. That state does not belong on `Condition` and should not be held on `Character`.

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance of `Condition`). Never use *instance* as a synonym for a separate state-carrier class.

## Collection classes

When a concept owns multiple related objects **and** the collection has unique behavior beyond holding them — such as supersession logic, end-of-turn checks, or add/remove rules — introduce a named collection class that owns that behavior.

```markdown
#### **Imposed Conditions**
applied conditions          | Imposed Condition
apply new condition         | Condition Source, Condition, Imposed Condition
                            |   invariant: same-source more-severe — remove lesser
                            |   invariant: different-source more-severe — park lesser as inactive
```

## Collaborators

Collaborators are the other domain classes a concept works with to fulfil a responsibility — the CRC-level record of the relationships described in `oo-concepts.md` (`## Relationships`). List every class that participates in making the responsibility work. Do not leave implied actors unnamed — if a behavior implies a chain of actors, every actor must appear as a collaborator on some responsibility.

A concept is **not** responsible for receiving an action directed at it. The receiver of an operation does not need a responsibility to be acted upon. The actor that performs the action owns the responsibility.

## Invariants

An **invariant** is a short declarative constraint — phrased as a statement of what must always be true — placed inline under the responsibility it constrains using `|   invariant:`. Invariants are not procedures; they describe constraints, not steps.

---

## Consistent shape

```
## **{{KAName}}**

[Optional 1–2 sentence intro]

### **{{ka_name as a Class}}**             ← MUST appear first; matches the KA
property name              | Collaborator
operation name             | Collaborator
                           |   invariant: rule that must always hold

### **{{another Class}}**
property name              | Collaborator
operation name             | Collaborator, Collaborator

### **{{SubtypeName}} : {{BaseClass}}**
delta responsibility       | Collaborator

### references                              ← one per KA, peer to classes
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made                          ← one per KA, peer to classes
- decision rationale
```

The Boundary Domain is one flat section — all boundary classes share a single `# Boundary Domain` group with one `### references` and one `### decisions made` at the bottom.
