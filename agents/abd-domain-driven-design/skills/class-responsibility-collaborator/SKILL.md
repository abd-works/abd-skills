---
name: class-responsibility-collaborator
description: >-
  For every domain concept: assign responsibility, name collaborators,
  write lifecycle states and transitions, and declare invariants — all
  in one structured pass before object-model.
---
# class-responsibility-collaborator

## Purpose

This skill refines a collection of domain concepts from context and defines each concept's ownership, collaborators, lifecycle states, and invariants — all in one structured pass. 

**CRC (Class-Responsibility-Collaborator)** modeling. introduced by Ward Cunningham and Kent is lightweight way to explore object-oriented designs. A CRC model asks three questions per concept — what is it responsible for, what does it collaborate with, and what class does it belong to — so teams can role-play interactions and catch misplaced responsibilities before writing code. 

This skill refines existing domain artifacts in context to formally structure each domain concept's authority and boundaries: what each one owns, who it depends on, how it changes over time, and what must always remain true. Teams use this to surface hidden coupling and agree on lifecycle rules before writing code.

---

## When to use this skill

- You have a set of domain concepts with behaviors identified but ownership, boundaries, and lifecycle rules are not yet explicit.
- The user asks to "run CRC," "assign responsibilities," "add lifecycle," or "elaborate invariants."
- The user wants to understand or generate a class-responsibility-collaborator model.
- The domain has sufficient complexity that explicit responsibility boundaries, lifecycle guards, and always-true constraints are worth modeling.

---

## Core concepts

### Class

A **class** in CRC modeling is any named domain concept that carries its own identity and behavior — not a programming-language class. It is distinct domain concept: each class gets its own CRC entry so the team can reason about what it owns, who it works with, and how it changes over time. Classes come from whatever domain analysis produced the concepts being refined.

### Responsibility

A **responsibility** is a short English statement of what a concept **must do** — the behavior it owns and no other concept should duplicate. Responsibilities are derived from the sketch's behavior lines, but sharpened: each one names the single concern this concept is the authority on.

### Collaborators

**Collaborators** are the other domain concepts this one works with to fulfill its responsibilities. They are derived from the sketch's collaboration lines and subtype edges. If a concept collaborates with many others it may be doing too much; if it collaborates with none it may be a data bag rather than a true domain object.

### Subtype notation

When a concept is a specialization, its name line uses **`Child : Parent`** notation. The child block states only delta responsibilities — what it adds or overrides — and inherits the rest from the parent.

### State / lifecycle

A **state/lifecycle** block names the **states** a concept can occupy, the **transitions** between them, and any **terminal states**. Illegal transitions — moves the domain explicitly forbids — are called out so they cannot be coded by accident. One concept, one lifecycle. If a concept has no meaningful states it is stateless and the block is marked `(stateless)`.

### Invariants

An **invariant** is a short declarative constraint — phrased with "must", "cannot", or "only if" — that the type enforces at all times. Invariants are not procedures; they describe what must remain true, not how to make it true. Tie each invariant to a state or transition when the connection is obvious. When the lifecycle is clear but invariants are not yet enumerable, write `(none yet)`.

---

## The shape of a CRC block

Each concept from the sketch becomes one named block. The name is flush left; fields are indented beneath it. Subtypes use `Child : Parent` notation. Stateless concepts mark their lifecycle field `(stateless)`.

```markdown
## Module: [Check Resolution]

Check
    responsible: resolves whether an attempted action succeeds or fails by comparing the total roll to the difficulty class
    collaborators: Difficulty Class, Modifier
    lifecycle: (stateless)
    invariants: shape is always roll total versus difficulty class; subtypes only vary how total or DC is produced

Difficulty Class
    responsible: holds the numeric threshold an action must meet or exceed to succeed
    collaborators: (none)
    lifecycle: (stateless)
    invariants: (none)

Condition
    responsible: represents a named state applied to a character that imposes specific modifiers or restrictions
    collaborators: Check Result
    lifecycle:
        states: inactive, active, superseded, resolved
        transitions: inactive → active (source effect imposed), active → superseded (more severe condition in chain applied from same source), active → resolved (source effect ends or successful resistance check)
        illegal: resolved → active (a resolved condition cannot re-activate from the same source without a new imposition)
        terminal: resolved
    invariants:
        - a condition already present in the supersession chain is overridden by the more severe one, never duplicated
        - a combined condition is removed entirely when its source effect ends; its constituents do not revert to independent active states

Saving Throw : Check
    responsible: adds an ability-score basis and proficiency eligibility on top of the base check resolution
    collaborators: Ability Score, Proficiency
    lifecycle: (stateless)
    invariants: (none)
```

---

## Build

1. **Read the module file.** Confirm `state: domain-sketch` in the front matter.
2. **Inventory concepts.** List every `### Concept` and `### Subtype *is a type of* Base` heading from the Object Sketch section.
3. **Derive CRC fields.** For each concept, produce the first two fields using `templates/crc-outline-template.md`:
   - **`responsible:`** — one sentence stating what this concept owns, derived from its sketch behaviors.
   - **`collaborators:`** — comma-separated list of domain concepts it works with, derived from sketch collaborations and subtype edges. Write `(none)` when there are none.
4. **Derive lifecycle fields.** For each concept, scan its CRC responsibilities and the sketch behavior bullets for state-shaped mechanics — state changes, threshold ladders, supersession, spend/recover. If found:
   - **`lifecycle:`** — list named states, allowed transitions (one line each), illegal transitions, and terminal states.
   - If stateless, write `lifecycle: (stateless)`.
5. **Derive invariant fields.** For each concept, add declarative "must / cannot / only if" constraints as `invariants:` bullets. Tie to a state or transition when obvious. Write `(none yet)` when the lifecycle is clear but invariants are not yet enumerable. Write `(none)` for stateless concepts with no always-true constraints.
6. **Write the `## CRC` section.** Append it after the existing Object Sketch content in the module file. Group blocks by module when the file has multiple `## Module:` sections. English only — no method signatures, no typed properties.
7. **Bump state.** Change the front matter from `state: domain-sketch` to `state: crc`.

---

## Validate

1. **Coverage.** Every concept and subtype from the Object Sketch has a corresponding CRC block.
2. **Responsibility present.** Every block has a non-empty `responsible:` line.
3. **Collaborators present.** Every block lists collaborators or says `(none)` explicitly.
4. **Subtype notation.** Subtypes use `Child : Parent` and state only delta responsibilities.
5. **Lifecycle present.** Every block has a `lifecycle:` field — either a populated block or `(stateless)`.
6. **Invariants present.** Every block with a lifecycle has an `invariants:` field — populated, `(none yet)`, or `(none)`.
7. **English only.** No method signatures, typed properties, or UML notation anywhere.
8. **State marker.** Front matter reads `state: crc`.
9. **Additive.** All prior content (Object Sketch, Domain-logic) is unchanged — CRC is appended, not substituted.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Collaborators trace to sketch collaborations and subtype edges

**Scanner:** Manual review

The `collaborators:` line in each CRC block must list domain concepts that appear in the Object Sketch's collaboration lines or subtype edges for that concept. Concepts with no sketch collaborations must say `(none)` explicitly. Passing means every listed collaborator is traceable and no-collaborator blocks are marked. Failing means collaborators are invented, omitted without explanation, or left blank.

#### DO

- List collaborators that correspond to sketch collaboration lines or subtype relationships.

  **Example (pass):** Sketch says "Check — collaborates with → Difficulty Class, Modifier"; CRC block has `collaborators: Difficulty Class, Modifier`.

- Write `(none)` when a concept has no sketch collaborations.

  **Example (pass):**
  ```
  Modifier
      responsible: represents a single numeric adjustment to a check
      collaborators: (none)
  ```

#### DO NOT

- Invent collaborators that have no basis in the Object Sketch.

  **Example (fail):** CRC block lists `collaborators: Logger, EventBus` but neither concept appears anywhere in the sketch.

- Leave the collaborators line blank or omit it entirely.

  **Example (fail):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      collaborators:
  ```

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: English prose only — no method signatures or typed notation

**Scanner:** Manual review

The entire CRC section — responsibilities, rejections, collaborators, lifecycle transitions, and invariants — must be written in plain English. No method signatures, typed parameters, return types, UML notation, cardinality markers, or code-level constructs are permitted anywhere. Passing means every line reads as a natural-language sentence or phrase. Failing means design-level notation has leaked into any field.

#### DO

- Write responsibilities, rejections, and collaborator descriptions in prose.

  **Example (pass):** `responsible: resolves whether an attempted action succeeds or fails against a target difficulty`

- Describe lifecycle transitions and constraints in natural English.

  **Example (pass):** `transitions: inactive → active (source effect imposed), active → resolved (source effect ends or resistance check succeeds)`

- Write invariants as declarative English statements.

  **Example (pass):** `- a condition already present in the supersession chain is overridden by the more severe one, never duplicated`

#### DO NOT

- Include operation signatures with parameters or return types.

  **Example (fail):** `responsible: resolve(roll: int, dc: int) -> bool`

- Use typed property declarations.

  **Example (fail):** `responsible: stores result: CheckResult and modifiers: List<Modifier>`

- Include UML or cardinality notation in collaborators.

  **Example (fail):** `collaborators: DifficultyClass 1..1, Modifier 0..*`

- Use code-style boolean expressions in invariants.

  **Example (fail):** `invariants: damage >= threshold && !isImmune` — write "damage equals or exceeds the threshold and the character is not immune" instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Every concept from object sketch has a CRC block

**Scanner:** Manual review

After CRC enrichment, every concept and subtype heading from the Object Sketch section must have a corresponding CRC block in the CRC section. No concept may be silently dropped. Passing means every concept is accounted for. Failing means a concept exists in the Object Sketch but has no CRC block.

#### DO

- Create a CRC block for each `### Concept` heading in the Object Sketch.

  **Example (pass):** Object Sketch has `### Check`, `### Difficulty Class`, `### Trait` — CRC section has blocks named `Check`, `Difficulty Class`, `Trait`.

- Create a CRC block for each `### Subtype *is a type of* Base` heading in the Object Sketch.

  **Example (pass):** Object Sketch has `### Saving Throw *is a type of* Check` — CRC section has a block `Saving Throw : Check`.

#### DO NOT

- Drop a concept without creating a CRC block for it.

  **Example (fail):** `### Trait` exists in the Object Sketch but no CRC block mentions Trait — it simply vanished.

- Introduce a CRC block that has no corresponding concept in the Object Sketch.

  **Example (fail):** A CRC block for "Resolution Engine" appears but no concept heading in the sketch supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Invariants present for lifecycle concepts

**Scanner:** Manual review

Every concept that has a populated `lifecycle:` block must also have an `invariants:` field with at least one declarative constraint or an explicit `(none yet)` placeholder. Stateless concepts must have `invariants: (none)` or a value. Passing means every CRC block has an invariants field. Failing means a block with a lifecycle has no invariants field at all.

#### DO

- Add at least one invariant tied to the lifecycle for stateful concepts.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          ...
      invariants:
          - a condition already present in the supersession chain is overridden by the more severe one, never duplicated
          - a combined condition is removed entirely when its source effect ends
  ```

- Use `(none yet)` when the lifecycle is clear but invariants are not yet enumerable.

  **Example (pass):**
  ```
  Check Result
      ...
      lifecycle:
          states: pending, succeeded, failed
          ...
      invariants: (none yet)
  ```

- Use `(none)` for stateless concepts with no always-true constraints.

  **Example (pass):**
  ```
  Difficulty Class
      ...
      lifecycle: (stateless)
      invariants: (none)
  ```

#### DO NOT

- Write a lifecycle block and omit the `invariants:` field entirely.

  **Example (fail):** A CRC block ends after `lifecycle: states: ...` with no `invariants:` line — reader cannot tell whether constraints were considered.

- Duplicate lifecycle transitions as pseudo-invariants.

  **Example (fail):** `invariants: must transition from inactive to active before resolving` — that is a transition rule, not a declarative constraint on what must always be true.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: State marker is crc

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: crc`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: crc`.

  **Example (pass):**
  ```
  ---
  state: crc
  ---
  ```

#### DO NOT

- Leave the state at `domain-sketch` (the previous step).

  **Example (fail):**
  ```
  ---
  state: domain-sketch
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Stateful concepts have lifecycle blocks

**Scanner:** Manual review

Every concept whose responsibilities or sketch behaviors imply state changes, threshold ladders, supersession, or spend/recover must have either a populated `lifecycle:` block or `lifecycle: (stateless)`. Passing means no concept with state-shaped mechanics is left without coverage. Failing means a concept's mechanics imply state but its CRC block has no lifecycle field.

#### DO

- Add a populated lifecycle block for concepts with state-shaped mechanics.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          transitions: inactive → active (source effect imposed), active → resolved (source effect ends)
          illegal: resolved → active (cannot re-activate from same source without new imposition)
          terminal: resolved
  ```

- Write `lifecycle: (stateless)` for concepts that appear in CRC but own no state changes.

  **Example (pass):**
  ```
  Difficulty Class
      responsible: holds the numeric threshold an action must meet or exceed to succeed
      ...
      lifecycle: (stateless)
  ```

#### DO NOT

- Omit the `lifecycle:` field entirely.

  **Example (fail):** A CRC block for `Condition` ends after `collaborators:` with no `lifecycle:` line — reader cannot tell whether lifecycle was considered.

- Assume a concept is stateless without checking its sketch behavior bullets.

  **Example (fail):** `Condition` has sketch behaviors "applied, superseded, resolved" but is given `lifecycle: (stateless)` without any reasoning.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Subtypes use Child : Parent on the name line

**Scanner:** Manual review

When a concept is a specialization of another, its CRC block name line must use `Child : Parent` notation. The block states only delta responsibilities — what the subtype adds or overrides beyond the base. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate base responsibilities.

#### DO

- Use `Child : Parent` on the name line for subtypes.

  **Example (pass):**
  ```
  Saving Throw : Check
      responsible: adds an ability-score basis and proficiency eligibility on top of the base check resolution
      collaborators: Ability Score, Proficiency
  ```

- State only delta responsibilities that the subtype adds beyond what the parent already owns.

  **Example (pass):** Parent `Check` owns resolution; subtype `Saving Throw : Check` adds only "adds an ability-score basis."

#### DO NOT

- Use the Object Sketch English heading form in CRC blocks.

  **Example (fail):** `Saving Throw *is a type of* Check` — CRC uses `:` notation, not the sketch's English form.

- Use code-style inheritance syntax.

  **Example (fail):** `SavingThrow extends Check` or `class SavingThrow(Check)`

- Duplicate base responsibilities in the subtype block.

  **Example (fail):** Subtype repeats "resolves whether an attempted action succeeds or fails" — that belongs on the parent `Check` only.

**Source:** Engagement convention (class-responsibility-collaborator skill).
<!-- execute_rules:bundle_rules:end -->
