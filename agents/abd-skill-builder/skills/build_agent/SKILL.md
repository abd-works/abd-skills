---
name: build-agent
description: Scaffold a multi-skill agent — thin AGENTS.md merge from content/*.md, leaf skills under skills/. For orchestrators, not single skill packages.
---

# Build agent

## When to use

You want an **orchestrator** repo: one **`AGENTS.md`** that describes **order, gates, and hand-offs**, with **each stage** implemented as a **separate** folder under **`skills/<name>/`** (each with its own **`SKILL.md`**).

Typical in this monorepo: **`agents/abd-context-to-memory`** (convert → chunk → embed → search as separate skills).

## When not to use

You want **one** Open Agent Skill package with **`content/parts/`**, **`phase_files`**, **`generate.py`**, and **`scripts/base/build.py`**. That is **build_skill** (`skills/build_skill/scripts/build_skill.py`), not this leaf.

## What gets created

`new_agent.py` writes a **new directory** (parent must exist; target folder must not):

| Path | Role |
| --- | --- |
| `content/*.md` | Stubs merged into **`AGENTS.md`** (headings from **`skill-config.json`**). |
| `skill-config.json` | **`agents_md.sections`**: `{ "heading", "file" }` pairs. |
| `scripts/build.py` | Copied from **`skills/build_agent/templates/build.py`** — same merge pattern as **`agents/abd-context-to-memory/scripts/build.py`**. |
| `skills/workspace/` | Copied from **`skills/build_agent/templates/workspace_skill/`** (get/set workspace scripts). |
| `skills/` | Add other leaf skills here (`capabilities/` packs install under **`skills/capabilities/`** on this repo only; target agents use their own `skills/`). |
| `SKILL.md` | Minimal discovery; real workflow is **`AGENTS.md`**. |

## Commands

From **abd-skill-builder** repo root:

```bash
python skills/build_agent/scripts/new_agent.py --name my-agent --out path/to/parent
cd path/to/parent/my-agent
# edit content/*.md, populate skills/
python scripts/build.py
```

## Reference

- **Layout vs skill package:** [content/layout.md](content/layout.md)
- **Installer:** [scripts/README.md](scripts/README.md)
- **Skill vs agent scripts:** [../../scripts/base/README.md](../../scripts/base/README.md)
- **Architecture note:** [../../content/builder-architecture.md](../../content/builder-architecture.md)
