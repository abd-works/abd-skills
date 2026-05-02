---
name: class-responsibility-collaborator
description: >-
  For every domain concept: assign responsibility, reject misplaced concerns,
  name collaborators, write lifecycle states and transitions, and declare
  invariants — all in one structured notation pass before object-model.
---
# class-responsibility-collaborator

## Purpose

Naming concepts and sketching behaviors tells the team *what exists* in the domain, but it does not settle what each concept **owns, refuses, and depends on** — nor does it make lifecycle rules and always-true constraints explicit enough to carry into scenario walks. This skill closes both gaps in one pass: for every concept the team writes a compact CRC block that locks down responsibility boundaries, then extends that block with lifecycle states and declarative invariants for concepts that carry state. The result is a structured, scannable record per concept that downstream skills (object-model, scenario-walkthrough) can read without re-interpreting prose.

---

## When to use this skill

- The module file's front matter shows `state: domain-sketch`.
- The user asks to "run CRC," "assign responsibilities," "add lifecycle," or "elaborate invariants."
- The next modeling step needs responsibility boundaries, lifecycle guards, and always-true constraints before scenario walks.

---

## Core concepts

### Responsibility

A **responsibility** is a short English statement of what a concept **must do** — the behavior it owns and no other concept should duplicate. Responsibilities are derived from the sketch's behavior lines, but sharpened: each one names the single concern this concept is the authority on.

### Not responsible for

Every concept also carries at least one **"not responsible for"** statement — a plausible concern that someone might mistakenly assign to it, explicitly rejected. A good rejection names a specific behavior and says where it actually belongs (or that it is out of scope). This prevents scope creep by making boundaries visible before code exists.

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
    not_responsible: does not own the narrative consequence of failure — that belongs to the calling rule or encounter context
    collaborators: Difficulty Class, Modifier
    lifecycle: (stateless)
    invariants: shape is always roll total versus difficulty class; subtypes only vary how total or DC is produced

Difficulty Class
    responsible: holds the numeric threshold an action must meet or exceed to succeed
    not_responsible: does not apply the roll or determine success — setting the threshold is its only job
    collaborators: (none)
    lifecycle: (stateless)
    invariants: (none)

Condition
    responsible: represents a named state applied to a character that imposes specific modifiers or restrictions
    not_responsible: does not enforce its own modifiers — enforcement belongs to the consuming module (Combat for action restrictions, Check Resolution for check penalties)
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
    not_responsible: does not own the generic pass/fail resolution — that is inherited from Check
    collaborators: Ability Score, Proficiency
    lifecycle: (stateless)
    invariants: (none)
```

---

## Build

1. **Read the module file.** Confirm `state: domain-sketch` in the front matter.
2. **Inventory concepts.** List every `### Concept` and `### Subtype *is a type of* Base` heading from the Object Sketch section.
3. **Derive CRC fields.** For each concept, produce the first three fields using `templates/crc-outline-template.md`:
   - **`responsible:`** — one sentence stating what this concept owns, derived from its sketch behaviors.
   - **`not_responsible:`** — at least one plausible misplaced concern explicitly rejected, with a note on where it actually belongs when possible.
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
3. **Rejection present.** Every block has a non-empty `not_responsible:` line rejecting at least one plausible misplaced concern.
4. **Collaborators present.** Every block lists collaborators or says `(none)` explicitly.
5. **Subtype notation.** Subtypes use `Child : Parent` and state only delta responsibilities.
6. **Lifecycle present.** Every block has a `lifecycle:` field — either a populated block or `(stateless)`.
7. **Invariants present.** Every block with a lifecycle has an `invariants:` field — populated, `(none yet)`, or `(none)`.
8. **English only.** No method signatures, typed properties, or UML notation anywhere.
9. **State marker.** Front matter reads `state: crc`.
10. **Additive.** All prior content (Object Sketch, Domain-logic) is unchanged — CRC is appended, not substituted.

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
      not_responsible: does not combine itself with other modifiers — stacking is the Check's job
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
      not_responsible: does not own narrative consequences
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

### Rule: Every CRC block has at least one "not responsible for" rejection

**Scanner:** Manual review

Every CRC block must include a non-empty `not_responsible:` line that explicitly rejects at least one plausible misplaced concern. Passing means every block names something the concept must not own. Failing means the line is missing, empty, or contains only a placeholder.

#### DO

- State a concrete behavior that someone might mistakenly assign to this concept, and reject it.

  **Example (pass):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      not_responsible: does not own the narrative consequence of failure — that belongs to the calling rule or encounter context
      collaborators: Difficulty Class, Modifier
  ```

- When possible, name where the rejected concern actually belongs.

  **Example (pass):** `not_responsible: does not determine the base DC — that is the Difficulty Class's responsibility`

#### DO NOT

- Omit the `not_responsible:` line entirely.

  **Example (fail):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      collaborators: Difficulty Class, Modifier
  ```

- Use a generic placeholder that rejects nothing specific.

  **Example (fail):** `not_responsible: N/A` or `not_responsible: nothing to note`

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
      not_responsible: does not own the generic pass/fail resolution — that is inherited from Check
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
