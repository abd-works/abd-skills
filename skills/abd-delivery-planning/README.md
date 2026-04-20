---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice …"
---

# abd-delivery-planning

## Overview

Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice work).

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
engagement context + risks
           |
           v
  strategies/*.md -----> chosen strategy -----> runs + checkpoints
           |                                        |
           +----------------------------------------+
                              v
                 agile-delivery-plan.md (workspace)
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
