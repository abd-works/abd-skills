---
name: abd-impact-mapping
catalog_garden_tier: practice
catalog_garden_order: 15
catalogue_one_liner: >-
  Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.
description: >-
  Teaches collaborative impact mapping — layered goals, actors, observable impacts, and deliverable
  options. Emits six template outputs (hierarchy, ASCII map, and BUILD/OUTCOME hypotheses, each in
  Markdown and plain text). Use when connecting organisational outcomes to scope, facilitating
  discovery, or replacing feature-first backlogs.
---
# abd-impact-mapping

## Purpose

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see *why* an option might matter before debating build order.

The map answers four questions in order: *Why are we doing this?* *Who can help or hinder?* *How should behaviour change?* *What could we do to support that change?* Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `impact-map.md` (and paired outputs). Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an impact map is, goal/actor/impact/deliverable definitions, goal and impact metrics, assumptions (build and outcome types), phased backlogs, and the shape of a good map.
- **`reference/examples.md`** — a worked hierarchy example (live-ops product) showing nested goals, actors, impacts with metrics, and phased deliverables.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

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

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-impact-mapping \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
