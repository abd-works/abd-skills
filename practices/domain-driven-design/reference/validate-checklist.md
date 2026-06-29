# Domain-Driven Design — Shared Validate Checklist

Apply these items during [`common/reference/rule-checklist.md`](../../../common/reference/rule-checklist.md) for every DDD practice skill.

---

## All DDD practice skills

- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.
- **Per-phase output file** — each fidelity skill writes its own artifact (`domain-glossary.md`, `domain-language.md`, `domain-model.md`, etc.); no prior or later phase content in the same file.
- **Template instructions omitted** — generated project files contain stakeholder-facing content only.

---

## Glossary and language

- **Source traceability** — every claim traces to a real file on disk. See [`source-traceability.md`](./source-traceability.md).
- **KA shape** — every KA intro opens with "*KAName* is …"; `#### Decisions made` under each `## KA`.
- **Terms** — behavioral bullets; boundary terms carry `*(owned by: Module)*`; domain terms *italicized*.

---

## Model and specification

- **Coverage** — every concept from the prior-phase domain artifact has a corresponding block in the new artifact.
- **No slash terms** — no `A / B` names in headings or blocks (model).
- **Diagram on disk** — when `reference/diagram-workflow.md` exists, the `.drawio` file exists before the cell is marked done.

---

## Context map, building blocks, walkthrough

- **Complete coverage** — every input concept or scenario appears in the output or is explicitly marked unresolved.
- **Walk lines trace** — pseudocode maps to class and operation from the prior-phase file.
