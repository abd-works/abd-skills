# Corrections log

Project: mm3e-online-holistic (Ability module)
Source: abd-key-abstractions → abd-domain-sketch pipeline

---

## Entry: Over-promoted KAs in a small module

- **Status:** confirmed
- **Context:** Generating `ability-key-abstractions.md` from `ability-domain-language.md` for the Ability module (8 ability scores, defenses, absent/debilitated states).
- **DO / DO NOT:**
  - **DO** apply the independence test strictly: a concept that only exists as a state, invariant, or derived value of another concept fails the independence test and must stay as a property, behavior, or concept within the KA grouping — not promoted to its own KA.
  - **DO** consider module size before multiplying KAs — a small, cohesive module (one core mechanic with states and derived values) is likely one KA, not four.
  - **DO NOT** promote absent-state, debilitated-state, or derived-value groups to KA status when they have no identity outside the base concept they modify.
- **Example (wrong):**
  Four KAs generated for the Ability module:
  - `Ability Score` — the base concept
  - `Absent Ability` — actually a state on ability (no rank, auto-fail, per-ability capability-loss effects)
  - `Derived Defense` — actually defense values derived from ability ranks
  - `Debilitated Ability` — actually an invariant on ability (rank floor at −5, per-ability-group conditions)

  `Absent Ability` and `Debilitated Ability` have no identity outside the ability they modify — they are conditions/states applied to a character when an ability enters a threshold. `Derived Defense` groups concepts that exist because abilities exist — they derive from ability ranks and belong under the same KA.
- **Example (correct):**
  One KA for the entire module:
  - `Ability` — owns rank, cost formula, cascade rule, physical/mental partition, eight named instances, absent state (per-ability capability-loss effects), debilitated state (per-ability-group conditions at rank < −5), derived defense values (Dodge, Parry, Fortitude, Toughness, Will), initiative, and Enhanced Ability as a subtype.

  Absent and debilitated are modeled as behavior bullets and invariants on the `ability` concept. Defense is a concept under the Ability KA with five subtypes. The module is small — one KA reflects the actual domain structure.
- **Likely source:** `instruction not read` — the independence test and module-fit test in the skill were applied too loosely; states and derived values were treated as if they had standalone identity when they do not.

---
