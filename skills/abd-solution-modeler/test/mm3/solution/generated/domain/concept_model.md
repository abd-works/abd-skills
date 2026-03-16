# Concept Model — Mutants & Masterminds 3rd Edition

## Module: Resolution

**Check**
- Number modifier
      Invariant: modifier = trait rank + circumstance modifiers
- Number result
      Invariant: result = d20 roll + modifier
- resolve(DifficultyClass) → Degree
      DifficultyClass
      Invariant: result ≥ DC = success; each 5 over/under = 1 Degree
- Interactions: Resolve Check, Perform SkillCheck, Perform AttackCheck, Resist Effect

**DifficultyClass**
- Number value
      Invariant: value ≥ 0
- Interactions: Resolve Check, Resist Effect

**Degree**
- Number margin
      Invariant: margin = check result - DC
- Number degrees
      Invariant: degrees = floor(abs(margin) / 5); minimum 1 on any success/failure
- Boolean success
      Invariant: success = (margin ≥ 0)
- Interactions: Calculate Degree, Resist Damage, Resist Affliction

**OpposedCheck**
- Check attacker_check
      Check
- Check defender_check
      Check
- resolve() → Degree
      Invariant: higher result wins; ties go to defender
- Interactions: Resolve OpposedCheck, Trip Target, Disarm Target, Grab Target

**RoutineCheck**
- Check base_check
      Check
- Boolean qualifies
      Invariant: qualifies = (rank + 10 ≥ DC) AND no stress/threat
- resolve(DifficultyClass) → Number
      Invariant: result = rank + 10 (no roll)
- Interactions: Perform RoutineCheck

## Module: Character

**Hero**
- String name
- List<Ability> abilities
      Ability
      Invariant: exactly 8 abilities
- List<Skill> skills
      Skill
- List<Advantage> advantages
      Advantage
- List<Power> powers
      Power
- List<Defense> defenses
      Defense
      Invariant: exactly 5 defenses (Dodge, Parry, Fortitude, Toughness, Will)
- Number power_points_spent
      PowerPoint
      Invariant: power_points_spent ≤ power_points_total
- PowerLevel power_level
      PowerLevel
- List<Complication> complications
      Complication
      Invariant: at least 2 complications (including Motivation)
- Number hero_points
      HeroPoint
      Invariant: hero_points ≥ 0
- Interactions: Build Hero, Execute Combat Round, Spend HeroPoint, Activate ExtraEffort

**Ability**
- AbilityType type {strength, stamina, agility, dexterity, fighting, intellect, awareness, presence}
- Number rank
      Rank
      Invariant: rank ≥ -5 unless absent
- Boolean absent
      Invariant: when absent, rank has no value
- Boolean enhanced
      Invariant: enhanced portion can be nullified; normal portion cannot
- Number enhanced_ranks
      Invariant: enhanced_ranks ≤ rank
- Interactions: Assign Ability Rank, Apply Enhanced Ability, Handle Debilitated Ability, Handle Absent Ability

**Rank**
- Number value
      Invariant: typically 0–20 for heroes; abilities can go to -5
- Interactions: used across all trait assignments

**PowerPoint**
- Number total
      Invariant: total = 15 × PowerLevel for starting hero
- Number spent
      Invariant: spent ≤ total
- Number available
      Invariant: available = total - spent
- Interactions: Build Hero, Advance Hero

**PowerLevel**
- Number level
      Invariant: level ≥ 1; default 10
- validate_attack_cap(Number attack_bonus, Number effect_rank) → Boolean
      Invariant: attack_bonus + effect_rank ≤ 2 × level
- validate_defense_cap(Number defense, Number toughness) → Boolean
      Invariant: defense + toughness ≤ 2 × level
- validate_skill_cap(Number skill_total) → Boolean
      Invariant: skill_total ≤ level + 10
- Interactions: Validate PowerLevel Cap

**Complication**
- String name
- String description
- ComplicationType type {accident, disability, enemy, identity, motivation, power_loss, prejudice, quirk, relationship, rivalry, secret, temper, weakness}
- Interactions: Define Background, Earn and Activate Complication

**Motivation** : Complication
- MotivationType motivation_type {doing_good, recognition, responsibility, thrills, justice, patriotism, acceptance}
- Interactions: Select Motivation

## Module: Skills

**Skill**
- String name
- AbilityType linked_ability
      Ability
- Number rank
      Rank
      Invariant: rank ≥ 0; total bonus ≤ PowerLevel + 10
- Boolean trained
      Invariant: trained = (rank > 0)
- Boolean requires_training
- check(DifficultyClass) → Degree
      Check, DifficultyClass
      Invariant: result = d20 + rank + ability_rank + modifiers
- Interactions: Acquire Skill, Perform SkillCheck

## Module: Advantages

**Advantage**
- String name
- AdvantageCategory category {combat, fortune, general, skill}
- Number rank
      Rank
      Invariant: rank ≥ 1; some advantages unranked (rank = 1)
- Boolean ranked
      Invariant: ranked determines if multiple ranks allowed
- Interactions: Select Advantage, Apply CombatAdvantage in Combat, Apply FortuneAdvantage

## Module: Powers

**Power**
- String name
- List<Effect> effects
      Effect
      Invariant: at least 1 effect
- List<Descriptor> descriptors
      Descriptor
- Number total_cost
      PowerPoint
      Invariant: total_cost = sum of effect costs after modifiers
- Interactions: Construct Power, Counter and Nullify Power

**Effect**
- String name
- EffectType type {affliction, blast, burrowing, communication, comprehend, concealment, create, damage, dazzle, deflect, elongation, enhanced_trait, feature, flight, growth, healing, illusion, immunity, insubstantial, leaping, luck_control, mind_reading, morph, move_object, movement, nullify, protection, quickness, regeneration, remote_sensing, senses, shrinking, speed, summon, swimming, teleport, transform, variable, weaken}
- Number rank
      Rank
- Number base_cost_per_rank
      Invariant: base_cost_per_rank ≥ 1
- DurationType duration {instant, concentration, sustained, continuous, permanent}
- RangeType range {personal, close, ranged, perception}
- List<Modifier> modifiers
      Modifier
- Number modified_cost_per_rank
      Invariant: modified_cost_per_rank = base_cost_per_rank + sum(extra costs) - sum(flaw costs); minimum 1
- calculate_total_cost() → Number
      Invariant: total = modified_cost_per_rank × rank + flat_modifiers
- Interactions: Select Base Effect, Apply Extra, Apply Flaw, Set Duration, Set Range

**Extra** : Modifier
- Number cost_per_rank
      Invariant: cost_per_rank ≥ 1
- Interactions: Apply Extra to Effect

**Flaw** : Modifier
- Number cost_reduction_per_rank
      Invariant: cost_reduction_per_rank ≥ 1
- Interactions: Apply Flaw to Effect

**Modifier**
- String name
- ModifierKind kind {extra, flaw, flat_extra, flat_flaw}
- Number value
      Invariant: value ≥ 1
- Interactions: Apply Extra, Apply Flaw

**Descriptor**
- String name
- DescriptorCategory category {source, medium, type}
- counters(Descriptor other) → Boolean
      Invariant: fire counters ice; light counters darkness; etc.
- Interactions: Assign Descriptor, Counter Incoming Effect

**Array**
- List<AlternateEffect> alternate_effects
      AlternateEffect
      Invariant: at least 2 alternate effects
- AlternateEffect active_effect
      Invariant: exactly one active at a time
- Number base_cost
      Invariant: base_cost = cost of most expensive effect; others cost 1 or 2 each
- switch(AlternateEffect target) → void
      Invariant: requires Free Action; cannot switch if unable to take free actions
- Interactions: Build Array, Switch Active AlternateEffect

**AlternateEffect**
- Effect effect
      Effect
- Boolean dynamic
      Invariant: dynamic allows partial rank allocation
- Interactions: Build Array, Switch Active AlternateEffect

## Module: Combat

**Attack**
- AttackType type {close, ranged, perception, area}
- Number attack_bonus
      Invariant: attack_bonus = fighting_rank + close_combat_rank (close) or dexterity_rank + ranged_combat_rank (ranged)
- check(Defense) → Degree
      AttackCheck, Defense
      Invariant: result = d20 + attack_bonus vs target DefenseClass
- Interactions: Perform Attack

**AttackCheck** : Check
- Attack attack
      Attack
- Defense target_defense
      Defense
      Invariant: close → Parry; ranged → Dodge
- Interactions: Perform Close Attack, Perform Ranged Attack

**Defense**
- DefenseType type {dodge, parry, fortitude, toughness, will}
- Number rank
      Rank
- AbilityType linked_ability
      Ability
      Invariant: dodge→agility; parry→fighting; fortitude→stamina; toughness→stamina; will→awareness
- Number defense_class
      DefenseClass
      Invariant: defense_class = rank + 10
- Interactions: Resist Effect, Perform Attack

**Initiative**
- Number bonus
      Invariant: bonus = agility_rank + modifiers
- Number result
      Invariant: result = d20 + bonus
- Interactions: Determine Initiative, Roll Initiative

**Round**
- List<Turn> turns
      Turn
      Invariant: turns ordered by Initiative result descending
- Interactions: Execute Combat Round

**Turn**
- Hero actor
      Hero
- List<Action> actions
      Action
      Invariant: 1 standard + 1 move + any free actions per turn
- Interactions: Execute Combat Round

**Action**
- ActionType type {standard, move, free, reaction}
- Interactions: Execute Combat Round, Execute Maneuver

**Maneuver**
- ManeuverType type {aim, all_out_attack, charge, defend, delay, disarm, grab, interpose, move_by_action, power_attack, ready, slam, team_attack, trip}
- execute(Hero actor, Hero target) → Degree
      Check
- Interactions: Execute Maneuver

**ResistanceCheck** : Check
- Defense defense_used
      Defense
- Effect resisted_effect
      Effect
- Number dc
      DifficultyClass
      Invariant: dc = effect_rank + 10 (or + 15 for Damage)
- Interactions: Resist Damage, Resist Affliction, Resist Weaken, Resist Nullify

## Module: Attack Effects

**Damage** : Effect
- Number rank
      Rank
- resist(Defense toughness) → DamageResult
      ResistanceCheck, DamageResult
      Invariant: DC = rank + 15; cumulative -1 per prior failure
- Interactions: Resist Damage, Equip Weapon

**Affliction** : Effect
- List<Condition> first_degree_conditions
      Condition
- List<Condition> second_degree_conditions
      Condition
- List<Condition> third_degree_conditions
      Condition
- DefenseType resisted_by
      Defense
- resist(Defense) → Condition
      ResistanceCheck, Condition, Degree
      Invariant: DC = rank + 10; 1st degree → first_degree; 2nd → second_degree; 3rd → third_degree
- Interactions: Resist Affliction

**Weaken** : Effect
- String weakened_trait
- DefenseType resisted_by
      Defense
- resist(Defense) → Number
      ResistanceCheck, Degree
      Invariant: DC = rank + 10; target loses 1 rank per Degree of failure
- Interactions: Resist Weaken

**Nullify** : Effect
- List<Descriptor> affected_descriptors
      Descriptor
- resist(Check) → Boolean
      ResistanceCheck
      Invariant: DC = rank + 10; vs 11 + target effect rank
- Interactions: Nullify Active Effect, Resist Nullify

## Module: Conditions

**Condition**
- ConditionType type {compelled, controlled, dazed, stunned, defenseless, disabled, fatigued, exhausted, hindered, immobile, impaired, vulnerable, weakened, unaware}
- ConditionSeverity severity {mild, moderate, severe}
- Interactions: Apply Condition, Recover from Condition

**CombinedCondition** : Condition
- List<Condition> components
      Condition
      Invariant: e.g. Asleep = defenseless + stunned + unaware
- CombinedType combined_type {asleep, blind, bound, dying, entranced, incapacitated, paralyzed, prone, restrained, staggered, surprised, transformed}
- Interactions: Apply CombinedCondition

**ConditionTier**
- Condition mild
- Condition moderate
- Condition severe
      Invariant: progression: impaired→disabled→debilitated; dazed→stunned→incapacitated; hindered→immobile; vulnerable→defenseless
- escalate(Condition current) → Condition
      Invariant: returns next tier; if already severe, no further escalation
- Interactions: Escalate Condition Severity

**DamageResult**
- Number toughness_penalty
      Invariant: cumulative -1 per failed Toughness check
- Condition applied_condition
      Condition
      Invariant: 1 degree = -1 only; 2 degrees = dazed + -1; 3 degrees = staggered; 4+ degrees = incapacitated
- Interactions: Apply DamageResult, Resist Damage

## Module: Resources

**HeroPoint**
- Number available
      Invariant: available ≥ 0; starts at 1 per session
- spend(HeroPointUse use) → void
      Invariant: available ≥ 1 to spend
- HeroPointUse use_type {reroll, power_stunt, recover, inspiration, instant_counter, editing}
- Interactions: Spend HeroPoint

**ExtraEffort**
- ExtraEffortType type {power_boost, power_stunt, extra_action, improved_check}
- activate(Hero) → void
      Invariant: hero gains benefit immediately; becomes Fatigued after round
- Interactions: Activate ExtraEffort

**PowerStunt**
- AlternateEffect temporary_effect
      AlternateEffect
- PowerStuntSource source {hero_point, extra_effort}
- DurationType duration
      Invariant: lasts until end of turn (ExtraEffort) or end of scene (HeroPoint)
- Interactions: Perform PowerStunt

## Module: Equipment

**Equipment**
- String name
- Number equipment_points
      Invariant: total ≤ 5 × Equipment advantage rank
- Interactions: Use Equipment

**Device** : Power
- Boolean easily_removable
      Invariant: easily_removable → -2 per 5 points; not easily → -1 per 5 points
- Interactions: Use Device Power, Lose Device

**Weapon** : Equipment
- Damage damage_effect
      Damage
- WeaponType type {melee, ranged}
- Number damage_rank
      Rank
- Interactions: Equip Weapon

**Armor** : Equipment
- Number protection_rank
      Rank
      Invariant: adds to Toughness Defense
- Interactions: Equip Armor

**Vehicle**
- Number size
- Number strength
- Number speed
- Number toughness
- Number defense
- List<Feature> features
      Feature
- Interactions: Operate Vehicle

**Headquarters**
- Number size
- Number toughness
- List<Feature> features
      Feature
- Interactions: Manage Headquarters

**Feature**
- String name
- FeatureType type {communications, computer, concealed, defense_system, dock, fire_prevention, gym, hangar, infirmary, isolated, lab, library, living_space, personnel, power_system, security_system, workshop}
- Interactions: Use Headquarters Feature

## Module: Entities

**Minion**
- Hero base_stats
      Hero
      Invariant: incapacitated on any failed resistance check (no degrees)
- Number point_budget
      PowerPoint
      Invariant: point_budget = 15 × Minion advantage rank
- Interactions: Command Minion, Summon Minion, Defeat Minion

**Sidekick** : Minion
- Number point_budget
      PowerPoint
      Invariant: point_budget = 5 × Sidekick advantage rank; uses full Hero rules
- Interactions: Direct Sidekick

**Construct**
- Hero base_stats
      Hero
      Invariant: Stamina absent; immune to Fortitude effects; no Stamina-based recovery
- Interactions: Handle Construct Damage

**Archetype**
- String name
- ArchetypeType type {battlesuit, construct, crime_fighter, energy_controller, gadgeteer, martial_artist, mimic, mystic, paragon, powerhouse, psychic, shapeshifter, speedster, warrior}
- Hero template
      Hero
- Interactions: Choose Archetype Template
