# UX Graph JSON — Schema and upstream mapping

Machine-readable spine for the UX perspective. Parallel to `story-graph.json` and `domain-model.json`.

**Canonical file:** `docs/ux/mockup/ux-graph.json`  
**Schema:** `abd-ux-graph/v1`

Human projections: `mockups.md`, per-screen `.md`, `.aria.yaml`, `.drawio` — generated or checked against the graph, not linked from it.

---

## Containment hierarchy

```text
ux-graph.json
└── flows[]
    └── screens[]
        └── regions[]          ← full wireframe state inline (name, slot, type, control fields)
connections[]                  ← navigation between screens
```

Same pattern as other view graphs — **containment only**, no typed cross-links, no path pointers to sibling artifacts:

| Story graph | Domain model | UX graph |
| --- | --- | --- |
| `product` | `product` | `product` |
| `epics[]` | `modules[]` | `flows[]` |
| `stories[]` | `classes[]` | `screens[]` |
| `acceptance_criteria[]` / `scenarios[]` | `properties[]` / `operations[]` | `regions[]` |
| `increments[]` | `relationships[]` | `connections[]` |

Cross-view traceability (story names on screens, domain terms on screens, paths to aria/spec/state files) does **not** belong in the graph — same as story-graph does not embed domain terms and domain-model does not embed story names.

---

## Root fields

| Field | Required | Meaning |
| --- | --- | --- |
| `schema` | yes | Always `"abd-ux-graph/v1"` |
| `product` | yes | System or product name |
| `scope` | yes | Flow, epic, or engagement scope |
| `flows` | yes | User flows containing screens |
| `connections` | yes | Directed navigation edges (may be empty) |

---

## Flow

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Flow name (matches epic or user journey) |
| `screens` | yes | Screens in this flow |

---

## Screen

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Screen display name (matches `connections[].from/to`) |
| `slug` | yes | Stable slug for semantic locators and generated filenames |
| `layout` | yes | `sidebar`, `split-screen`, `form`, `modal`, `flyout`, or `stack` |
| `col` | yes | Grid column for multi-screen drawio layout |
| `row` | yes | Grid row |
| `regions` | yes | Full wireframe regions for this screen (may be empty while outlining) |

---

## Region

Regions evolve from the `drawio-mockup.mjs` state format — all control detail lives **inline** on the region object.

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Region name (domain language) |
| `slot` | yes | `panel`, `body`, `left`, `right`, `header`, or `footer` |
| `type` | yes | Control/content type (see table below) |
| *(type fields)* | no | Placeholder, value, columns, rows, nodes, fields, buttons, etc. per type |

### Region types

From `abd-ux-mockup/reference/concepts.md` and `drawio-mockup.mjs`:

| `type` | Key fields |
| --- | --- |
| `tree` | `nodes[]` — `label`, `indent`, `expanded?`, `icon`, `selected?` |
| `listbox` | `items[]` — `label`, `icon`, `selected?`, `dimmed?` |
| `context-menu` | `groups[].items[]` — `label`, `shortcut` |
| `toolbar-icons` | `buttons[]` — `icon`, `tooltip`, `active?` |
| `filter-bar` | `placeholder`, `value` |
| `browse-panel` | `categories[]` — `label`, `icon` |
| `nav-tabs` | `tabs[]` — `label`, `active?` |
| `form` | `fields[]` — `label`, `input`, `options?`; `buttons[]` |
| `list` | `columns[]`, `rows`, `actions[]` |
| `toolbar` | `buttons[]` — `label` |
| `button-bar` | `buttons[]` — `label`, `primary?` |
| `chrome` | `name` |

### Layouts

`sidebar` | `split-screen` | `form` | `modal` | `flyout` | `stack`

---

## Connection

| Field | Required | Meaning |
| --- | --- | --- |
| `from` | yes | Source screen `name` |
| `to` | yes | Target screen `name` |
| `label` | yes | Transition label (domain language) |

---

## Upstream mapping

| Upstream | UX graph |
| --- | --- |
| IA `initial-ia.md` screen block | `flows[].screens[]` |
| IA region / layout | `layout`, `regions[]` |
| IA transitions | `connections[]` |
| Mockup design + aria work | inline `regions[]` control fields |

---

## Semantic pointer (for context-graph)

```text
flows/Shop in store/screens/Search Results
flows/Shop in store/screens/Search Results/regions/results list
```

---

## Templates

Practice-wide artifacts under `practices/user-experience-design/references/`:

| File | Purpose |
| --- | --- |
| `ux-graph-template.json` | `abd-ux-graph/v1` placeholder scaffold |
| `ux-graph-outline.json` | Minimal valid PawPlace graph |
| `ux-graph-example.json` | Filled PawPlace example with inline region state |
| `ux-graph-json.md` | This document |

Project scaffold: `common/context-scaffold/ux/mockup/ux-graph.json`

---

## drawio-mockup projection

`drawio-mockup.mjs` historically consumed a separate `state.json` bundle. When rendering from `ux-graph.json`, project the graph to the legacy bundle shape at the tool boundary (`target`, `screens[]`, `connections[]`) — the graph itself stays self-contained.

---

## ux-ops

Validate and lifecycle-manage `ux-graph.json`:

```bash
export PYTHONPATH="practices/user-experience-design/skills/supporting/ux-ops/scripts"
python3 practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py read --file docs/ux/mockup/ux-graph.json
```

See `skills/supporting/ux-ops/SKILL.md`.

---

## Relationship to delivery-graph solution

Canonical UX view spine is **`ux-graph.json`** — one self-contained file per view, same pattern as `story-graph.json` and `domain-model.json`. Legacy `state.json` and per-screen `*-state.json` may remain as render projections until mockup tooling reads the graph directly.
