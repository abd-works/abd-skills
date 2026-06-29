# Input traps — drawio-domain-sync

Pre-flight only — not grill questions. Check each trap before rendering; flag gaps honestly.

- **Source ambiguity** — Which domain artifact is authoritative when both domain model and domain specification exist? Default to highest fidelity (domain specification > domain model > domain language).
- **Layout destruction** — Will a full re-render overwrite manual positioning the user already did in Draw.io? Prefer incremental CLI updates when a diagram already exists.
- **Wrong sync direction** — Is the markdown or the diagram the source of truth? Markdown wins; sync-back requires user review before applying diffs.
- **Domain language asymmetry** — When the source is domain language, row-level bullet edits do not round-trip from diagram to markdown — only concept add/delete and inheritance edges do.
- **Missing KA coverage** — Does every concept under each Key Abstraction appear on its tab? Boundary classes must be directly connected only — not two hops away.
