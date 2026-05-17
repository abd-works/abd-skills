# Scanners — abd-architecture-outline

No automated scanners are shipped yet. The bundled rules are enforced by manual review and the Validate checklist in `SKILL.md`.

Candidates for future automation:

| Rule | Possible scanner check |
|---|---|
| `outline-leads-with-the-four-diagrams` | First four `##` headings after the document title are platform/layered/context/deployment. |
| `principles-are-decidable-one-sentence-stances` | Each principle bullet is a single sentence; word count < 40. |
| `major-systems-stay-at-one-line` | Major Systems section contains a table only; no paragraphs. |
| `decision-records-named-and-on-disk` | Every `ADR-NNN` cited in the outline has a matching file under `docs/architecture/decisions/`. |
