---
name: abd-ux-user-impact-map
catalog_garden_tier: practice
catalog_garden_order: 5
catalogue_one_liner: >-
  Map who gets what value from this product — so you build for real outcomes not assumed ones.
description: >-
  Map organisational goals to actors, behaviour changes, and deliverable options via collaborative impact mapping. Use when connecting outcomes to scope or replacing feature-first backlogs.
context-perspective: ux
context-fidelity:
  - level: shaping
    mode: user-impact-map
---
# abd-ux-user-impact-map

## Purpose

Map who gets what value from this product — so you build for real outcomes, not assumed ones, and assumptions are visible before deciding build order.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **Goal vs feature** — Is your top-level goal a measurable business outcome, or a feature you've already decided to build?
- **Missing actor** — Who can block or undermine this goal that you haven't listed as an actor?
- **Impact vs task** — Are your impacts observable behaviour changes in the actor, or tasks the team needs to perform?
- **Deliverable attachment** — Does each deliverable serve exactly one impact, or are you bundling unrelated work under a convenient heading?
- **Assumption visibility** — Which build or outcome assumption would kill the initiative if wrong — and is it stated on the map?

---

## Output file

**Deliverables folder:** see `../common/skill-workflow.md` — Output file resolution.

**File name:** `impact-map.md` (and paired outputs). Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

Follow `../common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an impact map is, goal/actor/impact/deliverable definitions, goal and impact metrics, assumptions (build and outcome types), phased backlogs, and the shape of a good map.
- **`reference/examples.md`** — a worked hierarchy example (live-ops product) showing nested goals, actors, impacts with metrics, and phased deliverables.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/impact-map.md` | Hierarchy view: broader to finer `GOAL:` levels, then ACTOR / IMPACT / DELIVERABLE; optional `METRIC:` under goals and impacts; optional phased table. |
| `templates/impact-map.txt` | Same hierarchy tree and phased TSV (if any) as plain text. |
| `templates/impact-map-ascii.md` | ASCII wall sketch (four columns): OBJECTIVE (Why?) \| PERSONA (Who?) \| IMPACT (How?) \| INITIATIVE (What?). |
| `templates/impact-map-ascii.txt` | Same four-column table as plain text. |
| `templates/impact-map-hypotheses.md` | Build and outcome hypothesis sentences: same facts as the tree. `Then` clause uses goal as verb phrase with metric. |
| `templates/impact-map-hypotheses.txt` | Same hypothesis shape as plain text. |

**Parity:** Within each pair (hierarchy, ASCII, hypotheses), the `.md` and `.txt` versions match. Across all six files — same goal stack, actors, impacts, deliverables, and phased items. Impacts stay behavioural; each deliverable supports one impact; hypothesis lines use the same names as the hierarchy view.

**Quality bar:** Match the concepts in `reference/concepts.md` for structure. Use `rules/*.md` for generative wording (goal, impact, actor, deliverable, assumptions, phased backlog Actor / impact column).

**Depth:** Do not emit only Markdown or only plain text unless the user explicitly asks for a single format.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect the map as a product owner, developer, and facilitator would.

- **Goal** — Broader to finer `GOAL:` hierarchy; actors attach under the mapped `GOAL:`.
- **Actors** — Situational who (segment, moment, context); everyone who can help or block the goal.
- **Impacts** — Observable behaviour for each actor; verb-led, one movement per line.
- **Deliverables** — Each deliverable sits under an impact it serves; phased backlog rows each name an impact on this map.
- **Metrics** — `METRIC:` under a `GOAL:` holds lagging proof; `METRIC:` under an `IMPACT:` holds behaviour proxies.
- **Cross-artifact parity** — Hierarchy `.md` and `.txt` match; ASCII pair matches; hypotheses pair matches; all six align on goals, actors, impacts, and deliverables.
- **Rules pass** — Generated maps meet each `rules/*.md`.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
