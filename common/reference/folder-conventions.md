# Folder Conventions

This file is the authoritative reference for **where every skill writes its deliverables** within a project workspace. All practice skills in the `abd-skills/practices` family follow these conventions by default. The user may override any path — skills always have first say on extra deliverable outputs and can override anything here.  Existng paths also take precedent.

The empty folder-and-file scaffold that mirrors this table lives at [`context-scaffold/`](./context-scaffold/). Use it as a starting-point skeleton when initialising a new workspace. ONLY create foldres just-in-time and when needed.

---

## Default output resolution (all skills)

All paths below are relative to **`<project>/`** — the project root within the workspace
(e.g. `pml-my/`, `pml-midtier/`). All deliverables live under `<project>/docs/` by default.

Skills resolve their deliverables folder in this order:

1. **Explicit user path** — if the user names a file or folder, use exactly that.
2. **Existing workspace convention** — if previous phase output already lives in a recognisable folder, write next to it.
3. **Canonical scaffold path** — use the path from the table below (relative to the workspace root, typically under `docs/`).
4. **Workspace root** — last resort only.

---

## Scaffold tree and skill mapping

```
docs/
│
├── domain/
│   ├── language/
│   │   └── domain-language.md              ← abd-domain-language
│   ├── model/
│   │   ├── domain-model.md                 ← abd-domain-model
│   │   ├── domain-model.drawio             ← drawio-domain-sync (same stem as domain-model.md)
│   │   └── domain.json                     ← scanner input (maintained alongside domain-model.md)
│   ├── specification/
│   │   ├── domain-specification.md         ← abd-domain-specification
│   │   └── domain-specification.drawio     ← drawio-domain-sync (same stem as domain-specification.md)
│   ├── glossary/
│   │   └── domain-glossary.md              ← abd-domain-glossary
│   └── supporting/
│       ├── bounded-context-map.md          ← abd-bounded-context-map
│       ├── ddd-building-blocks.md          ← abd-ddd-design-building-blocks
│       └── walkthrough.md                  ← abd-domain-walk
│
├── stories/
│   ├── story-map/
│   │   ├── story-map.md                    ← abd-story-mapping
│   │   ├── story-graph.json                ← story-graph-ops (machine-readable; source for drawio-story-sync)
│   │   ├── story-map.drawio                ← drawio-story-sync --mode outline
│   │   ├── thin-slicing.md                 ← abd-thin-slicing
│   │   └── thin-slicing.drawio             ← drawio-story-sync --mode thin-slicing
│   ├── acceptance-criteria/
│   │   ├── acceptance-criteria.md          ← abd-story-acceptance-criteria
│   │   ├── acceptance-criteria.drawio      ← drawio-story-sync --mode acceptance-criteria
│   │   └── domain.json                     ← scanner input copy alongside acceptance criteria
│   └── specification/
│       ├── specification-by-example.md     ← abd-story-specification  (one file, all stories)
│       └── full-specification-by-example.md ← abd-story-specification  (expanded, all epics variant)
│
├── ux/
│   ├── information-architecture/
│   │   ├── information-architecture.md     ← abd-ux-information-architecture
│   │   └── information-architecture.drawio ← abd-ux-information-architecture (via drawio-ux.mjs)
│   ├── mockup/
│   │   ├── state.json                      ← abd-ux-mockup (shared state source of truth)
│   │   ├── mockups.md                      ← abd-ux-mockup (master index / all-screens spec)
│   │   ├── mockup.drawio                   ← abd-ux-mockup (generated wireframe; see screens/ below)
│   │   └── screens/
│   │       ├── <screen-slug>.aria.yaml     ← abd-ux-mockup  (one per screen)
│   │       ├── <screen-slug>-state.json    ← abd-ux-mockup  (one per screen)
│   │       ├── <screen-slug>.drawio        ← abd-ux-mockup  (one per screen)
│   │       └── <screen-slug>.md           ← abd-ux-mockup  (one per screen)
│   └── specification/
│       └── ux-specification.md             ← abd-ux-specification
│
├── architecture/
│   ├── diagrams/
│   │   └── system-context.drawio           ← abd-architecture-outline  (via arch-drawio.ps1 init/export)
│   ├── blueprint/
│   │   ├── architecture-blueprint.md       ← abd-architecture-blueprint
│   │   ├── platform-architecture-elements.md ← abd-architecture-blueprint
│   │   ├── platform-architecture.drawio    ← abd-architecture-blueprint  (via arch-drawio.ps1)
│   │   ├── module-overview.drawio          ← abd-architecture-blueprint  (via arch-drawio.ps1)
│   │   ├── architecture-flow.drawio        ← abd-architecture-blueprint  (via arch-drawio.ps1)
│   │   └── testing-flow.drawio             ← abd-architecture-blueprint  (via arch-drawio.ps1)
│   ├── specification/
│   │   └── <specification-name>/           ← one subfolder per specification
│   │       ├── architecture-specification.md  ← abd-architecture-specification  (manual)
│   │       └── architecture-specification-participants.drawio ← abd-architecture-specification (via build_participants_diagram.py)
│   └── decisions/
│       └── ADR-NNN-description.md          ← one file per architectural decision record
│
├── bdd/
│   └── <feature>-behavior.md               ← abd-bdd-behavior  (BDD behavior spec; one file per feature)
│   NOTE: bdd-specification and bdd-development test files go in the project test folder, not here
│
├── context/                                ← context pipeline outputs (abd-context-* skills)
│   ├── markdown/                           ← abd-context-to-markdown (converted source Markdown)
│   ├── memory/                             ← abd-context-chunk (chunked files + context_chunking_spec.yaml)
│   │   └── rag/                            ← abd-context-db-embed (FAISS vector index)
│   ├── app-extraction/
│   │   └── extracted-pages/                ← abd-context-app-extractor (ARIA YAML + screenshots)
│   └── app-sandbox/
│       └── stubs/                          ← abd-context-app-sandbox (generated stubs + stub registry)
│
├── external/                               ← other inputs and source data (not skill outputs)
│   ├── code-research/                      ← abd-code-research output
│   ├── app-extraction/
│   │   └── pages/
│   │       └── <page-slug>/
│   │           ├── aria.yaml               ← abd-context-app-extractor
│   │           └── screenshot.png          ← abd-context-app-extractor
│   ├── app-sandbox/
│   │   └── stubs/                          ← abd-context-app-sandbox (stub registry + credentials)
│   └── context-chunks/                     ← legacy context memory chunks (superseded by docs/context/)
│
└── cdd-sessions/                           ← context-driven-delivery session artefacts
    └── <YYYY-MM-DD>-<topic>/
        ├── cdd-session-journal.md          ← context-driven-delivery (append-only narrative)
        └── cdd-session-checklist.md        ← context-driven-delivery (grid progress)
```

---

## Notes

| Skill | Canonical file name | Notes |
|---|---|---|
| abd-domain-specification | `domain-specification.md` | Renamed from `class-model.md` — confirmed |
| abd-story-acceptance-test | project test folder | Test code goes in the host project's test folder, not `docs/` — correct by design |
| abd-ux-information-architecture | `docs/ux/information-architecture/information-architecture.md` + `.drawio` | Path and filename confirmed |
| abd-ux-mockup | `docs/ux/mockup/screens/` | `mockup/` (singular) confirmed |
| abd-architecture-specification | `docs/architecture/specification/<specification-name>/` | One subfolder per specification |
| abd-bdd-behavior | `docs/bdd/<feature>-behavior.md` | Behavior spec only; test/spec files go in the project test folder |
| cdd sessions | `docs/cdd-sessions/<YYYY-MM-DD>-<topic>/` | Matches scaffold |

---

## Non-standard locations and `cdd-context-index.md`

When a user moves any deliverable away from its canonical scaffold path — into a project-specific folder, a monorepo sub-package, or anywhere else — **that change must be recorded** so that skills and the CDD orchestrator can find the file without asking every time.

### How it works

Any skill (or the CDD orchestrator) that writes a file to a **non-standard path** must create or update `cdd-context-index.md` at the workspace root (or the agreed project root). This file is the single map from artifact type to actual location.

### Format

```markdown
# CDD Context Index

<!-- One row per artifact that lives outside its canonical docs/ path. -->
<!-- Skills and CDD read this file first when scanning for artifacts. -->

| Artifact | Canonical path | Actual path | Notes |
|---|---|---|---|
| domain-language | `docs/domain/language/domain-language.md` | `src/domain/domain-language.md` | moved alongside code |
| story-map | `docs/stories/story-map/story-map.md` | `product/stories/story-map.md` | product team preference |
| architecture-blueprint | `docs/architecture/blueprint/architecture-blueprint.md` | `docs/arch/blueprint.md` | shortened path |
```

### Rules

- **Only non-standard entries go here.** Files at their canonical scaffold path are not listed — that would duplicate the scaffold tree.
- **The skill that moves or writes to a non-standard path creates or updates the row.** The CDD orchestrator also updates it when the user declares a custom location during grilling.
- **`cdd-context-index.md` is checked first** by CDD and by skills before falling back to the scaffold tree. If a path is listed here, use it without asking.
- **If the user changes a location mid-session**, the orchestrator updates the index and confirms the change in the session journal.

### Empty scaffold file

An empty `cdd-context-index.md` is included in [`context-scaffold/`](./context-scaffold/cdd-context-index.md) with the table header only, ready to populate when a project deviates from defaults.

---

## How to reference this document

**Do not** add a `## Output file` section to practice `SKILL.md` files. [`common/reference/skill-workflow.md`](./skill-workflow.md) § Output file resolution resolves folder (user path → `cdd-context-index.md` → existing deliverables → this document → workspace root) and file name (`reference/output.md` if present, else the entry below).

When authoring a **new** skill, add its row to the scaffold tree above. Add `reference/output.md` on the skill only when it breaks the default (tests in project tree, multiple outputs, non-`.md` deliverable).
