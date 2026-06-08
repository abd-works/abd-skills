---
rule_id: scenario-walkthrough-update-spec-on-gap
---

## Scenario walkthrough: update the spec when the walk finds a gap

If the walkthrough reveals a **missing `depends_on`**, wrong responsibility, or evidence hole **and** the team agrees it is in scope, **update `map-model-spec.json`** (and **`chunk_id` citations** per contract) before treating Deepen as done for that slice. Do not leave the fix only in walkthrough prose.

**DO**

- File a short **Gaps** section in the walkthrough, then either patch the spec or record an explicit deferral in **`open_questions`** / queue.

**DON'T**

- Close Deepen with walkthrough-only text that contradicts the spec without reconciling.
