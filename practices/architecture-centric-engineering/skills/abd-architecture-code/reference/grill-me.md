# Grill me — abd-architecture-code

**Mechanics:** [`common/reference/grill-me-with-practice-skill.md`](../../../../../common/reference/grill-me-with-practice-skill.md) — one question at a time; generate-to-learn when enough is shared.

Ask until layer boundaries, spec coverage, and test tiers are concrete:

- Where does each layer's responsibility end — what may it know about adjacent layers?
- Which spec patterns have never been exercised by a real story?
- For each scenario, is the risk in domain logic or framework plumbing?
- What responses from other systems or layers are assumed but unverified?
- Which behaviors are proven at only one test tier?
- Which error, concurrency, or partial-failure flows does the spec imply but the story doesn't name?
