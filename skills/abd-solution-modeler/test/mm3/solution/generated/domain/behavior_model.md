# Behavior Model — Mutants & Masterminds 3rd Edition

## Module: Resolution

**Check**
- Number modifier
      Invariant: modifier = trait rank + circumstance modifiers
- Number result
- DifficultyClass target_dc
      DifficultyClass — association
- Degree outcome
      Degree — creates
- roll() → Number
      Invariant: result = d20 + modifier
- resolve() → Degree
      DifficultyClass
      Invariant: margin = result - target_dc.value; degrees = floor(abs(margin)/5)
- apply_circumstance(Number bonus) → void
      Invariant: modifier adjusted; ±2 minor, ±5 major
- Interactions: Resolve Check, Perform SkillCheck, Resist Effect

**DifficultyClass**
- Number value
      Invariant: value ≥ 0
- set_from_rank(Number rank, Number base) → void
      Invariant: value = rank + base (10 for effects, 15 for Damage)

**Degree**
- Number margin
- Number degrees
      Invariant: degrees = floor(abs(margin)/5); min 1
- Boolean success
      Invariant: success = (margin ≥ 0)
- Check source_check
      Check — association

**OpposedCheck**
- Check attacker_check
      Check — composition
- Check defender_check
      Check — composition
- resolve() → Degree
      Invariant: higher wins; tie → defender

**RoutineCheck** : Check
- Boolean qualifies
      Invariant: qualifies = (rank + 10 ≥ DC) AND no stress
- auto_resolve() → Number
      Invariant: result = rank + 10 (no roll)

## Module: Character

**Hero**
- String name
- Dictionary<AbilityType, Ability> abilities
      Ability — composition
- List<Skill> skills
      Skill — composition
- List<Advantage> advantages
      Advantage — aggregation
- List<Power> powers
      Power — composition
- Dictionary<DefenseType, Defense> defenses
      Defense — composition
- PowerPoint budget
      PowerPoint — composition
- PowerLevel power_level
      PowerLevel — aggregation
- List<Complication> complications
      Complication — composition
- Number hero_points
      HeroPoint
- List<Condition> active_conditions
      Condition — aggregation
- Number toughness_penalty
      Invariant: cumulative -1 per failed Toughness check
- add_condition(Condition condition) → void
      Invariant: condition added to active_conditions
- remove_condition(Condition condition) → void
      Invariant: condition removed from active_conditions
- increment_toughness_penalty() → void
      Invariant: toughness_penalty -= 1
- recovery_check() → Degree
      Check — creates
      Invariant: DC 10; success removes worst Damage condition and resets penalty
- Interactions: Build Hero, Execute Combat Round, Manage Condition

**Ability**
- AbilityType type {strength, stamina, agility, dexterity, fighting, intellect, awareness, presence}
- Number rank
      Rank
      Invariant: rank ≥ -5 unless absent
- Boolean absent
- Boolean enhanced
- Number enhanced_ranks
      Invariant: enhanced_ranks ≤ rank
- Hero owner
      Hero — association
- cost() → Number
      PowerPoint
      Invariant: cost = rank × 2
- is_debilitated() → Boolean
      Invariant: rank < -5
- nullify_enhanced() → void
      Invariant: rank reduced by enhanced_ranks; enhanced = false
- Interactions: Assign Ability Rank, Handle Debilitated Ability

**PowerPoint**
- Number total
      Invariant: total = 15 × PowerLevel.level
- Number spent
      Invariant: spent ≤ total
- Hero owner
      Hero — association
- allocate(Number amount) → Boolean
      Invariant: spent + amount ≤ total; returns false if insufficient
- Interactions: Build Hero, Advance Hero

**PowerLevel**
- Number level
      Invariant: level ≥ 1; default 10
- validate_attack_cap(Number attack, Number effect) → Boolean
      Invariant: attack + effect ≤ 2 × level
- validate_defense_cap(Number defense, Number toughness) → Boolean
      Invariant: defense + toughness ≤ 2 × level
- validate_skill_cap(Number total) → Boolean
      Invariant: total ≤ level + 10
- Interactions: Validate PowerLevel Cap

**Complication**
- String name
- String description
- ComplicationType type
- Hero owner
      Hero — association
- trigger() → HeroPoint
      HeroPoint
      Invariant: hero.hero_points += 1
- Interactions: Trigger Complication, Earn HeroPoint

**Motivation** : Complication
- MotivationType motivation_type

## Module: Skills

**Skill**
- String name
- AbilityType linked_ability
      Ability — association
- Number rank
      Rank
- Boolean trained
      Invariant: trained = (rank > 0)
- Boolean requires_training
- Hero owner
      Hero — association
- check(DifficultyClass dc) → Degree
      Check — creates
      Invariant: modifier = rank + linked_ability.rank
- total_bonus() → Number
      Invariant: total = rank + linked_ability.rank
- Interactions: Acquire Skill, Perform SkillCheck

## Module: Advantages

**Advantage**
- String name
- AdvantageCategory category {combat, fortune, general, skill}
- Number rank
      Rank
- Boolean ranked
- Hero owner
      Hero — association
- cost() → Number
      PowerPoint
      Invariant: cost = rank (1 PP per rank)
- apply(Hero target) → void
      Invariant: applies advantage benefit in context
- Interactions: Select Advantage, Apply CombatAdvantage

## Module: Powers

**Power**
- String name
- List<Effect> effects
      Effect — composition
- List<Descriptor> descriptors
      Descriptor — aggregation
- Hero owner
      Hero — association
- calculate_total_cost() → Number
      Invariant: sum of all effect costs
- is_removable() → Boolean
      Invariant: true if any effect has Removable flaw
- Interactions: Construct Power, Counter and Nullify Power

**Effect**
- String name
- EffectType type
- Number rank
      Rank
- Number base_cost_per_rank
- DurationType duration
- RangeType range
- List<Modifier> modifiers
      Modifier — aggregation
- Power parent_power
      Power — association
- calculate_modified_cost() → Number
      Invariant: (base + extras - flaws) × rank + flat; min 1/rank
- requires_attack_check() → Boolean
      Invariant: close/ranged → true; perception → false; area → Dodge for half
- get_resistance_dc() → Number
      Invariant: rank + 10 (or rank + 15 for Damage)
- Interactions: Select Base Effect, Apply Extra, Apply Flaw

**Modifier**
- String name
- ModifierKind kind {extra, flaw, flat_extra, flat_flaw}
- Number value
- Effect applied_to
      Effect — association
- adjust_cost(Number base) → Number
      Invariant: extra → base + value; flaw → base - value; flat → separate

**Descriptor**
- String name
- DescriptorCategory category {source, medium, type}
- Power tagged_power
      Power — association
- counters(Descriptor other) → Boolean
      Invariant: opposing categories counter

**Array**
- List<AlternateEffect> alternate_effects
      AlternateEffect — composition
- AlternateEffect active_effect
- Power parent_power
      Power — association
- Number base_cost
      Invariant: most expensive effect cost; others 1-2 each
- switch(AlternateEffect target) → void
      Invariant: requires Free Action; deactivates current; activates target
- Interactions: Build Array, Switch AlternateEffect

**AlternateEffect**
- Effect effect
      Effect — composition
- Boolean dynamic
- Array parent_array
      Array — association

## Module: Combat

**Attack**
- AttackType type {close, ranged, perception, area}
- Number attack_bonus
- Hero attacker
      Hero — association
- calculate_bonus() → Number
      Invariant: close = fighting + close_combat_skill; ranged = dexterity + ranged_combat_skill
- check(Defense target) → Degree
      AttackCheck — creates
      Invariant: d20 + attack_bonus vs target.defense_class
- Interactions: Perform Attack

**AttackCheck** : Check
- Attack source_attack
      Attack — association
- Defense target_defense
      Defense — association

**Defense**
- DefenseType type {dodge, parry, fortitude, toughness, will}
- Number rank
      Rank
- Ability linked_ability
      Ability — association
- Hero owner
      Hero — association
- defense_class() → Number
      Invariant: rank + 10
- cost() → Number
      PowerPoint
      Invariant: 1 PP per rank above linked_ability.rank
- Interactions: Resist Effect, Perform Attack

**ResistanceCheck** : Check
- Defense defense_used
      Defense — association
- Effect resisted_effect
      Effect — association
- Hero target
      Hero — association
- resolve_damage() → DamageResult
      DamageResult — creates
      Invariant: DC = rank + 15 + target.toughness_penalty
- resolve_affliction() → Condition
      Condition — creates
      Invariant: DC = rank + 10; Degree maps to Affliction tier
- resolve_weaken() → Number
      Invariant: DC = rank + 10; ranks lost = Degree of failure
- Interactions: Resist Damage, Resist Affliction, Resist Weaken

**Initiative**
- Number bonus
- Number result
- Hero combatant
      Hero — association
- roll() → Number
      Invariant: result = d20 + bonus

**Round**
- List<Turn> turns
      Turn — composition
- order_turns() → void
      Invariant: turns sorted by Initiative.result descending

**Turn**
- Hero actor
      Hero — association
- List<Action> actions_taken
      Action — composition
- Round parent_round
      Round — association
- has_standard_action() → Boolean
      Invariant: true if standard action not yet used

**Action**
- ActionType type {standard, move, free, reaction}

**Maneuver**
- ManeuverType type
- Hero actor
      Hero — association
- Hero target
      Hero — association
- execute() → Degree
      Check — creates

## Module: Attack Effects

**Damage** : Effect
- resist(Defense toughness, Number penalty) → DamageResult
      ResistanceCheck — creates, DamageResult — creates
      Invariant: DC = rank + 15 + penalty
- Hero target
      Hero — association

**Affliction** : Effect
- List<Condition> first_degree
- List<Condition> second_degree
- List<Condition> third_degree
- DefenseType resisted_by
- resist(Defense) → Condition
      ResistanceCheck — creates, Condition — creates
      Invariant: 1°→first_degree; 2°→second_degree; 3°→third_degree

**Weaken** : Effect
- String weakened_trait
- DefenseType resisted_by
- resist(Defense) → Number
      ResistanceCheck — creates

**Nullify** : Effect
- List<Descriptor> affected_descriptors
      Descriptor — aggregation
- resist(Check target_check) → Boolean
      ResistanceCheck — creates
      Invariant: DC = rank + 10 vs 11 + target_effect_rank

## Module: Conditions

**Condition**
- ConditionType type
- ConditionSeverity severity {mild, moderate, severe}
- Hero affected
      Hero — association
- apply(Hero target) → void
      Invariant: adds to target.active_conditions
- remove(Hero target) → void
      Invariant: removes from target.active_conditions

**CombinedCondition** : Condition
- List<Condition> components
      Condition — composition
- CombinedType combined_type
- apply(Hero target) → void
      Invariant: applies all component conditions

**ConditionTier**
- Condition mild
- Condition moderate
- Condition severe
- escalate(Condition current) → Condition
      Invariant: returns next tier; null if already severe

**DamageResult**
- Number toughness_penalty
- Condition applied_condition
- ResistanceCheck source_check
      ResistanceCheck — association
- apply(Hero target) → void
      Invariant: target.toughness_penalty += 1; target gains applied_condition

## Module: Resources

**HeroPoint**
- Number available
      Invariant: ≥ 0; starts 1/session
- HeroPointUse use_type
- Hero owner
      Hero — association
- spend(HeroPointUse use) → void
      Invariant: available ≥ 1; decrements available
- reroll(Check original) → Check
      Check — creates
      Invariant: new roll minimum 11
- power_stunt(Effect template) → PowerStunt
      PowerStunt — creates

**ExtraEffort**
- ExtraEffortType type
- Hero actor
      Hero — association
- activate() → void
      Invariant: applies benefit; schedules Fatigued at end of round
- apply_fatigue() → void
      Condition — creates
      Invariant: actor gains Fatigued; if already Fatigued → Exhausted

**PowerStunt**
- AlternateEffect temporary_effect
      AlternateEffect — composition
- PowerStuntSource source {hero_point, extra_effort}
- DurationType duration
- Hero actor
      Hero — association

## Module: Equipment

**Equipment**
- String name
- Number equipment_points
- Hero owner
      Hero — association

**Device** : Power
- Boolean easily_removable
- Hero owner
      Hero — association
- remove() → void
      Invariant: owner loses all associated Power effects

**Weapon** : Equipment
- Damage damage_effect
      Damage — composition
- WeaponType type {melee, ranged}
- equip(Hero user) → void
      Invariant: user gains access to damage_effect

**Armor** : Equipment
- Number protection_rank
- Defense toughness_defense
      Defense — association
- equip(Hero user) → void
      Invariant: user.toughness.rank += protection_rank

**Vehicle**
- Number size
- Number strength
- Number speed
- Number toughness
- Number defense
- List<Feature> features
      Feature — composition

**Headquarters**
- Number size
- Number toughness
- List<Feature> features
      Feature — composition

**Feature**
- String name
- FeatureType type

## Module: Entities

**Minion**
- Hero base_stats
      Hero — composition
- Number point_budget
- Hero commander
      Hero — association
- resist(ResistanceCheck check) → void
      Invariant: any failure → incapacitated (no degrees)

**Sidekick** : Minion
- Number point_budget
      Invariant: 5 × Sidekick advantage rank; full Hero rules apply

**Construct**
- Hero base_stats
      Hero — composition
      Invariant: Stamina absent; immune to Fortitude effects

**Archetype**
- String name
- ArchetypeType type
- Hero template
      Hero — composition
- customize(PowerPoint budget) → Hero
      Invariant: creates Hero from template within budget
