---
description: >-
  Ship a feature end-to-end through the story-driven-delivery pipeline.
  Use when the user describes a new or changed feature.
mode: agent
---

Run these skills in order for the feature the user described. Read each skill and follow its instructions fully before moving to the next. For DDD steps, only run them if those artifacts already exist in the project.

1. **Story Map** — `abd-story-mapping`
2. **Domain Language** _(if exists)_ — `abd-domain-language`
3. **Acceptance Criteria** — `abd-story-acceptance-criteria`
4. **domain model** _(if exists)_ — `abd-domain-model`
5. **Spec by Example** — `abd-story-specification`
6. **Class Model** _(if exists)_ — `abd-domain-specification`
7. **Acceptance Tests (RED)** — `abd-story-acceptance-test`
8. **Production Code (GREEN)** — `abd-clean-code`
