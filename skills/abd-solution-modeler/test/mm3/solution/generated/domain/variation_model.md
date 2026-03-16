# Variation Model — Mutants & Masterminds 3rd Edition

## Inheritance Hierarchies

### Check Hierarchy
```
Check (base)
├── RoutineCheck — auto-succeeds when rank + 10 ≥ DC
├── OpposedCheck — compares two Check results
├── AttackCheck — d20 + attack_bonus vs DefenseClass
│   ├── close: uses Fighting + close_combat skill vs Parry
│   └── ranged: uses Dexterity + ranged_combat skill vs Dodge
└── ResistanceCheck — d20 + Defense vs Effect DC
    ├── damage: vs DC rank + 15 + cumulative penalty
    ├── affliction: vs DC rank + 10; Degree → ConditionTier
    ├── weaken: vs DC rank + 10; lose ranks per Degree
    └── nullify: 11 + effect_rank vs Nullify DC
```

Shared protocol: `roll() → Number`, `resolve() → Degree`
Variation axis: what modifier and DC formula each subtype uses

### Effect Hierarchy
```
Effect (base)
├── Damage — resisted by Toughness; DC = rank + 15; cumulative penalty
├── Affliction — resisted by specified Defense; 3-tier Condition progression
├── Weaken — resisted by specified Defense; reduces trait Rank per Degree
├── Nullify — opposed check; suppresses matching Descriptor Powers
├── Healing — removes Damage Conditions from target
├── Regeneration — periodic automatic Damage recovery
├── Protection — adds to Toughness Defense rank
├── Immunity — grants complete immunity to specific Effect/Descriptor
├── Move Object — telekinetic force; Strength equivalent
├── Mind Reading — reads target thoughts; opposed by Will
├── Transform — changes target into different form
├── Summon — creates Minion with point budget
├── Variable — redistributable points for assumed forms
└── ... (30+ total effect types)
```

Shared protocol: `calculate_modified_cost() → Number`, `requires_attack_check() → Boolean`, `get_resistance_dc() → Number`
Variation axes: DurationType, RangeType, resist defense, DC formula

### Modifier Hierarchy
```
Modifier (base)
├── Extra — increases cost per rank
│   ├── Accurate, Area, Contagious, Extended Range, Homing, Impervious
│   ├── Increased Range, Indirect, Multiattack, Penetrating
│   ├── Perception Range, Reach, Reaction, Secondary Effect, Selective
│   └── ... (30+ extra types)
├── Flaw — decreases cost per rank
│   ├── Activation, Check Required, Concentration, Diminished Range
│   ├── Distracting, Fades, Feedback, Grab-based, Inaccurate
│   ├── Limited, Noticeable, Reduced Range, Removable, Side Effect
│   └── ... (20+ flaw types)
├── FlatExtra — fixed point increase
└── FlatFlaw — fixed point decrease
```

Shared protocol: `adjust_cost(Number base) → Number`
Variation axis: per-rank vs flat; positive vs negative

### Condition Hierarchy
```
Condition (base)
├── BasicCondition — single status effect
│   ├── Dazed, Stunned (action impairment tier)
│   ├── Hindered, Immobile (movement impairment tier)
│   ├── Impaired, Disabled (trait impairment tier)
│   ├── Vulnerable, Defenseless (defense impairment tier)
│   ├── Compelled, Controlled (will impairment tier)
│   ├── Fatigued, Exhausted (stamina impairment tier)
│   ├── Weakened, Unaware
│   └── ... (14 basic types)
└── CombinedCondition — compound of BasicConditions
    ├── Asleep = Defenseless + Stunned + Unaware
    ├── Blind = Unaware(visual) + Hindered + Vulnerable
    ├── Bound = Defenseless + Immobile + Impaired
    ├── Dying = Incapacitated + near death
    ├── Incapacitated = Defenseless + Stunned + Unaware
    ├── Paralyzed = Defenseless + Immobile + Stunned
    ├── Staggered = Dazed + Hindered
    └── ... (12 combined types)
```

Shared protocol: `apply(Hero) → void`, `remove(Hero) → void`
Variation axis: severity tier (ConditionTier progression)

### Advantage Hierarchy
```
Advantage (base)
├── CombatAdvantage — tactical combat options
│   ├── Accurate Attack, All-out Attack, Defensive Attack, Power Attack (trade-offs)
│   ├── Improved Critical, Improved Initiative (passive bonuses)
│   ├── Fast Grab, Improved Grab, Improved Hold (grapple specialization)
│   └── ... (25 combat types)
├── FortuneAdvantage — meta-currency and luck
│   ├── Beginner's Luck, Luck, Seize Initiative, Ultimate Effort
│   └── ... (6 fortune types)
├── GeneralAdvantage — general capabilities
│   ├── Equipment, Minion, Sidekick (resource-granting)
│   ├── Diehard, Great Endurance (survivability)
│   └── ... (14 general types)
└── SkillAdvantage — skill enhancements
    ├── Skill Mastery, Jack-of-all-Trades (broad skill bonuses)
    ├── Daze, Fascinate, Startle, Taunt (interaction combat)
    └── ... (20 skill types)
```

Shared protocol: `cost() → Number`, `apply(Hero) → void`

## Variation Paths (from decisions.json)

### Duration Variation
- `if` Effect.duration = Instant → one-time; no maintenance
- `if` Effect.duration = Concentration → active while hero concentrates; standard Action each turn
- `if` Effect.duration = Sustained → maintained with free Action; ends if stunned
- `if` Effect.duration = Continuous → persists until actively ended; survives incapacitation
- `if` Effect.duration = Permanent → always on; cannot be turned off; `cannot` be nullified with Innate

### Range Variation
- `if` Effect.range = Close → requires adjacency; uses Fighting/close_combat for AttackCheck
- `if` Effect.range = Ranged → requires line of sight within distance; uses Dexterity/ranged_combat
- `if` Effect.range = Perception → automatic hit; no AttackCheck; `requires` perceiving target

### Damage Resolution Branching
- `if` ResistanceCheck failure 1° → toughness_penalty += 1 only
- `if` ResistanceCheck failure 2° → Dazed + toughness_penalty += 1
- `if` ResistanceCheck failure 3° → Staggered (Dazed + Hindered)
- `if` ResistanceCheck failure 4°+ → Incapacitated

### Affliction Resolution Branching
- `if` ResistanceCheck failure 1° → first_degree Conditions applied
- `if` ResistanceCheck failure 2° → second_degree Conditions replace first
- `if` ResistanceCheck failure 3° → third_degree Conditions replace second

### Ability Debilitation Branching
- `if` Strength debilitated → hero collapses
- `if` Stamina debilitated → hero is Dying
- `if` Agility debilitated → hero `cannot` move
- `if` Dexterity debilitated → hero `cannot` manipulate objects
- `if` Fighting debilitated → hero `cannot` make close attacks
- `if` Intellect/Awareness/Presence debilitated → hero is Unaware

### Extra Effort Branching
- `if` ExtraEffort.type = power_boost → +1 Effect Rank for one use
- `if` ExtraEffort.type = power_stunt → temporary AlternateEffect
- `if` ExtraEffort.type = extra_action → additional standard Action
- `if` ExtraEffort.type = improved_check → +2 circumstance bonus
- `when` ExtraEffort used and hero already Fatigued → becomes Exhausted
- `when` ExtraEffort used and hero already Exhausted → becomes Incapacitated

### HeroPoint Use Branching
- `if` use_type = reroll → re-roll Check; minimum result 11
- `if` use_type = power_stunt → temporary AlternateEffect for scene
- `if` use_type = recover → remove one Condition immediately
- `if` use_type = inspiration → gain one Advantage for one Round
- `if` use_type = instant_counter → counter incoming Effect as Reaction
- `if` use_type = editing → introduce narrative element

### Minion vs Full Character
- `if` target is Minion → any failed ResistanceCheck = Incapacitated (no Degrees)
- `if` target is full Hero → Degrees determine severity per normal rules
- `if` target is Construct → immune to Fortitude effects; no Stamina-based recovery

### Equipment vs Device vs Innate Power
- `if` Equipment → mundane; 1 PP = 5 equipment points; easily replaced
- `if` Device → Power with Removable Flaw; can be taken away; `cannot` use when removed
- `if` Innate Power → built-in; `cannot` be nullified with Innate Extra

### Area Shape Variation
- `if` AreaShape = Burst → sphere centered on point; all in radius affected
- `if` AreaShape = Cloud → burst that lingers; affects those entering
- `if` AreaShape = Cone → emanates from user in arc
- `if` AreaShape = Line → straight path from user
- `if` AreaShape = Shapeable → custom form within volume limit
