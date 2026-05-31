---
catalog_garden_tier: practice
catalog_garden_order: 10
name: abd-architecture-outline
catalogue_one_liner: >-
  First architecture artifact — four diagrams, principles, tech stack, major systems, and ADRs on one page.
description: >-
  Produce the first architecture artifact for a new or unfamiliar system —
  a mostly-diagrams document that fixes platform, layering, system context,
  deployment topology, guiding principles, technology stack, and a brief
  catalogue of major systems with decision records. The outline answers
  "what is this thing made of and what does it sit next to?" before any
  deeper architecture work begins. Use when kicking off a new project,
  onboarding needs a canonical picture, choosing a platform, settling system
  ownership, or preparing for an architecture review.
---
# abd-architecture-outline

## Purpose

A team that cannot draw its system on one page also cannot agree on what to build next. Outlines fix that. This skill produces the first architecture artifact for a system — short on prose, heavy on diagrams — so engineers, product, and stakeholders share a single picture of the platform, the layers, the neighbours, the deployment topology, and the principles in force. When the outline is in place, deeper architecture work (blueprint, reference, mechanisms) can start without re-litigating what the system *is*.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `architecture-outline.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an outline is, the four diagrams, guiding principles, major systems catalogue, decision records, and what the outline does NOT contain.
- **`reference/examples.md`** — a typical outline tree and the shape of a good outline.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/architecture-outline.md` | The outline document — four diagrams with captions, guiding principles, tech stack table, major systems table, and ADR list. |
| `templates/decision-record.md` | One ADR file per outline-level decision under `docs/architecture/decisions/`. |

**Diagram workflow:**

1. Seed diagrams: `.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>`
2. Fill placeholders in each `.drawio` file with real system components.
3. Export PNGs: `.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>`
4. Reference the PNGs from the outline markdown.

**Quality bar:** Four diagrams present (platform, layered, context, deployment), each with a caption of three sentences or fewer. Principles are decidable one-sentence stances (5–10 total). Major systems are one line each. ADRs exist on disk.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-architecture-outline \
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

- **Four diagrams present** — platform, layered, system context, deployment topology — each with a caption of three sentences or fewer.
- **Each diagram has a paired `.drawio` source** — `.\scripts\arch-drawio.ps1 verify` prints PASS.
- **Canonical filenames used** — `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, `deployment-architecture.drawio`.
- **Layered diagram shows dependency direction** — arrows are one-way, no cycles drawn.
- **Principles are decidable** — every principle is one sentence and could be applied to a real code change.
- **Technology stack is a table** — Layer / Technology / Version / Purpose; no narrative paragraphs.
- **Major systems are one line each** — no internal component descriptions.
- **ADRs exist on disk** — every ADR named in the outline has a matching file under `docs/architecture/decisions/`.
- **No mechanism detail** — auth, error handling, logging, caching are *named* if at all, never explained.
- **No data model** — entity relationships and persistence schemas are absent.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
