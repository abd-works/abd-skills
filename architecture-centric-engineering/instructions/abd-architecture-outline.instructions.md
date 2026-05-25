# Run abd-architecture-outline

Read `skills/architecture-centric-delivery/abd-architecture-outline/SKILL.md` and follow the Build steps.

When producing or updating an architecture outline:

1. Use `templates/architecture-outline.md` as the starting point.
2. Lead with the four diagrams in order: platform, layered architecture, system context, deployment topology.
3. Keep principles to one decidable sentence each (5–10 total).
4. Keep the major systems catalogue to one line per system; defer all "how" detail to the blueprint and reference documents.
5. Capture every outline-level decision as its own ADR file under `docs/architecture/decisions/` using `templates/decision-record.md`.
6. Validate against the bundled rules block at the end of `SKILL.md` before completing.
