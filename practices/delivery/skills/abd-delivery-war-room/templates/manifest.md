# War Room Manifest

```yaml
goal: "<one-line engagement goal>"
profile: greenfield | brownfield | small-build | feature | bespoke
autonomy: tight | moderate | full
checkpoint_policy: after_every_slot | after_every_run | on_block_only
scanner_infra_policy: block_chain_until_fixed
scanner_exception_policy: documented_obvious_irrelevance_only
runtime: isolated-subagent
role_agents_bootstrapped: false   # lead sets true after eight agents spawned once
kanban:
  board_file: board.json
  columns: [backlog, in_progress, review, done, blocked, stalled]
  stage_flow: [in_progress, review, done]
  sync_script: delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py
cross_run_pipeline:
  next_run_opens_after: prior_run_specification_exit   # NOT prior_run_engineering_exit
  parallel_while_prior_run_engineering: true
  upstream_roles: [business-expert, product-owner]
wip_policy:
  # Total concurrent agents per role across ALL stages (Model B — role-based pools, not stage-locked).
  # Agents self-direct to the highest-priority eligible slot (downstream-first).
  # Delivery lead scan loop reads this every scan_interval_seconds and spawns/removes agents to match.
  product-owner:    { executor: 1, reviewer: 1 }
  business-expert:  { executor: 1, reviewer: 1 }
  ux-designer:      { executor: 1, reviewer: 1 }
  engineer:         { executor: 1, reviewer: 1 }
  scan_interval_seconds: 10
run_sizing_policy:
  stories_per_slot: 2
  stages_per_run: 1
  stall_timeout_minutes: 15
  notification_detail: high
```

## Slots

Full schedule — written to `slot-NN-start.md` at plan approval. Each row includes `depends_on` for pipeline ordering.

```yaml
slots:
  - id: "01"
    run: "Run 1 — <run name>"
    stage: shaping | discovery | exploration | specification | engineering
    slot_type: executor | reviewer
    role: product-owner | business-expert | ux-designer | engineer
    depends_on: ["00"]          # optional — prior slot ids
    prior_executor_slot: "01" # reviewer rows only
    skills:
      - <practice-skill-name>
    expected_artifacts:
      - <artifact-path>
    entry_conditions:
      - <precondition from stages/<stage>.md>
    early_question_triggers:
      - <trigger-name>
```

## Notes

- Delivery lead writes **all** slot start files when the plan is approved; role agents pull from **`board.json`**.
- **Progress:** `board.json` + `delivery-plan-checklist.md` + `slot-NN-finished.md` + optional `slot-NN-claim.md`.
- Run **`sync_kanban_board.py`** after slot/stage events — see `kanban` block above.
- Add **rework** executor slots when a reviewer fails; update `depends_on` on downstream slots if needed.
- Eight role agents (`product-owner`, `product-owner-reviewer`, …) run in parallel when dependencies allow.
- **Cross-run resume:** when active work is in engineering, author **next run** exploration+spec slot starts; wire first slot `depends_on` to prior run **spec exit** so PO/BE are not idle (see `cross_run_pipeline` above and `abd-delivery-planning` rule `cross-run-upstream-parallelism.md`).
