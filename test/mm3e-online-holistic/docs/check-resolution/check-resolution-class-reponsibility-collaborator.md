---
state: domain-sketch
---

# Module: [Check Resolution]

_Object model for all Check Resolution terms. Concepts: Trait, Rank, Measurement, Check, Check Result, Condition. Subtypes: Graded Check Result, Opposed Check, Resistance Check, Routine Check, Team Check. Properties, instances, composites, and boundary terms modeled inline._

Scope: The d20 resolution mechanic (roll + modifier vs DC), checks (routine, opposed, resistance), degrees of success/failure, measurements and the Rank/Measure table, and conditions (basic and combined).

**Core terms**:
- d20
- check
- Difficulty Class (DC)
- opposed check
- resistance check
- routine check
- degree of success
- degree of failure
- modifier
- rank
- measure
- condition
- combined condition
- difficulty scale
- difficulty
- dazed
- stunned
- staggered
- incapacitated
- dying
- vulnerable
- defenseless
- impaired
- disabled
- weakened
- exhausted
- fatigued
- Gamemaster (GM)
- player character (PC)
- non-player character (NPC)

**Moved to other modules**:
- hero point → Combat
- extra effort → Combat
- power stunt → Combat
- reaction → Combat

---

All uncertain outcomes are resolved with one mechanic: roll d20, add all appropriate modifiers, compare against a Difficulty Class; meeting or exceeding the DC is success. Each check is tied to exactly one trait. Opposed, resistance, and routine checks are specializations — not different systems. Graded checks produce degrees based on the margin above or below the DC; a natural 20 always increases the degree of success by one.

---

# Core Domain

## **Trait**

A trait is the base abstraction for every quantifiable game characteristic a character possesses — abilities, skills, defenses, powers, and advantages are all traits. Trait owns the concept of rank: every trait has exactly one rank, a single numeric measure of its effectiveness, and that rank is the value that flows into checks as the modifier. Without a trait there is no rank, without a rank there is no modifier, and without a modifier there is no check. The Rank and Measure abstraction translates trait ranks into real-world values (mass, time, distance, volume), but it is the trait that carries the rank in the first place. Defenses (Dodge, Parry, Fortitude, Toughness, Will) are traits derived from abilities; they supply the DC or the modifier for resistance and attack checks. Other modules (Ability, Skill, Power, Advantage) define specific kinds of traits, but the abstract concept — a quantifiable characteristic with a rank — belongs here. Every trait is always referenced through a check ("Strength check," "Dodge resistance check"), making Trait the single point of connection between a character's capabilities and the resolution system.

### Ubiquitous Language

#### **Trait**
- A trait is any quantifiable game characteristic a character possesses — abilities, skills, advantages, powers, and defenses are all traits.
- Every trait has a rank; rank is the single numeric measure of a trait's effectiveness.
- A check is always a check *of* a trait — "Strength check," "Acrobatics check," "Dodge resistance check" — there is no check without a trait supplying the modifier.
- The Measurements Table translates trait ranks into real-world values (mass, time, distance, volume); traits are what have ranks, so measurements are a property of traits.
- Defenses (Dodge, Parry, Fortitude, Toughness, Will) are traits derived from abilities; they supply the DC or the modifier for resistance and attack checks.
- Other modules (Ability, Skill, Power, Advantage) define *specific* traits; the abstract concept of what a trait is — a quantifiable characteristic with a rank — belongs here.

#### **Rank**
- Every quantifiable trait has a rank — the single numeric value measuring that trait's effectiveness.
- Ranks can be negative; each lower rank halves the previous measurement.
- Ranks must not be added directly; convert to measures, add the measures, then convert back to a rank.

#### **Measurement** 
- The Measurements Table maps each rank to mass, time, distance, and volume on a roughly doubling scale.
- Distance Rank = Time Rank + Speed Rank; Time Rank = Distance Rank − Speed Rank; Throwing Distance Rank = Strength Rank − Mass Rank.
- Measurements are approximate, especially at higher ranks — guidelines, not precise values.

### Domain Sketch

#### **Trait**
- is a *quantifiable characteristic* of a *character*
- has exactly one *rank* — the single numeric value measuring its effectiveness
- makes a *check*, its *rank* as the primary  *modifier*
- has a *difficulty ladder* — either a trait-specific one (e.g. *Athletics*, *Vehicles*) or the default ladder when no specific one exists
- *abilities*, *defenses*, *skills*, *powers*, and *advantages* are all *traits* — each is a subtype owned by its own module

#### **Rank**:
- is a single numeric value carried by a *trait* — the measure of that *trait's* effectiveness
- can be negative; each lower *rank* halves the previous *measurement* value
- feeds into *Measurement* for conversion to real-world values (*mass*, *time*, *distance*, *volume*)
- follows a roughly doubling scale — each *rank* increase approximately doubles the *measurement* value
- **Invariant:** *ranks* must never be added directly; convert to *measures*, perform arithmetic on the *measures*, then convert back to a *rank*

#### **Measurement**
- translates a *rank* into a real-world value across four dimensions: *mass*, *time*, *distance*, and *volume*
- determines *throwing distance* by subtracting the *object's mass rank* from the *thrower's strength rank* and looking up the result as a *distance* value
- determines *travel distance* by adding *time rank* and *speed rank* and looking up the result as a *distance* value
- determines *travel time* by subtracting *speed rank* from *distance rank* and looking up the result as a *time* value
- resolves combined quantities by converting *ranks* to *measures*, performing the arithmetic on the *measures*, then converting back to a *rank*
- values at higher *ranks* are approximate — guidelines for play, not precise calculations

### Class Responsibility Collaborator

#### **Trait**
belong to character         | Character
effectiveness rank          | Rank
difficulty ladder           | Difficulty Ladder
                            |   invariant: every trait has a ladder — trait-specific or the default
makes check                 | Check
                            |   invariant: modifier = rank value

#### **Rank**
numeric value               | Number
                            |   invariant: may be negative; each lower rank halves the measurement value
translate to measure        | Measurement, Measurement Type
                            |   invariant: each rank increase approximately doubles the measurement value
add                         | Rank, Measurement, Measurement Type
                            |   invariant: ranks must not be added directly — convert to measures first


#### **Measurement Type**   | [ throwing distance, travel distance, travel time, lifting ]

#### **Ranked Measurements**
type                        | Measurement Type
units                       | mass, distance, volume, time
rank measured               | Rank
value                       | Number

#### **Measurement**
ranked measurements         | Ranked Measurement
                            |   invariant: one real-world value for every rank for this measurement type
calculate                   | Rank, Rank, Measurement Type
                            |   invariant: look up value for operator rank and scale rank from the type's table
                            |   invariant: each rank step approximately doubles the real-world value
---

## **Check**

A check is the core resolution mechanic — the single mechanism through which any uncertain outcome in the game is determined. It binds together a d20 roll, a trait-derived modifier, and a Difficulty Class into one comparison: roll plus modifier versus DC, with success on a match or exceed. The check owns this formula and is the single source of truth for whether an action succeeds or fails; no other abstraction may duplicate this determination. Three specialized forms exist within its boundary: opposed checks (two characters' results compared directly), resistance checks (defense bonus versus an effect's DC, typically 10 + effect rank), and routine checks (a fixed result of 10 replacing the die, used when circumstances are not demanding). Trait supplies the modifier, and the GM controls which DCs, circumstance modifiers, and routine allowances apply. Every check references exactly one trait — "Strength check," "Dodge resistance check" — and without a trait there is no check.

A check must always produce a binary success/failure result. When graded, it yields a degree that the Degree abstraction interprets. A natural 20 is always a critical success (degree increased by one). Circumstance modifiers (±2 minor, ±5 major) and team checks (helpers rolling against DC 10 to grant bonuses) layer onto the base formula but never change its fundamental shape. The invariant: d20 + modifier vs DC, every time, no exceptions.

### Ubiquitous Language

#### **check**
- A check is d20 + trait rank (plus any additional modifiers) vs a Difficulty Class (DC); equaling or exceeding the DC is success, below is failure.
- Whenever a character attempts something where the outcome is in doubt, it requires a check of an appropriate trait — ability, skill, power, etc.
- Additional modifiers come from circumstances, advantages, or power effects layered on top of the trait rank.
- A natural 20 on a check is a critical success: determine the degree normally, then increase it by one degree; this can turn a failure into a success.

#### **d20**
- The game uses a single twenty-sided die (d20) to resolve actions.
- "d20+2" means roll the die and add two; "d20−4" means roll and subtract four.
- The die can also express percentages in increments of 5% (multiply the face value by 5).

#### **modifier**
- A modifier is a number added to or subtracted from a d20 roll before comparing to the DC.
- The primary modifier comes from the trait's rank; additional modifiers come from circumstances, advantages, or power effects.
- A minor circumstance modifier is ±2; a major circumstance modifier is ±5.
- Missing required tools imposes a −5 penalty; makeshift tools reduce this to −2.
- Circumstance modifiers apply to the check result (not the DC) for consistency.

#### **opposed check**
- An opposed check pits two characters' check results against each other; the higher result wins.
- On a tie, the character with the higher bonus wins; if bonuses are also equal, roll d20 — 1–10 one character wins, 11–20 the other.
- Routine opposition sets the DC as the opposing character's modifier + 10 (used when the opponent is not actively opposing).
- A comparison check compares ranks directly without rolling; the higher rank wins (no luck involved).

#### **resistance check**
- A resistance check is d20 + defense bonus vs the hazard's DC (typically 10 + effect rank).
- Resistance checks may be graded, with different outcomes at different degrees of success or failure.

#### **is routine (property on Check)**
- when true, d20 is fixed at 10; all other modifiers apply as normal
- a character with a +10 bonus achieves 20, succeeding at DC 20 tasks without rolling
- if the routine total fails, the player may still roll — the task is just not routine for that character
- the GM decides when conditions allow; some traits widen that scope

#### **degree of success / degree of failure**
- A graded check counts each 5 full points above the DC as one additional degree of success; a bare success is one degree.
- Degrees of success range up to four (DC + 15 or higher). A natural 20 (critical success) increases the degree of success by one.
- A graded check counts each 5 full points below the DC as one additional degree of failure; a bare failure is one degree.
- Degrees of failure range down to four (DC − 20 or lower), though more than two degrees of failure rarely matter in practice.
- Specific types of graded checks — notably resistance checks — give defined results for each degree of failure.

#### **Gamemaster (GM) / player character (PC) / non-player character (NPC)**
- The GM creates adventures, portrays villains and supporting characters, describes the world, and decides the outcome of actions based on die rolls and rules. The GM sets the DC for checks based on circumstances. The GM decides when a routine check is allowed and how many characters can help in a team check.
- A player controls a superhero they have created; they interact with other PCs and with the world and stories created by the GM. Players declare extra effort, spend hero points, and choose which actions their heroes take each turn.
- NPCs include villains, supporting cast, thugs, cops — any character controlled by the GM rather than a player. Active defenses in combat against NPCs are generally routine opposition (DC 10 + defense).

---

### Domain Sketch

#### **Check**
- is made *using* the *trait* of a *character*
- is made *against* a *difficulty class* set by the *GM* or passing a selected *difficulty stage* from *difficulty ladder*
- may have a *circumstance modifier* applied to the check *result* (±2 minor, ±5 major)
- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*, producing a *check result*
- **Invariant:** shape is always *roll total* versus *difficulty class*; subtypes only vary how *total* or *DC* is produced

#### **D20**
- is rolled by a *check* to produce the base numeric result
- owns the *roll* function — the act of generating a random value in [1, 20]

#### **Check Result**
- is produced by a *check* — the outcome of comparing *roll total* to *difficulty class*
- is either *success* (*roll total* meets or exceeds *difficulty class*) or *failure* (below)
- carries the *margin* — how far above or below the *difficulty class* the *roll total* fell
- carries *degrees of success* or *degrees of failure* when graded — each full five points of margin adds one degree
- a *natural 20* can turn *failure* into *success* and adds one degree of success

#### **Graded Check Result**
- adds *degrees of success* and *degrees of failure* based on the *margin*
- each full *five points* of *margin* above *difficulty class* adds a *degree of success*; each full *five points* below adds a *degree of failure*
- a *natural 20* increases the *degree of success* by one after normal calculation (*critical success*)
- on a *resistance check*, each *degree of failure* maps to a specific *condition* imposed on the *character*

#### **Difficulty Ladder**
- is a ranked set of named *difficulty stages* linked to a *trait*
- supplies the *GM* with calibrated *difficulty classes* drawn from named *difficulty stages* rather than an arbitrary numeric DC
- provides a default ladder (Very Easy DC 0 through Nigh-impossible DC 40) when no *trait*-specific ladder exists
- trait-specific ladders (e.g. *Vehicles Difficulties*) reuse the same *stage descriptor* names but supply *task descriptions* scoped to the *trait*
- the *GM* may select a *difficulty stage* from the ladder and pass its *DC value* directly to a *check*

#### **Difficulty Stage**
- is a single named entry within a *difficulty ladder*
- carries a *stage descriptor* (e.g. Easy, Challenging, Heroic), a *DC value* (in steps of 5 from 0 to 40), and a *task description* for the linked *trait*
- the *stage descriptor* is the domain name — "Challenging" or "Formidable" — not a row number or index
- supplies its *DC value* to a *check* when the GM selects this stage rather than setting a numeric DC directly

#### **Opposed check**
- is made against an *opposing character's* *check result* as the *difficulty class*
- is rolled by both the *active character* and the *opposing character*; the *higher result* wins
- on a *tie*, the *higher bonus* wins; if *bonuses* also tie, a *tie-break d20* decides (1–10 vs 11–20)
- *passive opposition* sets *difficulty class* to *opposing trait modifier + 10* when the *opponent* is not *actively contesting*
- a *comparison check* skips the *d20* and compares *ranks* directly — higher *rank* wins; no luck involved

#### **Resistance check**
- uses a *defense bonus* (from a *defense trait*) as its *modifier*
- *difficulty class* is typically *10 + effect rank* from the *effect* being resisted
- produces a *graded check result*
- each *degree of failure* in the *result* maps to a specific *condition* imposed on the *character*

#### **is routine (property on Check)**
- when *true*, *d20* is fixed at *10*; all other *modifiers* still apply
- if *10 + modifiers* meets or exceeds the *difficulty class*, the *character* succeeds without *rolling*
- if the *routine total* is insufficient, the *player* may still *roll* — the task is by definition not *routine* for that *character*
- some *traits* widen what counts as *routine* for a given *character*

#### **Team Check**
- has a *leader* who *rolls* the primary *check* normally
- has one or more *helpers* who each *roll* the same *trait* versus a fixed *difficulty class* of *10*
- each *helper success* grants the *leader* a +2 *circumstance modifier*; three or more *helper successes* grant +5
- *helper failure* may impose a −2 *circumstance modifier* on the *leader's* *check*
- the *leader's* *check result* determines the outcome — *helpers* only modify it

---

### Class Responsibility Collaborator

#### **Check**
use trait            | Trait
use difficulty class | Difficulty Class, Difficulty Stage
apply circumstance   | Circumstance Modifier
is routine           | (boolean — GM-decided; when true d20 is fixed at 10; player may still roll if routine total fails)
resolve             | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result
                                | invariant: d20 + trait rank + circumstance modifier >= difficulty class

#### **Opposed Check**
use opposing trait   | Trait
resolve             | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result
                                | invariant: both characters resolve as standard Checks; higher result wins
                                | invariant: tie → higher bonus wins; bonus tie → d20 (1–10 vs 11–20)
                                | invariant: passive opposition DC = opposing modifier + 10
                                | invariant: rank vs rank — no d20 roll; higher rank wins directly

#### **Team Check**
use helper traits     | Trait
resolve              | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result
                                 | invariant: leader resolves as a standard Check
resolve helper       | D20, Trait, Check Result
                                 | invariant: each helper rolls same Trait vs DC 10
apply helper outcome | Circumstance Modifier
                                 | invariant: 1 success → +2; 3+ successes → +5; cap +5
                                 | invariant: 2+ failures → −2; cap −2


#### **D20**
roll                | Check
                                | invariant: result in [1, 20]

#### **Difficulty Ladder**
stages               | Difficulty Stage
link to trait        | Trait
                                | invariant: every trait has a ladder — trait-specific or default (Very Easy DC 0 to Nigh-impossible DC 40)
supply dc to check  | Difficulty Stage, Check

#### **Difficulty Stage**
descriptor           | (stage name e.g. Challenging, Formidable)
dc value             | Difficulty Class
task description     | Trait
supply dc           | Check

---

### Decisions made

#### **Check**
- *Check* alone owns *success/failure* for uncertain outcomes; nothing else reimplements *roll total* versus *difficulty class*.
- *Check result* is a concept, not a property of *Check* — it carries its own responsibilities (success/failure, margin, grading, degree mapping to conditions).
- *Degree of success* and *degree of failure* are properties of a *graded check result*, not standalone concepts.

#### **Resistance Check**
- A *Resistance Check* always produces a *graded check result* — simple pass/fail is insufficient because conditions are imposed per degree of failure.
- Its DC is always derived from the resisted *Power Effect's* effectiveness rank + 10; a difficulty ladder or GM-set DC is never applicable.
- *Comparison check* (rank vs rank, no roll) stays a special case inside *opposed check*, not a second engine.
- *d20* is the instrument a *check* rolls — a property, not a separate concept.
- *Modifier* is a value slot on a *check* (primary from *trait rank*, plus stacked *circumstance modifiers*) — a property, not a concept.
- *Gamemaster*, *player character*, *non-player character* are user/actor roles, not domain objects in this module.

#### **Difficulty Ladder**
-  is a concept, not a property of *Trait* or *DC* — it owns its own structure (a ranked set of *difficulty stages*) and its own responsibility (providing calibrated named DCs for a specific trait).
- The general Difficulty Classes ladder (DC 0–40) is the default instance; trait-specific ladders share the same stage structure but supply different task descriptions.

#### **Difficulty Stage** 
- is a concept within a *Difficulty Ladder* — each stage carries its own descriptor, DC, and task description; it is not a generic "row" or "entry."

---

### References

#### **check**
**Ref: Ch1 The Basics**
Source: context/rules/HeroesHandbook-rules__chunk_005.md
Locator: lines 244–284
Extract: whole

**Ref: Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

**Ref: The Die**
Source: context/rules/HeroesHandbook-rules__chunk_004.md
Locator: lines 202–243
Extract: whole

**Ref: Check Examples**
Source: context/rules/HeroesHandbook-rules__chunk_011.md
Locator: lines 931–990
Extract: whole

**Ref: Circumstances And Difficulty**
Source: context/rules/HeroesHandbook-rules__chunk_015.md
Locator: lines 1147–1194
Extract: whole

**Ref: The Gamemaster**
Source: context/rules/HeroesHandbook-rules__chunk_006.md
Locator: lines 285–335
Extract: whole

#### **Check Result**
**Ref: Degrees Of Success And Failure**
Source: context/rules/HeroesHandbook-rules__chunk_013.md
Locator: lines 1038–1101
Extract: whole

**Ref: Critical Success**
Source: context/rules/HeroesHandbook-rules__chunk_010.md
Locator: lines 875–930
Extract: whole

#### **Difficulty Ladder / Difficulty Stage**
**Ref: Difficulty Classes**
Source: context/rules/HeroesHandbook-rules__chunk_010.md
Locator: lines 875–930
Extract: Difficulty Classes ladder (Very Easy DC 0 through Nigh-impossible DC 40 with example tasks)

**Ref: Assigning Difficulties**
Source: context/rules/HeroesHandbook-rules__chunk_217.md
Locator: lines 15152–15227
Extract: Difficulty Class Examples table with same stage descriptors and DC values from GM chapter

#### **modifier**
**Ref: Circumstances And Difficulty**
Source: context/rules/HeroesHandbook-rules__chunk_015.md
Locator: lines 1147–1194
Extract: whole

#### **opposed check**
**Ref: Opposed Check Examples**
Source: context/rules/HeroesHandbook-rules__chunk_012.md
Locator: lines 991–1037
Extract: whole

**Ref: Opposed Checks**
Source: context/rules/HeroesHandbook-rules__chunk_014.md
Locator: lines 1102–1146
Extract: whole

#### **resistance check**
**Ref: Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole

#### **is routine (property on Check)**
**Ref: Check Examples**
Source: context/rules/HeroesHandbook-rules__chunk_011.md
Locator: lines 931–990
Extract: whole

#### **Team Check**
**Ref: Circumstances And Difficulty**
Source: context/rules/HeroesHandbook-rules__chunk_015.md
Locator: lines 1147–1194
Extract: whole

---

## **Condition**

Condition is the status-effect system that translates mechanical outcomes — failed resistance checks, fatigue from extra effort, environmental hazards — into named states that impose concrete modifiers on a character. Each condition tracks its *condition source* (the power, effect, attacker, or event that imposed it) and carries an active or inactive status; only active conditions apply their modifiers. Basic conditions impose a single modifier (dazed limits actions, impaired applies −2, vulnerable halves defenses); combined conditions bundle multiple basics under one name (staggered = dazed + hindered, incapacitated = defenseless + stunned + unaware), and individual constituents can be resolved or superseded independently. Condition owns the supersession hierarchy (dazed → stunned, impaired → disabled → debilitated, vulnerable → defenseless, hindered → immobile) and three distinct supersession rules: when a source imposes a more severe condition than one it already imposed, the lesser is removed; when a source would impose a lesser condition it already surpassed, nothing happens; when a lesser condition arrives from a different source while a more severe one is already active, the lesser is parked as inactive and becomes active once the blocking condition is gone. Condition interacts with Check by consuming degrees of failure from resistance checks, with Hero Point which can directly remove specific conditions via Recover, and with Extra Effort whose fatigue cost imposes conditions on the fatigued → exhausted → incapacitated escalation track. When multiple active conditions apply, all effects stack.

### Ubiquitous Language

#### **Condition**
- A condition is a named state imposed on a character by effects, injuries, or fatigue — shorthand for a set of game modifiers.
- If multiple conditions apply, use all of their effects; some conditions supersede lesser ones.
- Each basic condition describes a single game modifier; they are the building blocks of the condition system.

#### **Condition Source**
- The condition source is the power effect, attacker, or event/situation that imposed a condition on a character.
- Used to distinguish same-source from different-source supersession.

#### **Basic Condition**
- A basic condition imposes a single modifier or restriction on a character.

#### **Combined Condition**
- A combined condition bundles multiple basic conditions under one name; individual constituents can be resolved or superseded independently.

---

### Domain Sketch

#### **Condition**
- is applied to a *character*; the *source* does the imposing — the condition is what the character carries and enforces
- is created from a *condition source* 
- is *active* or *inactive*, and enforces *penalties* and *restrictions* only when *active*
- *penalizes* a suffering *character* according to a *game modifier* (eg *impaired* applies −2, *vulnerable* halves defenses)
- may also *restrict* a suffering *character* (e.g. *dazed* limits actions)

- *supersedes* a less severe *condition* from the same source — removing the lesser
- is *superseded by* a more severe *condition* that overrides it
- is *inactive* when imposed while a more severe *condition* from a *different source* is already active; becomes *active* once the blocking condition is removed
- is removed when its *condition source* ends
- **Invariant:** only *active* conditions apply modifiers; same-source supersession removes the lesser; different-source supersession parks it as *inactive*

Examples:
- *dazed* — limited to *free actions* and one *standard action* per turn; superseded by *stunned*
- *stunned* — cannot take any *actions*, including *free actions*; supersedes *dazed*
- *vulnerable* — *active defenses* halved (round up); superseded by *defenseless*
- *defenseless* — *active defense bonuses* become 0; attackers may use *routine checks*; forgoing routine makes any hit a *critical hit*; supersedes *vulnerable*
- *impaired* — −2 *circumstance penalty* on *checks* (may be scoped to a *trait*); superseded by *disabled*
- *disabled* — −5 *circumstance penalty* on *checks* (may be scoped); superseded by *debilitated*
- *weakened* — temporary *power point* loss in a *trait*; superseded by *debilitated*
- *debilitated* — one or more *abilities* lowered below −5
- *hindered* — half normal *speed* (−1 *speed rank*); superseded by *immobile*
- *immobile* — no *movement speed*; still capable of *actions* unless another *condition* prevents it
- *compelled* — limited to *free actions* and one *standard action* chosen by the *controller*; superseded by *controlled*
- *controlled* — all *actions* each turn dictated by another *character*
- *fatigued* — *hindered*; recovers after one hour of rest
- *normal* — unharmed, unaffected, acting normally
- *transformed* — some or all *traits* altered by an outside agency; *power point total* cannot increase
- *unaware* — completely unaware of surroundings; cannot make *interaction* or *Perception checks* (may be scoped to specific senses)

#### **Condition Source**
- is the *power effect* and *attacker*, or *event/situation* that imposed a *condition*
- is recorded when the *condition* is applied; used to distinguish same-source from different-source *supersession*
- is data owned by the *condition* — it has no lifecycle of its own
- **Invariant:** two conditions sharing the same source follow same-source supersession rules; conditions from different sources follow different-source rules


#### **Combined Condition**
- combines multiple *basic conditions* under one name ( eg *staggered* ) as shorthand for a set that goes together
- resolves each *basic condition* making it up independently — an effect that removes one leaves the others in place
- supersedes each *basic condition* making it up independently — a more severe condition replaces only its matching *basic condition*, leaving the rest unchanged
- removes all *basic conditions* making it up simultaneously when its *condition source* ends — a successful resistance check or negating effect clears the whole combined condition at once

*Examples:*
- *staggered* = *dazed* + *hindered*
- *incapacitated* = *defenseless* + *stunned* + *unaware*; generally fall *prone*
- *dying* = *incapacitated* + near death; *Fortitude* DC 15 each round — two *degrees of success* stabilizes, three total *degrees of failure* means death
- *exhausted* = *impaired* + *hindered*; recovers after one hour of comfortable rest
- *asleep* = *defenseless* + *stunned* + *unaware*; hearing *Perception check* (3+ *degrees of success*) or shaking wakes the *character*
- *blind* = *hindered* + visually *unaware* + *vulnerable*; may also be *impaired* or *disabled* for vision-dependent activities
- *bound* = *defenseless* + *immobile* + *impaired*
- *deaf* — auditory concealment from the *character*; may allow surprise attacks
- *entranced* = *stunned*; any obvious *threat* breaks the trance; an ally can free with *interaction skill check* (DC 10 + *effect rank*)
- *paralyzed* = *defenseless* + *immobile* + physically *stunned*; still aware; can take purely mental *actions*
- *prone* — −5 *close attack penalty*; opponents get +5 *close* / −5 *ranged attack modifier*; *hindered*; standing up is a *move action*
- *restrained* = *hindered* + *vulnerable*; if anchored to an *immobile* object, *immobile* instead of *hindered*
- *surprised* = *stunned* + *vulnerable*

---


### Class Responsibility Collaborator

#### **Condition**
label                      | (name of the condition, e.g. *dazed*, *stunned*)
game modifier              | (penalty value or restriction description)
supersedes                 | Condition
superseded by              | Condition

#### **Imposed Condition**
imposing source            | Condition Source
condition type             | Condition
active status              | (active or inactive)
suppressing condition      | Imposed Condition
                           |   invariant: set when parked inactive by a different-source more-severe condition

#### **Imposed Conditions**
applied conditions         | Imposed Condition
apply new condition        | Condition Source, Condition, Imposed Condition
                           |   invariant: same-source more-severe — remove lesser imposed condition
                           |   invariant: same-source less-severe — do nothing
                           |   invariant: different-source more-severe — park lesser as inactive, set suppressing condition

#### **Condition Source**
Effect                     | Power Effect
Other                      | String
                           |  invariant :source be either a power effect or any named string to identify some kind of event 
                           |  or condition


#### **Ongoing Effects**
active effects             | Power Effect
add                        | Power Effect
resist                     | Power Effect, Check
                           |   invariant: resistance check made at end of each of the character's turns while effect is active
end effect                 | Power Effect, Imposed Conditions
                           |   invariant: clears only the conditions that this effect imposed
---
### Decisions made

#### **Condition**
- Each named *condition* (*dazed*, *stunned*, *impaired*, etc.) is an **instance** of *Condition*, not a subtype — they differ by data (which modifiers, which restrictions) but share the same lifecycle: applied, stacked, superseded, resolved.
- *Combined conditions* are **composites** — each names a bundle of *basic condition* instances, not a separate concept with its own behavior.
- *Condition* is imposed as a *result* of a *check* (typically via *degrees of failure* on a *resistance check*); the chain from check to condition is a cross-concept relationship, not duplicated resolution logic.
- Each *Condition* instance owns *supersedes* and *superseded_by* as properties — the *supersession chain* is navigable through condition data itself, not via a separate runtime object.

#### **Condition Source**
- *Condition Source* is a **value** on the *Condition* instance, not a separate runtime object — it is the identity token (name, reference, or descriptor) of whatever caused the condition to be imposed.

---

### References

#### **Condition**
**Ref: Reactions**
Source: context/rules/HeroesHandbook-rules__chunk_017.md
Locator: lines 1238–1344
Extract: whole

**Ref: Combined Conditions**
Source: context/rules/HeroesHandbook-rules__chunk_018.md
Locator: lines 1345–1425
Extract: whole

#### **Condition Source**
**Ref: Combined Conditions**
Source: context/rules/HeroesHandbook-rules__chunk_018.md
Locator: lines 1345–1425
Extract: whole

---

# Boundary Domain

### Ubiquitous Language

#### **Power Effect** *(owned by: Power)*
- An effect is the basic building block of a power; it describes what a power does in game terms.
- Resistance check DC is typically 10 + effect rank — the effect's rank is what the character resists against.
- Conditions are imposed by effects (as well as by injuries, fatigue, and environmental hazards).
- Some effects are ongoing — they must be resisted multiple times, not just once.

#### **Character** *(owned by: Character Construction)*
- A character is the entity that possesses traits, makes checks, and has conditions applied to it.
- Every rule in this module acts on or through a character — there is no check without a character making it.
- A character tracks *ongoing effects* separately from *imposed conditions* — an ongoing effect may be the source of some conditions, but conditions can also arrive from fatigue, environment, or direct application with no associated ongoing effect.

#### **Power Points** *(owned by: Character Construction)*
- A character's power point total is referenced by conditions: Transformed cannot increase it; Weakened temporarily removes power points from a trait.

#### **Game Modifier** *(owned by: consuming module)*
- Conditions define modifiers (action restrictions, check penalties, defense reductions); enforcement is owned by the consuming module.

#### **Action Round Structure** *(owned by: Combat)*
- Defines standard/move/free actions and turn order that conditions restrict.
- A round is 6 seconds; each character gets one turn per round.

---

### Domain Sketch

#### **Power Effect**
- has a *rank* that determines the *resistance check* DC (DC = rank + 10)
- may impose one or more *conditions* on a *character* based on the type of effect and the *degree of failure* on the resistance check
- may be **ongoing** for a target *character*: requires a *resistance check* at the end of each of the target's turns until ended
- when ongoing and the *resistance check* succeeds: the effect ends and all *conditions* it imposed on the *character* are removed
- when ongoing and the *resistance check* fails: the effect persists; all conditions it imposed remain; further conditions may be added per the effect's description
- **Invariant:** an ongoing effect is either active or ended; when ended, all conditions it imposed — whether *active* or *inactive* — are removed from the *character*

#### **Character**
- makes *checks* using its *traits*
- carries *imposed conditions* via its *Imposed Conditions* collection
- carries *ongoing effects* via its *Ongoing Effects* collection — separate from conditions; an ongoing effect tracks which conditions it caused so it can clear them when it ends

#### **Power Points**
- referenced by *conditions* — *Transformed* prevents the total from increasing; *Weakened* temporarily reduces power points in a *trait*

#### **Game Modifier**
- carries a *penalty value* or *restriction description* enforced by a consuming module

#### **Action Round Structure**
- defines the *action types* (*standard*, *move*, *free*) that *conditions* may restrict

---

### Class Responsibility Collaborator

#### **Power Effect** *(is a type of Trait)*
resistance trait           | Trait
ongoing Targets            |  Character,
make resistance            |
check for ongoing targets  | Character, Check
condition on failure       | Condition, Degree of Failure
                           |   invariant: which conditions are imposed is defined by the effect type — owned by Power module
end                        | Imposed Conditions
                           |   invariant: on end — all conditions imposed by this effect, active or inactive, are removed


#### **Character**
traits                     | Trait
imposed conditions         | Imposed Conditions
ongoing effects            | Ongoing Effects

---

### Decisions made

- The "ongoing" quality is a property of an effect, not a separate concept. Whether an effect requires repeated resistance checks is determined by the Power module (the effect's definition), not by this module.
- This module is responsible only for the check-resolution behavior when an ongoing effect is in play: what happens on success (ends + conditions cleared) and failure (persists + conditions remain).
- **Out of scope (Power module):** How a power effect selects which conditions to impose — the mapping from effect type and degree of failure to specific conditions — is not modeled here. This module only knows that `condition on failure` is triggered; the Power module owns the condition-selection rules.
- A resistance check is not a distinct subtype — it is a plain *Check* where the *Power Effect* supplies the DC (effect rank + 10) and the target uses their defense *trait*. No separate concept is needed; the combat context that determines who makes it belongs to the Combat module.

### References

**Ref: Resistance and Ongoing Effects**
Source: context/rules/HeroesHandbook-rules__chunk_209.md
Locator: lines 14791–14830
Extract: whole

**Ref: Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole

**Ref: The Gamemaster**
Source: context/rules/HeroesHandbook-rules__chunk_006.md
Locator: lines 285–335
Extract: whole

**Ref: Reactions**
Source: context/rules/HeroesHandbook-rules__chunk_017.md
Locator: lines 1238–1344
Extract: whole
