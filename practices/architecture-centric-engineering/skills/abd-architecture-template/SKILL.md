---
catalog_garden_tier: practice
catalog_garden_order: 40
name: abd-architecture-template
catalogue_one_liner: >-
  Deep-dive reference document — one mechanism at a time with principles, patterns, diagrams, walkthroughs, and tests.
description: >-
  Produce or assign architecture reference for cross-cutting mechanisms —
  one mechanism at a time with principles, patterns, diagrams, walkthroughs,
  and tests. Reuses an existing reference section when already documented;
  creates only missing mechanisms. Use when a layered architecture description
  and a list of mechanisms with intent are known, and before production code
  is written.
---
# abd-architecture-template

## Purpose

Architecture decisions usually live in someone's head, a deck, or a wiki page that nobody opens twice. This skill packages those decisions into a **reference document** for the chosen architecture — **or assigns** sections that already exist. Each mechanism is documented **once**; later runs reuse it and only add what's missing.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**Primary file:** `architecture-reference.md` under `docs/architecture/`. Add a scoped prefix (e.g. `increment-8-marketing-engine-reference.md`) only when many new mechanisms would bloat the canonical file.

**Assignment record:** When mechanisms are reused, append or update a short **Mechanism assignments** table at the end of the run (in the ticket note, handoff comment, or companion markdown) — mechanism name, decision (`assign` | `create`), path, section heading.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — mechanisms, assign vs create workflow, five-part shape, section organization.
- **`reference/examples.md`** — per-mechanism mode example and the shape of a good mechanism section.

### 2. Resolve — assign or create (quick or long pass)

1. **Discover** existing reference files under `docs/architecture/` and read `docs/planning/delivery-war-room/mechanism-registry.json` when present.
2. **List mechanisms in scope** from the ticket blueprint (and upstream artifacts).
3. For each mechanism: **assign** if complete, **create** if missing.
4. On kanban: if **all assign** → quick pass (assignment table only); if **any create** → long pass (author sections + update registry).

### 3. Generate (create path only)

Read every file in **`rules/`**; author new sections to those rules.

| Template | What to produce |
| --- | --- |
| `templates/architecture-reference.md` | New mechanism section(s) only, or a new scoped reference file when warranted. |

**Prerequisites for create path:**
1. A **layered description** of the target architecture (layers, tech in each, responsibilities).
2. A **list of mechanisms to create** — those not satisfied by assign.

**Section organization:** Count mechanisms being **created**. 2–3 tightly related → combined section. 4+ → one section per mechanism.

**Code standards:** Production code samples follow the project's coding standard (default: `abd-clean-code`). Test snippets follow the project's testing standard (default: `abd-acceptance-test-driven-development`).

### 4. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-architecture-template \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Reuse honored** — no duplicate mechanism sections; assignment table lists every mechanism in scope with assign or create.
- **Required sections** — every **created** mechanism has Principles & Patterns, File Structure, Participants, Flow, Walkthrough Example, and Testing subsection.
- **TOC** — the file opens with a Table of Contents with anchor links to every H2.
- **Diagrams present** — every mechanism has a class diagram AND a sequence diagram.
- **Walkthroughs are step-numbered** — not prose paragraphs. Each step names the participant.
- **Code follows the project's coding standard** — no `Manager`, `Handler`; domain entities carry behaviour.
- **Tests follow the project's testing standard** — Given/When/Then helpers; story-driven names.
- **Grounded in source of truth** — layer and mechanism names match the architecture's agreed source.
- **Section organization matches mechanism count** — 2–3 → combined; 4+ → per-mechanism.
- **Self-contained mechanisms** — a reader who jumps to one mechanism has enough to implement it.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
