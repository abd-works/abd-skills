# Cross-Module Relationships — option-b

Source: chunk_evidence.json
Option: B  |  AI (OpenAI) reads every chunk, extracts concepts + cross-module relationships. No code pre-filter.
Total relationships detected: 69
Unique relationship types: 41

Each entry: [count] **FromConcept** (FromModule) --relationship--> **ToConcept** (ToModule)
Count = number of chunks where this relationship signal was detected.

---

[6x] **Power** (Powers) is constrained by **PowerLevel** (Character)
       Justification: Powers are purchased from the Power Point budget
       Evidence chunks (5 of 6): 9575430bef02, 634190f2dd84, aa943c38ef67, dd5713402cfd, c8f8dadd6203

[5x] **Ability** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Abilities are purchased from the same Power Point budget and subject to Power Level caps
       Evidence chunks (5 of 5): aa943c38ef67, dd5713402cfd, c8f8dadd6203, db250ced1e81, d1e949b40c7a

[4x] **Advantage** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Advantages are purchased from the same Power Point budget and subject to Power Level caps
       Evidence chunks (4 of 4): aa943c38ef67, dd5713402cfd, c8f8dadd6203, 301534069c2d

[3x] **Skill** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Skills are purchased from the same Power Point budget and subject to Power Level caps
       Evidence chunks (3 of 3): aa943c38ef67, dd5713402cfd, c8f8dadd6203

[3x] **Defense** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Defenses are purchased from the same Power Point budget and subject to Power Level caps
       Evidence chunks (3 of 3): aa943c38ef67, dd5713402cfd, c8f8dadd6203

[3x] **Check** (Resolution) produces **Skill** (Character Traits)
       Justification: Acrobatics check determines success of maneuvers
       Evidence chunks (3 of 3): 5b37523dc91b, 2df9d8dcc068, f41e7b13c82a

[3x] **Skill** (Character Traits) is constrained by **Check** (Resolution)
       Justification: Skills are resolved through checks.
       Evidence chunks (3 of 3): 5f561d435c81, 86e82163c6b8, d5441abe7f45

[2x] **Skill** (Character Traits) uses / depends on **Check** (Resolution)
       Justification: skills are used to make checks
       Evidence chunks (2 of 2): 7420eccba7af, 7db012c9a682

[2x] **PowerPoint** (Character) is constrained by **PowerLevel** (Character)
       Justification: Total points must not exceed Power Level caps
       Evidence chunks (2 of 2): 9575430bef02, 634190f2dd84

[2x] **Ability** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Abilities are purchased from the Power Point budget
       Evidence chunks (2 of 2): 9575430bef02, 634190f2dd84

[2x] **Advantage** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Advantages are purchased from the Power Point budget
       Evidence chunks (2 of 2): 9575430bef02, 634190f2dd84

[2x] **Skill** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Skills are purchased from the Power Point budget
       Evidence chunks (2 of 2): 9575430bef02, 634190f2dd84

[2x] **Defense** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Defenses are purchased from the Power Point budget
       Evidence chunks (2 of 2): 9575430bef02, 634190f2dd84

[2x] **Skill** (Character Traits) uses / depends on **Ability** (Character Traits)
       Justification: Skills are derived from character abilities.
       Evidence chunks (2 of 2): b511fe78f53a, 33e0c08724ff

[2x] **Defense** (Character Traits) uses / depends on **Power** (Powers)
       Justification: Defenses are influenced by powers like Energy Control.
       Evidence chunks (2 of 2): 14dd371ce972, 714405399e02

[1x] **Skill** (MODULES AND CONCEPTS) modifies **Check** (MODULES AND CONCEPTS)
       Justification: training in a skill makes characters more effective at checks
       Evidence chunks (1 of 1): 89a1fc58a123

[1x] **Degree** (Resolution) modifies **Condition** (Combat)
       Justification: degrees of success and failure affect conditions
       Evidence chunks (1 of 1): 0b30704b97a2

[1x] **ExtraEffort** (Character) uses / depends on **Power** (Powers)
       Justification: extra effort allows retrying certain effects
       Evidence chunks (1 of 1): 4742b3550bee

[1x] **Advantage** (Character Traits) uses / depends on **Power** (Powers)
       Justification: advantages and powers work together
       Evidence chunks (1 of 1): e05fc680a484

[1x] **PowerLevel** (Character) is constrained by **Ability** (Character Traits)
       Justification: Power Level caps constrain the abilities that can be purchased
       Evidence chunks (1 of 1): 02269b6c9ef6

[1x] **Power** (Powers) modifies **Condition** (Combat)
       Justification: Powers can create conditions during combat.
       Evidence chunks (1 of 1): b511fe78f53a

[1x] **Defense** (Character Traits) uses / depends on **Advantage** (Character Traits)
       Justification: Toughness can be increased using advantages.
       Evidence chunks (1 of 1): 714405399e02

[1x] **Degree** (Resolution) modifies **Action** (Combat)
       Justification: Degrees of failure affect action outcomes
       Evidence chunks (1 of 1): 5b37523dc91b

[1x] **Check** (Resolution) produces **Action** (Combat)
       Justification: Success of checks defines actions taken
       Evidence chunks (1 of 1): 2df9d8dcc068

[1x] **Skill** (Character Traits) produces **Action** (Combat)
       Justification: Deception check determines action outcomes
       Evidence chunks (1 of 1): 4e205a3c2745

[1x] **Condition** (Combat) produces **Check** (Resolution)
       Justification: Intimidation check results in impaired condition
       Evidence chunks (1 of 1): 9a2865ac841b

[1x] **HeroPoint** (Character) uses / depends on **Power** (Powers)
       Justification: Luck allows re-rolling by spending hero points.
       Evidence chunks (1 of 1): 3a7f34326ad9

[1x] **Power** (Powers) produces **Condition** (Combat)
       Justification: Effects can cause conditions based on success or failure.
       Evidence chunks (1 of 1): f45e1af7c8dc

[1x] **Power** (Powers) is constrained by **ExtraEffort** (Powers)
       Justification: Tiring effects require extra effort to use
       Evidence chunks (1 of 1): 7ade13289c0f

[1x] **Device** (Powers) is constrained by **HeroPoint** (Character)
       Justification: Characters must spend hero points to use devices temporarily.
       Evidence chunks (1 of 1): 83acf5380dc1

[1x] **Ability** (Character Traits) produces **Construct** (Character Traits)
       Justification: constructs can buy ability ranks
       Evidence chunks (1 of 1): 05327100448d

[1x] **Toughness** (Character Traits) is constrained by **Damage** (Powers)
       Justification: constructs have a Toughness rank that measures damage resistance
       Evidence chunks (1 of 1): 6be13e770e51

[1x] **Fortitude** (Combat) targets **Condition** (Combat)
       Justification: Fortitude checks determine conditions like fatigued and exhausted.
       Evidence chunks (1 of 1): 800b98bbc634

[1x] **Condition** (Combat) produces **Fortitude** (Combat)
       Justification: failure on Fortitude check leads to incapacitated condition
       Evidence chunks (1 of 1): 7973bfe6a35b

[1x] **Damage** (Powers) targets **Toughness** (Character Traits)
       Justification: Damage effect requires Toughness resistance check
       Evidence chunks (1 of 1): 7ed36e3d5075

[1x] **Effect** (Powers) produces **Resistance Check** (Combat)
       Justification: effects have ranks that determine resistance difficulty
       Evidence chunks (1 of 1): f62657e080ad

[1x] **Attack Check** (Combat) produces **Resistance Check** (Combat)
       Justification: successful attack check leads to resistance check
       Evidence chunks (1 of 1): 9136b6d87e68

[1x] **Attack** (Combat) uses / depends on **Degree** (Resolution)
       Justification: Attack check determines degree of success
       Evidence chunks (1 of 1): 575d730364ed

[1x] **Attack** (Combat) modifies **Effect** (Powers)
       Justification: Effect bonus is modified by attack mechanics
       Evidence chunks (1 of 1): 575d730364ed

[1x] **Defense** (Character Traits) produces **Condition** (Combat)
       Justification: defenseless character has active defense bonuses of 0
       Evidence chunks (1 of 1): 32947a2a15f9

[1x] **Degree** (Resolution) uses / depends on **Check** (Resolution)
       Justification: degree of failure is based on check result
       Evidence chunks (1 of 1): 32947a2a15f9
