---
description: >-
  Sync upstream artifacts after a downstream change. Use when code, tests,
  specs, or AC have changed and higher-level docs may be out of date.
mode: agent
---

An artifact has changed. Ask the user whether to sync in both directions. Only offer levels whose artifacts exist. Stop at each level if the user says no.

## Changed downstream ? offer upstream

| Changed | Offer upstream | Skills |
| --- | --- | --- |
| **Production code** | Acceptance tests, Class Model | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md`, `skills/domain-driven-design/abd-domain-implementation/SKILL.md` |
| **Acceptance tests** or **Class Model** | Spec by Example, domain model | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md`, `skills/domain-driven-design/abd-domain-model/SKILL.md` |
| **Spec by Example** or **domain model** | Acceptance Criteria, Domain Language | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md`, `skills/domain-driven-design/abd-domain-language/SKILL.md` |
| **Acceptance Criteria** or **Domain Language** | Story Map, Domain Language, Key Abstractions | `skills/story-driven-delivery/abd-story-mapping/SKILL.md`, `skills/domain-driven-design/abd-domain-language/SKILL.md`, `skills/domain-driven-design/abd-key-abstractions/SKILL.md` |

## Changed on one side of a level ? offer the other side

| Changed | Offer peer | Skills |
| --- | --- | --- |
| **Acceptance tests** | Class Model | `skills/domain-driven-design/abd-domain-implementation/SKILL.md` |
| **Class Model** | Acceptance tests | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md` |
| **Spec by Example** | domain model | `skills/domain-driven-design/abd-domain-model/SKILL.md` |
| **domain model** | Spec by Example | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md` |
| **Acceptance Criteria** | Domain Language | `skills/domain-driven-design/abd-domain-language/SKILL.md` |
| **Domain Language** | Acceptance Criteria | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md` |
| **Story Map** | Domain Language, Key Abstractions | `skills/domain-driven-design/abd-domain-language/SKILL.md`, `skills/domain-driven-design/abd-key-abstractions/SKILL.md` |
| **Domain Language** or **Key Abstractions** | Story Map | `skills/story-driven-delivery/abd-story-mapping/SKILL.md` |

## Changed upstream ? offer downstream

| Changed | Offer downstream | Skills |
| --- | --- | --- |
| **Story Map**, **Domain Language**, or **Key Abstractions** | Acceptance Criteria, Domain Language | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md`, `skills/domain-driven-design/abd-domain-language/SKILL.md` |
| **Acceptance Criteria** or **Domain Language** | Spec by Example, domain model | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md`, `skills/domain-driven-design/abd-domain-model/SKILL.md` |
| **Spec by Example** or **domain model** | Acceptance tests, Class Model | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md`, `skills/domain-driven-design/abd-domain-implementation/SKILL.md` |
| **Acceptance tests** or **Class Model** | Production code | `architecture-centric-engineering/skills/abd-clean-code/SKILL.md` |
