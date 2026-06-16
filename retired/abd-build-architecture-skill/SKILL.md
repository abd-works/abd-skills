---
name: abd-build-architecture-skill
catalog_garden_tier: practice
catalog_garden_order: 50
catalogue_one_liner: >-
  Turn a finished architecture reference into an active, loadable implementation skill with templates, rules, and scanners.
description: >-
  Build a new implementation skill — a full practice-skill package that
  generates code in a chosen architecture — from an architecture-mechanism
  reference document. Input is a finished reference (one file with layered
  description and one section per mechanism). Output is a complete
  practice-skill folder: SKILL.md, templates/ that produce real domain
  modules, rules/*.md that validate generated code against the reference's
  principles and patterns, ide-files/, and a scanners/ stub. Use when you
  have a finished architecture reference and need the agent or team to
  generate code that follows that architecture consistently.
---
# abd-build-architecture-skill

## Purpose

A team can write down its architecture and still ship code that drifts from it within a quarter. Documents do not enforce themselves. This skill closes that gap by turning a finished architecture document into an **active, automatable practice** — a packaged generator that produces real code in the architecture on demand, with checkable rules an agent or reviewer can run against any change. When this skill is done, the architecture is no longer just written down somewhere; it is something the team can *invoke*.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** A new folder `<arch-name>-technical-architecture/` containing the full skill package.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an architecture implementation skill is, reference→skill mapping, domain vs mechanism slice, scanners, and the generated skill shape.
- **`reference/examples.md`** — generated skill folder structure and shape of a good generated skill.
- **`templates/generated-SKILL.md`** — the worked example of the target `SKILL.md` shape for the generated skill. Do NOT modify this template.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/generated-SKILL.md` | The `SKILL.md` of the implementation skill being built |
| `templates/generated-domain-module.template.txt` | The implementation template the generated skill ships under `templates/` |
| `templates/generated-rule.md` | One rule file per mechanism principle in the generated skill's `rules/` |

**Key constraints:**
- One generated rule per reference principle — trace each back to the source.
- Templates cover every file in the reference's File Structure blocks — with filled examples.
- The generated skill inherits project coding/testing standards by reference, not copy.
- Scanner YAML fields appear only when the scanner script exists on disk.
- `ide-files/` ships three files with `.mdc`/`.instructions.md` body parity.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-build-architecture-skill \
  --workspace <path-to-generated-skill>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect the generated skill the way a reviewer would inspect any new practice skill.

- **Reference present and owned** — `inputs/architecture-reference.md` exists (single file, self-contained).
- **One rule per principle** — every principle from the reference has a `rules/<slug>.md`.
- **Templates cover the file structure** — every file path in reference File Structure blocks appears in a template with a filled example.
- **`SKILL.md` shape** — Purpose, Agent Instructions, Core concepts, Example, Build, Validate.
- **`ide-files/` parity** — `.mdc` and `.instructions.md` bodies match after normalization.
- **No invented mechanisms** — no rule enforces a principle absent from the reference.
- **Code conventions inherited** — references project coding/testing standard by name, not copy.
- **Scanners honest** — `scanner:` YAML only when the `.py` exists; otherwise manual review with TODO.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
