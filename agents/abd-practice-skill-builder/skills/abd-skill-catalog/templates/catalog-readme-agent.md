---
catalogue_summary: "{{CATALOGUE_SUMMARY}}"
---

# {{NAME}}

## Overview

{{OVERVIEW_STUB}}

_Maintainer / AI: replace this stub with a concise catalogue description (not a dump of `{{ENTRY_FILE}}`). Cover: what the agent does, why it exists, main steps (high-level sequence only), and which other agents and skills it works with (names/paths). Operational rules and long workflows stay in `{{ENTRY_FILE}}`. If the README is wrong or thin, rewrite the file after reading that entry doc — the generator never overwrites an existing README._

## How it fits together

_Put one ASCII diagram in the fenced block below (orchestration, roles, skills you load, workspace artifacts)._

```ascii
  user / workspace
        |
        v
  this agent (entry doc) -----> artifacts + handoffs
```

## Source

- [{{ENTRY_FILE}}]({{ENTRY_FILE}})
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
