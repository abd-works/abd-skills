# Input traps — abd-bounded-context-map

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Hidden coupling** — Which contexts do people treat as independent but actually share data, vocabulary, or lifecycle?
- **Ownership ambiguity** — Where does one team's responsibility end and another's begin — and does everyone agree?
- **Translation cost** — Which boundary crossings silently corrupt meaning because the same word means different things on each side?
- **Missing context** — Is there a bounded context the team hasn't named yet because it lives inside someone's head or a spreadsheet?
- **Relationship direction** — For each dependency, which side sets the rules — and what happens when the downstream context disagrees?
