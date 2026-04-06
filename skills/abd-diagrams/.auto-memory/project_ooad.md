---
name: OOAD Skill Project
description: Jeff is building a complete OOAD (Object-Oriented Analysis & Design) skill for Cowork. Phase 1 is done: a Draw.io class diagram CLI + wrapping skill.
type: project
---

Jeff is building a multi-phase OOAD skill. Phase 1 (done) includes:

- `drawio_cli.py` — Python CLI for creating/editing Draw.io class diagrams using Jeff's notation style
- `.claude/skills/ooad/SKILL.md` — Cowork skill wrapping the CLI

Both live in the user's OOAD-skill workspace folder.

**Why:** Jeff wants Claude to be able to create properly-formatted class diagrams during OOAD conversations, following the notation conventions he demonstrated in his class-diagrams video (swimlane classes, correct arrow types, inline dependency annotations, UML frames, object instances).

**How to apply:** Pick up from the OOAD skill folder. Phase 2 (in progress): domain walkthroughs / sequence diagrams documented with **dual artifacts** (Draw.io + Markdown templates), `references/class-diagrams.md` and `references/sequence-diagrams.md`, and root `SKILL.md` section on walkthroughs. Sequence **Draw.io** is template-based (no CLI yet); class diagrams remain CLI-driven.

The CLI supports: `new`, `add-class`, `add-field`, `add-method`, `add-association`, `add-composition`, `add-aggregation`, `add-inheritance`, `add-dependency`, `add-frame`, `add-object`, `add-instance-of`, `list-classes`, `show-class`, `describe`.

Jeff's notation conventions (from video analysis + drawio file):
- Fields above divider, methods below
- Visibility prefixes: `+` public, `-` private, `#` protected
- Abstract members are italic (--abstract flag)
- Inline dependency hints on 2nd line of field/method text
- Composition = filled diamond (lifecycle ownership)
- Aggregation = hollow diamond (independent lifetime)
- Inheritance = dashed line with hollow block arrow
- UML frames group related classes
