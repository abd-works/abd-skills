---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Write tests first. Write code to pass them. This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should …"
---

# abd-acceptance-test-driven-development

## Overview

Write tests first. Write code to pass them.

This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is test-driven: write a test that expresses the expected behavior, run it to confirm it fails (RED), then rely on a  downstream skill or agent to develop the production code skill to implement until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do —  test methods show the Given-When-Then flow and helper functions do the work.

The skill covers the full test quality bar: domain language in names, observable-behavior assertions, coverage of normal and failure paths, helper reuse, and clean production code that makes tests easy to write.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
failing example (red)
           |
           v
  minimal code (green) -----> refactor -----> rules + scanners
           ^                                      |
           +--------------------------------------+
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
