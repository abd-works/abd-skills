---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
catalogue_one_liner: >-
  Second-level architecture — components in paragraphs, typed mechanisms, data model, testing strategy, and ADRs.
description: >-
  Produce the second-level architecture document after the outline — a
  blueprint that names each architectural component in a paragraph or two
  (purpose, dependencies, interactions, no internal details), names every
  cross-cutting concern as a typed "architecture mechanism" (security, error
  handling, logging, validation, configuration, etc.), shows the data
  architecture at the model level, captures a common testing strategy, and
  records decisions. Deep internals defer to abd-architecture-specification.
  Use when an outline exists and the team needs component-level detail,
  mechanism cataloguing, data architecture, or preparing for architecture review.
---
# abd-architecture-blueprint

## Purpose

The outline shows what a system *is*; the blueprint shows what it is *made of*. A blueprint is the document a tech lead opens to answer "where does the order code live? what does it depend on? how does it talk to the catalogue?" without yet drilling into the implementation patterns. It names every architectural component in a paragraph or two, catalogues every cross-cutting concern as an **architecture mechanism**, shows the data architecture at the model level, captures the common testing strategy, and lists the decisions taken at this level. When the blueprint is in place, the **architecture reference** can go deep on one mechanism at a time without re-explaining the system to its reader.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `architecture-blueprint.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — components vs systems, architecture mechanisms, data architecture, testing architecture at this level, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** — typical blueprint file tree and the shape of a good blueprint.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/architecture-blueprint.md` | The blueprint document — scope, components, mechanisms, data architecture, testing architecture, extension (if applicable), and ADR list. |

**Diagram workflow:**

1. Seed diagrams: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill `component-overview.drawio` and `entity-relationships.drawio` with real components/entities.
3. Export PNGs: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`
4. Reference the PNGs from sections 2 and 4.

**Quality bar:** Components described in 1–2 paragraphs (purpose, dependencies, interactions — no internals). Every mechanism is a named, typed subsection. Data architecture is entity-level. Extension section present only when warranted.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-architecture-blueprint \
  --workspace <path-to-output>
```

Then verify diagrams:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Components in paragraphs, not internals** — every component has 1–2 paragraphs; no class lists, no method tables, no file trees.
- **Paired drawio for component overview** — `component-overview.drawio` exists; verify prints PASS.
- **Every mechanism is named, typed, and short** — each cross-cutting concern has its own subsection with 1–2 paragraphs; deep walkthroughs deferred.
- **Data architecture is entity-level** — relationship diagram and ownership table; no schemas, no DDL.
- **Paired drawio for entity relationships** — `entity-relationships.drawio` exists; verify prints PASS.
- **Testing architecture is common-across-the-system** — tiers, boundaries, common doubles only.
- **Extension section present only when warranted** — no "TBD" placeholder.
- **ADRs exist on disk** — every ADR cited has a matching file; numbering continues from outline.
- **No outline-level material** — no platform diagram, no tech-stack table, no major-systems one-liners.
- **No reference-level material** — no code walkthroughs, no multi-participant sequence diagrams.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
