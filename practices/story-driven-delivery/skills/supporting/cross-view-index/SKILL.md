---
name: cross-view-index
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Keep a cheap, navigable JSON index of cross-view links so skills load only what they need.
description: >-
  Maintain artifact-graph.json as the cross-view index that connects stories to domain concepts, UX screens, and architecture mechanisms. Use when building or repairing links between views, detecting drift, or cheaply looking up which artifacts a skill needs before loading full MD files.
context-perspective: stories
context-role: support
context-fidelity:
  - level: discovery
    mode: graph-ops
  - level: exploration
    mode: graph-ops
---

# cross-view-index

## Why this skill exists

Every practice produces Markdown artifacts in `docs/`:

| View | Key artifacts |
|---|---|
| Stories | `story-graph.json`, `story-map.md`, `acceptance-criteria.md` |
| Domain | `domain-language.md`, `domain-model.md`, `domain-glossary.md` |
| UX | `information-architecture.md`, `mockups.md`, `screens/<slug>.md` |
| Architecture | `architecture-blueprint.md`, `specification/<name>/` |

**The problem:** skills that work across views (e.g. `abd-ux-mockup` needs domain terms; `abd-domain-model` needs story context) must load all upstream files to find the relevant parts. This costs tokens and makes drift invisible.

**The solution:** `artifact-graph.json` — a lightweight JSON index (~5 KB) that maps story names to the specific domain concepts, UX screens, and architecture mechanisms they touch. Skills load the index first, then fetch only the linked files. Drift surfaces when links point to missing or renamed artifacts.

---

## Output file

**File name:** `artifact-graph.json`

**Canonical path:** `docs/artifact-graph.json`

If the project uses non-standard paths, record the actual location in `cdd-context-index.md`.

---

## Mandatory workflow (checklist)

Whenever `artifact-graph.json` is created or meaningfully edited:

1. **Run `init`** (first time only) to create the file from the empty template.
2. **Edit** using the CLI — never hand-edit `artifact-graph.json` directly.
3. **Validate:** `python scripts/artifact_graph_cli.py validate --file <path>` (must succeed).
4. **Report** the validation command you ran.

---

## Agent obligations (do not skip)

| Must | Detail |
|---|---|
| **Use this skill's CLI** | Always run **`scripts/artifact_graph_cli.py`** — never hand-write JSON. |
| **Validate after every change** | Run `validate` before declaring done. |
| **Report completion** | Say what you ran (e.g. "validated with `validate`") — not just "wrote JSON." |

**Anti-patterns (reject):**

- Hand-editing `artifact-graph.json` and stopping without `validate`.
- Linking stories to node IDs that haven't been registered in `domain_nodes`, `ux_nodes`, or `arch_nodes`.
- Skipping drift detection after a multi-step editing session.

---

## When to use this skill

| Situation | Action |
|---|---|
| Starting a new workspace | Run `init` to create the empty graph; populate `artifact_registry` with actual file paths. |
| After `abd-story-mapping` produces stories | Run `link` to associate each story with its domain, UX, and arch nodes. |
| After `abd-domain-model` adds or renames a concept | Register the concept in `domain_nodes`; run `drift` to find stale story links. |
| After `abd-ux-mockup` adds a screen | Register the screen in `ux_nodes`; link it to stories via `link`. |
| A skill needs upstream context for a specific story | Run `lookup` to get the list of relevant files; load only those. |
| Suspecting view drift | Run `drift` to surface missing files or dangling links. |
| Reporting on link coverage | Run `stats`. |

---

## Schema

**Schema identifier:** `abd-artifact-graph/v1`

### Top-level fields

| Field | Purpose |
|---|---|
| `schema` | Always `"abd-artifact-graph/v1"` — used by the CLI to reject wrong-schema files. |
| `product` | Product name (matches `story-graph.json`). |
| `artifact_registry` | Map of canonical artifact names to file paths. Skills read this to find the right file without asking. |
| `domain_nodes` | All registered domain concepts by ID (`"Module.Concept"`). |
| `ux_nodes` | All registered UX screens by slug (`"screen-slug"`). |
| `arch_nodes` | All registered architecture mechanisms by ID (`"mechanism-id"`). |
| `story_links` | Cross-view links keyed by **exact story name** (must match `story-graph.json`). |

### Node IDs

| View | ID format | Example |
|---|---|---|
| Domain | `"Module.Concept"` | `"Catalog.Product"` |
| UX | `"screen-slug"` (kebab-case) | `"product-search"` |
| Architecture | `"mechanism-id"` (kebab-case) | `"catalog-api"` |

### `domain_nodes` entry

```json
"Catalog.Product": {
  "module": "Catalog",
  "concept": "Product",
  "file": "docs/domain/model/domain-model.md"
}
```

### `ux_nodes` entry

```json
"product-search": {
  "label": "Product Search",
  "file": "docs/ux/mockup/screens/product-search.md"
}
```

### `arch_nodes` entry

```json
"catalog-api": {
  "label": "Catalog API",
  "file": "docs/architecture/specification/catalog-api/architecture-specification.md",
  "mechanism": "REST"
}
```

### `story_links` entry

```json
"Search Products by Keyword": {
  "epic": "Shop in store",
  "sub_epic": "Find products and check stock",
  "domain": ["Catalog.Product", "Catalog.SearchResult"],
  "ux": ["product-search"],
  "arch": ["catalog-api"]
}
```

---

## CLI

Implementation: **`scripts/artifact_graph_cli.py`**

```text
python artifact_graph_cli.py init     --file <path> [--product "Name"] [--force]
python artifact_graph_cli.py read     --file <path>
python artifact_graph_cli.py validate --file <path> [--root <workspace-root>]
python artifact_graph_cli.py link     --file <path> --story "Exact Story Name"
                                      [--epic "Epic Name"] [--sub-epic "Sub-epic Name"]
                                      [--domain Module.Concept ...]
                                      [--ux screen-slug ...]
                                      [--arch mechanism-id ...]
python artifact_graph_cli.py lookup   --file <path> --story "Exact Story Name"
python artifact_graph_cli.py reverse  --file <path> --domain "Module.Concept"
python artifact_graph_cli.py reverse  --file <path> --ux "screen-slug"
python artifact_graph_cli.py reverse  --file <path> --arch "mechanism-id"
python artifact_graph_cli.py drift    --file <path> [--root <workspace-root>]
python artifact_graph_cli.py stats    --file <path>
```

---

## How skills use this index

### Pattern: load the index, then fetch only what you need

Instead of loading all domain, UX, and architecture files up front, a skill does:

1. **Load `artifact-graph.json`** (cheap — ~5 KB).
2. **Identify the story or stories in scope** (from the user's request or the current kanban cell).
3. **Run `lookup --story "Story Name"`** to get the list of linked files.
4. **Load only those files** — the domain-model section for `Catalog.Product`, the screen spec for `product-search`, etc.

This cuts context by 60–90% in multi-view engagements where most artifacts are irrelevant to the current story.

### Pattern: cross-view consistency check before generating

Before generating content for a story in any view:

1. Run `lookup` to see what the other views say about this story.
2. Load the linked files.
3. Generate with full cross-view context — domain terms, accepted screen layout, arch constraints — already in scope.

### Pattern: drift detection at the start of a session

At the start of a multi-session engagement, run:

```bash
python artifact_graph_cli.py drift --file docs/artifact-graph.json --root .
```

Any missing file or dangling link is a view that has drifted. Fix those before proceeding.

---

## Relationship to other skills

| Skill | Relationship |
|---|---|
| **story-graph-ops** | `artifact-graph.json` story names must match `story-graph.json` exactly. Run `story-graph-ops` first; then register links here. |
| **abd-story-mapping** | Story names come from story-map.md → story-graph.json. Do not invent names here. |
| **abd-domain-model** | Register each module/concept in `domain_nodes` after `domain-model.md` is written. |
| **abd-ux-mockup** | Register each screen slug in `ux_nodes` after screen files are written. |
| **abd-architecture-specification** | Register each mechanism in `arch_nodes` after the spec folder is created. |

---

## Sources

- CLI: `scripts/artifact_graph_cli.py`
- Empty template: `templates/artifact-graph.json`
- Populated example: `templates/artifact-graph-example.json`
- Concepts: `reference/concepts.md`
