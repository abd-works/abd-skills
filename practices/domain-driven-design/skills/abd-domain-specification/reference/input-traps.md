# Input traps — abd-domain-specification

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Type precision** — which properties are typed as generic primitives when the domain actually constrains them — where does "string" hide a real domain type with its own rules?
- **Relationship ownership** — when two concepts reference each other, which one owns the relationship — and what happens to the dependent when the owner changes or disappears?
- **Cross-concept invariants** — which business rules span multiple classes — and where does the enforcement logic actually live when no single class owns the whole rule?
- **Interaction completeness** — for operations with multiple steps, are we confident we know every participant — or are there hidden collaborators the sequence depends on?
- **Identity assumptions** — which concepts have identity and which don't — and what breaks if something we treat as a value actually needs to be tracked individually?
