---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design. This skill covers the full quality bar for implementation code: single-responsibility functions and classes, intention-revealing names, explicit constructor …"
---

# abd-clean-code

## Overview

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

The skill covers the full implementation quality bar: names that reveal intent, guard-clause control flow, no magic numbers, no swallowed exceptions, no hidden globals, encapsulated internals, and domain vocabulary throughout.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
code / modules under review
           |
           v
  rules (smells, naming) -----> guidance -----> safe refactors
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
