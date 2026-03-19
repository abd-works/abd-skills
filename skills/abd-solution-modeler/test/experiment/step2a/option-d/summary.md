# Summary — option-d

Chunks: 267  |  AI calls: 1  |  Time: 0.315s
Concept mentions: 1323  |  Relationships: 267

## Concept Evidence by Module

Format per concept: [definition:N | table:N | rule:N | example:N | mention:N]


### Character
Total evidence instances: 159 across 2 concepts

  **Character**  [definition:8 | mention:124]
  **Complication**  [definition:3 | mention:24]

### Character Traits
Total evidence instances: 336 across 4 concepts

  **Skill**  [definition:2 | mention:102]
  **Defense**  [definition:9 | mention:87]
  **Advantage**  [definition:5 | mention:67]
  **Ability**  [definition:3 | mention:61]

### Combat
Total evidence instances: 212 across 2 concepts

  **Action**  [definition:37 | mention:120]
  **Condition**  [definition:3 | mention:52]

### Powers
Total evidence instances: 421 across 3 concepts

  **Power**  [definition:9 | mention:177]
  **Effect**  [definition:38 | mention:117]
  **Modifier**  [definition:8 | mention:72]

### Resolution
Total evidence instances: 195 across 2 concepts

  **Check**  [definition:15 | mention:111]
  **Degree**  [definition:1 | mention:68]

## Cross-Module Relationships

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

[6x] **Power** (Powers) is constrained by **PowerLevel** (Character)
       Justification: detected by code pattern
       Evidence chunks (5 of 6): 7a6d568a6006, 301ee8a15809, 05f80df9e48f, b60c97b07a3c, 1094aa03eba1

[5x] **HeroPoint** (Character) modifies **Check** (Resolution)
       Justification: detected by code pattern
       Evidence chunks (5 of 5): 792ccb4b72a0, 9ab4a1de72d2, 3a7f34326ad9, 706d511e685d, d421725a8d2c
