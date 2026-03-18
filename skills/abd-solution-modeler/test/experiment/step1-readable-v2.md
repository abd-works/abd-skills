# Step 1 — Modules and Epics (v2 Output)

---

## Module: Resolution | Epic: Resolve **Check**

**Module:** The single mechanic that resolves all uncertain outcomes: roll d20, add modifier, compare to DC; degree of success or failure determines what happens next. (chunk: 4cd63373be61)

**Concepts:**
- **Check** [foundational] — Owns: whether an action succeeds or fails and by how much. (chunk: 4cd63373be61)
  - Number modifier (chunk: 714405399e02)
  - Number difficulty_class (chunk: 714405399e02)
  - resolve() → Degree (chunk: 4cd63373be61)
- **Degree** [foundational] — Owns: how far above or below DC a result landed — drives what consequence applies. (chunk: 4cd63373be61)
  - EnumType value {success, failure, critical_success, critical_failure} (chunk: 4cd63373be61)

**Epic:** **Player** or **GM** calls for a **Check** when an outcome is uncertain; **System** compares result to **DifficultyClass** and returns a **Degree**. (chunk: 4cd63373be61)
- Triggering-Actor: Player or GM | Responding-Actor: System
- Pre-Condition: Given an action with uncertain outcome is declared; And a **DifficultyClass** or opposing **Defense** is set (chunk: 714405399e02)

**Stories:**
- Make Skill **Check** (chunk: 89a1fc58a123) — **Player** declares skill action → **System** returns **Degree**
- Resist **Effect** (chunk: 714405399e02) — **System** triggers resistance **Check** → **System** applies **Condition** per **Degree** of failure
- Make Opposed **Check** (chunk: 6b20869c8bc9) — **Player** rolls against another **Character** → **System** returns winner by margin

**Chunk index:** identified: 4cd63373be61, 714405399e02, 6b20869c8bc9 | provisional: 89a1fc58a123

---

## Module: Character | Epic: Build **Character**

**Module:** The aggregate root holding all hero traits and resources — purchased within a Power Point budget constrained by Power Level caps; also owns the hero point pool, complications, and extra effort. (chunk: d4cad3e10e05)

**Concepts:**
- **Character** [foundational] — Owns: whether the sheet is valid — total cost within budget and all Power Level caps met. (chunk: d4cad3e10e05)
  - Number power_points_budget (chunk: d4cad3e10e05)
  - Number power_level (chunk: d4cad3e10e05)
  - Dictionary\<String, Trait\> traits (chunk: d4cad3e10e05)
  - List\<Power\> powers (chunk: d4cad3e10e05)
  - List\<Complication\> complications (chunk: d4cad3e10e05)
  - Number hero_point_pool (chunk: 792ccb4b72a0)
  - validate() → Boolean (chunk: d4cad3e10e05)
  - total_cost() → Number (chunk: d4cad3e10e05)
  - advance(awarded_pp) → void (chunk: d4cad3e10e05)
- **PowerLevel** [foundational] — Owns: the cap on combined attack+effect and defense+resistance pairs. (chunk: d4cad3e10e05)
  - Number rank (chunk: d4cad3e10e05)
  - validate_pair(offensive, defensive) → Boolean (chunk: d4cad3e10e05)
- **HeroPoint** — Owns: what the player can trade it for — re-roll, condition recovery, inspiration, or counter attempt. (chunk: 792ccb4b72a0)
  - spend(use) → void (chunk: 792ccb4b72a0)
- **Complication** — Owns: when invoked, creates a story problem; triggers award of a HeroPoint. (chunk: d4cad3e10e05)
  - String description (chunk: d4cad3e10e05)
- **ExtraEffort** `[defer]` — evidence exists (trades fatigue for bonus); full mechanics not yet read. (chunk: 4cd63373be61)

**Epic:** **Player** allocates **PowerPoints** across traits within **PowerLevel** caps; **System** validates the sheet is legal. (chunk: d4cad3e10e05)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **PowerLevel** is set; And **PowerPoints** budget is established (chunk: d4cad3e10e05)

**Stories:**
- Select **Complication** (chunk: d4cad3e10e05) — **Player** chooses **Complications** → **System** records; no PP cost
- Validate **Character** Sheet (chunk: d4cad3e10e05) — **Player** submits sheet → **System** checks cost and **PowerLevel** caps; returns valid or violations
- Advance **Character** (chunk: d4cad3e10e05) — **Player** spends awarded **PowerPoints** → **System** applies costs and revalidates caps
- Spend **HeroPoint** (chunk: 792ccb4b72a0) — **Player** spends **HeroPoint** → **System** applies re-roll, recovery, inspiration, or counter
- Earn **HeroPoint** from **Complication** (chunk: 792ccb4b72a0) — **GM** invokes **Complication** → **System** awards one **HeroPoint**
- Use Extra Effort `[defer]` (chunk: 4cd63373be61) — **Player** declares extra effort → full mechanics deferred to Step 2

**Chunk index:** identified: d4cad3e10e05, 792ccb4b72a0, 4cd63373be61 | provisional: 9865e6185ff0

---

## Module: Character Traits | Epic: Configure **Character Traits**

**Module:** The purchased traits that define what a character can do — abilities, defenses, skills, and advantages — all bought from the same Power Point budget, subject to Power Level caps. (chunk: d4cad3e10e05)

**Concepts:**
- **Ability** [foundational] — Owns: the modifier contributed to its associated checks and derived defense values. (chunk: 714405399e02)
  - EnumType name {Strength, Stamina, Agility, Dexterity, Fighting, Intellect, Awareness, Presence} (chunk: 714405399e02)
  - Number rank (chunk: 714405399e02)
  - modifier() → Number (chunk: 714405399e02)
- **Defense** [foundational] — Owns: the difficulty class attackers must beat and whether it is active or impaired. (chunk: 714405399e02)
  - EnumType type {Dodge, Parry, Fortitude, Toughness, Will} (chunk: 714405399e02)
  - Number rank (chunk: 714405399e02)
  - Boolean is_active (chunk: 714405399e02)
  - defense_class() → Number (chunk: 714405399e02)
- **Skill** — Owns: the trained bonus added to a specific ability check; whether the check can be made untrained. (chunk: 94d3158e4b6b)
  - String name (chunk: 94d3158e4b6b)
  - Number rank (chunk: 94d3158e4b6b)
  - Ability linked_ability (chunk: 89a1fc58a123)
  - bonus() → Number (chunk: 89a1fc58a123)
- **Advantage** — Owns: the specific rule or tradeoff it grants — combat modifier, fortune effect, or general capability. (chunk: 481ffcf3c778)
  - EnumType type {combat, fortune, general, skill} (chunk: 2b979f00a098)
  - Boolean ranked (chunk: 2b979f00a098)

**Epic:** **Player** purchases **Ability** ranks, **Skills**, and **Advantages** with **PowerPoints**; **System** derives **Defense** values and validates **PowerLevel** compliance. (chunk: 714405399e02)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Character** exists with **PowerLevel** set and **PowerPoints** available (chunk: d4cad3e10e05)

**Stories:**
- Set **Ability** Rank (chunk: 714405399e02) — **Player** assigns rank to **Ability** → **System** deducts cost and recalculates derived **Defense** values
- Train **Skill** (chunk: 94d3158e4b6b) — **Player** spends **PowerPoints** on **Skill** ranks → **System** records rank and adds to linked **Ability** modifier
- Select **Advantage** (chunk: 2b979f00a098) — **Player** picks an **Advantage** → **System** records it and applies the rule or tradeoff
- Apply **Condition** to **Defense** (chunk: 714405399e02) — **Character** gains Vulnerable or Defenseless → **System** halves active **Defense** or sets to 0

**Chunk index:** identified: 714405399e02, 94d3158e4b6b, 2b979f00a098, 481ffcf3c778 | provisional: 89a1fc58a123

---

## Module: Powers | Epic: Build **Power**

**Module:** The system for defining extraordinary abilities: named Effects purchased at a per-rank cost, adjusted by Extras and Flaws, constrained by PowerLevel caps. (chunk: 2b9b77a24290)

**Concepts:**
- **Power** [foundational] — Owns: the final per-rank cost after extras and flaws, and whether the effect is active. (chunk: 2b9b77a24290)
  - Effect effect (chunk: 2b9b77a24290)
  - Number rank (chunk: 2b9b77a24290)
  - List\<Modifier\> extras (chunk: d4cad3e10e05)
  - List\<Modifier\> flaws (chunk: d4cad3e10e05)
  - EnumType action {standard, move, free, reaction, none} (chunk: 2b9b77a24290)
  - EnumType range {personal, close, ranged, perception} (chunk: 2b9b77a24290)
  - EnumType duration {instant, concentration, sustained, continuous, permanent} (chunk: 2b9b77a24290)
  - cost_per_rank() → Number (chunk: 2b9b77a24290)
  - activate() → ActivationResult (chunk: 05f80df9e48f)
- **Effect** [foundational] — Owns: what resistance check type applies, what DC the effect sets, what happens on each degree of failure. (chunk: 2b9b77a24290)
  - Number base_cost_per_rank (chunk: 2b9b77a24290)
  - EnumType resistance_check {Dodge, Fortitude, Toughness, Will, none} (chunk: 2b9b77a24290)
  - resolve(rank, target) → Degree (chunk: 2b9b77a24290)
  - Effect subtypes `[defer]` — named effects (Affliction, Damage, Healing, etc.) have distinct mechanics; taxonomy deferred to Step 2. (chunk: d4cad3e10e05)
- **Modifier** — Owns: how much it adjusts the effect's cost per rank — adding (Extra) or subtracting (Flaw). (chunk: d4cad3e10e05)
  - EnumType kind {extra, flaw} (chunk: d4cad3e10e05)
  - Number cost_adjustment (chunk: d4cad3e10e05)
  - EnumType scope {per_rank, flat} (chunk: d4cad3e10e05)

**Epic:** **Player** selects an **Effect**, sets rank, and applies **Modifiers** to define a **Power** within **PowerPoints** budget and **PowerLevel** caps. (chunk: 2b9b77a24290)
- Triggering-Actor: Player | Responding-Actor: System
- Pre-Condition: Given **Character** has unspent **PowerPoints**; And **PowerLevel** is set (chunk: d4cad3e10e05)

**Stories:**
- Select and Rank **Effect** (chunk: 2b9b77a24290) — **Player** chooses **Effect** and rank → **System** calculates cost and validates **PowerLevel** cap
- Apply **Extra** to **Effect** (chunk: d4cad3e10e05) — **Player** adds **Extra** → **System** increases cost per rank
- Apply **Flaw** to **Effect** (chunk: d4cad3e10e05) — **Player** adds **Flaw** → **System** reduces cost per rank (minimum 1)
- Build **Power** Array (chunk: d4cad3e10e05) — **Player** groups **Effects** under shared base → **System** prices base at highest cost; alternates at 1PP
- Activate **Effect** in Play `[defer]` (chunk: 05f80df9e48f) — **Character** uses **Power** in scene → full resolution mechanics deferred to Step 2

**Chunk index:** identified: 2b9b77a24290, 05f80df9e48f, d4cad3e10e05 | provisional: 9c7fcc5049c4, 068f6ea2c39b, 7ade13289c0f

---

## Module: Combat | Epic: Resolve Combat Exchange

**Module:** The structured exchange of attacks, defenses, and conditions — initiative, action economy, attack resolution, and condition accumulation. (chunk: 6b20869c8bc9)

**Concepts:**
- **Action** [foundational] — Owns: which type a character can take on their turn and what it can accomplish. (chunk: 6b20869c8bc9)
  - EnumType type {standard, move, free, reaction, none} (chunk: 6b20869c8bc9)
  - is_available(character) → Boolean (chunk: 6b20869c8bc9)
- **Condition** [foundational] — Owns: what actions become unavailable at each severity and how recovery progresses. (chunk: 4cd63373be61)
  - EnumType severity {impaired, disabled, staggered, incapacitated, dying, dead} (chunk: 4cd63373be61)
  - Number toughness_penalty (chunk: 714405399e02)
  - worsen() → Condition (chunk: 4cd63373be61)
  - recover() → Condition (chunk: 4cd63373be61)

**Epic:** **Player** or **GM** declares an **Action** targeting another **Character**; **System** resolves the **Check** sequence and applies the resulting **Condition** or state change. (chunk: 6b20869c8bc9)
- Triggering-Actor: Player or GM | Responding-Actor: System
- Pre-Condition: Given **Character** has an **Action** available this turn; And a valid target exists (chunk: 6b20869c8bc9)

**Stories:**
- Make Attack (chunk: 6b20869c8bc9) — **Player** declares attack **Action**, rolls **Check** → **System** compares to **Defense** class; if hit, triggers resistance **Check**
- Resist Damage (chunk: 714405399e02) — **System** triggers Toughness **Check** against **Effect** DC → **System** applies **Condition** per **Degree** of failure
- Execute Maneuver (chunk: 086d54227650) — **Player** declares combat maneuver with attack → **System** applies tradeoff before resolving **Check**
- Recover from **Condition** (chunk: 4cd63373be61) — **Player** takes Recover **Action** or rests → **System** removes one **Condition** step

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
