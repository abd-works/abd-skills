# Delivery graph solution — connected views

**Status:** Design / agreed direction — not implemented yet.

## Solution in one sentence

**Each perspective owns a type-safe view graph with simple containment; a separate context graph links nodes across views at any hierarchy level using path-based references — so skills resolve scope cheaply without duplicating prose in Markdown.**

---

## Problem

Delivery artifacts span four perspectives (domain, stories, UX, architecture). Today they live mostly in Markdown with implicit cross-references. Skills are told to “read upstream artifacts,” which is expensive in tokens and easy to skip. Connections drift because they are copied into prose instead of declared once.

We need:

- **Concrete, typed models** per view (not a generic abstract graph).
- **Simple containment** inside each view (trees, as today).
- **Cross-view links** at any level (a screen can relate to an epic, a story, or a scenario; an epic can relate to a module, a KA, or a class).
- **No edge-type proliferation** — hierarchy level is a property of the node, not a different kind of edge.

---

## Architecture overview

```text
┌─────────────────────────────────────────────────────────────────┐
│  context-graph.json                                             │
│  Path-based links between nodes in any view, at any level       │
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
| **Context graph** | Registry of cross-view links | **Simple links** between node paths — no edge-type taxonomy |

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

### View graph rules

1. **Containment only** inside a view — no typed cross-links.
2. **Stable node ids** on every node: `{view}:{kind}:{slug}` (e.g. `story:epic:shop-in-store`).
3. **Canonical path** on every node: file path + JSON pointer (or markdown anchor).
4. **Skills write the view graph first** (or validate into it); Markdown is generated or checked against it.
5. View graphs may **consolidate** over time (e.g. ux-graph absorbing navigation from `state.json`) — one spine per view, same pattern as story-graph.

---

## Context graph (cross-view links)

**Canonical file:** `docs/context/context-graph.json`  
**Schema:** `abd-context-graph/v1`

The context graph does **not** duplicate view content. It records **which node in one view relates to which node in another**, at **any hierarchy level**.

### Link shape (no edge types)

```json
{
  "schema": "abd-context-graph/v1",
  "product": "PawPlace",
  "links": [
    {
      "from": "ux:screen:search-results",
      "to": "story:epic:shop-in-store"
    },
    {
      "from": "ux:region:results-list",
      "to": "story:scenario:keyword-returns-matching-products"
    },
    {
      "from": "story:epic:shop-in-store",
      "to": "domain:module:catalog"
    },
    {
      "from": "story:story:confirm-product-stock",
      "to": "domain:ka:stock-management"
    },
    {
      "from": "arch:mechanism:repository-pattern",
      "to": "domain:class:StockAvailability"
    },
    {
      "from": "arch:mechanism:repository-pattern",
      "to": "story:story:confirm-product-stock"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `from`, `to` | Stable node ids from any view graph |
| Optional `note` | Human-readable intent when helpful — not a schema edge type |

**No `DISPLAYS` vs `DISPLAYS_EPIC` vs `IMPLEMENTS_STORY`.** Level differences are in the **node kinds** (`Screen` → `Epic` vs `Region` → `Scenario`), not in the link machinery.

### Path-based node references

Each view-graph node carries:

```json
{
  "id": "story:story:search-products-by-keyword",
  "kind": "Story",
  "name": "Search Products by Keyword",
  "path": "docs/stories/story-map/story-graph.json",
  "pointer": "/epics/0/sub_epics/0/stories/0"
}
```

The context graph links **ids**. Skills resolve ids → `path` + `pointer` → fetch only that slice.

Non-canonical paths are listed in `cdd-context-index.md` (existing); node `path` fields point to the actual file.

### Roll-up on read (not on write)

A link from a screen to an epic is intentionally coarse. When a skill needs finer scope:

1. Collect direct links touching scope nodes.
2. Optionally expand through **containment** inside the relevant view graph (epic → child stories).
3. Fetch canonical content for the resulting node set.

Store explicit links; expand hierarchy at query time.

---

## How the views relate (vocabulary)

“Story describes interactions for domain and UX” is too weak — it sounds like stories own the other views. Better framing:

| View | Role (one line) | Toward domain | Toward stories | Toward UX | Toward architecture |
| --- | --- | --- | --- | --- | --- |
| **Domain** | Structure and rules — what exists, what must hold | — | concepts stories **exercise** | state and labels UX **presents** | structures arch **realizes** |
| **Stories** | Behavior — what actors and systems do, under what acceptance | **exercises** domain concepts | — | outcomes UX **enables** | behavior arch **implements** |
| **UX** | Presentation — what people see, touch, and navigate | **presents** domain state | **enables** story behavior | — | UI arch **implements** |
| **Architecture** | Realization — how behavior and structure are built in technology | **realizes** domain model | **implements** story behavior | **implements** UX surfaces | — |

### Cross-view verbs (for skills and docs)

Use these when writing `note` on context links or describing handoffs:

| From → To | Verb | Example |
| --- | --- | --- |
| Stories → Domain | **exercises** | Story exercises `Product`, `StockAvailability` |
| Stories → UX | **surfaces through** | Story surfaces through Search Results screen |
| UX → Domain | **presents** | Region presents `Product` list |
| UX → Stories | **enables** | Control enables “search by keyword” story |
| Architecture → Stories | **implements** | Module implements checkout stories |
| Architecture → Domain | **realizes** | Repository realizes `Order` aggregate |
| Architecture → UX | **implements** | Client module implements product-detail screen |

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
3. When the skill establishes a cross-view relationship, it appends a **link** to `context-graph.json` (any level ↔ any level).
4. Markdown / Draw.io is generated from the view graph or validated against it.

### Read time (index-first, cheap context)

1. Load `context-graph.json` (small).
2. Resolve run scope from kanban / user (increment, epic, story names).
3. Find scope node ids in the relevant view graph(s).
4. Collect links touching those ids; optionally roll up/down containment in view graphs.
5. Fetch **only** `path` + `pointer` (or anchor) for hit nodes.
6. If a required link is missing, **flag a gap** — do not fabricate (see `handling-incomplete-context.md`).

### Validation

| Check | Layer |
| --- | --- |
| View graph well-formed | Per-view schema + existing scanners |
| Every link endpoint resolves to a node id | `context-graph` validator |
| Cross-view claims in Markdown have matching links | New integrity scanners |
| Orphan nodes in scope | Coverage report per increment |

---

## Relationship to existing pieces

| Existing piece | Role in this solution |
| --- | --- |
| `story-graph.json` + `story-graph-ops` | Story view graph — **keep**; extend with stable ids |
| `domain.json` | Vocabulary index for scanners — **keep** alongside `domain-graph.json` |
| `abd-context-semantic-index` | Ingestion-time tagging of raw corpus — feeds **evidence** links into context graph for brownfield |
| `cdd-context-index.md` | Path overrides when artifacts are not at canonical `docs/` paths |
| `context-taxonomy.md` | Perspective × fidelity grid — **unchanged**; views map to perspectives |
| `folder-conventions.md` | Canonical paths — **extend** with new graph files |
| Markdown projections | Human-readable views — **not** source of truth for cross-view links |

---

## Implementation phases

| Phase | Deliverable | Notes |
| --- | --- | --- |
| **0** | This document + `abd-context-graph/v1` schema stub | Agree ids, layout, verbs |
| **1** | Stable ids on `story-graph` nodes; `context-graph.json` manual links for one fixture | PawPlace mini |
| **2** | `context-graph-ops` CLI: `link`, `neighbors`, `validate`, `coverage` | Mirror `story-graph-ops` |
| **3** | `domain-graph.json` schema + domain skills emit on write | Alongside `domain.json` |
| **4** | `ux-graph.json` from IA / mockup skills | IA trace tables → links |
| **5** | `arch-graph.json` from blueprint / specification skills | Mechanism nodes + links |
| **6** | Read-gates on pilot skills (`abd-story-specification`, `abd-ux-mockup`, `abd-architecture-specification`) | Index-first context |
| **7** | Integrity scanners + eval fixtures for “ignored upstream link” | See `docs/Solution.md` promotion model |

---

## What this is not

- Not a graph database requirement — JSON in git is the source of truth.
- Not RDF / JSON-LD — typed view graphs + simple links are enough.
- Not edge-type proliferation — one link shape; semantics live in node kinds and optional `note`.
- Not a single mega-tree — each view keeps its own containment; context graph wires across them.
- Not replacing Markdown — projections stay for humans; graphs stay for machines and skills.

---

## Open questions

1. **ux-graph vs `state.json`** — when to merge navigation spine into state files vs separate `ux-graph.json`.
2. **Link symmetry** — store one direction only and infer reverse on read, or store both for clarity.
3. **Evidence links** — how `abd-context-semantic-index` chunk ids map into `context-graph` for brownfield traceability.
4. **Versioning** — optimistic concurrency on `context-graph.json` (same `--expect-sha` pattern as `story-graph-ops`).

---

## References

| Piece | Path |
| --- | --- |
| Context taxonomy (perspectives) | `common/context-taxonomy.md` |
| Folder conventions | `common/folder-conventions.md` |
| Story graph ops | `practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md` |
| Scenarios on story graph | `practices/story-driven-delivery/skills/abd-story-specification/rules/scenarios-on-story-graph.md` |
| Semantic context index | `practices/context-driven-delivery/skills/abd-context-semantic-index/SKILL.md` |
| Incomplete context discipline | `practices/story-driven-delivery/reference/handling-incomplete-context.md` |
| Eval / skill learning loop | `docs/Solution.md` |
