<!--
  crc.md — CRC with lifecycle and invariants.

  Copy to: <workspace>/abd-domain-driven-design/crc.md (or append ## CRC section to module file)

  Each concept gets one named block with five fields:
    responsible:     — what this concept owns (one sentence)
    not_responsible: — at least one explicitly rejected concern
    collaborators:   — other domain concepts worked with, or (none)
    lifecycle:       — states, transitions, illegal moves, terminal states — or (stateless)
    invariants:      — declarative must/cannot/only-if constraints — or (none) / (none yet)
-->

## Module: [{{ModuleName}}]

{{ConceptName}}
    responsible: {{one sentence — what this concept owns}}
    not_responsible: {{at least one plausible wrong owner, explicitly rejected}}
    collaborators: {{TypeA, TypeB, ... or (none)}}
    lifecycle: {{(stateless) — or: states: ...; transitions: ...; illegal: ...; terminal: ...}}
    invariants: {{must/cannot/only-if bullets — or (none) / (none yet)}}

{{SubtypeName}} : {{BaseConcept}}
    responsible: {{delta only — what this subtype adds or overrides}}
    not_responsible: {{...}}
    collaborators: {{...}}
    lifecycle: {{...}}
    invariants: {{...}}

---

## Module: [{{AnotherModule}}]

{{ConceptName}}
    responsible: {{...}}
    not_responsible: {{...}}
    collaborators: {{...}}
    lifecycle: {{...}}
    invariants: {{...}}

---

Instructions:

- Group concepts by module; module names match `domain-sketch.md` `## Module: [Name]` when present.
- One concept name per block (no `###` heading — the name is the first line).
- Subtype / generalization: `ChildConcept : ParentConcept` on the first line; delta responsibilities only.
- `collaborators:` lists other domain concepts this one works with (from sketch collaboration lines).
- `lifecycle:` — use `(stateless)` for concepts with no meaningful states.
- `invariants:` — use `(none)` for stateless concepts, `(none yet)` when lifecycle exists but constraints are not yet enumerable.
- English only; no operation signatures (those belong in object-model).

---

## Filled example (Check Resolution module)

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

Modifier
    responsible: represents a single numeric adjustment applied to a check roll
    not_responsible: does not combine itself with other modifiers — stacking is the Check's responsibility
    collaborators: (none)
    lifecycle: (stateless)
    invariants: (none)

Condition
    responsible: represents a named state applied to a character that imposes specific modifiers or restrictions
    not_responsible: does not enforce its own modifiers — enforcement belongs to the consuming module
    collaborators: Check Result
    lifecycle:
        states: inactive, active, superseded, resolved
        transitions: inactive → active (source effect imposed), active → superseded (more severe condition in chain applied), active → resolved (source effect ends or resistance check succeeds)
        illegal: resolved → active (cannot re-activate from the same source without a new imposition)
        terminal: resolved
    invariants:
        - a condition already present in the supersession chain is overridden by the more severe one, never duplicated
        - a combined condition is removed entirely when its source effect ends

Saving Throw : Check
    responsible: adds an ability-score basis and proficiency eligibility on top of the base check resolution
    not_responsible: does not own the generic pass/fail resolution — that is inherited from Check
    collaborators: Ability Score, Proficiency
    lifecycle: (stateless)
    invariants: (none)
```
