# Input traps — abd-domain-model

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Responsibility ambiguity** — when two concepts could reasonably own the same behavior, which one actually does — and what's the real-world evidence for that choice?
- **Hidden invariants** — which business rules feel so obvious that nobody has stated them — and what breaks downstream if the model doesn't make them explicit?
- **Collaboration direction** — when two concepts interact, which one initiates — and are we sure the direction reflects how the business actually works, not just how we'd code it?
- **Subtype vs. configuration** — when behavior varies by kind, is the variation genuinely structural or is it just a flag — and what happens when a new kind appears?
- **Missing concepts** — are there behaviors assigned to existing concepts that really belong to a concept nobody has named yet — a missing collaborator hiding inside another class?
