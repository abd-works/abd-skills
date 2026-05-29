---
name: abd-kanban-planning
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  Strategy selection and system of work configuration — no pre-planned runs or slot tables.
description: >-
  Select delivery strategy, configure system of work (stages, scope progression,
  skill order), and define scatter/decomposition rules. Planning drives the Kanban
  board via strategy — not by pre-authoring runs, slots, or assignments.
---

# abd-kanban-planning

## When to use this skill

- You want to **select a delivery strategy** based on context and risk.
- You need to **configure a system of work** (stages, scope levels, ordered skills).
- You need to **define scatter rules** (how and when tickets decompose at scope boundaries).
- You want to **save a new reusable strategy** under `strategies/`.

Do **not** use this skill to produce artifacts (maps, slices, AC, tests, code). This skill configures *how* delivery flows — the system of work, strategy, and decomposition rules that drive the JIT Kanban board.

### Why delivery planning

Agents benefit from an explicit delivery lifecycle: not just *what* to do next, but **when scope changes**, **when to scatter**, **how to group work**, and **when to stop for feedback**. The strategy + system of work provide the spine without pre-planning every assignment.

- **Uncertainty is real** — keep the strategy living; update when corrections accumulate.
- **Risk before volume** — order increments so the hardest unknowns fail early.
- **JIT over pre-plan** — decompose only when needed, not everything upfront.
- **Humans in the loop** — checkpoint policy makes confirmation predictable.

---

## Core concepts

### System of work

A **system of work** defines the delivery pattern:

| Dimension | What it defines |
| --- | --- |
| **Stages** | Ordered sequence: shaping → discovery → exploration → specification → engineering |
| **Scope per stage** | Granularity of tickets at this stage: all, increment, sprint, story |
| **Skills per stage** | Ordered list of practice skills, with default role assignment |

The system of work is **static once configured**. It answers: "for any ticket at stage X, what skills run in what order?"

### Strategy

A **strategy** defines how work flows through the system:

| Dimension | What it defines |
| --- | --- |
| **Scope progression** | Which scope levels apply at each stage (may differ from default) |
| **Scatter rules** | When and how to decompose tickets at scope boundaries |
| **Sprint grouping** | How to group stories into sprints (default 3-4, adjustable) |
| **JIT policy** | How far ahead to scatter (next 1-2 items by default) |
| **Checkpoint policy** | Where to stop for feedback (per skill, per stage, per increment) |
| **Risk classification** | Which risks are present and how they affect ordering |

### Backlog

The backlog is **hierarchical** and **ordered**:

- Hierarchy comes from the story map (epics → sub-epics → stories)
- Order comes from thin-slicing priority
- Only decomposed as far as needed (JIT)
- Delivery lead or user can pre-decompose specific items

---

## Risk classification

Classify risks to inform strategy selection:

| Risk type | Meaning | Signals |
| --- | --- | --- |
| **Value risk** | Building the wrong thing | Vague briefs, no research, conflicting goals |
| **Technical risk** | Wrong tech, infra, or architecture | Proprietary APIs, unfamiliar stacks, scale unknowns |
| **Delivery risk** | Miss schedule or quality bar | Large scope, dependencies, deadlines |
| **Domain risk** | Misunderstand business rules | Regulatory regimes, complex rules, jargon |
| **Integration risk** | External systems constrain design | Legacy, quirky APIs, backward compat |
| **AI-model risk** | Agent likely to hallucinate | No training data, undocumented APIs |

Risk types drive strategy selection and checkpoint tightness.

---

## Strategy selection procedure

### Step 1 — Context analysis

Read all context. Identify:

1. **Known domains** — strong training data, documented APIs.
2. **Risky domains** — proprietary, internal, novel logic.
3. **Integration points** — external systems, dependencies.
4. **Complexity drivers** — regulatory, multi-actor, concurrency.
5. **Existing assets** — prior story graphs, specs, tests, code.

### Step 2 — Select strategy

1. Open `strategies/` in this skill folder.
2. Read each strategy's **When to use** section.
3. Match context and risks to a strategy (or blend multiple).
4. If no strategy fits, design custom — offer to save later.

### Step 3 — Configure system of work

From the selected strategy, write `system-of-work.json`:

- Which stages are active
- Scope level per stage
- Ordered skills per stage with role assignments
- Any optional skills (marked in strategy)

### Step 4 — Define scatter and decomposition rules

Write `strategy.md` in the war room with:

- **Scope progression**: which stages scatter vs advance
- **Sprint grouping**: how many stories per sprint (default 3-4)
- **JIT policy**: scatter next N only, or scatter all
- **Ordering**: priority source (story map, user override, risk-first)
- **Checkpoint policy**: per-skill, per-stage, or per-increment

### Step 5 — Present and confirm

Present to user:

1. Context assessment and classified risks.
2. Selected strategy (name, from which file, adaptations).
3. System of work table (stages, scope, skills).
4. Scatter rules and checkpoint policy.

**CHECKPOINT.** Wait for user confirm before setup.

---

## Delivery flow — stage sequence

| # | Stage | Default scope | Primary focus |
| --- | --- | --- | --- |
| 0 | Context | all | Convert, chunk, and embed source material for agent memory (optional) |
| 1 | Shaping | all | Story map, thin slices, module partition |
| 2 | Discovery | increment | Domain terms, UL, architecture, IA |
| 3 | Exploration | increment | UL refresh, AC, UX mockup, arch template |
| 4 | Specification | sprint | CRC, spec-by-example, scenario walkthrough |
| 5 | Engineering | sprint | Interface, object model, ATDD, clean code |

**Scope transitions** (scatter points):
- Context (all) → Shaping (all): same scope — advance, no scatter
- Shaping (all) → Discovery (increment): scatter by thin-slicing increments
- Exploration (increment) → Specification (sprint): scatter by sprint grouping

### Stage 0: Context (optional)

The context stage prepares source material for agent consumption. It is **optional** — skip when:

- Context is already small and readable (a few markdown files, a short brief)
- The team already has domain knowledge loaded
- The project is a bug fix or small story with no external documents

**Include when:**

- Source material is in office formats (PDF, PPTX, DOCX, XLSX) that agents cannot read directly
- There are many files that need indexing for semantic search
- The domain is complex and agents need RAG-backed retrieval during later stages
- Prior engagement material exists that should be searchable

**Skills (ordered, conditional):**

| Skill | When to include |
| --- | --- |
| `abd-convert-to-markdown` | Source files are PDF, PPTX, DOCX, XLSX, or other non-markdown formats |
| `abd-semantic-context-chunker` | Multiple source types; need to classify what context exists before chunking |
| `abd-chunk-markdown` | Large converted files need splitting for retrieval |
| `abd-embed-vectors` | Need semantic search (RAG) during later stages |

The kanban lead assesses source material at strategy selection and decides which context skills are needed (or skips the stage entirely).

Stage definitions: [`../../content/stages/README.md`](../../content/stages/README.md)

---

## Checkpoint granularity

| Level | When | Use for |
| --- | --- | --- |
| **Per skill** | After each skill completes on a ticket | High uncertainty, early work |
| **Per stage** | After all skills complete (stage exit gate) | Normal flow |
| **Per increment** | After increment tickets complete | Multi-increment review |

Default: start granular (per-skill), relax as confidence builds.

---

## Scatter rules (configurable per strategy)

### Default scatter heuristics

| Transition | Default rule |
| --- | --- |
| all → increment | One ticket per increment from thin-slicing. Scatter all. |
| increment → sprint | Group 3-4 stories per sprint. Scatter next 1-2 increments JIT. |
| sprint → story | Rare. Only if strategy requires per-story tickets. |

### User overrides

Users can specify:
- "Divide increment 1 into 3 sprints, increment 2 into 5 sprints"
- "Scatter all increments now"
- "Only scatter next 2"
- "Leave later increments until we know more"
- "Increment 1 sprint 1: story 1 then 2 then 3" (specific ordering)

### AI error rate adjustment

When AI output error rate is high (>10%):
- **Shrink scope**: move from increment-level to sprint-level or story-level
- Tighten checkpoints to per-skill
- After error rate drops, expand back

When error rate is low (<5%):
- **Expand scope**: move from sprint to increment across flows
- Relax checkpoints to per-stage

---

## Where to save

Strategy output is written to:

```text
<workspace>/docs/planning/delivery-war-room/
  system-of-work.json        # Stage + scope + skill definitions
  strategy.md                # Scope progression, scatter rules, checkpoint policy
  manifest.md                # WIP policy, autonomy, agent pool sizing
```

---

## Files in this skill

| File / path | Purpose |
| --- | --- |
| `SKILL.md` (this file) | Strategy selection, system of work, scatter rules, strategy catalog |
| `strategies/*.md` | One prepackaged strategy per file |
| `rules/*.md` | Plan quality rules |
| `scanners/plan-shape-scanner.py` | Validates strategy output |

---

## Bootcamp stages (canonical names)

| # | Stage | Default scope | Default role | Notes |
| --- | --- | --- | --- | --- |
| 0 | **context** | all | Engineer | Convert, chunk, embed source material (optional) |
| 1 | **shaping** | all | Product Owner | Story map, thin slices, module partition |
| 2 | **discovery** | increment | Product Owner | Domain → UL → architecture → IA |
| 3 | **exploration** | increment | Product Owner | UL → AC → UX mockup → arch template |
| 4 | **specification** | sprint | Product Owner | CRC → spec → walkthrough → interface → arch ref |
| 5 | **engineering** | sprint | Multi-role | interface impl → object model → ATDD → clean code |

## Team roles

Four roles: **Product Owner**, **Business Expert**, **UX Designer**, **Engineer**. [team-roles.md](../../content/roles/team-roles.md)

---

## Strategy file structure

Each strategy file in `strategies/` defines:

| Section | Content |
| --- | --- |
| **When to use** | Context signals and risk types that match this strategy |
| **Typical scope** | What boundary or area this applies to |
| **System of work** | Stages, scope per stage, skills per stage (table or reference to default) |
| **Scatter rules** | How tickets decompose at scope boundaries |
| **Sprint grouping** | Stories per sprint, grouping heuristics |
| **JIT policy** | How far ahead to decompose |
| **Checkpoint policy** | Where to stop for feedback |
| **Key constraints** | Non-negotiable rules for this strategy |

## Scope progression (scatter points)

| From | To | Scatter trigger |
| --- | --- | --- |
| Context (all) | Shaping (all) | Same scope — advance, no scatter |
| Shaping (all) | Discovery (increment) | Thin-slicing produces increments |
| Exploration (increment) | Specification (sprint) | DL groups stories into sprints |
| Specification (sprint) | Engineering (sprint) | Same scope — advance, no scatter |

---

## Strategy catalog

| File | When to use (summary) |
| --- | --- |
| [new-user-story.md](strategies/new-user-story.md) | 1–3 stories on existing solution |
| [new-thin-slice.md](strategies/new-thin-slice.md) | Vertical slice (~5–15 stories) |
| [new-initiative-no-documented-architecture.md](strategies/new-initiative-no-documented-architecture.md) | Greenfield; no architecture |
| [new-initiative-proprietary-technology-risk.md](strategies/new-initiative-proprietary-technology-risk.md) | Proprietary/undocumented systems |
| [new-initiative-business-user-experience-risk.md](strategies/new-initiative-business-user-experience-risk.md) | UX/domain risk dominant |
| [brownfield-current-state.md](strategies/brownfield-current-state.md) | Map and test existing system |
| [legacy-migration.md](strategies/legacy-migration.md) | Replace system; legacy is truth |
| [regulatory-compliance-heavy.md](strategies/regulatory-compliance-heavy.md) | Regulation/compliance dominates |
| [bug-fix.md](strategies/bug-fix.md) | Defect or regression |
| [spike-proof-of-concept.md](strategies/spike-proof-of-concept.md) | Answer one question before delivery |

---

## Adding a strategy

After a custom engagement, save a new `<slug>.md` in `strategies/` with the same sections. Reference bootcamp stages and scope levels. Include scatter rules and sprint grouping heuristics.

---

## Adapting a strategy

When selecting a strategy, adapt it:

1. **Add/remove stages** — bug fix skips shaping; spike skips engineering.
2. **Add/remove skills** — brownfield adds module partition; UX-heavy adds IA.
3. **Change scope levels** — if stories are huge, add sub-story scope.
4. **Override sprint grouping** — "2 stories per sprint for this complex area."
5. **Change JIT policy** — "scatter all increments now, we know the domain."
6. **Adjust checkpoints** — "per-skill for increment 1, per-stage after."
