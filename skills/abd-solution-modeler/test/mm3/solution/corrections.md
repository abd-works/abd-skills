# Corrections

## Phase 6 — Concept Model

- **DO NOT** invent a direct ability rank cap from PowerLevel.
- **Example (wrong):** `ability_rank_limit: ability rank <= power_level` — no such rule exists in M&M 3e.
- **Example (correct):** Abilities are uncapped directly; they are constrained indirectly through defense trade-off limits (dodge/parry + toughness <= PL*2, fortitude + will <= PL*2) and the power point budget.

## Skill-level — Phases 2, 5, 6, 7 (process fix)

- **DO NOT** flatten rich subsystems into enum values. When context describes variants with distinct mechanics (own cost, resistance, rules), each is a concept.
- **Example (wrong):** `EnumType effect_type {damage, affliction, movement, sensory}` — treats 30+ mechanically distinct effect types as labels.
- **Example (correct):** **Damage** : **Effect**, **Affliction** : **Effect**, **Healing** : **Effect**, **Senses** : **Effect** etc. — each with own cost, resistance, conditions.

- **DO NOT** use short aliases (2-3 chars) in concept_guidance.json. They false-match English text.
- **Example (wrong):** `"PowerLevel": ["power level", "PL"]` — "PL" matches "applying", "playing", "display"...
- **Example (correct):** `"PowerLevel": ["power level"]` — full phrase only.

- **DO NOT** substitute background knowledge for evidence. Read the actual evidence files per concept.
- **Example (wrong):** Modeling Damage as "forces Toughness resistance check" from memory instead of citing act_0337.
- **Example (correct):** Every property/operation cites evidence ID or raw text from evidence files.

- **DO NOT** stop at top-N terms when scanning for hidden concepts. Check coverage per module — every subsystem in the context needs a concept.
- **Example (wrong):** Phase 5 scanned top 30 terms, missed Affliction, Immunity, Healing, Senses, Nullify, Weaken...
- **Example (correct):** For each module, read context chunks and verify every distinct mechanic is named.
