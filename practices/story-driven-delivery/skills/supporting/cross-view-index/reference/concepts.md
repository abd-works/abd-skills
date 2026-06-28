# Cross-view Index — Concepts

## The multi-view problem

An ABD engagement produces artifacts in four parallel views. Each view has its own source of truth in Markdown:

```
Stories ──────── story-map.md, story-graph.json
Domain ────────── domain-language.md, domain-model.md
UX ────────────── information-architecture.md, screens/*.md
Architecture ──── architecture-blueprint.md, specification/*/
```

These views **describe the same product from different angles**. A story like "Search Products by Keyword" has:

- A **domain shape** — the `Product` and `SearchResult` concepts it operates on.
- A **UX shape** — the `product-search` screen that exposes it.
- An **architecture shape** — the `catalog-api` and `search-index` mechanisms that implement it.

When views are only connected through human memory and prose, two problems emerge:

### Problem 1 — Drift

Files evolve independently. A domain concept is renamed, but the UX screen still refers to the old term. A story is split into two, but the architecture spec still targets the old story name. A screen is added, but no story knows about it. By the time anyone notices, multiple artifacts are inconsistent and correcting them is expensive.

### Problem 2 — Context cost

Skills that need cross-view context (e.g. `abd-ux-mockup` needing domain terms from `domain-language.md`) must load all upstream files to find the relevant parts. A large engagement's domain language file can be 50–200 KB. Loading it entirely to find the three terms relevant to one screen wastes tokens and inflates context windows.

---

## The solution: artifact-graph.json

`artifact-graph.json` is a **lightweight cross-view index** (~5 KB) that:

1. **Registers all artifact files** by canonical name (the `artifact_registry`).
2. **Registers all cross-view nodes** — domain concepts, UX screens, architecture mechanisms.
3. **Links each story** to the specific nodes it touches.

Skills can load the index in a single read, then follow links to load **only the files relevant to the current story**.

---

## What is a "node"?

A node is any named artifact element that can be referenced across views. Nodes have IDs, file paths, and (optionally) section anchors.

| Node type | Represents | ID format | Example |
|---|---|---|---|
| Domain node | A concept (class) in a domain module | `"Module.Concept"` | `"Catalog.Product"` |
| UX node | A named screen in the mockup | `"screen-slug"` | `"product-search"` |
| Arch node | An architecture mechanism or specification | `"mechanism-id"` | `"catalog-api"` |

Node IDs are **stable keys** — they must not change unless the underlying artifact is renamed. When an artifact is renamed, update the node ID, then run `drift` to find and repair all story links that referenced the old ID.

---

## What is a "story link"?

A story link is the set of cross-view references for one story, keyed by the story's **exact name** (must match `story-graph.json`).

```json
"Search Products by Keyword": {
  "epic": "Shop in store",
  "sub_epic": "Find products and check stock",
  "domain": ["Catalog.Product", "Catalog.SearchResult"],
  "ux": ["product-search"],
  "arch": ["catalog-api", "search-index"]
}
```

The `domain`, `ux`, and `arch` arrays list the node IDs that this story directly exercises. A skill doing work on this story needs only those artifacts, not everything in the project.

---

## Architecture mechanisms vs. story coverage

Architecture mechanisms are intentionally **not mapped 1:1 to stories**. A single mechanism (e.g. the authentication middleware) may apply to dozens of stories without each story needing to carry that link. The `arch` array in `story_links` should only contain mechanisms that are **specific to that story's behavior** — not universal infrastructure.

Universal mechanisms (authentication, logging, error handling) belong in the architecture blueprint and do not need to be repeated in every story link.

---

## Drift detection

Drift is detected by comparing what the graph *says* against what is *on disk*:

| Drift type | What it means |
|---|---|
| Missing registry file | A primary view artifact (e.g. `domain-model.md`) doesn't exist yet or was moved |
| Missing node file | A registered domain/UX/arch file was deleted, moved, or not yet created |
| Dangling story link | A story references a node ID that no longer exists in `domain_nodes`, `ux_nodes`, or `arch_nodes` |

Run `artifact_graph_cli.py drift --file docs/artifact-graph.json --root .` at the start of any multi-session engagement to catch drift before it compounds.

---

## When to build links

Links are built incrementally as views mature:

| Stage | Action |
|---|---|
| Discovery | Register domain modules in `domain_nodes` after `domain-language.md` exists. Link stories to modules (not yet to specific concepts). |
| Exploration | Register specific concepts in `domain_nodes` after `domain-model.md` exists. Register screens in `ux_nodes` after IA is written. Link stories fully. |
| Specification | Register arch mechanisms in `arch_nodes` after `architecture-blueprint.md` exists. Complete `arch` links for stories in current increment. |
| Engineering | Run `drift` before each increment to verify all linked files exist. |

---

## The `artifact_registry` section

The registry maps canonical artifact names to **file paths relative to the workspace root**. Skills read this section instead of hardcoding canonical paths or asking the user where files are.

```json
"artifact_registry": {
  "story_graph": "docs/stories/story-map/story-graph.json",
  "domain_language": "docs/domain/language/domain-language.md",
  "domain_model": "docs/domain/model/domain-model.md",
  "domain_glossary": "docs/domain/glossary/domain-glossary.md",
  "ux_information_architecture": "docs/ux/information-architecture/information-architecture.md",
  "ux_mockup_index": "docs/ux/mockup/mockups.md",
  "architecture_blueprint": "docs/architecture/blueprint/architecture-blueprint.md"
}
```

When a project uses non-standard paths (recorded in `cdd-context-index.md`), update the registry entries to match. The registry is the single place where canonical names resolve to actual paths.

---

## Relationship to story-graph.json

`story-graph.json` is the **structural** backbone: epics, sub-epics, stories, acceptance criteria, scenarios, increments, and test references.

`artifact-graph.json` is the **cross-view** backbone: which domain concepts, UX screens, and architecture mechanisms each story touches.

They complement each other. A skill working purely within the story view only needs `story-graph.json`. A skill that crosses views (generating UX specs, validating domain coverage, checking arch alignment) additionally loads `artifact-graph.json` to navigate efficiently.

---

## Token efficiency model

| Scenario | Without index | With index |
|---|---|---|
| UX skill needs domain terms for one screen | Load entire `domain-language.md` (50–200 KB) | Load `artifact-graph.json` (5 KB) → load only the relevant KA sections |
| Domain skill needs story context for one concept | Load entire `story-map.md` (10–50 KB) + AC file | Load index → `reverse --domain "Module.Concept"` → load the 2–3 story AC entries |
| Architecture skill needs to check story coverage | Load all story and domain files | Load index → `stats` shows gaps; `lookup` for specific stories |

The index pays for itself at the first multi-view task in any engagement.
