---
description: >-
  Fix a defect: write a failing test that catches it, fix the code until green,
  then update docs to match. Use when the user describes a bug or defect.
mode: agent
---

Run these skills in order for the defect the user described. Read each skill and follow its instructions fully before moving to the next. For DDD steps, only run them if those artifacts already exist in the project.

1. **Failing Test (RED)** — find or create the test that catches this defect: `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md`
2. **Production Code (GREEN)** — fix code until the test passes: `skills/engineering/abd-clean-code/SKILL.md`
3. **Domain Language** _(if exists)_ — `skills/domain-driven-design/abd-domain-language/SKILL.md`
4. **Domain Sketch** _(if exists)_ — `skills/domain-driven-design/abd-domain-sketch/SKILL.md`
5. **Object Model** _(if exists)_ — `skills/domain-driven-design/abd-object-model/SKILL.md`
6. **Scenario Walkthrough** _(if exists)_ — `skills/domain-driven-design/abd-scenario-walkthrough/SKILL.md`
7. **Acceptance Criteria** — `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md`
8. **Spec by Example** — `skills/story-driven-delivery/abd-specification-by-example/SKILL.md`
9. **Story Map** — update the story if scope or behavior changed: `skills/story-driven-delivery/abd-story-mapping/SKILL.md`
