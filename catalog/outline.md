# ABD Skills & Agents — Catalogue Outline

> Auto-generated from repository `skills/` and `agents/`.
> Run `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` to refresh.

This outline mirrors the reader-facing style of `process-outline.md`:
each row gives a **short description** and where to open the source.

## Summary — Skills

| Skill | Description | Open |
| --- | --- | --- |
| **abd-acceptance-criteria** | WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for execute_rules. | [SKILL.md](../skills/abd-acceptance-criteria/SKILL.md) |
| **abd-acceptance-test-driven-development** | Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR). | [SKILL.md](../skills/abd-acceptance-test-driven-development/SKILL.md) |
| **abd-clean-code** | Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS). | [SKILL.md](../skills/abd-clean-code/SKILL.md) |
| **abd-delivery-planning** | Delivery plans only: context, risks, strategies, staged runs and checkpoints (not stories, tests, or code). | [SKILL.md](../skills/abd-delivery-planning/SKILL.md) |
| **abd-delivery-war-room** | Experimental file-based war room for handoffs between abd-delivery-lead and abd-team-member: delivery-war-room/ under the engagement workspace with INSTRUCTIONS.md, manifest.md, and slot-NN-start.md / slot-NN-finished.md. Not wired into the delivery-lead or team-member agents until re-integrated … | [SKILL.md](../skills/abd-delivery-war-room/SKILL.md) |
| **abd-impact-mapping** | Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources. | [SKILL.md](../skills/abd-impact-mapping/SKILL.md) |
| **abd-opportunity-canvas** | Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build. | [SKILL.md](../skills/abd-opportunity-canvas/SKILL.md) |
| **abd-simple-validated-learning** | Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build. | [SKILL.md](../skills/abd-simple-validated-learning/SKILL.md) |
| **abd-specification-by-example** | Given/When/Then scenarios with real domain values; plain or outline (data tables) templates. | [SKILL.md](../skills/abd-specification-by-example/SKILL.md) |
| **abd-story-mapping** | Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources. | [SKILL.md](../skills/abd-story-mapping/SKILL.md) |
| **abd-thin-slicing** | Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates. | [SKILL.md](../skills/abd-thin-slicing/SKILL.md) |
| **abd-commit-msg** | Commit messages from scope and changed files; no story_graph (/commit and similar). | [SKILL.md](../skills/commit-msg/SKILL.md) |
| **deploy-skill-to-cursor** | Junction-link a repo skill into Cursor user skills on Windows (no file copy). | [SKILL.md](../skills/deploy-skill-to-cursor/SKILL.md) |
| **drawio-story-sync** | story-graph.json to Draw.io story maps; validated load/save and diagram sync. | [SKILL.md](../skills/drawio-story-sync/SKILL.md) |
| **execute-rules** | Bundle rules into SKILL.md, run scanners, fix failures; quality gate before and after work. | [SKILL.md](../skills/execute_using_rules/SKILL.md) |
| **miro-story-sync** | story-graph.json to Miro story maps; validated load and REST-driven board sync. | [SKILL.md](../skills/miro-story-sync/SKILL.md) |
| **abd-ooad** | Turn specs, manuals, or messy sources into OO domain models (scan → extract → refine) with Draw.io. | [SKILL.md](../skills/ooad/SKILL.md) |
| **abd-proposal-respond** | RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG. | [SKILL.md](../skills/proposal-respond/SKILL.md) |
| **skill-garden-catalogue** | Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current. | [SKILL.md](../skills/skill-garden-catalogue/SKILL.md) |
| **story-graph-ops** | CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift. | [SKILL.md](../skills/story-graph-ops/SKILL.md) |
| **track-task** | Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace. | [SKILL.md](../skills/track_task/SKILL.md) |
| **workspace** | Set/read active_skill_workspace in skill-config; scripts resolve the engagement root. | [SKILL.md](../skills/workspace_skill/SKILL.md) |
| **abd-skill-catalog** | Regenerate the browsable skills/agents catalogue (HTML + outline) from repo packages. | [SKILL.md](../agents/abd-practice-skill-builder/skills/abd-skill-catalog/SKILL.md) |

## Summary — Agents

| Agent | Description | Open |
| --- | --- | --- |
| **abd-context-to-memory** | Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and semantic search. Optional: review context_chunking_spec.yaml before chunk+embed. | [AGENTS.md](../agents/abd-context-to-memory/AGENTS.md) |
| **abd-delivery-lead** | Orchestrates ABD delivery (workspace, plan, stages, handoffs); delegates work to abd-team-member; uses abd-delivery-planning to manage plan creation. | [AGENT.md](../agents/abd-delivery-lead/AGENT.md) |
| **abd-practice-skill-builder** | Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML … | [AGENTS.md](../agents/abd-practice-skill-builder/AGENTS.md) |
| **abd-team-member** | ABD executor for one role per turn (Product Owner, Analyst, or Engineer); requires team-role + workspace; produces stage artifacts via practice skills, often under abd-delivery-lead handoffs. | [AGENT.md](../agents/abd-team-member/AGENT.md) |
| **ai-research-assistant** | Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a research report that helps the user decide whether their approach is well-founded, exposed, or genuinely novel. You are an impartial advisor — not … | [AGENTS.md](../agents/ai-research-assistant/AGENTS.md) |

---

## Skills (detail)

### abd-acceptance-criteria

- **Directory:** [`skills/abd-acceptance-criteria/`](../skills/abd-acceptance-criteria/)

**Summary:**

WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for execute_rules.

**Description (from Purpose / body):**

Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit negatives (BUT). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

This skill is the practice standard for that work: templates for deliverables, rules for what “good” means (atomic AC, actor alternation, domain emphasis, channel-specific detail, source evidence when AC come from documents), and scanners that can run predictable mechanical checks alongside human review.

**Repository layout:**

- **[rules/](skill/abd-acceptance-criteria.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-acceptance-criteria/scanners)** — Folder (14 items).
- **[templates/](../skills/abd-acceptance-criteria/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-acceptance-criteria/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-acceptance-criteria/SKILL.html) — name: abd-acceptance-criteria

### abd-acceptance-test-driven-development

- **Directory:** [`skills/abd-acceptance-test-driven-development/`](../skills/abd-acceptance-test-driven-development/)

**Summary:**

Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR).

**Description (from Purpose / body):**

Write tests first. Write code to pass them.

This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is test-driven: write a test that expresses the expected behavior, run it to confirm it fails (RED), then rely on a  downstream skill or agent to develop the production code skill to implement until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do —  test methods show the Given-When-Then flow and helper functions do the work.

The skill covers the full test quality bar: domain language in names, observable-behavior assertions, coverage of normal and …

**Repository layout:**

- **[rules/](skill/abd-acceptance-test-driven-development.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-acceptance-test-driven-development/scanners)** — Folder (2 items).
- **[templates/](../skills/abd-acceptance-test-driven-development/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-acceptance-test-driven-development/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-acceptance-test-driven-development/SKILL.html) — name: abd-acceptance-test-driven-development

### abd-clean-code

- **Directory:** [`skills/abd-clean-code/`](../skills/abd-clean-code/)

**Summary:**

Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS).

**Description (from Purpose / body):**

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

The skill covers the full implementation quality bar: names that reveal intent, guard-clause control flow, no magic numbers, no swallowed exceptions, no hidden globals, encapsulated internals, and domain vocabulary throughout.

**Repository layout:**

- **[rules/](skill/abd-clean-code.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-clean-code/scanners)** — Folder (2 items).
- **[templates/](../skills/abd-clean-code/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-clean-code/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-clean-code/SKILL.html) — name: abd-clean-code

### abd-delivery-planning

- **Directory:** [`skills/abd-delivery-planning/`](../skills/abd-delivery-planning/)

**Summary:**

Delivery plans only: context, risks, strategies, staged runs and checkpoints (not stories, tests, or code).

**Description (from Purpose / body):**

Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice work).

**Repository layout:**

- **[rules/](skill/abd-delivery-planning.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-delivery-planning/scanners)** — Folder (3 items).
- **[scripts/](../skills/abd-delivery-planning/scripts)** — Build, catalogue, validation, or packaging automation.
- **[strategies/](../skills/abd-delivery-planning/strategies)** — Folder (9 items).
- **[tests/](../skills/abd-delivery-planning/tests)** — Folder (4 items).
- [README.md](doc/skill/abd-delivery-planning/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-delivery-planning/SKILL.html) — name: abd-delivery-planning

### abd-delivery-war-room

- **Directory:** [`skills/abd-delivery-war-room/`](../skills/abd-delivery-war-room/)

**Summary:**

Experimental file-based war room for handoffs between abd-delivery-lead and abd-team-member: delivery-war-room/ under the engagement workspace with INSTRUCTIONS.md, manifest.md, and slot-NN-start.md / slot-NN-finished.md. Not wired into the delivery-lead or team-member agents until re-integrated …

**Description (from Purpose / body):**

Reduce repeated paste handoffs between orchestrator and team-member threads by keeping state on disk under the engagement root.

**Repository layout:**

- [SKILL.md](doc/skill/abd-delivery-war-room/SKILL.html) — name: abd-delivery-war-room

### abd-impact-mapping

- **Directory:** [`skills/abd-impact-mapping/`](../skills/abd-impact-mapping/)

**Summary:**

Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.

**Description (from Purpose / body):**

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see why an option might matter before debating build order.

The map answers four questions in order (see Core concepts): Why are we doing this? Who can help or hinder? How should behaviour change? What could we do to support that change? Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

This skill defines the ideas behind a sound map, how to structure one, and what good looks like. Workspace layout, CLIs, and agent wiring belong in other skills.

**Repository layout:**

- **[inputs/](../skills/abd-impact-mapping/inputs)** — Folder (2 items).
- **[manual/](../skills/abd-impact-mapping/manual)** — Folder (0 items).
- **[rules/](skill/abd-impact-mapping.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../skills/abd-impact-mapping/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-impact-mapping/README.html) — catalogue_summary: "Impact maps: goal, actors, behaviour impacts, and deliverable options grounded in discovery."
- [SKILL.md](doc/skill/abd-impact-mapping/SKILL.html) — name: abd-impact-mapping

### abd-opportunity-canvas

- **Directory:** [`skills/abd-opportunity-canvas/`](../skills/abd-opportunity-canvas/)

**Summary:**

Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build.

**Description (from Purpose / body):**

This skill exists so you do not start "building a solution" while people are thinking about a different problem, a different customer, or a different definition of success. 

This skill makes an opportunity explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that downstream build and delivery work is based on a shared model. This skill captures this alignment as an opportunity model, in the form of a opportunity canvas.

Every part of the canvas is also a candidate assumption — beliefs about customers, value, and capability that teams often make explicit, turn into falsifiable statements, and run through a lightweight validation path outside this skill (see abd-simple-validated-learning). This skill’s job is to surface that uncertainty in the model; who …

**Repository layout:**

- **[rules/](skill/abd-opportunity-canvas.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../skills/abd-opportunity-canvas/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](doc/skill/abd-opportunity-canvas/SKILL.html) — name: abd-opportunity-canvas

### abd-simple-validated-learning

- **Directory:** [`skills/abd-simple-validated-learning/`](../skills/abd-simple-validated-learning/)

**Summary:**

Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.

**Description (from Purpose / body):**

Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. This skill is for surfacing those assumptions explicitly and working through them iteratively before the organisation treats them as fact or commits to a full build. The agent (or facilitator) mines the supplied context for assumptions, rewrites them as falsifiable hypotheses, prioritises them into a validation backlog, and structures each item to move through Plan → Validate → Learn.

The skill emphasises up-front discovery and validation:research, analysis, assessing current and target state (eg operations, finances, systems) validation with SMEs, deep dives, quick prototypes, cohort tests, and other relatively cheap validation activities. A longer build–measure–learn loop belongs in delivery practices once the …

**Repository layout:**

- **[inputs/](../skills/abd-simple-validated-learning/inputs)** — Folder (1 items).
- **[rules/](skill/abd-simple-validated-learning.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../skills/abd-simple-validated-learning/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-simple-validated-learning/README.html) — catalogue_summary: >-
- [SKILL.md](doc/skill/abd-simple-validated-learning/SKILL.html) — name: abd-simple-validated-learning

### abd-specification-by-example

- **Directory:** [`skills/abd-specification-by-example/`](../skills/abd-specification-by-example/)

**Summary:**

Given/When/Then scenarios with real domain values; plain or outline (data tables) templates.

**Description (from Purpose / body):**

Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

**Repository layout:**

- **[rules/](skill/abd-specification-by-example.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-specification-by-example/scanners)** — Folder (2 items).
- **[templates/](../skills/abd-specification-by-example/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-specification-by-example/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-specification-by-example/SKILL.html) — name: abd-specification-by-example

### abd-story-mapping

- **Directory:** [`skills/abd-story-mapping/`](../skills/abd-story-mapping/)

**Summary:**

Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources.

**Description (from Purpose / body):**

A story map in the Jeff Patton sense is a single shared picture of the product: you organize understanding into a small stack of nested levels—epics (broad capability areas), sub-epics (flows or feature areas within an epic), and stories (leaves: one observable user or system interaction each). The map is not a dump of source material, a WBS, or a list of build tasks; it is outcomes and behaviors—what happens in the product—so product, delivery, and domain people can read the same structure.

Naming is part of the model: epics, sub-epics, and stories use verb–noun titles; who is acting (persona/actor, user vs. system) is carried outside the name (e.g. story_type / diagram convention), not stuffed into the title. Good maps read as a journey (sequence along the backbone) and a skeleton of scope (depth into detail), with consistent language from top to bottom.

This document defines …

**Repository layout:**

- **[rules/](skill/abd-story-mapping.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-story-mapping/scanners)** — Folder (6 items).
- **[templates/](../skills/abd-story-mapping/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-story-mapping/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-story-mapping/SKILL.html) — name: abd-story-mapping

### abd-thin-slicing

- **Directory:** [`skills/abd-thin-slicing/`](../skills/abd-thin-slicing/)

**Summary:**

Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates.

**Description (from Purpose / body):**

Define prioritized increments. Group stories in a story map (and any notes on risk, constraints, or learning goals) into prioritized increments that can be delivered together. Each incremement includes its priority order, outcomes, slicing notes, and an ordered list od stories.

**Repository layout:**

- **[rules/](skill/abd-thin-slicing.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../skills/abd-thin-slicing/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/abd-thin-slicing/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/abd-thin-slicing/SKILL.html) — name: abd-thin-slicing

### abd-commit-msg

- **Directory:** [`skills/commit-msg/`](../skills/commit-msg/)

**Summary:**

Commit messages from scope and changed files; no story_graph (/commit and similar).

**Description (from Purpose / body):**

Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit.

**Repository layout:**

- **[content/](../skills/commit-msg/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../skills/commit-msg/docs)** — Human-oriented documentation for the package.
- **[rules/](skill/commit-msg.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../skills/commit-msg/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](doc/skill/commit-msg/AGENTS.html) — Core Definitions
- [README.md](doc/skill/commit-msg/README.html) — ace-commit-msg
- [skill-config.json](../skills/commit-msg/skill-config.json) — "name": "abd-commit-msg",
- [SKILL.md](doc/skill/commit-msg/SKILL.html) — name: abd-commit-msg

### deploy-skill-to-cursor

- **Directory:** [`skills/deploy-skill-to-cursor/`](../skills/deploy-skill-to-cursor/)

**Summary:**

Junction-link a repo skill into Cursor user skills on Windows (no file copy).

**Description (from Purpose / body):**

Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill.

**Repository layout:**

- **[scripts/](../skills/deploy-skill-to-cursor/scripts)** — Build, catalogue, validation, or packaging automation.
- [README.md](doc/skill/deploy-skill-to-cursor/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/deploy-skill-to-cursor/SKILL.html) — name: deploy-skill-to-cursor

### drawio-story-sync

- **Directory:** [`skills/drawio-story-sync/`](../skills/drawio-story-sync/)

**Summary:**

story-graph.json to Draw.io story maps; validated load/save and diagram sync.

**Description (from Purpose / body):**

Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance criteria, prioritization increments) from story-graph.json. Uses story-graph-ops for validated JSON load/save and story_graph_ops (StoryMap, nodes, domain) for the story tree that DrawIO rendering expects. Use when producing or diffing story-map.drawio files, or when wiring CI/scripts for diagram refresh and update reports.

**Repository layout:**

- **[.ruff_cache/](../skills/drawio-story-sync/.ruff_cache)** — Folder (2 items).
- **[scripts/](../skills/drawio-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../skills/drawio-story-sync/tests)** — Folder (4 items).
- [README.md](doc/skill/drawio-story-sync/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/drawio-story-sync/SKILL.html) — name: drawio-story-sync

### execute-rules

- **Directory:** [`skills/execute_using_rules/`](../skills/execute_using_rules/)

**Summary:**

Bundle rules into SKILL.md, run scanners, fix failures; quality gate before and after work.

**Description (from Purpose / body):**

Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.

**Repository layout:**

- **[scripts/](../skills/execute_using_rules/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/execute_using_rules/templates)** — Authoring templates and structural skeletons.
- **[tests/](../skills/execute_using_rules/tests)** — Folder (4 items).
- [README.md](doc/skill/execute_using_rules/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/execute_using_rules/SKILL.html) — name: execute-rules

### miro-story-sync

- **Directory:** [`skills/miro-story-sync/`](../skills/miro-story-sync/)

**Summary:**

story-graph.json to Miro story maps; validated load and REST-driven board sync.

**Description (from Purpose / body):**

Render and synchronize story-map Miro boards (outline today; exploration with acceptance criteria and prioritization increments planned) from story-graph.json. Reuses the common diagram_story_sync package (DiagramStoryNode ABCs, layout constants, comparison helpers, UpdateReport) and implements Miro-specific element creation, board I/O, and a pluggable MiroTransport (REST API v2 + in-memory fake for tests). Use when producing or refreshing Miro story maps from story-graph.json, or when wiring CI/scripts for Miro board updates.

**Repository layout:**

- **[scripts/](../skills/miro-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../skills/miro-story-sync/tests)** — Folder (3 items).
- [README.md](doc/skill/miro-story-sync/README.html) — catalogue_summary: "Render and synchronize story-map Miro boards (outline today; exploration with acceptance criteria and prioritization increments planned) from story-graph.json …
- [SKILL.md](doc/skill/miro-story-sync/SKILL.html) — name: miro-story-sync

### abd-ooad

- **Directory:** [`skills/ooad/`](../skills/ooad/)

**Summary:**

Turn specs, manuals, or messy sources into OO domain models (scan → extract → refine) with Draw.io.

**Description (from Purpose / body):**

Object-Oriented Analysis and Design (OOAD) from raw material. Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction, Refinement) with built-in Draw.io diagram generation via scripts/drawio_cli.py. ALWAYS use this skill when a user provides domain material and asks you to extract domain concepts, build class diagrams, identify responsibilities, or create object models. Create domain-scan-model.md and domain-scan-model.drawio files in the project workspace.

**Repository layout:**

- **[content/](../skills/ooad/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../skills/ooad/docs)** — Human-oriented documentation for the package.
- **[potential/](../skills/ooad/potential)** — Folder (4 items).
- **[runs/](../skills/ooad/runs)** — Folder (1 items).
- **[scripts/](../skills/ooad/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/ooad/templates)** — Authoring templates and structural skeletons.
- [_fix_md2.py](../skills/ooad/_fix_md2.py) — import re
- [AGENTS.md](doc/skill/ooad/AGENTS.html) — AGENTS — abd-ooad
- [README.md](doc/skill/ooad/README.html) — abd-diagrams
- [skill-config.json](../skills/ooad/skill-config.json) — "name": "abd-ooad",
- [SKILL.md](doc/skill/ooad/SKILL.html) — name: abd-ooad

### abd-proposal-respond

- **Directory:** [`skills/proposal-respond/`](../skills/proposal-respond/)

**Summary:**

RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG.

**Description (from Purpose / body):**

Respond to client proposals (RFP, Q&A, requirements) by converting materials to memory, creating a response strategy, and answering questions iteratively. Depends on abd-context-to-memory for RAG. Use when responding to proposals, creating response plans, answering RFP questions, or iterating on proposal strategy.

**Repository layout:**

- **[content/](../skills/proposal-respond/content)** — Source parts merged into agent instructions or outputs.
- **[rules/](skill/proposal-respond.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../skills/proposal-respond/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](doc/skill/proposal-respond/AGENTS.html) — Core Definitions
- [README.md](doc/skill/proposal-respond/README.html) — abd-proposal-respond
- [skill-config.json](../skills/proposal-respond/skill-config.json) — "name": "abd-proposal-respond",
- [SKILL.md](doc/skill/proposal-respond/SKILL.html) — name: abd-proposal-respond

### skill-garden-catalogue

- **Directory:** [`skills/skill-garden-catalogue/`](../skills/skill-garden-catalogue/)

**Summary:**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current.

**Description (from Purpose / body):**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current.

**Repository layout:**

- **[scripts/](../skills/skill-garden-catalogue/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/skill-garden-catalogue/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/skill/skill-garden-catalogue/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/skill-garden-catalogue/SKILL.html) — name: skill-garden-catalogue

### story-graph-ops

- **Directory:** [`skills/story-graph-ops/`](../skills/story-graph-ops/)

**Summary:**

CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift.

**Description (from Purpose / body):**

Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after hand-writing JSON from memory or from reading other repositories for “schema hints.” Prefer the story-graph CLI; use story_map and related modules for richer edits. Complements ABD practice skills—ops skill owns the serialized graph lifecycle on disk.

**Repository layout:**

- **[logs/](../skills/story-graph-ops/logs)** — Folder (1 items).
- **[scripts/](../skills/story-graph-ops/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../skills/story-graph-ops/tests)** — Folder (7 items).
- [MIGRATION_PARITY.md](doc/skill/story-graph-ops/MIGRATION_PARITY.html) — Story graph parity: agile_bots → story-graph-ops
- [README.md](doc/skill/story-graph-ops/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/story-graph-ops/SKILL.html) — name: story-graph-ops

### track-task

- **Directory:** [`skills/track_task/`](../skills/track_task/)

**Summary:**

Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace.

**Description (from Purpose / body):**

Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources.

**Repository layout:**

- **[scripts/](../skills/track_task/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../skills/track_task/tests)** — Folder (3 items).
- [README.md](doc/skill/track_task/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/track_task/SKILL.html) — name: track-task

### workspace

- **Directory:** [`skills/workspace_skill/`](../skills/workspace_skill/)

**Summary:**

Set/read active_skill_workspace in skill-config; scripts resolve the engagement root.

**Description (from Purpose / body):**

Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically.

**Repository layout:**

- **[scripts/](../skills/workspace_skill/scripts)** — Build, catalogue, validation, or packaging automation.
- [README.md](doc/skill/workspace_skill/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/skill/workspace_skill/SKILL.html) — name: workspace
- [Untitled](../skills/workspace_skill/Untitled) — workspace_skill

### abd-skill-catalog

- **Directory:** [`agents/abd-practice-skill-builder/skills/abd-skill-catalog/`](../agents/abd-practice-skill-builder/skills/abd-skill-catalog/)

**Summary:**

Regenerate the browsable skills/agents catalogue (HTML + outline) from repo packages.

**Description (from Purpose / body):**

Scan agilebydesign-skills (skills/ and agents/), maintain each package’s root README.md for catalogue copy (overview + ASCII), then regenerate catalog/ HTML and outline.md from those files plus a generated file tree.

**Repository layout:**

- **[scripts/](../agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../agents/abd-practice-skill-builder/skills/abd-skill-catalog/templates)** — Authoring templates and structural skeletons.
- [README.md](doc/agent/abd-practice-skill-builder/README.html) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](doc/agent/abd-practice-skill-builder/SKILL.html) — name: abd-skill-catalog

---

## Agents (detail)

### abd-context-to-memory

- **Directory:** [`agents/abd-context-to-memory/`](../agents/abd-context-to-memory/)
- **Entry:** [`agents/abd-context-to-memory/AGENTS.md`](../agents/abd-context-to-memory/AGENTS.md)

**Summary:**

Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and semantic search. Optional: review context_chunking_spec.yaml before chunk+embed.

**Description:**

Flow: turn source documents into Markdown (under markdown/ in the topic tree), draft a chunking strategy (context_chunking_spec.yaml), split into labeled chunks in memory/, embed into a local FAISS index under memory/rag/, then search semantically. Optionally pause after the spec so a human can review or edit the YAML before chunk + embed (strategy pass); otherwise run straight through. Hold basic quality across stages (real headings before chunking, sane splits after).

Per-stage detail: *skills/abd-/SKILL.md and each skill's references/**.

---

**Repository layout:**

- **[conf/](../agents/abd-context-to-memory/conf)** — Folder (0 items).
- **[content/](../agents/abd-context-to-memory/content)** — Source parts merged into agent instructions or outputs.
- **[scripts/](../agents/abd-context-to-memory/scripts)** — Build, catalogue, validation, or packaging automation.
- **[skills/](../agents/abd-context-to-memory/skills)** — Nested skills shipped inside an agent package.
- [AGENTS.md](doc/agent/abd-context-to-memory/AGENTS.html) — AGENTS — abd-context-to-memory
- [README.md](doc/agent/abd-context-to-memory/README.html) — catalogue_summary: >-
- [requirements-export.txt](../agents/abd-context-to-memory/requirements-export.txt) — Export: markdown → Excel, Word, PDF
- [requirements-rag.txt](../agents/abd-context-to-memory/requirements-rag.txt) — RAG (vector search) dependencies for ace-context-to-memory
- [skill-config.json](../agents/abd-context-to-memory/skill-config.json) — "name": "abd-context-to-memory",

### abd-delivery-lead

- **Directory:** [`agents/abd-delivery-lead/`](../agents/abd-delivery-lead/)
- **Entry:** [`agents/abd-delivery-lead/AGENT.md`](../agents/abd-delivery-lead/AGENT.md)

**Summary:**

Orchestrates ABD delivery (workspace, plan, stages, handoffs); delegates work to abd-team-member; uses abd-delivery-planning to manage plan creation.

**Description:**

# ABD Delivery Lead

You are a delivery lead agent orchestrating an Agile by Design (ABD) delivery flow.

You own the orchestration lifecycle: workspace, planning checkpoints (when to stop and confirm), sequencing runs and stages, bootstrapping abd-team-member agents, handoff gates, and cross-stage quality. You do not produce deliverables yourself — you delegate to team members with the right role, workspace, and practice skills.

Planning detail lives in the skill, not in this file. For every planning decision — what a plan and run are, how to assess context, risk types, strategies, example plans, and how to design runs — read abd-delivery-planning (skills/abd-delivery-planning/SKILL.md and the strategies/ folder — start with strategies/README.md, then the strategy file(s) that match …

**Repository layout:**

- **[docs/](../agents/abd-delivery-lead/docs)** — Human-oriented documentation for the package.
- **[stages/](../agents/abd-delivery-lead/stages)** — Folder (6 items).
- **[tests/](../agents/abd-delivery-lead/tests)** — Folder (3 items).
- [AGENT.md](doc/agent/abd-delivery-lead/AGENT.html) — ABD Delivery Lead
- [Deploy-ToCursor.ps1](../agents/abd-delivery-lead/Deploy-ToCursor.ps1) — .SYNOPSIS
- [README.md](doc/agent/abd-delivery-lead/README.html) — catalogue_summary: >-

### abd-practice-skill-builder

- **Directory:** [`agents/abd-practice-skill-builder/`](../agents/abd-practice-skill-builder/)
- **Entry:** [`agents/abd-practice-skill-builder/AGENTS.md`](../agents/abd-practice-skill-builder/AGENTS.md)

**Summary:**

Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML …

**Description:**

Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML manual (vendored shell assets in abd-practice-skill-manual).

Orchestrate using the agent-local packages in skills/ under this agent (same idea as abd-context-to-memory routing to nested skills/abd-/SKILL.md*).

---

**Repository layout:**

- **[progress/](../agents/abd-practice-skill-builder/progress)** — Folder (1 items).
- **[rules/](agent/abd-practice-skill-builder.html#entry-contents)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../agents/abd-practice-skill-builder/scripts)** — Build, catalogue, validation, or packaging automation.
- **[skills/](../agents/abd-practice-skill-builder/skills)** — Nested skills shipped inside an agent package.
- [AGENTS.md](doc/agent/abd-practice-skill-builder/AGENTS.html) — AGENTS — abd-practice-skill-builder
- [skill-config.json](../agents/abd-practice-skill-builder/skill-config.json) — "name": "abd-practice-skill-builder",

### abd-team-member

- **Directory:** [`agents/abd-team-member/`](../agents/abd-team-member/)
- **Entry:** [`agents/abd-team-member/AGENT.md`](../agents/abd-team-member/AGENT.md)

**Summary:**

ABD executor for one role per turn (Product Owner, Analyst, or Engineer); requires team-role + workspace; produces stage artifacts via practice skills, often under abd-delivery-lead handoffs.

**Description:**

# ABD Team Member

You are an ABD team member agent.

Setting: Every session is scoped by a team-role and a workspace (see Bootstrap inputs below). You play one role at a time—Product Owner, Analyst, or Engineer—not the whole delivery org. Typically abd-delivery-lead (or a human) opens your turn with that role, the engagement root, and any handoff brief; you execute stage work under that setting while the lead owns orchestration, gates, and plan/checklist alignment.

You sit in a delivery flow: you take the assigned team-role and own your slice of going from raw context to working software.

That means accepting handoffs from upstream, doing the work required for that role, and using the Agile by Design practice skills bundled with the role. You generate outputs (story graphs, specs …

**Repository layout:**

- **[roles/](../agents/abd-team-member/roles)** — Persona playbooks for multi-role agents.
- [AGENT.md](doc/agent/abd-team-member/AGENT.html) — ABD Team Member
- [Deploy-ToCursor.ps1](../agents/abd-team-member/Deploy-ToCursor.ps1) — .SYNOPSIS
- [README.md](doc/agent/abd-team-member/README.html) — catalogue_summary: >-

### ai-research-assistant

- **Directory:** [`agents/ai-research-assistant/`](../agents/ai-research-assistant/)
- **Entry:** [`agents/ai-research-assistant/AGENTS.md`](../agents/ai-research-assistant/AGENTS.md)

**Summary:**

Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a research report that helps the user decide whether their approach is well-founded, exposed, or genuinely novel. You are an impartial advisor — not …

**Description:**

Orchestrate hypothesis-driven research on AI-augmented delivery and context
engineering practices. You coordinate three skills in sequence to produce a
research report that helps the user decide whether their approach is
well-founded, exposed, or genuinely novel.

You are an impartial advisor — not a cheerleader. The user has explicitly
asked you to be the voice of reason, to go online, search your model knowledge,
and keep them from going in directions that are not well-established.

---

**Repository layout:**

- **[skills/](../agents/ai-research-assistant/skills)** — Nested skills shipped inside an agent package.
- [AGENTS.md](doc/agent/ai-research-assistant/AGENTS.html) — AGENTS — ai-research-assistant
- [README.md](doc/agent/ai-research-assistant/README.html) — catalogue_summary: "Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a …
