---
description: >-
  Sync upstream artifacts after a downstream change. Use when code, tests,
  specs, or AC have changed and higher-level docs may be out of date.
mode: agent
---

An artifact has changed. Ask the user whether to sync in both directions. Only offer levels whose artifacts exist. Stop at each level if the user says no.

## Changed downstream → offer upstream

| Changed | Offer upstream | Skills |
| --- | --- | --- |
| **Production code** | Acceptance tests, Object model | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md`, `skills/domain-driven-design/abd-object-model/SKILL.md` |
| **Acceptance tests** or **Object model** | Spec by Example, CRC | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md`, `skills/domain-driven-design/abd-class-responsibility-collaborator/SKILL.md` |
| **Spec by Example** or **CRC** | Acceptance Criteria, Ubiquitous Language | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md`, `skills/domain-driven-design/abd-ubiquitous-language/SKILL.md` |
| **Acceptance Criteria** or **Ubiquitous Language** | Story Map, Domain Language, Key Abstractions | `skills/story-driven-delivery/abd-story-mapping/SKILL.md`, `skills/domain-driven-design/abd-domain-language/SKILL.md`, `skills/domain-driven-design/abd-key-abstractions/SKILL.md` |

## Changed on one side of a level → offer the other side

| Changed | Offer peer | Skills |
| --- | --- | --- |
| **Acceptance tests** | Object model | `skills/domain-driven-design/abd-object-model/SKILL.md` |
| **Object model** | Acceptance tests | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md` |
| **Spec by Example** | CRC | `skills/domain-driven-design/abd-class-responsibility-collaborator/SKILL.md` |
| **CRC** | Spec by Example | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md` |
| **Acceptance Criteria** | Ubiquitous Language | `skills/domain-driven-design/abd-ubiquitous-language/SKILL.md` |
| **Ubiquitous Language** | Acceptance Criteria | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md` |
| **Story Map** | Domain Language, Key Abstractions | `skills/domain-driven-design/abd-domain-language/SKILL.md`, `skills/domain-driven-design/abd-key-abstractions/SKILL.md` |
| **Domain Language** or **Key Abstractions** | Story Map | `skills/story-driven-delivery/abd-story-mapping/SKILL.md` |

## Changed upstream → offer downstream

| Changed | Offer downstream | Skills |
| --- | --- | --- |
| **Story Map**, **Domain Language**, or **Key Abstractions** | Acceptance Criteria, Ubiquitous Language | `skills/story-driven-delivery/abd-acceptance-criteria/SKILL.md`, `skills/domain-driven-design/abd-ubiquitous-language/SKILL.md` |
| **Acceptance Criteria** or **Ubiquitous Language** | Spec by Example, CRC | `skills/story-driven-delivery/abd-specification-by-example/SKILL.md`, `skills/domain-driven-design/abd-class-responsibility-collaborator/SKILL.md` |
| **Spec by Example** or **CRC** | Acceptance tests, Object model | `skills/story-driven-delivery/abd-acceptance-test-driven-development/SKILL.md`, `skills/domain-driven-design/abd-object-model/SKILL.md` |
| **Acceptance tests** or **Object model** | Production code | `skills/engineering/abd-clean-code/SKILL.md` |
