---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Produce thin-sliced delivery increments: vertical MVIs, spine vs optional paths, quality trade-offs, marketable increment names, and early risk validation. From a story map, write all template artifacts in templates/ (thin-slicing.md and thin-slicing.txt) with identical increment and story …"
---

# abd-thin-slicing

## Overview

Define prioritized increments. Group stories in a story map (and any notes on risk, constraints, or learning goals) into prioritized increments that can be delivered together. Each incremement includes its priority order, outcomes, slicing notes, and an ordered list od stories.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
backlog / MMF candidates
           |
           v
  thin-slice rules -----> ordered slices -----> ready-for-build packages
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
