# Cross-Module Relationships — option-e

Source: chunk_evidence.json
Option: E  |  Hybrid: code signals all chunks; AI supplements high-density low-signal chunks only.
Total relationships detected: 322
Unique relationship types: 27

Each entry: [count] **FromConcept** (FromModule) --relationship--> **ToConcept** (ToModule)
Count = number of chunks where this relationship signal was detected.

---

[69x] **Effect** (Powers) produces **Condition** (Combat)
       Justification: detected by code pattern
       Evidence chunks (5 of 69): 9c9f9b5a490d, b551e66974e2, 7a6d568a6006, 792ccb4b72a0, 6d18f5cb0ab3

[53x] **Effect** (Powers) uses / depends on **Check** (Resolution)
       Justification: detected by code pattern
       Evidence chunks (5 of 53): 0b30704b97a2, 7a6d568a6006, 4742b3550bee, e05fc680a484, d1e949b40c7a

[50x] **Skill** (Character Traits) uses modifier from **Ability** (Character Traits)
       Justification: detected by code pattern
       Evidence chunks (5 of 50): 34cb0222a3bd, 89a1fc58a123, 903a8c445c1a, dd71074ce318, 7420eccba7af

[37x] **Condition** (Combat) impairs **Defense** (Character Traits)
       Justification: detected by code pattern
       Evidence chunks (5 of 37): 6d18f5cb0ab3, e087f7a0b70b, 04f4880a6e63, b511fe78f53a, 685941d4ae65

[29x] **AttackCheck** (Combat) extends / inherits from **Check** (Resolution)
       Justification: detected by code pattern
       Evidence chunks (5 of 29): dd71074ce318, dd71074ce318, 7420eccba7af, 0b30704b97a2, 0b30704b97a2

[18x] **AttackCheck** (Combat) targets **Defense** (Character Traits)
       Justification: detected by code pattern
       Evidence chunks (5 of 18): 0b30704b97a2, dcdc4c459ab6, b511fe78f53a, 6717e2899e27, c1c422470246

[16x] **Power** (Powers) is constrained by **PowerLevel** (Character)
       Justification: detected by code pattern
       Evidence chunks (5 of 16): 7a6d568a6006, 301ee8a15809, 9b8b75c1b5e7, 6c8715df5e97, 3c75d5b04a0e

[7x] **Ability** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Abilities are bought from the same Power Point budget and subject to Power Level caps.
       Evidence chunks (5 of 7): 9b8b75c1b5e7, 6c8715df5e97, a67593d532fb, a37758230a66, 6e090a5bf703

[5x] **HeroPoint** (Character) modifies **Check** (Resolution)
       Justification: detected by code pattern
       Evidence chunks (5 of 5): 792ccb4b72a0, 9ab4a1de72d2, 3a7f34326ad9, 706d511e685d, d421725a8d2c

[4x] **Skill** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Skills are bought from the same Power Point budget and subject to Power Level caps.
       Evidence chunks (4 of 4): 9b8b75c1b5e7, 6c8715df5e97, cefb93c1d699, 267bbd73af09

[3x] **Defense** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Defenses are bought from the same Power Point budget and subject to Power Level caps.
       Evidence chunks (3 of 3): 9b8b75c1b5e7, 6c8715df5e97, cefb93c1d699

[3x] **PowerPoint** (Character) is constrained by **PowerLevel** (Character)
       Justification: Power Point budget constrained by Power Level caps
       Evidence chunks (3 of 3): 3c75d5b04a0e, f97fb5b16662, 9575430bef02

[3x] **Ability** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Abilities bought from the same Power Point budget and subject to Power Level caps
       Evidence chunks (3 of 3): 3c75d5b04a0e, f97fb5b16662, 9575430bef02

[3x] **Skill** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Skills bought from the same Power Point budget and subject to Power Level caps
       Evidence chunks (3 of 3): 3c75d5b04a0e, f97fb5b16662, 9575430bef02

[3x] **Defense** (CharacterTraits) is constrained by **PowerLevel** (Character)
       Justification: Defenses bought from the same Power Point budget and subject to Power Level caps
       Evidence chunks (3 of 3): 3c75d5b04a0e, f97fb5b16662, 9575430bef02

[3x] **Ability** (Character Traits) is constrained by **PowerLevel** (Powers)
       Justification: Abilities are purchased within a Power Point budget constrained by Power Level caps.
       Evidence chunks (3 of 3): 9b4ab26032fa, ab9b367b750f, 919d7063d0ae

[3x] **Skill** (Character Traits) is constrained by **PowerLevel** (Powers)
       Justification: Skills are purchased within a Power Point budget constrained by Power Level caps.
       Evidence chunks (3 of 3): 9b4ab26032fa, ab9b367b750f, 919d7063d0ae

[2x] **Power** (Powers) is constrained by **PowerLevel** (Powers)
       Justification: Powers are defined at a per-rank cost, constrained by Power Level caps.
       Evidence chunks (2 of 2): 9b4ab26032fa, ab9b367b750f

[2x] **Defense** (Character Traits) is constrained by **PowerLevel** (Powers)
       Justification: Defenses are purchased within a Power Point budget constrained by Power Level caps.
       Evidence chunks (2 of 2): 9b4ab26032fa, 919d7063d0ae

[2x] **Ability** (Character Traits) produces **Defense** (Character Traits)
       Justification: Abilities contribute to defense totals.
       Evidence chunks (2 of 2): 60fdef9305c6, 6805431193d6

[1x] **Advantage** (Character Traits) is constrained by **PowerLevel** (Character)
       Justification: Advantages are bought from the same Power Point budget and subject to Power Level caps.
       Evidence chunks (1 of 1): 9b8b75c1b5e7

[1x] **Skill** (Character Traits) is constrained by **Power Point** (Character)
       Justification: Skills are purchased from the Power Point budget.
       Evidence chunks (1 of 1): fd5ed2485118

[1x] **Power** (Powers) is constrained by **Power Level** (Character)
       Justification: Powers are subject to Power Level caps.
       Evidence chunks (1 of 1): fd5ed2485118

[1x] **Effect** (Powers) produces **Weapon** (Gadgets & Gear)
       Justification: Weapons produce effects upon hitting a target.
       Evidence chunks (1 of 1): 2c3d57c2a1b3

[1x] **Construct** (Combat) uses / depends on **Damage** (Powers)
       Justification: Constructs suffer damage like inanimate objects.
       Evidence chunks (1 of 1): 6be13e770e51

[1x] **Skill** (Character Traits) targets **Repair** (Powers)
       Justification: Technology skill description for repairing damaged objects.
       Evidence chunks (1 of 1): 6be13e770e51

[1x] **Power Point** (Character) is constrained by **Power Level** (Character)
       Justification: Limits imposed by the series power level.
       Evidence chunks (1 of 1): 598bd6ff5a02
