# Class diagram from `map-model-spec.json`

**When:** During **process phases 4–9** (terms & mechanisms through integrate), whenever you have **materially updated** the domain model in `**map-model-spec.json`**, re-run the generator so the class diagram file beside your spec stays aligned with promoted concepts, modules, and `**depends_on`**.

**Continual refinement:** The Draw.io file is the **diagram half** of the same loop described in [domain-model.md](domain-model.md) → **Continual refinement — class definition + diagram**. As you add or tighten **properties**, **operations**, and **relationships** in the spec (and tag **`**newly added**`** in prose when useful), **re-render** so reviewers compare **code + diagram + narrative** in one pass. Do **not** treat the diagram as a one-time export at the end of Integrate unless the model truly did not change after that point.

---

## Command (skill package)

From the **abd-maps-models-specs** root (directory that contains `scripts/` and `skill-config.json`), with `**skill-config.json`** pointing at the workspace that contains `**solution.conf`**:

```bash
python scripts/render_map_model_class_diagram.py
```

- **Input:** `<output_dir>/map-model-spec.json` (see `[domain-model.md](domain-model.md)` and your workspace `solution.conf`).
- **Output:** `<output_dir>/map-model-class-diagram.drawio` — **native diagrams.net XML** (same `**mxfile` / `mxCell`** shape as agile_bots story-map Draw.io), with modules, concepts, members, and `**depends_on`** edges. Emitter lives in this skill: `**scripts/map_model_spec_drawio.py**` (keep in sync with `**agile_bots**` `synchronizers.story_io.map_model_spec_drawio` when changing output).

**Prerequisite:** `skill-config.json` must set `**active_skill_workspace`** (workspace with `**solution.conf`**) — same as other skill scripts.

### Optional layout plan (logical, not pixels)

- **`map-model-spec.json`** remains the **source of truth** for classes, members, and edges.
- Optionally add **`<output_dir>/class-diagram-layout-plan.json`** — **clusters** and **order** only (`schema_version`: `1`). The emitter turns that into x/y (padding, column width, gaps). If the file is missing or invalid, layout falls back to **inheritance tiers + grid** (previous behavior).
- JSON Schema: `**schemas/class-diagram-layout-plan.schema.json**`. Minimal example: `**examples/class-diagram-layout-plan-minimal.json**`.
- **Render CLI:** if `class-diagram-layout-plan.json` exists under `<output_dir>`, it is picked up automatically. Use `--no-layout-plan` to force tier+grid only, or `--layout-plan path/to/file.json` to point at a specific file.

Optional path override:

```bash
python scripts/render_map_model_class_diagram.py --out path/to/custom-name.drawio
```

Re-running the command **replaces** the `.drawio` file. Manual edits in diagrams.net are **not** merged back into the layout-plan JSON; re-publish the JSON when you want the next render to follow a new logical layout.

---

## Open in diagrams.net

Open `**map-model-class-diagram.drawio`** in VS Code (Draw.io extension), diagrams.net desktop, or **app.diagrams.net** → **File → Open from…**. The file is native Draw.io XML (editable shapes).

---

