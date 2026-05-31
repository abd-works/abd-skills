---
name: class-responsibility-collaborator
catalog_garden_tier: practice
catalog_garden_order: 5
catalogue_one_liner: >-
  CRC cards from ubiquitous language; responsibilities, collaborators, invariants per concept.
description: >-
  For every domain concept: assign responsibilities, name collaborators,
  and declare invariants — all in one structured pass before object-model.
  Use when a completed Ubiquitous Language exists and the user asks to "run CRC",
  "assign responsibilities", or "build the CRC", or when ownership, boundaries,
  and invariants need to be made explicit before writing code.
---
# abd-class-responsibility-collaborator

## Purpose

This skill takes domain concepts from a completed Ubiquitous Language and produces a structured CRC model: for each concept, what it is responsible for, who it collaborates with, and what must always remain true. The result is a standalone file with `### **Class**` blocks under each Key Abstraction.

**CRC (Class-Responsibility-Collaborator)** modeling, introduced by Ward Cunningham and Kent Beck, is a lightweight way to explore object-oriented designs. This skill extends the classic technique by requiring explicit property and operation names, inline invariants, and subtype deltas — so the team can reason about ownership and boundaries before writing code.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `crc.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-crc.md`.

The file is **not** an in-place enrichment of the ubiquitous-language file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — CRC block format, subtypes, value objects and state-carrier classes, collection classes, collaborators, invariants, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/crc-outline-template.md` | The CRC file with responsibility tables under each class, grouped by KA. |
| `templates/domain.json` | Domain JSON with class names, attributes (noun-phrase responsibilities), and inheritance. |

**Quality bar:** Every behavior bullet from the Ubiquitous Language maps to at least one responsibility. Noun phrases for state, verb phrases for operations. No slash terms. Collaborators trace to UL sketch collaborations. Subtype blocks carry only deltas. State marker set to `crc`.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-class-responsibility-collaborator \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Per-phase output file** — named `[<name>-]crc.md`. No prior or later phase content lives in it.
- **Every KA has a class that names it** — the KA's own class is listed first with its responsibility table.
- **Coverage** — every concept from the ubiquitous-language file has a corresponding `### **Class**` block.
- **No sub-headings under classes** — responsibility tables live directly under each `### **Class**` heading.
- **References per KA** — one `### references` per KA with fenced `source` blocks.
- **Decisions per KA** — one `### decisions made` per KA listing CRC judgment calls.
- **No slash terms** — no `A / B` names in any heading or block.
- **Property names** — noun phrases using domain vocabulary.
- **Operation names** — verb phrases.
- **Subtype deltas only** — subtype blocks contain only added or overridden responsibilities.
- **Collaborators explicit** — no responsibility with implied actors has an empty collaborator column.
- **Invariants indented** — `|   invariant:` with three spaces after the pipe.
- **State marker** — front matter reads `state: crc`.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
