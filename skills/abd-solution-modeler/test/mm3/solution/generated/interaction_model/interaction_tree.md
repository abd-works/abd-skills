# Epic: Build Character (Player creates **Character** within **Power Level** limits)

- Triggering-Actor: **Player**
- Responding-Actor: **Gamemaster**
- Pre-Condition: none
- Failure-Modes:
  - **Power Level** cap exceeded
  - **Power Point** budget exceeded
- Domain Concepts: **Character**, **Ability**, **Skill**, **Advantage**, **Power Level**, **Power Point**, **Complication**, **Hero Archetype**

## Sub-Epic: Allocate Abilities and Skills

- Triggering-Actor: [Player]
- Responding-Actor: [Gamemaster]
- Pre-Condition: [none]
- Domain Concepts: **Ability**, **Skill**, **Power Level**

### Story: Assign Ability Ranks (Player allocates **Ability** ranks within **Power Level** cap)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: allocates ranks to **Ability** traits
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms ranks stay within **Power Level** limits
- Pre-Condition: [none]
- Failure-Modes:
  - **Ability** rank exceeds **Power Level** cap
- Domain Concepts: **Ability**, **Power Level**

### Story: Assign Skill Ranks (Player allocates **Skill** ranks keyed to **Ability**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: allocates ranks to **Skill** traits
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms **Skill** is keyed to correct **Ability**
- Pre-Condition: [none]
- Failure-Modes:
  - **Skill** rank exceeds **Power Level** cap
- Domain Concepts: **Skill**, **Ability**, **Power Level**

### Story: Select Advantages (Player chooses **Advantage** traits for **Character**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: selects **Advantage** traits
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms **Advantage** eligibility and cost
- Pre-Condition: [none]
- Failure-Modes:
  - **Power Point** budget exceeded
- Domain Concepts: **Advantage**, **Character**, **Power Point**

### Story: Define Complications (Player defines **Complication** hooks for **Character**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: defines **Complication** that can grant **Hero Point**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: approves **Complication** for play
- Pre-Condition: [none]
- Failure-Modes:
  - **Complication** too narrow to trigger
- Domain Concepts: **Complication**, **Character**, **Hero Point**

---

## Sub-Epic: Build Powers

- Triggering-Actor: [Player]
- Responding-Actor: [Gamemaster]
- Pre-Condition: [none]
- Domain Concepts: **Power**, **Effect**, **Modifier**, **Descriptor**

### Story: Create Power from Effects (Player builds **Power** from **Effect** and **Modifier**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: selects **Effect** type, applies **Extra** and **Flaw**, adds **Descriptor**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms **Power** cost and legality
- Pre-Condition: [none]
- Failure-Modes:
  - **Power Point** budget exceeded
  - **Effect** rank exceeds **Power Level** cap
- Domain Concepts: **Power**, **Effect**, **Modifier**, **Extra**, **Flaw**, **Descriptor**, **Power Point**

### Story: Build Power Array (Player groups alternate **Effect** in **Power Array**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: defines **Power Array** with alternate **Effect** options
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms **Power Array** cost and switching rules
- Pre-Condition: [none]
- Failure-Modes:
  - **Power Array** cost miscalculated
- Domain Concepts: **Power Array**, **Power**, **Effect**

### Story: Create Device (Player builds **Device** as removable **Power**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: defines **Device** with **Effect** and **Equipment** traits
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: confirms **Device** cost and removal rules
- Pre-Condition: [none]
- Failure-Modes:
  - **Device** cost miscalculated
- Domain Concepts: **Device**, **Power**, **Equipment**

---

# Epic: Resolve Combat (Participants act in **Action Round** using **Attack** and **Defense**)

- Triggering-Actor: **Player** or **Gamemaster**
- Responding-Actor: **Gamemaster** or **Player**
- Pre-Condition: conflict initiated
- Failure-Modes:
  - **Initiative** ties unresolved
- Domain Concepts: **Action Round**, **Initiative**, **Action**, **Attack**, **Defense**, **Dodge**, **Parry**, **Toughness**

## Sub-Epic: Establish Turn Order

- Triggering-Actor: [Player or Gamemaster]
- Responding-Actor: [Gamemaster or Player]
- Pre-Condition: [conflict initiated]
- Domain Concepts: **Initiative**, **Action Round**, **Ability**

### Story: Roll Initiative (Participant rolls **Check** for **Initiative** order)

- Trigger:
  - Triggering-Actor: **Player** or **Gamemaster**
  - Behavior: rolls **Check** (d20 + **Ability** modifier) for **Initiative**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: establishes **Action Round** turn order
- Pre-Condition: conflict initiated
- Failure-Modes:
  - **Initiative** ties require tiebreaker
- Domain Concepts: **Initiative**, **Check**, **Ability**, **Action Round**

---

## Sub-Epic: Execute Attacks and Defenses

- Triggering-Actor: [Player or Gamemaster]
- Responding-Actor: [Gamemaster or Player]
- Pre-Condition: [turn in **Action Round**]
- Domain Concepts: **Attack**, **Defense**, **Dodge**, **Parry**, **Toughness**

### Story: Make Attack Check (Attacker rolls **Attack** vs target **Dodge** or **Parry**)

- Trigger:
  - Triggering-Actor: **Player** or **Gamemaster**
  - Behavior: rolls **Attack** **Check** vs target **Defense**
- Response:
  - Responding-Actor: **Gamemaster** or **Player**
  - Behavior: compares **Attack** result to **Dodge** or **Parry**
- Pre-Condition: attacker has **Action** available
- Failure-Modes:
  - **Attack** misses **Defense**
- Domain Concepts: **Attack**, **Defense**, **Dodge**, **Parry**, **Check**

### Story: Resist Damage (Target rolls **Toughness** vs **Attack Effect** rank)

- Trigger:
  - Triggering-Actor: **Gamemaster**
  - Behavior: applies **Attack Effect** hit to target
- Response:
  - Responding-Actor: **Player** or **Gamemaster**
  - Behavior: rolls **Resistance** **Check** (Toughness) vs **Attack Effect** rank
- Pre-Condition: **Attack** hit target
- Failure-Modes:
  - **Toughness** fails by degree; **Condition** applied
- Domain Concepts: **Toughness**, **Resistance**, **Attack Effect**, **Condition**, **Check**

### Story: Resist Affliction (Target rolls **Fortitude**, **Will**, or **Reflex** vs **Affliction Effect** rank)

- Trigger:
  - Triggering-Actor: **Gamemaster**
  - Behavior: applies **Affliction Effect** hit to target
- Response:
  - Responding-Actor: **Player** or **Gamemaster**
  - Behavior: rolls **Resistance** **Check** (Fortitude/Will/Reflex) vs **Affliction Effect** rank
- Pre-Condition: **Attack** hit target with **Affliction Effect**
- Failure-Modes:
  - **Resistance** fails by degree; **Condition** severity increases
- Domain Concepts: **Affliction Effect**, **Resistance**, **Fortitude**, **Will**, **Reflex**, **Condition**, **Check**

### Story: Apply Maneuver (Participant uses **Maneuver** that applies **Advantage** rules)

- Trigger:
  - Triggering-Actor: **Player** or **Gamemaster**
  - Behavior: declares **Maneuver** (e.g. Accurate Attack, Feint)
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: adjudicates **Maneuver** modifiers to **Attack** or **Defense**
- Pre-Condition: participant has **Action** available
- Failure-Modes:
  - **Maneuver** invalid for situation
- Domain Concepts: **Maneuver**, **Advantage**, **Attack**, **Defense**, **Action**

---

# Epic: Spend Hero Points (Player spends **Hero Point** for reroll or **Extra Effort**)

- Triggering-Actor: **Player**
- Responding-Actor: **Gamemaster**
- Pre-Condition: **Player** has **Hero Point**
- Failure-Modes:
  - **Hero Point** budget exhausted
- Domain Concepts: **Hero Point**, **Extra Effort**, **Complication**

### Story: Reroll Check (Player spends **Hero Point** to reroll **Check**)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: spends **Hero Point** to reroll failed **Check**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: allows reroll; applies new result
- Pre-Condition: **Player** has **Hero Point**
- Failure-Modes:
  - **Hero Point** exhausted
- Domain Concepts: **Hero Point**, **Check**

### Story: Use Extra Effort (Player spends **Hero Point** or fatigue for temporary **Power** boost)

- Trigger:
  - Triggering-Actor: **Player**
  - Behavior: spends **Hero Point** or fatigue for **Extra Effort**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: grants temporary **Power** boost per **Extra Effort** rules
- Pre-Condition: **Player** has **Hero Point** or fatigue available
- Failure-Modes:
  - **Extra Effort** invalid for **Power**
- Domain Concepts: **Extra Effort**, **Hero Point**, **Power**

### Story: Gain Hero Point from Complication (Gamemaster awards **Hero Point** when **Complication** creates trouble)

- Trigger:
  - Triggering-Actor: **Gamemaster**
  - Behavior: **Complication** creates trouble in scene
- Response:
  - Responding-Actor: **Player**
  - Behavior: receives **Hero Point** for **Complication** trigger
- Pre-Condition: **Complication** is active for **Character**
- Failure-Modes:
  - **Complication** not applicable to situation
- Domain Concepts: **Complication**, **Hero Point**, **Character**

---

# Epic: Use Equipment (Participant uses **Equipment**, **Weapon**, **Armor**, or **Vehicle**)

- Triggering-Actor: **Player** or **Gamemaster**
- Responding-Actor: **Gamemaster** or **Player**
- Pre-Condition: **Character** has access to **Equipment**
- Failure-Modes:
  - **Equipment** unavailable or broken
- Domain Concepts: **Equipment**, **Weapon**, **Armor**, **Vehicle**, **Device**

### Story: Use Weapon in Attack (Participant uses **Weapon** for **Attack**)

- Trigger:
  - Triggering-Actor: **Player** or **Gamemaster**
  - Behavior: uses **Weapon** as part of **Attack**
- Response:
  - Responding-Actor: **Gamemaster**
  - Behavior: applies **Weapon** damage and traits to **Attack**
- Pre-Condition: **Character** has **Weapon**
- Failure-Modes:
  - **Weapon** out of range or inappropriate
- Domain Concepts: **Weapon**, **Attack**, **Equipment**

### Story: Use Armor for Protection (Character benefits from **Armor** **Toughness**)

- Trigger:
  - Triggering-Actor: **Gamemaster**
  - Behavior: applies **Armor** bonus to **Toughness** resistance
- Response:
  - Responding-Actor: **Player**
  - Behavior: receives **Toughness** bonus from **Armor**
- Pre-Condition: **Character** wears **Armor**
- Failure-Modes:
  - **Armor** penetrated or bypassed
- Domain Concepts: **Armor**, **Toughness**, **Equipment**
