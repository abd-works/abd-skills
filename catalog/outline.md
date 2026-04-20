# ABD Skills & Agents — Catalogue Outline

> Auto-generated from repository `skills/` and `agents/`.
> Run `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` to refresh.

This outline mirrors the reader-facing style of `process-outline.md`:
each row gives a **short description** and where to open the source.

## Summary — Skills

| Skill | Description | Open |
| --- | --- | --- |
| **abd-acceptance-criteria** | Teaches exploration-phase acceptance criteria for story-graph.json: WHEN/THEN/AND/BUT, behavioral language, per-story domain terms, atomic AC, actor alternation, channel-specific detail, and verb–noun naming for story elements. Ships Markdown rules and Python scanners under this skill root for … | [SKILL.md](../skills/abd-acceptance-criteria/SKILL.md) |
| **abd-acceptance-test-driven-development** | Write tests first. Write code to pass them. This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should … | [SKILL.md](../skills/abd-acceptance-test-driven-development/SKILL.md) |
| **abd-clean-code** | Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design. This skill covers the full quality bar for implementation code: single-responsibility functions and classes, intention-revealing names, explicit constructor … | [SKILL.md](../skills/abd-clean-code/SKILL.md) |
| **abd-delivery-planning** | Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice … | [SKILL.md](../skills/abd-delivery-planning/SKILL.md) |
| **abd-skill-catalog** | Scan the agilebydesign-skills repository (root skills/ and agents/), then regenerate a reader-facing Markdown outline plus a small multi-page HTML site. Each skill and agent entry includes a short summary paragraph (for tables and cards) plus a longer description from ## Purpose when present … | [SKILL.md](../skills/abd-skill-catalog/SKILL.md) |
| **abd-specification-by-example** | Produce specification-by-example scenarios: concrete Given/When/Then steps with real domain values, bold concept names, italic values. Two templates: plain scenarios (inline values, default) and outline (same steps, multiple data rows). Use when writing BDD scenarios, refining AC into specs, or … | [SKILL.md](../skills/abd-specification-by-example/SKILL.md) |
| **abd-story-mapping** | Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and actors via story_type. When building a map from sources, outputs all template artifacts in templates/ (currently story-map.md and story-map.txt) with the same tree — not one or the other. Use when structuring … | [SKILL.md](../skills/abd-story-mapping/SKILL.md) |
| **abd-thin-slicing** | Produce thin-sliced delivery increments: vertical MVIs, spine vs optional paths, quality trade-offs, marketable increment names, and early risk validation. From a story map, write all template artifacts in templates/ (thin-slicing.md and thin-slicing.txt) with identical increment and story … | [SKILL.md](../skills/abd-thin-slicing/SKILL.md) |
| **abd-commit-msg** | Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit. | [SKILL.md](../skills/commit-msg/SKILL.md) |
| **deploy-skill-to-cursor** | Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill. | [SKILL.md](../skills/deploy-skill-to-cursor/SKILL.md) |
| **execute-rules** | Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after. | [SKILL.md](../skills/execute_using_rules/SKILL.md) |
| **abd-ooad** | Object-Oriented Analysis and Design (OOAD) from raw material. Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction … | [SKILL.md](../skills/ooad/SKILL.md) |
| **abd-proposal-respond** | Respond to client proposals (RFP, Q&A, requirements) by converting materials to memory, creating a response strategy, and answering questions iteratively. Depends on abd-context-to-memory for RAG. Use when responding to proposals, creating response plans, answering RFP questions, or iterating on … | [SKILL.md](../skills/proposal-respond/SKILL.md) |
| **skill-garden-catalogue** | Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current. | [SKILL.md](../skills/skill-garden-catalogue/SKILL.md) |
| **story-graph-ops** | Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after … | [SKILL.md](../skills/story-graph-ops/SKILL.md) |
| **track-task** | Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources. | [SKILL.md](../skills/track_task/SKILL.md) |
| **workspace** | Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically. | [SKILL.md](../skills/workspace_skill/SKILL.md) |

## Summary — Agents

| Agent | Description | Open |
| --- | --- | --- |
| **abd-context-to-memory** | Orchestrate convert → chunk → embed → search by coordinating this agent's skills. Decide when each stage runs, whether to use a strategy pass (review context_chunking_spec.yaml before chunk + embed) or straight-through, and hold cross-stage quality (real headings before chunking, sane splits after … | [AGENTS.md](../agents/abd-context-to-memory/AGENTS.md) |
| **ABD Delivery Lead** | You are a delivery lead agent orchestrating an Agile by Design (ABD) delivery flow. | [AGENT.md](../agents/abd-delivery-lead/AGENT.md) |
| **abd-skill-builder** | Provide portable repository standards aligned with Open Agent Skills: a focused SKILL.md for discovery, a merged AGENTS.md for multi-step workflow, plus documentation of build and validation (merge, build.py, scanners, CI), and a scaffold CLI so new skills match skills.sh-style layout without … | [AGENTS.md](../agents/abd-skill-builder/AGENTS.md) |
| **ABD Team Member** | You are an ABD team member agent. | [AGENT.md](../agents/abd-team-member/AGENT.md) |
| **ai-research-assistant** | Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a research report that helps the user decide whether their approach is well-founded, exposed, or genuinely novel. You are an impartial advisor — not … | [AGENTS.md](../agents/ai-research-assistant/AGENTS.md) |

---

## Skills (detail)

### abd-acceptance-criteria

- **Directory:** [`skills/abd-acceptance-criteria/`](../skills/abd-acceptance-criteria/)

**Summary:**

Teaches exploration-phase acceptance criteria for story-graph.json: WHEN/THEN/AND/BUT, behavioral language, per-story domain terms, atomic AC, actor alternation, channel-specific detail, and verb–noun naming for story elements. Ships Markdown rules and Python scanners under this skill root for …

**Description (from Purpose / body):**

Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit negatives (BUT). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

This skill is the practice standard for that work: templates for deliverables, rules for what “good” means (atomic AC, actor alternation, domain emphasis, channel-specific detail, source evidence when AC come from documents), and scanners that can run predictable mechanical checks alongside human review.

**Repository layout:**

- **[rules/](../skills/abd-acceptance-criteria/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-acceptance-criteria/scanners)** — Supporting folder (14 items).
- **[templates/](../skills/abd-acceptance-criteria/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-acceptance-criteria/SKILL.md) — name: abd-acceptance-criteria

### abd-acceptance-test-driven-development

- **Directory:** [`skills/abd-acceptance-test-driven-development/`](../skills/abd-acceptance-test-driven-development/)

**Summary:**

Write tests first. Write code to pass them. This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should …

**Description (from Purpose / body):**

Write tests first. Write code to pass them.

This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is test-driven: write a test that expresses the expected behavior, run it to confirm it fails (RED), then rely on a  downstream skill or agent to develop the production code skill to implement until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do —  test methods show the Given-When-Then flow and helper functions do the work.

The skill covers the full test quality bar: domain language in names, observable-behavior assertions, coverage of normal and …

**Repository layout:**

- **[rules/](../skills/abd-acceptance-test-driven-development/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-acceptance-test-driven-development/scanners)** — Supporting folder (2 items).
- **[templates/](../skills/abd-acceptance-test-driven-development/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-acceptance-test-driven-development/SKILL.md) — name: abd-acceptance-test-driven-development

### abd-clean-code

- **Directory:** [`skills/abd-clean-code/`](../skills/abd-clean-code/)

**Summary:**

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design. This skill covers the full quality bar for implementation code: single-responsibility functions and classes, intention-revealing names, explicit constructor …

**Description (from Purpose / body):**

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

The skill covers the full implementation quality bar: names that reveal intent, guard-clause control flow, no magic numbers, no swallowed exceptions, no hidden globals, encapsulated internals, and domain vocabulary throughout.

**Repository layout:**

- **[rules/](../skills/abd-clean-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-clean-code/scanners)** — Supporting folder (2 items).
- **[templates/](../skills/abd-clean-code/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-clean-code/SKILL.md) — name: abd-clean-code

### abd-delivery-planning

- **Directory:** [`skills/abd-delivery-planning/`](../skills/abd-delivery-planning/)

**Summary:**

Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice …

**Description (from Purpose / body):**

Build and revise agile delivery plans: context assessment, risk types, strategies (scan strategies/ for matching When to use), runs (stages, scope, checkpoints, rationale), and example plans. Planning only — not for producing story artifacts, tests, or code (those come from downstream practice work).

**Repository layout:**

- **[strategies/](../skills/abd-delivery-planning/strategies)** — Supporting folder (9 items).
- [SKILL.md](../skills/abd-delivery-planning/SKILL.md) — name: abd-delivery-planning

### abd-skill-catalog

- **Directory:** [`skills/abd-skill-catalog/`](../skills/abd-skill-catalog/)

**Summary:**

Scan the agilebydesign-skills repository (root skills/ and agents/), then regenerate a reader-facing Markdown outline plus a small multi-page HTML site. Each skill and agent entry includes a short summary paragraph (for tables and cards) plus a longer description from ## Purpose when present …

**Description (from Purpose / body):**

Scan the agilebydesign-skills repository (root skills/ and agents/), then regenerate a reader-facing Markdown outline plus a small multi-page HTML site. Each skill and agent entry includes a short summary paragraph (for tables and cards) plus a longer description from ## Purpose when present. Optional repository layout summarizes files (with links) and common folders in one line each.

**Repository layout:**

- **[scripts/](../skills/abd-skill-catalog/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/abd-skill-catalog/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-skill-catalog/SKILL.md) — name: abd-skill-catalog

### abd-specification-by-example

- **Directory:** [`skills/abd-specification-by-example/`](../skills/abd-specification-by-example/)

**Summary:**

Produce specification-by-example scenarios: concrete Given/When/Then steps with real domain values, bold concept names, italic values. Two templates: plain scenarios (inline values, default) and outline (same steps, multiple data rows). Use when writing BDD scenarios, refining AC into specs, or …

**Description (from Purpose / body):**

Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

**Repository layout:**

- **[rules/](../skills/abd-specification-by-example/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-specification-by-example/scanners)** — Supporting folder (2 items).
- **[templates/](../skills/abd-specification-by-example/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-specification-by-example/SKILL.md) — name: abd-specification-by-example

### abd-story-mapping

- **Directory:** [`skills/abd-story-mapping/`](../skills/abd-story-mapping/)

**Summary:**

Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and actors via story_type. When building a map from sources, outputs all template artifacts in templates/ (currently story-map.md and story-map.txt) with the same tree — not one or the other. Use when structuring …

**Description (from Purpose / body):**

Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and actors via story_type. When building a map from sources, outputs all template artifacts in templates/ (currently story-map.md and story-map.txt) with the same tree — not one or the other. Use when structuring product discovery, decomposing user journeys, identifying epics and flows, story mapping, organizing requirements into a hierarchical map, or when the user mentions story maps, epics, sub-epics, or Jeff Patton–style backlog structure.

**Repository layout:**

- **[rules/](../skills/abd-story-mapping/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../skills/abd-story-mapping/scanners)** — Supporting folder (7 items).
- **[templates/](../skills/abd-story-mapping/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-story-mapping/SKILL.md) — name: abd-story-mapping

### abd-thin-slicing

- **Directory:** [`skills/abd-thin-slicing/`](../skills/abd-thin-slicing/)

**Summary:**

Produce thin-sliced delivery increments: vertical MVIs, spine vs optional paths, quality trade-offs, marketable increment names, and early risk validation. From a story map, write all template artifacts in templates/ (thin-slicing.md and thin-slicing.txt) with identical increment and story …

**Description (from Purpose / body):**

Define prioritized increments. Group stories in a story map (and any notes on risk, constraints, or learning goals) into prioritized increments that can be delivered together. Each incremement includes its priority order, outcomes, slicing notes, and an ordered list od stories.

**Repository layout:**

- **[rules/](../skills/abd-thin-slicing/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../skills/abd-thin-slicing/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/abd-thin-slicing/SKILL.md) — name: abd-thin-slicing

### abd-commit-msg

- **Directory:** [`skills/commit-msg/`](../skills/commit-msg/)

**Summary:**

Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit.

**Description (from Purpose / body):**

Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit.

**Repository layout:**

- **[content/](../skills/commit-msg/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../skills/commit-msg/docs)** — Human-oriented documentation for the package.
- **[rules/](../skills/commit-msg/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../skills/commit-msg/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../skills/commit-msg/AGENTS.md) — Core Definitions
- [README.md](../skills/commit-msg/README.md) — ace-commit-msg
- [skill-config.json](../skills/commit-msg/skill-config.json) — "name": "abd-commit-msg",
- [SKILL.md](../skills/commit-msg/SKILL.md) — name: abd-commit-msg

### deploy-skill-to-cursor

- **Directory:** [`skills/deploy-skill-to-cursor/`](../skills/deploy-skill-to-cursor/)

**Summary:**

Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill.

**Description (from Purpose / body):**

Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill.

**Repository layout:**

- **[scripts/](../skills/deploy-skill-to-cursor/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../skills/deploy-skill-to-cursor/SKILL.md) — name: deploy-skill-to-cursor

### execute-rules

- **Directory:** [`skills/execute_using_rules/`](../skills/execute_using_rules/)

**Summary:**

Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.

**Description (from Purpose / body):**

Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.

**Repository layout:**

- **[scripts/](../skills/execute_using_rules/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/execute_using_rules/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/execute_using_rules/SKILL.md) — name: execute-rules

### abd-ooad

- **Directory:** [`skills/ooad/`](../skills/ooad/)

**Summary:**

Object-Oriented Analysis and Design (OOAD) from raw material. Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction …

**Description (from Purpose / body):**

Object-Oriented Analysis and Design (OOAD) from raw material. Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction, Refinement) with built-in Draw.io diagram generation via scripts/drawio_cli.py. ALWAYS use this skill when a user provides domain material and asks you to extract domain concepts, build class diagrams, identify responsibilities, or create object models. Create domain-scan-model.md and domain-scan-model.drawio files in the project workspace.

**Repository layout:**

- **[content/](../skills/ooad/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../skills/ooad/docs)** — Human-oriented documentation for the package.
- **[potential/](../skills/ooad/potential)** — Supporting folder (4 items).
- **[runs/](../skills/ooad/runs)** — Supporting folder (1 items).
- **[scripts/](../skills/ooad/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/ooad/templates)** — Authoring templates and structural skeletons.
- [_fix_md2.py](../skills/ooad/_fix_md2.py) — import re
- [AGENTS.md](../skills/ooad/AGENTS.md) — AGENTS — abd-ooad
- [README.md](../skills/ooad/README.md) — abd-diagrams
- [skill-config.json](../skills/ooad/skill-config.json) — "name": "abd-ooad",
- [SKILL.md](../skills/ooad/SKILL.md) — name: abd-ooad

### abd-proposal-respond

- **Directory:** [`skills/proposal-respond/`](../skills/proposal-respond/)

**Summary:**

Respond to client proposals (RFP, Q&A, requirements) by converting materials to memory, creating a response strategy, and answering questions iteratively. Depends on abd-context-to-memory for RAG. Use when responding to proposals, creating response plans, answering RFP questions, or iterating on …

**Description (from Purpose / body):**

Respond to client proposals (RFP, Q&A, requirements) by converting materials to memory, creating a response strategy, and answering questions iteratively. Depends on abd-context-to-memory for RAG. Use when responding to proposals, creating response plans, answering RFP questions, or iterating on proposal strategy.

**Repository layout:**

- **[content/](../skills/proposal-respond/content)** — Source parts merged into agent instructions or outputs.
- **[rules/](../skills/proposal-respond/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../skills/proposal-respond/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../skills/proposal-respond/AGENTS.md) — Core Definitions
- [README.md](../skills/proposal-respond/README.md) — abd-proposal-respond
- [skill-config.json](../skills/proposal-respond/skill-config.json) — "name": "abd-proposal-respond",
- [SKILL.md](../skills/proposal-respond/SKILL.md) — name: abd-proposal-respond

### skill-garden-catalogue

- **Directory:** [`skills/skill-garden-catalogue/`](../skills/skill-garden-catalogue/)

**Summary:**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current.

**Description (from Purpose / body):**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current.

**Repository layout:**

- **[scripts/](../skills/skill-garden-catalogue/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../skills/skill-garden-catalogue/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../skills/skill-garden-catalogue/SKILL.md) — name: skill-garden-catalogue

### story-graph-ops

- **Directory:** [`skills/story-graph-ops/`](../skills/story-graph-ops/)

**Summary:**

Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after …

**Description (from Purpose / body):**

Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after hand-writing JSON from memory or from reading other repositories for “schema hints.” Prefer the story-graph CLI; use story_map and related modules for richer edits. Complements ABD practice skills—ops skill owns the serialized graph lifecycle on disk.

**Repository layout:**

- **[scripts/](../skills/story-graph-ops/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../skills/story-graph-ops/SKILL.md) — name: story-graph-ops

### track-task

- **Directory:** [`skills/track_task/`](../skills/track_task/)

**Summary:**

Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources.

**Description (from Purpose / body):**

Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources.

**Repository layout:**

- **[scripts/](../skills/track_task/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../skills/track_task/SKILL.md) — name: track-task

### workspace

- **Directory:** [`skills/workspace_skill/`](../skills/workspace_skill/)

**Summary:**

Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically.

**Description (from Purpose / body):**

Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically.

**Repository layout:**

- **[scripts/](../skills/workspace_skill/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../skills/workspace_skill/SKILL.md) — name: workspace
- [Untitled](../skills/workspace_skill/Untitled) — workspace_skill

---

## Agents (detail)

### abd-context-to-memory

- **Directory:** [`agents/abd-context-to-memory/`](../agents/abd-context-to-memory/)
- **Entry:** [`agents/abd-context-to-memory/AGENTS.md`](../agents/abd-context-to-memory/AGENTS.md)

**Summary:**

Orchestrate convert → chunk → embed → search by coordinating this agent's skills. Decide when each stage runs, whether to use a strategy pass (review context_chunking_spec.yaml before chunk + embed) or straight-through, and hold cross-stage quality (real headings before chunking, sane splits after …

**Description:**

Orchestrate convert → chunk → embed → search by coordinating this agent's skills. Decide when each stage runs, whether to use a strategy pass (review context_chunking_spec.yaml before chunk + embed) or straight-through, and hold cross-stage quality (real headings before chunking, sane splits after chunking).

Per-stage procedures: *skills/abd-/SKILL.md and each skill's references/**.

---

**Repository layout:**

- **[conf/](../agents/abd-context-to-memory/conf)** — Supporting folder (1 items).
- **[content/](../agents/abd-context-to-memory/content)** — Source parts merged into agent instructions or outputs.
- **[scripts/](../agents/abd-context-to-memory/scripts)** — Build, catalogue, validation, or packaging automation.
- **[skills/](../agents/abd-context-to-memory/skills)** — Nested skills shipped inside an agent package.
- [AGENTS.md](../agents/abd-context-to-memory/AGENTS.md) — AGENTS — abd-context-to-memory
- [requirements-export.txt](../agents/abd-context-to-memory/requirements-export.txt) — Export: markdown → Excel, Word, PDF
- [requirements-rag.txt](../agents/abd-context-to-memory/requirements-rag.txt) — RAG (vector search) dependencies for ace-context-to-memory
- [skill-config.json](../agents/abd-context-to-memory/skill-config.json) — "name": "abd-context-to-memory",

### ABD Delivery Lead

- **Directory:** [`agents/abd-delivery-lead/`](../agents/abd-delivery-lead/)
- **Entry:** [`agents/abd-delivery-lead/AGENT.md`](../agents/abd-delivery-lead/AGENT.md)

**Summary:**

You are a delivery lead agent orchestrating an Agile by Design (ABD) delivery flow.

**Description:**

# ABD Delivery Lead

You are a delivery lead agent orchestrating an Agile by Design (ABD) delivery flow.

You own the orchestration lifecycle: workspace, planning checkpoints (when to stop and confirm), sequencing runs and stages, bootstrapping abd-team-member agents, handoff gates, and cross-stage quality. You do not produce deliverables yourself — you delegate to team members with the right role, workspace, and practice skills.

Planning detail lives in the skill, not in this file. For every planning decision — what a plan and run are, how to assess context, risk types, strategies, example plans, and how to design runs — read abd-delivery-planning (skills/abd-delivery-planning/SKILL.md and the strategies/ folder — start with strategies/README.md, then the strategy file(s) that match …

**Repository layout:**

- **[docs/](../agents/abd-delivery-lead/docs)** — Human-oriented documentation for the package.
- **[scripts/](../agents/abd-delivery-lead/scripts)** — Build, catalogue, validation, or packaging automation.
- **[stages/](../agents/abd-delivery-lead/stages)** — Supporting folder (6 items).
- [AGENT.md](../agents/abd-delivery-lead/AGENT.md) — ABD Delivery Lead
- [Deploy-ToCursor.ps1](../agents/abd-delivery-lead/Deploy-ToCursor.ps1) — .SYNOPSIS

### abd-skill-builder

- **Directory:** [`agents/abd-skill-builder/`](../agents/abd-skill-builder/)
- **Entry:** [`agents/abd-skill-builder/AGENTS.md`](../agents/abd-skill-builder/AGENTS.md)

**Summary:**

Provide portable repository standards aligned with Open Agent Skills: a focused SKILL.md for discovery, a merged AGENTS.md for multi-step workflow, plus documentation of build and validation (merge, build.py, scanners, CI), and a scaffold CLI so new skills match skills.sh-style layout without …

**Description:**

Provide portable repository standards aligned with Open Agent Skills: a focused SKILL.md for discovery, a merged AGENTS.md for multi-step workflow, plus documentation of build and validation (merge, build.py, scanners, CI), and a scaffold CLI so new skills match skills.sh-style layout without hand-copying fixtures.


---

**Repository layout:**

- **[content/](../agents/abd-skill-builder/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../agents/abd-skill-builder/docs)** — Human-oriented documentation for the package.
- **[scripts/](../agents/abd-skill-builder/scripts)** — Build, catalogue, validation, or packaging automation.
- **[skills/](../agents/abd-skill-builder/skills)** — Nested skills shipped inside an agent package.
- **[test/](../agents/abd-skill-builder/test)** — Automated tests for the agent or skill package.
- [.gitignore](../agents/abd-skill-builder/.gitignore) — Live workflow checklists from python scripts/base/generate.py --phase <slug> when
- [AGENTS.md](../agents/abd-skill-builder/AGENTS.md) — AGENTS — abd-skill-builder
- [requirements-dev.txt](../agents/abd-skill-builder/requirements-dev.txt) — Dev-only: pytest for smoke tests (see test/README.md)
- [skill-config.json](../agents/abd-skill-builder/skill-config.json) — "name": "abd-skill-builder",
- [SKILL.md](../agents/abd-skill-builder/SKILL.md) — name: abd-skill-builder

### ABD Team Member

- **Directory:** [`agents/abd-team-member/`](../agents/abd-team-member/)
- **Entry:** [`agents/abd-team-member/AGENT.md`](../agents/abd-team-member/AGENT.md)

**Summary:**

You are an ABD team member agent.

**Description:**

# ABD Team Member

You are an ABD team member agent.

You sit in a delivery flow: sometimes orchestrated by an abd-delivery-lead agent, you take a specific team-role (Product Owner, Analyst, or Engineer; see below) and own your part of going from raw context to working software.

This means accepting handoffs from upstream, doing the work required based on your specific role, and using the by Design practice skills that come with that role. You generate outputs (story graphs, specs, tests, code, etc.) so they are available for downstream agents or the user can continue work required to achieve this outcome.

## Bootstrap inputs (required from outside)

Every session MUST be given both of the following. If either is missing, ask once, then proceed with stated assumptions only if the user …

**Repository layout:**

- **[roles/](../agents/abd-team-member/roles)** — Persona playbooks for multi-role agents.
- [AGENT.md](../agents/abd-team-member/AGENT.md) — ABD Team Member
- [Deploy-ToCursor.ps1](../agents/abd-team-member/Deploy-ToCursor.ps1) — .SYNOPSIS

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
- [AGENTS.md](../agents/ai-research-assistant/AGENTS.md) — AGENTS — ai-research-assistant
