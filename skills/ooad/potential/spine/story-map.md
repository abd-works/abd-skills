# Story map 

**Enduring reference for Story map** (`Epic, Story, Scenario, Steps`). 

A **story map** is a hierarchy of **interactions**. An **interaction** is a single meaningful exchange between two actors that results in either retrieval of state or a change of state.

## Purpose

The story map captures **who does what, in what order, under what conditions**. It is the user- and value-facing view: epics group capabilities, stories are the smallest independently deliverable, testable behaviors, and steps are atomic interactions. Every epic, story, scenario, and step is grounded in domain language via `**Concept`**; every such concept must exist in the domain model.

**Epics are important** (scope, actors, grouping) **but meaningless if they do not verify the domain** — an epic that does not **name and exercise** real `**concepts[]`** (same spelling as the domain model) and **evidence** is organizational noise, not design.

## What goes in the Story Map

**The interaction (unit):** Each node is an interaction with: **Name** (verb-noun or subject-qualifier); **Statement** (one-sentence summary; use `**Concept`** in the statement). **Pre-Condition** — label only; what must be true before the interaction; state qualifies through the label; use `**Concept`**. **Trigger** — **Triggering-Actor** and **Behavior** only (who starts and what they do); fold qualifying state into **Behavior** text and **Examples** tables—**no** separate Triggering-State field. **Response** — **Responding-Actor** and **Behavior** only (who responds and what they do); fold resulting state into **Behavior** text and **Examples** tables—**no** separate Resulting-State field. **Examples** — collection of tables at the interaction level; one per concept referenced in labels; Pre-Condition, Trigger, and Response reference these through their labels. **Failure-Modes** — up to three; how the exchange can fail (rule/state based only). **Constraints** — zero or more; qualitative instructions on how the interaction is shaped; may be a sentence, a file reference, or (commonly) a markdown file; constraints are inherited from parent to child. **Children** — child interactions.

**State** qualifies an interaction through its **label** — a description of the condition. The interaction's **Examples** (tables) live on the interaction; labels reference the domain concepts that correspond to those tables.

**Node hierarchy:**

- **Epic** — Can nest: epic children (sub-epics) or story children. Names typically verb-noun. **Statement:** describes the *scope* of the epic (broad flows it encompasses), not a single interaction.
- **Sub-Epic** — An epic whose parent is an epic; logical grouping of related stories; a feature area, not a behavior itself.
- **Story** — The **backbone** of the map. Smallest unit of testable value that is independently deliverable. Has a triggering actor, a responding actor, and produces observable state change; if it has no actor and no state change, it is not a story. **Statement:** one trigger and response. Everything below the story (scenarios, steps, examples) **belongs to the story**. Epic and sub-epic exist to **group stories**; they are organizational structure, not the primary unit of value.
- **Scenario** — Groups steps; optional container for a story. Names describe the primary conditions tested (e.g. success path, failure path). Split scenarios when pre-conditions differ, success vs failure paths, or different branches.
- **Step** — Atomic interaction within a scenario; one action by one actor. **Statement:** often When (Trigger) and Then (Response). Identify separate steps when: explicit action-reaction, actor or response changes, or when enumerating permutations (validation paths, branches, edge cases).

**Name and statement (all nodes):** Use active verb language. Short name first, longer statement in brackets. Format: `Node: Short Name (Longer statement.)` — e.g. `Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays list of **Country** options.)`

**Domain grounding:** Every epic, story, scenario, and step must be grounded in domain language. Use `**Concept`** in labels (name, statement, pre-condition, trigger, response). Avoid generic terms — use `**Country`**, `**PaymentType`**, not "country" or "payment type". Concepts are placed at the level where they apply to all descendants. Every `**Concept**` must exist in the domain model as `**concepts[].name**` with the **identical spelling** — **100% match**, **non-negotiable**. No drift, no synonyms in story text when the model has fixed a canonical name.

**Inheritance:** Child nodes inherit from parents (actors, pre-condition, examples, domain concepts, constraints). Use `[brackets]` for inherited values (e.g. `Triggering-Actor: [User]`, `Examples: [Logged In User, Active Session]`) so readers see what applies. Never use `Pre-Condition: [inherited]` alone — always include the label. Put shared concepts at epic level; story-specific concepts at story level.

---

# Why story mapping before domain types

This pipeline orders the **shaped story map** before **sparse domain types** (`concepts[]`).

**Reason:** If types land first, epics and stories get **pulled toward nouns that already exist in** `concepts[]`, and alignment rules reward **surface string match** between story text and type names. That **amplifies noun explosion** and confuses **documentation artifacts** with **stateful domain types**.

**Story-first** forces each slice of value to be stated as **actor → behavior → anchor** (what state is read, written, or queried). Types are then promoted only where the **story map and evidence** justify **distinct** behavioral contracts—not because a word appeared in a heading.

**Read vs write:** A story may be anchored on **observation** or **query** only; mutation is not required. That matches the **behavioral description of value** principle in `[principles.md](principles.md)`.

See also: `[principles.md](principles.md)` (principles; checkable rules in `rules/`), and `[shaped-story-map.md](shaped-story-map.md)` for the Phase 3 JSON shape and validators.



---

# Story Map Format

## Hierarchy

Each node is an interaction. Epic → Sub-Epic (or Epic) → Story → Scenario → Step. Epics can nest (epic children = sub-epics).


| Node     | Meaning                                                                                                                                                                                                                       | Heading                                    |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Epic     | Large domain capability — a major area of the system. Groups stories; statement = scope (broad flows), not a single interaction.                                                                                              | `# Epic: <name> (<statement>)`             |
| Sub-Epic | An epic whose parent is an epic; logical grouping of related stories — a feature area, not a behavior itself.                                                                                                                 | `## Epic: <name> (<statement>)`            |
| Story    | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. Statement = one trigger and response. | `### Story: <name> (<statement>)`          |
| Scenario | Condition-specific grouping of steps within a story (e.g. success path, failure path). Names describe conditions tested.                                                                                                      | `#### Scenario: <name>`                    |
| Step     | Atomic interaction — one action by one actor. When/Then: Trigger as When, Response as Then.                                                                                                                                   | `- Step N: <name> (When/Then <statement>)` |


## Per Interaction

- **Pre-Condition** — label only; what must be true before. Use Given/And for steps. State qualifies through the label; use `**Concept`**. Examples live on the interaction.
- **Trigger** — **Triggering-Actor** (who starts) and **Behavior** (what they do). Use When/And on **steps** when you need multiple beats; domain concepts belong in **Behavior** or **Examples** tables, not a third “state” sub-field.
- **Response** — **Responding-Actor** (who responds) and **Behavior** (what they do). Use Then/And on **steps** when needed; same rule for concepts and tables.
- **Examples** — tables at the interaction level; one per concept referenced in labels. Pre-Condition, Trigger, and Response reference these through their labels.
- **Failure-Modes** — bullet list, max 3; rule/state based only (no infrastructure failures).
- **Constraints** — zero or more; qualitative instructions; sentence, file ref, or markdown ref; inherited from parent to child.
- **Domain concepts** — Use `**Concept`** in labels; every concept must exist in the domain model.

### Step format

- **When/Then** — Trigger as When, Response as Then (e.g. `When **User** browses countries; Then **System** displays list of **Country** options`).
- **Vanilla steps** — verb-noun short labels (e.g. `User submits form`, `System validates payment`).

Strategy or scope specifies which format applies.

### Commonly Generated Fields Per Node


| Node     | Commonly Generated                                              | Case-by-Case                     |
| -------- | --------------------------------------------------------------- | -------------------------------- |
| Epic     | Triggering-Actor, Responding-Actor, Name, Pre-Condition         | Constraints                      |
| Story    | Trigger, Response, Name, Examples, Pre-Condition, Failure-Modes | Constraints                      |
| Scenario | Trigger, Response, Pre-Condition, Examples                      |                                  |
| Step     | Trigger, Response, Examples                                     | Constraints (when step-specific) |


## Domain Grounding

Use `**Concept`** in labels (name, statement, pre-condition, trigger, response). Place concepts at the level where they apply to all descendants. Avoid generic terms — use `**Country`**, `**PaymentType`**, not "country" or "payment type". Every concept must exist in the domain model; **spelling must match `concepts[].name` exactly (100%)** — **non-negotiable** (rule **scaffold-concept-story-name-alignment** at scaffold). No drift.

**Scaffold JSON (`confirming_stories[]` on an epic):** Include **as many** story **names** as you need so foundational concepts for that epic are exercised — there is **no** “stop at two” rule; two was never a ceiling, only a bad habit.

## Inheritance

Attributes from a parent node are inherited by child nodes. Use **brackets** for inherited values so readers see what applies: `Triggering-Actor: [User]`, `Responding-Actor: [System]`, `Examples: [Logged In User, Active Session]`. Unbracketed values are defined on the node. If the parent changes, update bracketed values in children.

**Commonly inherited:**

- **Story from Epic:** Triggering-Actor, Responding-Actor, Pre-Condition, Examples (by name), domain concepts.
- **Scenario from Story:** Often nothing needs to be stated explicitly (inherited applies).
- **Step from Story:** Triggering-Actor, Responding-Actor (e.g. [User], [System]). Exception: when a step is system-triggered, that step may override Triggering-Actor.

**Rule:** Put shared concepts at the epic level; add story-specific concepts only at the story level. Only put something at a level if it applies to every descendant.

## Examples

Tables **live on the interaction**. One table per concept referenced in Pre-Condition, Trigger, or Response labels. Tables should align with examples in the domain model (same scenario prefix, same columns where applicable).

**Naming:** Name tables by state or condition — "Selected Country", "Approved Payment", "User Payment Type Access" — not generic labels like "Payment" or "Country". When multiple tables for the same concept appear in one step, add a qualifier in parentheses (e.g. `Selected PaymentType (selected, not available for country)`). When inherited, list those names: `Examples: [Logged In User, Active Session, User Payment Type Access]`.

```
ConceptName (qualifier):
| scenario | field1 | field2 |
|----------|--------|--------|
| success  | val1   | val2   |

===
AnotherConcept (qualifier):
| scenario | field1 |
|----------|--------|
| success  | val1   |
```

- **Scenario column** required; use kebab-case (e.g. `success`, `invalid-payment-details`, `payment-type-not-available`)
- **Separator:** `===` between tables; no blank lines between tables
- **Header:** Tables require a header separator row (`|---|---|`)
- **Inherited:** `Examples: [Table Name 1, Table Name 2]`

---

## Example 1: Interaction tree (payment by country)

Epic → story → scenario → steps, with **Examples** tables on the story. Illustrative only; every **Concept** must exist in the domain model with matching spelling. Sub-epics omitted—add nested `## Epic: …` under the top epic when you need another grouping layer before stories.

**Phase 3 JSON** uses the same pairing: `**trigger`** / `**response**` objects with `**actor**` and `**behavior**` only — see `[shaped-story-map.md](shaped-story-map.md)`.

```
# Epic: Pay by country (Customer completes payment using **Country**-specific **PaymentType** rules.)

Triggering-Actor: **User**
Responding-Actor: **System**
Pre-Condition: Authenticated Session
Examples: [Logged In User, Active Session]

### Story: Submit payment (When **User** submits **PaymentDetails**; Then **System** accepts or rejects the payment.)

Pre-Condition: Selected **Country** and **PaymentType**

Trigger:
  - Triggering-Actor: **User**
  - Behavior: Select **Country** and **PaymentType** for payment, then submit

Response:
  - Responding-Actor: **System**
  - Behavior: Validate, accept, and update **PaymentDetails**

Failure-Modes: **PaymentType** not available for **Country**; **PaymentDetails** amount fails validation threshold

#### Scenario: Success path

- Step 1: Select country for payment (When **User** browses **Country** list; Then **System** displays **Country** options.)
- Step 2: Submit payment (When **User** submits **PaymentDetails**; Then **System** records accepted **PaymentDetails**.)

Selected Country:
| scenario    | country_code | country_name  |
|-------------|--------------|---------------|
| pay-us-wire | US           | United States |

===
Available PaymentType for country:
| scenario    | payment_type | available |
|-------------|--------------|-----------|
| pay-us-wire | wire         | true      |
```

---

## Validation Checklist

**Epic**

- Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- Pre-Condition on parent only when shared; children list only new or specialized state

**Story**

- Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- Trigger: **Triggering-Actor** and **Behavior** only (reference **Concept** in behavior text or **Examples**)
- Response: **Responding-Actor** and **Behavior** only (same)

**Step**

- `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- Trigger and Response with [inherited] when from parent

**Example tables**

- Tables live on the interaction; one per concept referenced in labels
- Names by state/condition (e.g. Selected Country, Approved Payment); qualifier in parentheses when needed
- Scenario column required; kebab-case
- Each table: label, header row, separator row, data rows; `===` between tables

**Hierarchy**

- Epic → Epic/Story → Scenario → Step
- Each node touches at least one domain concept via `**Concept`**

