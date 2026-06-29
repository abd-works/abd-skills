# Input traps — abd-ddd-design-building-blocks

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Identity assumption** — Does this concept truly need a persistent identity, or are you giving it one out of habit?
- **Aggregate boundary** — What invariant does this aggregate protect — and can you state it as a business rule, not a database constraint?
- **Value Object hiding** — Are any "entities" actually interchangeable by value — same data means same thing, no lifecycle?
- **Service or misplaced logic** — Is this domain service genuinely homeless, or does the operation belong on an entity you haven't modelled yet?
- **Consistency boundary** — Does the business really need immediate consistency here, or would eventual consistency be acceptable — and who decided?
