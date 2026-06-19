---
description: >-
  Sync generated delivery artifacts after a change. Use when code, tests,
  specs, or AC have changed and peer, upstream, or downstream docs may be out of date.
agent: agent
---

An artifact has changed. Use `AskQuestion` to ask the user which directions to sync. Only offer levels whose artifacts exist in the workspace. Stop at each level if the user says no.

## Step 1 — Ask which direction to sync

Use `AskQuestion` to ask:

```
What do you want to sync?
- Upstream  (propagate change upward to higher-level artifacts)
- Downstream  (propagate change downward to lower-level artifacts)
- Peer  (sync the artifact at the same level)
- All directions
```

## Step 2 — Determine available artifacts from skills

Before asking anything, scan the workspace for which skill directories exist under `.github/skills/` (or `../skills/`). Use that to build the list of available artifacts — only include an artifact if its corresponding skill folder is present:

| Skill folder | Artifact |
| --- | --- |
| `abd-story-acceptance-test` | Acceptance tests |
| `abd-domain-specification` | Class Model |
| `abd-story-specification` | Spec by Example |
| `abd-domain-model` | Domain Model |
| `abd-story-acceptance-criteria` | Acceptance Criteria |
| `abd-domain-sketch` | Domain Sketch |
| `abd-story-mapping` | Story Map |
| `abd-domain-language` | Domain Language |
| `abd-key-abstractions` | Key Abstractions |
| `abd-clean-code` | Production code |

Then use `AskQuestion` to ask the user which of the **available** artifacts they want to sync, offering only what was found.

## Step 3 — Execute

For each direction the user approves, invoke the relevant skill and stop if the user declines.

## Sync map

### Downstream changed → offer upstream

| Changed | Offer upstream | Skills |
| --- | --- | --- |
| Production code | Acceptance tests, Class Model | `abd-story-acceptance-test`, `abd-domain-specification` |
| Acceptance tests or Class Model | Spec by Example, Domain Model | `abd-story-specification`, `abd-domain-model` |
| Spec by Example or Domain Model | Acceptance Criteria, Domain Sketch | `abd-story-acceptance-criteria`, `abd-domain-sketch` |
| Acceptance Criteria or Domain Sketch | Story Map, Domain Language, Key Abstractions | `abd-story-mapping`, `abd-domain-language`, `abd-key-abstractions` |

### One side changed → offer peer

| Changed | Offer peer | Skills |
| --- | --- | --- |
| Acceptance tests | Class Model | `abd-domain-specification` |
| Class Model | Acceptance tests | `abd-story-acceptance-test` |
| Spec by Example | Domain Model | `abd-domain-model` |
| Domain Model | Spec by Example | `abd-story-specification` |
| Acceptance Criteria | Domain Sketch | `abd-domain-sketch` |
| Domain Sketch | Acceptance Criteria | `abd-story-acceptance-criteria` |
| Story Map | Domain Language, Key Abstractions | `abd-domain-language`, `abd-key-abstractions` |
| Domain Language or Key Abstractions | Story Map | `abd-story-mapping` |

### Upstream changed → offer downstream

| Changed | Offer downstream | Skills |
| --- | --- | --- |
| Story Map, Domain Language, or Key Abstractions | Acceptance Criteria, Domain Sketch | `abd-story-acceptance-criteria`, `abd-domain-sketch` |
| Acceptance Criteria or Domain Sketch | Spec by Example, Domain Model | `abd-story-specification`, `abd-domain-model` |
| Spec by Example or Domain Model | Acceptance tests, Class Model | `abd-story-acceptance-test`, `abd-domain-specification` |
| Acceptance tests or Class Model | Production code | `abd-clean-code` |
