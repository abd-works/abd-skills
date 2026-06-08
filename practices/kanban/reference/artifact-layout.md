# Artifact layout — canonical paths

**Source of truth** for where delivery agents write artifacts. Read this on every skill claim **before** producing output.

Practice skills may define their own default paths — **kanban layout wins** when running under the delivery kanban board unless the user names an explicit override.

---

## Top-level structure

```text
<workspace>/docs/
  end-to-end/                    # Whole solution — one subfolder per stage
    shaping/                     # flat
    discovery/
      domain/
      stories/
      ux/
      architecture/
    exploration/                 # filled when increments roll up
      domain/
      stories/
      ux/
      architecture/
    specification/               # flat
    engineering/                 # flat
  increments/                    # Per-increment working area (exploration ? engineering only)
    <n>-<slug>/                  # e.g. 8-marketing-engine
      exploration/
        domain/
        stories/
        ux/
        architecture/
      specification/             # flat
      engineering/               # flat
  planning/delivery-kanban-board/
```

| Stage | Write during delivery | Whole-solution canonical |
| --- | --- | --- |
| **Shaping** | `docs/end-to-end/shaping/` | same — filled directly |
| **Discovery** | `docs/end-to-end/discovery/` | same — filled directly |
| **Exploration** | `docs/increments/<n>-<slug>/exploration/` | `docs/end-to-end/exploration/` — merge when increment done |
| **Specification** | `docs/increments/<n>-<slug>/specification/` | `docs/end-to-end/specification/` — merge when increment done |
| **Engineering** | `docs/increments/<n>-<slug>/engineering/` (+ `src/` code) | `docs/end-to-end/engineering/` — merge when increment done |

### Increment folder naming (mandatory)

**Format:** `<n>-<slug>` — increment number, hyphen, kebab-case slug from the **marketable increment name** in `docs/end-to-end/discovery/stories/thin-slicing.md`.

| Rule | Detail |
| --- | --- |
| **DO** | `8-marketing-engine`, `1-walk-in-driver`, `9-power-ups` |
| **DO NOT** | `increment-8`, `increment-1`, bare number only |
| **Slug source** | First phrase of the increment title in thin-slicing — lowercase, spaces ? hyphens, drop punctuation |
| **Resolve from ticket** | Ticket lineage gives increment number; read matching title from `thin-slicing.md` for slug |

Example: Increment 8 *Marketing engine — reviews, alerts, and content* ? `docs/increments/8-marketing-engine/`.

Kanban lead creates `docs/increments/<n>-<slug>/` when scattering increment tickets from thin-slicing.

**DO NOT** use legacy paths (`docs/shaping/`, `docs/discovery/`, `docs/domain/`, `docs/story/`, `increment-<n>/`, etc.) outside this layout.

---

## End-to-end — stage subfolders

`docs/end-to-end/` has **exactly five stage subfolders** — one per delivery stage.

- **`shaping/`**, **`specification/`**, **`engineering/`** — files are **flat** inside each subfolder (no family subfolders).
- **`discovery/`** and **`exploration/`** — organized by concern in **four subfolders**: `stories/`, `architecture/`, `ux/`, `domain/`. Increment number is in the folder path (`increments/<n>-<slug>/`), not in filenames.

- **`shaping/`** and **`discovery/`** — agents write here **during** those stages.
- **`exploration/`**, **`specification/`**, **`engineering/`** — start empty; **filled as increments complete** (kanban lead merges from `docs/increments/<n>-<slug>/` into the matching end-to-end stage folder).

### end-to-end/shaping/ (write directly)

| Skill | File(s) |
| --- | --- |
| `abd-domain-glossary` | `domain/domain-glossary.md` (single file, default) or `domain/domain-glossary/<module>.md` (per-module, large systems) |
| `abd-bounded-context-map` | `bounded-context-map.md` (+ `.drawio`) |
| `abd-story-mapping` (outline) | `story-graph.json`, `story-map.md` |
| `abd-opportunity-generation` | `opportunity-canvas.md` |
| `abd-impact-mapping` | `impact-map.md` |
| `abd-architecture-outline` | `architecture-outline.md` (+ `.drawio`) |

### end-to-end/discovery/ (write directly — four concern subfolders)

```text
docs/end-to-end/discovery/
  stories/       # story map, graph, thin slicing
  architecture/  # blueprint, SLOs, ADRs, entity diagrams
  ux/            # information architecture
  domain/        # domain terms
```

| Subfolder | Skill | File(s) |
| --- | --- | --- |
| **`domain/`** | *(domain terms produced during Shaping by `abd-domain-glossary`)* | — |
| **`stories/`** | `abd-story-mapping` (full) | `story-graph.json`, `story-map.md` (+ `.drawio`) |
| **`stories/`** | `abd-thin-slicing` | `thin-slicing.md` (+ `.drawio`, `.txt`) |
| **`stories/`** | `drawio-story-sync` | `thin-slicing.drawio` (increments diagram) |
| **`ux/`** | `abd-information-architecture` | `information-architecture.md`, `information-architecture.drawio` |
| **`architecture/`** | `abd-architecture-blueprint` | `architecture-blueprint.md` (+ diagram) |
| **`architecture/`** | `abd-service-level-objectives` | `service-level-objectives.md` |
| **`architecture/`** | ADRs | `ADR-*.md` |

`docs/end-to-end/discovery/stories/story-graph.json` is the **whole-solution** canonical graph (shaping outline may start in `shaping/story-graph.json` then discovery owns the full graph).

### end-to-end/exploration/ (filled from increment roll-up — four concern subfolders)

```text
docs/end-to-end/exploration/
  domain/        # Domain Language
  stories/       # acceptance criteria
  ux/            # mockups, wireframe .drawio, *-state.json
  architecture/  # architecture mechanism templates
```

| Subfolder | Skill | File(s) |
| --- | --- | --- |
| **`domain/`** | `abd-domain-language` | `domain-language.md` (+ `.drawio`) |
| **`stories/`** | `abd-acceptance-criteria` | `acceptance-criteria.md` (+ `.drawio`) |
| **`ux/`** | `abd-ux-mockup` | `mockups.md`, screen `*.drawio`, `*-state.json` |
| **`architecture/`** | `abd-architecture-specification` | `architecture-template.md` |

Merge increment exploration content into the matching subfolder when increment exploration work is done.

### end-to-end/specification/ (filled from increment roll-up)

| File | Content |
| --- | --- |
| `domain model.md`, `domain.json` | **One** whole-solution domain model |
| `specification-by-example.md` | **One** whole-solution spec file |
| `interface-design.md` | **One** whole-solution interface spec |
| `architecture-reference.md`, `architecture-reference-assignment.md` | Whole-solution arch reference |

### end-to-end/engineering/ (filled from increment roll-up)

| File | Content |
| --- | --- |
| `class-model.md` | **One** whole-solution Class Model doc |

Production code and tests live in **`src/`** per architecture reference — not under `end-to-end/engineering/`.

---

## Increments — working folder

Active increment work (exploration ? engineering only) writes to **`docs/increments/<n>-<slug>/`**. **`specification/`** and **`engineering/`** are flat; **`exploration/`** uses the same four concern subfolders as end-to-end exploration.

```text
docs/increments/8-marketing-engine/
  exploration/
    domain/
    stories/
    ux/
    architecture/
  specification/
  engineering/
```

### Increment integration rule (mandatory)

**One canonical file per artifact type per increment stage folder.** Sprint/story scope ? **section inside that file**, never a new file.

| Forbidden | Use instead |
| --- | --- |
| `*-sprint-*`, `*-story-*`, `*-scenario-*` in filename | Section in stage canonical file |
| Family subfolders under **`specification/`** or **`engineering/`** | Stage subfolder only — flat files |
| `increment-<n>/` folder names | `<n>-<slug>/` from thin-slicing |

#### increments/…/exploration/ (four concern subfolders — same as end-to-end)

| Subfolder | Skill | File(s) |
| --- | --- | --- |
| **`domain/`** | `abd-domain-language` | `domain-language.md` (+ `.drawio`) |
| **`stories/`** | `abd-acceptance-criteria` | `acceptance-criteria.md` (+ `.drawio`) |
| **`ux/`** | `abd-ux-mockup` | `mockups.md`, screen `*.drawio`, `*-state.json` |
| **`architecture/`** | `abd-architecture-specification` | `architecture-template.md` |

#### increments/…/specification/

| Skill | File(s) |
| --- | --- |
| `abd-domain-model` | `domain model.md`, `domain.json` |
| `abd-specification-by-example` | `specification-by-example.md` |
| `abd-ux-specification` (spec pass) | `interface-design.md` |
| `abd-architecture-specification` | `architecture-reference.md`, `architecture-reference-assignment.md` |

#### increments/…/engineering/

| Skill | File(s) |
| --- | --- |
| `abd-domain-specification` | `class-model.md` |
| `abd-domain-code` | `src/` (domain classes + tests, TDD) |
| ATDD, clean-code, interface impl | `src/` |

### Story graph — canonical structured store (mandatory sync)

`docs/end-to-end/discovery/stories/story-graph.json` is the **structured source of truth** for story structure, **`acceptance_criteria`**, and **`scenarios`**. Markdown files (`acceptance-criteria.md`, `specification-by-example.md`) are human-readable deliverables; **they are not a substitute for the graph**.

| Skill | Markdown deliverable | **Also required** — sync into `story-graph.json` |
| --- | --- | --- |
| `abd-story-mapping` | `story-map.md` | `md_story_map_to_story_graph.py` (create or replace skeleton) |
| `abd-thin-slicing` | `thin-slicing.md` | `md_thin_slice_to_story_graph.py` (increments array) |
| `abd-acceptance-criteria` | `acceptance-criteria.md` | `md_acceptance_criteria_to_story_graph.py` ? `acceptance_criteria[]` on matched stories |
| `abd-specification-by-example` | `specification-by-example.md` | `scenarios[]` / `scenario_outlines[]` on matched stories via **story-graph-ops** (`story_graph_cli.py` write or patch — no md parser yet) |

**When:** immediately after Step 4 (draft) and before Step 6 (review) in [executor-workflow.md](../reference/agent-workflow/executor-workflow.md). Run from engagement root:

```bash
python skills/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py \
  docs/increments/<n>-<slug>/exploration/stories/acceptance-criteria.md \
  docs/end-to-end/discovery/stories/story-graph.json
```

Then validate: `python skills/story-graph-ops/scripts/story_graph_cli.py read --file docs/end-to-end/discovery/stories/story-graph.json`

**DO NOT** mark `abd-acceptance-criteria` or `abd-specification-by-example` done on the board while in-scope stories still have empty `acceptance_criteria` or `scenarios` in the graph.

Kanban lead: on increment roll-up, verify graph populated for that increment's stories before archiving the last ticket.

**Draw.io:** After graph/markdown sync, queue **`drawio-story-sync`** / **`drawio-domain-sync`** as **background tasks** — see [drawio-sync-background.md](../reference/agent-workflow/drawio-sync-background.md). Do not block the executor on render completion.

---

## Increment complete — merge into end-to-end stage folder

When **every ticket** for increment `<n>` (`<n>-<slug>`) is archived, **kanban lead** merges each increment stage folder into the **matching end-to-end stage folder** — append sections (`## Increment <n>: <title>`); integrate into existing canonical files.

| Increment source | Merge into |
| --- | --- |
| `increments/<n>-<slug>/exploration/domain/*` | `docs/end-to-end/exploration/domain/` |
| `increments/<n>-<slug>/exploration/stories/*` | `docs/end-to-end/exploration/stories/` |
| `increments/<n>-<slug>/exploration/ux/*` | `docs/end-to-end/exploration/ux/` |
| `increments/<n>-<slug>/exploration/architecture/*` | `docs/end-to-end/exploration/architecture/` |
| `increments/<n>-<slug>/specification/*` | `docs/end-to-end/specification/` |
| `increments/<n>-<slug>/engineering/*` | `docs/end-to-end/engineering/` |
| Graph updates | `docs/end-to-end/discovery/stories/story-graph.json` |

Log: `{"event":"increment_rollup","increment":"<n>-<slug>","timestamp":"..."}` in `metrics-log.jsonl`.

After roll-up, **`docs/end-to-end/<stage>/`** is authoritative for the whole solution at that stage. Increment folders remain as history.

---

## kanban board

```text
<workspace>/docs/kanban/
  board.json · kanban.json · metrics-log.jsonl · INSTRUCTIONS.md · heartbeat-*.json
```

**Handoffs** (`abd-kanban-handoff` / `/abd-kanban-handoff`):

```text
<workspace>/docs/kanban/handoffs/
  handoff-latest.md
  handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md
```

---

## Agent checklist (before write)

1. Read ticket **stage** and **increment** from `board.json`.
2. **Shaping** ? `docs/end-to-end/shaping/`. **Discovery** ? `docs/end-to-end/discovery/`.
3. **Exploration / specification / engineering** ? resolve `<n>-<slug>` from ticket + `discovery/stories/thin-slicing.md`. **Exploration** ? `docs/increments/<n>-<slug>/exploration/{domain,stories,ux,architecture}/`. **Specification / engineering** ? flat inside stage folder.
4. One canonical file per type per folder — add sections; never sprint/story/scenario siblings.
5. **Increment archived** ? kanban lead merges increment stage folder ? matching `docs/end-to-end/<stage>/`.


