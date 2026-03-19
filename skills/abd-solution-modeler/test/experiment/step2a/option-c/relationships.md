# Cross-Module Relationships — option-c

Source: chunk_evidence.json
Option: C  |  Code-only: term match + definition patterns + co-occurrence + relationship patterns. No AI calls.
Total relationships detected: 386
Unique relationship types: 10

Each entry: [count] **FromConcept** (FromModule) --relationship--> **ToConcept** (ToModule)
Count = number of chunks where this relationship signal was detected.

---

[91x] **Effect** (Powers) uses / depends on **Check** (Resolution)
       Evidence chunks (5 of 91): dd71074ce318, 0b30704b97a2, 0b30704b97a2, 7a6d568a6006, 7a6d568a6006

[69x] **Effect** (Powers) produces **Condition** (Combat)
       Evidence chunks (5 of 69): 9c9f9b5a490d, b551e66974e2, 7a6d568a6006, 792ccb4b72a0, 6d18f5cb0ab3

[59x] **Condition** (Combat) impairs **Defense** (Character Traits)
       Evidence chunks (5 of 59): 6d18f5cb0ab3, 6d18f5cb0ab3, e087f7a0b70b, e087f7a0b70b, 04f4880a6e63

[50x] **Skill** (Character Traits) uses modifier from **Ability** (Character Traits)
       Evidence chunks (5 of 50): 34cb0222a3bd, 89a1fc58a123, 903a8c445c1a, dd71074ce318, 7420eccba7af

[41x] **HeroPoint** (Character) modifies **Check** (Resolution)
       Evidence chunks (5 of 41): 4cd63373be61, 4742b3550bee, 792ccb4b72a0, 079ee72c1633, 9132e0aa79c8

[29x] **AttackCheck** (Combat) extends / inherits from **Check** (Resolution)
       Evidence chunks (5 of 29): dd71074ce318, dd71074ce318, 7420eccba7af, 0b30704b97a2, 0b30704b97a2

[18x] **AttackCheck** (Combat) targets **Defense** (Character Traits)
       Evidence chunks (5 of 18): 0b30704b97a2, dcdc4c459ab6, b511fe78f53a, 6717e2899e27, c1c422470246

[14x] **Power** (Powers) is constrained by **PowerLevel** (Character)
       Evidence chunks (5 of 14): 7a6d568a6006, 301ee8a15809, cb4093e23f62, f1bc1ad153ee, 05f80df9e48f

[11x] **Advantage** (Character Traits) modifies **AttackCheck** (Combat)
       Evidence chunks (5 of 11): 301ee8a15809, a92e401b2501, 74ebb15a5905, 6dd3b64a2720, 481ffcf3c778

[4x] **Advantage** (Character Traits) modifies **Defense** (Character Traits)
       Evidence chunks (4 of 4): 74ebb15a5905, 87f598748db8, 086d54227650, 32947a2a15f9
