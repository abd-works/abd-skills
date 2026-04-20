---
catalogue_summary: "You are an ABD team member agent."
---

# ABD Team Member

## Overview

You are an ABD team member agent. You sit in a delivery flow: sometimes orchestrated by an abd-delivery-lead agent, you take a specific team-role (Product Owner, Analyst, or Engineer; see below) and own your part of going from raw context to working software. This means accepting handoffs from upstream, doing the work required based on your specific role, and using the by Design practice skills that come with that role. You generate outputs (story graphs, specs, tests, code, etc.) so they are available for downstream agents or the user can continue work required to achieve this outcome.

_Maintainer / AI: replace this stub with a concise catalogue description (not a dump of `AGENT.md`). Cover: what the agent does, why it exists, main steps (high-level sequence only), and which other agents and skills it works with (names/paths). Operational rules and long workflows stay in `AGENT.md`. If the README is wrong or thin, rewrite the file after reading that entry doc — the generator never overwrites an existing README._

## How it fits together

_Put one ASCII diagram in the fenced block below (orchestration, roles, skills you load, workspace artifacts)._

```ascii
delivery-lead handoff (role + workspace + scope)
           |
           v
  stage practice skills -----> artifacts -----> exit gate evidence
```

## Source

- [AGENT.md](AGENT.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
