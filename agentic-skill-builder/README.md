# Agentic skill builder

Sub-project under **`agilebydesign-skills/agentic-skill-builder/`** for **agentic orchestration** of skill authoring: building skills to repository standards, operating them as structural tests, critiquing outputs with domain expertise, and (optionally) deploying to git with versioning.

This is **not** a Cursor “skill” package. It is a normal Python project (library + CLI + docs).

*(This folder was previously scaffolded as `skills-delivery`; all project files now live here.)*

## Layout

| Path | Purpose |
| ---- | ------- |
| `src/agentic_skill_builder/` | Application code (LangGraph graphs, agents, CLIs) |
| `docs/` | Plans, architecture, runbooks |
| `conf/` | Example configs, graph defaults (no secrets) |
| `test/` | Pytest tests |
| `log/` | Runtime logs (gitignored contents; folder may exist) |
| `requirements/` | Pinned dependency sets for this project only |

Python dependencies are managed with **`pyproject.toml`** + **`uv`/`pip`**; use a **local virtual environment** (`.venv/`) — see `docs/development/python-environment.md`.

## First read

- **`docs/plans/langgraph-agentic-orchestration-plan.md`** — master plan for LangGraph-based builder / operator / critic / deployer and human-in-the-loop gates.

## Status

**Planning / scaffold.** Implementation of LangGraph graphs is not yet in `src/`.
