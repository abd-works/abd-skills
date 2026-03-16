# Refined Domain Model — Mutants & Masterminds 3rd Edition

## Module: Resolution
- concepts — **Check**, **DifficultyClass**, **Degree**, **OpposedCheck**, **RoutineCheck**

**Check**
- Number modifier
      Invariant: modifier = trait rank + circumstance modifiers
- Number result
- DifficultyClass target_dc
      DifficultyClass — association
- roll() → Number
      Invariant: result = d20 + modifier
- resolve() → Degree
      Degree — creates
      Invariant: margin = result - dc; degrees = floor(abs(margin)/5)
- apply_circumstance(Number bonus) → void
      Invariant: ±2 minor, ±5 major
- Interactions: Resolve Check, Perform SkillCheck, Resist Effect

**DifficultyClass**
- Number value
      Invariant: value ≥ 0
- set_from_rank(Number rank, Number base) → void
      Invariant: value = rank + base

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
      Invariant: result = rank + 10

## Module: Character
- concepts — **Hero**, **Ability**, **PowerPoint**, **PowerLevel**, **Complication**, **Motivation**

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
      Invariant: ≥ 2 including Motivation
- Number hero_points
      Invariant: ≥ 0
- List<Condition> active_conditions
      Condition — aggregation
- Number toughness_penalty
      Invariant: cumulative -1 per failed Toughness check
- add_condition(Condition) → void
- remove_condition(Condition) → void
- increment_toughness_penalty() → void
- recovery_check() → Degree
      Check — creates
      Invariant: DC 10; success removes worst Damage Condition
- Interactions: Build Hero, Execute Combat Round, Manage Condition

**Ability**
- AbilityType type {strength, stamina, agility, dexterity, fighting, intellect, awareness, presence}
- Number rank
      Invariant: ≥ -5 unless absent
- Boolean absent
- Boolean enhanced
- Number enhanced_ranks
      Invariant: enhanced_ranks ≤ rank
- Hero owner
      Hero — association
- cost() → Number
      Invariant: rank × 2
- is_debilitated() → Boolean
      Invariant: rank < -5
- nullify_enhanced() → void
      Invariant: rank -= enhanced_ranks; enhanced = false
- Interactions: Assign Ability Rank, Handle Debilitated Ability

**PowerPoint**
- Number total
      Invariant: total = 15 × PowerLevel.level
- Number spent
      Invariant: spent ≤ total
- Hero owner
      Hero — association
- allocate(Number amount) → Boolean
      Invariant: returns false if spent + amount > total

**PowerLevel**
- Number level
      Invariant: ≥ 1; default 10
- validate_attack_cap(Number attack, Number effect) → Boolean
      Invariant: attack + effect ≤ 2 × level
- validate_defense_cap(Number defense, Number toughness) → Boolean
      Invariant: defense + toughness ≤ 2 × level
- validate_skill_cap(Number total) → Boolean
      Invariant: total ≤ level + 10

**Complication**
- String name
- String description
- ComplicationType type {accident, disability, enemy, identity, motivation, power_loss, prejudice, quirk, relationship, rivalry, secret, temper, weakness}
- Hero owner
      Hero — association
- trigger() → void
      Invariant: owner.hero_points += 1

**Motivation** : Complication
- MotivationType motivation_type {doing_good, recognition, responsibility, thrills, justice, patriotism, acceptance}

## Module: Skills
- concepts — **Skill**

**Skill**
- String name
- AbilityType linked_ability
      Ability — association
- Number rank
      Invariant: ≥ 0; total_bonus ≤ PowerLevel + 10
- Boolean trained
      Invariant: trained = (rank > 0)
- Boolean requires_training
- Hero owner
      Hero — association
- check(DifficultyClass) → Degree
      Check — creates
      Invariant: modifier = rank + linked_ability.rank
- total_bonus() → Number
      Invariant: rank + linked_ability.rank

## Module: Advantages
- concepts — **Advantage**

**Advantage**
- String name
- AdvantageCategory category {combat, fortune, general, skill}
- Number rank
      Invariant: ≥ 1
- Boolean ranked
- Hero owner
      Hero — association
- cost() → Number
      Invariant: 1 PP per rank
- apply(Hero) → void

## Module: Powers
- concepts — **Power**, **Effect**, **Modifier**, **Extra**, **Flaw**, **Descriptor**, **Array**, **AlternateEffect**

**Power**
- String name
- List<Effect> effects
      Effect — composition
      Invariant: ≥ 1
- List<Descriptor> descriptors
      Descriptor — aggregation
- Hero owner
      Hero — association
- calculate_total_cost() → Number
- is_removable() → Boolean

**Effect**
- String name
- EffectType type
- Number rank
- Number base_cost_per_rank
      Invariant: ≥ 1
- DurationType duration {instant, concentration, sustained, continuous, permanent}
- RangeType range {personal, close, ranged, perception}
- List<Modifier> modifiers
      Modifier — aggregation
- Power parent_power
      Power — association
- calculate_modified_cost() → Number
      Invariant: (base + extras - flaws) × rank + flat; min 1/rank
- requires_attack_check() → Boolean
      Invariant: close/ranged → true; perception → false
- get_resistance_dc() → Number
      Invariant: rank + 10 (rank + 15 for Damage)

**Modifier**
- String name
- ModifierKind kind {extra, flaw, flat_extra, flat_flaw}
- Number value
      Invariant: ≥ 1
- Effect applied_to
      Effect — association
- adjust_cost(Number base) → Number

**Extra** : Modifier
- Number cost_per_rank
      Invariant: ≥ 1

**Flaw** : Modifier
- Number cost_reduction_per_rank
      Invariant: ≥ 1

**Descriptor**
- String name
- DescriptorCategory category {source, medium, type}
- Power tagged_power
      Power — association
- counters(Descriptor other) → Boolean

**Array**
- List<AlternateEffect> alternate_effects
      AlternateEffect — composition
      Invariant: ≥ 2
- AlternateEffect active_effect
      Invariant: exactly 1 active
- Power parent_power
      Power — association
- Number base_cost
      Invariant: most expensive effect; others 1-2 each
- switch(AlternateEffect) → void
      Invariant: requires Free Action

**AlternateEffect**
- Effect effect
      Effect — composition
- Boolean dynamic
- Array parent_array
      Array — association

## Module: Combat
- concepts — **Attack**, **AttackCheck**, **Defense**, **ResistanceCheck**, **Initiative**, **Round**, **Turn**, **Action**, **Maneuver**

**Attack**
- AttackType type {close, ranged, perception, area}
- Number attack_bonus
- Hero attacker
      Hero — association
- calculate_bonus() → Number
      Invariant: close = fighting + close_combat; ranged = dexterity + ranged_combat
- check(Defense) → Degree
      AttackCheck — creates

**AttackCheck** : Check
- Attack source_attack
      Attack — association
- Defense target_defense
      Defense — association
      Invariant: close → Parry; ranged → Dodge

**Defense**
- DefenseType type {dodge, parry, fortitude, toughness, will}
- Number rank
- Ability linked_ability
      Ability — association
      Invariant: dodge→agility; parry→fighting; fortitude→stamina; toughness→stamina; will→awareness
- Hero owner
      Hero — association
- defense_class() → Number
      Invariant: rank + 10
- cost() → Number
      Invariant: 1 PP per rank above linked_ability.rank

**ResistanceCheck** : Check
- Defense defense_used
      Defense — association
- Effect resisted_effect
      Effect — association
- Hero target
      Hero — association
- resolve_damage() → DamageResult
      DamageResult — creates
      Invariant: DC = rank + 15 + toughness_penalty
- resolve_affliction() → Condition
      Condition — creates
      Invariant: Degree maps to Affliction tier
- resolve_weaken() → Number
      Invariant: ranks lost = Degree of failure

**Initiative**
- Number bonus
      Invariant: agility.rank + modifiers
- Number result
- Hero combatant
      Hero — association
- roll() → Number
      Invariant: d20 + bonus

**Round**
- List<Turn> turns
      Turn — composition
- order_turns() → void
      Invariant: descending Initiative.result

**Turn**
- Hero actor
      Hero — association
- List<Action> actions_taken
      Action — composition
      Invariant: 1 standard + 1 move + free actions
- has_standard_action() → Boolean

**Action**
- ActionType type {standard, move, free, reaction}

**Maneuver**
- ManeuverType type {aim, all_out_attack, charge, defend, delay, disarm, grab, interpose, move_by_action, power_attack, ready, slam, team_attack, trip}
- Hero actor
      Hero — association
- Hero target
      Hero — association
- execute() → Degree
      Check — creates

## Module: Attack Effects
- concepts — **Damage**, **Affliction**, **Weaken**, **Nullify**

**Damage** : Effect
- Hero target
      Hero — association
- resist(Defense toughness, Number penalty) → DamageResult
      ResistanceCheck — creates, DamageResult — creates
      Invariant: DC = rank + 15 + penalty

**Affliction** : Effect
- List<Condition> first_degree
      Condition — aggregation
- List<Condition> second_degree
      Condition — aggregation
- List<Condition> third_degree
      Condition — aggregation
- DefenseType resisted_by
- Hero target
      Hero — association
- resist(Defense) → Condition
      ResistanceCheck — creates, Condition — creates

**Weaken** : Effect
- String weakened_trait
- DefenseType resisted_by
- Hero target
      Hero — association
- resist(Defense) → Number
      ResistanceCheck — creates

**Nullify** : Effect
- List<Descriptor> affected_descriptors
      Descriptor — aggregation
- Hero target
      Hero — association
- resist(Check target_check) → Boolean
      ResistanceCheck — creates

## Module: Conditions
- concepts — **Condition**, **CombinedCondition**, **ConditionTier**, **DamageResult**

**Condition**
- ConditionType type {compelled, controlled, dazed, stunned, defenseless, disabled, fatigued, exhausted, hindered, immobile, impaired, vulnerable, weakened, unaware}
- ConditionSeverity severity {mild, moderate, severe}
- Hero affected
      Hero — association
- apply(Hero) → void
- remove(Hero) → void

**CombinedCondition** : Condition
- List<Condition> components
      Condition — composition
- CombinedType combined_type {asleep, blind, bound, dying, entranced, incapacitated, paralyzed, prone, restrained, staggered, surprised, transformed}
- apply(Hero) → void
      Invariant: applies all components

**ConditionTier**
- Condition mild
- Condition moderate
- Condition severe
      Invariant: impaired→disabled→debilitated; dazed→stunned→incapacitated
- escalate(Condition) → Condition

**DamageResult**
- Number toughness_penalty
      Invariant: cumulative -1
- Condition applied_condition
      Invariant: 1°=-1; 2°=dazed+-1; 3°=staggered; 4°+=incapacitated
- ResistanceCheck source_check
      ResistanceCheck — association
- apply(Hero) → void
      Invariant: target.toughness_penalty += 1; target gains condition

## Module: Resources
- concepts — **HeroPoint**, **ExtraEffort**, **PowerStunt**

**HeroPoint**
- Number available
      Invariant: ≥ 0; starts 1/session
- HeroPointUse use_type {reroll, power_stunt, recover, inspiration, instant_counter, editing}
- Hero owner
      Hero — association
- spend(HeroPointUse) → void
      Invariant: available ≥ 1
- reroll(Check) → Check
      Check — creates
      Invariant: minimum result 11
- power_stunt(Effect) → PowerStunt
      PowerStunt — creates

**ExtraEffort**
- ExtraEffortType type {power_boost, power_stunt, extra_action, improved_check}
- Hero actor
      Hero — association
- activate() → void
      Invariant: benefit immediate; fatigue scheduled
- apply_fatigue() → void
      Condition — creates
      Invariant: Fatigued; if already Fatigued → Exhausted; if Exhausted → Incapacitated

**PowerStunt**
- AlternateEffect temporary_effect
      AlternateEffect — composition
- PowerStuntSource source {hero_point, extra_effort}
- Hero actor
      Hero — association

## Module: Equipment
- concepts — **Equipment**, **Device**, **Weapon**, **Armor**, **Vehicle**, **Headquarters**, **Feature**

**Equipment**
- String name
- Number equipment_points
      Invariant: ≤ 5 × Equipment advantage rank
- Hero owner
      Hero — association

**Device** : Power
- Boolean easily_removable
- Hero owner
      Hero — association
- remove() → void
      Invariant: owner loses associated Power effects

**Weapon** : Equipment
- Damage damage_effect
      Damage — composition
- WeaponType type {melee, ranged}
- equip(Hero) → void

**Armor** : Equipment
- Number protection_rank
- Defense toughness_defense
      Defense — association
- equip(Hero) → void
      Invariant: toughness.rank += protection_rank

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
- FeatureType type {communications, computer, concealed, defense_system, dock, fire_prevention, gym, hangar, infirmary, isolated, lab, library, living_space, personnel, power_system, security_system, workshop}

## Module: Entities
- concepts — **Minion**, **Sidekick**, **Construct**, **Archetype**

**Minion**
- Hero base_stats
      Hero — composition
- Number point_budget
      Invariant: 15 × Minion advantage rank
- Hero commander
      Hero — association
- resist(ResistanceCheck) → void
      Invariant: any failure → Incapacitated

**Sidekick** : Minion
- Number point_budget
      Invariant: 5 × Sidekick advantage rank; full Hero rules

**Construct**
- Hero base_stats
      Hero — composition
      Invariant: Stamina absent; immune to Fortitude

**Archetype**
- String name
- ArchetypeType type {battlesuit, construct, crime_fighter, energy_controller, gadgeteer, martial_artist, mimic, mystic, paragon, powerhouse, psychic, shapeshifter, speedster, warrior}
- Hero template
      Hero — composition
- customize(PowerPoint) → Hero
