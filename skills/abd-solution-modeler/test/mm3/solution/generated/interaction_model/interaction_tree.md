# Interaction Tree — Mutants & Masterminds 3e (Phase 10: Refined Domain Model)

# Epic: Build **Hero** (Assemble playable **Hero** from **PowerPoint** within **PowerLevel**)
- Triggering-Actor: **Player**
- Responding-Actor: **System**
- Pre-Condition: **PowerLevel** set; **PowerPoint**.total = 15 × **PowerLevel**.level
- Resulting-State: **Hero** built and valid within **PowerLevel** caps

## Epic: Assign **Ability** **Rank**

### Story: Purchase **Ability** **Rank** (Spend **PowerPoint** at 2 PP per **Rank**)
- Trigger: **Player** selects **AbilityType** and desired **Rank**
- Response: **Ability**.rank set; **PowerPoint** allocated
- Failure-Modes: Insufficient **PowerPoint**; total exceeds **PowerLevel** cap
- Step 1: When **Player** selects **AbilityType** and **Rank**; Then **Ability**.cost() = rank × 2
- Step 2: When **PowerPoint**.allocate(cost); Then **Ability**.rank set
- Step 3: When all eight set; Then validate total spent

Ability (purchase):
| scenario | ability_type | rank | cost | remaining_pp |
|----------|-------------|------|------|-------------|
| buy-strength-4 | strength | 4 | 8 | 142 |
| buy-stamina-2 | stamina | 2 | 4 | 138 |
===

### Story: Handle Debilitated **Ability** (Resolve when **Rank** < -5)
- Trigger: **Ability**.rank drops below -5
- Response: Type-specific penalties applied
- Failure-Modes: None (automatic system response)

#### Scenario: Debilitated Physical
- Step 1: When **Ability**.is_debilitated() for Strength; Then **Hero** collapses
- Step 2: When **Ability**.is_debilitated() for Stamina; Then **Hero** gains Dying **CombinedCondition**
- Step 3: When **Ability**.is_debilitated() for Agility; Then **Hero** gains Immobile **Condition**

#### Scenario: Debilitated Mental
- Step 1: When **Ability**.is_debilitated() for Intellect/Awareness/Presence; Then **Hero** gains Unaware **Condition**

## Epic: Construct **Power**

### Story: Select Base **Effect** (Choose **EffectType** and base cost)
- Trigger: **Player** chooses **EffectType**
- Response: **Effect** created with type-specific defaults
### Story: Apply **Extra** (Increase cost/capability)
### Story: Apply **Flaw** (Decrease cost)
### Story: Assign **Descriptor**
### Story: Build **Array** (Group **AlternateEffect**)
### Story: Validate **PowerLevel** Cap

## Epic: Acquire **Skill**
### Story: Purchase **Skill** **Rank**
### Story: Perform Trained **SkillCheck**

## Epic: Select **Advantage**
### Story: Purchase **Advantage**

## Epic: Define Background
### Story: Select **Motivation**
### Story: Add **Complication**
### Story: Allocate **Defense** **Rank**

---

# Epic: Resolve **Check** (Determine outcome of d20 **Check** vs **DifficultyClass**)
- Triggering-Actor: **Hero**
- Responding-Actor: **System**
- Pre-Condition: **Hero** has relevant trait **Rank**
- Resulting-State: **Degree** determined

## Epic: Perform Standard **Check**

### Story: Resolve Basic **Check** (d20 + modifier vs DC)
- Trigger: **Hero** attempts uncertain action
- Response: **Degree** determined
- Failure-Modes: Natural 1 is not auto-fail (just low result)
- Step 1: When **Hero** initiates; Then **Check** created with modifier
- Step 2: When **Check**.roll(); Then result = d20 + modifier
- Step 3: When **Check**.resolve(); Then **Degree** = margin / 5
- Step 4: When **Degree**.success; Then action succeeds with degree count

Check (basic resolution):
| scenario | modifier | d20_roll | result | dc | margin | degrees | success |
|----------|----------|----------|--------|-----|--------|---------|---------|
| easy-pass | +8 | 12 | 20 | 15 | +5 | 1 | true |
| hard-pass | +8 | 14 | 22 | 20 | +2 | 0 | true |
| close-fail | +8 | 6 | 14 | 15 | -1 | 0 | false |
| bad-fail | +8 | 3 | 11 | 25 | -14 | 2 | false |
===

### Story: Perform **OpposedCheck**
- Trigger: Two actors compete
- Response: Higher margin wins
- Failure-Modes: Both tied → defender wins

### Story: Apply Critical Hit (Natural 20 → +5 DC)
- Trigger: **AttackCheck** roll = natural 20
- Response: target **ResistanceCheck** DC += 5
- Constraint: only on **AttackCheck**, not other **Check** types

## Epic: Perform **SkillCheck**
### Story: Perform Interaction **SkillCheck**
### Story: Perform Perception **Check**
### Story: Perform Close Combat **SkillCheck**
### Story: Perform Ranged Combat **SkillCheck**

---

# Epic: Execute Combat **Round**
- Triggering-Actor: **Gamemaster**
- Responding-Actor: **System**
- Pre-Condition: Combat initiated
- Resulting-State: All **Turn** resolved

## Epic: Determine **Initiative**
### Story: Roll **Initiative** (d20 + Agility for **Turn** order)
### Story: Delay **Turn**
### Story: Ready **Action**

## Epic: Perform **Attack**
- Triggering-Actor: **Hero**
- Responding-Actor: target **Hero**
- Pre-Condition: **Action** available; target in range

### Story: Perform Close **Attack** (vs Parry **DefenseClass**)
- Trigger: **Hero** declares close **Attack** on adjacent target
- Response: **AttackCheck** resolves; on hit **Effect** applied
- Failure-Modes: Miss (result < DefenseClass); target out of reach
- Step 1: When declares; Then **Attack**.calculate_bonus() = fighting + close_combat
- Step 2: When **Attack**.check(target.parry); Then d20 + bonus vs Parry + 10
- Step 3: When hit; Then **Effect** applied
- Step 4: When natural 20; Then critical: DC += 5

AttackCheck (close):
| scenario | attack_bonus | d20_roll | result | parry_dc | hit |
|----------|-------------|----------|--------|----------|-----|
| solid-hit | +10 | 14 | 24 | 20 | true |
| near-miss | +10 | 9 | 19 | 20 | false |
| critical | +10 | 20 | 30 | 20 | true (+5 DC) |
===

### Story: Perform Ranged **Attack** (vs Dodge **DefenseClass**)
- Trigger: **Hero** declares ranged **Attack**
- Response: **AttackCheck** vs Dodge + 10
- Failure-Modes: Miss; target beyond range; no line of sight

### Story: Perform Area **Attack** (**ResistanceCheck** for all in area)
- Trigger: **Hero** uses area **Effect**
- Response: All targets Dodge for half; then **ResistanceCheck**
- Failure-Modes: No targets in area

#### Scenario: Targets Dodge for Half
- Step 1: When area **Effect** used; Then all targets make Dodge **Check** vs DC
- Step 2: When Dodge succeeds; Then **Effect** rank halved for that target
- Step 3: When Dodge fails; Then full **Effect** rank applied

### Story: Perform Perception **Attack** (Auto-hit)
- Trigger: Perception **Range** **Effect** used
- Response: No **AttackCheck**; direct to **ResistanceCheck**
- Constraint: **Hero** must perceive target

### Story: Resolve Multiattack

## Epic: Resist **Effect**
- Triggering-Actor: **System**
- Responding-Actor: target **Hero**

### Story: Resist **Damage** (**Toughness** vs DC **Rank** + 15)
- Trigger: **Damage** hits target
- Response: **DamageResult** applied based on **Degree** of failure
- Failure-Modes: Cumulative penalty makes subsequent checks harder
- Step 1: When **Damage** hits; Then DC = rank + 15 + toughness_penalty
- Step 2: When target rolls d20 + Toughness vs DC
- Step 3: When 1° failure; Then -1 penalty only
- Step 4: When 2° failure; Then Dazed + -1 penalty
- Step 5: When 3° failure; Then Staggered (Dazed + Hindered)
- Step 6: When 4°+ failure; Then Incapacitated

DamageResult (damage resistance):
| scenario | damage_rank | toughness | penalty | d20 | result | dc | margin | condition |
|----------|------------|-----------|---------|-----|--------|-----|--------|-----------|
| shrug-off | 8 | 10 | 0 | 15 | 25 | 23 | +2 | none |
| bruised | 8 | 10 | 0 | 10 | 20 | 23 | -3 | -1 penalty |
| dazed-hit | 8 | 10 | -1 | 8 | 17 | 23 | -6 | dazed + -1 |
| staggered | 8 | 10 | -2 | 4 | 12 | 23 | -11 | staggered |
| knockout | 8 | 10 | -3 | 2 | 9 | 23 | -14 | incapacitated |
===

### Story: Resist **Affliction** (**Defense** vs DC **Rank** + 10)
- Trigger: **Affliction** hits target
- Response: **Condition** applied by **Degree** of failure
- Failure-Modes: 3rd degree may be permanent until resisted

#### Scenario: Progressive Affliction
- Step 1: When **Affliction** hits; Then DC = rank + 10
- Step 2: When 1° failure; Then first_degree **Condition** applied
- Step 3: When 2° failure; Then second_degree **Condition** replaces first
- Step 4: When 3° failure; Then third_degree **Condition** replaces second

Affliction (example: Daze/Stun/Incapacitate):
| scenario | affliction_rank | defense | d20 | result | dc | degree | condition |
|----------|----------------|---------|-----|--------|----|--------|-----------|
| resist | 8 | 10 | 12 | 22 | 18 | success | none |
| dazed | 8 | 10 | 5 | 15 | 18 | 1° fail | dazed |
| stunned | 8 | 10 | 2 | 12 | 18 | 2° fail | stunned |
| incapacitated | 8 | 10 | 1 | 11 | 18 | 3° fail | incapacitated |
===

### Story: Resist **Weaken** (Lose **Rank** per **Degree**)
### Story: Resist **Nullify** (Maintain or lose **Power**)

## Epic: Execute **Maneuver**

### Story: Grab Target (Restrain via **OpposedCheck**)
- Trigger: **Hero** declares Grab on adjacent target
- Response: **OpposedCheck** determines grapple
- Failure-Modes: Target escapes; attacker lacks free hand

#### Scenario: Successful Grab
- Step 1: When attacker rolls Strength **Check**; Then result determined
- Step 2: When target rolls Dodge or Strength **Check**; Then compared
- Step 3: When attacker wins; Then target gains Restrained **Condition**
- Step 4: When attacker maintains next **Round**; Then sustained

#### Scenario: Target Escapes
- Step 1: When target's **Check** exceeds attacker's; Then Grab fails
- Step 2: When already restrained target wins; Then Restrained **Condition** removed

### Story: Aim at Target
### Story: Trip Target
### Story: Disarm Target
### Story: Charge Target
### Story: Slam Target
### Story: Interpose for Ally
### Story: Perform Team **Attack**
### Story: Defend (+2 active **Defense**)

---

# Epic: Manage **Condition**

## Epic: Apply **Condition**
### Story: Apply Basic **Condition**
### Story: Apply **CombinedCondition**
### Story: Escalate via **ConditionTier**
### Story: Apply **DamageResult**

## Epic: Recover from **Condition**

### Story: Recover from **Damage** (Recovery **Check** DC 10)
- Trigger: **Hero** spends standard **Action** for recovery
- Response: d20 + Toughness vs DC 10
- Failure-Modes: Failure means Condition persists; **Hero** loses **Action**

#### Scenario: Successful Recovery
- Step 1: When **Hero** rolls recovery; Then d20 + Toughness vs DC 10
- Step 2: When success; Then toughness_penalty reduced; worst **Condition** removed

#### Scenario: Failed Recovery
- Step 1: When recovery fails; Then **Condition** persists
- Step 2: When **Hero** has no **Condition** worse than penalty; Then recovery removes -1 penalty only

### Story: Stabilize Dying **Hero**
- Trigger: **Hero** has Dying **CombinedCondition**
- Response: Fortitude **Check** DC 10 or **HeroPoint**
- Failure-Modes: Continued failure → death at GM discretion

---

# Epic: Spend **HeroPoint**
- Triggering-Actor: **Hero**
- Pre-Condition: **HeroPoint**.available ≥ 1

### Story: Re-roll **Check** (Min result 11)
- Trigger: **Hero** unhappy with **Check** result
- Response: New roll; minimum 11 enforced
- Constraint: 1 re-roll per **Check**

HeroPoint (reroll):
| scenario | original_roll | reroll | min_applied | final |
|----------|--------------|--------|-------------|-------|
| low-reroll | 5 | 8 | 11 | 11 |
| good-reroll | 5 | 16 | no | 16 |
===

### Story: Perform **PowerStunt** via **HeroPoint**
### Story: Recover from **Condition** via **HeroPoint**
### Story: Gain Inspiration **Advantage**
### Story: Counter **Effect** Instantly
### Story: Edit Scene

---

# Epic: Activate **ExtraEffort**
- Pre-Condition: **Hero** not Exhausted

### Story: Boost **Power** **Rank** (+1 for one use)
### Story: Gain Extra **Action**
### Story: Perform **PowerStunt** via **ExtraEffort**
### Story: Suffer Fatigue (Fatigued → Exhausted → Incapacitated)
- Trigger: **Round** ends after **ExtraEffort**
- Response: **ExtraEffort**.apply_fatigue() escalates fatigue
- Failure-Modes: Already Exhausted → Incapacitated

ExtraEffort (fatigue escalation):
| scenario | current_condition | after_effort |
|----------|------------------|-------------|
| fresh | none | fatigued |
| already-tired | fatigued | exhausted |
| pushed-limit | exhausted | incapacitated |
===

---

# Epic: Use **Equipment** and **Device**

## Epic: Equip Combat Gear
### Story: Equip Melee **Weapon**
### Story: Equip Ranged **Weapon**
### Story: Equip **Armor**
### Story: Use **Device** **Power**
### Story: Lose **Device**

## Epic: Operate **Vehicle**
### Story: Drive **Vehicle**
### Story: Attack from **Vehicle**

## Epic: Manage **Headquarters**
### Story: Use **Feature**

---

# Epic: Counter and **Nullify** **Power**
### Story: Counter Incoming **Effect**
### Story: **Nullify** Active **Effect**
### Story: Resist **Nullify**

---

# Epic: Command **Minion** and **Sidekick**

### Story: Defeat **Minion** (Any failure = Incapacitated)
- Trigger: **Minion** fails any **ResistanceCheck**
- Response: Immediately Incapacitated (no Degrees)
- Constraint: **Minion** rule only; **Sidekick** uses normal Degree rules

Minion (defeat):
| scenario | resistance_check | result | dc | outcome |
|----------|-----------------|--------|-----|---------|
| minion-hit | toughness | 14 | 18 | incapacitated |
| hero-same | toughness | 14 | 18 | -1 penalty (1° fail) |
===

### Story: Summon **Minion**
### Story: Direct **Sidekick**
### Story: Handle **Construct** **Damage**

---

# Epic: Earn and Activate **Complication**

### Story: Trigger **Complication** (**Gamemaster** activates for **HeroPoint**)
- Trigger: **Gamemaster** decides **Complication** relevant to scene
- Response: **Complication**.trigger() → **Hero**.hero_points += 1
- Failure-Modes: **Hero** may reject (loses **HeroPoint** opportunity)
### Story: Advance **Hero** (Spend earned **PowerPoint**)
### Story: Raise **PowerLevel**
