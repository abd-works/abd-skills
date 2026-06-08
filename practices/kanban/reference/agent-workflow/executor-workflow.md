# Executor workflow

The app provides your context: workspace, ticket, stage, and skill to run. You execute and signal done — a separate reviewer agent (same delivery role) validates your output.

### Step 1 — Identify the skill

Read the ticket and stage to confirm which skill to run. Announce: ticket ID, stage, skill name.

### Step 2 — Sync with workspace

Scan for existing artifacts per [artifact-layout.md](./artifact-layout.md). Before creating a file, search for the canonical path and update in place rather than creating a duplicate.

### Step 3 — Read practice skill

Read the assigned practice skill's `SKILL.md` and bundled **rules** — templates, vocabulary, formatting, quality bar. Announce that rules were loaded.

### Step 4 — Produce draft

Produce the deliverable per [artifact-layout.md](./artifact-layout.md). Integrate as sections — no sprint/story/scenario files.

**CHECKPOINT.** Present draft summary and unknowns. Wait for confirm before Step 5.

### Step 5 — Update story graph (mandatory for story skills)

Sync structured content into `story-graph.json`. Markdown alone is insufficient — scanners and downstream skills read the graph.

| Skill | What to sync |
| --- | --- |
| `abd-story-mapping` | Epics, sub-epics, stories |
| `abd-thin-slicing` | Slice assignments |
| `abd-acceptance-criteria` | `acceptance_criteria[]` on every in-scope story — must be non-empty |
| `abd-specification-by-example` | `scenarios[]` / `scenario_outlines[]` on matched stories |
| All other skills | Skip unless stories were renamed or split |

**DO NOT** signal complete for AC or spec-by-example while graph arrays for in-scope stories are still empty.

### Step 5b — Queue Draw.io refresh (non-blocking)

When the completed skill appears in the [drawio sync trigger table](drawio-sync-background.md), queue a background render — do not await before Steps 6–7.

### Step 6 — Signal execution complete

Signal to the app that execution is done. The app assigns a **separate reviewer agent** (same delivery role) who runs `reviewer-workflow.md`. Do not self-review.

### Step 7 — Signal done

Signal review complete to the app. The app handles next skill assignment.

**When blocked:** note the blocker — kanban lead handles in scan cycle.
