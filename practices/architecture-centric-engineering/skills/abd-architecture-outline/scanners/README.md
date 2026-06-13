# Scanners — abd-architecture-outline

No automated scanners are shipped yet. The bundled rules are enforced by manual review and the Validate checklist in `SKILL.md`.

Candidates for future automation:

| Rule | Possible scanner check |
|---|---|
| `outline-leads-with-system-context-diagram` | First `##` heading after the document title is the system context section; no layered, platform, or deployment diagram headings present. |
| `principles-are-decidable-one-sentence-stances` | Each principle bullet is a single sentence; word count < 40. |
| `major-systems-stay-at-one-line` | Major Systems section contains a table only; no paragraphs. |
| `decision-records-named-and-on-disk` | Every `ADR-NNN` cited in the outline has a matching file under `docs/architecture/decisions/`. |
