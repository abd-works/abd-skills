---
rule_id: epic-requires-confirming-stories
phases: [step1]
order: 30
scanner: mms_scan_epic_requires_confirming_stories.py
impact: HIGH
---

## Every epic must be confirmed by at least two story names

An epic with fewer than two confirming stories has not been sufficiently validated. The confirming stories are not the deliverable — they are the evidence that the epic describes a real, coherent functional area with independently testable behaviors underneath it.

The scanner (`mms_scan_epic_requires_confirming_stories.py`) highlights epics with fewer than two confirming stories. It does not determine what the missing stories should be — that judgment belongs to the AI.

**DO** include at least two story names in `confirming_stories` for every epic.

**DO** ensure each confirming story name describes a complete, independently testable behavior — not an implementation step.

**DO NOT** leave `confirming_stories` empty or with only one entry. An epic that cannot produce two story names is either too narrow (collapse it into another epic) or too vague (it has not been sufficiently understood yet — flag `[uncertain]`).
