# Slot NN — Start

```yaml
team-role: product-owner | business-expert | ux-designer | engineer
slot_type: executor | reviewer
workspace: <absolute path to engagement root>
run: "Run N — <increment name>"   # work ticket — one Kanban column per run at a time
ticket_run: N                     # optional numeric run id for board.json sync
stage: shaping | discovery | exploration | specification | engineering
depends_on:                 # slot ids that must have finished.md before this slot is claimable
  - "04"                    # Run N+1 first exploration: prior RUN spec exit, NOT prior run eng exit
run_scope: <exact story ids or slice id — executor only; never qualitative>
skills:
  - <practice-skill-name>   # executor: one primary skill per pair; reviewer: same skill as paired executor
prior_executor_slot: <NN>   # reviewer only — executor slot being reviewed
artifact_paths:             # reviewer only — from executor finished file (may be filled when executor completes)
  - <workspace-relative path>
corrections: docs/corrections-log.md — filter by Affects for this stage and scope
checkpoint: after_slot | mid_slot | none
entry_conditions_met:
  - <verified precondition from stages/<stage>.md>
early_questions:
  - <trigger-name>: <condition — STOP and write blocked.md if triggered>
```

**Reviewer slots:** `team-role` is the **same role as the executor** under review (e.g. `product-owner`), not a generic `reviewer`. `slot_type: reviewer`. `depends_on` must include `prior_executor_slot`.

## Context

- Upstream artifacts: <paths from prior stages or depends_on slots>
- Decisions from prior stages: <key decisions or constraints>
- Open questions: <unresolved items>

## Filtered corrections

<Paste relevant entries from docs/corrections-log.md filtered by Affects for this stage/role/scope.>
