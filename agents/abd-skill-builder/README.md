---
catalogue_summary: "Provide portable repository standards aligned with Open Agent Skills: a focused SKILL.md for discovery, a merged AGENTS.md for multi-step workflow, plus documentation of build and validation (merge, build.py, scanners, CI), and a scaffold CLI so new skills match skills.sh-style layout without …"
---

# abd-skill-builder

## Overview

Provide portable repository standards aligned with Open Agent Skills: a focused SKILL.md for discovery, a merged AGENTS.md for multi-step workflow, plus documentation of build and validation (merge, build.py, scanners, CI), and a scaffold CLI so new skills match skills.sh-style layout without hand-copying fixtures.


---

_Maintainer / AI: replace this stub with a concise catalogue description (not a dump of `AGENTS.md`). Cover: what the agent does, why it exists, main steps (high-level sequence only), and which other agents and skills it works with (names/paths). Operational rules and long workflows stay in `AGENTS.md`. If the README is wrong or thin, rewrite the file after reading that entry doc — the generator never overwrites an existing README._

## How it fits together

_Put one ASCII diagram in the fenced block below (orchestration, roles, skills you load, workspace artifacts)._

```ascii
author intent
           |
           v
  build_skill / build_agent -----> scaffolds -----> validated skill or agent tree
```

## Source

- [AGENTS.md](AGENTS.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
