# Domain Concept Guidance (v2 — Evidence-Refined)

## Modules

### Module: Resolution
- concepts — **Check**, **DifficultyClass**, **Degree**, **Modifier**, **OpposedCheck**, **RoutineCheck**

### Module: Character
- concepts — **Hero**, **Ability**, **Rank**, **PowerPoint**, **PowerLevel**, **Complication**, **Motivation**, **Archetype**

### Module: Skills
- concepts — **Skill**, **SkillCheck**, **SkillType**, **InteractionSkill**, **ManipulationSkill**

### Module: Advantages
- concepts — **Advantage**, **CombatAdvantage**, **FortuneAdvantage**, **GeneralAdvantage**, **SkillAdvantage**

### Module: Powers
- concepts — **Power**, **Effect**, **Extra**, **Flaw**, **Descriptor**, **Array**, **AlternateEffect**, **Duration**, **Range**, **AreaShape**

### Module: Attack Effects
- concepts — **Damage**, **Affliction**, **Weaken**, **Nullify**

### Module: Defense Effects
- concepts — **Protection**, **Immunity**, **Regeneration**, **Healing**

### Module: Movement Effects
- concepts — **Flight**, **Speed**, **Teleport**, **Leaping**, **Burrowing**, **Swimming**, **Movement**

### Module: Sensory Effects
- concepts — **Senses**, **Concealment**, **Illusion**, **Communication**, **RemoteSensing**, **Dazzle**

### Module: Control Effects
- concepts — **MindReading**, **MoveObject**, **Transform**, **Summon**, **Variable**

### Module: Combat
- concepts — **Attack**, **AttackCheck**, **Defense**, **DefenseClass**, **Initiative**, **Round**, **Turn**, **Action**, **Maneuver**, **ResistanceCheck**

### Module: Conditions
- concepts — **Condition**, **CombinedCondition**, **ConditionTier**, **DamageResult**

### Module: Resources
- concepts — **HeroPoint**, **ExtraEffort**, **PowerStunt**

### Module: Equipment
- concepts — **Equipment**, **Device**, **Weapon**, **Armor**, **Vehicle**, **Headquarters**, **Feature**

### Module: Entities
- concepts — **Minion**, **Sidekick**, **Construct**

## Concepts (candidate)

**Hero** — possesses **Ability**, **Skill**, **Advantage**, **Power**; constrained by **PowerLevel**
**Ability** — one of eight base attributes (STR, STA, AGL, DEX, FGT, INT, AWE, PRE); contributes to **Check** and **Defense**
**Rank** — numeric measure of any trait; bought with **PowerPoint**
**PowerPoint** — currency spent to acquire all traits
**PowerLevel** — campaign ceiling that caps **Attack**+**Effect** and **Defense**+Toughness at 2×PL
**Skill** — trained capability; adds **Rank** to **SkillCheck** rolls
**InteractionSkill** — **Skill** subtype (Deception, Intimidation, Persuasion) opposed by target's **Insight**
**ManipulationSkill** — **Skill** subtype (Sleight of Hand, Stealth, Technology) involving physical precision
**Advantage** — special capability granting tactical or narrative options; four categories
**Power** — superhuman capability composed of one or more **Effect** plus **Modifier** plus **Descriptor**
**Effect** — base mechanical unit of a **Power** (~30 types); has **Duration**, **Range**, and cost per **Rank**
**Extra** — positive **Modifier** increasing **Effect** cost and capability
**Flaw** — negative **Modifier** decreasing **Effect** cost and capability
**Descriptor** — narrative tag on a **Power** defining source, medium, and counter relationships
**Duration** — temporal scope of an **Effect**: Instant, Concentration, Sustained, Continuous, Permanent
**Range** — spatial scope of an **Effect**: Close, Ranged, Perception
**AreaShape** — shape of area **Effect**: Burst, Cloud, Cone, Line, Shapeable
**Array** — collection of **AlternateEffect** sharing a point budget; only one active at a time
**AlternateEffect** — one option in an **Array**
**Damage** — attack **Effect** inflicting harm; resisted by Toughness **Defense**; cumulative -1 penalty on failure
**Affliction** — attack **Effect** applying **Condition** by **Degree** of failure (3-tier progression)
**Weaken** — attack **Effect** reducing target's trait **Rank** by **Degree** of failure
**Nullify** — **Effect** that suppresses target's **Power** by **Descriptor** match
**Protection** — defensive **Effect** adding to Toughness **Defense**
**Immunity** — defensive **Effect** granting complete immunity to specific **Effect** or **Descriptor**
**Healing** — **Effect** removing **Damage** **Condition** from target
**Regeneration** — **Effect** granting periodic automatic recovery from **Damage**
**Check** — d20 + modifier roll against **DifficultyClass**
**DifficultyClass** — target number for a **Check**; typically **Rank** + 10 or **Rank** + 15
**Degree** — unit of success/failure; each 5 points over/under **DifficultyClass** = 1 **Degree**
**OpposedCheck** — two competing **Check** results compared; higher wins
**RoutineCheck** — automatic success when **Rank** ≥ DC-10 and no stress
**AttackCheck** — **Check** to hit target (d20 + attack bonus vs **DefenseClass**)
**ResistanceCheck** — **Check** to resist **Effect** (d20 + **Defense** vs effect DC)
**DefenseClass** — **Defense** + 10; target number for **AttackCheck**
**Attack** — offensive interaction; Close or Ranged **AttackCheck** against target
**Defense** — five defensive traits: Dodge, Parry, Fortitude, Toughness, Will
**Condition** — status effect applied to **Hero** (27 basic types); severity tiers
**CombinedCondition** — compound **Condition**: Asleep, Bound, Dying, Incapacitated, etc.
**ConditionTier** — severity progression: Impaired→Disabled→Debilitated; Dazed→Stunned→Incapacitated
**DamageResult** — outcome ladder from Toughness failure: -1 penalty → Dazed → Staggered → Incapacitated
**Action** — Standard, Move, Free, Reaction; consumed during a **Turn**
**Round** — ~6 seconds of game time containing all **Turn** in **Initiative** order
**Turn** — one character's **Action** within a **Round**
**Initiative** — determines **Turn** order (d20 + Agility + modifiers)
**Maneuver** — tactical option: Aim, Charge, Grab, Trip, Disarm, Slam, Defend, etc.
**HeroPoint** — meta-resource earned from **Complication**; spent on re-rolls, stunts, recovery
**ExtraEffort** — temporary boost at cost of Fatigued **Condition**
**PowerStunt** — temporary **AlternateEffect** gained via **HeroPoint** or **ExtraEffort**
**Equipment** — mundane gear; 5 equipment points per **Rank** of Equipment **Advantage**
**Device** — **Power** with Removable **Flaw**; can be taken away
**Weapon** — **Equipment** or **Device** dealing **Damage**
**Armor** — **Equipment** or **Device** providing **Protection**
**Vehicle** — mobile platform with Size, Speed, Toughness, **Defense**
**Headquarters** — base with **Feature** (Communications, Lab, Security, etc.)
**Feature** — individual capability of **Headquarters** or minor **Power** benefit
**Minion** — subordinate entity; incapacitated on any failed **ResistanceCheck**
**Sidekick** — advanced **Minion** with full trait progression
**Construct** — entity without Stamina; immune to Fortitude; special **Damage** rules
**Complication** — narrative hook triggered by **Gamemaster**; awards **HeroPoint**
**Motivation** — drive for heroism; subtype of **Complication**
**Archetype** — pre-built **Hero** template (20 types)
**Modifier** — **Extra** or **Flaw** applied to an **Effect**

## Mechanisms (likely)

- **Check Resolution** — d20 + modifier vs DC; **Degree** of success/failure determine outcome severity
- **Power Construction** — combine base **Effect** + **Extra**/**Flaw** + **Descriptor**; cost = (base + extras - flaws) per **Rank**
- **Damage Escalation** — cumulative -1 Toughness penalty per failed **ResistanceCheck**; **Condition** worsen across **Degree**
- **Condition Progression** — three-tier severity: Impaired→Disabled→Debilitated; Dazed→Stunned→Incapacitated; "becomes" transitions
- **Affliction Resolution** — attacker's **Effect** **Rank** sets DC; target resists with specified **Defense**; each **Degree** of failure applies next **ConditionTier**
- **Array Switching** — only one **AlternateEffect** active; switching costs Free **Action**
- **Power Level Capping** — **Attack** + **Effect** ≤ 2×PL; **Defense** + Toughness ≤ 2×PL; **Skill** + **Ability** ≤ 2×PL
- **Hero Point Economy** — earned from **Complication** activation by **Gamemaster**; spent on re-rolls, **PowerStunt**, recovery, counters
- **Extra Effort / Fatigue** — gain immediate benefit (boost, stunt, extra **Action**); become Fatigued after **Round** ends
- **Counter Matching** — oppose an **Effect** using same or opposed **Descriptor**; requires ready **Action** + **Check**
- **Resistance Cascade** — **Effect** hits → target rolls **ResistanceCheck** → **Degree** determines **Condition** → **Condition** may escalate on subsequent hits

## Actors (likely)

- **Hero** — player-controlled protagonist; primary actor in all interactions
- **Gamemaster** — rules arbiter, narrator, controls setting and triggers **Complication**
- **Villain** — antagonist character; GM-controlled; same trait structure as **Hero**
- **Minion** — subordinate entity; simplified rules (one-hit defeat)
- **Construct** — non-living entity; no Stamina; immune to Fortitude effects

## Extraction Guidance

### Priority Concepts
- **Check**, **Effect**, **Power**, **Defense**, **Condition**
- **Damage**, **Affliction**, **Rank**, **Hero**, **Attack**
- **HeroPoint**, **Array**, **Modifier**, **Duration**, **Range**

### Priority Mechanisms
- **Check Resolution**, **Power Construction**, **Damage Escalation**
- **Condition Progression**, **Affliction Resolution**, **Power Level Capping**
- **Resistance Cascade**, **Hero Point Economy**

### Variation Axes
- Effect type (Attack / Defense / Movement / Sensory / Control / General)
- Duration (Instant / Concentration / Sustained / Continuous / Permanent)
- Range (Close / Ranged / Perception)
- Area shape (Burst / Cloud / Cone / Line / Shapeable)
- Condition severity tier (3-level progression)
- Descriptor source (Mutant / Magic / Technology / Cosmic / Divine / Psionic)
- Attack type (Close / Ranged / Perception / Area)
- Advantage category (Combat / Fortune / General / Skill)
- Equipment vs Device vs Innate Power
- Skill type (Interaction / Manipulation / Combat / General)

### Synonym Hints
- **Check**: roll, test, check result
- **DifficultyClass**: DC, target number, difficulty
- **Hero**: character, PC, player character
- **Rank**: level, rating, score
- **Effect**: power effect, base effect
- **Condition**: status, status effect
- **HeroPoint**: hero point
- **PowerPoint**: power point, PP, character point
- **Modifier**: extra, flaw
- **Defense**: dodge, parry, fortitude, toughness, will
- **Damage**: harm, injury, damage effect
- **Affliction**: affliction effect, condition attack
- **Maneuver**: combat maneuver, tactical action
- **Equipment**: gear, item
- **Device**: removable power, gadget
