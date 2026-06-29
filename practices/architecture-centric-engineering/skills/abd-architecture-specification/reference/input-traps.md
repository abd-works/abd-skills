# Input traps — abd-architecture-specification

Assumptions, ambiguities, and missing context that commonly produce a weak specification. Check each trap against available input before generating — flag gaps honestly; do not invent patterns to fill them.

- **Domain-to-file mapping** — when a new domain concept appears, does the spec make it obvious which files get created, where they live, and what they're named — or does that require a judgment call every time?
- **Mechanism boundaries in code** — for each mechanism, can you point to exactly where its code starts and stops? If two mechanisms touch the same file or class, is the ownership clear or are they entangled?
- **Walkthrough vs. real flow** — does the walkthrough trace a path that a real request actually follows, or does it show an idealized sequence that skips the messy parts (retries, fallbacks, partial failures)?
- **Test tier proof** — what does each test tier actually prove about the architecture? If a tier is just re-testing the same behavior at a different layer, what unique architectural risk is it supposed to catch?
- **Pattern fit for edge cases** — the spec defines patterns for the common case, but what happens when a story doesn't fit the pattern cleanly? Where are the seams that will need judgment, and are those documented or left implicit?
