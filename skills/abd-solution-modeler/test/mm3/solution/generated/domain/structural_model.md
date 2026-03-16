# Structural Model — Mutants & Masterminds 3rd Edition

## Module: Resolution

**Check**
- Number modifier
      Invariant: modifier = trait rank + circumstance modifiers
- Number result
      Invariant: result = d20 roll + modifier
- DifficultyClass target_dc
      DifficultyClass — association
- resolve() → Degree
      Degree — creates
      Invariant: result ≥ target_dc.value = success
- Interactions: Resolve Check, Perform SkillCheck, Perform AttackCheck, Resist Effect

**DifficultyClass**
- Number value
      Invariant: value ≥ 0
- Check resolved_by
      Check — association (back-reference)
- Interactions: Resolve Check, Resist Effect

**Degree**
- Number margin
      Invariant: margin = check result - DC
- Number degrees
      Invariant: degrees = floor(abs(margin) / 5); minimum 1 on any success/failure
- Boolean success
      Invariant: success = (margin ≥ 0)
- Check source_check
      Check — association (back-reference to creator)
- Interactions: Calculate Degree, Resist Damage, Resist Affliction

**OpposedCheck**
- Check attacker_check
      Check — composition
- Check defender_check
      Check — composition
- resolve() → Degree
      Degree — creates
      Invariant: higher result wins; ties favor defender
- Interactions: Resolve OpposedCheck, Grab Target, Trip Target, Disarm Target

**RoutineCheck** : Check
- Boolean qualifies
      Invariant: qualifies = (rank + 10 ≥ DC) AND no stress/threat
- resolve() → Number
      Invariant: result = rank + 10 (no roll)
- Interactions: Perform RoutineCheck

## Module: Character

**Hero**
- String name
- Dictionary<AbilityType, Ability> abilities
      Ability — composition
      Invariant: exactly 8 entries
- List<Skill> skills
      Skill — composition
- List<Advantage> advantages
      Advantage — aggregation
- List<Power> powers
      Power — composition
- Dictionary<DefenseType, Defense> defenses
      Defense — composition
      Invariant: exactly 5 entries
- PowerPoint budget
      PowerPoint — composition
- PowerLevel power_level
      PowerLevel — aggregation
- List<Complication> complications
      Complication — composition
      Invariant: ≥ 2 complications including Motivation
- Number hero_points
      HeroPoint
      Invariant: hero_points ≥ 0
- List<Condition> active_conditions
      Condition — aggregation
- Number toughness_penalty
      Invariant: cumulative -1 per failed Toughness ResistanceCheck
- Interactions: Build Hero, Execute Combat Round, Spend HeroPoint

**Ability**
- AbilityType type {strength, stamina, agility, dexterity, fighting, intellect, awareness, presence}
- Number rank
      Rank
      Invariant: rank ≥ -5 unless absent
- Boolean absent
- Boolean enhanced
- Number enhanced_ranks
      Invariant: enhanced_ranks ≤ rank; enhanced portion can be nullified
- Hero owner
      Hero — association (back-reference)
- List<Defense> contributes_to
      Defense — association
- List<Skill> linked_skills
      Skill — association
- Interactions: Assign Ability Rank, Handle Debilitated Ability, Handle Absent Ability

**PowerPoint**
- Number total
      Invariant: total = 15 × PowerLevel.level for starting hero
- Number spent
      Invariant: spent ≤ total
- Hero owner
      Hero — association (back-reference)
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
- Interactions: Validate PowerLevel Cap, Raise PowerLevel

**Complication**
- String name
- String description
- ComplicationType type {accident, disability, enemy, identity, motivation, power_loss, prejudice, quirk, relationship, rivalry, secret, temper, weakness}
- Hero owner
      Hero — association (back-reference)
- Interactions: Trigger Complication, Earn HeroPoint from Complication

**Motivation** : Complication
- MotivationType motivation_type {doing_good, recognition, responsibility, thrills, justice, patriotism, acceptance}
- Interactions: Select Motivation

## Module: Skills

**Skill**
- String name
- AbilityType linked_ability
      Ability — association
- Number rank
      Rank
      Invariant: rank ≥ 0; rank + ability_rank ≤ PowerLevel + 10
- Boolean trained
      Invariant: trained = (rank > 0)
- Boolean requires_training
- Hero owner
      Hero — association (back-reference)
- check(DifficultyClass) → Degree
      Check — creates
      Invariant: modifier = rank + linked_ability.rank
- Interactions: Acquire Skill, Perform SkillCheck

## Module: Advantages

**Advantage**
- String name
- AdvantageCategory category {combat, fortune, general, skill}
- Number rank
      Rank
      Invariant: rank ≥ 1
- Boolean ranked
- Hero owner
      Hero — association (back-reference)
- Interactions: Select Advantage, Apply CombatAdvantage, Apply FortuneAdvantage

## Module: Powers

**Power**
- String name
- List<Effect> effects
      Effect — composition
      Invariant: ≥ 1 effect
- List<Descriptor> descriptors
      Descriptor — aggregation
- Hero owner
      Hero — association (back-reference)
- calculate_total_cost() → Number
      PowerPoint
      Invariant: sum of all effect costs after modifiers
- Interactions: Construct Power, Counter and Nullify Power

**Effect**
- String name
- EffectType type
- Number rank
      Rank
- Number base_cost_per_rank
      Invariant: base_cost_per_rank ≥ 1
- DurationType duration {instant, concentration, sustained, continuous, permanent}
- RangeType range {personal, close, ranged, perception}
- List<Modifier> modifiers
      Modifier — aggregation
- Power parent_power
      Power — association (back-reference)
- calculate_modified_cost() → Number
      Invariant: (base + sum(extras) - sum(flaws)) × rank + flat_modifiers; minimum 1 per rank
- Interactions: Select Base Effect, Apply Extra, Apply Flaw, Set Duration, Set Range

**Extra** : Modifier
- Number cost_per_rank
      Invariant: cost_per_rank ≥ 1
- Effect applied_to
      Effect — association (back-reference)
- Interactions: Apply Extra to Effect

**Flaw** : Modifier
- Number cost_reduction_per_rank
      Invariant: cost_reduction_per_rank ≥ 1
- Effect applied_to
      Effect — association (back-reference)
- Interactions: Apply Flaw to Effect

**Modifier**
- String name
- ModifierKind kind {extra, flaw, flat_extra, flat_flaw}
- Number value
      Invariant: value ≥ 1
- Effect applied_to
      Effect — association (back-reference)

**Descriptor**
- String name
- DescriptorCategory category {source, medium, type}
- Power tagged_power
      Power — association (back-reference)
- counters(Descriptor other) → Boolean
      Invariant: opposing descriptors counter each other
- Interactions: Assign Descriptor, Counter Incoming Effect

**Array**
- List<AlternateEffect> alternate_effects
      AlternateEffect — composition
      Invariant: ≥ 2 alternate effects
- AlternateEffect active_effect
      Invariant: exactly 1 active
- Power parent_power
      Power — association (back-reference)
- Number base_cost
      Invariant: cost of most expensive effect; others cost 1 or 2 each
- switch(AlternateEffect target) → void
      Invariant: requires Free Action
- Interactions: Build Array, Switch Active AlternateEffect

**AlternateEffect**
- Effect effect
      Effect — composition
- Boolean dynamic
- Array parent_array
      Array — association (back-reference)
- Interactions: Build Array, Switch Active AlternateEffect

## Module: Combat

**Attack**
- AttackType type {close, ranged, perception, area}
- Number attack_bonus
- Hero attacker
      Hero — association
- check(Defense target_defense) → Degree
      AttackCheck — creates
- Interactions: Perform Attack

**AttackCheck** : Check
- Attack source_attack
      Attack — association (back-reference)
- Defense target_defense
      Defense — association
      Invariant: close → Parry; ranged → Dodge
- Interactions: Perform Close Attack, Perform Ranged Attack

**Defense**
- DefenseType type {dodge, parry, fortitude, toughness, will}
- Number rank
      Rank
- Ability linked_ability
      Ability — association
      Invariant: dodge→agility; parry→fighting; fortitude→stamina; toughness→stamina; will→awareness
- Number defense_class
      Invariant: defense_class = rank + 10
- Hero owner
      Hero — association (back-reference)
- Interactions: Resist Effect, Perform Attack

**ResistanceCheck** : Check
- Defense defense_used
      Defense — association
- Effect resisted_effect
      Effect — association
- DifficultyClass effect_dc
      DifficultyClass — composition
      Invariant: dc = effect_rank + 10 (or + 15 for Damage)
- Hero target
      Hero — association
- Interactions: Resist Damage, Resist Affliction, Resist Weaken, Resist Nullify

**Initiative**
- Number bonus
      Invariant: bonus = agility.rank + modifiers
- Number result
      Invariant: result = d20 + bonus
- Hero combatant
      Hero — association
- Interactions: Roll Initiative

**Round**
- List<Turn> turns
      Turn — composition
      Invariant: ordered by Initiative.result descending
- Interactions: Execute Combat Round

**Turn**
- Hero actor
      Hero — association
- List<Action> actions_taken
      Action — composition
      Invariant: 1 standard + 1 move + any free per turn
- Round parent_round
      Round — association (back-reference)
- Interactions: Execute Combat Round

**Action**
- ActionType type {standard, move, free, reaction}
- Turn parent_turn
      Turn — association (back-reference)

**Maneuver**
- ManeuverType type {aim, all_out_attack, charge, defend, delay, disarm, grab, interpose, move_by_action, power_attack, ready, slam, team_attack, trip}
- Hero actor
      Hero — association
- Hero target
      Hero — association
- execute() → Degree
      Check — creates
- Interactions: Execute Maneuver

## Module: Attack Effects

**Damage** : Effect
- resist(Defense toughness, Number cumulative_penalty) → DamageResult
      ResistanceCheck — creates, DamageResult — creates
      Invariant: DC = rank + 15 + cumulative_penalty
- Hero target
      Hero — association
- Interactions: Resist Damage

**Affliction** : Effect
- List<Condition> first_degree
      Condition — aggregation
- List<Condition> second_degree
      Condition — aggregation
- List<Condition> third_degree
      Condition — aggregation
- DefenseType resisted_by
      Defense — association
- resist(Defense) → Condition
      ResistanceCheck — creates, Condition — creates
      Invariant: DC = rank + 10
- Hero target
      Hero — association
- Interactions: Resist Affliction

**Weaken** : Effect
- String weakened_trait
- DefenseType resisted_by
      Defense — association
- resist(Defense) → Number
      ResistanceCheck — creates
      Invariant: target loses 1 rank per Degree of failure
- Hero target
      Hero — association
- Interactions: Resist Weaken

**Nullify** : Effect
- List<Descriptor> affected_descriptors
      Descriptor — aggregation
- resist(Check target_check) → Boolean
      ResistanceCheck — creates
      Invariant: DC = rank + 10; vs 11 + target effect rank
- Hero target
      Hero — association
- Interactions: Nullify Active Effect

## Module: Conditions

**Condition**
- ConditionType type {compelled, controlled, dazed, stunned, defenseless, disabled, fatigued, exhausted, hindered, immobile, impaired, vulnerable, weakened, unaware}
- ConditionSeverity severity {mild, moderate, severe}
- Hero affected
      Hero — association (back-reference)
- Interactions: Apply Condition, Recover from Condition

**CombinedCondition** : Condition
- List<Condition> components
      Condition — composition
      Invariant: e.g. Asleep = defenseless + stunned + unaware
- CombinedType combined_type {asleep, blind, bound, dying, entranced, incapacitated, paralyzed, prone, restrained, staggered, surprised, transformed}
- Interactions: Apply CombinedCondition

**ConditionTier**
- Condition mild
      Condition — association
- Condition moderate
      Condition — association
- Condition severe
      Condition — association
      Invariant: impaired→disabled→debilitated; dazed→stunned→incapacitated
- escalate(Condition current) → Condition
      Invariant: returns next tier
- Interactions: Escalate Condition Severity

**DamageResult**
- Number toughness_penalty
      Invariant: cumulative -1 per failed Toughness check
- Condition applied_condition
      Condition — association
      Invariant: 1° = -1; 2° = dazed + -1; 3° = staggered; 4°+ = incapacitated
- ResistanceCheck source_check
      ResistanceCheck — association (back-reference)
- Interactions: Apply DamageResult, Resist Damage

## Module: Resources

**HeroPoint**
- Number available
      Invariant: available ≥ 0; starts at 1 per session
- HeroPointUse use_type {reroll, power_stunt, recover, inspiration, instant_counter, editing}
- Hero owner
      Hero — association (back-reference)
- spend(HeroPointUse use) → void
      Invariant: available ≥ 1
- Interactions: Spend HeroPoint

**ExtraEffort**
- ExtraEffortType type {power_boost, power_stunt, extra_action, improved_check}
- Hero actor
      Hero — association
- activate() → void
      Condition — creates (Fatigued after round)
      Invariant: benefit immediate; Fatigued at end of round
- Interactions: Activate ExtraEffort

**PowerStunt**
- AlternateEffect temporary_effect
      AlternateEffect — composition
- PowerStuntSource source {hero_point, extra_effort}
- DurationType duration
      Invariant: end of turn (ExtraEffort) or end of scene (HeroPoint)
- Hero actor
      Hero — association (back-reference)
- Interactions: Perform PowerStunt

## Module: Equipment

**Equipment**
- String name
- Number equipment_points
      Invariant: total ≤ 5 × Equipment advantage rank
- Hero owner
      Hero — association (back-reference)
- Interactions: Use Equipment

**Device** : Power
- Boolean easily_removable
      Invariant: easily_removable → -2 per 5; not easily → -1 per 5
- Hero owner
      Hero — association (back-reference)
- Interactions: Use Device Power, Lose Device

**Weapon** : Equipment
- Damage damage_effect
      Damage — composition
- WeaponType type {melee, ranged}
- Interactions: Equip Weapon

**Armor** : Equipment
- Number protection_rank
      Rank
      Invariant: adds to Toughness Defense.rank
- Defense toughness_defense
      Defense — association
- Interactions: Equip Armor

**Vehicle**
- Number size
- Number strength
- Number speed
- Number toughness
- Number defense
- List<Feature> features
      Feature — composition
- Interactions: Operate Vehicle

**Headquarters**
- Number size
- Number toughness
- List<Feature> features
      Feature — composition
- Interactions: Manage Headquarters

**Feature**
- String name
- FeatureType type {communications, computer, concealed, defense_system, dock, fire_prevention, gym, hangar, infirmary, isolated, lab, library, living_space, personnel, power_system, security_system, workshop}
- Interactions: Use Headquarters Feature

## Module: Entities

**Minion**
- Hero base_stats
      Hero — composition
      Invariant: incapacitated on any failed resistance check
- Number point_budget
      Invariant: 15 × Minion advantage rank
- Hero commander
      Hero — association (back-reference)
- Interactions: Summon Minion, Defeat Minion

**Sidekick** : Minion
- Number point_budget
      Invariant: 5 × Sidekick advantage rank; uses full Hero rules
- Interactions: Direct Sidekick

**Construct**
- Hero base_stats
      Hero — composition
      Invariant: Stamina absent; immune to Fortitude effects
- Interactions: Handle Construct Damage

**Archetype**
- String name
- ArchetypeType type {battlesuit, construct, crime_fighter, energy_controller, gadgeteer, martial_artist, mimic, mystic, paragon, powerhouse, psychic, shapeshifter, speedster, warrior}
- Hero template
      Hero — composition
- Interactions: Choose Archetype Template
