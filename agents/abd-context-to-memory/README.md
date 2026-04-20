---
catalogue_summary: "Orchestrate convert → chunk → embed → search by coordinating this agent's skills. Decide when each stage runs, whether to use a strategy pass (review context_chunking_spec.yaml before chunk + embed) or straight-through, and hold cross-stage quality (real headings before chunking, sane splits after …"
---

# abd-context-to-memory

## Overview

Orchestrate convert → chunk → embed → search by coordinating this agent's skills. Decide when each stage runs, whether to use a strategy pass (review context_chunking_spec.yaml before chunk + embed) or straight-through, and hold cross-stage quality (real headings before chunking, sane splits after chunking).

Per-stage procedures: *skills/abd-/SKILL.md and each skill's references/**.

---

_Maintainer / AI: replace this stub with a concise catalogue description (not a dump of `AGENTS.md`). Cover: what the agent does, why it exists, main steps (high-level sequence only), and which other agents and skills it works with (names/paths). Operational rules and long workflows stay in `AGENTS.md`. If the README is wrong or thin, rewrite the file after reading that entry doc — the generator never overwrites an existing README._

## How it fits together

_Put one ASCII diagram in the fenced block below (orchestration, roles, skills you load, workspace artifacts)._

```ascii
source docs / assets
           |
           v
  convert / chunk -----> markdown mirror -----> embed / index (when wired)
```

## Source

- [AGENTS.md](AGENTS.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
