# Corrections log

Project: domain-sketch skill
Source: domain-sketch skill (pipeline runs)

---

## Entry: Concept defined inline as property instead of its own concept block

- **Status:** confirmed
- **Context:** domain-sketch — check-resolution module, `### condition > Domain Sketch`
- **DO:** When a named domain concept is first introduced as a tracked property or reference on another concept, give it its own `### concept-name` block in the domain sketch. Do not embed the concept's full definition inline as a parenthetical on another concept's bullet.
- **Example (wrong):**
  `- tracks its *condition source* — the *power*, *effect*, *attacker*, or *event/situation* that imposed it — and carries an *active* or *inactive* status`
  The full definition of *Condition Source* was embedded inline inside `### condition` rather than extracted as its own `### condition source` concept block.
- **Example (correct):**
  The inline definition was trimmed to `- tracks its *condition source* and carries an *active* or *inactive* status`. A separate `### condition source` concept block was added with its own `#### Domain Sketch` bullets, `#### Decisions made`, and `#### References`.
- **Likely source:** prompt gap — the domain-sketch skill does not instruct checking whether a named concept introduced as a property on another concept warrants its own block before embedding its definition inline.

---

## Entry: Boundary concept placed in Core Domain instead of Boundary Domain

- **Status:** confirmed
- **Context:** domain-sketch — check-resolution module, `### ongoing effect`
- **DO:** When a concept is owned by another module and only touches this module at its edge, model it in the `# Boundary Domain` section under the correct owning module heading — not as a `### concept-name` block in Core Domain. Ask: does this module *own* the concept's lifecycle, or does it only *observe* a quality of it?
- **Example (wrong):**
  `### ongoing effect` was created as a Core Domain concept block with its own `#### Domain Sketch`, `#### Decisions made`, and `#### References`. A decision note even stated it was "not a synonym for *power effect*" — but it was still placed in Core.
- **Example (correct):**
  The block was removed from Core Domain. The "ongoing" quality was modeled as Domain Sketch bullets on the `## Effect / power effect` Boundary Domain entry: whether an effect is ongoing is the Power module's concern; this module only owns the check-resolution behavior (what happens when the resistance check succeeds or fails).
- **Likely source:** prompt gap — the domain-sketch skill does not instruct checking the owning module of a concept before placing it in Core vs. Boundary Domain.

---

## Entry: Effect behavior described on a condition concept bullet

- **Status:** confirmed
- **Context:** domain-sketch — check-resolution module, `### condition > Domain Sketch`
- **DO:** Each behavior bullet on a concept must describe what *that concept* does or is. Do not embed the behavior or decision logic of a collaborating concept inline as a parenthetical.
- **Example (wrong):**
  `- is imposed *failed resistance checks* (the effect defines which *condition* applies at each *degree of failure*), *fatigue* from *extra effort*, *environmental hazards*, or *power effects*`
  The parenthetical describes *effect* behavior (degree-of-failure → condition mapping) inside a `### condition` bullet.
- **Example (correct):**
  Trimmed to: `- is imposed by its *condition source* — a *failed resistance check*, *fatigue* from *extra effort*, an *environmental hazard*, or a *power effect* directly`. The degree-of-failure logic belongs in `## Effect / power effect` Domain Sketch.
- **Likely source:** prompt gap — the domain-sketch skill does not instruct verifying that each bullet's subject matches the concept being described before writing parentheticals that cross into a collaborator's responsibility.

---

## Entry: Behavior and its produced result written as separate bullets

- **Status:** confirmed
- **Context:** domain-sketch — check-resolution module, `### check > Domain Sketch`
- **DO:** When a behavior bullet directly produces a result, write the result on the same line as the behavior. Do not separate them into two bullets.
- **Example (wrong):**
  ```
  - is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*
  - produces a *check result*
  ```
  Two separate bullets when the second is the direct output of the first.
- **Example (correct):**
  `- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*, producing a *check result*`
  Cause and result on the same line.
- **Likely source:** prompt gap — the domain-sketch skill does not instruct combining a behavior and its immediate produced result onto a single bullet.

---
