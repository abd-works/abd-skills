# Run abd-service-level-objectives

Read `skills/architecture-centric-engineering/abd-service-level-objectives/SKILL.md` and follow the Build steps.

When producing or updating the SLO matrix:

1. Use `templates/service-level-objectives.md` as the starting point and `templates/slo-row.md` when adding a single row inside a story or ADR.
2. Every SLO has three numbers: **target value**, **volume**, **percentage**. No bare adjectives ("fast", "highly available", "secure"). No 100% on dimensions where incidents are real (availability, latency, success rate).
3. Every row has a named **scope** (system / parent epic / epic / story) and exactly one of the six **NFR categories** (Performance & Scalability, Availability & Reliability, Security & Compliance, Usability & Accessibility, Maintainability & Supportability, Interoperability & Compatibility).
4. Map criticality (mission-critical / business-important / best-effort) against the story map; investment in SLOs follows criticality.
5. Ship a concrete error-budget policy with actions at 50% / 25% / 0% thresholds. No "review periodically".
6. SLAs (if any) are strictly looser than the SLO that supports them — never equal, never tighter.
7. Validate against the bundled rules block at the end of `SKILL.md` before completing.
