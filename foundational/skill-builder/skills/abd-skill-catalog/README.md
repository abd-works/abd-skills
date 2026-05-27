---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Regenerate the browsable AI Garden (skills + agents HTML + outline.md) from repo packages."
---

# abd-skill-catalog

## Overview

Scan agilebydesign-skills (skills/ and agents/), maintain each package’s root README.md for card and detail copy (overview + ASCII), then regenerate catalog/ HTML and outline.md from those files plus a generated file tree.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The AI Garden renders this block literally in a `<pre>`._

```ascii
skills/  agents/
       \      /
        v    v
   package README.md (Overview + ```ascii)
        |
        v
  generate_abd_catalog.py -----> catalog/*.html + outline.md
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
