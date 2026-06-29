# Input traps — abd-domain-walk

Pre-flight only — not grill questions. Check each trap before generating; flag gaps honestly.

- **Happy-path blindness** — Which scenarios have you walked only as success paths, without testing what happens when a step fails or data is missing?
- **Model gap** — Which pseudocode line required you to invent a method or class that does not exist in the domain model?
- **Cooperation under stress** — What happens when two aggregates need to coordinate and one rejects the request?
- **Real data** — Are your scenario values realistic enough to expose edge cases, or are they "example 1, example 2" placeholders?
- **Missing scenario** — Which business scenario did the domain expert mention that you have not walked yet?
