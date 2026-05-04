---
name: class-responsibility-collaborator
description: >-
  For every domain concept: assign responsibilities, name collaborators,
  and declare invariants — all in one structured pass before object-model.
---
# class-responsibility-collaborator

## Purpose

This skill takes domain concepts from a completed domain sketch and produces a structured CRC model: for each concept, what it is responsible for, who it collaborates with, and what must always remain true. The result is a module file with `### Class Responsibility Collaborator` sections appended after the existing domain sketch content.

**CRC (Class-Responsibility-Collaborator)** modeling, introduced by Ward Cunningham and Kent Beck, is a lightweight way to explore object-oriented designs. This skill extends the classic technique by requiring explicit property and operation names, inline invariants, and subtype deltas — so the team can reason about ownership and boundaries before writing code.

---

## When to use this skill

- You have a completed domain sketch with behavior bullets but ownership, boundaries, and invariants are not yet explicit.
- The user asks to "run CRC," "assign responsibilities," or "build the CRC."
- The domain has sufficient complexity that explicit responsibility boundaries and always-true constraints are worth modeling.

---

## Core concepts

For OO fundamentals, read [`common/oo-concepts.md`](../../common/oo-concepts.md) in full before proceeding. The sections below cover only what is specific to the CRC format.

### The CRC block format

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

### Subtypes

Subtypes use `#### **ConceptName : BaseConcept**` on the heading line. The block lists **only delta responsibilities** — what the subtype adds or overrides. Inherited responsibilities are not repeated — see `## Inheritance and subtypes` in `oo-concepts.md` for the delta rule.

```markdown
#### **ConceptName : BaseConcept**
added responsibility        | Collaborator
                            |   invariant: constraint specific to this subtype
```

### Value objects and state-carrier classes

When applying a concept to an entity requires state that is unique from the concept itself, introduce a separate **state-carrier class** — do not add that state to the concept or to the entity.

- **`Condition`** is a value object: its values are *dazed*, *stunned*, etc. It holds the label, modifier, and supersession relationships that are the same for every character.
- **`Imposed Condition`** is a state-carrier class: it manages the state required to impose a condition on a specific character — active/inactive status, suppressing condition, source. That state does not belong on `Condition` and should not be held on `Character`.

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance of `Condition`). Never use *instance* as a synonym for a separate state-carrier class.

### Collection classes

When a concept owns multiple related objects **and** the collection has unique behavior beyond holding them — such as supersession logic, end-of-turn checks, or add/remove rules — introduce a named collection class that owns that behavior.

```markdown
#### **Imposed Conditions**
applied conditions          | Imposed Condition
apply new condition         | Condition Source, Condition, Imposed Condition
                            |   invariant: same-source more-severe — remove lesser
                            |   invariant: different-source more-severe — park lesser as inactive
```

### Collaborators

Collaborators are the other domain classes a concept works with to fulfil a responsibility — the CRC-level record of the relationships described in `oo-concepts.md` (`## Relationships`). List every class that participates in making the responsibility work. Do not leave implied actors unnamed — if a behavior implies a chain of actors, every actor must appear as a collaborator on some responsibility.

A concept is **not** responsible for receiving an action directed at it. The receiver of an operation does not need a responsibility to be acted upon. The actor that performs the action owns the responsibility. Example: a `Power Effect` does not resist itself — a `Character` (via its traits) makes the resistance check. The effect may declare *what* is used to resist it (`resistance trait`), but it does not own the act of resisting.

### Invariants

An **invariant** is a short declarative constraint — phrased as a statement of what must always be true — placed inline under the responsibility it constrains using `|   invariant:`. Invariants are not procedures; they describe constraints, not steps.

---

## The shape of a module file

Each knowledge area in the module file follows this structure:

```markdown
## **Knowledge Area Name**

<intro paragraph>

### Ubiquitous Language

#### **ConceptName**
- term definition

---

### Domain Sketch

#### **ConceptName**
- behavior bullet

---

### Class Responsibility Collaborator

#### **ConceptName**
responsibility              | Collaborator

#### **ConceptName : BaseConcept**
delta responsibility        | Collaborator

---

### Decisions made

- decision rationale

### References

**Ref: ...**
```

The Boundary Domain is one flat section — all boundary concepts share a single `### Ubiquitous Language`, `### Domain Sketch`, and `### Class Responsibility Collaborator` rather than being split into per-concept `##` sections.

---

## Build

1. **Read the domain sketch.** Every behavior bullet is a candidate responsibility. Each `#### **ConceptName**` block seeds one CRC block.
2. **Resolve slash terms.** Any concept named `A / B` in the domain sketch must be resolved to one canonical name before writing CRC blocks.
3. **Identify state-carrier needs.** For each concept, ask: does applying this concept to an entity require state unique from the concept? If yes, introduce a state-carrier class.
4. **Identify collection class needs.** For each entity that holds multiple related objects, ask: does managing that collection require unique behavior? If yes, introduce a collection class.
5. **Write CRC blocks.** For each concept — including state-carriers and collection classes — produce a `#### **ConceptName**` block using the table format. Subtypes use `#### **ConceptName : BaseConcept**` and carry only deltas.
6. **Trace every behavior to a responsibility.** Each behavior bullet in the domain sketch must be traceable to at least one responsibility (property or operation) in the CRC. If a bullet is missing coverage, add the responsibility or note the gap in Decisions.
7. **Verify explicit chains.** For every responsibility that implies multiple actors or steps, confirm that every implied actor appears as a collaborator on some responsibility in the CRC. Nothing nebulous.
8. **Append the CRC section.** Add `### Class Responsibility Collaborator` after `### Domain Sketch` within each knowledge-area section. Do not replace or modify prior content.
9. **Bump state.** Update front matter `state:` to `crc`.

---

## Validate

1. **Coverage.** Every concept from the domain sketch has a CRC block.
2. **No slash terms.** No `A / B` names appear in any CRC heading or block.
3. **Property names.** Every property name is a noun phrase using domain vocabulary — no technical terms (`flag`, `boolean`, `list`, `type` as a bare noun).
4. **Operation names.** Every operation name is a verb phrase.
5. **Vocabulary tight.** Each responsibility name uses vocabulary from the behavior bullet that inspired it.
6. **Subtype deltas only.** Subtype blocks contain only responsibilities that add or override the parent.
7. **Collaborators explicit.** No responsibility with implied actors has an empty or vague collaborator column.
8. **Receiver not responsible.** No concept has a responsibility that amounts to "receive X" or "be acted upon by X."
9. **Invariants indented.** Invariant lines use `|   invariant:` with three spaces after the pipe.
10. **`|` separators aligned.** Column separators are aligned within each block.
11. **State marker.** Front matter reads `state: crc`.
12. **Additive.** All prior content is unchanged — CRC is appended, not substituted.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Collaborators trace to sketch collaborations and subtype edges

**Scanner:** Manual review

The collaborator column in each CRC block must list domain concepts that appear in the domain sketch's behavior bullets or subtype edges for that concept. No collaborator may be invented. An empty collaborator column must contain a value description in parentheses (for primitives/enums) or be explicitly empty only when the responsibility truly has no collaborating concept.

#### DO

- List collaborators that correspond to concepts named in the behavior bullet.

  **Example (pass):** Sketch says "supersedes a less severe condition from the same source"; CRC has `supersede | Condition`.

- Use a parenthetical value description for primitive/enum collaborators.

  **Example (pass):** `active status | (active or inactive)`

#### DO NOT

- Invent collaborators that have no basis in the domain sketch.

  **Example (fail):** CRC block lists `Logger, EventBus` but neither concept appears anywhere in the sketch.

- Leave the collaborator column blank without explanation.

  **Example (fail):** `supersede |` with nothing on the right.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: No technical terms in responsibility names

**Scanner:** Manual review

Responsibility names — both property names and operation names — must use domain language vocabulary. Technical implementation terms are forbidden.

#### DO NOT use these terms (or their variants) in responsibility names:

- `flag` → use a domain phrase like `is ongoing`
- `boolean`, `bool` → use the domain state name
- `list`, `array`, `collection` → introduce a named collection class instead
- `type` as a bare noun → use a qualified domain noun
- `status` as a bare noun → qualify it: `active status`, `activation status`
- `own` as a prefix → use descriptive qualifiers from behavior language

#### DO

- Derive the noun or verb from the behavior bullet that inspired the responsibility.

  **Example (pass):** Behavior says "penalizes a suffering character according to a game modifier" → property is `game modifier`, not `modifier` or `penalty`.

  **Example (pass):** Behavior says "may be ongoing for a target character" → property is `is ongoing`, not `ongoing flag`.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Responsibility vocabulary matches inspiring behavior

**Scanner:** Manual review (grammar/vocabulary spot-check)

Each responsibility name must use vocabulary that is tight to the domain sketch behavior bullet that inspired it. The match need not be word-for-word, but the domain terms should be recognizable. A reader who sees the responsibility name and the behavior bullet should be able to connect them without explanation.

#### DO

- Use the key noun or verb from the behavior bullet.

  **Example (pass):** Behavior: "carries *imposed conditions* via its *Imposed Conditions* collection" → responsibility: `imposed conditions | Imposed Conditions`.

  **Example (pass):** Behavior: "is removed when its *condition source* ends" → operation: `end | Imposed Conditions`.

#### DO NOT

- Use a generic name that could apply to any concept.

  **Example (fail):** Behavior says "enforces penalties and restrictions only when active" but responsibility is named `apply` — too vague.

- Rename a domain term to a technical synonym.

  **Example (fail):** Behavior says "imposing source" but responsibility is named `origin` or `source ref`.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Introduce a state-carrier class when application requires unique state

**Scanner:** Manual review

When applying a concept to an entity requires state that is unique from the concept itself — state that varies per application, per entity, or over time — introduce a separate state-carrier class. Do not add that state to the original concept or to the entity.

#### DO

- Introduce a state-carrier class when the applied state is distinct from the concept's definition.

  **Example (pass):** `Condition` holds its label, modifier, and supersession relationships. `Imposed Condition` holds the active/inactive status, suppressing condition, and source — state that is unique to each application on a specific character.

- Name the state-carrier after its role in the application: `Imposed Condition`, not `ConditionInstance` or `AppliedCondition`.

#### DO NOT

- Add per-application state to the value object concept.

  **Example (fail):** Adding `active status` and `suppressing condition` directly to `Condition` — these vary per character and per imposition, not per condition type.

- Add per-concept state to the entity that holds it.

  **Example (fail):** Adding `active status` directly to `Character` — the character may carry many conditions, each with its own status.

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance/value of `Condition`). Never use *instance* as a synonym for a state-carrier class.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Introduce a collection class when the collection has unique behavior

**Scanner:** Manual review

When an entity owns multiple related objects and managing that collection requires unique behavior beyond simple holding — such as supersession logic, sequential processing, or constraint enforcement — introduce a named collection class that owns that behavior.

#### DO

- Introduce a collection class and give it the management responsibilities.

  **Example (pass):** `Imposed Conditions` owns `apply new condition` with supersession invariants. `Character` simply holds `imposed conditions | Imposed Conditions`.

#### DO NOT

- Put collection management behavior directly on the entity.

  **Example (fail):** `Character` owns `apply new condition` with all supersession logic — the character class becomes bloated with condition-management concerns.

- Leave collection management implied without a named owner.

  **Example (fail):** Writing "character tracks ongoing effects" in the domain sketch with no named class to own the tracking.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Every domain sketch behavior has a backing responsibility

**Scanner:** Manual review

Each behavior bullet in the domain sketch must be traceable to at least one responsibility (property or operation) in the CRC block for the same concept. Behaviors that produce no CRC entry must be explained in the Decisions section.

#### DO

- For every behavior bullet, produce at least one property or operation.

  **Example (pass):** Sketch: "makes checks using its traits" → CRC has `traits | Trait`.

  **Example (pass):** Sketch: "carries imposed conditions" → CRC has `imposed conditions | Imposed Conditions`.

#### DO NOT

- Leave a behavior bullet with no corresponding CRC entry and no decision note.

  **Example (fail):** Sketch says "has a difficulty ladder" but no property for it appears in the CRC block.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: A concept is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not need a responsibility to receive it. Only the actor that performs the action owns the responsibility. If a behavior describes something happening *to* a concept, look for the acting concept and place the responsibility there.

#### DO

- Place the responsibility on the concept that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. The `Character` (via `Ongoing Effects`) owns `make resistance check for ongoing targets`. The `Power Effect` owns `resistance trait` (declaring how it is resisted) — not a `resist` operation.

#### DO NOT

- Give a concept a responsibility that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):** `Power Effect` has `resist | Resistance Check` — the effect does not resist itself.

  **Example (fail):** `Character` has `receive condition | Condition` — the character does not receive; the `Imposed Conditions` collection applies it.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Explicit chain of responsibility — no nebulous behaviors

**Scanner:** Manual review

When a behavior implies a chain of actors or steps, every actor in that chain must be traceable to a property or operation with explicit collaborators in the CRC. Nothing may be left implied or nebulous.

#### DO

- Trace each step in the chain to a named responsibility with collaborators.

  **Example (pass):** Behavior: "may be ongoing for a target character: requires a resistance check at the end of each of the target's turns until ended."
  CRC produces:
  ```
  ongoing targets             | Character
  make resistance check       | Character, Check
                              |   invariant: check made at end of each ongoing target's turn
  ```

#### DO NOT

- Write a property and leave the downstream action it implies without an owner.

  **Example (fail):** CRC has `is ongoing | (active or ended)` with no corresponding operation for who tracks ongoing targets or who triggers the end-of-turn check.

- Leave "may" or "requires" language in a behavior without modeling the full chain.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Slash terms resolved before CRC

**Scanner:** Manual review

Any concept named `A / B` in the domain sketch must be resolved to one canonical name before writing CRC blocks. Slash terms are acceptable in domain sketch headers as working hedges, but must not appear in CRC headings or responsibility names.

#### DO

- Choose one name and use it consistently throughout the CRC section.

  **Example (pass):** Domain sketch has `#### **Check Result / Graded Check Result**` → CRC uses `#### **Check Result**` throughout.

#### DO NOT

- Use slash notation in any CRC heading or block.

  **Example (fail):** `#### **Check Result / Graded Check Result**` appears in the CRC section.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: English prose only — no method signatures or typed notation

**Scanner:** Manual review

Responsibility names, collaborator names, and invariants must be written in plain domain language. No method signatures, typed parameters, return types, UML notation, or code-level constructs are permitted.

#### DO

- Write responsibility names as noun or verb phrases.

  **Example (pass):** `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result`

- Write invariants as declarative English statements.

  **Example (pass):** `|   invariant: only active conditions apply modifiers`

#### DO NOT

- Include operation signatures with parameters or return types.

  **Example (fail):** `resolve(roll: int, dc: int) -> bool`

- Use UML or cardinality notation.

  **Example (fail):** `collaborators: DifficultyClass 1..1, Modifier 0..*`

- Use code-style boolean expressions in invariants.

  **Example (fail):** `invariant: damage >= threshold && !isImmune`

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Every concept from domain sketch has a CRC block

**Scanner:** Manual review

After CRC enrichment, every concept from the domain sketch must have a corresponding CRC block. No concept may be silently dropped.

#### DO

- Create a CRC block for each `#### **ConceptName**` heading in the domain sketch.

#### DO NOT

- Drop a concept without creating a CRC block for it.

  **Example (fail):** Sketch has `#### **Trait**` but no CRC block mentions Trait.

- Introduce a CRC block that has no corresponding concept in the sketch.

  **Example (fail):** A CRC block for `Resolution Engine` appears but no concept heading in the sketch supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Subtypes use ConceptName : BaseConcept on the heading line

**Scanner:** Manual review

When a concept is a specialization of another, its CRC heading must use `#### **ConceptName : BaseConcept**` notation. The block states only delta responsibilities — what it adds or overrides — and inherits the rest from the parent silently.

#### DO

- Use `#### **ConceptName : BaseConcept**` for subtypes.

  **Example (pass):**
  ```
  #### **Opposed Check : Check**
  use opposing trait          | Trait
                              |   invariant: both sides resolve as standard Checks; higher result wins
  ```

- State only delta responsibilities.

  **Example (pass):** Parent `Check` owns `resolve`; subtype `Opposed Check : Check` adds only `use opposing trait` and its invariants.

#### DO NOT

- Use the domain sketch English form `*is a type of*` in CRC headings.

  **Example (fail):** `#### **Opposed Check** *(is a type of Check)*`

- Duplicate parent responsibilities in the subtype block.

  **Example (fail):** `Opposed Check` repeats `use trait`, `use difficulty class`, `apply circumstance` — those are identical to the parent and must not be restated.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: State marker is crc

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: crc`.

#### DO

- Set the front matter to exactly `state: crc`.

#### DO NOT

- Leave the state at `domain-sketch`.
- Omit the front matter entirely.

**Source:** Engagement convention (class-responsibility-collaborator skill).
<!-- execute_rules:bundle_rules:end -->
