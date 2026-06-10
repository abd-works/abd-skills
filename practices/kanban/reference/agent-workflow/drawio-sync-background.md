# Draw.io sync — background tasks (non-blocking)

**Skills:** `drawio-story-sync` · `drawio-domain-sync` (read each `SKILL.md` before dispatch).

Diagram refresh is **downstream of** markdown/graph writes. It must **not** block the executor from Step 6 (scanners), Step 7 (mark done), or the pull loop.

---

## Rules

1. **Queue after Step 5** (story-graph sync when applicable) and **before** Step 6 — or immediately after Step 7 if the skill had no graph step.
2. **Never await** the render/sync subprocess in the executor session. Use **`block_until_ms: 0`** (shell) or **`Task` + `run_in_background: true`** (domain diagrams that need layout).
3. **Log every queue** to `docs/kanban/metrics-log.jsonl`:

   ```json
   {"event":"drawio_sync_queued","sync_skill":"drawio-story-sync","trigger_skill":"abd-story-acceptance-criteria","ticket_id":"<id>","paths":{"graph":"...","out":"..."},"timestamp":"<ISO 8601>"}
   ```

4. Parent skill **`execution_status: done`** does not depend on draw.io finishing. Failures are fixed on a later scan or a dedicated re-run — do not roll back the parent skill.
5. Resolve paths from [artifact-layout.md](../../reference/artifact-layout.md). Canonical graph: `docs/end-to-end/discovery/stories/story-graph.json`.

---

## Trigger table — `drawio-story-sync`

Run **`render`** (or **`sync`** when the user edited an outline `.drawio` and graph must catch up). All commands from engagement **`workspace`** root; PYTHONPATH must include `skills/drawio-story-sync/scripts` and `skills/story-graph-ops/scripts`.

| After parent skill | When | Command (background shell) |
| --- | --- | --- |
| `abd-story-mapping` (outline) | Graph + `story-map.md` written under `docs/end-to-end/shaping/` or `discovery/stories/` | `render --mode outline --graph <graph> --out <stories-folder>/story-map.drawio` |
| `abd-story-mapping` (full) | Same under `docs/end-to-end/discovery/stories/` | same |
| `abd-thin-slicing` | After `md_thin_slice_to_story_graph.py` | `render --mode thin-slicing --graph <graph> --out <stories-folder>/thin-slicing.drawio` |
| `abd-story-acceptance-criteria` | After `md_acceptance_criteria_to_story_graph.py` — graph must have AC | `render --mode acceptance-criteria --graph <graph> --out <stories-folder>/acceptance-criteria.drawio` |
| `abd-story-specification` | After scenarios merged into graph | `render --mode acceptance-criteria --graph <graph> --out <stories-folder>/acceptance-criteria.drawio` (refresh exploration diagram) |
| User / lead: outline `.drawio` edited | Graph must follow diagram | `sync --drawio <story-map.drawio> --graph <graph>` (refreshes acceptance-criteria + thin-slicing companions) |

**Increment tickets:** use the increment's `exploration/stories/` or `discovery/stories/` folder beside the canonical graph (graph path stays `docs/end-to-end/discovery/stories/story-graph.json`).

**Validate (background task responsibility, not executor):** after render, run `story_graph_cli.py read --file <graph>` if the command touched the graph (`sync` only).

---

## Trigger table — `drawio-domain-sync`

Domain diagrams are **page-per Key Abstraction**. Prefer a **background `Task` subagent** (read `drawio-domain-sync/SKILL.md`, render all KA pages) — do not block the claiming agent.

| After parent skill | Source model | Output (beside source) |
| --- | --- | --- |
| `abd-domain-glossary` | per-module files in `modules/` | optional `<name>-class-diagram.drawio` under same folder |
| `abd-domain-language` | `domain-language.md` | `domain-language-class-diagram.drawio` under `discovery/domain/` |
| `abd-domain-model` | `domain-model.md` | `domain-model-class-diagram.drawio` under `exploration/domain/` |
| `abd-domain-specification` | `class-model.md` | `class-model-class-diagram.drawio` under `specification/` |

Queue only when the source file changed in the current skill pass. Skip if the user waived diagrams.

---

## Dispatch patterns

### Story diagrams (CLI — background shell)

```powershell
# Executor: block_until_ms 0 — do not wait
$env:PYTHONPATH = "skills/drawio-story-sync/scripts;skills/story-graph-ops/scripts"
python skills/drawio-story-sync/scripts/drawio_story_sync_cli.py render `
  --mode acceptance-criteria `
  --graph docs/end-to-end/discovery/stories/story-graph.json `
  --out docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.drawio
```

### Domain diagrams (background Task subagent)

```text
Task run_in_background: true
Prompt: Read drawio-domain-sync/SKILL.md. Workspace: <root>.
Render/refresh class diagram for <source.md> ? <output.drawio>. Log errors to metrics-log.jsonl event drawio_sync_failed.
Do not update board.json.
```

---

## Kanban lead

On scan cycle: if `drawio_sync_failed` appears in `metrics-log.jsonl`, re-queue the matching background command. Do not spawn duplicate renders for the same `(trigger_skill, ticket_id, out path)` while `drawio_sync_queued` is newer than any failure for that triple.

---

## Agent checklist

- [ ] Parent markdown + graph sync complete (Step 5) before story `render`.
- [ ] Background job queued; executor continued to scanners / mark done.
- [ ] `drawio_sync_queued` logged with ticket id and paths.
- [ ] Did **not** hold the pull loop waiting for Draw.io.
