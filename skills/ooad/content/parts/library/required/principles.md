# Principles

1. **Orientation before extraction** — domain-scan is observation and mapping, not yet data collection. Identify 3–7 high-confidence anchors and suspected tensions before extracting candidates.

2. **Things before data** — Model the domain's real entities, responsibilities, and relationships first. Do not invent data fields just because templates have room.

3. **Nouns → verbs → structure** — Extract domain concepts (nouns) as candidates, turn relevant verbs into operations, then build relationships and invariants that encode domain rules.

4. **Model incrementally, validate constantly** — Build the model phase by phase, consulting key scenarios and use cases at domain-scan, raw-candidates, add-properties-semantically-tight, smashed-abstractions-and-hidden-roles, and model-in-layers. Tensions and contradictions are signals for refinement.

5. **Diagram and Markdown stay synchronized** — Maintain both class diagram (.drawio) and Markdown documentation side-by-side. Changes to one must be reflected in the other.

6. **Domain facts trump templates** — If the source material contradicts a standard pattern or template, favor the domain truth. Document the deviation and the reason.

7. **Inheritance is a last resort** — Prefer composition and aggregation. Use inheritance only when behavior generalizes cleanly across a family of related classes.

8. **Names matter** — Refine names throughout the process. A clear, honest name reveals the model's intent; ambiguous or misleading names hide problems.

9. **Diagram CLI is non-negotiable** — Class diagrams must be created and validated using `scripts/drawio_cli.py` and the templates in `templates/`. Do not hand-write Draw.io XML or invent diagram conventions.

10. **Workspace awareness** — Always know which project workspace you are writing to. All outputs go under `<workspace>/abd-ooad/`, never to ad-hoc locations.
