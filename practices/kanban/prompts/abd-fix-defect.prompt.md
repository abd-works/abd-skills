---
description: >-
  Fix a defect: write a failing test that catches it, fix the code until green,
  then update docs to match. Use when the user describes a bug or defect.
mode: agent
---

You are now in **defect-fixing mode**. Every bug reported in this session follows this process — no exceptions. Read each skill fully before acting on it. Skip DDD steps only if those artifacts do not yet exist in the project.

1. **Failing Test (RED)** — find or write the test that catches this defect: `../skills/abd-story-acceptance-test/SKILL.md`
2. **Production Code (GREEN)** — fix code until the test passes: `../skills/abd-clean-code/SKILL.md`
3. **Domain Language** _(if exists)_ — update terms or concept sketches affected by the fix: `../skills/abd-domain-language/SKILL.md`
4. **Domain Specification** _(if exists)_ — update the class model if types or responsibilities changed: `../skills/abd-domain-specification/SKILL.md`
5. **Acceptance Criteria** _(if exists)_ — correct any WHEN/THEN that was wrong or missing: `../skills/abd-story-acceptance-criteria/SKILL.md`
6. **Spec by Example** _(if exists)_ — update or add scenarios that cover the defect: `../skills/abd-story-specification/SKILL.md`
7. **Story Map** _(if scope or behavior changed)_ — update the story that owned this behavior: `../skills/abd-story-mapping/SKILL.md`
