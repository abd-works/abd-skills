# Sync Generated Artifacts (always-on)

Apply this rule whenever you change any generated delivery artifact.

## Core rule

After changing an artifact, offer synchronization in both directions:

1. **Peer sync** (other artifact at same level)
2. **Upstream sync** (higher-level artifacts)
3. **Downstream sync** (lower-level artifacts)

Only offer targets that exist in the current workspace.  
If the user declines at a level, stop at that level.

## Required interaction

Always ask explicitly before performing sync:

```text
I updated <artifact>. Do you want me to sync:
1) peer artifacts,
2) upstream artifacts,
3) downstream artifacts?
```

If user says no, do not auto-sync anything.

## Sync map

### Downstream changed -> offer upstream

| Changed artifact | Offer sync to | Skills |
| --- | --- | --- |
| Production code | Acceptance tests, domain specification | `abd-story-acceptance-test`, `abd-domain-specification` |
| Acceptance tests or domain specification | Spec by Example, Domain Model | `abd-story-specification`, `abd-domain-model` |
| Spec by Example or Domain Model | Acceptance Criteria, Domain Sketch | `abd-story-acceptance-criteria`, `abd-domain-sketch` |
| Acceptance Criteria or Domain Sketch | Story Map, Domain Language, Key Abstractions | `abd-story-mapping`, `abd-domain-language`, `abd-key-abstractions` |

### One side changed -> offer peer

| Changed artifact | Offer sync to peer | Skills |
| --- | --- | --- |
| Acceptance tests | domain specification | `abd-domain-specification` |
| domain specification | Acceptance tests | `abd-story-acceptance-test` |
| Spec by Example | Domain Model | `abd-domain-model` |
| Domain Model | Spec by Example | `abd-story-specification` |
| Acceptance Criteria | Domain Sketch | `abd-domain-sketch` |
| Domain Sketch | Acceptance Criteria | `abd-story-acceptance-criteria` |
| Story Map | Domain Language, Key Abstractions | `abd-domain-language`, `abd-key-abstractions` |
| Domain Language or Key Abstractions | Story Map | `abd-story-mapping` |

### Upstream changed -> offer downstream

| Changed artifact | Offer sync to | Skills |
| --- | --- | --- |
| Story Map, Domain Language, or Key Abstractions | Acceptance Criteria, Domain Sketch | `abd-story-acceptance-criteria`, `abd-domain-sketch` |
| Acceptance Criteria or Domain Sketch | Spec by Example, Domain Model | `abd-story-specification`, `abd-domain-model` |
| Spec by Example or Domain Model | Acceptance tests, domain specification | `abd-story-acceptance-test`, `abd-domain-specification` |
| Acceptance tests or domain specification | Production code | `abd-clean-code` |

## Do not apply this rule when

- The change is not part of the delivery artifact chain.
- The target artifact files do not exist and the user did not ask to create them.
- The user explicitly requests no synchronization.
