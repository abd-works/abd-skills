# Map-Model-Spec (Step 4 scaffold)

## Module: Check Resolution | Epic: Resolve Check

**Module:** Mechanism for resolving checks (d20 + modifier vs DC) and degrees of success or failure; includes skill checks, opposed checks, and resistance checks. (chunk: unit_00048)

**Concepts:**
- **Check** [foundational] — Owns: Determines success or failure by comparing roll result to DC; produces degree of success or failure. (chunk: unit_00048)
  - chunk_ids: [unit_00048, unit_00306, unit_01220]
- **DifficultyClass** — Owns: Target number for a check; varies by task. (chunk: unit_01220)
  - chunk_ids: [unit_01220]

**Epic:** **Player** or **System** rolls d20 + modifier; result is compared to DC to determine degree of success or failure. (chunk: unit_00048)
- Triggering-Actor: Player or GM | Responding-Actor: System
- Confirming stories: Resolve skill check, Resolve opposed check, Resolve resistance check

**Chunk index:** identified: [unit_00048, unit_00306, unit_01220] | provisional: [unit_04061] | ambiguous: []

---

## Module: Conflict and Actions | Epic: Run Action Round

**Module:** Action round, initiative order, and action types (standard, move, free, reaction) during conflicts. (chunk: unit_00048)

**Concepts:**
- **ActionRound** [foundational] — Owns: Orders turns by initiative; constrains what actions can be taken. (chunk: unit_00862)
  - chunk_ids: [unit_00048, unit_00862, unit_04149]
- **Initiative** — Owns: Determines order of action in conflict (d20 + initiative modifier). (chunk: unit_00862)
  - chunk_ids: [unit_00862]

**Epic:** **System** establishes initiative order; **Player** and **System** take actions within the round. (chunk: unit_04149)
- Triggering-Actor: GM | Responding-Actor: Player and System
- Confirming stories: Determine initiative order, Take standard action, Apply conditions from actions

**Chunk index:** identified: [unit_00048, unit_00862, unit_04149] | provisional: [] | ambiguous: []

---

## Module: Damage and Recovery | Epic: Resolve Damage

**Module:** Damage resistance check (Toughness vs rank+15), degrees of failure, and recovery. (chunk: unit_04061)

**Concepts:**
- **DamageResistance** [foundational] — Owns: Resolves damage effect via Toughness check; applies degree-based conditions. (chunk: unit_04061)
  - chunk_ids: [unit_04061, unit_01999]
- **Recovery** — Owns: Removes damage conditions over time; Healing/Regeneration can speed this. (chunk: unit_01999)
  - chunk_ids: [unit_01999]

**Epic:** **System** resolves damage resistance check; **Target** receives condition by degree of failure; recovery removes conditions. (chunk: unit_04061)
- Triggering-Actor: Attacker / Effect | Responding-Actor: Target / System
- Confirming stories: Resolve damage resistance check, Apply damage condition, Recover from damage

**Chunk index:** identified: [unit_04061, unit_01999] | provisional: [] | ambiguous: []

---

## Module: Character Traits | Epic: Build Character

**Module:** Allocation of power points to abilities, skills, advantages, powers, and complications; constrained by power level. (chunk: unit_00518)

**Concepts:**
- **PowerPoint** [foundational] — Owns: Budget for buying abilities, skills, advantages, powers. (chunk: unit_00518)
  - chunk_ids: [unit_00518, unit_03879]
- **Advantage** — Owns: Character option purchased with power points (1 per advantage or rank). (chunk: unit_00518)
  - chunk_ids: [unit_03879, unit_00518]

**Epic:** **Player** spends power points on abilities, skills, advantages, powers within power level limits. (chunk: unit_00518)
- Triggering-Actor: Player | Responding-Actor: System
- Confirming stories: Allocate ability ranks, Choose advantages, Select powers within PL

**Chunk index:** identified: [unit_00518, unit_03879, unit_00177] | provisional: [] | ambiguous: []

---

## Module: Powers and Effects | Epic: Configure Power

**Module:** Power effects, modifiers (extras and flaws), descriptors, and cost; application of effects in conflict. (chunk: unit_02684)

**Concepts:**
- **Effect** [foundational] — Owns: Named mechanical effect with rank, modifiers, and cost; may be noticeable or subtle. (chunk: unit_02684)
  - chunk_ids: [unit_02684, unit_03032, unit_01697]
- **Modifier** — Owns: Extra or flaw that changes effect cost or behavior. (chunk: unit_02684)
  - chunk_ids: [unit_02684, unit_03032]

**Epic:** **Player** defines effects with rank, modifiers, and descriptors; **System** enforces cost and PL limits. (chunk: unit_02684)
- Triggering-Actor: Player | Responding-Actor: System
- Confirming stories: Apply extra to effect, Apply flaw to effect, Resolve power resistance

**Chunk index:** identified: [unit_02684, unit_03032, unit_01697, unit_00665] | provisional: [] | ambiguous: []

---

## Cross-cutting notes

Condition (e.g. Weakened, dazed, staggered) appears in both Conflict and Actions and Damage and Recovery; may be [cross-cutting] once deepened. Check (roll vs DC) is used by resistance checks in Damage and by skill/opposed checks in Check Resolution.
