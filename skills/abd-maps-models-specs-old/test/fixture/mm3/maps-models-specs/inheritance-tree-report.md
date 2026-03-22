# Domain object inheritance — `extends` trees (MM3)

Each concept below is listed in **depth-first** order. Under each name: excerpt from the handbook chunk(s) linked in `map-model-spec.json`, then a one-line source line.

## Outline

Ability
  Awareness
  ConstructAdvantageAbilityGate
  Stamina
    StaminaBreathHoldRoundBudget
AbilityRank
  AbilityRankPurchase
  InteractionTargetMentalThreshold
AlternateEffectArray
Check
  AcrobaticsTaskMenu
  AllOutAttackDefenseForAttackTrade
  AreaAndPerceptionAutomaticEffectResolution
  AttackCheckVersusDefenseClass
  ClimbCircumstanceModifierTable
  CriticalSuccess
  ForensicEvidenceAnalysisCheck
  InitiativeCheck
  JuryRiggedRepairCheck
  OpposedCheck
  OptionalInitiativeForTimedChallenge
  PrecariousSurfaceMovementCheck
  ReactionVersusFreeActionTiming
  RoutineAttackCheckAgainstMinion
  SkillCheckModifierSources
  StandardAndMoveActionPerCombatRound
  ToolingPenalty
  UltimateEffortFixedResult
Condition
  ActiveDefenseDegradation
  BasicCondition
  ConditionsFromResistanceFailure
  DamageConditionMinuteRecovery
  HeroDeathVersusMinionLethality
  IntimidationDemoralize
  MinionCombatResolutionPackage
  TurnStartEndsUntilNextTurnEffects
CoveringAttack
DescriptorLayer
DifficultyClass
  CatchFallingTargetDexterityDC
  DeceptionBelievabilityDCAdjustment
  SecurityOrTrapDCLadder
  TechnologyRestrictedCommunicationsDC
  VisualPerceptionVisibilityDC
MeasurementTable
  AthleticsJumpDistanceFromCheck
  CombatRoundDurationEstimate
  EnvironmentalHazardIntensityExamples
  MaterialToughnessOrdinalScale
  TimeMeasureRow
OpposedEffectCheck
PowerEffect
  Advantage
    AdvantageNameGroupings
    AdvantageRankAndDescriptionPattern
    FightingStyleAdvantageBundleExamples
  AlternateFormDescriptorPackages
  BlastRangedDamageEffect
  CommunicationLimitedFlaw
  ConcealmentEffectExtras
  ConstructArchetypePowerExamples
  CreateEffectExtras
  DefensePowerEffectPattern
  Descriptor
    SeriesRequiredDescriptorRule
  EnhancedTraitLimitedAndPermanent
  EquipmentAfflictionFortitudeDCExample
  ExtraEffortPowerSurge
  HeadquartersDefenseSystemEffectCap
  PerceptionRangeTargetingAndConcealment
  PowerActivationAndResolution
  PowerEffectNameTableFragment
  PowerEffectStandardCostPerRank
  PowerEffectSummaryLine
  PowerEffectType
  PowerExtraSection
  SamplePowerWriteupSchema
PowerModifierCatalog
PowerPoints
  AlternateVehicleEquipmentPointPricing
  PowerLevel
Rank
  FallDamageRankFromDistanceRank
  VehicleSizeCategoryPointCost
ResistanceCheck
  DamageResistanceDegreeOutcomes
  EffectResistanceWaiverRules
  ImperviousSkipsUnneededAttackRoll
  SuffocationFortitudeEscalation
  ToughnessResistanceAfterDamageHit
Skill
  AcrobaticsMitigateFallDistance
  CloseCombatSkillSpecialization
  InteractionSkill
  InvestigationVersusPerceptionSearch
  SkillCatalog
  TechnologyInventingPrerequisite
  TechnologyRepairDamagedObjects
  TechnologySkillHQCommunicationsUse
SkillCheck
  CovertMessageSkillExchange
  ExpertiseRoutineAndPlayerBoundary
  InsightVersusIllusion
  OpposedSkillPairing
  PersuasionAttitudeShift
  SleightOfHandContortionAndObservation
  StealthTailingProcedure
  TreatmentDiagnosisAndAilmentAssist
SkillCheckPicksEffectTask

## Concepts and evidence

### Ability

ABILITY RANKS .............. 107

Buying Ability Ranks ..........107

— HeroesHandbook, chunk unit_00015, section_path: CHAPTER 3: ABILITIES ........107 / ABILITY RANKS .............. 107

### Awareness

AWARENESS (AWE)

While Intellect covers reasoning, Awareness describes common sense and intuition, what some might call “wis- dom.” A character with a high Intellect and a low Aware- ness may be an “absent-minded professor” type, smart but not always aware of what’s going on. On the other hand, a not so bright (low Intellect) character may have great deal of common sense (high Awareness). Your Awareness modifier applies to:

• Will defense, for resisting attacks on your mind. • •

Insight and Perception skill checks. Awareness checks to resolve matters of intuition when a specific skill doesn’t apply.

— HeroesHandbook, chunk unit_00793_merged, section_path: FIGHTING (FGT) / AWARENESS (AWE)

### ConstructAdvantageAbilityGate

ADVANTAGES

Constructs can have advantages at the same cost as other characters. Some advantages are less useful or even use- less to constructs and, like skills, constructs cannot have advantages requiring abilities they lack.

— HeroesHandbook, chunk unit_03751, section_path: SKILLS / ADVANTAGES

### Stamina

STAMINA (STA)

Stamina is health, endurance, and overall physical resil- ience. Stamina is important because it affects a charac- ter’s ability to resist most forms of damage. Your Stamina modifier applies to:

• • •

Toughness defense, for resisting damage. Fortitude defense, for resisting effects targeting your character’s health. Stamina checks to resist or recover from things af- fecting your character’s health when a specific de- fense doesn’t apply.

— HeroesHandbook, chunk unit_00775_merged, section_path: INTELLECT (INT) / STAMINA (STA)

### StaminaBreathHoldRoundBudget

SUFFOCATION

Characters can hold their breath for ten rounds (one min- ute) plus a number of rounds equal to twice their Stamina. After that time they must make a Fortitude check (DC 10) each round to continue holding their breath. The DC in- creases by +1 for each previous success. Failure on the Fortitude check means the character becomes incapaci- tated . On the following round the character is dying. A dy- ing character cannot stabilize until able to breathe again. Heroes with Immunity to Suffocation can go an unlimited time without air. A fall inflicts damage rank 4 plus twice the distance rank fallen, to a maximum of rank 16 damage. Characters with the Acrobatics skill can fall greater distances without risk of damage. Falling into or onto a dangerous surface may cause additional damage, at the GM’s discretion. Catching a falling person or object requires a Dexterity check (DC 5). If you successfully catch a falling object, subtract your Strength rank from the falling damage rank. Both you and the object suffer any remaining dam- age. So if a character with Strength 6 catches someone falling for 12 damage, subtract 6 from 12, and both char- acters resist damage 6. If the catcher is using a power— such as Flight or Move Object—to catch the falling ob- ject, the power’s rank can be substituted for Strength at the GM’s discretion.

— HeroesHandbook, chunk unit_03995, section_path: STARVATION AND THIRST / SUFFOCATION

### AbilityRank

ABILITY RANKS .............. 107

Buying Ability Ranks ..........107

— HeroesHandbook, chunk unit_00015, section_path: CHAPTER 3: ABILITIES ........107 / ABILITY RANKS .............. 107

### AbilityRankPurchase

BUYING ABILITY RANKS

You choose your hero’s ability ranks by spending power points on them. Increasing an ability rank by 1 costs 2 power points, so putting two points into Strength, for ex- ample, raises it from 0 to 1. Remember a rank of 0 is av- erage, 2 is a fair amount of talent or natural ability, 3 is exceptional, 4 extraordinary, and so forth. (See the Ability Benchmarks table for guidelines.)

— HeroesHandbook, chunk unit_00749, section_path: ABILITY RANKS / BUYING ABILITY RANKS

* * *

ALTERING ABILITIES

Over the course of play, your hero’s ability ranks may change for the following reasons:

Some power effects raise or lower ability ranks (see the Powers chapter). You can improve ability ranks permanently by spend- ing earned power points on them, but you cannot increase an ability rank above the limits set by the series’ power level (see Power Level, page 24). Whenever an ability rank changes, all traits associated with the ability change as well. So if you increase your character’s Agility, his Agility-based skills and Dodge de- fense also increase. Likewise, if the hero’s Agility bonus decreases, his Agility-based skills and Dodge suffer.

— HeroesHandbook, chunk unit_00810_merged, section_path: DELUXE HERO’S HANDBOOK / ALTERING ABILITIES

### InteractionTargetMentalThreshold

INTERACTION SKILLS

Certain skills, called interaction skills, are aimed at deal- ing with others through social interaction. Interaction skills allow you to influence the attitudes of others and get them to cooperate with you in one way or another. Since interaction skills are intended for dealing with others so- cially, they have certain requirements. First, you must be able to interact with the subject(s) of the skill. They must be aware of you and able to under- stand you. If they can’t hear or understand you for some reason, you have a –5 circumstance penalty to your skill check (see Circumstance Modifiers in The Basics). Interaction skills work best on intelligent subjects, ones with an Intellect rank of –4 or better. You can use them on creatures with Int –5, but again with a –5 circumstance penalty; they’re just too dumb to get the subtleties of your point. You can’t use interaction skills at all on sub- jects lacking one or more mental abilities. (Try convincing a rock to be your friend—or afraid of you—sometime.)

— HeroesHandbook, chunk unit_00907, section_path: SKILL BENCHMARKS / INTERACTION SKILLS

### AlternateEffectArray

Arrays—collections of Alternate Effects—are one of the more complex and important constructs in MUTANTS & MASTERMINDS and require some special care in terms of their creation and use. Players should take these things into account when creating characters with arrays, and Gamemasters should consider them when approving such characters and dealing with them in play. The main reason for the Alternate Effect modifier is to allow a degree of flexibility in terms of a character’s power effects within the cost restrictions laid down by having a finite number of power points. It’s based on the assumption that a wide range of powers has a diminishing return in terms of value, since characters can only use so many effects at once. A power with various “settings,” usable one at a time, is more valuable than a power with only one, but not as valuable as various effects all usable at the same time. However, Alternate Effect can be abused to try and squeeze the most “efficiency” out of a character’s power points, gain- ing the most effects for the lowest cost. The guidelines for Alternate Effects are intended to help limit this somewhat, but there is no way they can eliminate the possibility entirely and still provide all the benefits of flexibility they’re intended to offer. Some Gamemaster oversight is therefore necessary when it comes to the creation and use of arrays. Before giving a character Alternate Effects, it is wise to ask, “Is an array really needed for this concept?” Some concepts, such as a variety of different attacks, clearly call for an array. Others, like a power with a few rarely used stunts, may not call for an array. Such a power may be better served by acquiring such occasional stunts through extra effort and the spend- ing of hero points rather than the creation of a permanent set of Alternate Effects. That is what the power stunts rules are for, after all: so you do not have to fill up character sheets with minor Alternate Effects a hero will rarely ever use. If you decide an array is appropriate, the first thing is to determine its overall theme and associated descriptors. Is it an ar- ray of different attacks, like a “weapons array” of a battlesuit? Is it a collection of regular power stunts for a themed power like earth control, or spells for magic? Is it a series of alternate forms for a metamorph? And so forth. Arrays should have some unifying theme beyond “all the powers I want my hero to have,” and Gamemasters should feel free to veto inap- propriate arrays lacking a strong theme. effects in the array, its cost is discounted in terms of the “free” points they have to spend. Like any power, an Alternate Effect may be made up of two or more effects, but their total cost cannot exceed the cost of the primary effect.

— HeroesHandbook, chunk unit_02751_s1, section_path: DELUXE HERO’S HANDBOOK / UNDER THE HOOD: ALTERNATE EFFECTS

* * *

ALTERNATE EQUIPMENT

Just as with power effects, there is a diminishing value in having multiple items with a similar function, or a single piece of equipment with multiple functions, usable only one at a time. Equipment can have the Alternate Effect modifier (see the Extras section of the Powers chapter), such as a weapon capable of different modes of opera- tion, or a reconfigurable tool. Characters can also have Alternate Equipment, an array of items usable only one at a time. This is typically a multi- function item, or a kit or collection of various smaller items. The classic example is the utility belt (see its de- scription later in this chapter). Alternate Equipment can also include things like an arsenal of weapons the char- acter can swap out, providing different sets of weapons, with only a limited number usable at once. Characters may not necessarily carry all their equipment with them at all times. The GM may allow players to spend a hero point in order to have a particular item of equip- ment “on-hand” at a particular time. This is essentially an equipment “power stunt”—a one-time use of the item for one scene—and the Gamemaster rules whether or not having a particular item on-hand is even possible. For example, a hero out for an evening in his secret identity might have something like a concealed weapon or other small item on-hand, but it’s unlikely the character is carry- ing a large weapon or item unless he has some means of concealing it.

— HeroesHandbook, chunk unit_03248, section_path: EQUIPMENT EFFECTS AND FEATURES / ALTERNATE EQUIPMENT

### Check

CHECKS

Your hero stands perched on the rooftop, looking down through the skylight. In the abandoned warehouse below, the villain throws the switch that begins lowering your hero’s friends into the vat of boiling acid! You turn to the Gamemaster and say: “I leap down, smashing through the skylight, swing over to the catwalk, kick the bad guy out of the way, then flip the switch to stop the lowering mechanism!” How exactly do you do that in the game? Whenever a character in MUTANTS & MASTERMINDS attempts something where the outcome is in doubt, it requires a check of an appropriate trait: ability, skill, power, etc. (also known as a “trait check” or a “[fill-in trait name]” check, like a “Dexterity check,” for example). Make a check by rolling the die, adding the appropriate rank, and comparing the result against a difficulty class (DC): if your result equals or exceeds the DC, you succeed. If it does not, then your attempt fails. Sometimes how much you exceed or fail to exceed the DC matters, but of- ten it is simply whether you do or not that counts. Check = d20 + ability vs. difficulty class So in the previous example, how many checks are there? Let’s break things down and look at what the hero is doing:

— HeroesHandbook, chunk unit_00266, section_path: GAME PLAY / CHECKS

* * *

DIFFICULTY CLASS

Checks are made against a difficulty class or DC, a num- ber set by the GM, which your check must equal or exceed to achieve success. So for a task with a DC of 15 you must roll a check total of 15 or greater to succeed. In some cas- es, the results of a check vary based on how much higher or lower the result is than the DC, known as its degree of success or failure.

— HeroesHandbook, chunk unit_00282, section_path: CRITICAL SUCCESS / DIFFICULTY CLASS

### AcrobaticsTaskMenu

TASK

Lessen damage from a fall (–1 per degree) Acrobatic maneuver Move from prone to standing as a free action Contort to fit through a tight space

— HeroesHandbook, chunk unit_00965, section_path: DC / TASK

### AllOutAttackDefenseForAttackTrade

ALL-OUT ATTACK

When you make an attack you can take a penalty of up to –2 on your active defenses (Dodge and Parry) and add the same number (up to +2) to your attack bonus. Your defense bonuses cannot be reduced below +0 and your attack bonus cannot more than double. The changes to attack and defense bonus are declared before you make the attack check and last until the start of your next turn.

— HeroesHandbook, chunk unit_04242, section_path: DEMORALIZE / ALL-OUT ATTACK

### AreaAndPerceptionAutomaticEffectResolution

RECOVERY

0 0 1 1 1 3 5 7 8 9 15 20+ Perception and Area effects do not require attack checks, they automatically affect a given target or area (see the Area extra in the Powers chapter). Because of this, these attacks cannot score critical hits or misses, nor do modifi- ers affecting the attack check—including various maneu- vers—affect them.

— HeroesHandbook, chunk unit_04108, section_path: PERCEPTION AND AREA EFFECTS / RECOVERY

### AttackCheckVersusDefenseClass

ATTACKS

An attack check represents an attempt to hit a target with an attack. When you make an attack check, roll the die and add your bonus with that attack. If your result equals or exceeds the target’s defense, your attack hits and may have some effect. Attack Check = d20 + attack bonus vs. defense class

— HeroesHandbook, chunk unit_04040, section_path: CONFLICTS / ATTACKS

### ClimbCircumstanceModifierTable

CIRCUMSTANCE MODIFIERS

An air duct, chimney, or other area where you can brace against two opposite walls A corner where you can brace against perpendicular walls Climb of less than 10 feet total Surface slightly slippery Surface very slippery +1 speed rank (up to your full speed) Not vulnerable while climbing

— HeroesHandbook, chunk unit_00978, section_path: EXAMPLE SURFACE / CIRCUMSTANCE MODIFIERS

### CriticalSuccess

CRITICAL SUCCESS

If you roll a 20 on the die when making a check you’ve scored a critical success. Determine the degree of success normally and then increase it by one degree. This can turn a low-level success into something more significant, but more importantly, it can turn a failure into a full-fledged success! A critical success with an attack check is called a critical hit, discussed later in this chapter and in the Ac- tion & Adventure chapter.

— HeroesHandbook, chunk unit_00280, section_path: DELUXE HERO’S HANDBOOK / CRITICAL SUCCESS

### ForensicEvidenceAnalysisCheck

ANALYZE EVIDENCE

• • • •

You can make an Investigation check to apply forensic knowledge to evidence. This function of Investigation does not give you clues where none exist. It simply allows you to extract useful information from evidence and clues you have found. The base DC 15, modified by the time elapsed since the evidence was left, and whether or not the scene was dis- turbed. Success gives you information based on the clue (and determined by the GM). Two or more degrees of fail- ure may provide misleading or confusing evidence, also at the GM’s discretion.

— HeroesHandbook, chunk unit_01130_merged, section_path: GATHER EVIDENCE / ANALYZE EVIDENCE

### InitiativeCheck

INITIATIVE

When things start happening quickly, MUTANTS & MASTER- MINDS characters use their initiative bonuses to determine who goes first. Each character involved in a conflict makes a check of d20 + initiative modifier, which is: Initiative Modifier = Agility + Advantages (Improved Initiative) + Power Modifiers Characters then act in initiative order, from highest to low- est. For details see the Action & Adventure chapter.

— HeroesHandbook, chunk unit_00862, section_path: RESISTANCE CHECKS / INITIATIVE

### JuryRiggedRepairCheck

JURY-RIGGING

You can also attempt jury-rigged, or temporary, repairs. Doing this reduces the repair DC by an additional 5 (for a total of –10 to the DC to build the item), and allows you to make the Technology check as a standard action. Howev- er, a jury-rigged repair can only fix a single problem, and the repair only lasts until the end of the scene. The jury- rigged item must be fully repaired thereafter, and cannot be jury-rigged again until it is fully repaired. Intellect • Trained Only • Manipulation • Requires Tools

— HeroesHandbook, chunk unit_01226, section_path: REPAIRING / JURY-RIGGING

### OpposedCheck

OPPOSED CHECKS

Some checks are opposed. They are made against an- other character’s check result as the DC. Whoever gets the higher result wins. An example is trying to bluff someone. You roll a Deception check, while the GM rolls an Insight check for your target. If you beat the target’s Insight check result, you succeed. For ties on opposed checks, the character with the higher bonus wins. If the bonuses are the same, roll d20. On a 1–10, one character wins, and on an 11–20, victory goes to the other character; decide which character is “high” and which is “low” before rolling. Opposed checks offer the Gamemaster a useful tool for comparing the efforts of two characters quickly and eas- ily. This applies not only to skills, but also powers and, in some cases, abilities. If two or more characters compete at a particular task, you can resolve it with an opposed check. The character with the highest check result wins. Of course, you can play things out if you want, but sometimes it’s good to be able to resolve things with a quick opposed check and move on. As Gamemaster, if you find yourself without a particular rule to resolve a conflict or contest between characters, the opposed check is your friend. Pick the appropriate skill, power, or ability, make checks for the characters and compare the results to see how they did. opposing character’s modifier +10, just like the result of a routine check (previously). Active defenses in combat, where characters are focusing on other actions, are generally routine opposition, which is why attack checks are made against a DC of 10 + the ap- propriate defense. Active opposed checks in combat are an option when a character goes on the defensive. See Defend in the Action & Adventure chapter for details.

— HeroesHandbook, chunk unit_00326, section_path: DC–20 / OPPOSED CHECKS

### OptionalInitiativeForTimedChallenge

CHALLENGES AND INITIATIVE

Challenges may or may not involve initiative checks, de- pending on the nature of the challenge. If all of the characters get a turn and it does not particu- larly matter who goes first, then the Gamemaster can dis- pense with initiative for the challenge. For example, if the heroes all have to leap across a chasm, then it is a chal- lenge they must all complete, and it does not particularly matter which of them goes first or last in doing so (since their actions are all virtually simultaneous). With other challenges, it does matter who goes first, par- ticular when the challenge is timed in some fashion. So, for example, if the GM determines that part of a burning building will collapse after the first round, initiative may be checked to see which heroes go before the collapse and who does not quite act fast enough. The same may be true of other traps or hazards, which can have initiative ranks of their own.

— HeroesHandbook, chunk unit_03970, section_path: CHALLENGES / CHALLENGES AND INITIATIVE

### PrecariousSurfaceMovementCheck

BALANCING

You can keep your balance and move along a precari- ous surface at your ground speed minus 1 rank with a successful Acrobatics check against the surface’s DC. A degree of failure indicates you spend your move action just maintaining your balance and do not actually move, while two or more degrees of failure means you lose your balance and fall.

— HeroesHandbook, chunk unit_00937, section_path: ACROBATICS / BALANCING

### ReactionVersusFreeActionTiming

REACTION

A reaction is something that happens in response to something else, like a reflex. Like free actions, reactions take so little time they’re considered free. The difference between the two is a free action is a conscious choice made on the character’s turn to act. A reaction can oc- cur even when it’s not your turn to act. Some powers and other traits are usable as reactions.

— HeroesHandbook, chunk unit_03937, section_path: FREE ACTION / REACTION

### RoutineAttackCheckAgainstMinion

MINIONS

Minions are minor characters subject to special rules in combat, and generally easier to defeat than normal char- acters. Villains often employ hordes of minions against heroes. The following rules apply to minions:

• Minions cannot score critical hits against non-min-

ions.

• •

Non-minions can make attack checks against min- ions as routine checks. If a minion fails a resistance check, the minion suffers the worst degree of the effect. So a minion failing a So a hero with Parry 11 has a defense class of 21 (11 + 10) against close attacks. If the same hero has Dodge 9, that is a defense class of 19 (9 + 10) against ranged attacks.

— HeroesHandbook, chunk unit_04128_merged, section_path: DEFENSES / MINIONS

### SkillCheckModifierSources

MISCELLANEOUS MODIFIERS

Miscellaneous modifiers to skill checks include modifiers for circumstances, and bonuses from advantages or pow- ers, among others. The higher the total, the better the result. You’re usually look- ing for a total that equals or exceeds a particular difficulty class (DC), which may be based on another character’s traits.

— HeroesHandbook, chunk unit_00891, section_path: ABILITY MODIFIER / MISCELLANEOUS MODIFIERS

### StandardAndMoveActionPerCombatRound

STANDARD ACTION

A standard action allows you to do something. You can make an attack, use a skill, advantage, or power, or per- form other similar actions. During a combat round, you can take a standard action and a move action.

— HeroesHandbook, chunk unit_03921, section_path: ACTION TYPES / STANDARD ACTION

### ToolingPenalty

TOOLS

Some tasks require tools. If tools are needed, the spe- cific items are mentioned in the description of the task or skill. If you don’t have the appropriate tools, you may still be able to attempt the task, but at a major disadvan- tage, for a –5 circumstance penalty on your check, if the GM decides you can attempt the task at all. A character may be able to put together makeshift tools in order to make the check. If the GM allows this, reduce the circumstance penalty to –2.

— HeroesHandbook, chunk unit_00347, section_path: UNDER THE HOOD: CIRCUMSTANCES / TOOLS

### UltimateEffortFixedResult

SAMPLE ULTIMATE EFFORTS

The following are some potential Ultimate Efforts. The GM is free to add others suitable to the series.

• • •

Ultimate Aim: When you take a standard action to aim an attack (see Aim, page 246), you can spend a hero point to apply a 20 result to the attack check on the following round. Since the Ultimate Aim bonus is not a natural 20, it also does not qualify as an auto- matic or critical hit. Ultimate Resistance: You can spend a hero point to apply a 20 result to a resistance check with one de- fense determined when you acquire this advantage. Ultimate Skill: You can spend a hero point to apply a 20 result to checks with a particular skill.

— HeroesHandbook, chunk unit_01644_merged, section_path: DELUXE HERO’S HANDBOOK / SAMPLE ULTIMATE EFFORTS

### Condition

CONDITIONS

Heroes run into their share of difficulties in their work. One way MUTANTS & MASTERMINDS measures this is with dif- ferent conditions. They are shorthand for the different game modifiers imposed by things from power effects to injuries or fatigue. So, for example, “vulnerable” is a condi- tion where a hero’s active defenses are reduced. An oppo- nent grabbing them or an entangling mass of glue might make heroes vulnerable, or they might be made vulner- able by a foe’s cunning combat maneuver or being caught off-guard. The game effect is the same (the hero’s active defenses are reduced), so it is easier to just refer to the overall condition as “vulnerable” and describe the differ- ent situations that cause it. This section describes the different conditions that can af- fect characters in MUTANTS & MASTERMINDS. If multiple condi- tions apply, use all of their effects. Some conditions super- sede other, lesser, conditions, as given in their descriptions.

— HeroesHandbook, chunk unit_00385, section_path: DELUXE HERO’S HANDBOOK / CONDITIONS

### ActiveDefenseDegradation

ACTIVE DEFENSES

Dodge and Parry defenses require a measure of action to be fully effective. Limits on your mobility, focus, and reac- tion time adversely affect them. If you are vulnerable, your Dodge and Parry defense ranks are halved (divide their normal values by 2 and round up), and if you are defense- less, they are both reduced to 0!

— HeroesHandbook, chunk unit_00856, section_path: TOUGHNESS RANK / ACTIVE DEFENSES

* * *

DEFENSES & INITIATIVE

Heroes face many hazards in their line of work, from attacks by villainous foes to traps and fiendish mind control. A hero’s defenses are abilities used to avoid such things, determining the difficulty to affect a hero with an attack, or to make resistance checks against them. Each defense is based on a particular ability, modified by the hero’s advantages and powers. For more on defenses in general and how you use them, see Chapter 8.

— HeroesHandbook, chunk unit_00835, section_path: DELUXE HERO’S HANDBOOK / DEFENSES & INITIATIVE

### BasicCondition

BASIC CONDITIONS

Each basic condition describes a single game modifier. They are the “building blocks” of conditions, much as ef- fects are the basic building blocks of powers. Indeed, many power effects reference these basic conditions in the descriptions of what they do. See the Powers chapter for details.

• • • • •

Compelled: A compelled character is directed by an outside force, but struggling against it; the character is limited to free actions and a single standard action per turn, with both types of action being chosen by another, controlling character. As usual, this standard action can be traded for a move action. Controlled supersedes compelled. Controlled: A controlled character has no free will; the character’s actions each turn are dictated by an- other, controlling, character. Dazed: A dazed character is limited to free actions and a single standard action per turn, although the character may use that action to perform a move, as usual. Stunned supersedes dazed. Debilitated: The character has one or more abilities lowered below –5. (See Debilitated Abilities in the Abilities chapter.) Defenseless: A defenseless character has active de- fense bonuses of 0. Attackers can make attacks on defenseless opponents as routine checks (see Rou- tine Checks). If the attacker chooses to forgo the rou- tine check and make a normal attack check, any hit is treated as a critical hit (see Critical Hits, page 240). Defenseless characters are often prone, providing opponents with an additional bonus to attack checks (see Prone, later in this section).

— HeroesHandbook, chunk unit_00387_merged, section_path: CONDITIONS / BASIC CONDITIONS

* * *

hand” for talking about a group of basic conditions that go together in a particular circumstance, much like a pow- er is a collection of basic effects. The individual conditions making up a combined condi- tion can be resolved individually. For example, if an effect that removes the dazed condition is used on a staggered character (who is dazed and hindered), then the character is no longer dazed, only hindered. Similarly, if an effect im- poses a condition that supersedes part of the combined condition, only that part changes. So an effect that stuns a staggered character means the character is now stunned (superseding dazed) and hindered. Similarly, an effect that immobilizes a staggered character leaves the target dazed and immobile (superseding the hindered element of the combined condition).

— HeroesHandbook, chunk unit_00412, section_path: DELUXE HERO’S HANDBOOK / DELUXE HERO’S HANDBOOK

### ConditionsFromResistanceFailure

CONDITIONS

A failed resistance check against an attack imposes one or more conditions on the target, depending on the type of effect and the degree of failure. See the effect descrip- tion and the Conditions section of The Basics chapter for more on the various conditions.

— HeroesHandbook, chunk unit_04147, section_path: ONGOING EFFECTS / CONDITIONS

### DamageConditionMinuteRecovery

RECOVERY

As a result of conflict, characters often suffer adverse con- ditions (see Conditions in The Basics chapter) from being knocked around and hit with different powers. The spe- cific conditions are discussed in the effects defined in the Powers chapter, particularly Affliction and Damage, the most common effects of conflicts. Living targets remove one damage condition per minute of rest, starting from their most severe condition and working back. So a damaged character recovers from being inca- pacitated, then staggered, dazed, and finally removes a –1 Toughness check penalty per minute until fully recovered. The Healing and Regeneration effects can speed this process. Objects, having no Stamina, do not recover from damage unless they have an effect like Regeneration. Instead, they must be repaired. See the guidelines under the Technol- ogy skill when repairing damaged object.

— HeroesHandbook, chunk unit_04279, section_path: TEAM ATTACK / RECOVERY

* * *

DELUXE HERO’S HANDBOOK

The Healing and Regeneration effects can speed this pro- cess. Lasting or more serious injuries are handled as com- plications (see Lasting Injuries). Objects, having no Stamina, do not recover from damage unless they have an effect like Regeneration. Instead, they must be repaired. See the guidelines under the Technol- ogy skill when repairing damaged objects.

— HeroesHandbook, chunk unit_04100, section_path: DELUXE HERO’S HANDBOOK / DELUXE HERO’S HANDBOOK

### HeroDeathVersusMinionLethality

DEATH

Character death is a relatively rare happenstance in the comic books. Technically, it’s not so much rare as it is temporary. The tendency of comic book characters to return from the dead has become so commonplace it is cliché, with various stories and characters poking fun at it. The MUTANTS & MASTERMINDS rules make character death a similarly rare occurrence. Characters generally only acquire the dying condition after being incapacitated and suffering further harm, which usually means someone is actively trying to kill them. Even then, dying characters have opportunities to stabilize and stave off death. It takes a second active effort to kill a dying character outright, so accidental death due to a single bad die roll is all but impossible for the major characters in a series. Note that none of this applies to minions, who can be killed simply with a successful attack and a declaration of intent to do so. While heroes in a four-color or mainstream style game generally refrain from killing, minions can get mowed down by the dozens in gritty Iron Age style games. The Gamemaster can also kill off supporting characters as desired to suit the story. The greater “resilience” of main characters is not because they are physically any different or tougher, just that they are literally more important to the story of the game. Bonuses to Toughness protect against slam attack dam- age normally. Immunity to slam damage you inflict is a rank 2 Immunity effect, while Immunity to all slam dam- age is rank 5 (see Immunity in the Powers chapter).

— HeroesHandbook, chunk unit_04273, section_path: DELUXE HERO’S HANDBOOK / DEATH

### IntimidationDemoralize

DEMORALIZING

You can use Intimidation in combat as a standard action to undermine an opponent’s confidence. Make an Intimi- dation check as a standard action. If it succeeds, your tar- get is impaired (a –2 circumstance penalty on checks) un- til the end of your next round. With four or more degrees of success, the target is disabled (a –5 penalty) until the end of your next round.

— HeroesHandbook, chunk unit_01107, section_path: DELUXE HERO’S HANDBOOK / DEMORALIZING

### MinionCombatResolutionPackage

MINIONS

Minions are minor characters subject to special rules in combat, and generally easier to defeat than normal char- acters. Villains often employ hordes of minions against heroes. The following rules apply to minions:

• Minions cannot score critical hits against non-min-

ions.

• •

Non-minions can make attack checks against min- ions as routine checks. If a minion fails a resistance check, the minion suffers the worst degree of the effect. So a minion failing a So a hero with Parry 11 has a defense class of 21 (11 + 10) against close attacks. If the same hero has Dodge 9, that is a defense class of 19 (9 + 10) against ranged attacks.

— HeroesHandbook, chunk unit_04128_merged, section_path: DEFENSES / MINIONS

### TurnStartEndsUntilNextTurnEffects

STARTING YOUR TURN

The Gamemaster informs you when it is your turn. When you start your turn, you should:

End effects that last “until the start of your next turn”.

— HeroesHandbook, chunk unit_03943_merged, section_path: TAKING YOUR TURN / STARTING YOUR TURN

### CoveringAttack

COVERING ATTACK

by your covering attack at the cost of being automati- cally attacked by it; make a normal attack check to hit that opponent.

— HeroesHandbook, chunk unit_02878, section_path: MULTIPLE TARGETS / COVERING ATTACK

### DescriptorLayer

TYPES OF DESCRIPTORS

Descriptors come in many different forms. The break- down in this section is inexact, and deliberately so; some descriptors fall into more than one category, while others might not fall into any of these categories, being unique to that particular character or power. Still, the following are the major types of descriptors suited to MUTANTS & MAS- TERMINDS powers, and things to consider when creating or choosing powers for a character.

— HeroesHandbook, chunk unit_03090, section_path: DESCRIPTORS / TYPES OF DESCRIPTORS

* * *

RESULT

Lastly, a power’s result is what happens when the power is used beyond just the game mechanics of its effect. For example, the rules of the Affliction ef- fect describe the penalties suffered by the target, but they don’t describe the result, the nature of the Affliction itself. Is it glow- ing bonds of energy, sudden fever and dizziness, a curse of misfortune, a life- sapping vapor, or any number of other things? Result descriptors tend to be fairly broad, given the potential range of results avail- able to effects in the game. Some powers may not have or need result descriptors; after all, “Mind Control” is a pretty clear description of a result. However, “an in- duced trance where the human brain becomes capable of accepting neurolin- guistic programming inputs” is also a valid descriptor for that same effect. Like medium descriptors, result descriptors may or may not match others the power al- ready has. Take a taser-like weapon able to stun the nervous system of its target: it has an invented origin (someone designed and built it), a techno- logical source (it’s a technological device with a battery), uses a energy medium (an electrical shock), and results in an electrical overload of the tar- get’s nervous system (the result descriptor for its Affliction effect). This tells us a lot about that particular power and ways it might interact with other effects.

— HeroesHandbook, chunk unit_03129, section_path: DELUXE HERO’S HANDBOOK / RESULT

* * *

APPLYING DESCRIPTORS IN PLAY

While descriptors are generally applied to powers when those powers are defined (that is, when a character is created), in some cases, certain descriptors may be left unspecified and defined during play. This can either be because nobody thought to define the descriptor in ad- vance, or it was deliberately left vague, to be filled-in later. So, for example, a particular heroine might not know the origin or source of her powers, and her player doesn’t want to know, leaving them a mystery for later development in the game. The GM agrees and so the heroine’s powers have no origin or source descriptors. Instead, the GM chooses them, which isn’t known until the heroine is subject to an anti-magical field and discovers her powers don’t work! The GM awards the player a hero point for the unexpected set- back and now the source of the heroine’s powers is known, although their origin still remains a mystery…. Applying descriptors in play gives you a lot of flexibility, letting you handle certain things “on the fly” rather than having to describe every aspect of a character in excruci- ating detail beforehand. The key tool for handling the ap- plication of descriptors in play is the use of hero points. If applying a new descriptor is a setback for the hero, then award the player a hero point, just like any other setback (see Complications, page 30). If the new descriptor is chosen by the player and gives the hero a minor advan- tage, you might ask the player to pay a hero point for the privilege, although you can balance this with an immedi- ate hero point award for the clever idea, if you want (mak- ing the hero point a token expenditure). If it’s neither, then there’s no hero point cost, just apply the descriptor.

— HeroesHandbook, chunk unit_03142, section_path: DELUXE HERO’S HANDBOOK / APPLYING DESCRIPTORS IN PLAY

### DifficultyClass

DIFFICULTY CLASS

Checks are made against a difficulty class or DC, a num- ber set by the GM, which your check must equal or exceed to achieve success. So for a task with a DC of 15 you must roll a check total of 15 or greater to succeed. In some cas- es, the results of a check vary based on how much higher or lower the result is than the DC, known as its degree of success or failure.

— HeroesHandbook, chunk unit_00282, section_path: CRITICAL SUCCESS / DIFFICULTY CLASS

### CatchFallingTargetDexterityDC

SUFFOCATION

Characters can hold their breath for ten rounds (one min- ute) plus a number of rounds equal to twice their Stamina. After that time they must make a Fortitude check (DC 10) each round to continue holding their breath. The DC in- creases by +1 for each previous success. Failure on the Fortitude check means the character becomes incapaci- tated . On the following round the character is dying. A dy- ing character cannot stabilize until able to breathe again. Heroes with Immunity to Suffocation can go an unlimited time without air. A fall inflicts damage rank 4 plus twice the distance rank fallen, to a maximum of rank 16 damage. Characters with the Acrobatics skill can fall greater distances without risk of damage. Falling into or onto a dangerous surface may cause additional damage, at the GM’s discretion. Catching a falling person or object requires a Dexterity check (DC 5). If you successfully catch a falling object, subtract your Strength rank from the falling damage rank. Both you and the object suffer any remaining dam- age. So if a character with Strength 6 catches someone falling for 12 damage, subtract 6 from 12, and both char- acters resist damage 6. If the catcher is using a power— such as Flight or Move Object—to catch the falling ob- ject, the power’s rank can be substituted for Strength at the GM’s discretion.

— HeroesHandbook, chunk unit_03995, section_path: STARVATION AND THIRST / SUFFOCATION

### DeceptionBelievabilityDCAdjustment

MODIFIER

The target wants to believe you. The deception is believable and doesn’t affect the target much either way. The deception is a little hard to believe or puts the target at some kind of risk. The deception is difficult to believe or entails a serious risk. The deception is way out there, almost too incredible to consider. –5 +0 +5 +10 +20 There are a number of factors to consider when choosing skills for your MUTANTS & MASTERMINDS character.

— HeroesHandbook, chunk unit_01026, section_path: RESISTANCE CIRCUMSTANCE / MODIFIER

### SecurityOrTrapDCLadder

DC

10 15 20 25 30 35 40 +5 Failure on your skill check means nothing happens, but you can keep trying. More than one degree of failure sets off the security or trap, if it is possible to do so. 128128

— HeroesHandbook, chunk unit_01256, section_path: MODIFIERS / DC

### TechnologyRestrictedCommunicationsDC

COMMUNICATIONS

The communications feature allows the headquarters to receive and transmit on a wide range of radio and TV bands, monitor police and emergency channels, coor- dinate communications between members of a team, and so forth. It includes communications equipment, consoles, and monitors. The system’s access to restricted communication bands depends on the clearance and skills of the user. Heroes often have access to special government channels, while a successful Technology skill check (DC 25) can grant a user illegal access to re- stricted systems.

— HeroesHandbook, chunk unit_03622, section_path: DELUXE HERO’S HANDBOOK / COMMUNICATIONS

### VisualPerceptionVisibilityDC

SEEING

Make a check against a DC based on how visible the ob- ject is or against an opposed Stealth check. Something in plain sight is DC 0, while something subtle or easily over- looked may be DC 5, 10 or more. Visual perception is also used to detect someone in disguise (see the Deception skill) or to notice a concealed object (see the Sleight of Hand skill).

— HeroesHandbook, chunk unit_01160, section_path: HEARING / SEEING

### MeasurementTable

THINGS TO KNOW ABOUT MEASUREMENTS

When using the Measurements Table, there are a few important things to keep in mind:

• • •

Each rank represents a range of measures. Time rank 4 is actually all measures between 1 and 2 minutes, and time rank 16 is everything between 2 and 4 days! So if you’re looking for a measurement that’s not on the table, pick the next highest one that is; so 12 hours is a time rank of 13 (more than 8 hours, but less than 16), and 6 miles is a distance rank of 11 (more than 4 miles, but less than 8). Like abilities, measures can have negative ranks. In the time rank example, the time it takes a Speed 14 hero to cover 30 miles is rank –1, or 3 seconds. You can extend the negative side the Measurement Table just like you can the positive side, with each lower rank halving the previous measurement. So rank –6 is half a pound, 1/16th of a second, and 3 inches, for example. Don’t directly add ranks. Putting rank 4 distance together with rank 6 distance is not rank 10 distance! Rank 4 is a distance measurement of 500 feet. Rank 6 is 600 yards (1,800 feet). Adding the measurements, you get about 2,300 feet. If you directly added the ranks, you’d get rank 10 distance, or 4 miles! If you have different ranks, it is best to either handle them separately or convert them to measurements, add the measurements together, and convert them back to a rank. In the previous example, 2,300 feet is rank 7 distance (around half a mile).

• Measurements are approximate. Especially at

the higher end, where each rank represents a wide range of measurements, the Measurements Table isn’t intended to provide precise values; it’s just a ballpark estimate so you have an idea of how things work in the context of the game. Don’t focus too heavily on precise answers, just use the table for general guidelines.

— HeroesHandbook, chunk unit_00222_merged, section_path: ADVANTAGES / THINGS TO KNOW ABOUT MEASUREMENTS

* * *

RANKS & MEASURES

MUTANTS & MASTERMINDS uses the term rank when talking about the value of a game trait. So you might say a hero has “rank 8 Strength” or simply “Strength 8” (which mean the same thing), or that an effect is rank 5, 9, 15, or what have you. Every quantifiable trait in M&M has a rank as- signed to it. The game also uses a system of measures, real world values like pounds, seconds, minutes, hours, feet, yards, and miles, to name a few. There is a direct relationship between rank and measure, as shown on the Measure- ments Table. (You can find a metric version of the Mea- surements Table in the back of the book.)

— HeroesHandbook, chunk unit_00232, section_path: COMPLICATIONS / RANKS & MEASURES

### AthleticsJumpDistanceFromCheck

JUMPING

The result of an Athletics check is the distance (in feet) you can clear in a running long-jump. If you make a stand- ing jump, divide the distance in half. If you make a verti- cal jump (straight up) divide the distance by 5, and if you make a standing vertical jump, divide it by 10. Your Athletics bonus + 10 is the base distance you can jump under routine circumstances. So a hero with a +10 Athletics bonus can make a routine long-jump of 20 feet, 116116

— HeroesHandbook, chunk unit_00984, section_path: FALLING / JUMPING

### CombatRoundDurationEstimate

ACTION ROUNDS

The action round (or simply round) is how MUTANTS & MASTERMINDS breaks down time when things like who goes first and how much each character can accomplish are important. A round represents about six seconds of time in the game world. During a round, each character involved takes a turn, which is that character’s opportunity to do something. A character has an allotment of actions, used during that character’s turn. Players decide what their characters do on their turns, while the GM handles everyone else’s turn.

— HeroesHandbook, chunk unit_03913, section_path: CHAPTER 8: ACTION & ADVENTURE / ACTION ROUNDS

### EnvironmentalHazardIntensityExamples

FIRE EXAMPLE

Lingering irradiation Nuclear fallout Exposure to radioactive materials Stellar radiation (deep space) Nuclear reactor Nuclear blast 1 2 4 6 8 Torch Campfire Blowtorch Flame thrower Burning jet fuel, napalm 10+ Chemical accelerants and fire powers

— HeroesHandbook, chunk unit_04024, section_path: RANK / FIRE EXAMPLE

### MaterialToughnessOrdinalScale

TOUGHNESS

Paper Soil Glass Ice Rope Wood Stone Iron Reinforced Concrete Steel Titanium Super-alloys

— HeroesHandbook, chunk unit_01997, section_path: MATERIAL / TOUGHNESS

### TimeMeasureRow

TIME

1/8 second 1/4 second 1/2 second 1 second 3 seconds 6 seconds 12 seconds 30 seconds 1 minute 2 minutes 4 minutes 8 minutes 15 minutes 30 minutes 1 hour 2 hours 4 hours 8 hours 16 hours 1 day 2 days 4 days 1 week 2 weeks 1 month 2 months 4 months 8 months 1.5 years 3 years 6 years 12 years 25 years 50 years 100 years 200 years x2

— HeroesHandbook, chunk unit_00248, section_path: MASS / TIME

### OpposedEffectCheck

OVERCOMING ILLUSIONS

Characters encountering an illusion do not receive checks to recognize it as illusory until they interact with it in some fashion. A successful Insight check against an illusion (DC 10 + Illusion rank) reveals it as false. A failed check means the character does not notice anything amiss. A charac- ter faced with clear proof an illusion isn’t real needs no

— HeroesHandbook, chunk unit_02137, section_path: ILLUSIONARY EFFECTS / OVERCOMING ILLUSIONS

* * *

MY ALLY, MY ENEMY

A common Illusion trick is to switch the appearances of an enemy and an ally, causing a foe’s teammate to at- tack that enemy by mistake. You can generally handle this with an opposed check of Illusion and Insight; if you win, the target is unaware of the switch and attacks the wrong target.

— HeroesHandbook, chunk unit_02160, section_path: MENTAL ILLUSIONS / MY ALLY, MY ENEMY

* * *

MIMIC

You can read another character’s mind. To use Mind Read- ing, make an opposed effect check against the result of the target’s Will check. The degree of success determines the degree of contact:

— HeroesHandbook, chunk unit_02269, section_path: SENSORY / MIMIC

### PowerEffect

ACQUIRING POWERS ..... 143

Power Costs ...........................143 Power Descriptors...............143

— HeroesHandbook, chunk unit_00038, section_path: CHAPTER 6: POWERS ........ 143 / ACQUIRING POWERS ..... 143

### Advantage

ADVANTAGES

Halfway between skills and powers, advantages are minor benefits characters have, allowing them to do things oth- ers cannot. They range from special combat maneuvers to things like financial resources, contacts, and so forth. Many advantages have no rank, or rather just one rank; a character either has the advantage (and the benefits that it grants) or does not. Other advantages may have multiple ranks, like abilities and skills, measuring their effectiveness. For details on the various advantages and what they pro- vide, see the Advantages chapter.

— HeroesHandbook, chunk unit_00220, section_path: DELUXE HERO’S HANDBOOK / ADVANTAGES

* * *

6. ADVANTAGES

Choose the advantages you want your character to have and pay 1 power point per advantage or rank in a advan- tage. See the Advantages chapter for details.

— HeroesHandbook, chunk unit_00518, section_path: 5. SKILLS / 6. ADVANTAGES

### AdvantageNameGroupings

ADVANTAGE

Assessment Benefit Diehard Eidetic Memory Equipment Extraordinary Effort Fearless Great Endurance Instant Up Interpose Minion Second Chance Sidekick Teamwork Trance

## ADVANTAGE

Agile Feint Animal Empathy Artificer Attractive Connected Contacts Daze Fascinate Favored Foe Hide in Plain Sight Improvised Tools Inventor Jack-of-all-trades Languages Ritualist Skill Mastery Startle Taunt Tracking Well-informed

— HeroesHandbook, chunk unit_01362_merged, section_path: ADVANTAGE / ADVANTAGE

### AdvantageRankAndDescriptionPattern

ADVANTAGE DESCRIPTIONS

Each advantage is listed by name, type, and if the advan- tage is available in multiple ranks, followed by a descrip- tion of the advantage’s benefits. The effects of additional ranks of the advantage (if any) are noted in the text of each advantage. In some cases a advantage’s description mentions the normal conditions for characters who do not have the advantage for comparison.

— HeroesHandbook, chunk unit_01317, section_path: TYPES OF ADVANTAGES / ADVANTAGE DESCRIPTIONS

### FightingStyleAdvantageBundleExamples

SAMPLE FIGHTING STYLES

Use the following advantage combos as examples of how to create different fighting styles. Students who have not yet mastered a style may have only some of a style’s associated advantages rather than all of them. Any of these fighting styles might include ranks of the Close Attack advantage. Other fighting style advantages might include:

• • • •

Boxing: All-out Attack, Defensive Attack, Improved Critical (Unarmed), Power Attack, Takedown. Judo: Accurate Attack, Defensive Attack, Improved Disarm, Improved Grab, Improved Hold, Improved Trip. Kung Fu: Defensive Attack, Improved Critical (Unarmed), Improved Smash, Improved Trip, Instant Up, Power Attack, Startle. Sword-fighting: Accurate Attack, Defensive Attack, Improved Disarm, Improved Initiative, Power Attack, Taunt.

• Wrestling: Chokehold, Fast Grab, Improved Grab, Improved Hold, Power Attack.

— HeroesHandbook, chunk unit_01423_merged, section_path: MARTIAL ARTS AND FIGHTING STYLES / SAMPLE FIGHTING STYLES

### AlternateFormDescriptorPackages

Energy: You are made up of energy, such as fire or electricity: Damage (close or ranged), Flight, Immunity, Insub- stantial 3, and Teleport (Energy Medium). Gaseous: You are a cloud of gas, like fog or mist: Affliction (Suffocate), Concealment (Visual, Attack), Flight, Immu- nity, and Insubstantial 2. Ghost: You are incorporeal and invisible, largely unaffected by the physical world: Concealment (Visual), Flight, Im- munity, and Insubstantial 4. Heroic: You have a distinct “hero” form, in addition to your “normal” form. Essentially, all your powers have the Activa- tion modifier! The inability to assume your heroic form might also constitute a complication for you from time to time. Liquid: You are made up of liquid (such as water): Affliction (Suffocate), Concealment (Visual, Limited to Underwa- ter), Elongation, Immunity, Insubstantial 1, and Swimming. Particulate: Your body is composed of a granular or particulate substance like sand, dust, salt, and so forth: Dam- age, Elongation, Immunity, Insubstantial 1, and Movement (Slithering). Shadow: You transform into a living shadow: Concealment (Visual, Limited to Darkness and Shadows), Immunity, Insubstantial 4, and Movement (Slithering, Wall-crawling). Solid: You are made up of a hard solid substance like stone or metal: Enhanced Stamina, Enhanced Strength, Im- munity, and Protection. Swarm: Your “body” is actually thousands of other tiny creatures: insects, worms, even little robots: Flight, Immunity, Insubstantial 2, and Movement (Slithering, Wall-crawling). Two-Dimensional: You can flatten yourself to become almost infinitely thin: Concealment (Visual, Limited to One Side), Damage (Penetrating – sharp edges), Insubstantial 1 (for slipping through narrow spaces), and Movement (Slithering). 150150

— HeroesHandbook, chunk unit_01855, section_path: DELUXE HERO’S HANDBOOK / FLAWS

### BlastRangedDamageEffect

BLAST

Effect: Ranged Damage • 2 points per rank You can make a damaging ranged attack. It might be a blast of energy, a projectile (arrow, bullet, throwing blade, etc.), or some similar effect. You make a ranged attack check against the target’s Dodge defense. The attack’s damage equals your power rank and the target makes a Toughness resistance check against it. (leaving the character unable to burrow through dense clay or solid rock), or only snow and ice (being unable to burrow through earth and soil at all). –1 cost per rank.

— HeroesHandbook, chunk unit_01872, section_path: FLAWS / BLAST

### CommunicationLimitedFlaw

FLAWS

Limited: Communication may be limited to only mem- bers of a particular group, such as a species, family, mem- bers of an organization, and so forth. This is in addition to limitations imposed by medium (that is, requiring sub- jects to have a means of picking up on the Communica- tion). –1 cost per rank. itself is already Sense-Dependent: Communication sense-dependent (in that the subject(s) must be able to sense your communication medium to pick up your transmissions) and so cannot have this flaw. However, other perception range effects can be Communication- Dependent, meaning you must be in communication with your subject for them to work (using your Commu- nication medium as a “carrier” for the other effect). If your Communication is blocked in any way, the other effect doesn’t work. -1 cost per rank.

— HeroesHandbook, chunk unit_01897, section_path: EXTRAS / FLAWS

### ConcealmentEffectExtras

EXTRAS

Affects Others: This modifier allows you to grant Conceal- ment to others while you are touching them, or at range, if you also apply the Range modifier. +1 cost per rank. Area: Concealment with Affects Others (previously) or At- tack (immediately following) may have this extra, affecting everything in the area. To only affect some targets in the area, apply the Selective modifier as well. +1 cost per rank. Attack: Use this extra for a Concealment effect you can impose on others (whether they want to be concealed or not). An invisibility ray, for example, is a Visual Conceal- ment Attack, while a field of darkness is a Burst Area Visual Concealment Attack. +0 cost per rank. Precise: You can vary your Concealment at will as a free action: going from total to partial to no concealment, concealing some parts and not others, or anywhere in- between. If your Concealment affects multiple senses, you can also choose to affect some of those senses and not others. Concealment is normally all-or-nothing: either you are concealed to the full amount of your effect, or you’re not. Flat +1 point.

— HeroesHandbook, chunk unit_01928, section_path: SENSORY / EXTRAS

### ConstructArchetypePowerExamples

POWERS

Undead: Immunity 30 (Fortitude effects), Protection 3

— HeroesHandbook, chunk unit_03784, section_path: AWE / POWERS

* * *

POWERS

Armor: Protection 12, Impervious • 24 points Giant: Growth 16, Continuous, Permanent, Innate • 33 points Robot: Immunity 30 (Fortitude) • 30 points 3 0 1 4

— HeroesHandbook, chunk unit_03847, section_path: AWE / POWERS

### CreateEffectExtras

EXTRAS

Continuous: Continuous Create makes objects that re- main until they are destroyed, nullified, or you choose to dismiss them. +1 cost per rank. Impervious: Applied to Create, this extra makes the ob- jects’ Toughness Impervious. +1 cost per rank. Innate: Continuous or Permanent Create with this modi- fier makes objects that cannot be nullified, they’re essen- tially “real” objects for all intents and purposes (although the user can “unmake” them at will unless the effect is also permanent). Flat +1 point. Movable: You can move your created objects around with a Move Object effect at your Create rank (see Move Object in this chapter for details). +1 cost per rank. Precise: You can create more precise and detailed ob- jects. The exact parameters of Precise Create are up to the GM, but generally, you can create objects with moving parts, and considerable detail. Flat +1 point. Selective: You can make your created objects selectively “transparent” to attacks, blocking some while allow- ing others (yours and your allies’, for example) to pass through them. You can also selectively make your objects solid to some creatures and incorporeal to others, such as allowing one person to walk through a created wall, while blocking another. It takes a free action to change the selective nature of an object; permanent created ob- 154154

— HeroesHandbook, chunk unit_01955, section_path: SUPPORTING WEIGHT / EXTRAS

### DefensePowerEffectPattern

DEFENSE

Defense effects protect in various ways, typically offering a bonus to resistance checks, or granting outright immu- nity to particular effects or conditions. Most defense ef- fects work only on the user and are subtle and permanent, functioning at all times. Some are activated and sustained as a free action, meaning they can switch on or off, but can potentially leave the user unprotected.

— HeroesHandbook, chunk unit_01711, section_path: CONTROL / DEFENSE

### Descriptor

TRAINING

Finally, some heroes acquire powers through hard work and training, whether physical discipline, studying esoter- ic martial arts techniques, meditation and introspection to unlock hidden mental powers, or mastering the arts of magic. Such training is typically arduous and not every- one has what it takes to accomplish it. Heroes who gained their powers through training may have rivals or foes who trained with them (see the Enemy and Rivalry complica- tions later in this chapter). Origins can serve as descriptors for a character’s powers (see Descriptors in the Powers chapter). For example, a super-powered mutant has the “mutant” descriptor, mean- ing the character may be detected by mutant-detection powers, affected by mutant-specific devices, and so forth. The same is true for a mystic, an alien, or any other origin.

— HeroesHandbook, chunk unit_00695, section_path: MUTANT / TRAINING

* * *

DESCRIPTORS ................. 204

Types of Descriptors ..........204 Applying Descriptors .........206

— HeroesHandbook, chunk unit_00080, section_path: MODIFIERS...................... 187 / DESCRIPTORS ................. 204

### SeriesRequiredDescriptorRule

REQUIRED DESCRIPTORS

In some settings, the Gamemaster may require certain descriptors for all powers. Usually, a required descrip- tor reflects some common element of the series. For ex- ample, if all characters with powers are mutants, then all powers have the “mutant” descriptor by definition, un- less the player comes up with a good explanation why they should not. If all superhumans are psychic mutants, then all powers have both the “psychic” and “mutant” descriptors. The GM sets the rules as far as what descrip- tors are required (or restricted) in the series. A character who breaks this guideline—say the one alien in a setting where all powers are otherwise mutant in origin—might have a Benefit (unusual origin) or face certain complica- tions, possibly both.

— HeroesHandbook, chunk unit_01695, section_path: MUTANTS & MASTERMINDS / REQUIRED DESCRIPTORS

### EnhancedTraitLimitedAndPermanent

FLAWS

Limited: Enhanced Traits are often Limited in some fash- ion, such as Nighttime (or Daytime) Only, While Angry (or in another emotional state), Underwater (or in some other environment), and so forth. A limit that rarely comes into play—like losing your Enhanced Trait during a new moon—can be handled as a power loss complication. See Complications in The Basics chapter for details. –1 cost per rank. Permanent: At no change in cost, your Enhanced Trait may be a permanent improvement, rather than a sus- tained effect. The primary difference is that your per- manent enhancement cannot be turned on and off and cannot be improved by extra effort, including using it to perform power stunts (see Extra Effort). There is no ac- tion to use a Permanent Enhanced Trait, as it is always ac- tive. +0 cost per rank. 158158

— HeroesHandbook, chunk unit_02025, section_path: GENERAL / FLAWS

### EquipmentAfflictionFortitudeDCExample

ENERGY WEAPONS

Blaster pistol: A pistol that fires a coherent bolt of energy. Blaster rifle: A larger rifle-sized weapon that fires a more powerful bolt of energy. Taser: A compressed-air weapon firing a pair of darts. On impact they release a powerful electrical charge, for an Affliction effect that can daze, stun, or incapacitate (For- titude resistance, DC 15).

— HeroesHandbook, chunk unit_03364, section_path: PROJECTILE WEAPONS / ENERGY WEAPONS

### ExtraEffortPowerSurge

POWER

Increase one of your hero’s power effects by +1 rank until the start of the hero’s next turn. Permanent effects cannot be increased in this way.

— HeroesHandbook, chunk unit_00433, section_path: MUTANTS & MASTERMINDS / POWER

* * *

RETRY

Certain effects (see the Powers chapter) require extra ef- fort to retry after a certain degree of failure. The extra ef- fort merely permits another attempt to use the effect; it grants no other benefits.

— HeroesHandbook, chunk unit_00439, section_path: RESISTANCE / RETRY

### HeadquartersDefenseSystemEffectCap

DEFENSE SYSTEM

A defense system consists of various weapon emplace- ments defending the exterior and interior of the head- quarters. A defense system can have any attack effect with a cost no greater than twice the HQ power level. Their attack bonus is equal to the power level.

— HeroesHandbook, chunk unit_03628, section_path: CONCEALED / DEFENSE SYSTEM

### PerceptionRangeTargetingAndConcealment

CONCEALMENT AND PERCEPTION RANGE

Perception range effects must accurately perceive a target in order to affect it. This generally means you cannot target subjects with total concealment from your accurate senses with perception range effects. Thus, foes with Visual Conceal- ment (the most common accurate sense) can be quite effective against characters relying on perception range attacks, unless the attacker has an unusual accurate sense to circumvent the Concealment. This is one reason Visual Concealment costs extra. At the Gamemaster’s discretion, a successful Perception check to accurately locate a target with an acute sense may al- low you to use perception range effects on that target; however, the target still benefits from concealment, granting a +5 circumstance bonus to resistance against the effect. ranks. A plant’s sense of its surroundings is limited, so it won’t be able to give (or recognize) detailed descriptions or answer questions about events outside its immediate vicinity.

— HeroesHandbook, chunk unit_01919, section_path: DELUXE HERO’S HANDBOOK / CONCEALMENT AND PERCEPTION RANGE

### PowerActivationAndResolution

HOW POWERS WORK

Using powers is a fairly simple matter. Some power effects work automatically. Others—particularly those affecting other people—require some effort to use, like an attack check or a effect check. Powers affecting others allow resistance checks against their effects.

— HeroesHandbook, chunk unit_01733, section_path: SENSE TYPES / HOW POWERS WORK

### PowerEffectNameTableFragment

NAME

Affliction Alternate Form Blast

— HeroesHandbook, chunk unit_01764, section_path: COST / NAME

* * *

NAME

Senses Shapeshift Shrinking Sleep Snare Speed Strike Suffocation Summon Attack Attack Control Super-Speed See description Movement Movement Control General Attack Swimming Teleport Transform Variable Weaken

— HeroesHandbook, chunk unit_01783, section_path: COST / NAME

### PowerEffectStandardCostPerRank

POWER COSTS

Power effects are acquired in ranks, like ranks for other traits. The more ranks an effect has, the greater its effect. Each effect of a power has a standard cost per rank.

— HeroesHandbook, chunk unit_01682, section_path: ACQUIRING POWERS / POWER COSTS

### PowerEffectSummaryLine

EFFECT DESCRIPTION FORMAT

Action: Standard • Range: Close Duration: Instant • Cost: 1 point per rank

— HeroesHandbook, chunk unit_01824, section_path: ATTACK / EFFECT DESCRIPTION FORMAT

### PowerEffectType

EFFECT TYPES

Power effects fall into certain categories or effect types. Effects of the same type follow similar rules and provide de- scriptors for certain other effects. This section discusses the different effect types and the rules governing them.

— HeroesHandbook, chunk unit_01705, section_path: POWERS THAT AREN’T / EFFECT TYPES

### PowerExtraSection

EXTRAS

A listing of extras relevant or unique to the effect. Ex- tras unique to an effect are in colored orange.

— HeroesHandbook, chunk unit_01833, section_path: EXTRAS / EXTRAS

### SamplePowerWriteupSchema

NAME

Effect(s): Modifier(s) • Cost Name: What the power is called. Feel free to mod- ify the name to suit how you’re using the power. Effects: The power’s effect or effects are listed by name. Modifiers: Any modifiers applying to the effect are listed with it. If a power has multiple effects, each is listed with its applicable modifiers. Cost: Lastly, the power’s cost is given. This is a cost per rank of the power if it has a ranked effect, oth- erwise it is a flat cost in power points. Some pow- ers may have a flat cost for the initial power, plus a cost per rank for additional ranks.

— HeroesHandbook, chunk unit_01846, section_path: SAMPLE POWERS / NAME

* * *

SAMPLE POWERS

Spread throughout this section are boxes like this one, providing examples of some of the most common powers found amongst superhero characters to give you a “menu” of pre-fabricated powers to choose from when creating your own heroes (and villains) in MU- TANTS & MASTERMINDS. Sample powers are presented on the Power Effects table in italics. Each power is presented in the following format:

— HeroesHandbook, chunk unit_01844, section_path: MUTANTS & MASTERMINDS / SAMPLE POWERS

### PowerModifierCatalog

FLAWS

Distracting: Coordinating the actions of your multiple limbs is difficult, so you are vulnerable while applying any extra limbs to an action. This flaw should generally not ap- ply to any creature with Innate Extra Limbs, especially if they are part of its natural physiology. -1 cost per rank.

— HeroesHandbook, chunk unit_02070, section_path: EXTRAS / FLAWS

* * *

EXTRAS

Action: This extra reduces the action required for you to use Healing. You cannot use Healing more than once per turn regardless. To heal multiple subjects at once, apply the Area modifier. +1 cost per rank. Affects Objects: Your Healing can also “heal” damage to non-living subjects. You make a Healing check against the subject’s worst damage condition, as normal. +1 cost per rank. Area: Healing with this extra grants the same benefit to all subjects in the affected area. Area Empathic Healing (see this power’s Flaws) is an unwise combination, as the heal- er takes on all of the damage conditions of the affected subjects at once! +1 cost per rank. Energizing: You can heal the fatigued and exhausted con- ditions as well as damage conditions: DC 10, one degree of success for fatigued, two degrees of success for exhausted. However, you take on the removed conditions and cannot use Healing to eliminate your own fatigue (although you can still use hero points to recover from them). If the Heal- ing check fails, you must wait the normal recovery time or use extra effort to try again. +1 cost per rank. Perception: Applied to Ranged Healing (following), Per- ception Ranged Healing does not require an attack check to “touch” the subject. +1 cost per rank. Persistent: Your Healing can remove even Incurable ef- fects (see the Incurable modifier). Flat +1 point. Ranged: Ranged Healing requires an attack check to “touch” the subject with the Healing effect. The GM may waive the check for a willing subject holding completely still, but the subject is defenseless that round, making it an unwise decision in the midst of combat. +1 cost per rank.

— HeroesHandbook, chunk unit_02123, section_path: MUTANTS & MASTERMINDS / EXTRAS

* * *

DAMAGING ILLUSIONS

Independent: Your active illusions only require a free action to maintain, rather than a standard action. +1 cost per rank. Selective: You choose who perceives your Illusion and who doesn’t. +1 cost per rank. For illusions so realistic they are capable of inflicting dam- age, add a Linked Perception Range Damage effect. At the GM’s discretion, this effect can even be made into a Linked Array with a variety of alternate attack effects, allowing your illusionist to inflict conditions other than damage on targets. Keep in mind the attack effects all need to be per- ception range to match the range of Illusion.

— HeroesHandbook, chunk unit_02154, section_path: EXTRAS / DAMAGING ILLUSIONS

* * *

FLAWS

Limited to Half Effect: You suffer half the normal effect rather than being entirely immune to it. For environmen- tal effects, you only make checks half as often. For other effects, halve the effect’s rank (round down) before de- termining its resistance check DC, including for things like Impervious. -1 cost per rank. There are characters in comic books flatly immune to certain things. Immunity is intended to provide this option in MU- TANTS & MASTERMINDS. It’s simpler at some point to say a character is immune to something than it is to bother rolling dice. Immunity also encourages creativity: if you can’t overcome a foe just by hitting him, what then? Encourage players to use tactics, cleverness, power stunts, and hero points to deal with foes immune to their more conventional attacks. If you find Immunity—especially broad immunities at higher ranks—a problem in your game, feel free to restrict it (per- haps to no more than 10 ranks) or eliminate it altogether, replacing it with Protection and defense bonuses with appropri- ate power modifiers. For a degree of immunity to Damage, see the Impervious extra in the Modifiers section.

— HeroesHandbook, chunk unit_02189, section_path: EXTRAS / FLAWS

* * *

FLAWS

Acrobatics Check Required: In order to use Leaping, you must make an Acrobatics skill check (DC 10). Each point your check total exceeds the DC allows you to use 1 rank of Leaping, up to your total rank. –1 cost per rank. Full Power: With this flaw, you can only leap your maxi- mum distance; you can make shorter leaps only by not using your Leaping effect at all, just the normal jumping distance for your Strength. This may suit uncontrollable “leaping” effects like rocket boosters and the like. Flat –1 point.

— HeroesHandbook, chunk unit_02232, section_path: EXTRAS / FLAWS

* * *

FLAWS

Close: Since Move Object works on things at a distance by definition, it cannot generally be reduced to close ranged. At the GM’s discretion, a Close Ranged Move Object effect may represent “tactile telekinesis” or a supernatural influ- ence over objects you are able to touch, but such things are usually better represented by the Enhanced Strength effect. –1 cost per rank.

— HeroesHandbook, chunk unit_02310, section_path: EXTRAS / FLAWS

* * *

EXTRAS

Affects Insubstantial: Nullify does not require this modi- fier to affect insubstantial targets, or the Insubstantial ef- fect itself. You can attempt to nullify the effects of insub- stantial targets normally. Alternate Resistance: Nullify may require a Fortitude rath- er than a Will check to represent an effect resisted by health and stamina rather than strength of will. +0 cost per rank. The Time, Space, and Dimension Travel effects of Move- ment are comparatively cheap considering what they do, primarily because such special movement capabilities are highly dependent on the plot and nature of the setting, and subject to a lot of Gamemaster oversight. Thus, they largely amount to supped-up Features, mainly allowing heroes to visit exotic locales. Temporal mechanics and the effects of time travel are left entirely up to the GM, who may choose to make Time Travel Limited, Uncontrolled, or Unreliable for player characters, or disallow it altogether, treating it solely as a plot-device in the setting. Space travel in the comic books rarely involves the laws of physics and tends to occur “at the speed of plot”. Charac- ters and vehicles (such as alien starships) able to traverse the void of space do so primarily to facilitate adventures out among the stars. Exactly how fast characters travel through the void of space does not really matter; it is how long it takes them to get where they’re going that mat- ters. So Space Travel is largely defined in terms of “how far can you go between scenes?” The same is true of the mechanism of travel, whether hyperspace, jump drive, faster-than-light “warp speed,” or what have you. The Gamemaster likewise decides on the existence and nature of other dimensions in the setting, what they are like, and who can reach them. Like Time Travel, the GM may require Dimension Travel be Limited, Uncontrolled, or Unreliable for player characters, or treat it solely as a plot-device rather than a defined effect. Area: An Area Nullify effect works on all targets in the area. Make a single power check and compare the result against the opposed checks of the targets. Targets lack- ing effects you can nullify are, naturally, unaffected. If your Area Nullify has a duration longer than instant, choose whether or not the effect remains in the chosen area (af- fecting anyone entering or leaving it) or moves with the targets hit with the initial effect. There is no difference in cost, but to be able to do both, take one Area Nullify as an Alternate Effect of the other. +1 cost per rank. Broad: Broad Nullify can counter effects of a particularly broad descriptor like magical, mutant, or technological effects. This modifier is available only with the Gamemas- ter’s permission and may depend on the effects available in the series. +1 cost per rank. Concentration: Any countered effect is suppressed and cannot be re-activated while you concentrate. The user of the countered effect may use extra effort to gain another opposed Nullify check.

— HeroesHandbook, chunk unit_02361_s1, section_path: ATTACK / EXTRAS

* * *

FLAWS

Limited to One Type: Your Quickness applies to only physical or mental tasks, not both. –1 cost per rank. Limited to One Task: Your Quickness applies to only one particular task, such as reading, mathematical calcula- tions, and so forth. –2 cost per rank.

— HeroesHandbook, chunk unit_02388, section_path: MUTANTS & MASTERMINDS / FLAWS

* * *

FLAWS

Source: Your Regeneration only works when you have ac- cess to a particular source to replenish yourself, such as blood, electricity, sand, scrap metal, sunlight, and so forth. –1 cost per rank.

— HeroesHandbook, chunk unit_02397, section_path: EXTRAS / FLAWS

* * *

EXTRAS

Dimensional: This modifier allows you to extend your Remote Sensing into other dimensions with range proxi- mate to your location in that dimension. One rank of Di- mensional allows you to sense into a single other dimen- sion, two for a group of related dimensions, and three for any dimension in the setting suitable to your Remote Sensing descriptors. Dimensional Remote Sensing for an accurate sense is especially useful for targeting other Di- mension effects. Flat +1 point per rank of Dimensional. No Conduit: Sensory effects targeted where you have dis- placed your senses do not affect you, but neither can you

— HeroesHandbook, chunk unit_02408, section_path: POWER-LIFTING / EXTRAS

* * *

FLAWS

Limited to Extended: You can only make extended tele- ports. You must have the Extended extra, and this flaw ef- fectively makes it a +0 modifier. –1 cost per rank. Medium: You require a medium for your teleportation, such as electrical or telephone wires, root structures, wa- terways, shadows, flames, mirrors, and so forth. You can only teleport from and to locations where your medium exists. –1 cost per rank.

— HeroesHandbook, chunk unit_02618, section_path: SUPER-SPEED / FLAWS

* * *

EXTRAS

Action: You can change the configuration of your effect faster, although only a Reaction Variable can change more often than once per turn, and then only in response to its trig- gering circumstances. Gamemasters should exercise caution with Variable effects that can be reconfigured as a free action or re- action: they not only grant tremendous flexibility, they can also slow down game play as the player considers virtually infinite possibilities for each action using the Variable effect. Move Action: +1 cost per rank . Free Action: +2 cost per rank. Reaction: +3 cost per rank. Affects Others: You can grant effects to someone else. The subject granted the use of the effect con- trols its configuration, if appropriate for its descrip- tors (although you retain the ability to withdraw use of the effect altogether whenever you wish). Affects Others Only: +0 cost per rank. Affects Others or yourself: +1 cost per rank. Perception: Applied to a Ranged Affects Others Variable, this extra allows you to grant the benefits of the effect to any target you can accurately perceive. +1 cost per rank. Ranged: A Variable effect with Affects Others may have the Ranged extra to improve the range at which you can grant the effect to another. This does not alter the ranges of the effect’s various configurations. To do so, apply the Range modifier to the effect(s) within a particular configu- ration. +1 cost per rank.

— HeroesHandbook, chunk unit_02655, section_path: DELUXE HERO’S HANDBOOK / EXTRAS

* * *

It takes at least a minute, possibly as long as an hour or more. The GM sets the specific time in cases where it matters, but it should be short enough that you can reconfigure between scenes in a game, but long enough that you effectively cannot do it during action time. The GM may allow you to spend a hero point to reconfigure your Variable effect during action time as a power stunt, if circumstances warrant it. –1 cost per rank.

— HeroesHandbook, chunk unit_02668_s2, section_path: DELUXE HERO’S HANDBOOK / UNDER THE HOOD: VARIABLE EFFECTS

* * *

FRACTIONAL COSTS

If total flaws reduce an effect’s cost per rank to less than 1 power point, each additional –1 to cost per rank beyond that adds to the number of ranks of the effect you get by spending 1 power point on a 1-to-1 basis. In essence, an effect’s cost can be expressed as the ratio of power points per rank (PP:R). So an effect costing 3 points per rank is 3:1. If that effect has a total of –2 in modifiers, it costs 1:1, or 1 power point per rank. Apply- ing another –1 modifier adds to the second part of the ratio, making it 1:2, or 1 power point per two ranks, and so forth. Continue the progression for further reductions. Game- masters may wish to limit the final modified cost ratio of any effect in the series (to 1:1, 1:2, 1:4, or whatever figure is appropriate). As a general rule, 1:5 (five ranks per power point) should be the lowest modified cost for an effect, but the GM sets the limit (if any). Example: A hero has Protection, which costs 1 point per rank. The Protection has two modifiers; the first is the Imperious extra (a +1 point per rank modifier), and the second is the flaw Limited to Blunt Physical Attacks (a –3 points per rank modifier) for a total modifier of –2. Since Protection costs 1 point per rank, the –2 modifier increases the number of ranks per power point, so the final cost is 1 power point per 3 ranks of Impervious Protection Limited to Blunt Physi- cal Attacks.

— HeroesHandbook, chunk unit_02692, section_path: APPLYING MODIFIERS / FRACTIONAL COSTS

* * *

When applied to an effect that doesn’t normally allow a resistance check, this flaw gives it one. Choose the de- fense when the flaw is applied. Since effects that work on others allow a resistance check by definition, this nearly always applies to personal effects that allow someone in- teracting with them to circumvent the effect with a suc- cessful check. For example, an Enhanced Parry defense effect might re- flect a low-level reading of a target’s mind to anticipate and avoid attacks. It allows a Will resistance check to overcome the effect, denying you the defense bonus against that op- ponent (and applying this flaw to the effect). Likewise, your Concealment effect might be illusory rather than a true physical transformation, permitting a Will resistance check for someone to overcome it. A sustained Protection effect might be some sort of “kinetic field” that permits an attack- er a Fortitude resistance check to overcome it. When applied to an effect that does normally allow a re- sistance check, this flaw gives it an additional one, which may be the same as its normal resistance, or different. The target makes both resistance checks and applies the bet- ter of the two to determine the effect’s result. For example, a Damage effect might involve whirling blades an attacker can avoid with a successful Dodge resistance check, circumventing the need for a Tough- ness check against the damage. Similarly a Weaken effect based on a poison dart might add a Toughness check to see if the dart penetrates the target’s skin in addition to making the usual Fortitude check against the effect. The target of a Sense-Dependent effect must be able to perceive the effect for it to work. The target gets a Dodge resistance check. Success means the target has managed to avert his eyes, cover his ears, etc. and the effect doesn’t work. Otherwise the effect works normally and the target makes the usual resistance check against it, if any. Opponents aware of a Sense-Dependent effect can also deliberately block the targeted sense: looking away, cover- ing or blocking their ears, etc. This provides a +10 bonus to resistance checks against the effect, but gives others partial concealment from that sense. An opponent unable to use a sense (blind, deaf, etc.) is immune to effects dependent on it. Opponents can do this by closing their eyes, wearing ear- or nose-plugs, or using another effect like Concealment. This gives you total concealment from that sense. Sensory effects are Sense-Dependent by definition, and cannot apply this flaw. To give a target additional resis- tance to a sensory effect, use the Resistible flaw.

— HeroesHandbook, chunk unit_03055, section_path: RESISTIBLE / -1 COST PER RANK

* * *

DEVICES

A device is an item that provides a particular power effect or set of effects. While devices are typically creations of ad- vanced science, they don’t have to be. Many heroes and villains have magical devices such as enchanted weapons and armor, magical talismans, wands and staves of power, and so forth. Some devices are products of alien technology so advanced they might as well be magical, or focuses of psychic or cosmic power beyond the understanding of both magic and science. All devices work the same way in game terms, regardless of their origin or descriptors. Generally speaking, devices are powers with the Removable flaw applied to them (see Removable in the Powers chapter), meaning the power is external to the character. Take away the device, and the wielder loses the ability to use those powers. So if an armored hero loses access to his battlesuit, for example, he also loses access to the powers tied-up in it. The same is the case of a hero loses a cosmic ring, magic helmet, or alien artifact, which is why Removable is a flaw for those powers. Just like other powers, devices cost power points (albeit reduced some by the Removable flaw). Characters who want to have and use a device on a regular basis have to pay power points to have it, just like having any other power. The device becomes a part of the character’s abilities. If the device is lost, stolen, or destroyed, the character can replace it, given time, since the device is considered a permanent part of the character. Only a re-allocation of the character’s power points will change this, and Gamemasters should allow characters to re-allocate power points spent on a Removable power if it is somehow permanently lost. In other cases, characters may make temporary use of a device. Most devices are usable by anyone able to operate them, in which case characters may loan devices to each other, or may pick up and use someone else’s device (or even steal a device away from someone in order to use it against them). The key concept here is the use of the device is tem- porary, something that happens during a single scene or, at most, a single adventure. If the character wants to continue

— HeroesHandbook, chunk unit_03166, section_path: CHAPTER 7: GADGETS & GEAR / DEVICES

### PowerPoints

COMPLICATIONS .............. 27

Choosing Complications .... 27 Motivation ............................... 27 Other Complications ........... 28

— HeroesHandbook, chunk unit_00056, section_path: POWER POINTS ................ 24 / COMPLICATIONS .............. 27

* * *

ACQUIRING POWERS ..... 143

Power Costs ...........................143 Power Descriptors...............143

— HeroesHandbook, chunk unit_00038, section_path: CHAPTER 6: POWERS ........ 143 / ACQUIRING POWERS ..... 143

### AlternateVehicleEquipmentPointPricing

ALTERNATE VEHICLES

Just like Alternate Equipment, characters may have mul- tiple vehicles. These are generally Alternate Equipment by definition, since it’s difficult to drive or pilot more than one vehicle at a time! So the character pays the full cost for the most expensive vehicle, and then 1 equip- ment point for each additional vehicle with the same or lesser cost. So a hero with an array of vehicles, such as a plane, boat, and car pays full equipment point cost for the most ex- pensive of the vehicles and just 1 equipment point for each of the others. The hero’s player can even spend a hero point to pull out a motorcycle, submarine, jet-ski, or whatever other vehicle the hero might have stashed away waiting for the right occasion.

— HeroesHandbook, chunk unit_03499, section_path: SHARED VEHICLES / ALTERNATE VEHICLES

### PowerLevel

3. POWER LEVEL

Your GM sets the starting power level for the series. Gener- ally, this is level 10, but it may range anywhere from level 5 to level 20 or more. The power level determines the player characters’ starting power points and exactly where you can spend them. See Power Level later in this chapter for details.

— HeroesHandbook, chunk unit_00502, section_path: 2. GAMEMASTER GUIDELINES / 3. POWER LEVEL

* * *

9. DETAILS

Go through the limits listed under Power Level in this chapter and make sure your hero’s traits all fit within them. If not, adjust the traits accordingly until they do. Go back through and add up the costs of your hero’s abili- ties, defenses, skills, advantages, and powers. You should end up with a figure equal to the starting power points shown on the Starting Power Points table. If not, double- check your math and either remove or add traits to your character to reach the starting power point total. Figure out things like your hero’s name, appearance, origin, background, and motivation. If you can, consider creating a sketch or detailed description of your hero’s costume.

— HeroesHandbook, chunk unit_00524, section_path: 8. COMPLICATIONS / 9. DETAILS

* * *

INCREASING POWER LEVEL

As heroes earn power points through adventuring and spend them to improve their traits, they will eventually run into the limits imposed by the series power level (see Power Level, earlier in this chapter, for details). For a while, this can be a good thing, since the power level limits encourage heroes to diversify and acquire new skills, ad- vantages, and powers rather than simply pumping points into their existing traits to increase them to unwieldy lev- els. However, sooner or later, you’re going to want to raise the power level, giving the heroes a bit more breathing room for advancement and spending their earned power points. A good guideline is to follow the starting power point to- tals when it comes to power level: when the heroes ac- cumulate an additional 15 power points from the start of the series or the last time the power level was raised, it’s probably time to raise the power level by +1. So a power level 10 game starts out with 150-point heroes. When they have earned another 15 power points (bringing their to- tal up to 165), the GM should consider raising the power level to 11, allowing the heroes to spend some of those power points to increase traits which are currently at the maximum limit. When you increase the power level, you should also re- evaluate the capabilities of the villains and other chal- lenges the heroes face. While NPCs don’t earn additional power points as such, and aren’t even subject to the same power level limits as the heroes, you should feel free to improve the traits of some non-player characters to keep pace with the heroes, ensuring those antagonists remain a suitable challenge. It’s also fine to have others lag be- hind, as the heroes outstrip some of their old foes, who no longer represent the kind of threat they did before, plus you can introduce new villains and challenges suited to the series power level as things progress.

— HeroesHandbook, chunk unit_00729, section_path: HERO ADVANCEMENT & IMPROVEMENT / INCREASING POWER LEVEL

### Rank

RANKS & MEASURES

MUTANTS & MASTERMINDS uses the term rank when talking about the value of a game trait. So you might say a hero has “rank 8 Strength” or simply “Strength 8” (which mean the same thing), or that an effect is rank 5, 9, 15, or what have you. Every quantifiable trait in M&M has a rank as- signed to it. The game also uses a system of measures, real world values like pounds, seconds, minutes, hours, feet, yards, and miles, to name a few. There is a direct relationship between rank and measure, as shown on the Measure- ments Table. (You can find a metric version of the Mea- surements Table in the back of the book.)

— HeroesHandbook, chunk unit_00232, section_path: COMPLICATIONS / RANKS & MEASURES

### FallDamageRankFromDistanceRank

SUFFOCATION

Characters can hold their breath for ten rounds (one min- ute) plus a number of rounds equal to twice their Stamina. After that time they must make a Fortitude check (DC 10) each round to continue holding their breath. The DC in- creases by +1 for each previous success. Failure on the Fortitude check means the character becomes incapaci- tated . On the following round the character is dying. A dy- ing character cannot stabilize until able to breathe again. Heroes with Immunity to Suffocation can go an unlimited time without air. A fall inflicts damage rank 4 plus twice the distance rank fallen, to a maximum of rank 16 damage. Characters with the Acrobatics skill can fall greater distances without risk of damage. Falling into or onto a dangerous surface may cause additional damage, at the GM’s discretion. Catching a falling person or object requires a Dexterity check (DC 5). If you successfully catch a falling object, subtract your Strength rank from the falling damage rank. Both you and the object suffer any remaining dam- age. So if a character with Strength 6 catches someone falling for 12 damage, subtract 6 from 12, and both char- acters resist damage 6. If the catcher is using a power— such as Flight or Move Object—to catch the falling ob- ject, the power’s rank can be substituted for Strength at the GM’s discretion.

— HeroesHandbook, chunk unit_03995, section_path: STARVATION AND THIRST / SUFFOCATION

### VehicleSizeCategoryPointCost

SIZE

its base Strength, Toughness, and Defense values. Vehicles start out at medium size by default, and each increase in size category costs 1 power point.

— HeroesHandbook, chunk unit_03450, section_path: VEHICLE TRAITS / SIZE

* * *

COST

1 point per size category 1 point per +1 Strength movement effect cost Toughness 1 point per +1 Toughness Defense Features Powers 1 point per +1 Defense 1 point per feature power cost (see Chapter 5) modes of movement (air, ground, and water, for example) pay full cost for the most expensive and can acquire the others as Alternate Effects (see the Alternate Effect modi- fier in the Powers chapter).

— HeroesHandbook, chunk unit_03475, section_path: TRAIT / COST

### ResistanceCheck

RESISTANCE CHECKS

A resistance check is an attempt to resist different ef- fects, ranging from damage and injury to traps, poisons, and various power effects. A resistance check is a d20 roll

+ the appropriate defense (typically Dodge, Fortitude,

Toughness, or Will). Resistance Check = d20 + defense bonus + modifiers vs. hazard’s DC (generally 10 + rank) The difficulty class is based on the strength of the hazard, such as the rank of an effect or the strength of a disease or poison, typically that value plus 10 (like a routine check). Resistance checks may be graded, with different results at different degrees.

— HeroesHandbook, chunk unit_00363_merged, section_path: ATTACK CHECKS / RESISTANCE CHECKS

### DamageResistanceDegreeOutcomes

DAMAGE RESISTANCE CHECK

Toughness vs. [Damage rank + 15] Success : The damage has no effect. Failure (one degree): The target has a –1 circumstance penalty to further resistance checks against damage. Failure (two degrees): The target is dazed until the end of their next turn and has a –1 circumstance penalty to further checks against damage. Failure (three degrees): The target is staggered and has a -1 circumstance penalty to further checks against damage. If the target is staggered again (three degrees of failure on a Damage resistance check), ap- ply the fourth degree of effect. The staggered condi- tion remains until the target recovers (see Recovery, following). Failure (four degrees): The target is incapacitated .

— HeroesHandbook, chunk unit_01979, section_path: ATTACK / DAMAGE RESISTANCE CHECK

### EffectResistanceWaiverRules

RESISTANCE CHECK

Effects targeting other characters allow a resistance check. The defense used and the difficulty class depend on the effect and its modifiers. Willing characters can forgo their resistance check against an effect, if they wish. This includes characters who think they’re receiving a beneficial effect, even if they’re not! You can’t forgo Toughness checks, but you may choose to discontinue the use of effects with a duration of Continu- ous or Sustained that grant a Toughness bonus in order to lower your resistance. Each effect lasts for a particular amount of time, which may be changed by modifiers. The Immunity effect allows characters to ignore certain ef- fects altogether, removing the need for a resistance check.

• •

Instant: When used, the effect occurs and ends in the same turn, although its results may linger.

— HeroesHandbook, chunk unit_01792_merged, section_path: DURATION / RESISTANCE CHECK

### ImperviousSkipsUnneededAttackRoll

DELUXE HERO’S HANDBOOK

Now the remaining smugglers get to go. They draw their guns and shoot at you! The GM rolls attack checks against the heroes. Two smugglers shoot at Ultramarine and three shoot at Princess, but they both have Impervious Toughness 8. Since the smugglers’ guns can’t hurt them, the GM does not bother rolling the attack checks. The remaining two shoot at Rook, but one is impaired and the other blind, so they both miss by a mile. Rook, you easily avoid the clumsy shots, especially from the guys dazzled by the flash bomb. Princess, Ultramarine, a couple of stray shots ricochet off of you harmlessly.

— HeroesHandbook, chunk unit_04085, section_path: DELUXE HERO’S HANDBOOK / DELUXE HERO’S HANDBOOK

### SuffocationFortitudeEscalation

SUFFOCATION

Characters can hold their breath for ten rounds (one min- ute) plus a number of rounds equal to twice their Stamina. After that time they must make a Fortitude check (DC 10) each round to continue holding their breath. The DC in- creases by +1 for each previous success. Failure on the Fortitude check means the character becomes incapaci- tated . On the following round the character is dying. A dy- ing character cannot stabilize until able to breathe again. Heroes with Immunity to Suffocation can go an unlimited time without air. A fall inflicts damage rank 4 plus twice the distance rank fallen, to a maximum of rank 16 damage. Characters with the Acrobatics skill can fall greater distances without risk of damage. Falling into or onto a dangerous surface may cause additional damage, at the GM’s discretion. Catching a falling person or object requires a Dexterity check (DC 5). If you successfully catch a falling object, subtract your Strength rank from the falling damage rank. Both you and the object suffer any remaining dam- age. So if a character with Strength 6 catches someone falling for 12 damage, subtract 6 from 12, and both char- acters resist damage 6. If the catcher is using a power— such as Flight or Move Object—to catch the falling ob- ject, the power’s rank can be substituted for Strength at the GM’s discretion.

— HeroesHandbook, chunk unit_03995, section_path: STARVATION AND THIRST / SUFFOCATION

### ToughnessResistanceAfterDamageHit

DAMAGE

A successful attack with a Damage effect requires the tar- get to make a Toughness resistance check.

— HeroesHandbook, chunk unit_04059, section_path: MUTANTS & MASTERMINDS / DAMAGE

### Skill

SKILL BASICS .................. 113

Acquiring Skills ....................113

— HeroesHandbook, chunk unit_00025, section_path: CHAPTER 4: SKILLS ........... 113 / SKILL BASICS .................. 113

### AcrobaticsMitigateFallDistance

SUFFOCATION

Characters can hold their breath for ten rounds (one min- ute) plus a number of rounds equal to twice their Stamina. After that time they must make a Fortitude check (DC 10) each round to continue holding their breath. The DC in- creases by +1 for each previous success. Failure on the Fortitude check means the character becomes incapaci- tated . On the following round the character is dying. A dy- ing character cannot stabilize until able to breathe again. Heroes with Immunity to Suffocation can go an unlimited time without air. A fall inflicts damage rank 4 plus twice the distance rank fallen, to a maximum of rank 16 damage. Characters with the Acrobatics skill can fall greater distances without risk of damage. Falling into or onto a dangerous surface may cause additional damage, at the GM’s discretion. Catching a falling person or object requires a Dexterity check (DC 5). If you successfully catch a falling object, subtract your Strength rank from the falling damage rank. Both you and the object suffer any remaining dam- age. So if a character with Strength 6 catches someone falling for 12 damage, subtract 6 from 12, and both char- acters resist damage 6. If the catcher is using a power— such as Flight or Move Object—to catch the falling ob- ject, the power’s rank can be substituted for Strength at the GM’s discretion.

— HeroesHandbook, chunk unit_03995, section_path: STARVATION AND THIRST / SUFFOCATION

### CloseCombatSkillSpecialization

CLOSE COMBAT

Fighting You’re trained with a particular type of close attack, giv- ing you a bonus to your attack checks with it equal to your skill rank (see Attack Check in The Basics and in the Action & Adventure chapter). Each close attack is a separate Close Combat skill with its own rank, and en- compasses a single weapon or power, although an ar- ray may be considered one power, at the Gamemaster’s discretion (see Arrays in the Powers chapter for more information). A successful DC 10 Athletics check allows you to swim your ground speed rank minus 2 as a move action. If the check fails, you make no progress through the water dur- ing the action. With more than one degree of failure, you go under. If underwater, you must hold your breath to avoid drowning (see page 238). So a hero might have Close Combat: Swords, but Close Combat: Melee Weapons is too broad. Close Combat: Un- armed is an option, meaning skill with unarmed strikes like punches and kicks. However, this bonus does not ap- ply to other forms of unarmed combat maneuvers, includ- ing, but not limited to, grabbing or tripping.

— HeroesHandbook, chunk unit_01006, section_path: MODIFIERS / CLOSE COMBAT

### InteractionSkill

INTERACTION SKILLS

Certain skills, called interaction skills, are aimed at deal- ing with others through social interaction. Interaction skills allow you to influence the attitudes of others and get them to cooperate with you in one way or another. Since interaction skills are intended for dealing with others so- cially, they have certain requirements. First, you must be able to interact with the subject(s) of the skill. They must be aware of you and able to under- stand you. If they can’t hear or understand you for some reason, you have a –5 circumstance penalty to your skill check (see Circumstance Modifiers in The Basics). Interaction skills work best on intelligent subjects, ones with an Intellect rank of –4 or better. You can use them on creatures with Int –5, but again with a –5 circumstance penalty; they’re just too dumb to get the subtleties of your point. You can’t use interaction skills at all on sub- jects lacking one or more mental abilities. (Try convincing a rock to be your friend—or afraid of you—sometime.)

— HeroesHandbook, chunk unit_00907, section_path: SKILL BENCHMARKS / INTERACTION SKILLS

### InvestigationVersusPerceptionSearch

SEARCH

You can search an area for clues, hidden items, traps, and other details. Perception allows you to immediately notice things, while an Investigation check allows you to pick up on details with some effort. 122122

— HeroesHandbook, chunk unit_01113, section_path: INVESTIGATION / SEARCH

### SkillCatalog

SKILL DESCRIPTIONS..... 114

Acrobatics ..............................115 Athletics ..................................116 Close Combat .......................117 Deception ..............................118 Expertise .................................119 Insight .....................................120 Intimidation ..........................121 Investigation .........................122 Perception .............................123 Persuasion .............................124 Ranged Combat ..................125 Sleight of Hand ....................125 Stealth .....................................126 Technology ............................127 Treatment ..............................129 Vehicles ...................................129

— HeroesHandbook, chunk unit_00029, section_path: HOW SKILLS WORK ........ 113 / SKILL DESCRIPTIONS..... 114

### TechnologyInventingPrerequisite

INVENTING

If you have the Inventor advantage (see the Advantages chapter), you can use Technology to create inventions, temporary devices. See Inventing, page 211, for details.

— HeroesHandbook, chunk unit_01247, section_path: DELUXE HERO’S HANDBOOK / INVENTING

### TechnologyRepairDamagedObjects

RECOVERY

As a result of conflict, characters often suffer adverse con- ditions (see Conditions in The Basics chapter) from being knocked around and hit with different powers. The spe- cific conditions are discussed in the effects defined in the Powers chapter, particularly Affliction and Damage, the most common effects of conflicts. Living targets remove one damage condition per minute of rest, starting from their most severe condition and working back. So a damaged character recovers from being inca- pacitated, then staggered, dazed, and finally removes a –1 Toughness check penalty per minute until fully recovered. The Healing and Regeneration effects can speed this process. Objects, having no Stamina, do not recover from damage unless they have an effect like Regeneration. Instead, they must be repaired. See the guidelines under the Technol- ogy skill when repairing damaged object.

— HeroesHandbook, chunk unit_04279, section_path: TEAM ATTACK / RECOVERY

* * *

DELUXE HERO’S HANDBOOK

The Healing and Regeneration effects can speed this pro- cess. Lasting or more serious injuries are handled as com- plications (see Lasting Injuries). Objects, having no Stamina, do not recover from damage unless they have an effect like Regeneration. Instead, they must be repaired. See the guidelines under the Technol- ogy skill when repairing damaged objects.

— HeroesHandbook, chunk unit_04100, section_path: DELUXE HERO’S HANDBOOK / DELUXE HERO’S HANDBOOK

### TechnologySkillHQCommunicationsUse

COMMUNICATIONS

The communications feature allows the headquarters to receive and transmit on a wide range of radio and TV bands, monitor police and emergency channels, coor- dinate communications between members of a team, and so forth. It includes communications equipment, consoles, and monitors. The system’s access to restricted communication bands depends on the clearance and skills of the user. Heroes often have access to special government channels, while a successful Technology skill check (DC 25) can grant a user illegal access to re- stricted systems.

— HeroesHandbook, chunk unit_03622, section_path: DELUXE HERO’S HANDBOOK / COMMUNICATIONS

### SkillCheck

SKILL BASICS .................. 113

Acquiring Skills ....................113

— HeroesHandbook, chunk unit_00025, section_path: CHAPTER 4: SKILLS ........... 113 / SKILL BASICS .................. 113

### CovertMessageSkillExchange

INNUENDO

You can use Deception to send covert messages using word-play and double-meanings while apparently talking about other things. The DC for a basic message is 10. Com- plex messages or messages trying to communicate new information have DCs of 15 or 20, respectively. The recipi- ent of the message must make a Insight check against the same DC to understand it.

— HeroesHandbook, chunk unit_01043, section_path: FEINTING / INNUENDO

* * *

INNUENDO

You can use Insight to pick up on hidden messages sent via the Deception skill (see the Deception skill descrip- tion).

— HeroesHandbook, chunk unit_01089, section_path: EVALUATE / INNUENDO

### ExpertiseRoutineAndPlayerBoundary

Expertise skills measure what your character knows about various things, whether you know anything about them or not. It’s fairly easy to measure what a hero knows by making the appropriate skill check or looking at the routine check value of (bonus +10). However, players may know things their characters do not, either because of the player’s life experience or knowledge of the game and its rules (and source material). In this case the Gamemaster may prefer players limit themselves to only what Expertise skills their heroes have rather than what they may or may not know about a given situation. The GM may bend this rule by allowing a player to spend a hero point to have a character act upon something he or she would have no way of knowing, calling it a “hunch” or a “lucky guess” (a version of the inspiration rule). See the Hero Points section for guidelines. If there’s a question as to how to handle an issue of player versus character expertise in the game, consult your Gamemaster.

— HeroesHandbook, chunk unit_01066, section_path: DELUXE HERO’S HANDBOOK / UNDER THE HOOD: CHARACTER EXPERTISE VS. PLAYER EXPERTISE

### InsightVersusIllusion

DETECT ILLUSION

The GM makes a secret Insight check to determine if your hero senses the true nature of an illusion (DC 10 + Illusion rank). Success means you pick up on a flaw in the illusion, sensing it is not real. See the Illusion effect in the Powers chapter for details.

— HeroesHandbook, chunk unit_01075, section_path: INSIGHT / DETECT ILLUSION

### OpposedSkillPairing

OPPOSED BY

Sneak up on someone Stealth Perception Con someone Deception Win a car race Vehicles Insight Vehicles Pretend to be someone else Steal a key chain unnoticed Deception Perception Sleight of Hand Perception Win a trivia contest Expertise Expertise Break computer security

— HeroesHandbook, chunk unit_00306, section_path: SKILL / OPPOSED BY

### PersuasionAttitudeShift

EFFECT

Hostile Will take risks to attack or interfere with you. Unfavorable Will insult, mislead, or otherwise cause you trouble. Indifferent Favorable Helpful Acts as socially expected towards you. Will chat, advise, and offer limited help. Will take risks to help or protect you. Persuading someone is at least a standard action, usually quite a bit longer. The GM decides if you can persuade at all once a conflict has broken out! Even if the initial check succeeds, the other character can only be persuaded so far; you can try again in the same scene, but you check against the subject’s initial attitude, and may end up wors- ening it rather than improving it! Example: The heroes must convince the imperi- ous King of Atlantis that the surface world is not responsible for recent attacks against his king- dom in order to avert a war. The king’s attitude is unfavorable towards these surface-world in- terlopers to begin with. The team’s spokesperson makes a Persuasion attempt and gets a check result of 22, a success with two degrees total. That shifts the king’s attitude one step, to indif- ferent. He’s inclined to continue negotiating with the heroes and willing to place the assault on the surface world on-hold for the time-being. The he- roes try to convince the king further, but any ad- ditional checks need at least the same degree of success as the first to get his attitude to favorable, where he is willing to call off the attack, and more than one degree of failure on any check moves his attitude to hostile, where he orders the intruders arrested and the attack to begin at once! way: you find a new approach to your argument, new evidence appears, and so forth. The GM may consider you at a disadvantage in further negotiations, imposing a cir- cumstance penalty as well.

— HeroesHandbook, chunk unit_01176, section_path: ATTITUDE / EFFECT

### SleightOfHandContortionAndObservation

CONTORTING

You can use Slight of Hand to contort your body. Make a DC 30 Sleight of Hand check to fit through a tight space wide enough for your head but too narrow for the width of your shoulders, or to reach through an opening wide enough for your hand, but too narrow for your arm.

— HeroesHandbook, chunk unit_01184, section_path: CONCEALING / CONTORTING

* * *

LEGERDEMAIN

Minor feats of sleight of hand, such as making a coin or playing card “vanish,” have a DC of 10 unless an observer is focused on noticing what you are doing. When you per- form this skill under observation, your check is opposed by the observer’s Perception check to see if they notice the trick.

— HeroesHandbook, chunk unit_01202, section_path: SAMPLE RESTRAINT / LEGERDEMAIN

### StealthTailingProcedure

TAILING

You can use Stealth to tail someone at your normal speed. This assumes you have some cover or conceal- ment (crowds of people, shadows, fog, etc.). If the subject is worried about being followed, he can make a Percep- tion check (opposed by your Stealth check) every time he changes course (goes around a street corner, exits a building, and so on). If he is unsuspecting, he only gets one Perception check for the scene. If the subject notices you, make a Deception check, opposed by Insight. If you succeed, you manage to pass off your presence as coinci- dence and can continue tailing. A failed Deception check, or being noticed a second time, means the subject knows something is up and reacts accordingly.

— HeroesHandbook, chunk unit_01218, section_path: OPERATING / TAILING

### TreatmentDiagnosisAndAilmentAssist

DIAGNOSIS

You can diagnose injuries and ailments with an eye to- ward further treatment. This takes at least a minute. At the GM’s discretion, a successful diagnosis provides a +2 bonus for favorable circumstances on further Treatment checks.

— HeroesHandbook, chunk unit_01274, section_path: TASK / DIAGNOSIS

* * *

TREAT DISEASE AND POISON

You can treat a character afflicted with a disease or poison. Each time the character makes a resistance check against the ailment, you make a Treatment check. One degree of success provides the patient with a +2 circumstance bo- nus to the resistance check, three or more degrees of suc- cess provides a +5 circumstance bonus.

— HeroesHandbook, chunk unit_01280, section_path: REVIVE / TREAT DISEASE AND POISON

### SkillCheckPicksEffectTask

CHECK EXAMPLES

Skill checks an effect may require include: Acrobatics: Suitable for effects requiring a measure of coordination or complex maneuvering. Deception: Good for effects intended to deceive, particularly sensory effects like Concealment or Illu- sion, and disguise or form-altering effects like Morph. Expertise: An Expertise skill check might represent having to know something about the subject of the effect or having to know something about the effect itself.

— HeroesHandbook, chunk unit_02972, section_path: DESCRIPTION / CHECK EXAMPLES
