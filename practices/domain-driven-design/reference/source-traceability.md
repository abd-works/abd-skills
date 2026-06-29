# Domain — Source Traceability

Every domain claim in glossary and language artifacts must trace to evidence on disk.

---

## Rules

- Every **`Source:`** reference points to a **real file** at an **exact location** (path + section or line when possible).
- **KA References** — one `### KA References` per KA; every term in the KA covered by at least one reference entry.
- **No fabricated sources** — if the source does not exist, flag the gap; do not invent a path.
- **Verbatim discipline** — when a rule requires verbatim names from upstream artifacts, copy character-for-character.

---

## Glossary-specific

- References grouped at KA level under `### KA References`, not per term when the rule set says KA-level grouping.
- Boundary terms: `*(owned by: Module)*` with a single named owner.

---

## Language-specific

- One `#### References` per KA, after `#### Decisions made`.
- Boundary entries: `Owned by: ModuleName`.
