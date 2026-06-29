# Input traps — abd-domain-code

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Invariant gaps** — which business rules feel "obvious" but haven't been stated — and what breaks if the code doesn't enforce them?
- **Behavior ownership** — when two domain objects could reasonably own the same operation, which one actually does — and what's the consequence of getting it wrong?
- **State transition coverage** — which state changes are legal and which aren't — and are we confident we've mapped every transition, including the ones that should be rejected?
- **Domain vs. infrastructure bleed** — where is the boundary between pure domain logic and infrastructure concerns — and what concepts are we tempted to leak across that line?
- **Edge interactions** — what happens at the limits — zero items, maximum quantities, duplicate entries — where domain rules interact in ways nobody explicitly stated?
