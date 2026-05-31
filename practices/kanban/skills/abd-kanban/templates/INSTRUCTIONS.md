# War room — agent bootstrap

**Read first (mandatory):**

1. [session-bootstrap.md](../../agents/reference/session-bootstrap.md)
2. [pull-model.md](../../agents/reference/pull-model.md)
3. [artifact-layout.md](../../reference/artifact-layout.md)

## Artifact paths (summary)

```text
docs/end-to-end/
  shaping/                    ← flat
  discovery/                  ← domain/, stories/, ux/, architecture/
  exploration/                ← same four subfolders (rolled up from increments)
  specification/              ← flat
  engineering/                ← flat
docs/increments/<n>-<slug>/   ← e.g. 8-marketing-engine
  exploration/                ← domain/, stories/, ux/, architecture/
  specification/              ← flat
  engineering/                ← flat
```

- Shaping → `end-to-end/shaping/`. Discovery → `end-to-end/discovery/{domain,stories,ux,architecture}/`.
- Active increment → `increments/<n>-<slug>/`; exploration uses the same four subfolders.
- Increment archived → kanban lead merges into matching `end-to-end/<stage>/` (per subfolder for exploration).
- Story graph: `end-to-end/discovery/stories/story-graph.json`. Increment names: `discovery/stories/thin-slicing.md`.

## Pull rules (summary)

- **Delivery roles:** Arm `AGENT_LOOP_TICK_<role>` on turn 1; pull all stages downstream-first; never exit after one skill.
- **Kanban lead:** Arm tick loop; scan; scatter; roll up completed increments; spawn executors. No reviewer agents.

## War room paths

| File | Purpose |
| --- | --- |
| `board.json` | Tickets, skill_progress |
| `kanban.json` | Stages, stage work required, team |
| `metrics-log.jsonl` | `agent_ready`, `increment_rollup`, … |
| `heartbeat-*.json` | Liveness |
