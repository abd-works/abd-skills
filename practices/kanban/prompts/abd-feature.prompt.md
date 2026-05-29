---
description: >-
  Ship a feature end-to-end through the story-driven-delivery pipeline.
  Use when the user describes a new or changed feature.
mode: agent
---

Run these skills in order for the feature the user described. Read each skill and follow its instructions fully before moving to the next. For DDD steps, only run them if those artifacts already exist in the project.

1. **Story Map** — `abd-story-mapping`
2. **Ubiquitous Language** _(if exists)_ — `abd-ubiquitous-language`
3. **Acceptance Criteria** — `abd-acceptance-criteria`
4. **CRC** _(if exists)_ — `abd-class-responsibility-collaborator`
5. **Spec by Example** — `abd-specification-by-example`
6. **Object Model** _(if exists)_ — `abd-object-model`
7. **Acceptance Tests (RED)** — `abd-acceptance-test-driven-development`
8. **Production Code (GREEN)** — `abd-clean-code`
