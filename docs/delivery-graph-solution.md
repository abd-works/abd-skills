# Delivery graph solution — connected views

**Status:** Design / agreed direction — not implemented yet.

## Solution in one sentence

**Each perspective owns a type-safe view graph with simple containment; a context graph of nodes and typed edges links views at any hierarchy level — so skills resolve scope cheaply without duplicating prose in Markdown.**

---

## Problem

Delivery artifacts span four perspectives (domain, stories, UX, architecture). Today they live mostly in Markdown with implicit cross-references. Skills are told to “read upstream artifacts,” which is expensive in tokens and easy to skip. Connections drift because they are copied into prose instead of declared once.

We need:

- **Concrete, typed models** per view (not a generic abstract graph).
- **Simple containment** inside each view (trees, as today).
- **Cross-view links** at any level (a screen can relate to an epic, a story, or a scenario; an epic can relate to a module, a KA, or a class).
- **Fixed cross-view edge types** — a small named vocabulary (`exercises`, `surfaces-through`, …); the same type applies at any hierarchy level.

---

## Architecture overview

```text
┌─────────────────────────────────────────────────────────────────┐
│  context-graph.json  (nodes + edges)                            │
│  Fixed cross-view edge types; any hierarchy level on endpoints  │
└────────────┬──────────────┬──────────────┬──────────────────────┘
             │              │              │
    ┌────────▼────┐  ┌──────▼─────┐  ┌─────▼─────┐  ┌──────────────┐
    │ story-graph │  │domain-graph│  │  ux-graph │  │ arch-graph   │
    │ (typed tree)│  │(typed tree)│  │(typed tree│  │ (typed tree) │
    └─────────────┘  └────────────┘  └───────────┘  └──────────────┘
         │                  │               │                │
    Markdown /           Markdown /    state.json /     Markdown /
    drawio views         drawio views  aria.yaml views  drawio views
```

**Two layers:**

| Layer | What it is | Edges |
| --- | --- | --- |
| **View graphs** | Type-safe, concrete trees per perspective | **Containment only** (parent owns children), same as today |
| **Context graph** | Node registry + cross-view edges | **Named edge types** (fixed vocabulary); endpoints at any hierarchy level |

Perspectives are **not containers** that hold separate copies of the truth. They are **views** over the same delivery. The context graph records how nodes in one view relate to nodes in another.

---

## View graphs (typed, containment only)

Each view is its own JSON graph. Internal structure uses familiar parent/child containment. No cross-view edges inside these files.

### story-graph

**Canonical file:** `docs/stories/story-map/story-graph.json`  
**Schema:** `abd-story-graph/v1` (existing)  
**Tooling:** `story-graph-ops` (existing)

| Node kind | Contains |
| --- | --- |
| `Epic` | `SubEpic`, `Story` |
| `SubEpic` | `SubEpic`, `Story` |
| `Story` | `Scenario`, `ScenarioOutline`, acceptance criteria |
| `Increment` | ordered story references |

Markdown (`story-map.md`, `specification-by-example.md`, …) and Draw.io diagrams are **projections** of this graph, not a competing source of truth.

### domain-graph

**Canonical file:** `docs/domain/model/domain-graph.json` (new; `domain.json` remains for scanner vocabulary)  
**Evolves from:** `domain-model.md`, `domain.json`, KA / module structure in domain skills

| Node kind | Contains |
| --- | --- |
| `Module` | `KeyAbstraction`, `Class` |
| `KeyAbstraction` | `Class`, `Term` |
| `Class` | `Property`, `Responsibility` |
| `BoundedContext` | `Module` |

`domain.json` stays a **flat vocabulary index** (concept names, attributes, inheritance) for scanners. `domain-graph.json` holds **structure and containment** that markdown scatters today.

### ux-graph

**Canonical file:** `docs/ux/mockup/ux-graph.json` (new; may consolidate with `state.json` over time)  
**Evolves from:** per-screen `*-state.json`, `aria.yaml`, IA site map

| Node kind | Contains |
| --- | --- |
| `Flow` | `Screen` |
| `Screen` | `Region`, `Tab` |
| `Region` | `Control`, `ContentType` |
| `Control` | states, bindings (detail in `*-state.json`) |

Per-screen `*-state.json` files remain the **rich control/state source**; `ux-graph.json` is the **structural spine** (screens, regions, navigation) analogous to `story-graph.json`.

### arch-graph

**Canonical file:** `docs/architecture/arch-graph.json` (new)  
**Evolves from:** blueprint, module overview, mechanism sections

| Node kind | Contains |
| --- | --- |
| `System` | `Subsystem`, `Module` |
| `Module` | `Component`, `Mechanism` |
| `Mechanism` | decision references, participant lists |

Architecture prose (`architecture-specification.md`, ADRs) stays the **deep detail**; `arch-graph.json` holds **structure and mechanism placement**.

1. **Containment only** inside a view — no typed cross-links.
2. **Stable node ids** on every node: `{view}:{kind}:{slug}` (e.g. `story:epic:shop-in-store`).
3. **Semantic locator** on every node: file `path` + name-based `pointer` (see below) — not array indices.
4. **Skills write the view graph first** (or validate into it); Markdown is generated or checked against it.
5. View graphs may **consolidate** over time (e.g. ux-graph absorbing navigation from `state.json`) — one spine per view, same pattern as story-graph.

### Semantic locators (name-based pointers)

A node's `pointer` is a **path through the containment tree using element names**, not a JSON Pointer index.

```text
epics/Shop in store/sub_epics/Find products and check stock/stories/Search Products by Keyword
screens/Search Results/regions/Results list
modules/Catalog/classes/Product
modules/Catalog/mechanisms/Repository pattern
```

**Format:**

```text
{collection}/{name}/{collection}/{name}/…
```

| Part | Rule |
| --- | --- |
| `collection` | Plural segment for the child array in that view (`epics`, `sub_epics`, `stories`, `scenarios`, `screens`, `regions`, `modules`, `classes`, …) |
| `{name}` | The node's `name` field — **unquoted**; spaces and punctuation are fine |
| Root | Starts at the view graph root — no leading slash, no numeric indices |

**No quotes in the normal case.** The pointer lives inside a JSON string already; wrapping every name in `\"…\"` adds clutter and escaping pain for no benefit when names are plain text (which they almost always are).

**Escaping (rare):** only when a name contains `/`, wrap that segment in brackets: `stories/[Confirm stock/availability]`. If a name contains `]`, prefer renaming. Do not use per-segment JSON quotes.

**Why names, not indices:**

- **Readable** — agents, humans, and diffs see what the path means without loading the file.
- **Stable across reorder** — renaming aside, inserting a sibling does not invalidate the path the way `/epics/0/…` does.
- **Aligns with bot paths** — same mental model as `story_graph."Shop in store".stories."Search Products"` in story-graph-ops, without persisting quote characters.

**Resolution:** tooling walks the view graph at `path`, alternating `collection` / `name` segments (known collection vocabulary vs match on `name`). Sibling names must be unique within a parent.

**Markdown-only nodes** (e.g. architecture prose without a graph spine yet): `pointer` may be a markdown anchor path — `architecture-specification.md#repository-pattern` — until promoted into `arch-graph.json`.

---

## Context graph (cross-view graph)

**Canonical file:** `docs/context/context-graph.json`  
**Schema:** `abd-context-graph/v1`

The context graph is a standard **nodes + edges** graph. It does **not** duplicate view content — nodes are references into view graphs; edges declare cross-view relationships.

### Graph shape

```json
{
  "schema": "abd-context-graph/v1",
  "product": "PawPlace",
  "nodes": [
    {
      "id": "ux:screen:search-results",
      "kind": "Screen",
      "view": "ux",
      "path": "docs/ux/mockup/ux-graph.json",
      "pointer": "flows/Shop in store/screens/Search Results"
    },
    {
      "id": "story:epic:shop-in-store",
      "kind": "Epic",
      "view": "stories",
      "path": "docs/stories/story-map/story-graph.json",
      "pointer": "epics/Shop in store"
    },
    {
      "id": "ux:region:results-list",
      "kind": "Region",
      "view": "ux",
      "path": "docs/ux/mockup/ux-graph.json",
      "pointer": "flows/Shop in store/screens/Search Results/regions/Results list"
    },
    {
      "id": "story:scenario:keyword-returns-matching-products",
      "kind": "Scenario",
      "view": "stories",
      "path": "docs/stories/story-map/story-graph.json",
      "pointer": "epics/Shop in store/sub_epics/Find products and check stock/stories/Search Products by Keyword/scenarios/Keyword returns matching products"
    },
    {
      "id": "domain:module:catalog",
      "kind": "Module",
      "view": "domain",
      "path": "docs/domain/model/domain-graph.json",
      "pointer": "modules/Catalog"
    },
    {
      "id": "arch:mechanism:repository-pattern",
      "kind": "Mechanism",
      "view": "architecture",
      "path": "docs/architecture/arch-graph.json",
      "pointer": "modules/Catalog/mechanisms/Repository pattern"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "type": "enables",
      "source": "ux:screen:search-results",
      "target": "story:epic:shop-in-store"
    },
    {
      "id": "e2",
      "type": "enables",
      "source": "ux:region:results-list",
      "target": "story:scenario:keyword-returns-matching-products"
    },
    {
      "id": "e3",
      "type": "exercises",
      "source": "story:epic:shop-in-store",
      "target": "domain:module:catalog"
    },
    {
      "id": "e4",
      "type": "realizes",
      "source": "arch:mechanism:repository-pattern",
      "target": "domain:class:stock-availability"
    },
    {
      "id": "e5",
      "type": "implements",
      "source": "arch:mechanism:repository-pattern",
      "target": "story:story:confirm-product-stock"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `nodes[]` | Registry of cross-view node references (`id`, `kind`, `view`, `path`, `pointer`) |
| `edges[]` | Directed cross-view relationships |
| `edges[].type` | One of the **fixed cross-view edge types** (below) |
| `edges[].source`, `edges[].target` | Node ids — any kind, any hierarchy level |

Nodes are registered in the context graph when first linked (or when a skill explicitly registers scope). View graphs remain authoritative for containment and content; context graph nodes are **pointers**, not copies.

### Fixed cross-view edge types

Edge types are **fixed across views** — the same six names everywhere. Hierarchy level does not change the type: `enables` from `Screen` → `Epic` uses the same type as `Region` → `Scenario`.

| Edge type | Direction | Meaning |
| --- | --- | --- |
| `exercises` | stories → domain | Story behavior uses or constrains domain concepts |
| `surfaces-through` | stories → ux | Story outcome appears on a screen, region, or control |
| `presents` | ux → domain | UX shows domain state, labels, or structure |
| `enables` | ux → stories | UX affordance triggers or supports story behavior |
| `implements` | architecture → stories, ux | Technology delivers story behavior or UX surface |
| `realizes` | architecture → domain | Technology encodes domain structure or rules |

**No per-level edge types** — no `enables-epic` vs `enables-scenario`. The **node kinds** on `source` and `target` carry the level; `type` carries the cross-view semantics.

Optional `note` on an edge is free text for humans — not a schema extension.

### Node references (`path` + semantic `pointer`)

Each node (in view graphs and registered in the context graph) carries:

```json
{
  "id": "story:story:search-products-by-keyword",
  "kind": "Story",
  "view": "stories",
  "name": "Search Products by Keyword",
  "path": "docs/stories/story-map/story-graph.json",
  "pointer": "epics/Shop in store/sub_epics/Find products and check stock/stories/Search Products by Keyword"
}
```

| Field | Role |
| --- | --- |
| `id` | Stable slug for edges and APIs — does not change when display name is tweaked |
| `name` | Human label — appears as a segment in `pointer` |
| `path` | Which file holds the view graph (or markdown for prose-only nodes) |
| `pointer` | Name-based locator within that file — **semantic, not numeric** |

Skills resolve in two steps:

1. `id` or `pointer` → locate the node in the view graph.
2. Fetch only that node's content (and children if roll-up needs them).

`id` and `pointer` are redundant on purpose: **edges use `id`**; **logs, skills, and humans use `pointer`** when discussing location.

Non-canonical file locations are listed in `cdd-context-index.md` (existing); `path` points to the actual file on disk.

### Roll-up on read (not on write)

A link from a screen to an epic is intentionally coarse. When a skill needs finer scope:

1. Collect edges whose `source` or `target` touches scope nodes (filter by `type` when the skill cares).
2. Optionally expand through **containment** inside the relevant view graph (epic → child stories).
3. Fetch canonical content for the resulting node set.

Store explicit edges; expand hierarchy at query time.

---

## How the views relate (vocabulary)

“Story describes interactions for domain and UX” is too weak — it sounds like stories own the other views. Better framing:

| View | Role (one line) | Toward domain | Toward stories | Toward UX | Toward architecture |
| --- | --- | --- | --- | --- | --- |
| **Domain** | Structure and rules — what exists, what must hold | — | concepts stories **exercise** | state and labels UX **presents** | structures arch **realizes** |
| **Stories** | Behavior — what actors and systems do, under what acceptance | **exercises** domain concepts | — | outcomes UX **enables** | behavior arch **implements** |
| **UX** | Presentation — what people see, touch, and navigate | **presents** domain state | **enables** story behavior | — | UI arch **implements** |
| **Architecture** | Realization — how behavior and structure are built in technology | **realizes** domain model | **implements** story behavior | **implements** UX surfaces | — |

### Cross-view edge types (authoring reference)

These names are the **only** allowed `edges[].type` values in `context-graph.json`:

| Edge type | Typical source → target | Example |
| --- | --- | --- |
| `exercises` | stories → domain | `story:story:search-products` → `domain:class:Product` |
| `surfaces-through` | stories → ux | `story:story:search-products` → `ux:screen:search-results` |
| `presents` | ux → domain | `ux:region:results-list` → `domain:class:Product` |
| `enables` | ux → stories | `ux:screen:search-results` → `story:epic:shop-in-store` |
| `implements` | architecture → stories or ux | `arch:module:client` → `ux:screen:product-detail` |
| `realizes` | architecture → domain | `arch:mechanism:repository-pattern` → `domain:class:Order` |

**Stories are the behavioral spine** — they say what happens. Domain supplies the concepts and rules being exercised. UX supplies how it is presented and triggered. Architecture supplies how it is built.

---

## Workspace layout

```text
docs/
├── context/
│   └── context-graph.json          ← cross-view links (new)
├── domain/
│   └── model/
│       ├── domain-graph.json       ← domain view spine (new)
│       ├── domain.json             ← flat vocabulary for scanners (existing)
│       └── domain-model.md         ← projection
├── stories/
│   └── story-map/
│       ├── story-graph.json        ← story view spine (existing)
│       └── story-map.md            ← projection
├── ux/
│   └── mockup/
│       ├── ux-graph.json           ← ux view spine (new)
│       ├── state.json              ← shared ux state (existing)
│       └── screens/                ← per-screen detail (existing)
└── architecture/
    ├── arch-graph.json             ← architecture view spine (new)
    └── specification/              ← deep prose (existing)
```

`cdd-context-index.md` at workspace root lists artifacts not at these canonical paths (existing convention).

---

## Skill protocol

### Write time

1. Skill produces or updates its **view graph** node(s).
2. Skill registers **stable ids** on those nodes.
3. When the skill establishes a cross-view relationship, it registers nodes (if needed) and appends an **edge** to `context-graph.json` with the correct `type`, `source`, and `target` (any level ↔ any level).
4. Markdown / Draw.io is generated from the view graph or validated against it.

### Read time (index-first, cheap context)

1. Load `context-graph.json` (small).
2. Resolve run scope from kanban / user (increment, epic, story names).
3. Find scope node ids in the relevant view graph(s).
4. Collect edges touching those node ids (by `source` / `target`); filter by `type` when needed; optionally roll up/down containment in view graphs.
5. Fetch content for hit nodes via `path` + semantic `pointer` (or resolve `id` → `pointer` first).
6. If a required link is missing, **flag a gap** — do not fabricate (see `handling-incomplete-context.md`).

### Validation

| Check | Layer |
| --- | --- |
| View graph well-formed | Per-view schema + existing scanners |
| Every edge `source` / `target` resolves to a registered node id | `context-graph` validator |
| Every registered node `pointer` resolves to exactly one node in its view graph | `context-graph` validator |
| Sibling `name` values are unique within each parent (required for locators) | Per-view graph validator |
| Every edge `type` is one of the six fixed cross-view types | `context-graph` validator |
| Cross-view claims in Markdown have matching edges | New integrity scanners |
| Orphan nodes in scope | Coverage report per increment |

---

## Relationship to existing pieces

| Existing piece | Role in this solution |
| --- | --- |
| `story-graph.json` + `story-graph-ops` | Story view graph — **keep**; extend with stable ids |
| `domain.json` | Vocabulary index for scanners — **keep** alongside `domain-graph.json` |
| `abd-context-semantic-index` | Ingestion-time tagging of raw corpus — may inform brownfield edge authoring (future `evidence` type TBD) |
| `cdd-context-index.md` | Path overrides when artifacts are not at canonical `docs/` paths |
| `context-taxonomy.md` | Perspective × fidelity grid — **unchanged**; views map to perspectives |
| `folder-conventions.md` | Canonical paths — **extend** with new graph files |
| Markdown projections | Human-readable views — **not** source of truth for cross-view links |

---

## Implementation phases

| Phase | Deliverable | Notes |
| --- | --- | --- |
| **0** | This document + `abd-context-graph/v1` schema stub | Agree ids, layout, verbs |
| **1** | Stable ids on `story-graph` nodes; `context-graph.json` with nodes + edges for one fixture | PawPlace mini |
| **2** | `context-graph-ops` CLI: `add-edge`, `neighbors`, `validate`, `coverage`, `resolve-pointer` | Mirror `story-graph-ops`; name-walk resolver |
| **3** | `domain-graph.json` schema + domain skills emit on write | Alongside `domain.json` |
| **4** | `ux-graph.json` from IA / mockup skills | IA trace tables → `enables` / `presents` edges |
| **5** | `arch-graph.json` from blueprint / specification skills | Mechanism nodes + `implements` / `realizes` edges |
| **6** | Read-gates on pilot skills (`abd-story-specification`, `abd-ux-mockup`, `abd-architecture-specification`) | Index-first context |
| **7** | Integrity scanners + eval fixtures for “ignored upstream link” | See `docs/Solution.md` promotion model |

---

## What this is not

- Not a graph database requirement — JSON in git is the source of truth.
- Not RDF / JSON-LD — typed view graphs + simple links are enough.
- Not per-level edge types — six fixed cross-view types; hierarchy level is on the nodes, not in the type name.
- Not a single mega-tree — each view keeps its own containment; context graph wires across them.
- Not numeric JSON Pointers in authored files — locators use name paths (`epics/Shop in store/stories/…`), not `/epics/0/…`.
- Not replacing Markdown — projections stay for humans; graphs stay for machines and skills.

## Open questions

1. **ux-graph vs `state.json`** — when to merge navigation spine into state files vs separate `ux-graph.json`.
2. **Edge symmetry** — edges are directed; whether to infer reverse traversal on read for specific types.
3. **Evidence edges** — whether brownfield traceability needs a seventh type (e.g. `evidence`) from semantic-index chunks.
4. **`id` on rename** — keep stable slug and only update `pointer` + `name`, or migrate `id` and edge endpoints when display names change.
5. **Versioning** — optimistic concurrency on `context-graph.json` (same `--expect-sha` pattern as `story-graph-ops`).

---

## References

| Piece | Path |
| --- | --- |
| Context taxonomy (perspectives) | `common/reference/context-taxonomy.md` |
| Folder conventions | `common/reference/folder-conventions.md` |
| Story graph ops | `practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md` |
| Scenarios on story graph | `practices/story-driven-delivery/skills/abd-story-specification/rules/scenarios-on-story-graph.md` |
| Semantic context index | `practices/context-driven-delivery/skills/abd-context-semantic-index/SKILL.md` |
| Incomplete context discipline | `practices/story-driven-delivery/reference/handling-incomplete-context.md` |
| Eval / skill learning loop | `docs/Solution.md` |
