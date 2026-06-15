---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Teaches exploration-phase acceptance criteria for story-graph.json: WHEN/THEN/AND/BUT, behavioral language, per-story domain terms, atomic AC, actor alternation, channel-specific detail, and verb–noun naming for story elements. Ships Markdown rules and Python scanners under this skill root for …"
---

# abd-acceptance-criteria

## Overview

Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit negatives (BUT). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

This skill is the practice standard for that work: templates for deliverables, rules for what “good” means (atomic AC, actor alternation, domain emphasis, channel-specific detail, source evidence when AC come from documents), and scanners that can run predictable mechanical checks alongside human review.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
story / AC work (exploration)
           |
           v
  templates/*.md -----> rules/*.md -----> scanners/*.py
           |                  |                |
           +------------------+----------------+
                              v
                    feedback into story-graph.json
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
