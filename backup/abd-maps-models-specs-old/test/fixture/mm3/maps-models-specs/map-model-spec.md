# Map model spec — HeroesHandbook

_Human-readable twin of `map-model-spec.json`._

## Document metadata

| Field | Value |
|-------|-------|
| Phase | 5 |
| Source corpus | HeroesHandbook |
| Context index | `context/context_index.json` |
| N chunks | *(not stored in JSON per breadth step; see context index)* |
| Phase note | Breadth K-read batches merged into concepts and chunk buckets; hypothesis→scaffolded where batches substantiated. Run scanners + build_chunk_index. |

## Open questions

- unit_00001: chunk is effectively empty (PDF pointer only); no mechanism to map.
- unit_00092, unit_00098: armor and constructs (equipment/headquarters) are outside the six spine modules.
- unit_00108: GM assigning difficulties is GM procedure, not a concrete Check/DifficultyClass object rule in this excerpt.
- unit_00177: new-GM reading guidance; not a spine mechanism.
- unit_00264: session/scene narrative structure; not covered by spine modules.
- unit_00371: move actions (action economy) is outside the named spine modules.
- unit_00401: fragment only (weakened line); insufficient to scaffold a Condition concept beyond parent chunk.
- unit_00452, unit_00466, unit_00472: hero points (scene editing, inspiration, earning) are not represented in the current map-model-spec spine concepts.
- unit_00597, unit_00603, unit_00621, unit_00638, unit_00646: complications, motivations, injuries—story/HP economy, not mapped to the six modules.
- unit_00626: bullet placeholder only; no substantive text.
- unit_00665, unit_00671, unit_00679, unit_00711: naming, appearance, alien origin flavor—character creation outside spine mechanics.
- unit_00584: NPC effective power level vs. points is GM approximation; relationship to PowerPoints/PowerLevel limits needs parent decision.
- unit_00946: Acrobatics maneuver text is truncated mid-sentence; full DC/task set for stunts not available in this chunk.
- unit_01144: Perception chunk lists only the heading 'Awareness' with no mechanical rule.
- unit_01307: Introductory narrative on advantages does not add a distinct spine mechanism beyond existing Advantage / check modifiers.
- unit_01944: Trapping with Create cuts off mid-rule (attack + Dodge resistance incomplete).
- unit_01997: Material Toughness lists substance names without numeric rank values in this excerpt; mapping to Toughness ranks needs adjacent handbook text.
- unit_00925: Deluxe skill name list overlaps batch_0 SkillCatalog (unit_00029); confirm single canonical catalog vs. edition variants.
- unit_01032: Player advice on 'utility skills' is guidance only, not a distinct mechanical object.
- unit_02539 is a fragment with a FLAWS header but body about extended hearing; section alignment in the corpus is unclear.
- unit_02096 and unit_02593 mix multiple rules (effects/OCR layout); confirm whether they should be split for modeling.
- unit_02776 and unit_02878 are partial excerpts; full Area-range and Covering-attack rules may need adjacent chunks.
- unit_02593 combines Strike with minion-related extras (Sacrifice, Variable minions); confirm epic ownership vs. a Minions or Sidekicks cross-cutting area.
- unit_03381: Projectile-weapons chunk is garbled (repeated effect names without table structure); cannot recover rank/cost rows from text alone.
- unit_03441: Shields/armor lines mix stat bonuses with unrelated equipment names; unclear which numbers map to which traits.
- unit_03561: SPACE VEHICLES chunk is numeric fragment only (12 14 14 16) with no labels.
- unit_03680: PERSONNEL feature text is truncated mid-sentence; staffing rules incomplete.
- unit_03696: SECRET feature excerpt starts mid-rule; rebuild timing/conditions not fully stated.
- unit_03875, unit_03887: Single-number or numeric noise chunks; no interpretable rule.
- unit_03976: ENVIRONMENTAL HAZARDS opens a topic but cuts off before hazard mechanics.
- unit_04074: Narrative play-example opener only; no additional mechanical spine beyond flavor.
- unit_04128_merged: MINIONS text is corrupted (bullet gaps, Parry/Dodge sentence spliced in); routine-check and worst-degree rules need a clean K-read.
- unit_04248: FINISHING ATTACK cuts off before full routine-check rule is stated.
- Equipment/vehicles/HQ features (many chunks): rich setting content; mapping to the six spine modules often indirect (effect ranks, DCs, checks) and may need Equipment chapter pairing.

## Cross-cutting notes

[batch 0] Batch 0 mixes TOC fragments, character-creation chapters, and core rules. Resistance checks and conditions tie Abilities (defense bonuses) to Combat resolution; opposed checks and skill pairings bridge Skills and Checks. Several excerpts are table-of-contents or incomplete lines and should not drive new epics without K-read follow-up.

[batch 1] Batch 1 ties Skills to Checks via DCs, opposed rolls, and circumstance modifiers; powers reference attack checks, effect checks, and resistance checks; damage and material toughness link Combat resolution to ranked measurements. Advantages and power extras/flaws modify effective cost and resolution of checks in play.

[batch 2] Batch 2 is dominated by PowerEffect construction (effects, extras/flaws, fractional PP cost, Alternate Effects/arrays, descriptors, devices, equipment, inventing) with recurring ties to skill checks (Perception, Insight, Acrobatics, Expertise, Technology) and resistance/attack resolution (Fortitude, Will, Dodge, Toughness, attack checks). Several chunks are sensory or gear-adjacent (olfactory, survival/SCUBA, criminal surveillance) that still route through powers, equipment, or check modifiers.

[batch 3] Batch 3 mixes gear, vehicles, headquarters, constructs, and conflict chapters. Effect ranks and Affliction/Fortitude DCs tie equipment examples to Powers and ResistanceCheck; attack and defense class tie Abilities to Checks; suffocation, falling, poisons, and hazards link Rank/Measurement intuitions to Fortitude/Toughness loops; minions and Impervous examples alter default attack and resistance resolution. Many chunks are tables, lists, or PDF fragments—concepts stay hypothesis/scaffolded pending cleaner source reads.

---

## 1. Ranks and measures · Translate measurements

### Domain model

### Module: Ranks and measures

- **Foundational (module):** True
- **Description:** Rank values map to concrete measurements (distance, time, mass, volume) via the measurements table. — *chunk:* `unit_00232`
- **Depends on:**
—
- **Concepts:** **Rank**, **MeasurementTable**, **TimeMeasureRow**, **AthleticsJumpDistanceFromCheck**, **MaterialToughnessOrdinalScale**, **CombatRoundDurationEstimate**, **FallDamageRankFromDistanceRank**, **EnvironmentalHazardIntensityExamples**, **VehicleSizeCategoryPointCost**

#### **Rank**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00232`
- **Chunk evidence:** —
- **Owns:** Owns which discrete step on the measurement scale applies to a quantity for a given rank. — *chunk:* `unit_00232`
- **Properties:** —
- **Operations:** —

#### **MeasurementTable**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00222_merged`, `unit_00232`
- **Chunk evidence:** —
- **Owns:** Owns the table mapping each rank row to concrete units (distance, time, mass, volume, etc.). — *chunk:* `unit_00222_merged`
- **Properties:** —
- **Operations:** —

#### **TimeMeasureRow**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00248`
- **Chunk evidence:** —
- **Owns:** Owns the ordered list of concrete time durations corresponding to rank steps on the measurements scale. — *chunk:* `unit_00248`
- **extends:** `MeasurementTable`
- **Properties:** —
- **Operations:** —

#### **AthleticsJumpDistanceFromCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00984`
- **Chunk evidence:** —
- **Owns:** Owns converting an Athletics check result into jump distance in feet, with divisors for standing, vertical, and standing-vertical jumps, and routine distance from (Athletics bonus + 10). — *chunk:* `unit_00984`
- **extends:** `MeasurementTable`
- **Properties:** —
- **Operations:** —

#### **MaterialToughnessOrdinalScale**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01997`
- **Chunk evidence:** —
- **Owns:** Owns ordered material names for Toughness comparisons (paper through super-alloys) as a rank-ordered scale pending numeric rank binding from adjacent rules. — *chunk:* `unit_01997`
- **extends:** `MeasurementTable`
- **Properties:** —
- **Operations:** —

#### **CombatRoundDurationEstimate**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03913`
- **Chunk evidence:** —
- **Owns:** Owns that one action round represents about six seconds of in-world time when turn order and per-turn limits matter. — *chunk:* `unit_03913`
- **extends:** `MeasurementTable`
- **Properties:** —
- **Operations:** —

#### **FallDamageRankFromDistanceRank**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03995`
- **Chunk evidence:** —
- **Owns:** Owns fall damage as base rank 4 plus twice the distance rank fallen, capped at rank 16, before other surface or catcher adjustments. — *chunk:* `unit_03995`
- **extends:** `Rank`
- **Properties:** —
- **Operations:** —

#### **EnvironmentalHazardIntensityExamples**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_04024`
- **Chunk evidence:** —
- **Owns:** Owns example ranked intensities for radiation sources and fire/heats (torch through chemical accelerants) as a hazard reference scale fragment. — *chunk:* `unit_04024`
- **extends:** `MeasurementTable`
- **Properties:** —
- **Operations:** —

#### **VehicleSizeCategoryPointCost**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_03450`, `unit_03475`
- **Chunk evidence:** —
- **Owns:** Owns that vehicles default to medium size and each step up in size category costs one power point, adjusting base Strength, Toughness, and Defense (exact deltas truncated in chunk). — *chunk:* `unit_03450`
- **extends:** `Rank`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Translate measurements

**Full statement:** **Player** interprets **Rank** using **MeasurementTable** rows for distance, time, and related scales. — *chunk:* `unit_00232`

- **Triggering actor:** Player
- **Responding actor:** Gamemaster
- **Confirming stories (scaffold):**
  1. Lookup MeasurementTable
  2. Convert Rank

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00222_merged`, `unit_00232`, `unit_00248`, `unit_00984`, `unit_01997`, `unit_02207`, `unit_02329`, `unit_02562`, `unit_03450`, `unit_03475`, `unit_03913`, `unit_03995`, `unit_04024` |
| provisional | `unit_00048`, `unit_00937`, `unit_03381`, `unit_03574`, `unit_04012` |
| ambiguous | `unit_03381`, `unit_03561` |

---

## 2. Abilities · Express abilities

### Domain model

### Module: Abilities

- **Foundational (module):** True
- **Description:** The eight abilities and their ranks define the hero's baseline capability profile. — *chunk:* `unit_00015`
- **Depends on:**
—
- **Concepts:** **Ability**, **AbilityRank**, **Stamina**, **Awareness**, **AbilityRankPurchase**, **InteractionTargetMentalThreshold**, **ConstructAdvantageAbilityGate**, **StaminaBreathHoldRoundBudget**

#### **Ability**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00015`
- **Chunk evidence:** —
- **Owns:** Owns which of the eight core abilities applies to a rolled or derived value. — *chunk:* `unit_00015`
- **Properties:** —
- **Operations:** —

#### **AbilityRank**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00015`
- **Chunk evidence:** —
- **Owns:** Owns the numeric rank value for each ability on the hero sheet. — *chunk:* `unit_00015`
- **Properties:** —
- **Operations:** —

#### **Stamina**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00775_merged`
- **Chunk evidence:** —
- **Owns:** Owns physical resilience: applies to Toughness, Fortitude, and Stamina checks when no specific defense applies. — *chunk:* `unit_00775_merged`
- **extends:** `Ability`
- **Properties:** —
- **Operations:** —

#### **Awareness**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00793_merged`
- **Chunk evidence:** —
- **Owns:** Owns intuition and common sense: applies to Will, Insight and Perception skill checks, and Awareness checks when no skill applies. — *chunk:* `unit_00793_merged`
- **extends:** `Ability`
- **Properties:** —
- **Operations:** —

#### **AbilityRankPurchase**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00749`, `unit_00810_merged`
- **Chunk evidence:** —
- **Owns:** Owns spending 2 power points per +1 ability rank, subject to power level limits. — *chunk:* `unit_00749`
- **extends:** `AbilityRank`
- **Properties:** —
- **Operations:** —

#### **InteractionTargetMentalThreshold**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00907`
- **Chunk evidence:** —
- **Owns:** Owns circumstance penalties and outright prohibition when using interaction skills on subjects by Intellect rank (–5 at Int –5, unusable if missing mental abilities) and awareness/understanding requirements. — *chunk:* `unit_00907`
- **extends:** `AbilityRank`
- **Properties:** —
- **Operations:** —

#### **ConstructAdvantageAbilityGate**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03751`
- **Chunk evidence:** —
- **Owns:** Owns that constructs cannot take advantages that require abilities the construct does not have (parallel to skill restrictions). — *chunk:* `unit_03751`
- **extends:** `Ability`
- **Properties:** —
- **Operations:** —

#### **StaminaBreathHoldRoundBudget**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03995`
- **Chunk evidence:** —
- **Owns:** Owns holding breath for ten rounds plus rounds equal to twice Stamina rank before suffocation Fortitude checks begin. — *chunk:* `unit_03995`
- **extends:** `Stamina`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Express abilities

**Full statement:** **Player** assigns and reads **Ability** and **AbilityRank** when building and playing the hero. — *chunk:* `unit_00015`

- **Triggering actor:** Player
- **Responding actor:** Gamemaster
- **Confirming stories (scaffold):**
  1. Read Ability rank
  2. Set Ability rank

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00015`, `unit_00749`, `unit_00775_merged`, `unit_00793_merged`, `unit_00810_merged`, `unit_00907`, `unit_03751`, `unit_03995` |
| provisional | `unit_00017`, `unit_00835`, `unit_03735` |
| ambiguous | `unit_00835` |

---

## 3. Checks and tasks · Resolve checks

### Domain model

### Module: Checks and tasks

- **Foundational (module):** True
- **Description:** Tasks use checks against a Difficulty Class; degrees of success and failure interpret the margin. — *chunk:* `unit_00266`
- **Depends on:**
- **Ranks and measures** provides `Rank, MeasurementTable` for dependents `Check, DifficultyClass` — Difficulty values and measurement scales align with ranked tables (cited in check rules).
- **Concepts:** **Check**, **DifficultyClass**, **OpposedCheck**, **CriticalSuccess**, **ToolingPenalty**, **PrecariousSurfaceMovementCheck**, **SkillCheckModifierSources**, **AcrobaticsTaskMenu**, **ClimbCircumstanceModifierTable**, **DeceptionBelievabilityDCAdjustment**, **ForensicEvidenceAnalysisCheck**, **VisualPerceptionVisibilityDC**, **JuryRiggedRepairCheck**, **SecurityOrTrapDCLadder**, **UltimateEffortFixedResult**, **OpposedEffectCheck**, **AttackCheckVersusDefenseClass**, **RoutineAttackCheckAgainstMinion**, **TechnologyRestrictedCommunicationsDC**, **CatchFallingTargetDexterityDC**, **AllOutAttackDefenseForAttackTrade**, **StandardAndMoveActionPerCombatRound**, **ReactionVersusFreeActionTiming**

#### **Check**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00266`, `unit_00282`
- **Chunk evidence:** —
- **Owns:** Owns when a d20 roll plus modifiers is compared to a target to resolve a task outcome. — *chunk:* `unit_00266`
- **Properties:** —
- **Operations:** —

#### **DifficultyClass**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00282`
- **Chunk evidence:** —
- **Owns:** Owns the fixed target number a check must meet or beat for success. — *chunk:* `unit_00282`
- **Properties:** —
- **Operations:** —

#### **OpposedCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00326`
- **Chunk evidence:** —
- **Owns:** Owns resolving a contest by comparing two check results as the DC, with tie-breakers for equal results. — *chunk:* `unit_00326`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **CriticalSuccess**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00280`
- **Chunk evidence:** —
- **Owns:** Owns increasing degree of success by one when the d20 shows a natural 20 on a check. — *chunk:* `unit_00280`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **ToolingPenalty**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00347`
- **Chunk evidence:** —
- **Owns:** Owns imposing -5 on a check without required tools, or -2 with makeshift tools when the GM allows. — *chunk:* `unit_00347`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **PrecariousSurfaceMovementCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00937`
- **Chunk evidence:** —
- **Owns:** Owns moving along a precarious surface at ground speed minus 1 rank after a successful Acrobatics check vs. surface DC, with degrees of failure costing movement or causing a fall. — *chunk:* `unit_00937`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **SkillCheckModifierSources**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00891`
- **Chunk evidence:** —
- **Owns:** Owns that miscellaneous modifiers from circumstances, advantages, and powers stack toward meeting or beating a DC (often based on another character's traits). — *chunk:* `unit_00891`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **AcrobaticsTaskMenu**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00965`
- **Chunk evidence:** —
- **Owns:** Owns named Acrobatics applications (lessen fall damage per degree, acrobatic maneuver, prone-to-stand free action, contort through tight space) as task labels for checks. — *chunk:* `unit_00965`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **ClimbCircumstanceModifierTable**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00978`
- **Chunk evidence:** —
- **Owns:** Owns listed circumstance modifiers for climbing (bracing, corner, short climb, slipperiness, speed bonus, vulnerability while climbing). — *chunk:* `unit_00978`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **DeceptionBelievabilityDCAdjustment**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01026`
- **Chunk evidence:** —
- **Owns:** Owns DC shifts for Deception based on target willingness and how believable or risky the deception is (–5 to +20 per listed factors). — *chunk:* `unit_01026`
- **extends:** `DifficultyClass`
- **Properties:** —
- **Operations:** —

#### **ForensicEvidenceAnalysisCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01130_merged`
- **Chunk evidence:** —
- **Owns:** Owns Investigation check (base DC 15, time and disturbance modifiers) to extract information from existing evidence; two+ degrees of failure may mislead at GM discretion. — *chunk:* `unit_01130_merged`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **VisualPerceptionVisibilityDC**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01160`
- **Chunk evidence:** —
- **Owns:** Owns baseline DCs for spotting something by sight (plain sight 0, subtle 5–10+), opposed Stealth, and ties to disguise and concealed objects per linked skills. — *chunk:* `unit_01160`
- **extends:** `DifficultyClass`
- **Properties:** —
- **Operations:** —

#### **JuryRiggedRepairCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01226`
- **Chunk evidence:** —
- **Owns:** Owns temporary Technology repair with total –10 DC adjustment, standard-action check, single problem fixed, lasting until scene end, then requiring full repair before re-jury-rigging. — *chunk:* `unit_01226`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **SecurityOrTrapDCLadder**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01256`
- **Chunk evidence:** —
- **Owns:** Owns escalating DC rungs (10 through 40+5) for bypassing security/traps, with failure doing nothing and multiple degrees of failure triggering alarms or traps when possible. — *chunk:* `unit_01256`
- **extends:** `DifficultyClass`
- **Properties:** —
- **Operations:** —

#### **UltimateEffortFixedResult**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01644_merged`
- **Chunk evidence:** —
- **Owns:** Owns spending a hero point to treat a check result as 20 for Ultimate Aim (next round's aimed attack check), Ultimate Resistance (one chosen defense), or Ultimate Skill (one skill). — *chunk:* `unit_01644_merged`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **OpposedEffectCheck**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_02137`, `unit_02160`, `unit_02269`
- **Chunk evidence:** —
- **Owns:** Owns opposed checks where an effect’s rank or user sets DC or competes with a target’s roll (e.g., Illusion vs. Insight, Mind Reading vs. Will). — *chunk:* `unit_02137`
- **Properties:** —
- **Operations:** —

#### **AttackCheckVersusDefenseClass**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04040`
- **Chunk evidence:** —
- **Owns:** Owns attack resolution as d20 plus attack bonus meeting or beating the target defense class to hit. — *chunk:* `unit_04040`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **RoutineAttackCheckAgainstMinion**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_04128_merged`
- **Chunk evidence:** —
- **Owns:** Owns that non-minions may treat attack checks against minions as routine checks (minion combat chunk partially corrupted). — *chunk:* `unit_04128_merged`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **TechnologyRestrictedCommunicationsDC**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03622`
- **Chunk evidence:** —
- **Owns:** Owns DC 25 on a Technology skill check to gain illegal access to restricted communication systems when the GM allows. — *chunk:* `unit_03622`
- **extends:** `DifficultyClass`
- **Properties:** —
- **Operations:** —

#### **CatchFallingTargetDexterityDC**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03995`
- **Chunk evidence:** —
- **Owns:** Owns DC 5 Dexterity check to catch a falling person or object, then subtract catcher Strength (or GM-approved power rank) from fall damage rank for split remainder damage. — *chunk:* `unit_03995`
- **extends:** `DifficultyClass`
- **Properties:** —
- **Operations:** —

#### **AllOutAttackDefenseForAttackTrade**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04242`
- **Chunk evidence:** —
- **Owns:** Owns voluntarily taking up to -2 on Dodge and Parry until start of next turn to add up to +2 attack bonus, with defenses not below +0 and attack not more than doubled. — *chunk:* `unit_04242`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **StandardAndMoveActionPerCombatRound**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03921`
- **Chunk evidence:** —
- **Owns:** Owns that during a combat round a character can take one standard action and one move action on their turn (in addition to free/reaction rules elsewhere). — *chunk:* `unit_03921`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **ReactionVersusFreeActionTiming**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03937`
- **Chunk evidence:** —
- **Owns:** Owns that reactions are like free actions in speed but can occur off-turn in response to events, unlike conscious free actions on your turn. — *chunk:* `unit_03937`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Resolve checks

**Full statement:** **Player** rolls a **Check** against **DifficultyClass** and applies degree outcomes. — *chunk:* `unit_00266`

- **Triggering actor:** Player
- **Responding actor:** Gamemaster
- **Confirming stories (scaffold):**
  1. Roll versus DifficultyClass
  2. Compare check margin

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00167`, `unit_00266`, `unit_00280`, `unit_00282`, `unit_00326`, `unit_00347`, `unit_00891`, `unit_00937`, `unit_00965`, `unit_00978`, `unit_01026`, `unit_01130_merged`, `unit_01160`, `unit_01226`, `unit_01256`, `unit_01644_merged`, `unit_02056`, `unit_02137`, `unit_02160`, `unit_02972`, `unit_03296_s2`, `unit_03622`, `unit_03921`, `unit_03937`, `unit_03995`, `unit_04040`, `unit_04128_merged`, `unit_04242` |
| provisional | `unit_00108`, `unit_00946`, `unit_04248` |
| ambiguous | `unit_04128_merged` |

---

## 4. Skills · Apply skills

### Domain model

### Module: Skills

- **Foundational (module):** True
- **Description:** Skills apply trained or untrained use of abilities to specific tasks, usually as skill checks. — *chunk:* `unit_00025`
- **Depends on:**
- **Abilities** provides `Ability, AbilityRank` for dependents `Skill, SkillCheck` — Skills apply ability ranks and modifiers to trained tasks.
- **Checks and tasks** provides `Check, DifficultyClass` for dependents `SkillCheck` — Skill checks are resolved as checks against DC.
- **Concepts:** **Skill**, **SkillCheck**, **SkillCatalog**, **OpposedSkillPairing**, **InteractionSkill**, **CloseCombatSkillSpecialization**, **ExpertiseRoutineAndPlayerBoundary**, **CovertMessageSkillExchange**, **InsightVersusIllusion**, **InvestigationVersusPerceptionSearch**, **PersuasionAttitudeShift**, **SleightOfHandContortionAndObservation**, **StealthTailingProcedure**, **TechnologyInventingPrerequisite**, **TreatmentDiagnosisAndAilmentAssist**, **SkillCheckPicksEffectTask**, **TechnologySkillHQCommunicationsUse**, **AcrobaticsMitigateFallDistance**, **TechnologyRepairDamagedObjects**

#### **Skill**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00025`
- **Chunk evidence:** —
- **Owns:** Owns which trained ability applies to a given category of task. — *chunk:* `unit_00025`
- **Properties:** —
- **Operations:** —

#### **SkillCheck**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00025`
- **Chunk evidence:** —
- **Owns:** Owns the roll procedure when a skill (trained or untrained) applies to a task. — *chunk:* `unit_00025`
- **Properties:** —
- **Operations:** —

#### **SkillCatalog**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00029`
- **Chunk evidence:** —
- **Owns:** Owns the named default skill list (Acrobatics through Vehicles) as the chapter index for skill descriptions. — *chunk:* `unit_00029`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **OpposedSkillPairing**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00306`
- **Chunk evidence:** —
- **Owns:** Owns which opposing skill is rolled for common contests (e.g. Stealth vs Perception). — *chunk:* `unit_00306`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **InteractionSkill**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00907`
- **Chunk evidence:** —
- **Owns:** Owns social interaction skills aimed at influencing others, requiring subjects to be aware and able to understand the user, with stronger use on sufficiently intelligent subjects. — *chunk:* `unit_00907`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **CloseCombatSkillSpecialization**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01006`
- **Chunk evidence:** —
- **Owns:** Owns separate Close Combat skills per specific close attack (weapon or power), granting attack check bonus equal to skill rank, with scope limits (e.g. not all unarmed maneuvers). — *chunk:* `unit_01006`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **ExpertiseRoutineAndPlayerBoundary**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01066`
- **Chunk evidence:** —
- **Owns:** Owns using Expertise checks or routine (bonus + 10) to bound what the character knows versus player knowledge; GM may allow hero-point 'hunch' exceptions. — *chunk:* `unit_01066`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **CovertMessageSkillExchange**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01043`, `unit_01089`
- **Chunk evidence:** —
- **Owns:** Owns Deception (innuendo) DCs for covert messages and recipient Insight against the same DC to understand; Insight also used to detect hidden Deception messages. — *chunk:* `unit_01043`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **InsightVersusIllusion**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01075`
- **Chunk evidence:** —
- **Owns:** Owns secret Insight check (DC 10 + Illusion rank) to notice flaws in an illusion, revealing it as unreal. — *chunk:* `unit_01075`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **InvestigationVersusPerceptionSearch**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01113`
- **Chunk evidence:** —
- **Owns:** Owns that Perception notices immediately while Investigation finds clues, traps, and details with effort when searching an area. — *chunk:* `unit_01113`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **PersuasionAttitudeShift**

- **Evidence stage:** deepened
- **Foundational (concept):** True
- **Chunk ids:** `unit_01176`
- **Chunk evidence:** —
- **Owns:** Owns attitude track (hostile through helpful), standard-action persuasion, limits during conflict, repeated attempts against initial attitude, and degree-based shifts with example. — *chunk:* `unit_01176`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **SleightOfHandContortionAndObservation**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01184`, `unit_01202`
- **Chunk evidence:** —
- **Owns:** Owns DC 30 contortion through tight openings and minor legerdemain (DC 10) opposed by observer Perception when watched. — *chunk:* `unit_01184`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **StealthTailingProcedure**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01218`
- **Chunk evidence:** —
- **Owns:** Owns tailing at normal speed with cover, Perception checks on course changes or once if unsuspecting, and Deception vs Insight to pass off being noticed. — *chunk:* `unit_01218`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **TechnologyInventingPrerequisite**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01247`
- **Chunk evidence:** —
- **Owns:** Owns using Technology to create inventions when the character has the Inventor advantage, deferring full rules to the Inventing section. — *chunk:* `unit_01247`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **TreatmentDiagnosisAndAilmentAssist**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01274`, `unit_01280`
- **Chunk evidence:** —
- **Owns:** Owns minute-long diagnosis granting +2 circumstance on later Treatment checks at GM discretion, and Treatment checks each resistance attempt against disease/poison to grant +2 or +5 to the patient's resistance on degrees of success. — *chunk:* `unit_01274`
- **extends:** `SkillCheck`
- **Properties:** —
- **Operations:** —

#### **SkillCheckPicksEffectTask**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_02972`
- **Chunk evidence:** —
- **Owns:** Owns which skill applies when an effect’s operation is modeled as a task (examples: Acrobatics, Deception, Expertise). — *chunk:* `unit_02972`
- **Properties:** —
- **Operations:** —

#### **TechnologySkillHQCommunicationsUse**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03622`
- **Chunk evidence:** —
- **Owns:** Owns Technology skill as the gate for illegal access to restricted bands on headquarters communications gear, given user clearance and GM permission. — *chunk:* `unit_03622`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **AcrobaticsMitigateFallDistance**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_03995`
- **Chunk evidence:** —
- **Owns:** Owns Acrobatics skill allowing falls from greater distances without damage (exact thresholds not in this chunk). — *chunk:* `unit_03995`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

#### **TechnologyRepairDamagedObjects**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04279`, `unit_04100`
- **Chunk evidence:** —
- **Owns:** Owns using the Technology skill guidelines to repair damaged objects that lack Stamina-based natural recovery (per conflict recovery discussion). — *chunk:* `unit_04279`
- **extends:** `Skill`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Apply skills

**Full statement:** **Player** invokes **Skill** and **SkillCheck** when a task calls for trained expertise. — *chunk:* `unit_00025`

- **Triggering actor:** Player
- **Responding actor:** Gamemaster
- **Confirming stories (scaffold):**
  1. Roll SkillCheck
  2. Declare Skill use

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00025`, `unit_00029`, `unit_00306`, `unit_00907`, `unit_00925`, `unit_01006`, `unit_01032`, `unit_01043`, `unit_01066`, `unit_01075`, `unit_01089`, `unit_01113`, `unit_01176`, `unit_01184`, `unit_01202`, `unit_01218`, `unit_01247`, `unit_01274`, `unit_01280`, `unit_02096`, `unit_02232`, `unit_03208`, `unit_03254`, `unit_03292`, `unit_03622`, `unit_03995`, `unit_04100`, `unit_04279` |
| provisional | `unit_01144` |
| ambiguous |  |

---

## 5. Powers · Acquire powers

### Domain model

### Module: Powers

- **Foundational (module):** True
- **Description:** Powers are built from effects, ranked with power points, and expressed as abilities on the character. — *chunk:* `unit_00038`
- **Depends on:**
- **Abilities** provides `Ability, AbilityRank` for dependents `PowerEffect, PowerPoints` — Power builds tie to ability defenses and ranks.
- **Checks and tasks** provides `Check, DifficultyClass` for dependents `PowerEffect` — Powers use attack checks, effect checks, and resistance DCs.
- **Concepts:** **PowerEffect**, **PowerPoints**, **Advantage**, **Descriptor**, **ExtraEffortPowerSurge**, **PowerLevel**, **AdvantageNameGroupings**, **AdvantageRankAndDescriptionPattern**, **PowerEffectStandardCostPerRank**, **SeriesRequiredDescriptorRule**, **PowerEffectType**, **DefensePowerEffectPattern**, **PowerActivationAndResolution**, **PowerEffectNameTableFragment**, **PowerEffectSummaryLine**, **PowerExtraSection**, **SamplePowerWriteupSchema**, **AlternateFormDescriptorPackages**, **BlastRangedDamageEffect**, **CommunicationLimitedFlaw**, **PerceptionRangeTargetingAndConcealment**, **ConcealmentEffectExtras**, **CreateEffectExtras**, **EnhancedTraitLimitedAndPermanent**, **PowerModifierCatalog**, **AlternateEffectArray**, **DescriptorLayer**, **EquipmentAfflictionFortitudeDCExample**, **ConstructArchetypePowerExamples**, **AlternateVehicleEquipmentPointPricing**, **HeadquartersDefenseSystemEffectCap**

#### **PowerEffect**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00038`
- **Chunk evidence:** —
- **Owns:** Owns the mechanical effect definition and rank for a purchased power. — *chunk:* `unit_00038`
- **Properties:** —
- **Operations:** —

#### **PowerPoints**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00056`, `unit_00038`
- **Chunk evidence:** —
- **Owns:** Owns the budget spent to build and rank powers on the character. — *chunk:* `unit_00056`
- **Properties:** —
- **Operations:** —

#### **Advantage**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00220`, `unit_00518`
- **Chunk evidence:** —
- **Owns:** Owns minor benefits between skills and powers, sometimes ranked, purchased with power points. — *chunk:* `unit_00220`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **Descriptor**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00695`, `unit_00080`
- **Chunk evidence:** —
- **Owns:** Owns labels such as origin (mutant, mystic, alien) applied to powers for interaction with effects and devices. — *chunk:* `unit_00695`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **ExtraEffortPowerSurge**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00433`, `unit_00439`
- **Chunk evidence:** —
- **Owns:** Owns temporarily increasing one power effect by +1 rank until the start of the hero's next turn. — *chunk:* `unit_00433`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerLevel**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00502`, `unit_00524`, `unit_00729`
- **Chunk evidence:** —
- **Owns:** Owns the series limit that sets starting power points and caps where traits may be spent. — *chunk:* `unit_00502`
- **extends:** `PowerPoints`
- **Properties:** —
- **Operations:** —

#### **AdvantageNameGroupings**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01362_merged`
- **Chunk evidence:** —
- **Owns:** Owns exemplar groupings of advantage names (general and skill-related lists) as handbook index material for character building. — *chunk:* `unit_01362_merged`
- **extends:** `Advantage`
- **Properties:** —
- **Operations:** —

#### **AdvantageRankAndDescriptionPattern**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01317`
- **Chunk evidence:** —
- **Owns:** Owns that advantages are listed with name, type, optional ranks, and text describing benefits including extra rank effects and comparisons to characters without the advantage. — *chunk:* `unit_01317`
- **extends:** `Advantage`
- **Properties:** —
- **Operations:** —

#### **PowerEffectStandardCostPerRank**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01682`
- **Chunk evidence:** —
- **Owns:** Owns that each power effect is bought in ranks like other traits, with greater rank meaning greater effect, and each effect has a standard cost per rank. — *chunk:* `unit_01682`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **SeriesRequiredDescriptorRule**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01695`
- **Chunk evidence:** —
- **Owns:** Owns GM-mandated descriptors (e.g. mutant, psychic) applying to all powers in a series unless justified otherwise, with possible Benefit or complications for exceptions. — *chunk:* `unit_01695`
- **extends:** `Descriptor`
- **Properties:** —
- **Operations:** —

#### **PowerEffectType**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01705`
- **Chunk evidence:** —
- **Owns:** Owns categorization of power effects into types that share rules and provide descriptors for interactions with other effects. — *chunk:* `unit_01705`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **DefensePowerEffectPattern**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01711`
- **Chunk evidence:** —
- **Owns:** Owns that defense effects typically grant resistance bonuses or immunity, often personal, subtle, permanent, or free-action sustained with on/off vulnerability. — *chunk:* `unit_01711`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerActivationAndResolution**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01733`
- **Chunk evidence:** —
- **Owns:** Owns that some effects work automatically while others require effort such as attack or effect checks, and effects on others allow resistance checks unless waived. — *chunk:* `unit_01733`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerEffectNameTableFragment**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01764`, `unit_01783`
- **Chunk evidence:** —
- **Owns:** Owns partial alphabetical index rows of power effect names as handbook fragments (two consecutive table chunks). — *chunk:* `unit_01764`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerEffectSummaryLine**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01824`
- **Chunk evidence:** —
- **Owns:** Owns the standard one-line presentation of Action, Range, Duration, and Cost for an effect block. — *chunk:* `unit_01824`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerExtraSection**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01833`
- **Chunk evidence:** —
- **Owns:** Owns the extras subsection listing optional modifiers for an effect, including effect-unique extras highlighted in handbook layout. — *chunk:* `unit_01833`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **SamplePowerWriteupSchema**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01846`, `unit_01844`
- **Chunk evidence:** —
- **Owns:** Owns the fields for sample powers: name, listed effect(s) with modifiers, and cost (per rank, flat, or hybrid). — *chunk:* `unit_01846`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **AlternateFormDescriptorPackages**

- **Evidence stage:** deepened
- **Foundational (concept):** True
- **Chunk ids:** `unit_01855`
- **Chunk evidence:** —
- **Owns:** Owns example alternate forms (energy, gaseous, ghost, heroic, liquid, particulate, shadow, solid, swarm, two-dimensional) expressed as bundled suggested effects and modifiers. — *chunk:* `unit_01855`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **BlastRangedDamageEffect**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01872`
- **Chunk evidence:** —
- **Owns:** Owns the Blast sample: ranged Damage at 2 points per rank, ranged attack vs Dodge, damage equal to rank, Toughness resistance, with optional descriptor narrowing flaw text. — *chunk:* `unit_01872`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **CommunicationLimitedFlaw**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01897`
- **Chunk evidence:** —
- **Owns:** Owns Limited flaw examples for Communication (audience group restriction; Communication-Dependent carrier for other perception-range effects) with –1 cost per rank where applicable. — *chunk:* `unit_01897`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PerceptionRangeTargetingAndConcealment**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01919`
- **Chunk evidence:** —
- **Owns:** Owns that perception-range effects need accurate perception of the target (total concealment blocks), optional acute-sense Perception check to locate, and +5 resistance if concealed. — *chunk:* `unit_01919`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **ConcealmentEffectExtras**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01928`
- **Chunk evidence:** —
- **Owns:** Owns extras for Concealment (Affects Others, Area, Attack, Precise) with stated point or per-rank costs and interaction rules. — *chunk:* `unit_01928`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **CreateEffectExtras**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01955`
- **Chunk evidence:** —
- **Owns:** Owns extras for Create (Continuous, Impervious, Innate, Movable, Precise, Selective) with cost notes and object behavior implications. — *chunk:* `unit_01955`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **EnhancedTraitLimitedAndPermanent**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_02025`
- **Chunk evidence:** —
- **Owns:** Owns Limited flaw patterns and Permanent modifier behavior for Enhanced Trait (always on, no extra effort stunts, complication for rare limits). — *chunk:* `unit_02025`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **PowerModifierCatalog**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_02070`, `unit_02123`, `unit_02154`, `unit_02189`, `unit_02232`, `unit_02310`, `unit_02361_s1`, `unit_02388`, `unit_02397`, `unit_02408`, `unit_02618`, `unit_02655`, `unit_02668_s2`, `unit_02692`, `unit_03055`, `unit_03166`
- **Chunk evidence:** —
- **Owns:** Owns named extras and flaws that adjust power point cost per rank or add flat costs, and how they combine (including fractional PP:R ratios). — *chunk:* `unit_02692`
- **Properties:** —
- **Operations:** —

#### **AlternateEffectArray**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_02751_s1`, `unit_03248`
- **Chunk evidence:** —
- **Owns:** Owns themed Alternate Effect collections, GM oversight, and point-budget constraints relative to a primary effect. — *chunk:* `unit_02751_s1`
- **Properties:** —
- **Operations:** —

#### **DescriptorLayer**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_03090`, `unit_03129`, `unit_03142`
- **Chunk evidence:** —
- **Owns:** Owns descriptor types (including result descriptors), when descriptors are applied or revealed in play, and hero-point handling for descriptor surprises. — *chunk:* `unit_03090`
- **Properties:** —
- **Operations:** —

#### **EquipmentAfflictionFortitudeDCExample**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_03364`
- **Chunk evidence:** —
- **Owns:** Owns taser as compressed-air darts imposing Affliction resisted by Fortitude at DC 15 (equipment-stated effect parameters). — *chunk:* `unit_03364`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **ConstructArchetypePowerExamples**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_03784`, `unit_03847`
- **Chunk evidence:** —
- **Owns:** Owns sample construct power packages (e.g. undead Fortitude Immunity; armor Protection; robot Fortitude Immunity; giant Growth) as minion-scale references. — *chunk:* `unit_03847`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

#### **AlternateVehicleEquipmentPointPricing**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03499`
- **Chunk evidence:** —
- **Owns:** Owns paying full equipment cost for the most expensive vehicle and one equipment point per additional vehicle of same or lesser cost (Alternate Equipment pattern for vehicles). — *chunk:* `unit_03499`
- **extends:** `PowerPoints`
- **Properties:** —
- **Operations:** —

#### **HeadquartersDefenseSystemEffectCap**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03628`
- **Chunk evidence:** —
- **Owns:** Owns HQ defense emplacements using attack effects costing no more than twice headquarters power level, with attack bonus equal to that power level. — *chunk:* `unit_03628`
- **extends:** `PowerEffect`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Acquire powers

**Full statement:** **Player** spends **PowerPoints** to define **PowerEffect** entries on the hero sheet. — *chunk:* `unit_00038`

- **Triggering actor:** Player
- **Responding actor:** Gamemaster
- **Confirming stories (scaffold):**
  1. Buy PowerEffect
  2. Spend PowerPoints

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00038`, `unit_00056`, `unit_00220`, `unit_00433`, `unit_00502`, `unit_00518`, `unit_00532`, `unit_00549`, `unit_00695`, `unit_01317`, `unit_01362_merged`, `unit_01682`, `unit_01695`, `unit_01705`, `unit_01711`, `unit_01733`, `unit_01764`, `unit_01783`, `unit_01792_merged`, `unit_01824`, `unit_01833`, `unit_01844`, `unit_01846`, `unit_01855`, `unit_01872`, `unit_01897`, `unit_01919`, `unit_01928`, `unit_01955`, `unit_02025`, `unit_02043`, `unit_02070`, `unit_02123`, `unit_02154`, `unit_02189`, `unit_02213`, `unit_02269`, `unit_02301`, `unit_02310`, `unit_02337`, `unit_02352`, `unit_02361_s1`, `unit_02388`, `unit_02397`, `unit_02408`, `unit_02489`, `unit_02539`, `unit_02593`, `unit_02618`, `unit_02655`, `unit_02668_s2`, `unit_02677`, `unit_02692`, `unit_02719`, `unit_02751_s1`, `unit_02776`, `unit_03036`, `unit_03055`, `unit_03090`, `unit_03129`, `unit_03142`, `unit_03166`, `unit_03202`, `unit_03214`, `unit_03248`, `unit_03270`, `unit_03278`, `unit_03349`, `unit_03364`, `unit_03391`, `unit_03415`, `unit_03499`, `unit_03628`, `unit_03784`, `unit_03847` |
| provisional | `unit_00080`, `unit_00420`, `unit_00439`, `unit_00524`, `unit_00562`, `unit_00584`, `unit_00729`, `unit_01307`, `unit_01944`, `unit_03574`, `unit_03751` |
| ambiguous | `unit_00420`, `unit_01944`, `unit_02539`, `unit_02593`, `unit_02776`, `unit_03349` |

---

## 6. Combat resolution · Track combat state

### Domain model

### Module: Combat resolution

- **Foundational (module):** True
- **Description:** Conditions track temporary states; resistance checks resolve many hostile effects. — *chunk:* `unit_00385`
- **Depends on:**
- **Abilities** provides `Ability, AbilityRank` for dependents `ResistanceCheck, Condition` — Resistance saves use defense abilities; conditions alter capability.
- **Checks and tasks** provides `Check, DifficultyClass` for dependents `ResistanceCheck` — Resistance checks are checks against an effect DC.
- **Concepts:** **Condition**, **ResistanceCheck**, **BasicCondition**, **InitiativeCheck**, **ActiveDefenseDegradation**, **IntimidationDemoralize**, **FightingStyleAdvantageBundleExamples**, **EffectResistanceWaiverRules**, **DamageResistanceDegreeOutcomes**, **CoveringAttack**, **TurnStartEndsUntilNextTurnEffects**, **ToughnessResistanceAfterDamageHit**, **SuffocationFortitudeEscalation**, **ConditionsFromResistanceFailure**, **AreaAndPerceptionAutomaticEffectResolution**, **ImperviousSkipsUnneededAttackRoll**, **MinionCombatResolutionPackage**, **DamageConditionMinuteRecovery**, **HeroDeathVersusMinionLethality**, **OptionalInitiativeForTimedChallenge**

#### **Condition**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00385`
- **Chunk evidence:** —
- **Owns:** Owns which temporary status applies to a character and how it alters play. — *chunk:* `unit_00385`
- **Properties:** —
- **Operations:** —

#### **ResistanceCheck**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_00363_merged`
- **Chunk evidence:** —
- **Owns:** Owns the saving throw against an effect when rules call for Fortitude, Will, or Dodge resistance. — *chunk:* `unit_00363_merged`
- **Properties:** —
- **Operations:** —

#### **BasicCondition**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00387_merged`, `unit_00412`
- **Chunk evidence:** —
- **Owns:** Owns single-modifier status building blocks (e.g. compelled, controlled, dazed, debilitated, defenseless) that compose conditions. — *chunk:* `unit_00387_merged`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **InitiativeCheck**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00862`
- **Chunk evidence:** —
- **Owns:** Owns ordering turns using d20 plus initiative modifier (Agility + Improved Initiative + power modifiers). — *chunk:* `unit_00862`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **ActiveDefenseDegradation**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_00856`, `unit_00835`
- **Chunk evidence:** —
- **Owns:** Owns halving Dodge and Parry when vulnerable and reducing both to 0 when defenseless. — *chunk:* `unit_00856`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **IntimidationDemoralize**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01107`
- **Chunk evidence:** —
- **Owns:** Owns standard-action Intimidation in combat to impose impaired (–2 checks) or, with four+ degrees of success, disabled (–5 checks) until end of aggressor's next round. — *chunk:* `unit_01107`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **FightingStyleAdvantageBundleExamples**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_01423_merged`
- **Chunk evidence:** —
- **Owns:** Owns sample combinations of advantages illustrating martial fighting styles (boxing, judo, kung fu, sword-fighting, wrestling) including optional Close Attack ranks. — *chunk:* `unit_01423_merged`
- **extends:** `Advantage`
- **Properties:** —
- **Operations:** —

#### **EffectResistanceWaiverRules**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_01792_merged`
- **Chunk evidence:** —
- **Owns:** Owns voluntary waiver of resistance except Toughness; optional discontinuation of sustained/continuous Toughness bonuses; Immunity skipping checks; Instant duration definition start. — *chunk:* `unit_01792_merged`
- **extends:** `ResistanceCheck`
- **Properties:** —
- **Operations:** —

#### **DamageResistanceDegreeOutcomes**

- **Evidence stage:** deepened
- **Foundational (concept):** True
- **Chunk ids:** `unit_01979`
- **Chunk evidence:** —
- **Owns:** Owns Toughness resistance vs (damage rank + 15) with degrees mapping to cumulative –1 circumstance, dazed, staggered, incapacitated, and repeated stagger leading to fourth-degree effect. — *chunk:* `unit_01979`
- **extends:** `ResistanceCheck`
- **Properties:** —
- **Operations:** —

#### **CoveringAttack**

- **Evidence stage:** hypothesis
- **Foundational (concept):** False
- **Chunk ids:** `unit_02878`
- **Chunk evidence:** —
- **Owns:** Owns trade-offs where a target accepts exposure to a covering attack to gain an automatic attack in return (uses attack checks). — *chunk:* `unit_02878`
- **Properties:** —
- **Operations:** —

#### **TurnStartEndsUntilNextTurnEffects**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03943_merged`
- **Chunk evidence:** —
- **Owns:** Owns ending effects that last until the start of your next turn when that turn begins (partial turn-start checklist). — *chunk:* `unit_03943_merged`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **ToughnessResistanceAfterDamageHit**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04059`
- **Chunk evidence:** —
- **Owns:** Owns that a successful hit with Damage forces a Toughness resistance check. — *chunk:* `unit_04059`
- **extends:** `ResistanceCheck`
- **Properties:** —
- **Operations:** —

#### **SuffocationFortitudeEscalation**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03995`
- **Chunk evidence:** —
- **Owns:** Owns repeating Fortitude checks (DC 10 +1 per prior success) each round after breath limit; failure leads to incapacitated then dying unless breathing restored; Immunity to Suffocation bypasses. — *chunk:* `unit_03995`
- **extends:** `ResistanceCheck`
- **Properties:** —
- **Operations:** —

#### **ConditionsFromResistanceFailure**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04147`
- **Chunk evidence:** —
- **Owns:** Owns that failed resistance checks against attacks impose conditions by effect type and failure degree, referencing effect text and Conditions in Basics. — *chunk:* `unit_04147`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **AreaAndPerceptionAutomaticEffectResolution**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04108`
- **Chunk evidence:** —
- **Owns:** Owns that Perception and Area attacks skip attack checks, cannot crit or miss, and ignore attack-check modifiers including maneuvers. — *chunk:* `unit_04108`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

#### **ImperviousSkipsUnneededAttackRoll**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_04085`
- **Chunk evidence:** —
- **Owns:** Owns skipping attack rolls when incoming damage cannot overcome Impervious Toughness threshold (play-example: guns vs Impervious 8). — *chunk:* `unit_04085`
- **extends:** `ResistanceCheck`
- **Properties:** —
- **Operations:** —

#### **MinionCombatResolutionPackage**

- **Evidence stage:** hypothesis
- **Foundational (concept):** True
- **Chunk ids:** `unit_04128_merged`
- **Chunk evidence:** —
- **Owns:** Owns bundled minion combat exceptions: no critical hits vs non-minions; failed resistance suffers worst effect degree; routine attacks allowed for non-minions (chunk partially corrupted). — *chunk:* `unit_04128_merged`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **DamageConditionMinuteRecovery**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04279`, `unit_04100`
- **Chunk evidence:** —
- **Owns:** Owns living targets removing one damage condition per minute of rest from most severe downward; Healing/Regeneration accelerates; objects without Stamina need repair instead. — *chunk:* `unit_04279`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **HeroDeathVersusMinionLethality**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_04273`
- **Chunk evidence:** —
- **Owns:** Owns rare, staged PC death path versus simpler minion elimination on successful attack plus intent; slam damage immunity ranks referenced. — *chunk:* `unit_04273`
- **extends:** `Condition`
- **Properties:** —
- **Operations:** —

#### **OptionalInitiativeForTimedChallenge**

- **Evidence stage:** scaffolded
- **Foundational (concept):** True
- **Chunk ids:** `unit_03970`
- **Chunk evidence:** —
- **Owns:** Owns GM discretion to skip initiative when order is irrelevant, or roll initiative when timing matters (e.g. collapse after first round, hazards with initiative). — *chunk:* `unit_03970`
- **extends:** `Check`
- **Properties:** —
- **Operations:** —

### Story map

### Epic: Track combat state

**Full statement:** **Gamemaster** applies **Condition** changes; **Player** rolls **ResistanceCheck** when targeted. — *chunk:* `unit_00385`

- **Triggering actor:** Gamemaster
- **Responding actor:** Player
- **Confirming stories (scaffold):**
  1. Apply Condition
  2. Roll ResistanceCheck

### Evidence buckets (pair)

| Bucket | Chunk ids |
|--------|-----------|
| identified | `unit_00363_merged`, `unit_00385`, `unit_00387_merged`, `unit_00412`, `unit_00856`, `unit_00862`, `unit_01107`, `unit_01423_merged`, `unit_01979`, `unit_02252`, `unit_02604`, `unit_02878`, `unit_03324`, `unit_03341`, `unit_03943_merged`, `unit_03970`, `unit_03995`, `unit_04059`, `unit_04085`, `unit_04108`, `unit_04128_merged`, `unit_04147`, `unit_04273`, `unit_04279` |
| provisional | `unit_00401`, `unit_00420`, `unit_01997`, `unit_03913`, `unit_04074` |
| ambiguous | `unit_00835`, `unit_03976`, `unit_04128_merged` |

---
