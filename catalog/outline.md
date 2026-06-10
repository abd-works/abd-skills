# Foundry — plugins, skills & agents

> Auto-generated from repository **plugins** (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).
> Run `python foundational/skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` to refresh.

Each row gives a **short description** and where to open the source.

## Plugins

Repo-root capability plugins (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).

| Plugin | Summary | Open |
| --- | --- | --- |
| **Kanban** (`kanban/`) | 5 agents, 5 skills, 2 instructions, 10 prompts | [README.md](../practices/kanban/README.md) |
| **Story Driven Delivery** (`story-driven-delivery/`) | 8 skills, 2 instructions, 10 lib | [README.md](../practices/story-driven-delivery/README.md) |
| **Domain Driven Design** (`domain-driven-design/`) | 9 skills, 1 instructions | [README.md](../practices/domain-driven-design/README.md) |
| **Architecture Centric Engineering** (`architecture-centric-engineering/`) | 4 skills | [README.md](../practices/architecture-centric-engineering/README.md) |
| **Idea Shaping** (`idea-shaping/`) | Opportunity framing, impact mapping, cost of delay, and validated learning — before delivery work begins. | [README.md](../practices/idea-shaping/README.md) |
| **User Experience Design** (`user-experience-design/`) | 6 skills | [README.md](../practices/user-experience-design/README.md) |
| **Context To Memory** (`context-to-memory/`) | Convert office documents to markdown, chunk for retrieval, embed vectors, and search memory. | [README.md](../foundational/context-to-memory/README.md) |
| **Skill Builder** (`skill-builder/`) | Practice skills for authoring ABD practice packages: query hub sources, author SKILL.md + rules, build scanners, maintain the AI Garden catalog, and publish HTML manuals. | [README.md](../foundational/skill-builder/README.md) |
| **Skill Helpers** (`skill-helpers/`) | Infrastructure skills and cross-cutting helpers used across practice families. | [README.md](../foundational/skill-helpers/README.md) |
| **Utilities** (`utilities/`) | Proposal response, AI research assistant skills, and related utilities. | [README.md](../utilities/README.md) |

### Plugin layout (detail)

#### Kanban — `kanban/`

5 agents, 5 skills, 2 instructions, 10 prompts

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- **business-expert** — [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md)
- **engineer** — [AGENT.md](../practices/kanban/agents/engineer/AGENT.md)
- **kanban-lead** — [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md)
- **product-owner** — [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md)
- **ux-designer** — [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md)

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-kanban** — [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md)
- **abd-kanban-handoff** — [SKILL.md](../practices/kanban/skills/abd-kanban-handoff/SKILL.md)
- **abd-kanban-planning** — [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md)
- **abd-kanban-repo** — [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md)
- **kanban-estimation** — [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `kanban/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **kanban-git** — [kanban-git.instructions.md](../practices/kanban/instructions/kanban-git.instructions.md) (catalog: `instructions/kanban--instructions--kanban-git-instructions-md.html`)
- **sync-generated-artifacts** — [sync-generated-artifacts.instructions.md](../practices/kanban/instructions/sync-generated-artifacts.instructions.md) (catalog: `instructions/kanban--instructions--sync-generated-artifacts-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- **abd-feature** — [abd-feature.prompt.md](../practices/kanban/prompts/abd-feature.prompt.md) (catalog: `prompts/kanban--prompts--abd-feature-prompt-md.html`)
- **abd-fix-defect** — [abd-fix-defect.prompt.md](../practices/kanban/prompts/abd-fix-defect.prompt.md) (catalog: `prompts/kanban--prompts--abd-fix-defect-prompt-md.html`)
- **abd-kanban-handoff** — [abd-kanban-handoff.prompt.md](../practices/kanban/prompts/abd-kanban-handoff.prompt.md) (catalog: `prompts/kanban--prompts--abd-kanban-handoff-prompt-md.html`)
- **abd-run-discovery** — [abd-run-discovery.prompt.md](../practices/kanban/prompts/abd-run-discovery.prompt.md) (catalog: `prompts/kanban--prompts--abd-run-discovery-prompt-md.html`)
- **abd-run-engineering** — [abd-run-engineering.prompt.md](../practices/kanban/prompts/abd-run-engineering.prompt.md) (catalog: `prompts/kanban--prompts--abd-run-engineering-prompt-md.html`)
- **abd-run-exploration** — [abd-run-exploration.prompt.md](../practices/kanban/prompts/abd-run-exploration.prompt.md) (catalog: `prompts/kanban--prompts--abd-run-exploration-prompt-md.html`)
- **abd-run-shaping** — [abd-run-shaping.prompt.md](../practices/kanban/prompts/abd-run-shaping.prompt.md) (catalog: `prompts/kanban--prompts--abd-run-shaping-prompt-md.html`)
- **abd-run-specification** — [abd-run-specification.prompt.md](../practices/kanban/prompts/abd-run-specification.prompt.md) (catalog: `prompts/kanban--prompts--abd-run-specification-prompt-md.html`)
- **keyquestions** — [keyquestions.prompt.md](../practices/kanban/prompts/keyquestions.prompt.md) (catalog: `prompts/kanban--prompts--keyquestions-prompt-md.html`)
- **sync-upstream** — [sync-upstream.prompt.md](../practices/kanban/prompts/sync-upstream.prompt.md) (catalog: `prompts/kanban--prompts--sync-upstream-prompt-md.html`)

**Lib — shared Python packages**

- _(empty `kanban/lib/`)_

**Scripts — package-level automation**

- _(empty `kanban/scripts/`)_

---

#### Story Driven Delivery — `story-driven-delivery/`

8 skills, 2 instructions, 10 lib

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `story-driven-delivery/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-story-acceptance-criteria** — [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/SKILL.md)
- **abd-story-acceptance-test** — [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-test/SKILL.md)
- **abd-story-mapping** — [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md)
- **abd-story-specification** — [SKILL.md](../practices/story-driven-delivery/skills/abd-story-specification/SKILL.md)

**Supporting skills** (`skills/supporting/`)

- **abd-thin-slicing** — [SKILL.md](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/SKILL.md)
- **drawio-story-sync** — [SKILL.md](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/SKILL.md)
- **miro-story-sync** — [SKILL.md](../practices/story-driven-delivery/skills/supporting/miro-story-sync/SKILL.md)
- **story-graph-ops** — [SKILL.md](../practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `story-driven-delivery/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **drawio-story-sync** — [drawio-story-sync.instructions.md](../practices/story-driven-delivery/instructions/drawio-story-sync.instructions.md) (catalog: `instructions/story-driven-delivery--instructions--drawio-story-sync-instructions-md.html`)
- **story-graph-ops** — [story-graph-ops.instructions.md](../practices/story-driven-delivery/instructions/story-graph-ops.instructions.md) (catalog: `instructions/story-driven-delivery--instructions--story-graph-ops-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- _(empty `story-driven-delivery/prompts/`)_

**Lib — shared Python packages**

- [practices/story-driven-delivery/lib/diagram_story_sync/__init__.py](../practices/story-driven-delivery/lib/diagram_story_sync/__init__.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/bootstrap.py](../practices/story-driven-delivery/lib/diagram_story_sync/bootstrap.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/diagram_story_node.py](../practices/story-driven-delivery/lib/diagram_story_sync/diagram_story_node.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/layout_constants.py](../practices/story-driven-delivery/lib/diagram_story_sync/layout_constants.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/layout_data.py](../practices/story-driven-delivery/lib/diagram_story_sync/layout_data.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/node_comparison.py](../practices/story-driven-delivery/lib/diagram_story_sync/node_comparison.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/position.py](../practices/story-driven-delivery/lib/diagram_story_sync/position.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/render_summary.py](../practices/story-driven-delivery/lib/diagram_story_sync/render_summary.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/style_defaults.py](../practices/story-driven-delivery/lib/diagram_story_sync/style_defaults.py)
- [practices/story-driven-delivery/lib/diagram_story_sync/update_report.py](../practices/story-driven-delivery/lib/diagram_story_sync/update_report.py)

**Scripts — package-level automation**

- _(empty `story-driven-delivery/scripts/`)_

---

#### Domain Driven Design — `domain-driven-design/`

9 skills, 1 instructions

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `domain-driven-design/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-domain-code** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-code/SKILL.md)
- **abd-domain-glossary** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-glossary/SKILL.md)
- **abd-domain-language** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-language/SKILL.md)
- **abd-domain-model** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-model/SKILL.md)
- **abd-domain-specification** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-specification/SKILL.md)

**Supporting skills** (`skills/supporting/`)

- **abd-bounded-context-map** — [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/SKILL.md)
- **abd-ddd-design-building-blocks** — [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/SKILL.md)
- **abd-domain-walk** — [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-domain-walk/SKILL.md)
- **drawio-domain-sync** — [SKILL.md](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `domain-driven-design/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **ddd-building-blocks-fidelity-upgrade** — [ddd-building-blocks-fidelity-upgrade.instructions.md](../practices/domain-driven-design/instructions/ddd-building-blocks-fidelity-upgrade.instructions.md) (catalog: `instructions/domain-driven-design--instructions--ddd-building-blocks-fidelity-upgrade-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- _(empty `domain-driven-design/prompts/`)_

**Lib — shared Python packages**

- _(empty `domain-driven-design/lib/`)_

**Scripts — package-level automation**

- _(empty `domain-driven-design/scripts/`)_

---

#### Architecture Centric Engineering — `architecture-centric-engineering/`

4 skills

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `architecture-centric-engineering/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-architecture-blueprint** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md)
- **abd-architecture-code** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-code/SKILL.md)
- **abd-architecture-outline** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md)
- **abd-architecture-specification** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-specification/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `architecture-centric-engineering/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- _(empty `architecture-centric-engineering/instructions/`)_

**Prompts — .prompt.md → slash commands**

- _(empty `architecture-centric-engineering/prompts/`)_

**Lib — shared Python packages**

- _(empty `architecture-centric-engineering/lib/`)_

**Scripts — package-level automation**

- _(empty `architecture-centric-engineering/scripts/`)_

---

#### Idea Shaping — `idea-shaping/`

Opportunity framing, impact mapping, cost of delay, and validated learning — before delivery work begins.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `idea-shaping/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-cost-of-delay** — [SKILL.md](../practices/idea-shaping/skills/abd-cost-of-delay/SKILL.md)
- **abd-opportunity-generation** — [SKILL.md](../practices/idea-shaping/skills/abd-opportunity-generation/SKILL.md)
- **abd-simple-validated-learning** — [SKILL.md](../practices/idea-shaping/skills/abd-simple-validated-learning/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `idea-shaping/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- _(empty `idea-shaping/instructions/`)_

**Prompts — .prompt.md → slash commands**

- _(empty `idea-shaping/prompts/`)_

**Lib — shared Python packages**

- _(empty `idea-shaping/lib/`)_

**Scripts — package-level automation**

- _(empty `idea-shaping/scripts/`)_

---

#### User Experience Design — `user-experience-design/`

6 skills

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `user-experience-design/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-information-architecture** — [SKILL.md](../practices/user-experience-design/skills/abd-information-architecture/SKILL.md)
- **abd-ux-design** — [SKILL.md](../practices/user-experience-design/skills/abd-ux-design/SKILL.md)
- **abd-ux-information-architecture** — [SKILL.md](../practices/user-experience-design/skills/abd-ux-information-architecture/SKILL.md)
- **abd-ux-mockup** — [SKILL.md](../practices/user-experience-design/skills/abd-ux-mockup/SKILL.md)
- **abd-ux-specification** — [SKILL.md](../practices/user-experience-design/skills/abd-ux-specification/SKILL.md)
- **abd-ux-user-impact-map** — [SKILL.md](../practices/user-experience-design/skills/abd-ux-user-impact-map/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `user-experience-design/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- _(empty `user-experience-design/instructions/`)_

**Prompts — .prompt.md → slash commands**

- _(empty `user-experience-design/prompts/`)_

**Lib — shared Python packages**

- _(empty `user-experience-design/lib/`)_

**Scripts — package-level automation**

- _(empty `user-experience-design/scripts/`)_

---

#### Context To Memory — `context-to-memory/`

Convert office documents to markdown, chunk for retrieval, embed vectors, and search memory.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- **abd-context-to-memory** — [AGENTS.md](../foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md)

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-chunk-markdown** — [SKILL.md](../foundational/context-to-memory/skills/abd-chunk-markdown/SKILL.md)
- **abd-convert-to-markdown** — [SKILL.md](../foundational/context-to-memory/skills/abd-convert-to-markdown/SKILL.md)
- **abd-embed-vectors** — [SKILL.md](../foundational/context-to-memory/skills/abd-embed-vectors/SKILL.md)
- **abd-search-memory** — [SKILL.md](../foundational/context-to-memory/skills/abd-search-memory/SKILL.md)
- **abd-semantic-context-chunker** — [SKILL.md](../foundational/context-to-memory/skills/abd-semantic-context-chunker/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `context-to-memory/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- _(empty `context-to-memory/instructions/`)_

**Prompts — .prompt.md → slash commands**

- _(empty `context-to-memory/prompts/`)_

**Lib — shared Python packages**

- _(empty `context-to-memory/lib/`)_

**Scripts — package-level automation**

- _(empty `context-to-memory/scripts/`)_

---

#### Skill Builder — `skill-builder/`

Practice skills for authoring ABD practice packages: query hub sources, author SKILL.md + rules, build scanners, maintain the AI Garden catalog, and publish HTML manuals.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- **abd-practice-skill-builder** — [AGENTS.md](../foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md)

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-author-practice-skill** — [SKILL.md](../foundational/skill-builder/skills/abd-author-practice-skill/SKILL.md)
- **abd-build-practice-scanners** — [SKILL.md](../foundational/skill-builder/skills/abd-build-practice-scanners/SKILL.md)
- **abd-practice-skill-manual** — [SKILL.md](../foundational/skill-builder/skills/abd-practice-skill-manual/SKILL.md)
- **abd-query-practice-sources** — [SKILL.md](../foundational/skill-builder/skills/abd-query-practice-sources/SKILL.md)
- **abd-skill-catalog** — [SKILL.md](../foundational/skill-builder/skills/abd-skill-catalog/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `skill-builder/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **abd-author-practice-skill** — [abd-author-practice-skill.instructions.md](../foundational/skill-builder/instructions/abd-author-practice-skill.instructions.md) (catalog: `instructions/skill-builder--instructions--abd-author-practice-skill-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- _(empty `skill-builder/prompts/`)_

**Lib — shared Python packages**

- _(empty `skill-builder/lib/`)_

**Scripts — package-level automation**

- [foundational/skill-builder/scripts/export_m365_agents.py](../foundational/skill-builder/scripts/export_m365_agents.py)

---

#### Skill Helpers — `skill-helpers/`

Infrastructure skills and cross-cutting helpers used across practice families.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `skill-helpers/agents/`)_

**Skills — practice packages (SKILL.md)**

**Core skills**

- **commit-msg** — [SKILL.md](../foundational/skill-helpers/skills/commit-msg/SKILL.md)
- **execute-skill-using-skills-rules** — [SKILL.md](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md)
- **track_task** — [SKILL.md](../foundational/skill-helpers/skills/track_task/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `skill-helpers/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **execute-skill-using-skills-rules** — [execute-skill-using-skills-rules.instructions.md](../foundational/skill-helpers/instructions/execute-skill-using-skills-rules.instructions.md) (catalog: `instructions/skill-helpers--instructions--execute-skill-using-skills-rules-instructions-md.html`)
- **log-and-fix-skill-errors** — [log-and-fix-skill-errors.instructions.md](../foundational/skill-helpers/instructions/log-and-fix-skill-errors.instructions.md) (catalog: `instructions/skill-helpers--instructions--log-and-fix-skill-errors-instructions-md.html`)
- **workspace** — [workspace.instructions.md](../foundational/skill-helpers/instructions/workspace.instructions.md) (catalog: `instructions/skill-helpers--instructions--workspace-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- **clean-skills** — [clean-skills.prompt.md](../foundational/skill-helpers/prompts/clean-skills.prompt.md) (catalog: `prompts/skill-helpers--prompts--clean-skills-prompt-md.html`)
- **deploy-skills** — [deploy-skills.prompt.md](../foundational/skill-helpers/prompts/deploy-skills.prompt.md) (catalog: `prompts/skill-helpers--prompts--deploy-skills-prompt-md.html`)
- **execute-skill-using-skills-rules** — [execute-skill-using-skills-rules.prompt.md](../foundational/skill-helpers/prompts/execute-skill-using-skills-rules.prompt.md) (catalog: `prompts/skill-helpers--prompts--execute-skill-using-skills-rules-prompt-md.html`)
- **fix-skill** — [fix-skill.prompt.md](../foundational/skill-helpers/prompts/fix-skill.prompt.md) (catalog: `prompts/skill-helpers--prompts--fix-skill-prompt-md.html`)
- **log-and-fix-skill-errors** — [log-and-fix-skill-errors.prompt.md](../foundational/skill-helpers/prompts/log-and-fix-skill-errors.prompt.md) (catalog: `prompts/skill-helpers--prompts--log-and-fix-skill-errors-prompt-md.html`)
- **refresh_all_instructions** — [refresh_all_instructions.prompt.md](../foundational/skill-helpers/prompts/refresh_all_instructions.prompt.md) (catalog: `prompts/skill-helpers--prompts--refresh_all_instructions-prompt-md.html`)
- **workspace** — [workspace.prompt.md](../foundational/skill-helpers/prompts/workspace.prompt.md) (catalog: `prompts/skill-helpers--prompts--workspace-prompt-md.html`)

**Lib — shared Python packages**

- _(empty `skill-helpers/lib/`)_

**Scripts — package-level automation**

- [foundational/skill-helpers/scripts/_agent_root.py](../foundational/skill-helpers/scripts/_agent_root.py)
- [foundational/skill-helpers/scripts/get_workspace.py](../foundational/skill-helpers/scripts/get_workspace.py)
- [foundational/skill-helpers/scripts/set_workspace.py](../foundational/skill-helpers/scripts/set_workspace.py)

---

#### Utilities — `utilities/`

Proposal response, AI research assistant skills, and related utilities.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- **ai-research-assistant** — [AGENTS.md](../utilities/agents/ai-research-assistant/AGENTS.md)

**Skills — practice packages (SKILL.md)**

**Core skills**

- **abd-proposal-respond** — [SKILL.md](../utilities/skills/abd-proposal-respond/SKILL.md)
- **research-compare-approach** — [SKILL.md](../utilities/skills/research-compare-approach/SKILL.md)
- **research-problem-validation** — [SKILL.md](../utilities/skills/research-problem-validation/SKILL.md)
- **research-solution-landscape** — [SKILL.md](../utilities/skills/research-solution-landscape/SKILL.md)


**Content — shared prose merged on deploy**

- _(empty `utilities/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- _(empty `utilities/instructions/`)_

**Prompts — .prompt.md → slash commands**

- _(empty `utilities/prompts/`)_

**Lib — shared Python packages**

- _(empty `utilities/lib/`)_

**Scripts — package-level automation**

- _(empty `utilities/scripts/`)_

---

## Summary — Skills

| Skill | Plugin | Description | Open |
| --- | --- | --- | --- |
| **abd-domain-glossary** | `practices` | Build an organized domain glossary — terms grouped by Key Abstraction, KAs grouped into modules by shared concern. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-glossary/SKILL.md) |
| **abd-domain-language** | `practices` | Shared vocabulary with concept behavior in one file; terms, KAs, and concept blocks. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-language/SKILL.md) |
| **domain-model** | `practices` | Typed domain model from Domain Language; constructors, properties, methods, collaborators, invariants. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-model/SKILL.md) |
| **class-model** | `practices` | Typed Class Model from the domain model; properties, operations, relationships, invariants. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-specification/SKILL.md) |
| **ddd-design-building-blocks** | `practices` | DDD stereotypes (Entity, VO, Aggregate, Service, Event) from domain model artifacts. | [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/SKILL.md) |
| **drawio-domain-sync** | `practices` | Domain model to Draw.io class diagrams — one page per Key Abstraction — with sync back to source. | [SKILL.md](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/SKILL.md) |
| **scenario-walkthrough** | `practices` | Walk scenarios through domain model or domain spec; validate class-operation ownership end-to-end. | [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-domain-walk/SKILL.md) |
| **bounded-context-map** | `practices` | Bounded context inventory with dependency arcs across three dimensions. | [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/SKILL.md) |
| **abd-domain-code** | `practices` | Write domain-layer tests and production code from any domain context. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-code/SKILL.md) |
| **abd-story-mapping** | `practices` | Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources. | [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md) |
| **abd-thin-slicing** | `practices` | Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates. | [SKILL.md](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/SKILL.md) |
| **abd-story-acceptance-criteria** | `practices` | WHEN/THEN/AND/BUT acceptance criteria for stories; behavioral language, atomic AC, domain terms. | [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/SKILL.md) |
| **abd-story-specification** | `practices` | Given/When/Then scenarios with real domain values; plain or outline (data tables) templates. | [SKILL.md](../practices/story-driven-delivery/skills/abd-story-specification/SKILL.md) |
| **abd-story-acceptance-test** | `practices` | Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR). | [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-test/SKILL.md) |
| **drawio-story-sync** | `practices` | story-graph.json to Draw.io story maps; validated load/save and diagram sync. | [SKILL.md](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/SKILL.md) |
| **miro-story-sync** | `practices` | story-graph.json to Miro story maps; validated load and REST-driven board sync. | [SKILL.md](../practices/story-driven-delivery/skills/supporting/miro-story-sync/SKILL.md) |
| **story-graph-ops** | `practices` | CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift. | [SKILL.md](../practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md) |
| **abd-information-architecture** | `practices` | Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a … | [SKILL.md](../practices/user-experience-design/skills/abd-information-architecture/SKILL.md) |
| **abd-information-architecture** | `practices` | Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a … | [SKILL.md](../practices/user-experience-design/skills/abd-ux-information-architecture/SKILL.md) |
| **abd-impact-mapping** | `practices` | Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources. | [SKILL.md](../practices/user-experience-design/skills/abd-ux-user-impact-map/SKILL.md) |
| **abd-ux-mockup** | `practices` | Lo-fi wireframes — exact controls, interactions, and states drawn in Draw.io from IA screens. | [SKILL.md](../practices/user-experience-design/skills/abd-ux-mockup/SKILL.md) |
| **abd-interface-design** | `practices` | Translate approved hi-fi mockups into production-grade, accessible interface code. | [SKILL.md](../practices/user-experience-design/skills/abd-ux-specification/SKILL.md) |
| **abd-ux-specification** | `practices` | Translate approved hi-fi mockups into production-grade, accessible interface code. | [SKILL.md](../practices/user-experience-design/skills/abd-ux-design/SKILL.md) |
| **abd-architecture-outline** | `practices` | First architecture artifact — four diagrams, principles, tech stack, major systems, and ADRs on one page. | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md) |
| **abd-architecture-blueprint** | `practices` | Second-level architecture — components in paragraphs, typed mechanisms, data model, testing strategy, and ADRs. | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md) |
| **abd-architecture-specification** | `practices` | Specification that defines how to create code that follows a particular architecture. | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-specification/SKILL.md) |
| **abd-clean-code** | `stages` | Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS). | [SKILL.md](../stages/engineering/abd-clean-code/SKILL.md) |
| **abd-secure-code** | `stages` | OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write and prove security-sensitive production code before merge. | [SKILL.md](../stages/engineering/abd-secure-code/SKILL.md) |
| **abd-architecture-code** | `practices` | Generate tests and production code from a named architecture spec, using domain and story context to instantiate the spec's patterns. Use when writing code for a story that has a named spec (e.g. specs/mern, specs/hero-vtt). | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-code/SKILL.md) |
| **abd-kanban-handoff** | `practices` | Delivery handoff from board, artifacts, and chat � where shaping/discovery/increments stand and what to do next. | [SKILL.md](../practices/kanban/skills/abd-kanban-handoff/SKILL.md) |
| **abd-kanban** | `practices` | JIT kanban board — tickets flow through stages, scatter at scope boundaries, agents pull work. | [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md) |
| **abd-kanban-planning** | `practices` | Strategy selection and system of work configuration â€” no pre-planned runs or slot tables. | [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md) |
| **kanban-estimation** | `practices` | Collaborative estimation at any scope level  contributing factors, categories, team vote, and recorded rationale. | [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md) |
| **abd-kanban-repo** | `practices` | Git operations driven by Kanban board state changes — commits, branches, PRs per ticket lifecycle. | [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md) |
| **abd-chunk-markdown** | `foundational` | Split converted Markdown into retrieval-sized chunks with evidence labels, guided by a structure-based chunking spec. Use when the user wants to "chunk documents", "split for RAG", "draft a chunking strategy", or prepare markdown for embedding and semantic search. | [SKILL.md](../foundational/context-to-memory/skills/abd-chunk-markdown/SKILL.md) |
| **abd-convert-to-markdown** | `foundational` | Convert office documents (PDF, PPTX, DOCX, XLSX, etc.) to navigable Markdown with real headings, sections, and tables. Use when the user wants to convert a document or folder of documents to markdown, mentions "convert to markdown", "extract text", or needs source files prepared for chunking or … | [SKILL.md](../foundational/context-to-memory/skills/abd-convert-to-markdown/SKILL.md) |
| **abd-embed-vectors** | `foundational` | Embed text chunks into a local FAISS vector index for semantic search. Use when the user wants to "embed chunks", "build a vector index", "create embeddings", or prepare chunked content for RAG retrieval. | [SKILL.md](../foundational/context-to-memory/skills/abd-embed-vectors/SKILL.md) |
| **abd-search-memory** | `foundational` | Semantic search over a local FAISS vector index built from document chunks. Use when the user says "use memory", "search memory", "what does memory say", "from our content", "what do we have on [topic]", or asks about content that has been ingested into agent memory. | [SKILL.md](../foundational/context-to-memory/skills/abd-search-memory/SKILL.md) |
| **abd-semantic-context-chunker** | `foundational` | Index scattered source content by the kind of context it provides — Story, Domain, Architecture, UX — so you know what you have before deeper analysis begins. Use when you have lots of files from many sources and need a coverage index, when pointing downstream work at the right source material, or … | [SKILL.md](../foundational/context-to-memory/skills/abd-semantic-context-chunker/SKILL.md) |
| **abd-author-practice-skill** | `foundational` | Turn collected hub evidence into a finished practice skill: clear instructions and checkable do-and-don't norms that stay true to what you retrieved. | [SKILL.md](../foundational/skill-builder/skills/abd-author-practice-skill/SKILL.md) |
| **abd-build-practice-scanners** | `foundational` | Turn written rules into checks a machine can run, so drift is caught early instead of debated in chat. | [SKILL.md](../foundational/skill-builder/skills/abd-build-practice-scanners/SKILL.md) |
| **abd-practice-skill-manual** | `foundational` | Ship a readable HTML companion for a practice: longer walkthroughs, figures, and sources so people can study the method without parsing SKILL.md alone. | [SKILL.md](../foundational/skill-builder/skills/abd-practice-skill-manual/SKILL.md) |
| **abd-query-practice-sources** | `foundational` | Pull defensible excerpts from the content hub so a new practice can cite real sources, not guesswork: one auditable log of what you kept and why it matters. | [SKILL.md](../foundational/skill-builder/skills/abd-query-practice-sources/SKILL.md) |
| **abd-skill-catalog** | `foundational` | Regenerate the browsable AI Garden (skills + agents HTML + outline.md) from repo packages. | [SKILL.md](../foundational/skill-builder/skills/abd-skill-catalog/SKILL.md) |
| **abd-proposal-respond** | `utilities` | RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG. | [SKILL.md](../utilities/skills/abd-proposal-respond/SKILL.md) |
| **research-compare-approach** | `utilities` | Critically compare the user's approach against researched alternatives. Identifies strengths, weaknesses, trade-offs, and legitimate white space. Reads the user's codebase ONLY to understand what they built — never as a source of best practice. Use when the user wants to know how their solution … | [SKILL.md](../utilities/skills/research-compare-approach/SKILL.md) |
| **research-problem-validation** | `utilities` | Research whether a stated problem is real and worth solving. Searches online and model knowledge for who is talking about the problem, who says it is NOT a problem, competing problems in the same space, and the maturity of discourse. Use when validating a hypothesis, checking if a problem is … | [SKILL.md](../utilities/skills/research-problem-validation/SKILL.md) |
| **research-solution-landscape** | `utilities` | Map the landscape of competing solutions for a validated problem. Searches online and model knowledge for categories of approaches, key tools and frameworks, trade-offs, and which segments each solution targets. Use when the user wants to know how others are solving a problem, what the major … | [SKILL.md](../utilities/skills/research-solution-landscape/SKILL.md) |
| **abd-commit-msg** | `foundational` | Commit messages from scope and changed files; no story_graph (/commit and similar). | [SKILL.md](../foundational/skill-helpers/skills/commit-msg/SKILL.md) |
| **execute-skill-using-skills-rules** | `foundational` | Run scanners, validate output against rules, fix failures; quality gate before and after work. | [SKILL.md](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md) |
| **track-task** | `foundational` | Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace. | [SKILL.md](../foundational/skill-helpers/skills/track_task/SKILL.md) |
| **abd-impact-mapping** | `stages` | Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources. | [SKILL.md](../stages/idea-shaping/skills/abd-impact-mapping/SKILL.md) |
| **abd-opportunity-canvas** | `stages` | Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build. | [SKILL.md](../stages/idea-shaping/skills/abd-opportunity-generation/SKILL.md) |
| **abd-simple-validated-learning** | `stages` | Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build. | [SKILL.md](../stages/idea-shaping/skills/abd-simple-validated-learning/SKILL.md) |
| **abd-cost-of-delay** | `stages` | Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay. | [SKILL.md](../stages/idea-shaping/skills/abd-cost-of-delay/SKILL.md) |
| **abd-service-level-objectives** | `stages` | Measurable NFRs as SLI/SLO/SLA — target × volume × percentage, scoped to story map, with error-budget policy. | [SKILL.md](../stages/discovery/abd-service-level-objectives/SKILL.md) |
| **abd-code-research** | `stages` | Survey any codebase in two passes — Explorer and Deep Dive — to produce structured research that primes the architecture skill family. | [SKILL.md](../stages/discovery/abd-code-research/SKILL.md) |

## Summary — Agents

| Agent | Plugin | Description | Open |
| --- | --- | --- | --- |
| **business-expert** | `practices` | You are a Business Expert (domain specialist). You own the domain-driven-design practice family — vocabulary, module boundaries, responsibilities, typed models — so that story, UX, and code share one language. | [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md) |
| **engineer** | `practices` | You are an Engineer. You own the architecture-centric-engineering practice family — architecture outline, blueprint, mechanism templates, reference, and clean code. | [AGENT.md](../practices/kanban/agents/engineer/AGENT.md) |
| **kanban-lead** | `practices` | You are a kanban lead agent orchestrating an abd.works (ABD) kanban delivery flow. Your responsibility is to orchestrate the delivery lifecycle using a JIT kanban board. You configure the board, manage stage flow, trigger scatters at scope boundaries, analyze bottlenecks, and scale the agent pool … | [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md) |
| **product-owner** | `practices` | You are a Product Owner. You own the story-driven-delivery practice family — story maps, thin slices, acceptance criteria, specification-by-example, and acceptance tests. | [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md) |
| **ux-designer** | `practices` | You are a UX Designer. You own the user-experience-design practice family — information architecture, lo-fi mockups, interface specifications, and runnable UI. | [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md) |
| **abd-context-to-memory** | `foundational` | Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and semantic search. Optional: review context_chunking_spec.yaml before chunk+embed. | [AGENTS.md](../foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md) |
| **abd-practice-skill-builder** | `foundational` | Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML … | [AGENTS.md](../foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md) |
| **ai-research-assistant** | `utilities` | Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a research report that helps the user decide whether their approach is well-founded, exposed, or genuinely novel. You are an impartial advisor — not … | [AGENTS.md](../utilities/agents/ai-research-assistant/AGENTS.md) |

---

## Skills (detail)

### abd-domain-glossary

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-glossary/`](../practices/domain-driven-design/skills/abd-domain-glossary/)

**Summary:**

Build an organized domain glossary — terms grouped by Key Abstraction, KAs grouped into modules by shared concern.

**Description (from Purpose / body):**

Produce a structured domain glossary — terms grouped by Key Abstraction, Key Abstractions grouped into modules by shared concern — so that every downstream artifact (domain language, acceptance criteria, specification, code) draws from a single agreed vocabulary.

The primary output is a glossary, not a boundary diagram. Modules are the organizing container: a module groups the KAs and terms that share a core concern and can be understood together. Each module file contains:
- Key Abstractions — named building blocks that own a cluster of related terms
- Terms per KA — behavioral bullets and source references (exact file + location) per term
- Boundary terms — concepts this module depends on but does not own
- Scope — what region of the domain this module covers (emerges from the terms, not the other way around)

---

**Repository layout:**

- **[reference/](../practices/domain-driven-design/skills/abd-domain-glossary/reference)** — Folder (4 items).
- **[rules/](../practices/domain-driven-design/skills/abd-domain-glossary/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-domain-glossary/scanners)** — Folder (5 items).
- **[templates/](../practices/domain-driven-design/skills/abd-domain-glossary/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-glossary/SKILL.md) — name: abd-domain-glossary

### abd-domain-language

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-language/`](../practices/domain-driven-design/skills/abd-domain-language/)

**Summary:**

Shared vocabulary with concept behavior in one file; terms, KAs, and concept blocks.

**Description (from Purpose / body):**

Build a shared, rigorous vocabulary for the scope you are modeling so that domain experts and modelers agree on what each term means, what each concept does, and which rules must always hold — and capture that agreement in one living document the whole team uses without translation. The scope of one run can be a single module, several modules, or a whole-system sweep; the skill and its output shape stay the same.

This is a three-pass skill. It reads source, extracts terms with definitions, groups them into Key Abstractions, sketches each concept's behavior and properties, and writes one file. The final output is a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties.

---

**Repository layout:**

- **[reference/](../practices/domain-driven-design/skills/abd-domain-language/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/abd-domain-language/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-domain-language/scanners)** — Folder (3 items).
- **[templates/](../practices/domain-driven-design/skills/abd-domain-language/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-language/SKILL.md) — name: abd-domain-language

### domain-model

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-model/`](../practices/domain-driven-design/skills/abd-domain-model/)

**Summary:**

Typed domain model from Domain Language; constructors, properties, methods, collaborators, invariants.

**Description (from Purpose / body):**

This skill takes domain concepts from a completed Domain Language and produces a typed domain model: for each concept, a constructor, typed properties, method signatures with collaborators and invariants. The result is a standalone file with ### Class blocks under each Key Abstraction.

The format sits between domain model and a full Class Model — it uses typed notation (constructors, property types, method signatures) but avoids class-model embellishments (no << stereotypes >>, no List<T> or Dictionary<K,V>, no Interaction: blocks, no + visibility prefixes, no param names in method signatures).

---

**Repository layout:**

- **[reference/](../practices/domain-driven-design/skills/abd-domain-model/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/abd-domain-model/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-domain-model/scanners)** — Folder (8 items).
- **[templates/](../practices/domain-driven-design/skills/abd-domain-model/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-model/SKILL.md) — name: domain-model

### class-model

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-specification/`](../practices/domain-driven-design/skills/abd-domain-specification/)

**Summary:**

Typed Class Model from the domain model; properties, operations, relationships, invariants.

**Description (from Purpose / body):**

Build a typed Class Model for a module. When a domain model exists it is the primary input � the skill converts that behavioral model into a typed domain surface with far less effort. Without a domain model the skill can still produce an Class Model directly from domain knowledge.

---

**Repository layout:**

- **[reference/](../practices/domain-driven-design/skills/abd-domain-specification/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/abd-domain-specification/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-domain-specification/scanners)** — Folder (8 items).
- **[templates/](../practices/domain-driven-design/skills/abd-domain-specification/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-domain-specification/corrections-log.md) — ?# Corrections log
- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-specification/SKILL.md) — name: class-model

### ddd-design-building-blocks

- **Directory:** [`practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/`](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/)

**Summary:**

DDD stereotypes (Entity, VO, Aggregate, Service, Event) from domain model artifacts.

**Description (from Purpose / body):**

This skill works through a domain model concept by concept, identifying the right technical constraints through a set of questions that — while technical in framing — can only be answered by business requirements. For example: if two patients have the same name and date of birth, should we consider them the same patient? If a product changes, when do we update the inventory system?

Every DDD building block — Entity, Value Object, Aggregate, Service, Domain Event — looks technical but exposes a question only the business can answer. This skill models these elements by understanding business requirements for identity semantics, consistency boundaries, immutability guarantees, and integration contracts across business concepts and systems.

---

**Repository layout:**

- **[ide-files/](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/ide-files)** — Folder (2 items).
- **[reference/](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/reference)** — Folder (2 items).
- **[rules/](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/SKILL.md) — name: ddd-design-building-blocks

### drawio-domain-sync

- **Directory:** [`practices/domain-driven-design/skills/supporting/drawio-domain-sync/`](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/)

**Summary:**

Domain model to Draw.io class diagrams — one page per Key Abstraction — with sync back to source.

**Description (from Purpose / body):**

This skill turns any domain model artifact — a Domain Language, Domain Model, or Domain Specification — into a Draw.io class diagram the whole team can read, annotate, and edit. Each Key Abstraction in the source file becomes its own page in the diagram, keeping visual scope manageable and per-abstraction structure clear. When the team edits the diagram in Draw.io, the skill syncs those changes back to the source model file, so diagram and text never drift apart.

Positioning and layout are AI-driven: the agent reads the source, reasons about class relationships and inheritance chains, and places elements where the diagram reads best. There are no fixed grid scripts to run.

---

**Repository layout:**

- **[ide-files/](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/ide-files)** — Folder (1 items).
- **[reference/](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/templates)** — Authoring templates and structural skeletons.
- [diagrams.md](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/diagrams.md) — ﻿<!-- section: story_synthesizer.diagrams -->
- [skill-errors-log.md](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/skill-errors-log.md) — drawio-domain-sync — skill errors log
- [SKILL.md](../practices/domain-driven-design/skills/supporting/drawio-domain-sync/SKILL.md) — name: drawio-domain-sync

### scenario-walkthrough

- **Directory:** [`practices/domain-driven-design/skills/supporting/abd-domain-walk/`](../practices/domain-driven-design/skills/supporting/abd-domain-walk/)

**Summary:**

Walk scenarios through domain model or domain spec; validate class-operation ownership end-to-end.

**Description (from Purpose / body):**

Walk concrete scenarios through the typed Class Model (or domain model where the Class Model is not yet built). Each step must map to a class and an operation from the prior phase's file. When a step crosses a state change or must respect a guard, align with the invariants and interactions captured upstream. If a step has no owner, record a gap and revise upstream artifacts.

---

**Repository layout:**

- **[reference/](../practices/domain-driven-design/skills/supporting/abd-domain-walk/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/supporting/abd-domain-walk/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/supporting/abd-domain-walk/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/supporting/abd-domain-walk/corrections-log.md) — ﻿﻿# Corrections log
- [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-domain-walk/SKILL.md) — name: scenario-walkthrough

### bounded-context-map

- **Directory:** [`practices/domain-driven-design/skills/supporting/abd-bounded-context-map/`](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/)

**Summary:**

Bounded context inventory with dependency arcs across three dimensions.

**Description (from Purpose / body):**

Teams working across multiple models, services, or subsystems need a single shared picture of how those pieces relate — which concepts cross boundaries, how the systems talk to each other, and how the teams will collaborate. Without that picture, integration strategy is discovered in production, translation is ad hoc, and team dependencies are invisible until they block someone. This skill produces a Bounded Context Map: a named inventory of every bounded context with every dependency declared across three explicit dimensions — domain mapping, integration mechanism, and team engagement model — so the architecture is honest and the team structure matches.

---

**Repository layout:**

- **[inputs/](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/inputs)** — Folder (1 items).
- **[markdown/](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/markdown)** — Folder (1 items).
- **[reference/](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/reference)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/SKILL.md) — name: bounded-context-map
- [stuff.docx](../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/stuff.docx) — PK     ! ��4��  ?   [Content_Types].xml …

### abd-domain-code

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-code/`](../practices/domain-driven-design/skills/abd-domain-code/)

**Summary:**

Write domain-layer tests and production code from any domain context.

**Description (from Purpose / body):**

Turn whatever domain context exists into running, tested domain code.

- Tests first (RED) → production code (GREEN) → clean up (REFACTOR).
- Only the domain layer: classes, value objects, operations, invariants, domain events.
- No database, no HTTP, no framework coupling.

---

**Repository layout:**

- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-code/SKILL.md) — name: abd-domain-code

### abd-story-mapping

- **Directory:** [`practices/story-driven-delivery/skills/abd-story-mapping/`](../practices/story-driven-delivery/skills/abd-story-mapping/)

**Summary:**

Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources.

**Description (from Purpose / body):**

A story map is a single shared picture of the product: epics (broad capability areas), sub-epics (flows or feature areas), and stories (leaves: one observable user or system interaction each). The map is not a dump of source material or a list of build tasks; it is outcomes and behaviors — what happens in the product — so product, delivery, and domain people can read the same structure.

Naming is part of the model: epics, sub-epics, and stories use verb—noun titles; who is acting is carried outside the name (in story_type), not stuffed into the title.

---

**Repository layout:**

- **[reference/](../practices/story-driven-delivery/skills/abd-story-mapping/reference)** — Folder (2 items).
- **[rules/](../practices/story-driven-delivery/skills/abd-story-mapping/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-story-mapping/scanners)** — Folder (6 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-story-mapping/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-story-mapping/corrections-log.md) —    C o r r e c t i o n s   l o g 
- [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md) — name: abd-story-mapping

### abd-thin-slicing

- **Directory:** [`practices/story-driven-delivery/skills/supporting/abd-thin-slicing/`](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/)

**Summary:**

Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates.

**Description (from Purpose / body):**

Define prioritized increments. Group stories in a story map (and any notes on risk, constraints, or learning goals) into prioritized increments that can be delivered together. Each increment includes its priority order, outcomes, slicing notes, and an ordered list of stories.

---

**Repository layout:**

- **[reference/](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/reference)** — Folder (2 items).
- **[rules/](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/scanners)** — Folder (2 items).
- **[templates/](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/corrections-log.md) — ﻿# Corrections log
- [SKILL.md](../practices/story-driven-delivery/skills/supporting/abd-thin-slicing/SKILL.md) — name: abd-thin-slicing

### abd-story-acceptance-criteria

- **Directory:** [`practices/story-driven-delivery/skills/abd-story-acceptance-criteria/`](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/)

**Summary:**

WHEN/THEN/AND/BUT acceptance criteria for stories; behavioral language, atomic AC, domain terms.

**Description (from Purpose / body):**

Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit negatives (BUT). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

---

**Repository layout:**

- **[reference/](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/reference)** — Folder (2 items).
- **[rules/](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/scanners)** — Folder (14 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/corrections-log.md) — ﻿——#   C o r r e c t i o n s   l o g 
- [skill-errors-log.md](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/skill-errors-log.md) — ﻿# Skill Errors Log — abd-story-acceptance-criteria
- [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-criteria/SKILL.md) — name: abd-story-acceptance-criteria

### abd-story-specification

- **Directory:** [`practices/story-driven-delivery/skills/abd-story-specification/`](../practices/story-driven-delivery/skills/abd-story-specification/)

**Summary:**

Given/When/Then scenarios with real domain values; plain or outline (data tables) templates.

**Description (from Purpose / body):**

Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

---

**Repository layout:**

- **[reference/](../practices/story-driven-delivery/skills/abd-story-specification/reference)** — Folder (2 items).
- **[rules/](../practices/story-driven-delivery/skills/abd-story-specification/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-story-specification/scanners)** — Folder (3 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-story-specification/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-story-specification/corrections-log.md) —    C o r r e c t i o n s   l o g 
- [SKILL.md](../practices/story-driven-delivery/skills/abd-story-specification/SKILL.md) — name: abd-story-specification

### abd-story-acceptance-test

- **Directory:** [`practices/story-driven-delivery/skills/abd-story-acceptance-test/`](../practices/story-driven-delivery/skills/abd-story-acceptance-test/)

**Summary:**

Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR).

**Description (from Purpose / body):**

Write tests first. Write code to pass them.

This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is test-driven: write a test that expresses the expected behavior, run it to confirm it fails (RED), then implement production code until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do — test methods show the Given-When-Then flow and helper functions do the work.

---

**Repository layout:**

- **[reference/](../practices/story-driven-delivery/skills/abd-story-acceptance-test/reference)** — Folder (2 items).
- **[rules/](../practices/story-driven-delivery/skills/abd-story-acceptance-test/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-story-acceptance-test/scanners)** — Folder (2 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-story-acceptance-test/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-story-acceptance-test/corrections-log.md) —    C o r r e c t i o n s   l o g 
- [SKILL.md](../practices/story-driven-delivery/skills/abd-story-acceptance-test/SKILL.md) — name: abd-story-acceptance-test

### drawio-story-sync

- **Directory:** [`practices/story-driven-delivery/skills/supporting/drawio-story-sync/`](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/)

**Summary:**

story-graph.json to Draw.io story maps; validated load/save and diagram sync.

**Description (from Purpose / body):**

Renders and synchronizes story-map Draw.io diagrams (outline, exploration with acceptance criteria, prioritization increments) from story-graph.json. Use when producing or diffing story-map.drawio files, or when wiring CI/scripts for diagram refresh and update reports.

**Repository layout:**

- **[scripts/](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/tests)** — Folder (3 items).
- [SKILL.md](../practices/story-driven-delivery/skills/supporting/drawio-story-sync/SKILL.md) — name: drawio-story-sync

### miro-story-sync

- **Directory:** [`practices/story-driven-delivery/skills/supporting/miro-story-sync/`](../practices/story-driven-delivery/skills/supporting/miro-story-sync/)

**Summary:**

story-graph.json to Miro story maps; validated load and REST-driven board sync.

**Description (from Purpose / body):**

Renders and synchronizes story-map Miro boards (outline; exploration and increments planned) from story-graph.json. Use when producing or refreshing Miro story maps from story-graph.json, or when wiring CI/scripts for Miro board updates.

**Repository layout:**

- **[scripts/](../practices/story-driven-delivery/skills/supporting/miro-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/supporting/miro-story-sync/tests)** — Folder (2 items).
- [SKILL.md](../practices/story-driven-delivery/skills/supporting/miro-story-sync/SKILL.md) — name: miro-story-sync

### story-graph-ops

- **Directory:** [`practices/story-driven-delivery/skills/supporting/story-graph-ops/`](../practices/story-driven-delivery/skills/supporting/story-graph-ops/)

**Summary:**

CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift.

**Description (from Purpose / body):**

Creates, reads, updates, and deletes story-graph.json (epics, sub-epics, stories, AC, scenarios) as a standalone artifact using the CLI or Python modules. Always validate after edits; do not hand-write JSON without running this skill's tooling. Use when editing story-graph.json or managing its lifecycle on disk.

**Repository layout:**

- **[guidance/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/guidance)** — Folder (0 items).
- **[ide-files/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/ide-files)** — Folder (0 items).
- **[logs/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/logs)** — Folder (1 items).
- **[scanner-report/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/scanner-report)** — Folder (0 items).
- **[scripts/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/supporting/story-graph-ops/tests)** — Folder (11 items).
- [MIGRATION_PARITY.md](../practices/story-driven-delivery/skills/supporting/story-graph-ops/MIGRATION_PARITY.md) — Story graph parity: agile_bots → story-graph-ops
- [skill-errors-log.md](../practices/story-driven-delivery/skills/supporting/story-graph-ops/skill-errors-log.md) — Corrections log
- [SKILL.md](../practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md) — name: story-graph-ops

### abd-information-architecture

- **Directory:** [`practices/user-experience-design/skills/abd-information-architecture/`](../practices/user-experience-design/skills/abd-information-architecture/)

**Summary:**

Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a …

**Description (from Purpose / body):**

Doing IA work early — before detailed design or development — flushes out gaps in functional and domain understanding, surfaces disagreements about scope, naming, and navigation when they are cheap to resolve, and gives the team a concrete picture to challenge and confirm before committing to wireframes or implementation. Functional requirements and stories written against a named screen inventory and content model become more precise: they reference agreed surfaces by name, missing coverage shows up as absent nodes, and edge-case states are identified before anyone has built against the wrong assumption.

---

**Repository layout:**

- **[reference/](../practices/user-experience-design/skills/abd-information-architecture/reference)** — Folder (1 items).
- **[rules/](../practices/user-experience-design/skills/abd-information-architecture/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[screen-templates/](../practices/user-experience-design/skills/abd-information-architecture/screen-templates)** — Folder (0 items).
- **[scripts/](../practices/user-experience-design/skills/abd-information-architecture/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/user-experience-design/skills/abd-information-architecture/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/user-experience-design/skills/abd-information-architecture/SKILL.md) — catalog_garden_tier: practice

### abd-information-architecture

- **Directory:** [`practices/user-experience-design/skills/abd-ux-information-architecture/`](../practices/user-experience-design/skills/abd-ux-information-architecture/)

**Summary:**

Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a …

**Description (from Purpose / body):**

Doing IA work early — before detailed design or development — flushes out gaps in functional and domain understanding, surfaces disagreements about scope, naming, and navigation when they are cheap to resolve, and gives the team a concrete picture to challenge and confirm before committing to wireframes or implementation. Functional requirements and stories written against a named screen inventory and content model become more precise: they reference agreed surfaces by name, missing coverage shows up as absent nodes, and edge-case states are identified before anyone has built against the wrong assumption.

---

**Repository layout:**

- **[reference/](../practices/user-experience-design/skills/abd-ux-information-architecture/reference)** — Folder (2 items).
- **[rules/](../practices/user-experience-design/skills/abd-ux-information-architecture/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[screen-templates/](../practices/user-experience-design/skills/abd-ux-information-architecture/screen-templates)** — Folder (86 items).
- **[scripts/](../practices/user-experience-design/skills/abd-ux-information-architecture/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/user-experience-design/skills/abd-ux-information-architecture/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/user-experience-design/skills/abd-ux-information-architecture/corrections-log.md) — abd-information-architecture — corrections log
- [SKILL.md](../practices/user-experience-design/skills/abd-ux-information-architecture/SKILL.md) — catalog_garden_tier: practice

### abd-impact-mapping

- **Directory:** [`practices/user-experience-design/skills/abd-ux-user-impact-map/`](../practices/user-experience-design/skills/abd-ux-user-impact-map/)

**Summary:**

Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.

**Description (from Purpose / body):**

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see why an option might matter before debating build order.

The map answers four questions in order: Why are we doing this? Who can help or hinder? How should behaviour change? What could we do to support that change? Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

---

**Repository layout:**

- **[inputs/](../practices/user-experience-design/skills/abd-ux-user-impact-map/inputs)** — Folder (2 items).
- **[reference/](../practices/user-experience-design/skills/abd-ux-user-impact-map/reference)** — Folder (2 items).
- **[rules/](../practices/user-experience-design/skills/abd-ux-user-impact-map/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/user-experience-design/skills/abd-ux-user-impact-map/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/user-experience-design/skills/abd-ux-user-impact-map/SKILL.md) — name: abd-impact-mapping

### abd-ux-mockup

- **Directory:** [`practices/user-experience-design/skills/abd-ux-mockup/`](../practices/user-experience-design/skills/abd-ux-mockup/)

**Summary:**

Lo-fi wireframes — exact controls, interactions, and states drawn in Draw.io from IA screens.

**Description (from Purpose / body):**

The initial IA established the screen inventory, regions, and story coverage. The lo-fi mockup is the next precision pass: it locks down exactly which control renders each field, exactly what interactions are available in each state, and exactly what the user sees and does — without yet committing to visual design. Every input becomes a specific control type (text field, dropdown, checkbox). Every action becomes a positioned button with a primary/secondary weight. Every conditional state (validation error, empty list, disabled control) is explicitly placed. This skill packages that pass: take one IA screen, resolve its AC and domain terms, build a drawio-mockup.mjs state file, generate the .drawio wireframe, and save it — so interaction decisions are made deliberately and traceable, not invented during implementation.

---

**Repository layout:**

- **[reference/](../practices/user-experience-design/skills/abd-ux-mockup/reference)** — Folder (1 items).
- **[rules/](../practices/user-experience-design/skills/abd-ux-mockup/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../practices/user-experience-design/skills/abd-ux-mockup/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/user-experience-design/skills/abd-ux-mockup/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/user-experience-design/skills/abd-ux-mockup/corrections-log.md) — abd-lo-fi — corrections log
- [SKILL.md](../practices/user-experience-design/skills/abd-ux-mockup/SKILL.md) — catalog_garden_tier: practice

### abd-interface-design

- **Directory:** [`practices/user-experience-design/skills/abd-ux-specification/`](../practices/user-experience-design/skills/abd-ux-specification/)

**Summary:**

Translate approved hi-fi mockups into production-grade, accessible interface code.

**Description (from Purpose / body):**

Hi-fi mockups settle look and feel. The interface stage is where they become real code — and where most teams quietly stop honouring the upstream artifacts because "we're shipping now". This skill keeps that integrity: the implementation renders the same regions, the same affordances, the same labels, the same acceptance criteria, and the same visual decisions as the approved hi-fi, in production-grade code that an end user can actually use. It treats acceptance criteria as the testable surface (every clause is a working behaviour with a check), treats the ubiquitous language as the public vocabulary (labels and copy stay verbatim from the UL and AC), and treats accessibility and performance as constraints that are met, not aspirations that are mentioned.

---

**Repository layout:**

- **[reference/](../practices/user-experience-design/skills/abd-ux-specification/reference)** — Folder (1 items).
- **[rules/](../practices/user-experience-design/skills/abd-ux-specification/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/user-experience-design/skills/abd-ux-specification/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/user-experience-design/skills/abd-ux-specification/corrections-log.md) — abd-interface-design — corrections log
- [SKILL.md](../practices/user-experience-design/skills/abd-ux-specification/SKILL.md) — catalog_garden_tier: practice

### abd-ux-specification

- **Directory:** [`practices/user-experience-design/skills/abd-ux-design/`](../practices/user-experience-design/skills/abd-ux-design/)

**Summary:**

Translate approved hi-fi mockups into production-grade, accessible interface code.

**Description (from Purpose / body):**

Hi-fi mockups settle look and feel. The interface stage is where they become real code � and where most teams quietly stop honouring the upstream artifacts because "we're shipping now". This skill keeps that integrity: the implementation renders the same regions, the same affordances, the same labels, the same acceptance criteria, and the same visual decisions as the approved hi-fi, in production-grade code that an end user can actually use. It treats acceptance criteria as the testable surface (every clause is a working behaviour with a check), treats the Domain Language as the public vocabulary (labels and copy stay verbatim from the UL and AC), and treats accessibility and performance as constraints that are met, not aspirations that are mentioned.

---

**Repository layout:**

- **[reference/](../practices/user-experience-design/skills/abd-ux-design/reference)** — Folder (1 items).
- **[rules/](../practices/user-experience-design/skills/abd-ux-design/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/user-experience-design/skills/abd-ux-design/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/user-experience-design/skills/abd-ux-design/corrections-log.md) — abd-ux-specification — corrections log
- [SKILL.md](../practices/user-experience-design/skills/abd-ux-design/SKILL.md) — catalog_garden_tier: practice

### abd-architecture-outline

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-outline/`](../practices/architecture-centric-engineering/skills/abd-architecture-outline/)

**Summary:**

First architecture artifact — four diagrams, principles, tech stack, major systems, and ADRs on one page.

**Description (from Purpose / body):**

A team that cannot draw its system on one page also cannot agree on what to build next. Outlines fix that. This skill produces the first architecture artifact for a system — short on prose, heavy on diagrams — so engineers, product, and stakeholders share a single picture of the platform, the layers, the neighbours, the deployment topology, and the principles in force. When the outline is in place, deeper architecture work (blueprint, reference, mechanisms) can start without re-litigating what the system is.

---

**Repository layout:**

- **[reference/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/reference)** — Folder (2 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scanner-report)** — Folder (1 items).
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scanners)** — Folder (1 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/corrections-log.md) — ��#   C o r r e c t i o n s   l o g   �� �   a b d - a r c h i t e c t u r e - o u t l i n e 
- [deployment-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/deployment-architecture.png) — IHDR  *  ~   ��1�   sRGB ��
- [layered-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/layered-architecture.png) — IHDR  �  X   L��P   sRGB ��
- [platform-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/platform-architecture.png) — IHDR  (  4   P�   sRGB ��
- [process.docx](../practices/architecture-centric-engineering/skills/abd-architecture-outline/process.docx) — PK     ! ��
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md) — catalog_garden_tier: practice
- [system-context.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/system-context.png) — IHDR    Y   ݸ��   sRGB ��

### abd-architecture-blueprint

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-blueprint/`](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/)

**Summary:**

Second-level architecture — components in paragraphs, typed mechanisms, data model, testing strategy, and ADRs.

**Description (from Purpose / body):**

The outline shows what a system is; the blueprint shows what it is made of. A blueprint is the document a tech lead opens to answer "where does the order code live? what does it depend on? how does it talk to the catalogue?" without yet drilling into the implementation patterns. It names every architectural component in a paragraph or two, catalogues every cross-cutting concern as an architecture mechanism, shows the data architecture at the model level, captures the common testing strategy, and lists the decisions taken at this level. When the blueprint is in place, the architecture reference can go deep on one mechanism at a time without re-explaining the system to its reader.

---

**Repository layout:**

- **[reference/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/reference)** — Folder (2 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scanner-report)** — Folder (1 items).
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scanners)** — Folder (1 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md) — catalog_garden_tier: practice

### abd-architecture-specification

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-specification/`](../practices/architecture-centric-engineering/skills/abd-architecture-specification/)

**Summary:**

Specification that defines how to create code that follows a particular architecture.

**Description (from Purpose / body):**

An architecture specification tells engineers exactly how domain concepts and stories become code in a chosen stack — which files, classes, interactions, and tests implement each entity, operation, and scenario. The specification is one artifact: documentation and working template code stay aligned; each mechanism is documented once and reused; later runs extend only what is missing.

---

**Repository layout:**

- **[inputs/](../practices/architecture-centric-engineering/skills/abd-architecture-specification/inputs)** — Folder (1 items).
- **[reference/](../practices/architecture-centric-engineering/skills/abd-architecture-specification/reference)** — Folder (2 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-specification/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-specification/templates)** — Authoring templates and structural skeletons.
- [skill-errors-log.md](../practices/architecture-centric-engineering/skills/abd-architecture-specification/skill-errors-log.md) — Skill errors log � abd-architecture-specification
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-specification/SKILL.md) — catalog_garden_tier: practice

### abd-clean-code

- **Directory:** [`stages/engineering/abd-clean-code/`](../stages/engineering/abd-clean-code/)

**Summary:**

Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS).

**Description (from Purpose / body):**

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

---

**Repository layout:**

- **[reference/](../stages/engineering/abd-clean-code/reference)** — Folder (2 items).
- **[rules/](../stages/engineering/abd-clean-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../stages/engineering/abd-clean-code/scanners)** — Folder (2 items).
- **[scripts/](../stages/engineering/abd-clean-code/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../stages/engineering/abd-clean-code/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../stages/engineering/abd-clean-code/corrections-log.md) — abd-clean-code — corrections log
- [SKILL.md](../stages/engineering/abd-clean-code/SKILL.md) — name: abd-clean-code

### abd-secure-code

- **Directory:** [`stages/engineering/abd-secure-code/`](../stages/engineering/abd-secure-code/)

**Summary:**

OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write and prove security-sensitive production code before merge.

**Description (from Purpose / body):**

Engineers ship features faster than attackers find gaps — but only when secure defaults are explicit, reviewable, and mechanically checkable. This skill packages Secure Code Warrior guidance into concrete coding rules and automated scanners so teams and agents can write security-sensitive code and prove it meets the same bar before merge.

---

**Repository layout:**

- **[inputs/](../stages/engineering/abd-secure-code/inputs)** — Folder (5 items).
- **[reference/](../stages/engineering/abd-secure-code/reference)** — Folder (1 items).
- **[rules/](../stages/engineering/abd-secure-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../stages/engineering/abd-secure-code/scanners)** — Folder (5 items).
- **[scripts/](../stages/engineering/abd-secure-code/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../stages/engineering/abd-secure-code/templates)** — Authoring templates and structural skeletons.
- **[test/](../stages/engineering/abd-secure-code/test)** — Automated tests for the agent or skill package.
- [SKILL.md](../stages/engineering/abd-secure-code/SKILL.md) — name: abd-secure-code

### abd-architecture-code

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-code/`](../practices/architecture-centric-engineering/skills/abd-architecture-code/)

**Summary:**

Generate tests and production code from a named architecture spec, using domain and story context to instantiate the spec's patterns. Use when writing code for a story that has a named spec (e.g. specs/mern, specs/hero-vtt).

**Description (from Purpose / body):**

Given a named architecture spec and story scope with domain context, generate acceptance tests then production code that follows the spec's instructions, templates, file layout, and rules. Use when writing code for a story that has a named spec, adding a feature module to an existing codebase, or reviewing generated code for architecture compliance.

---

**Repository layout:**

- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-code/SKILL.md) — name: abd-architecture-code

### abd-kanban-handoff

- **Directory:** [`practices/kanban/skills/abd-kanban-handoff/`](../practices/kanban/skills/abd-kanban-handoff/)

**Summary:**

Delivery handoff from board, artifacts, and chat � where shaping/discovery/increments stand and what to do next.

**Description (from Purpose / body):**

Produce a delivery resume document so a fresh agent knows where JIT kanban delivery left off � which stages and scopes have advanced, which increments have material under docs/increments/, and what to run next � without re-reading the whole repo or chat.

Works with or without a live board: when board.json is missing or stale, infer progress from artifact presence and chat.

---

**Repository layout:**

- **[scripts/](../practices/kanban/skills/abd-kanban-handoff/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/kanban/skills/abd-kanban-handoff/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/kanban/skills/abd-kanban-handoff/SKILL.md) — name: abd-kanban-handoff

### abd-kanban

- **Directory:** [`practices/kanban/skills/abd-kanban/`](../practices/kanban/skills/abd-kanban/)

**Summary:**

JIT kanban board — tickets flow through stages, scatter at scope boundaries, agents pull work.

**Description (from Purpose / body):**

Configure the kanban board for a delivery engagement. The kanban board defines ordered stages, each with a scope level and stage work required. Tickets carry only a lazily-populated skill_progress map; the kanban board (kanban.json) is the single source of truth for which skills a stage require. The kanban app owns all board mechanics from there.

---

**Repository layout:**

- **[templates/](../practices/kanban/skills/abd-kanban/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md) — name: abd-kanban

### abd-kanban-planning

- **Directory:** [`practices/kanban/skills/abd-kanban-planning/`](../practices/kanban/skills/abd-kanban-planning/)

**Summary:**

Strategy selection and system of work configuration â€” no pre-planned runs or slot tables.

**Description (from Purpose / body):**

Kanban Planning configures how delivery flows â€” not what to build. It selects a strategy based on context and risk, configures the kanban board (stages, scope levels, stage work required), and defines scatter rules (how and when tickets decompose at scope boundaries). The result drives the JIT kanban board without pre-authoring every assignment.

Do not use this skill to produce artifacts (maps, slices, AC, tests, code). This skill is strictly about the delivery lifecycle spine â€” the kanban board stage configuration, strategy, and decomposition rules.

---

**Repository layout:**

- **[reference/](../practices/kanban/skills/abd-kanban-planning/reference)** — Folder (4 items).
- **[rules/](../practices/kanban/skills/abd-kanban-planning/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/kanban/skills/abd-kanban-planning/scanners)** — Folder (2 items).
- **[scripts/](../practices/kanban/skills/abd-kanban-planning/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/kanban/skills/abd-kanban-planning/tests)** — Folder (3 items).
- [corrections-log.md](../practices/kanban/skills/abd-kanban-planning/corrections-log.md) — abd-kanban-planning — corrections log
- [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md) — name: abd-kanban-planning

### kanban-estimation

- **Directory:** [`practices/kanban/skills/kanban-estimation/`](../practices/kanban/skills/kanban-estimation/)

**Summary:**

Collaborative estimation at any scope level  contributing factors, categories, team vote, and recorded rationale.

**Description (from Purpose / body):**

Teams estimate badly not because they lack a formula but because they skip the conversation. Effort gets assigned by one person's hunch, contributing factors go unexamined, and nobody records why a number landed where it did  so every future re-estimate starts from scratch. Delivery estimation packages the facilitation pattern that makes sizing collaborative, factor-aware, and traceable: teams walk through backlog items one at a time, name what drives effort, agree on a category, and save the reasoning alongside the number.



---

**Repository layout:**

- **[reference/](../practices/kanban/skills/kanban-estimation/reference)** — Folder (1 items).
- **[rules/](../practices/kanban/skills/kanban-estimation/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/kanban/skills/kanban-estimation/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md) — name: kanban-estimation

### abd-kanban-repo

- **Directory:** [`practices/kanban/skills/abd-kanban-repo/`](../practices/kanban/skills/abd-kanban-repo/)

**Summary:**

Git operations driven by Kanban board state changes — commits, branches, PRs per ticket lifecycle.

**Description (from Purpose / body):**

Manage git history for a delivery engagement. Commits, branches, pushes, and PRs are driven by ticket state changes on the Kanban board — not by slots or runs.

---

**Repository layout:**

- **[scripts/](../practices/kanban/skills/abd-kanban-repo/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md) — name: abd-kanban-repo

### abd-chunk-markdown

- **Directory:** [`foundational/context-to-memory/skills/abd-chunk-markdown/`](../foundational/context-to-memory/skills/abd-chunk-markdown/)

**Summary:**

Split converted Markdown into retrieval-sized chunks with evidence labels, guided by a structure-based chunking spec. Use when the user wants to "chunk documents", "split for RAG", "draft a chunking strategy", or prepare markdown for embedding and semantic search.

**Description (from Purpose / body):**

Split converted Markdown into retrieval-sized chunks with evidence labels, guided by a structure-based chunking spec. Use when the user wants to "chunk documents", "split for RAG", "draft a chunking strategy", or prepare markdown for embedding and semantic search.

**Repository layout:**

- **[references/](../foundational/context-to-memory/skills/abd-chunk-markdown/references)** — Folder (2 items).
- **[scripts/](../foundational/context-to-memory/skills/abd-chunk-markdown/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../foundational/context-to-memory/skills/abd-chunk-markdown/SKILL.md) — name: abd-chunk-markdown

### abd-convert-to-markdown

- **Directory:** [`foundational/context-to-memory/skills/abd-convert-to-markdown/`](../foundational/context-to-memory/skills/abd-convert-to-markdown/)

**Summary:**

Convert office documents (PDF, PPTX, DOCX, XLSX, etc.) to navigable Markdown with real headings, sections, and tables. Use when the user wants to convert a document or folder of documents to markdown, mentions "convert to markdown", "extract text", or needs source files prepared for chunking or …

**Description (from Purpose / body):**

Convert office documents (PDF, PPTX, DOCX, XLSX, etc.) to navigable Markdown with real headings, sections, and tables. Use when the user wants to convert a document or folder of documents to markdown, mentions "convert to markdown", "extract text", or needs source files prepared for chunking or agent context.

**Repository layout:**

- **[references/](../foundational/context-to-memory/skills/abd-convert-to-markdown/references)** — Folder (2 items).
- **[scripts/](../foundational/context-to-memory/skills/abd-convert-to-markdown/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../foundational/context-to-memory/skills/abd-convert-to-markdown/SKILL.md) — name: abd-convert-to-markdown

### abd-embed-vectors

- **Directory:** [`foundational/context-to-memory/skills/abd-embed-vectors/`](../foundational/context-to-memory/skills/abd-embed-vectors/)

**Summary:**

Embed text chunks into a local FAISS vector index for semantic search. Use when the user wants to "embed chunks", "build a vector index", "create embeddings", or prepare chunked content for RAG retrieval.

**Description (from Purpose / body):**

Embed text chunks into a local FAISS vector index for semantic search. Use when the user wants to "embed chunks", "build a vector index", "create embeddings", or prepare chunked content for RAG retrieval.

**Repository layout:**

- **[references/](../foundational/context-to-memory/skills/abd-embed-vectors/references)** — Folder (1 items).
- **[scripts/](../foundational/context-to-memory/skills/abd-embed-vectors/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../foundational/context-to-memory/skills/abd-embed-vectors/SKILL.md) — name: abd-embed-vectors

### abd-search-memory

- **Directory:** [`foundational/context-to-memory/skills/abd-search-memory/`](../foundational/context-to-memory/skills/abd-search-memory/)

**Summary:**

Semantic search over a local FAISS vector index built from document chunks. Use when the user says "use memory", "search memory", "what does memory say", "from our content", "what do we have on [topic]", or asks about content that has been ingested into agent memory.

**Description (from Purpose / body):**

Semantic search over a local FAISS vector index built from document chunks. Use when the user says "use memory", "search memory", "what does memory say", "from our content", "what do we have on [topic]", or asks about content that has been ingested into agent memory.

**Repository layout:**

- **[references/](../foundational/context-to-memory/skills/abd-search-memory/references)** — Folder (1 items).
- **[scripts/](../foundational/context-to-memory/skills/abd-search-memory/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../foundational/context-to-memory/skills/abd-search-memory/SKILL.md) — name: abd-search-memory

### abd-semantic-context-chunker

- **Directory:** [`foundational/context-to-memory/skills/abd-semantic-context-chunker/`](../foundational/context-to-memory/skills/abd-semantic-context-chunker/)

**Summary:**

Index scattered source content by the kind of context it provides — Story, Domain, Architecture, UX — so you know what you have before deeper analysis begins. Use when you have lots of files from many sources and need a coverage index, when pointing downstream work at the right source material, or …

**Description (from Purpose / body):**

Scan all source content, tag every piece by the kind of context it provides (Story, Domain, Architecture, UX), and produce a coverage index showing what you have across all four views — before any deeper analysis begins.

---

**Repository layout:**

- **[reference/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/reference)** — Folder (1 items).
- **[references/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/references)** — Folder (1 items).
- **[rules/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../foundational/context-to-memory/skills/abd-semantic-context-chunker/SKILL.md) — name: abd-semantic-context-chunker

### abd-author-practice-skill

- **Directory:** [`foundational/skill-builder/skills/abd-author-practice-skill/`](../foundational/skill-builder/skills/abd-author-practice-skill/)

**Summary:**

Turn collected hub evidence into a finished practice skill: clear instructions and checkable do-and-don't norms that stay true to what you retrieved.

**Description (from Purpose / body):**

Teams need practice skills that people and agents can follow without improvising or drifting away from what the sources actually say. This authoring skill helps you finish such a package after you have already chosen what to keep from the hub: the teaching on the skill page reads clearly, and the norms on the outputs are explicit enough to pass or fail. It guides you from that evidence to aligned prose and checks. Prerequisites, Build, and Not in this pass on this page carry retrieval and scanner wiring when you need those steps.

**Repository layout:**

- **[rules/](../foundational/skill-builder/skills/abd-author-practice-skill/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../foundational/skill-builder/skills/abd-author-practice-skill/scanners)** — Folder (1 items).
- **[scripts/](../foundational/skill-builder/skills/abd-author-practice-skill/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../foundational/skill-builder/skills/abd-author-practice-skill/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../foundational/skill-builder/skills/abd-author-practice-skill/corrections-log.md) — ﻿# Corrections log — abd-author-practice-skill
- [SKILL.md](../foundational/skill-builder/skills/abd-author-practice-skill/SKILL.md) — name: abd-author-practice-skill

### abd-build-practice-scanners

- **Directory:** [`foundational/skill-builder/skills/abd-build-practice-scanners/`](../foundational/skill-builder/skills/abd-build-practice-scanners/)

**Summary:**

Turn written rules into checks a machine can run, so drift is caught early instead of debated in chat.

**Description (from Purpose / body):**

Written DO / DO NOT rules are easy to ignore or misread. Small automated checks (scripts tied to those rules) make the same expectations repeatable: a failure means something concrete to fix, not a vague "are we sure?" moment.

**Repository layout:**

- **[rules/](../foundational/skill-builder/skills/abd-build-practice-scanners/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../foundational/skill-builder/skills/abd-build-practice-scanners/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../foundational/skill-builder/skills/abd-build-practice-scanners/SKILL.md) — name: abd-build-practice-scanners

### abd-practice-skill-manual

- **Directory:** [`foundational/skill-builder/skills/abd-practice-skill-manual/`](../foundational/skill-builder/skills/abd-practice-skill-manual/)

**Summary:**

Ship a readable HTML companion for a practice: longer walkthroughs, figures, and sources so people can study the method without parsing SKILL.md alone.

**Description (from Purpose / body):**

SKILL.md is the compact source of truth; many readers still want a browser-friendly walkthrough with room for diagrams, step layout, and quoted evidence. This skill produces that HTML manual next to the skill, using self-contained styling assets so it opens offline without another repo.

**Repository layout:**

- **[assets/](../foundational/skill-builder/skills/abd-practice-skill-manual/assets)** — Folder (3 items).
- **[rules/](../foundational/skill-builder/skills/abd-practice-skill-manual/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../foundational/skill-builder/skills/abd-practice-skill-manual/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../foundational/skill-builder/skills/abd-practice-skill-manual/SKILL.md) — name: abd-practice-skill-manual

### abd-query-practice-sources

- **Directory:** [`foundational/skill-builder/skills/abd-query-practice-sources/`](../foundational/skill-builder/skills/abd-query-practice-sources/)

**Summary:**

Pull defensible excerpts from the content hub so a new practice can cite real sources, not guesswork: one auditable log of what you kept and why it matters.

**Description (from Purpose / body):**

Before anyone writes instructions or rules for a practice, you need a single, honest record of what the hub actually contains on that topic: what you read, where it lives, and how each piece supports the skill. This skill is about finding and recording that evidence so later work stays anchored to real content.

**Repository layout:**

- **[rules/](../foundational/skill-builder/skills/abd-query-practice-sources/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../foundational/skill-builder/skills/abd-query-practice-sources/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../foundational/skill-builder/skills/abd-query-practice-sources/SKILL.md) — name: abd-query-practice-sources

### abd-skill-catalog

- **Directory:** [`foundational/skill-builder/skills/abd-skill-catalog/`](../foundational/skill-builder/skills/abd-skill-catalog/)

**Summary:**

Regenerate the browsable AI Garden (skills + agents HTML + outline.md) from repo packages.

**Description (from Purpose / body):**

Scan agilebydesign-skills family packages; maintain README card copy; regenerate catalog/ (families, skills, agents, outline.md) from the full package layout.

**Repository layout:**

- **[scripts/](../foundational/skill-builder/skills/abd-skill-catalog/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../foundational/skill-builder/skills/abd-skill-catalog/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../foundational/skill-builder/skills/abd-skill-catalog/corrections-log.md) — Corrections — abd-skill-catalog (generated AI Garden HTML)
- [README.md](../foundational/skill-builder/skills/abd-skill-catalog/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../foundational/skill-builder/skills/abd-skill-catalog/SKILL.md) — name: abd-skill-catalog

### abd-proposal-respond

- **Directory:** [`utilities/skills/abd-proposal-respond/`](../utilities/skills/abd-proposal-respond/)

**Summary:**

RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG.

**Description (from Purpose / body):**

Respond to client proposals by converting materials to memory, creating a response strategy, and answering questions in small batches. Uses abd-context-to-memory for RAG. Same iterate-on-strategy pattern as abd-shaping.

---

**Repository layout:**

- **[content/](../utilities/skills/abd-proposal-respond/content)** — Source parts merged into agent instructions or outputs.
- **[rules/](../utilities/skills/abd-proposal-respond/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../utilities/skills/abd-proposal-respond/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../utilities/skills/abd-proposal-respond/AGENTS.md) — Core Definitions
- [skill-config.json](../utilities/skills/abd-proposal-respond/skill-config.json) — "name": "abd-proposal-respond",
- [SKILL.md](../utilities/skills/abd-proposal-respond/SKILL.md) — name: abd-proposal-respond

### research-compare-approach

- **Directory:** [`utilities/skills/research-compare-approach/`](../utilities/skills/research-compare-approach/)

**Summary:**

Critically compare the user's approach against researched alternatives. Identifies strengths, weaknesses, trade-offs, and legitimate white space. Reads the user's codebase ONLY to understand what they built — never as a source of best practice. Use when the user wants to know how their solution …

**Description (from Purpose / body):**

Given a solution landscape (from research-solution-landscape) and the
user's own approach, produce a critical, honest comparison — not a
validation exercise.

**Repository layout:**

- **[templates/](../utilities/skills/research-compare-approach/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../utilities/skills/research-compare-approach/SKILL.md) — name: research-compare-approach

### research-problem-validation

- **Directory:** [`utilities/skills/research-problem-validation/`](../utilities/skills/research-problem-validation/)

**Summary:**

Research whether a stated problem is real and worth solving. Searches online and model knowledge for who is talking about the problem, who says it is NOT a problem, competing problems in the same space, and the maturity of discourse. Use when validating a hypothesis, checking if a problem is …

**Description (from Purpose / body):**

Given a problem statement (usually extracted from a hypothesis), determine
whether the problem is real, recognized, and worth solving — using
external evidence only.

**Repository layout:**

- [SKILL.md](../utilities/skills/research-problem-validation/SKILL.md) — name: research-problem-validation

### research-solution-landscape

- **Directory:** [`utilities/skills/research-solution-landscape/`](../utilities/skills/research-solution-landscape/)

**Summary:**

Map the landscape of competing solutions for a validated problem. Searches online and model knowledge for categories of approaches, key tools and frameworks, trade-offs, and which segments each solution targets. Use when the user wants to know how others are solving a problem, what the major …

**Description (from Purpose / body):**

Given a validated problem, map how people are actually solving it — the
categories of solutions, concrete tools and practices, and how they differ.

**Repository layout:**

- [SKILL.md](../utilities/skills/research-solution-landscape/SKILL.md) — name: research-solution-landscape

### abd-commit-msg

- **Directory:** [`foundational/skill-helpers/skills/commit-msg/`](../foundational/skill-helpers/skills/commit-msg/)

**Summary:**

Commit messages from scope and changed files; no story_graph (/commit and similar).

**Description (from Purpose / body):**

Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit.

**Repository layout:**

- **[docs/](../foundational/skill-helpers/skills/commit-msg/docs)** — Human-oriented documentation for the package.
- **[reference/](../foundational/skill-helpers/skills/commit-msg/reference)** — Folder (5 items).
- **[rules/](../foundational/skill-helpers/skills/commit-msg/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../foundational/skill-helpers/skills/commit-msg/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../foundational/skill-helpers/skills/commit-msg/AGENTS.md) — Core Definitions
- [README.md](../foundational/skill-helpers/skills/commit-msg/README.md) — ace-commit-msg
- [skill-config.json](../foundational/skill-helpers/skills/commit-msg/skill-config.json) — "name": "abd-commit-msg",
- [SKILL.md](../foundational/skill-helpers/skills/commit-msg/SKILL.md) — name: abd-commit-msg

### execute-skill-using-skills-rules

- **Directory:** [`foundational/skill-helpers/skills/execute-skill-using-skills-rules/`](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/)

**Summary:**

Run scanners, validate output against rules, fix failures; quality gate before and after work.

**Description (from Purpose / body):**

Read rules before work, validate output (AI pass + scanner pass), and follow the correction process after mistakes.

**Repository layout:**

- **[scripts/](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/templates)** — Authoring templates and structural skeletons.
- **[tests/](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/tests)** — Folder (4 items).
- [SKILL.md](../foundational/skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md) — name: execute-skill-using-skills-rules

### track-task

- **Directory:** [`foundational/skill-helpers/skills/track_task/`](../foundational/skill-helpers/skills/track_task/)

**Summary:**

Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace.

**Description (from Purpose / body):**

Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources.

**Repository layout:**

- **[scripts/](../foundational/skill-helpers/skills/track_task/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../foundational/skill-helpers/skills/track_task/tests)** — Folder (2 items).
- [README.md](../foundational/skill-helpers/skills/track_task/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../foundational/skill-helpers/skills/track_task/SKILL.md) — name: track-task

### abd-impact-mapping

- **Directory:** [`stages/idea-shaping/skills/abd-impact-mapping/`](../stages/idea-shaping/skills/abd-impact-mapping/)

**Summary:**

Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.

**Description (from Purpose / body):**

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see why an option might matter before debating build order.

The map answers four questions in order: Why are we doing this? Who can help or hinder? How should behaviour change? What could we do to support that change? Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

---

**Repository layout:**

- **[inputs/](../stages/idea-shaping/skills/abd-impact-mapping/inputs)** — Folder (2 items).
- **[reference/](../stages/idea-shaping/skills/abd-impact-mapping/reference)** — Folder (2 items).
- **[rules/](../stages/idea-shaping/skills/abd-impact-mapping/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../stages/idea-shaping/skills/abd-impact-mapping/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/idea-shaping/skills/abd-impact-mapping/SKILL.md) — name: abd-impact-mapping

### abd-opportunity-canvas

- **Directory:** [`stages/idea-shaping/skills/abd-opportunity-generation/`](../stages/idea-shaping/skills/abd-opportunity-generation/)

**Summary:**

Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build.

**Description (from Purpose / body):**

This skill exists so you do not start "building a solution" while people are thinking about a different problem, a different customer, or a different definition of success.

It makes an opportunity explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that downstream build and delivery work is based on a shared model. Every part of the canvas is also a candidate assumption — beliefs about customers, value, and capability that teams often turn into falsifiable statements and run through a lightweight validation path (see abd-simple-validated-learning).

---

**Repository layout:**

- **[reference/](../stages/idea-shaping/skills/abd-opportunity-generation/reference)** — Folder (1 items).
- **[rules/](../stages/idea-shaping/skills/abd-opportunity-generation/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../stages/idea-shaping/skills/abd-opportunity-generation/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/idea-shaping/skills/abd-opportunity-generation/SKILL.md) — name: abd-opportunity-canvas

### abd-simple-validated-learning

- **Directory:** [`stages/idea-shaping/skills/abd-simple-validated-learning/`](../stages/idea-shaping/skills/abd-simple-validated-learning/)

**Summary:**

Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.

**Description (from Purpose / body):**

Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. This skill is for surfacing those assumptions explicitly and working through them iteratively before the organisation treats them as fact or commits to a full build. The agent (or facilitator) mines the supplied context for assumptions, rewrites them as falsifiable hypotheses, prioritises them into a validation backlog, and structures each item to move through Plan → Validate → Learn.

---

**Repository layout:**

- **[inputs/](../stages/idea-shaping/skills/abd-simple-validated-learning/inputs)** — Folder (1 items).
- **[reference/](../stages/idea-shaping/skills/abd-simple-validated-learning/reference)** — Folder (1 items).
- **[rules/](../stages/idea-shaping/skills/abd-simple-validated-learning/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../stages/idea-shaping/skills/abd-simple-validated-learning/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/idea-shaping/skills/abd-simple-validated-learning/SKILL.md) — name: abd-simple-validated-learning

### abd-cost-of-delay

- **Directory:** [`stages/idea-shaping/skills/abd-cost-of-delay/`](../stages/idea-shaping/skills/abd-cost-of-delay/)

**Summary:**

Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay.

**Description (from Purpose / body):**

Teams routinely prioritize work by gut feel, stakeholder loudness, or first-in-first-out — all of which ignore how much value decays while items wait to be delivered. Cost of Delay puts a price tag on time so teams can make scheduling decisions based on economics rather than politics.

This skill classifies the value type and urgency of each feature or initiative in context, then builds a simple value model that makes assumptions explicit, calculates Cost of Delay per time period (month / week), divides by duration to get CD3, and ranks so the highest-value shortest-duration work goes first.

---

**Repository layout:**

- **[reference/](../stages/idea-shaping/skills/abd-cost-of-delay/reference)** — Folder (2 items).
- **[rules/](../stages/idea-shaping/skills/abd-cost-of-delay/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../stages/idea-shaping/skills/abd-cost-of-delay/scanners)** — Folder (4 items).
- **[scripts/](../stages/idea-shaping/skills/abd-cost-of-delay/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../stages/idea-shaping/skills/abd-cost-of-delay/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/idea-shaping/skills/abd-cost-of-delay/SKILL.md) — name: abd-cost-of-delay

### abd-service-level-objectives

- **Directory:** [`stages/discovery/abd-service-level-objectives/`](../stages/discovery/abd-service-level-objectives/)

**Summary:**

Measurable NFRs as SLI/SLO/SLA — target × volume × percentage, scoped to story map, with error-budget policy.

**Description (from Purpose / body):**

A non-functional requirement that cannot be measured is a wish. Teams that ship without measurable NFRs discover the truth in production — too late, too expensive, sometimes too public. This skill turns each NFR into a concrete Service Level Indicator (what is measured), Service Level Objective (the target on that indicator), and where a customer-facing commitment exists, a Service Level Agreement. Critically, each objective is scoped to the functional area it applies to: a single user story, an epic, a parent epic, or the system as a whole.

---

**Repository layout:**

- **[reference/](../stages/discovery/abd-service-level-objectives/reference)** — Folder (2 items).
- **[rules/](../stages/discovery/abd-service-level-objectives/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../stages/discovery/abd-service-level-objectives/scanners)** — Folder (0 items).
- **[templates/](../stages/discovery/abd-service-level-objectives/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/discovery/abd-service-level-objectives/SKILL.md) — name: abd-service-level-objectives

### abd-code-research

- **Directory:** [`stages/discovery/abd-code-research/`](../stages/discovery/abd-code-research/)

**Summary:**

Survey any codebase in two passes — Explorer and Deep Dive — to produce structured research that primes the architecture skill family.

**Description (from Purpose / body):**

Walking into an unfamiliar codebase without a map turns architecture work into guesswork. This skill makes the survey systematic: a first pass spans the codebase breadth-first, naming every meaningful research path and capturing raw source evidence; a second pass follows each path to the depth that architecture documentation needs. The two passes produce structured outputs that feed directly into abd-architecture-outline, abd-architecture-blueprint, and abd-architecture-specification, so those downstream skills start with evidence rather than assumptions. The skill works for any codebase — compiled or interpreted, monolith or modular, documented or bare — and scales from a 500-line script to a 200-file enterprise system.

---

**Repository layout:**

- **[ide-files/](../stages/discovery/abd-code-research/ide-files)** — Folder (2 items).
- **[prompts/](../stages/discovery/abd-code-research/prompts)** — Folder (1 items).
- **[rules/](../stages/discovery/abd-code-research/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../stages/discovery/abd-code-research/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../stages/discovery/abd-code-research/SKILL.md) — name: abd-code-research

---

## Agents (detail)

### business-expert

- **Directory:** [`practices/kanban/agents/business-expert/`](../practices/kanban/agents/business-expert/)
- **Entry:** [`practices/kanban/agents/business-expert/AGENT.md`](../practices/kanban/agents/business-expert/AGENT.md)

**Summary:**

You are a Business Expert (domain specialist). You own the domain-driven-design practice family — vocabulary, module boundaries, responsibilities, typed models — so that story, UX, and code share one language.

**Description:**

# Business Expert

You are a Business Expert (domain specialist). You own the domain-driven-design practice family — vocabulary, module boundaries, responsibilities, typed models — so that story, UX, and code share one language.

Your goal is to make business rules, entities, and collaborations explicit before they are buried in acceptance criteria, mockups, or code.

## Practice family

domain-driven-design/ — see stage files in reference/stages/ to understand which domain skills you run at each stage, what you need before starting, and what must be true before you're done.

Where to write: artifact-layout.md.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md) — Business Expert

### engineer

- **Directory:** [`practices/kanban/agents/engineer/`](../practices/kanban/agents/engineer/)
- **Entry:** [`practices/kanban/agents/engineer/AGENT.md`](../practices/kanban/agents/engineer/AGENT.md)

**Summary:**

You are an Engineer. You own the architecture-centric-engineering practice family — architecture outline, blueprint, mechanism templates, reference, and clean code.

**Description:**

# Engineer

You are an Engineer. You own the architecture-centric-engineering practice family — architecture outline, blueprint, mechanism templates, reference, and clean code.

Your goal is to make technical structure explicit early and ship code that passes acceptance tests while matching blueprint, reference, and interface specifications.

## Practice family

architecture-centric-engineering/ — see stage files in reference/stages/ to understand which architecture and code skills you run at each stage, what you need before starting, and what must be true before you're done.

Where to write: artifact-layout.md.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/engineer/AGENT.md) — Engineer

### kanban-lead

- **Directory:** [`practices/kanban/agents/kanban-lead/`](../practices/kanban/agents/kanban-lead/)
- **Entry:** [`practices/kanban/agents/kanban-lead/AGENT.md`](../practices/kanban/agents/kanban-lead/AGENT.md)

**Summary:**

You are a kanban lead agent orchestrating an abd.works (ABD) kanban delivery flow. Your responsibility is to orchestrate the delivery lifecycle using a JIT kanban board. You configure the board, manage stage flow, trigger scatters at scope boundaries, analyze bottlenecks, and scale the agent pool …

**Description:**

# ABD Kanban Lead

You are a kanban lead agent orchestrating an abd.works (ABD) kanban delivery flow. Your responsibility is to orchestrate the delivery lifecycle using a JIT kanban board. You configure the board, manage stage flow, trigger scatters at scope boundaries, analyze bottlenecks, and scale the agent pool. You do not produce deliverables — role agents do.

The board app (abd-delivery-agent-kanban) drives the scan loop, agent lifecycle, and heartbeat monitoring. Your job is strategy, setup, scatter decisions, exit gate validation, and bottleneck judgment.

## Bootstrap inputs (required)

- workspace — Absolute path where engagement artifacts live.

Optional:

- context — Brief, documents, links describing what is being delivered.
- strategy — Which strategy to use (from …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md) — ABD Kanban Lead

### product-owner

- **Directory:** [`practices/kanban/agents/product-owner/`](../practices/kanban/agents/product-owner/)
- **Entry:** [`practices/kanban/agents/product-owner/AGENT.md`](../practices/kanban/agents/product-owner/AGENT.md)

**Summary:**

You are a Product Owner. You own the story-driven-delivery practice family — story maps, thin slices, acceptance criteria, specification-by-example, and acceptance tests.

**Description:**

# Product Owner

You are a Product Owner. You own the story-driven-delivery practice family — story maps, thin slices, acceptance criteria, specification-by-example, and acceptance tests.

Your goal is to shape and refine what the team builds and in what order — the right thing, in the right order. You define behavior through specification and write failing acceptance tests; Engineers implement production code.

## Practice family

story-driven-delivery/ — see stage files in reference/stages/ to understand which story and spec skills you run at each stage, what you need before starting, and what must be true before you're done.

Where to write: artifact-layout.md.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md) — Product Owner

### ux-designer

- **Directory:** [`practices/kanban/agents/ux-designer/`](../practices/kanban/agents/ux-designer/)
- **Entry:** [`practices/kanban/agents/ux-designer/AGENT.md`](../practices/kanban/agents/ux-designer/AGENT.md)

**Summary:**

You are a UX Designer. You own the user-experience-design practice family — information architecture, lo-fi mockups, interface specifications, and runnable UI.

**Description:**

# UX Designer

You are a UX Designer. You own the user-experience-design practice family — information architecture, lo-fi mockups, interface specifications, and runnable UI.

Your goal is to make interaction and layout decisions explicit before engineers implement domain and production logic, without inventing vocabulary or behaviors that acceptance criteria do not support.

## Practice family

user-experience-design/ — see stage files in reference/stages/ to understand which UX skills you run at each stage, what you need before starting, and what must be true before you're done.

Where to write: artifact-layout.md.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md) — ﻿# UX Designer

### abd-context-to-memory

- **Directory:** [`foundational/context-to-memory/agents/abd-context-to-memory/`](../foundational/context-to-memory/agents/abd-context-to-memory/)
- **Entry:** [`foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md`](../foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md)

**Summary:**

Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and semantic search. Optional: review context_chunking_spec.yaml before chunk+embed.

**Description:**

Flow: turn source documents into Markdown (under markdown/ in the topic tree), draft a chunking strategy (context_chunking_spec.yaml), split into labeled chunks in memory/, embed into a local FAISS index under memory/rag/, then search semantically. Optionally pause after the spec so a human can review or edit the YAML before chunk + embed (strategy pass); otherwise run straight through. Hold basic quality across stages (real headings before chunking, sane splits after).

Per-stage detail: *skills/abd-context-to-memory/abd-/SKILL.md and each skill's references/**.

---

**Repository layout:**

- **[conf/](../foundational/context-to-memory/agents/abd-context-to-memory/conf)** — Folder (0 items).
- **[reference/](../foundational/context-to-memory/agents/abd-context-to-memory/reference)** — Folder (6 items).
- [AGENTS.md](../foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md) — AGENTS — abd-context-to-memory
- [README.md](../foundational/context-to-memory/agents/abd-context-to-memory/README.md) — catalogue_summary: >-
- [requirements-export.txt](../foundational/context-to-memory/agents/abd-context-to-memory/requirements-export.txt) — Export: markdown → Excel, Word, PDF
- [requirements-rag.txt](../foundational/context-to-memory/agents/abd-context-to-memory/requirements-rag.txt) — RAG (vector search) dependencies for ace-context-to-memory
- [skill-config.json](../foundational/context-to-memory/agents/abd-context-to-memory/skill-config.json) — "name": "abd-context-to-memory",

### abd-practice-skill-builder

- **Directory:** [`foundational/skill-builder/agents/abd-practice-skill-builder/`](../foundational/skill-builder/agents/abd-practice-skill-builder/)
- **Entry:** [`foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md`](../foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md)

**Summary:**

Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML …

**Description:**

Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML manual (vendored shell assets in abd-practice-skill-manual).

Orchestrate using the agent-local packages in skills/ under this agent (same idea as abd-context-to-memory routing to nested skills/abd-/SKILL.md*).

---

**Repository layout:**

- **[scripts/](../foundational/skill-builder/agents/abd-practice-skill-builder/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md) — AGENTS — abd-practice-skill-builder
- [corrections-log.md](../foundational/skill-builder/agents/abd-practice-skill-builder/corrections-log.md) — ﻿# Corrections log
- [README.md](../foundational/skill-builder/agents/abd-practice-skill-builder/README.md) — catalogue_summary: "Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence …
- [skill-config.json](../foundational/skill-builder/agents/abd-practice-skill-builder/skill-config.json) — "name": "abd-practice-skill-builder",

### ai-research-assistant

- **Directory:** [`utilities/agents/ai-research-assistant/`](../utilities/agents/ai-research-assistant/)
- **Entry:** [`utilities/agents/ai-research-assistant/AGENTS.md`](../utilities/agents/ai-research-assistant/AGENTS.md)

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

- [AGENTS.md](../utilities/agents/ai-research-assistant/AGENTS.md) — AGENTS — ai-research-assistant
