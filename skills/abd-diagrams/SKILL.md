---
name: abd-diagrams
description: >-
  Draw.io and Markdown norms for Agile by Design class and sequence diagrams: templates,
  layout rules, verify/relayout/fix-edge-styles CLI, and dual-file sync. The merged agent
  reference is AGENTS.md (built from content/parts/). For the linear OOAD walkthrough from
  specs or code, use the sibling skill abd-ooad.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# abd-diagrams — Diagram library (class & sequence)

This skill is the **diagram standards and tooling** layer: **Draw.io** + **Markdown** companions, **templates**, and **`drawio_cli.py`** for class diagrams.

## When to use this skill

Use **abd-diagrams** when you need to:

- Create or review **UML class diagrams** (structure, relationships, Jeff-style collaborators/invariants).
- Create or review **sequence / domain walkthrough** diagrams (lifelines, activations, messages).
- Apply **layout rules** (no overlapping classes, inheritance vertical order, orthogonal associations, sequence message rules).
- Run **`scripts/drawio_cli.py`** (`verify`, `relayout`, `fix-edge-styles`, etc.) on `.drawio` files.
- Keep **`.drawio` and `.md` pairs** aligned using the checked-in **templates**.

Use **`abd-ooad`** when the task is **OOAD from raw material** (read for meaning, name concepts, responsibilities, refine the model step by step).

## Primary reference: `AGENTS.md`

**`AGENTS.md`** at this skill root is the **single merged library** for agents and IDEs. It is **generated** from four source files:

| Source part | Topic |
|-------------|--------|
| `content/parts/class-diagrams.md` | Class diagrams: templates, sync rules, naming |
| `content/parts/class-diagram-layout-rules.md` | XML-level layout and edge-style rules |
| `content/parts/sequence-diagrams.md` | Sequence / walkthrough templates and sync |
| `content/parts/sequence-diagram-layout-rules.md` | Sequence layout and connection rules |

**Regenerate** after editing any part:

```bash
cd skills/abd-diagrams
python scripts/build_instructions.py
```

This writes **`AGENTS.md`** and **`content/built/AGENTS.md`**.

## Templates (always start here)

Paths are relative to the skill root:

| Kind | Draw.io | Markdown |
|------|---------|----------|
| Class | `templates/domain model template.drawio` | `templates/domain model template.md` |
| Sequence / walkthrough | `templates/domain realization template.drawio` | `templates/domain walkthrough template.md` |

Do **not** invent one-off shapes unless the user opts out—the templates encode the house notation (e.g. collaborators on the second line in Draw.io, matching `opt` / invariants in Markdown).

## Scripts

| Script | Role |
|--------|------|
| `scripts/build_instructions.py` | Merge `content/parts/*.md` → `AGENTS.md` |
| `scripts/drawio_cli.py` | Class diagram **create/edit**, **`verify`**, **`relayout`**, **`fix-edge-styles`**, etc. (`python scripts/drawio_cli.py --help`) |

**Note:** There is **no** CLI automation for sequence lifelines yet—new sequence work should **duplicate** `templates/domain realization template.drawio` and edit manually, following **`AGENTS.md`**.

## Workflow summary

1. For **methodology** (how to extract a model from text): follow **`abd-ooad`**.
2. For **notation and files**: follow **`AGENTS.md`** and the **templates**.
3. For **class diagram XML** hygiene: run **`drawio_cli.py`** commands as documented in **`AGENTS.md`** and CLI `--help`.
4. When changing library text: edit **`content/parts/*.md`**, then **`python scripts/build_instructions.py`**.

## Speech-to-text

Informal notes may say “vast diagram” or “lost diagram”—that usually means **class diagram** (see `content/parts/class-diagrams.md`).
