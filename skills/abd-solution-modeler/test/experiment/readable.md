# Step 1 — Modules and Epics (v3 Output)

---

## Module: Resolution | Epic: Resolve **Check**

**Module:** The single mechanic that resolves all uncertain outcomes: roll d20, add modifier, compare to DC; degree of success or failure determines what happens next. (chunk: 4cd63373be61)

**Concepts:**
- **Check** [foundational] — Owns: whether an action succeeds or fails and by how much. (chunk: 4cd63373be61)
  - chunk_ids: [4cd63373be61, 714405399e02]
  - Number modifier (chunk: 714405399e02)
  - Number difficulty_class (chunk: 714405399e02)
  - resolve() → Degree (chunk: 4cd63373be61)
- **Degree** [foundational] — Owns: how far above or below DC a result landed — drives what consequence applies. (chunk: 4cd63373be61)
  - chunk_ids: [4cd63373be61]
  - EnumType value {success, failure, critical_success, critical_failure} (chunk: 4cd63373be61)

**Epic:** **Player** or **GM** calls for a **Check** when an outcome is uncertain; **System** compares result to **DifficultyClass** and returns a **Degree**. (chunk: 4cd63373be61)
- Triggering-Actor: Player or GM | Responding-Actor: System
- Pre-Condition: Given an action with uncertain outcome is declared; And a **DifficultyClass** or opposing **Defense** is set (chunk: 714405399e02)
- Confirming stories: Make Skill **Check**, Resist **Effect**, Make Opposed **Check**

**Chunk index:** identified: 4cd63373be61, 714405399e02, 6b20869c8bc9 | provisional: 89a1fc58a123

---

## Module: Character | Epic: Build **Character**

**Module:** The aggregate root holding all hero traits and resources — purchased within a Power Point budget constrained by Power Level caps; also owns the hero point pool, complications, and extra effort. (chunk: d4cad3e10e05)

**Concepts:**
- **Character** [foundational] — Owns: whether the sheet is valid — total cost within budget and all Power Level caps met. (chunk: d4cad3e10e05)
  - chunk_ids: [d4cad3e10e05, 792ccb4b72a0]
  - Number power_points_budget, power_level, Dictionary\<String, Trait\> traits, List\<Power\> powers, List\<Complication\> complications, Number hero_point_pool (chunk: d4cad3e10e05)
  - validate() → Boolean, total_cost() → Number, advance(awarded_pp) → void (chunk: d4cad3e10e05)
- **PowerLevel** [foundational] — Owns: the cap on combined attack+effect and defense+resistance pairs. (chunk: d4cad3e10e05)
  - chunk_ids: [d4cad3e10e05]
  - Number rank (chunk: d4cad3e10e05)
  - validate_pair(offensive, defensive) → Boolean (chunk: d4cad3e10e05)
- **HeroPoint** — Owns: what the player can trade it for — re-roll, condition recovery, inspiration, or counter attempt. (chunk: 792ccb4b72a0)
  - chunk_ids: [792ccb4b72a0]
  - spend(use) → void (chunk: 792ccb4b72a0)
- **Complication** — Owns: when invoked, creates a story problem; triggers award of a HeroPoint. (chunk: d4cad3e10e05)
  - chunk_ids: [d4cad3e10e05, 792ccb4b72a0]
  - String description (chunk: d4cad3e10e05)
- **ExtraEffort** `[defer]` — evidence exists (trades fatigue for bonus); full mechanics not yet read. (chunk: 4cd63373be61)

**Epic:** **Player** allocates **PowerPoints** across traits within **PowerLevel** caps; **System** validates the sheet is legal. (chunk: d4cad3e10e05)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **PowerLevel** is set; And **PowerPoints** budget is established (chunk: d4cad3e10e05)
- Confirming stories: Validate **Character** Sheet, Advance **Character**, Spend **HeroPoint**

**Chunk index:** identified: d4cad3e10e05, 792ccb4b72a0, 4cd63373be61 | provisional: 9865e6185ff0

---

## Module: Character Traits | Epic: Configure **Character Traits**

**Module:** The purchased traits that define what a character can do — abilities, defenses, skills, and advantages — all bought from the same Power Point budget, subject to Power Level caps. (chunk: d4cad3e10e05)

**Concepts:**
- **Ability** [foundational] — Owns: the modifier contributed to its associated checks and derived defense values. (chunk: 714405399e02)
  - chunk_ids: [714405399e02]
  - EnumType name {Strength, Stamina, Agility, Dexterity, Fighting, Intellect, Awareness, Presence}, Number rank (chunk: 714405399e02)
  - modifier() → Number (chunk: 714405399e02)
- **Defense** [foundational] — Owns: the difficulty class attackers must beat and whether it is active or impaired. (chunk: 714405399e02)
  - chunk_ids: [714405399e02]
  - EnumType type {Dodge, Parry, Fortitude, Toughness, Will}, Number rank, Boolean is_active (chunk: 714405399e02)
  - defense_class() → Number (chunk: 714405399e02)
- **Skill** — Owns: the trained bonus added to a specific ability check; whether the check can be made untrained. (chunk: 94d3158e4b6b)
  - chunk_ids: [94d3158e4b6b, 89a1fc58a123]
  - String name, Number rank, Ability linked_ability (chunk: 94d3158e4b6b, 89a1fc58a123)
  - bonus() → Number (chunk: 89a1fc58a123)
- **Advantage** — Owns: the specific rule or tradeoff it grants — combat modifier, fortune effect, or general capability. (chunk: 481ffcf3c778)
  - chunk_ids: [481ffcf3c778, 2b979f00a098]
  - EnumType type {combat, fortune, general, skill}, Boolean ranked (chunk: 2b979f00a098)

**Epic:** **Player** purchases **Ability** ranks, **Skills**, and **Advantages** with **PowerPoints**; **System** derives **Defense** values and validates **PowerLevel** compliance. (chunk: 714405399e02)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Character** exists with **PowerLevel** set and **PowerPoints** available (chunk: d4cad3e10e05)
- Confirming stories: Set **Ability** Rank, Train **Skill**, Select **Advantage**

**Chunk index:** identified: 714405399e02, 94d3158e4b6b, 2b979f00a098, 481ffcf3c778 | provisional: 89a1fc58a123

---

## Module: Powers | Epic: Build **Power**

**Module:** The system for defining extraordinary abilities: named Effects purchased at a per-rank cost, adjusted by Extras and Flaws, constrained by PowerLevel caps. (chunk: 2b9b77a24290)

**Concepts:**
- **Power** [foundational] — Owns: the final per-rank cost after extras and flaws, and whether the effect is active. (chunk: 2b9b77a24290)
  - chunk_ids: [2b9b77a24290, 05f80df9e48f]
  - Effect effect, Number rank, List\<Modifier\> extras/flaws, EnumType action/range/duration (chunk: 2b9b77a24290)
  - cost_per_rank() → Number (chunk: 2b9b77a24290), activate() → ActivationResult (chunk: 05f80df9e48f)
- **Effect** [foundational] — Owns: what resistance check type applies, what DC the effect sets, what happens on each degree of failure. (chunk: 2b9b77a24290)
  - chunk_ids: [2b9b77a24290, d4cad3e10e05]
  - Number base_cost_per_rank, EnumType resistance_check {Dodge, Fortitude, Toughness, Will, none} (chunk: 2b9b77a24290)
  - resolve(rank, target) → Degree (chunk: 2b9b77a24290)
  - Effect subtypes `[defer]` — named effects (Affliction, Damage, Healing, etc.) have distinct mechanics; taxonomy deferred to Step 2. (chunk: d4cad3e10e05)
- **Modifier** — Owns: how much it adjusts the effect's cost per rank — adding (Extra) or subtracting (Flaw). (chunk: d4cad3e10e05)
  - chunk_ids: [d4cad3e10e05]
  - EnumType kind {extra, flaw}, Number cost_adjustment, EnumType scope {per_rank, flat} (chunk: d4cad3e10e05)

**Epic:** **Player** selects an **Effect**, sets rank, and applies **Modifiers** to define a **Power** within **PowerPoints** budget and **PowerLevel** caps. (chunk: 2b9b77a24290)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Character** has unspent **PowerPoints**; And **PowerLevel** is set (chunk: d4cad3e10e05)
- Confirming stories: Select and Rank **Effect**, Apply **Extra** to **Effect**, Apply **Flaw** to **Effect**

**Chunk index:** identified: 2b9b77a24290, 05f80df9e48f, d4cad3e10e05 | provisional: 9c7fcc5049c4, 068f6ea2c39b, 7ade13289c0f

---

## Module: Combat | Epic: Resolve Combat Exchange

**Module:** The structured exchange of attacks, defenses, and conditions — initiative, action economy, attack resolution, and condition accumulation. (chunk: 6b20869c8bc9)

**Concepts:**
- **Action** [foundational] — Owns: which type a character can take on their turn and what it can accomplish. (chunk: 6b20869c8bc9)
  - chunk_ids: [6b20869c8bc9]
  - EnumType type {standard, move, free, reaction, none} (chunk: 6b20869c8bc9)
  - is_available(character) → Boolean (chunk: 6b20869c8bc9)
- **Condition** [foundational] — Owns: what actions become unavailable at each severity and how recovery progresses. (chunk: 4cd63373be61)
  - chunk_ids: [4cd63373be61, 714405399e02]
  - EnumType severity {impaired, disabled, staggered, incapacitated, dying, dead}, Number toughness_penalty (chunk: 4cd63373be61, 714405399e02)
  - worsen() → Condition, recover() → Condition (chunk: 4cd63373be61)

**Epic:** **Player** or **GM** declares an **Action** targeting another **Character**; **System** resolves the **Check** sequence and applies the resulting **Condition** or state change. (chunk: 6b20869c8bc9)
- Triggering-Actor: Player or GM | Responding-Actor: System
- Pre-Condition: Given **Character** has an **Action** available this turn; And a valid target exists (chunk: 6b20869c8bc9)
- Confirming stories: Make Attack, Resist Damage, Execute Maneuver

**Chunk index:** identified: 6b20869c8bc9, 086d54227650, 4cd63373be61, 714405399e02 | provisional: 800b98bbc634

---

## Deferred and Uncertain

`[defer]` — ExtraEffort full mechanics. Evidence exists. Needs targeted read in Step 2. chunk: 4cd63373be61

`[defer]` — Activate Effect in play. Power has activate() but full resolution sequence (countering, sustained maintenance, concentration) not fully read. chunk: 05f80df9e48f

`[uncertain]` — Effect subtypes. Named effects (Affliction, Damage, Healing, Move Object, etc.) have distinct mechanics. Subtypes of Effect, or enum? Needs Step 2 targeted reads. chunk: d4cad3e10e05

`[uncertain]` — Equipment and Gear. Devices = Powers with Removable flaw (already in Powers). Pure equipment = Equipment Advantage (already in Character Traits). Likely no separate module — confirm before Step 2.

`[uncertain]` — Gamemastering. NPC creation uses Character rules. Encounter design and series tone are GM guidance, not domain. Likely no module — confirm before Step 2.

---

## Cross-Cutting

`[cross-cutting]` **PowerLevel** — Character (budget owner) + Powers (cap enforcement on effect rank).

`[cross-cutting]` **Resolution** (Check + Degree) — every module depends on it; model first in Step 2.

`[cross-cutting]` **HeroPoint** — Character (pool owner) + Complication (award trigger) + Advantage/Fortune type (spend interaction).

`[cross-cutting]` **Condition** — Combat (applied by damage) + Character Traits/Defense (impairs active defenses) + Character (ExtraEffort fatigue).
