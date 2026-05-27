---
catalogue_summary: "Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML …"
---

# abd-practice-skill-builder

## Overview

Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML manual (vendored shell assets in abd-practice-skill-manual).

Orchestrate using the agent-local packages in skills/ under this agent (same idea as abd-context-to-memory routing to nested skills/abd-/SKILL.md*).

---

_Maintainer / AI: replace this stub with a concise AI Garden description (not a dump of `AGENTS.md`). Cover: what the agent does, why it exists, main steps (high-level sequence only), and which other agents and skills it works with (names/paths). Operational rules and long workflows stay in `AGENTS.md`. If the README is wrong or thin, rewrite the file after reading that entry doc — the generator never overwrites an existing README._

## How it fits together

_Put one ASCII diagram in the fenced block below (orchestration, roles, skills you load, workspace artifacts)._

```ascii
  user / workspace
        |
        v
  this agent (entry doc) -----> artifacts + handoffs
```

## Source

- [AGENTS.md](AGENTS.md)
- Regenerated site: `python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
