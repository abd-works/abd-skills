---
name: elaborate-business-logic
description: >-
  Elaborate state machines and declarative invariants for stateful domain
  concepts so lifecycle rules are explicit, testable, and immune to
  assumption drift.
---
# elaborate-business-logic

## Purpose

Domain concepts that own lifecycle-shaped mechanics — state changes, threshold ladders, supersession, spend/recover — carry implicit rules that developers must honour when they build the real system. Left implicit, those rules drift: one developer assumes a transition is legal, another assumes it is not, and bugs hide behind silent disagreement. Elaborating state machines and declarative invariants makes the domain's rules visible in one place, checkable by review, and directly translatable into guards and tests downstream.

## When to use

- The module file has reached `state: crc` and you need to enrich it further.
- You are preparing for scenario walkthroughs and need lifecycle guards and always-true constraints to reference.
- A concept's CRC responsibilities hint at state changes or thresholds but no explicit lifecycle has been written yet.

## Core concepts

### State / lifecycle

A state/lifecycle block names the **states** a concept can occupy, the **transitions** between them, and any **terminal states** (states with no outbound transition). Illegal transitions — moves the domain explicitly forbids — are called out so they cannot be coded by accident.

One concept, one lifecycle. If a concept has no meaningful states it is stateless and gets no block.

### Invariants

An invariant is a short declarative constraint — phrased with "must", "cannot", or "only if" — that the type enforces. Invariants are not procedures; they describe what must remain true, not how to make it true. Tie each invariant to a state or transition when the connection is obvious.

Invariants and lifecycle are two views of the same rules: invariants are the constraints that make transitions legal and the facts that must hold in each state.

### When to skip a concept

Skip a concept entirely when it is stateless in the source and no mechanics bullets imply always-true constraints. Do not invent lifecycle for concepts that are pure data carriers or collaborators without state.

## Build

1. **Read the module file** — locate the CRC content and confirm the front-matter shows `state: crc`.
2. **Identify stateful concepts** — scan CRC responsibilities and the mechanics bullets carried forward from the object sketch. Mark each concept that owns state changes, threshold ladders, supersession, spend/recover, or other lifecycle-shaped mechanics.
3. **Write state/lifecycle blocks** — for each stateful concept, list named states, allowed transitions (one line each), illegal transitions (one line each), and terminal states where relevant.
4. **Write invariant lines** — for each concept with a lifecycle block, add declarative "must / cannot / only if" constraints. Tie to a state or transition when obvious. If the lifecycle exists but invariants are not yet enumerable, write "(none yet)".
5. **Skip stateless concepts** — concepts with no lifecycle and no implied constraints get no subsection.
6. **Bump state** — update the module file front-matter from `state: crc` to `state: business-logic`.

Only elaborate concepts that already appear in the CRC content; do not introduce new types. Use English prose only — no method signatures (those belong to a later phase). Derive detail from mechanics bullets and carry-forward extracts, not from inventing rules.

Use `templates/business-logic-module-template.md` for the per-concept layout.

## Validate

- Every CRC concept that is stateful (or has mechanics implying state) has either a **State / lifecycle** block or an explicit "(stateless — no lifecycle block)" note.
- Every concept with a **State / lifecycle** block has at least one **Invariant** line or an explicit "(none yet)".
- No duplication of CRC responsibilities or collaborator prose — only lifecycle and invariant elaboration appears.
- Front-matter `state` reads `business-logic` after the build completes.
- All lifecycle detail traces back to mechanics bullets or source extracts — nothing is invented.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: English only — no method signatures

All lifecycle and invariant content must be written in plain English prose. No method signatures, typed parameters, return types, or code-level notation may appear. Passing means every line reads as natural language. Failing means design-level notation has leaked into the business-logic elaboration.

#### DO

- Describe transitions and constraints in natural English.

  **Example (pass):** "A character transitions from active to staggered when damage equals or exceeds the staggered threshold."

- Use domain vocabulary without formalising it into code.

  **Example (pass):** "Damage condition must equal the highest single penalty applied, not the sum."

#### DO NOT

- Include method signatures with typed parameters.

  **Example (fail):** `applyDamage(amount: int, type: DamageType): void`

- Use return-type annotations or generic type syntax.

  **Example (fail):** `getCondition(): Condition<Staggered>`

- Use code-style boolean expressions instead of English.

  **Example (fail):** `damage >= threshold && !isImmune` instead of "damage equals or exceeds the threshold and the character is not immune."

### Rule: Invariants present for lifecycle concepts

Every concept that has a **State / lifecycle** block must also have at least one **Invariant** line or an explicit "(none yet)" placeholder. Passing means every lifecycle block is paired with invariant coverage. Failing means a lifecycle block exists with no invariant section at all.

#### DO

- Add at least one invariant tied to the lifecycle.

  **Example (pass):**
  ```
  ### Character
  #### State / lifecycle
  States: active, staggered, incapacitated, dying, dead
  ...
  #### Invariants
  - Damage condition must equal the highest single penalty applied, not the sum.
  - A character cannot transition to dying unless incapacitated first.
  ```

- Use "(none yet)" when the lifecycle is clear but invariants are not yet enumerable.

  **Example (pass):**
  ```
  ### Initiative Entry
  #### State / lifecycle
  States: waiting, acting, delayed, done
  ...
  #### Invariants
  (none yet)
  ```

#### DO NOT

- Write a lifecycle block and omit the invariant section entirely.

  **Example (fail):**
  ```
  ### Attack
  #### State / lifecycle
  States: declared, rolled, resolved
  Transitions: declared → rolled, rolled → resolved
  ```
  No `#### Invariants` heading follows — reader cannot tell whether invariants were considered.

- Duplicate lifecycle transitions as pseudo-invariants.

  **Example (fail):** "Must transition from declared to rolled before resolved" — that is a transition rule, not a declarative constraint.

### Rule: No CRC duplication

The business-logic section must not duplicate CRC "Responsible for" or "Collaborators" prose. Only lifecycle and invariant elaboration belongs here. Passing means the business-logic content adds new lifecycle and invariant detail without restating CRC responsibilities. Failing means CRC text has been copied or paraphrased into the business-logic section.

#### DO

- Reference a CRC concept by name and add only lifecycle states, transitions, and invariants.

  **Example (pass):**
  ```
  ### Power Level
  #### State / lifecycle
  States: base, shifted
  Transitions: base → shifted (power-level shift applied), shifted → base (shift expires)
  #### Invariants
  - Effective power level must never drop below 0.
  ```

- Keep CRC responsibilities in the CRC section and elaborate only the state/invariant dimension here.

  **Example (pass):** The CRC says "Responsible for: tracking current power level and applying shifts." The business-logic section adds lifecycle states and invariants without repeating that sentence.

#### DO NOT

- Copy or paraphrase CRC "Responsible for" lines into the business-logic section.

  **Example (fail):**
  ```
  ### Power Level
  Responsible for tracking current power level and applying shifts.
  #### State / lifecycle
  ...
  ```

- Reproduce collaborator lists from the CRC.

  **Example (fail):**
  ```
  ### Attack
  Collaborates with: Target Defence, Damage, Effect
  #### State / lifecycle
  ...
  ```

### Rule: State marker is business-logic

After this skill runs, the module file's YAML front matter must contain `state: business-logic`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: business-logic`.

  **Example (pass):**
  ```
  ---
  state: business-logic
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

### Rule: Stateful concepts have lifecycle blocks

Every CRC concept whose responsibilities or mechanics imply state changes, threshold ladders, supersession, or spend/recover must have either a **State / lifecycle** block or an explicit "(stateless — no lifecycle block)" note. Passing means no stateful concept is left without coverage. Failing means a concept with state-shaped mechanics has neither a lifecycle block nor a stateless annotation.

#### DO

- Add a State / lifecycle block for concepts with state-shaped mechanics.

  **Example (pass):**
  ```
  ### Power Attack
  #### State / lifecycle
  States: available, committed, resolved
  Transitions: available → committed (player declares), committed → resolved (attack roll completes)
  Terminal: resolved
  ```

- Add an explicit stateless note for concepts that appear in CRC but have no lifecycle.

  **Example (pass):**
  ```
  ### Damage Bonus
  (stateless — no lifecycle block)
  ```

#### DO NOT

- Omit a concept that has state-shaped mechanics without any annotation.

  **Example (fail):** The CRC lists "Condition" with responsibilities "applies modifiers while active, removed when duration expires" but the business-logic section has no entry for Condition.

- Assume a concept is stateless without checking its mechanics bullets.

  **Example (fail):** "Effect" has mechanics "activates on trigger, expires after duration" but is silently skipped — no lifecycle block, no "(stateless)" note.
<!-- execute_rules:bundle_rules:end -->
