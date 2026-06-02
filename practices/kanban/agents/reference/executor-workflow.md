# Agent workflow (execute + review in one pass)

**Shared kanban concepts**: [../../reference/kanban-board.md](../../reference/kanban-board.md) · [../../reference/agents-and-skills.md](../../reference/agents-and-skills.md)

Each agent executes **and** reviews in a single session — produce the deliverable, then validate it against the skill's rules and scanners. **No separate reviewer agents** — see [pull-model.md](pull-model.md).

## Step 0 — Session bootstrap + pull loop (mandatory first turn)

**Before Step 1**, read [session-bootstrap.md](session-bootstrap.md) and [pull-model.md](pull-model.md):

0. If `<workspace>/AGENT-SEED.md` exists → read it **first** (fixture mode team member executor).
1. Resolve `workspace` and war room paths.
2. **Arm `AGENT_LOOP_TICK_<delivery-role>`** pull loop with `notify_on_output`.
3. Write `heartbeat-<delivery-role>.json` with `status: working` and current ISO `ts`.
4. Read `board.json` and `kanban.json`.
5. Run pull scan — **all stages** in reverse order from `kanban.json`.

If no eligible skill → `agent_ready`, heartbeat `ready`, **keep pull loop armed**. Do not exit.

## Checkpoint protocol

When a step says **CHECKPOINT**:

1. **Present** state and flag unknowns.
2. **Stop** and wait.
3. **On response:** confirm → proceed · correct → log in `docs/corrections-log.md` per `execute-skill-using-skills-rules` **before** fixing · question → answer, re-present.

---

### Step 1 — Start skill from board (pull claim)

**Use `board_skill.py`** — do not hand-edit `board.json`:

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py pull \
  --workspace <workspace> --role <your-role> [--instance N]
```

Dry-run eligibility: add `--dry-run` to `pull`. If no claim, run `ready` (Step 7).

Announce: ticket ID, stage, skill name from CLI JSON output.

**Architecture skills:** Always run the full skill after claim. Inside the skill, choose **quick pass** (mapping document only) or **long pass** (create gaps) per [work-queue.md — Architecture skills](work-queue.md#architecture-skills). Kanban does not auto-skip before `in_progress`.

### Step 2 — Sync with workspace

Scan for existing artifacts per [artifact-layout.md](../../reference/artifact-layout.md) — `docs/end-to-end/<stage>/` (including concern subfolders under discovery and exploration), `docs/increments/<n>-<slug>/`, `docs/end-to-end/discovery/stories/story-graph.json`. Flag conflicts with ticket scope. **Before creating a file**, search for the canonical file in the correct stage folder and update in place.

### Step 3 — Read practice skill (authoring)

**Fixture mode:** If `<workspace>/CONTEXT.md` has `fixture_mode: true`, read [skill-fixture-mode.md](skill-fixture-mode.md) instead of this step through Step 6 — run `apply_skill_fixture.py apply` (or `apply-claim` after manual drop), then pull next. Skip checkpoint and scanners.

Read the assigned practice skill's `SKILL.md` and bundled **rules** — templates, vocabulary, formatting, quality bar for **building**.

The skill name comes from the kanban board's stage work required for the ticket's current stage.

Announce skill name and that rules were loaded for authoring.

### Step 4 — Produce draft

Produce the deliverable per [artifact-layout.md](../../reference/artifact-layout.md): `end-to-end/shaping/` or `end-to-end/discovery/` for those stages; `increments/<n>-<slug>/<stage>/` for increment work. Integrate as sections — no sprint/story/scenario files.

**CHECKPOINT.** Present draft summary and unknowns. Wait for confirm before Step 5.

### Step 5 — Update story graph (mandatory for story skills)

After checkpoint confirm, sync structured graph content into `docs/end-to-end/discovery/stories/story-graph.json`. **Markdown alone is insufficient** — scanners and downstream skills read the graph.

| Skill | Action |
| --- | --- |
| `abd-story-mapping` | `python skills/story-graph-ops/scripts/md_story_map_to_story_graph.py <story-map.md> <story-graph.json>` |
| `abd-thin-slicing` | `python skills/story-graph-ops/scripts/md_thin_slice_to_story_graph.py <thin-slicing.md> <story-graph.json>` |
| `abd-acceptance-criteria` | `python skills/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py <acceptance-criteria.md> <story-graph.json>` — every in-scope story must have non-empty `acceptance_criteria` |
| `abd-specification-by-example` | Merge `specification-by-example.md` scenarios into matched stories' `scenarios` / `scenario_outlines` via **story-graph-ops** (`story_graph_cli.py` — use `--expect-sha` on write). No md parser yet; do not skip. |
| All other skills | Skip unless you renamed/split stories (then patch graph via story-graph-ops) |

Validate after sync: `python skills/story-graph-ops/scripts/story_graph_cli.py read --file docs/end-to-end/discovery/stories/story-graph.json`

**DO NOT** proceed to Step 7 (mark done) for AC or spec-by-example while graph arrays for in-scope stories are still empty.

### Step 5b — Queue Draw.io refresh (non-blocking)

When the completed skill appears in the [drawio sync trigger table](drawio-sync-background.md), **spawn a background render/sync** — **do not await** before Step 6 or Step 7.

| Parent skill | Background skill |
| --- | --- |
| `abd-story-mapping`, `abd-thin-slicing`, `abd-acceptance-criteria`, `abd-specification-by-example` | `drawio-story-sync` (`render` or `sync`) |
| `abd-domain-terms`, `abd-ubiquitous-language`, `abd-class-responsibility-collaborator`, `abd-object-model` | `drawio-domain-sync` (Task subagent) |

Log `drawio_sync_queued` to `metrics-log.jsonl`. See [drawio-sync-background.md](drawio-sync-background.md) for commands and paths.

### Step 6 — Review pass (same agent)

**Mark the work pass complete** so the board shows review (magnifying glass) while you validate:

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py complete \
  --workspace <workspace> --ticket <id> --skill <name> --role <your-role> [--instance N]
```

Expect JSON `"action": "work_done"` and `review_status: in_progress` on the ticket.

Switch hats — now **validate** the output you just produced:

1. Re-read the practice skill's `rules/` directory as the quality bar.
2. Run scanners if available — use **engagement root** as `--workspace` and pass canonical graph explicitly when the skill is graph-aware:

   ```bash
   python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
       --skill-root <skill-name> \
       --workspace <engagement-root>
   ```

   For `abd-acceptance-criteria` / `abd-specification-by-example`, ensure Step 5 graph sync ran first so graph-based scanners see populated arrays. Scanners discover `story-graph.json` via recursive search from workspace root.
3. Emit per-rule verdicts (PASS/FAIL with evidence).
4. **Simple issues** — fix them directly and re-run scanners. Do not mark FAIL for mechanical problems you can fix yourself.
5. **Substantive issues** — if the review reveals a real problem you cannot fix mechanically (wrong model, missing abstraction), log it in `docs/corrections-log.md` and flag to kanban lead.

### Step 7 — Mark review done and pull next

**Run `board_skill.py complete` again** (same ticket/skill/role) after review passes — do not hand-edit `board.json`:

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py complete \
  --workspace <workspace> --ticket <id> --skill <name> --role <your-role> \
  [--instance N] [--notes "..."]
```

Expect JSON `"action": "completed"` and both `execution_status` and `review_status` set to `done`.

Conditional skip:

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py skip \
  --workspace <workspace> --ticket <id> --skill <name> --role <your-role> [--notes "..."]
```

Then **pull again** via `board_skill.py pull`. If no work:

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py ready \
  --workspace <workspace> --role <your-role> [--instance N]
```

If work is found → continue at Step 1 **in the same session** (do not exit). Pull loop stays armed.

**When blocked:** add a note to the ticket — kanban lead handles in scan cycle.
