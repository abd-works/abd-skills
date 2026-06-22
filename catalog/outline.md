# AI Garden — plugins, skills & agents

> Auto-generated from repository **plugins** (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).
> Run `python foundational/skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` to refresh.

Each row gives a **short description** and where to open the source.

## Plugins

Repo-root capability plugins (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).

| Plugin | Summary | Open |
| --- | --- | --- |
| **Kanban** (`kanban/`) | 9 agents, 4 skills, 12 content, 4 instructions, 4 prompts, 1 scripts | [README.md](../practices/kanban/README.md) |
| **Story Driven Delivery** (`story-driven-delivery/`) | Deploy: `python scripts/deploy_family_package.py --package story-driven-delivery --to <workspace>` | [README.md](../practices/story-driven-delivery/README.md) |
| **Domain Driven Design** (`domain-driven-design/`) | Practice skills for module partition, domain terms, ubiquitous language, CRC, object model, DDD building blocks, bounded contexts, and domain diagram sync. | [README.md](../practices/domain-driven-design/README.md) |
| **Architecture Centric Engineering** (`architecture-centric-engineering/`) | 10 skills, 2 content | [README.md](../practices/architecture-centric-engineering/README.md) |
| **Idea Shaping** (`idea-shaping/`) | Opportunity framing, impact mapping, cost of delay, and validated learning — before delivery work begins. | [README.md](../practices/idea-shaping/README.md) |
| **User Experience Design** (`user-experience-design/`) | Deploy: `python scripts/deploy_family_package.py --package user-experience-design --to <workspace>` | [README.md](../practices/kanban/user-experience-design/README.md) |
| **Context To Memory** (`context-to-memory/`) | Convert office documents to markdown, chunk for retrieval, embed vectors, and search memory. | [README.md](../foundational/context-to-memory/README.md) |
| **Skill Builder** (`skill-builder/`) | Practice skills for authoring ABD practice packages: query hub sources, author SKILL.md + rules, build scanners, maintain the AI Garden catalog, and publish HTML manuals. | [README.md](../foundational/skill-builder/README.md) |
| **Skill Helpers** (`skill-helpers/`) | Infrastructure skills and cross-cutting helpers used across practice families. | [README.md](../foundational/skill-helpers/README.md) |
| **Utilities** (`utilities/`) | Proposal response, AI research assistant skills, and related utilities. | [README.md](../utilities/README.md) |

### Plugin layout (detail)

#### Kanban — `kanban/`

9 agents, 4 skills, 12 content, 4 instructions, 4 prompts, 1 scripts

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- **business-expert** — [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md)
- **business-expert-reviewer** — [AGENT.md](../practices/kanban/agents/business-expert-reviewer/AGENT.md)
- **engineer** — [AGENT.md](../practices/kanban/agents/engineer/AGENT.md)
- **engineer-reviewer** — [AGENT.md](../practices/kanban/agents/engineer-reviewer/AGENT.md)
- **kanban-lead** — [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md)
- **product-owner** — [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md)
- **product-owner-reviewer** — [AGENT.md](../practices/kanban/agents/product-owner-reviewer/AGENT.md)
- **ux-designer** — [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md)
- **ux-designer-reviewer** — [AGENT.md](../practices/kanban/agents/ux-designer-reviewer/AGENT.md)

**Skills — practice packages (SKILL.md)**

- **abd-kanban** — [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md)
- **abd-kanban-planning** — [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md)
- **abd-kanban-repo** — [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md)
- **kanban-estimation** — [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md)

**Content — shared prose merged on deploy**

- [practices/kanban/content/kanban.md](../practices/kanban/content/kanban.md)
- [practices/kanban/content/roles/business-expert.md](../practices/kanban/content/roles/business-expert.md)
- [practices/kanban/content/roles/engineer.md](../practices/kanban/content/roles/engineer.md)
- [practices/kanban/content/roles/product-owner.md](../practices/kanban/content/roles/product-owner.md)
- [practices/kanban/content/roles/team-roles.md](../practices/kanban/content/roles/team-roles.md)
- [practices/kanban/content/roles/ux-designer.md](../practices/kanban/content/roles/ux-designer.md)
- [practices/kanban/content/stages/discovery.md](../practices/kanban/content/stages/discovery.md)
- [practices/kanban/content/stages/engineering.md](../practices/kanban/content/stages/engineering.md)
- [practices/kanban/content/stages/exploration.md](../practices/kanban/content/stages/exploration.md)
- [practices/kanban/content/stages/README.md](../practices/kanban/content/stages/README.md)
- [practices/kanban/content/stages/shaping.md](../practices/kanban/content/stages/shaping.md)
- [practices/kanban/content/stages/specification.md](../practices/kanban/content/stages/specification.md)

**Instructions — .mdc / .instructions.md → Cursor rules**

- **delivery-estimation** — [delivery-estimation.instructions.md](../practices/kanban/instructions/delivery-estimation.instructions.md) (catalog: `instructions/kanban--instructions--delivery-estimation-instructions-md.html`)
- **delivery-estimation.prompt** — [delivery-estimation.prompt.md](../practices/kanban/instructions/delivery-estimation.prompt.md) (catalog: `instructions/kanban--instructions--delivery-estimation-prompt-md.html`)
- **kanban-git** — [kanban-git.mdc](../practices/kanban/instructions/kanban-git.mdc) (catalog: `instructions/kanban--instructions--kanban-git-mdc.html`)
- **sync-upstream** — [sync-upstream.mdc](../practices/kanban/instructions/sync-upstream.mdc) (catalog: `instructions/kanban--instructions--sync-upstream-mdc.html`)

**Prompts — .prompt.md → slash commands**

- **abd-feature** — [abd-feature.prompt.md](../practices/kanban/prompts/abd-feature.prompt.md) (catalog: `prompts/kanban--prompts--abd-feature-prompt-md.html`)
- **abd-fix-defect** — [abd-fix-defect.prompt.md](../practices/kanban/prompts/abd-fix-defect.prompt.md) (catalog: `prompts/kanban--prompts--abd-fix-defect-prompt-md.html`)
- **brownfield-current-state** — [brownfield-current-state.prompt.md](../practices/kanban/prompts/brownfield-current-state.prompt.md) (catalog: `prompts/kanban--prompts--brownfield-current-state-prompt-md.html`)
- **sync-upstream** — [sync-upstream.prompt.md](../practices/kanban/prompts/sync-upstream.prompt.md) (catalog: `prompts/kanban--prompts--sync-upstream-prompt-md.html`)

**Lib — shared Python packages**

- _(empty `kanban/lib/`)_

**Scripts — package-level automation**

- [practices/kanban/scripts/copy_delivery.py](../practices/kanban/scripts/copy_delivery.py)

---

#### Story Driven Delivery — `story-driven-delivery/`

Deploy: `python scripts/deploy_family_package.py --package story-driven-delivery --to <workspace>`

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `story-driven-delivery/agents/`)_

**Skills — practice packages (SKILL.md)**

- **abd-acceptance-criteria** — [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/SKILL.md)
- **abd-acceptance-test-driven-development** — [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/SKILL.md)
- **abd-specification-by-example** — [SKILL.md](../practices/story-driven-delivery/skills/abd-specification-by-example/SKILL.md)
- **abd-story-mapping** — [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md)
- **abd-thin-slicing** — [SKILL.md](../practices/story-driven-delivery/skills/abd-thin-slicing/SKILL.md)
- **drawio-story-sync** — [SKILL.md](../practices/story-driven-delivery/skills/drawio-story-sync/SKILL.md)
- **miro-story-sync** — [SKILL.md](../practices/story-driven-delivery/skills/miro-story-sync/SKILL.md)
- **story-graph-ops** — [SKILL.md](../practices/story-driven-delivery/skills/story-graph-ops/SKILL.md)

**Content — shared prose merged on deploy**

- _(empty `story-driven-delivery/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **drawio-story-sync** — [drawio-story-sync.mdc](../practices/story-driven-delivery/instructions/drawio-story-sync.mdc) (catalog: `instructions/story-driven-delivery--instructions--drawio-story-sync-mdc.html`)
- **story-graph-ops** — [story-graph-ops.mdc](../practices/story-driven-delivery/instructions/story-graph-ops.mdc) (catalog: `instructions/story-driven-delivery--instructions--story-graph-ops-mdc.html`)

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
- [practices/story-driven-delivery/lib/README.md](../practices/story-driven-delivery/lib/README.md)

**Scripts — package-level automation**

- _(empty `story-driven-delivery/scripts/`)_

---

#### Domain Driven Design — `domain-driven-design/`

Practice skills for module partition, domain terms, ubiquitous language, CRC, object model, DDD building blocks, bounded contexts, and domain diagram sync.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `domain-driven-design/agents/`)_

**Skills — practice packages (SKILL.md)**

- **abd-bounded-context-map** — [SKILL.md](../practices/domain-driven-design/skills/abd-bounded-context-map/SKILL.md)
- **abd-class-responsibility-collaborator** — [SKILL.md](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/SKILL.md)
- **abd-ddd-design-building-blocks** — [SKILL.md](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/SKILL.md)
- **abd-domain-terms** — [SKILL.md](../practices/domain-driven-design/skills/abd-domain-terms/SKILL.md)
- **abd-module-partition** — [SKILL.md](../practices/domain-driven-design/skills/abd-module-partition/SKILL.md)
- **abd-object-model** — [SKILL.md](../practices/domain-driven-design/skills/abd-object-model/SKILL.md)
- **abd-scenario-walkthrough** — [SKILL.md](../practices/domain-driven-design/skills/abd-scenario-walkthrough/SKILL.md)
- **abd-ubiquitous-language** — [SKILL.md](../practices/domain-driven-design/skills/abd-ubiquitous-language/SKILL.md)
- **drawio-domain-sync** — [SKILL.md](../practices/domain-driven-design/skills/drawio-domain-sync/SKILL.md)

**Content — shared prose merged on deploy**

- [practices/domain-driven-design/content/oo-concepts.md](../practices/domain-driven-design/content/oo-concepts.md)

**Instructions — .mdc / .instructions.md → Cursor rules**

- **ddd-building-blocks-fidelity-upgrade** — [ddd-building-blocks-fidelity-upgrade.instructions.md](../practices/domain-driven-design/instructions/ddd-building-blocks-fidelity-upgrade.instructions.md) (catalog: `instructions/domain-driven-design--instructions--ddd-building-blocks-fidelity-upgrade-instructions-md.html`)
- **ddd-building-blocks-fidelity-upgrade** — [ddd-building-blocks-fidelity-upgrade.mdc](../practices/domain-driven-design/instructions/ddd-building-blocks-fidelity-upgrade.mdc) (catalog: `instructions/domain-driven-design--instructions--ddd-building-blocks-fidelity-upgrade-mdc.html`)
- **drawio-domain-sync** — [drawio-domain-sync.instructions.md](../practices/domain-driven-design/instructions/drawio-domain-sync.instructions.md) (catalog: `instructions/domain-driven-design--instructions--drawio-domain-sync-instructions-md.html`)

**Prompts — .prompt.md → slash commands**

- _(empty `domain-driven-design/prompts/`)_

**Lib — shared Python packages**

- _(empty `domain-driven-design/lib/`)_

**Scripts — package-level automation**

- _(empty `domain-driven-design/scripts/`)_

---

#### Architecture Centric Engineering — `architecture-centric-engineering/`

10 skills, 2 content

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `architecture-centric-engineering/agents/`)_

**Skills — practice packages (SKILL.md)**

- **abd-architecture-blueprint** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md)
- **abd-architecture-outline** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md)
- **abd-architecture-reference** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-reference/SKILL.md)
- **abd-architecture-template** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-template/SKILL.md)
- **abd-build-architecture-skill** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/SKILL.md)
- **abd-clean-code** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-clean-code/SKILL.md)
- **abd-secure-code** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-secure-code/SKILL.md)
- **abd-service-level-objectives** — [SKILL.md](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/SKILL.md)
- **hero-vtt-technical-architecture** — [SKILL.md](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/SKILL.md)
- **mern-technical-architecture** — [SKILL.md](../practices/architecture-centric-engineering/skills/mern-technical-architecture/SKILL.md)

**Content — shared prose merged on deploy**

- [practices/architecture-centric-engineering/content/architecture_and_design.json](../practices/architecture-centric-engineering/content/architecture_and_design.json)
- [practices/architecture-centric-engineering/content/data.md](../practices/architecture-centric-engineering/content/data.md)

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

- **abd-cost-of-delay** — [SKILL.md](../practices/idea-shaping/skills/abd-cost-of-delay/SKILL.md)
- **abd-impact-mapping** — [SKILL.md](../practices/idea-shaping/skills/abd-impact-mapping/SKILL.md)
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

Deploy: `python scripts/deploy_family_package.py --package user-experience-design --to <workspace>`

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `user-experience-design/agents/`)_

**Skills — practice packages (SKILL.md)**

- **abd-information-architecture** — [SKILL.md](../practices/kanban/user-experience-design/skills/abd-information-architecture/SKILL.md)
- **abd-interface-design** — [SKILL.md](../practices/kanban/user-experience-design/skills/abd-interface-design/SKILL.md)
- **abd-ux-mockup** — [SKILL.md](../practices/kanban/user-experience-design/skills/abd-ux-mockup/SKILL.md)

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

- **abd-author-practice-skill** — [SKILL.md](../foundational/skill-builder/skills/abd-author-practice-skill/SKILL.md)
- **abd-build-practice-scanners** — [SKILL.md](../foundational/skill-builder/skills/abd-build-practice-scanners/SKILL.md)
- **abd-practice-skill-manual** — [SKILL.md](../foundational/skill-builder/skills/abd-practice-skill-manual/SKILL.md)
- **abd-query-practice-sources** — [SKILL.md](../foundational/skill-builder/skills/abd-query-practice-sources/SKILL.md)
- **abd-skill-catalog** — [SKILL.md](../foundational/skill-builder/skills/abd-skill-catalog/SKILL.md)

**Content — shared prose merged on deploy**

- _(empty `skill-builder/content/`)_

**Instructions — .mdc / .instructions.md → Cursor rules**

- **abd-author-practice-skill** — [abd-author-practice-skill.instructions.md](../foundational/skill-builder/instructions/abd-author-practice-skill.instructions.md) (catalog: `instructions/skill-builder--instructions--abd-author-practice-skill-instructions-md.html`)
- **abd-author-practice-skill** — [abd-author-practice-skill.mdc](../foundational/skill-builder/instructions/abd-author-practice-skill.mdc) (catalog: `instructions/skill-builder--instructions--abd-author-practice-skill-mdc.html`)

**Prompts — .prompt.md → slash commands**

- _(empty `skill-builder/prompts/`)_

**Lib — shared Python packages**

- _(empty `skill-builder/lib/`)_

**Scripts — package-level automation**

- _(empty `skill-builder/scripts/`)_

---

#### Skill Helpers — `skill-helpers/`

Infrastructure skills and cross-cutting helpers used across practice families.

**Agents — orchestrators (AGENT.md / AGENTS.md)**

- _(empty `skill-helpers/agents/`)_

**Skills — practice packages (SKILL.md)**

- **commit-msg** — [SKILL.md](../foundational/skill-helpers/skills/commit-msg/SKILL.md)
- **common** — [SKILL.md](../foundational/skill-helpers/skills/common/skill-rule-workflow.md)
- **skill-garden-catalogue** — [SKILL.md](../foundational/skill-helpers/skills/skill-garden-catalogue/SKILL.md)
- **track_task** — [SKILL.md](../foundational/skill-helpers/skills/track_task/SKILL.md)

**Content — shared prose merged on deploy**

- [foundational/skill-helpers/content/templates/skill-errors-log.md](../foundational/skill-helpers/content/templates/skill-errors-log.md)
- [foundational/skill-helpers/content/workspace.md](../foundational/skill-helpers/content/workspace.md)

**Instructions — .mdc / .instructions.md → Cursor rules**

- **deploy-skills** — [deploy-skills.mdc](../foundational/skill-helpers/instructions/deploy-skills.mdc) (catalog: `instructions/skill-helpers--instructions--deploy-skills-mdc.html`)
- **common** — [common.instructions.md](../foundational/skill-helpers/instructions/common.instructions.md) (catalog: `instructions/skill-helpers--instructions--common-instructions-md.html`)
- **common** — [common.mdc](../foundational/skill-helpers/instructions/common.mdc) (catalog: `instructions/skill-helpers--instructions--common-mdc.html`)
- **log-and-fix-skill-errors** — [log-and-fix-skill-errors.instructions.md](../foundational/skill-helpers/instructions/log-and-fix-skill-errors.instructions.md) (catalog: `instructions/skill-helpers--instructions--log-and-fix-skill-errors-instructions-md.html`)
- **log-and-fix-skill-errors** — [log-and-fix-skill-errors.mdc](../foundational/skill-helpers/instructions/log-and-fix-skill-errors.mdc) (catalog: `instructions/skill-helpers--instructions--log-and-fix-skill-errors-mdc.html`)
- **workspace** — [workspace.mdc](../foundational/skill-helpers/instructions/workspace.mdc) (catalog: `instructions/skill-helpers--instructions--workspace-mdc.html`)

**Prompts — .prompt.md → slash commands**

- **common** — [common.prompt.md](../foundational/skill-helpers/prompts/common.prompt.md) (catalog: `prompts/skill-helpers--prompts--common-prompt-md.html`)
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
| **abd-impact-mapping** | `practices` | Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources. | [SKILL.md](../practices/idea-shaping/skills/abd-impact-mapping/SKILL.md) |
| **abd-opportunity-canvas** | `practices` | Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build. | [SKILL.md](../practices/idea-shaping/skills/abd-opportunity-generation/SKILL.md) |
| **abd-simple-validated-learning** | `practices` | Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build. | [SKILL.md](../practices/idea-shaping/skills/abd-simple-validated-learning/SKILL.md) |
| **abd-cost-of-delay** | `practices` | Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay. | [SKILL.md](../practices/idea-shaping/skills/abd-cost-of-delay/SKILL.md) |
| **module-partition** | `practices` | After domain scan, partition the source corpus into modules by allocating source file references to per-module index files. No classes, no anchors ” only module boundaries and file references to the source that belongs to each. Supports an Unallocated bucket for pending decisions and a Rejected … | [SKILL.md](../practices/domain-driven-design/skills/abd-module-partition/SKILL.md) |
| **domain-terms** | `practices` | Extract domain terms, group them into Key Abstractions, and produce a single domain-terms file — the shared vocabulary and building blocks for the module. | [SKILL.md](../practices/domain-driven-design/skills/abd-domain-terms/SKILL.md) |
| **abd-ubiquitous-language** | `practices` | Build a shared, rigorous vocabulary for the scope you are modeling — extract terms, group them into Key Abstractions, and sketch each concept's behavior — all in one file every downstream artifact can rely on. | [SKILL.md](../practices/domain-driven-design/skills/abd-ubiquitous-language/SKILL.md) |
| **class-responsibility-collaborator** | `practices` | For every domain concept: assign responsibilities, name collaborators, and declare invariants — all in one structured pass before object-model. | [SKILL.md](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/SKILL.md) |
| **object-model** | `practices` | Build a typed object model for a module. A CRC model makes it faster but is not required. Use when a module needs a typed domain surface before writing production code, or when a module has reached state: crc. | [SKILL.md](../practices/domain-driven-design/skills/abd-object-model/SKILL.md) |
| **ddd-design-building-blocks** | `practices` | Surface the business questions that DDD building block stereotypes encode — identity, consistency boundaries, ownership, and integration — and classify each domain concept (Entity, Value Object, Aggregate, Service, Domain Event) from a CRC, object model, or ubiquitous language. | [SKILL.md](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/SKILL.md) |
| **drawio-domain-sync** | `practices` | Render Ubiquitous Language, CRC, or object model artifacts to Draw.io class diagrams — one page per Key Abstraction — and sync diagram edits back to the source model. | [SKILL.md](../practices/domain-driven-design/skills/drawio-domain-sync/SKILL.md) |
| **scenario-walkthrough** | `practices` | Walk concrete scenarios through the object model. Every step maps to a class and operation; lifecycle guards and invariants come from the prior phase. Output is a standalone per-phase file. | [SKILL.md](../practices/domain-driven-design/skills/abd-scenario-walkthrough/SKILL.md) |
| **bounded-context-map** | `practices` | Map bounded contexts and their relationships so integration strategy, team collaboration, and domain translation are explicit before they are discovered in production. | [SKILL.md](../practices/domain-driven-design/skills/abd-bounded-context-map/SKILL.md) |
| **abd-story-mapping** | `practices` | Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources. | [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md) |
| **abd-thin-slicing** | `practices` | Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates. | [SKILL.md](../practices/story-driven-delivery/skills/abd-thin-slicing/SKILL.md) |
| **abd-acceptance-criteria** | `practices` | WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for common. | [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/SKILL.md) |
| **abd-specification-by-example** | `practices` | Given/When/Then scenarios with real domain values; plain or outline (data tables) templates. | [SKILL.md](../practices/story-driven-delivery/skills/abd-specification-by-example/SKILL.md) |
| **abd-acceptance-test-driven-development** | `practices` | Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR). | [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/SKILL.md) |
| **drawio-story-sync** | `practices` | story-graph.json to Draw.io story maps; validated load/save and diagram sync. | [SKILL.md](../practices/story-driven-delivery/skills/drawio-story-sync/SKILL.md) |
| **miro-story-sync** | `practices` | story-graph.json to Miro story maps; validated load and REST-driven board sync. | [SKILL.md](../practices/story-driven-delivery/skills/miro-story-sync/SKILL.md) |
| **story-graph-ops** | `practices` | CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift. | [SKILL.md](../practices/story-driven-delivery/skills/story-graph-ops/SKILL.md) |
| **abd-information-architecture** | `practices` | Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a … | [SKILL.md](../practices/kanban/user-experience-design/skills/abd-information-architecture/SKILL.md) |
| **abd-ux-mockup** | `practices` | Precision pass after the initial IA — specify exact controls, interactions, and states for any scope (full site, flow, epic, story), drawn in Draw.io as a lo-fi wireframe and saved as a versioned .drawio artifact. | [SKILL.md](../practices/kanban/user-experience-design/skills/abd-ux-mockup/SKILL.md) |
| **abd-interface-design** | `practices` | Translate the approved hi-fi mockup for a screen into production-grade, functional, accessible interface code in the chosen framework — without changing the domain labels, acceptance criteria, or visual decisions. | [SKILL.md](../practices/kanban/user-experience-design/skills/abd-interface-design/SKILL.md) |
| **abd-architecture-outline** | `practices` | Produce the first architecture artifact for a new or unfamiliar system — a mostly-diagrams document that fixes platform, layering, system context, deployment topology, guiding principles, technology stack, and a brief catalogue of major systems with decision records. The outline answers "what is … | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md) |
| **abd-architecture-blueprint** | `practices` | Produce the second-level architecture document after the outline — a blueprint that names each architectural component in a paragraph or two (purpose, dependencies, interactions, no internal details), names every cross-cutting concern as a typed "architecture mechanism" (security, error handling … | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md) |
| **abd-architecture-reference** | `practices` | Read abd-architecture-template output and produce runnable code files — the actual implementation of one architecture mechanism — either from the current project's stories or from a built-in hello-world scenario. | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-reference/SKILL.md) |
| **abd-architecture-template** | `practices` | Produce an architecture reference document for a specified architecture — one mechanism (e.g. error handling, caching, persistence, auth) at a time — so a downstream implementation skill can build code that matches. Each mechanism section names its principles and patterns, draws participants as a … | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-template/SKILL.md) |
| **abd-clean-code** | `practices` | Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS). | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-clean-code/SKILL.md) |
| **abd-secure-code** | `practices` | OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write and prove security-sensitive production code before merge. | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-secure-code/SKILL.md) |
| **mern-technical-architecture** | `practices` | Domain-first MERN web applications: domain modules, shared logic, Clean Architecture layers, story-driven tests, scanner-verified compliance. | [SKILL.md](../practices/architecture-centric-engineering/skills/mern-technical-architecture/SKILL.md) |
| **abd-build-architecture-skill** | `practices` | Build a new implementation skill — a full practice-skill package that generates code in a chosen architecture — from an architecture-mechanism reference document. Input is a finished reference (one file with layered description and one section per mechanism, covering principles, patterns, file … | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/SKILL.md) |
| **abd-service-level-objectives** | `practices` | Capture the non-functional requirements (NFRs) of a system as concrete Service Level Indicators, Objectives, and Agreements (SLI/SLO/SLA) tied to a specific scope — a story, an epic, a parent epic, or the whole system. NFRs are organised into six categories (Performance & Scalability, Availability … | [SKILL.md](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/SKILL.md) |
| **hero-vtt-technical-architecture** | `practices` | Generate production Hero Virtual Tabletop (WPF C#) modules following the three-layer architecture — Presentation (ViewModel) · Domain · COH Integration. Enforces the Skinny ViewModel, COH Game Bridge Seam, and Direct Memory Manipulation mechanisms from inputs/architecture-reference.md. | [SKILL.md](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/SKILL.md) |
| **abd-kanban-planning** | `practices` | Strategy selection and system of work configuration — no pre-planned runs or slot tables. | [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md) |
| **kanban-estimation** | `practices` | Collaborative estimation at any scope level — contributing factors, categories, team vote, and recorded rationale. | [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md) |
| **abd-kanban** | `practices` | JIT Kanban board for kanban-lead and role agents. delivery-war-room/ under the engagement workspace is the authoritative source of all delivery progress — board.json, system-of-work.json, metrics, and ticket history. Tickets flow through stages, scatter at scope boundaries, and agents pull … | [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md) |
| **abd-kanban-repo** | `practices` | Manage git history for a delivery engagement. Commits, branches, pushes, and PRs are driven by ticket state changes on the Kanban board — not by slots or runs. --- | [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md) |
| **abd-chunk-markdown** | `foundational` | Split converted Markdown into retrieval-sized chunks with evidence labels, guided by a structure-based chunking spec. Use when the user wants to "chunk documents", "split for RAG", "draft a chunking strategy", or prepare markdown for embedding and semantic search. | [SKILL.md](../foundational/context-to-memory/skills/abd-chunk-markdown/SKILL.md) |
| **abd-convert-to-markdown** | `foundational` | Convert office documents (PDF, PPTX, DOCX, XLSX, etc.) to navigable Markdown with real headings, sections, and tables. Use when the user wants to convert a document or folder of documents to markdown, mentions "convert to markdown", "extract text", or needs source files prepared for chunking or … | [SKILL.md](../foundational/context-to-memory/skills/abd-convert-to-markdown/SKILL.md) |
| **abd-embed-vectors** | `foundational` | Embed text chunks into a local FAISS vector index for semantic search. Use when the user wants to "embed chunks", "build a vector index", "create embeddings", or prepare chunked content for RAG retrieval. | [SKILL.md](../foundational/context-to-memory/skills/abd-embed-vectors/SKILL.md) |
| **abd-search-memory** | `foundational` | Semantic search over a local FAISS vector index built from document chunks. Use when the user says "use memory", "search memory", "what does memory say", "from our content", "what do we have on [topic]", or asks about content that has been ingested into agent memory. | [SKILL.md](../foundational/context-to-memory/skills/abd-search-memory/SKILL.md) |
| **abd-semantic-context-chunker** | `foundational` | Index scattered source content by the kind of context it provides — Story, Domain, Architecture, UX — so you know what you have before deeper analysis begins. | [SKILL.md](../foundational/context-to-memory/skills/abd-semantic-context-chunker/SKILL.md) |
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
| **common** | `foundational` | Run scanners, validate output against rules, fix failures; quality gate before and after work. | [SKILL.md](../foundational/skill-helpers/skills/common/skill-rule-workflow.md) |
| **skill-garden-catalogue** | `foundational` | Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML index page. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the inventory current. | [SKILL.md](../foundational/skill-helpers/skills/skill-garden-catalogue/SKILL.md) |
| **track-task** | `foundational` | Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace. | [SKILL.md](../foundational/skill-helpers/skills/track_task/SKILL.md) |

## Summary — Agents

| Agent | Plugin | Description | Open |
| --- | --- | --- | --- |
| **business-expert** | `practices` | You are a persistent Business Expert executor — one session, many skills. | [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md) |
| **business-expert-reviewer** | `practices` | You are a persistent Business Expert reviewer — one session, many review tasks. | [AGENT.md](../practices/kanban/agents/business-expert-reviewer/AGENT.md) |
| **engineer** | `practices` | You are a persistent Engineer executor — one session, many skills. | [AGENT.md](../practices/kanban/agents/engineer/AGENT.md) |
| **engineer-reviewer** | `practices` | You are a persistent Engineer reviewer — one session, many review tasks. | [AGENT.md](../practices/kanban/agents/engineer-reviewer/AGENT.md) |
| **kanban-lead** | `practices` | > PERSISTENT LOOP — MUST STAY RUNNING UNTIL ALL WORK COMPLETE. > > The kanban lead uses the loop skill to stay alive across the full engagement. A background shell emits a sentinel every N seconds; notify_on_output wakes the agent for a new turn each tick. Each turn is one scan cycle — read board … | [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md) |
| **product-owner** | `practices` | You are a persistent Product Owner executor — one session, many skills. | [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md) |
| **product-owner-reviewer** | `practices` | You are a persistent Product Owner reviewer — one session, many review tasks. | [AGENT.md](../practices/kanban/agents/product-owner-reviewer/AGENT.md) |
| **ux-designer** | `practices` | You are a persistent UX Designer executor — one session, many skills. | [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md) |
| **ux-designer-reviewer** | `practices` | You are a persistent UX Designer reviewer — one session, many review tasks. | [AGENT.md](../practices/kanban/agents/ux-designer-reviewer/AGENT.md) |
| **abd-context-to-memory** | `foundational` | Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and semantic search. Optional: review context_chunking_spec.yaml before chunk+embed. | [AGENTS.md](../foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md) |
| **abd-practice-skill-builder** | `foundational` | Goal: Produce practice skills under the agilebydesign-skills repository, in skills/<skill-name>/, grounded in abd-answers (Pinecone RAG): retrieve evidence, author the package (SKILL.md starter from abd-author-practice-skill template + *rules/.md), optional scanners, abd-skill-catalog, then an HTML … | [AGENTS.md](../foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md) |
| **ai-research-assistant** | `utilities` | Orchestrate hypothesis-driven research on AI-augmented delivery and context engineering practices. You coordinate three skills in sequence to produce a research report that helps the user decide whether their approach is well-founded, exposed, or genuinely novel. You are an impartial advisor — not … | [AGENTS.md](../utilities/agents/ai-research-assistant/AGENTS.md) |

---

## Skills (detail)

### abd-impact-mapping

- **Directory:** [`practices/idea-shaping/skills/abd-impact-mapping/`](../practices/idea-shaping/skills/abd-impact-mapping/)

**Summary:**

Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.

**Description (from Purpose / body):**

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see why an option might matter before debating build order.

The map answers four questions in order (see Core concepts): Why are we doing this? Who can help or hinder? How should behaviour change? What could we do to support that change? Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

This skill defines the ideas behind a sound map, how to structure one, and what good looks like. Workspace layout, CLIs, and agent wiring belong in other skills.

**Repository layout:**

- **[inputs/](../practices/idea-shaping/skills/abd-impact-mapping/inputs)** — Folder (2 items).
- **[rules/](../practices/idea-shaping/skills/abd-impact-mapping/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/idea-shaping/skills/abd-impact-mapping/templates)** — Authoring templates and structural skeletons.
- [README.md](../practices/idea-shaping/skills/abd-impact-mapping/README.md) — catalogue_summary: "Impact maps: goal, actors, behaviour impacts, and deliverable options grounded in discovery."
- [SKILL.md](../practices/idea-shaping/skills/abd-impact-mapping/SKILL.md) — name: abd-impact-mapping

### abd-opportunity-canvas

- **Directory:** [`practices/idea-shaping/skills/abd-opportunity-generation/`](../practices/idea-shaping/skills/abd-opportunity-generation/)

**Summary:**

Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build.

**Description (from Purpose / body):**

This skill exists so you do not start "building a solution" while people are thinking about a different problem, a different customer, or a different definition of success. 

This skill makes an opportunity explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that downstream build and delivery work is based on a shared model. This skill captures this alignment as an opportunity model, in the form of a opportunity canvas.

Every part of the canvas is also a candidate assumption — beliefs about customers, value, and capability that teams often make explicit, turn into falsifiable statements, and run through a lightweight validation path outside this skill (see abd-simple-validated-learning). This skill’s job is to surface that uncertainty in the model; who …

**Repository layout:**

- **[rules/](../practices/idea-shaping/skills/abd-opportunity-generation/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/idea-shaping/skills/abd-opportunity-generation/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/idea-shaping/skills/abd-opportunity-generation/SKILL.md) — name: abd-opportunity-canvas

### abd-simple-validated-learning

- **Directory:** [`practices/idea-shaping/skills/abd-simple-validated-learning/`](../practices/idea-shaping/skills/abd-simple-validated-learning/)

**Summary:**

Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.

**Description (from Purpose / body):**

Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. This skill is for surfacing those assumptions explicitly and working through them iteratively before the organisation treats them as fact or commits to a full build. The agent (or facilitator) mines the supplied context for assumptions, rewrites them as falsifiable hypotheses, prioritises them into a validation backlog, and structures each item to move through Plan → Validate → Learn.

The skill emphasises up-front discovery and validation:research, analysis, assessing current and target state (eg operations, finances, systems) validation with SMEs, deep dives, quick prototypes, cohort tests, and other relatively cheap validation activities. A longer build–measure–learn loop belongs in delivery practices once the …

**Repository layout:**

- **[inputs/](../practices/idea-shaping/skills/abd-simple-validated-learning/inputs)** — Folder (1 items).
- **[rules/](../practices/idea-shaping/skills/abd-simple-validated-learning/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/idea-shaping/skills/abd-simple-validated-learning/templates)** — Authoring templates and structural skeletons.
- [README.md](../practices/idea-shaping/skills/abd-simple-validated-learning/README.md) — catalogue_summary: >-
- [SKILL.md](../practices/idea-shaping/skills/abd-simple-validated-learning/SKILL.md) — name: abd-simple-validated-learning

### abd-cost-of-delay

- **Directory:** [`practices/idea-shaping/skills/abd-cost-of-delay/`](../practices/idea-shaping/skills/abd-cost-of-delay/)

**Summary:**

Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay.

**Description (from Purpose / body):**

Teams routinely prioritize work by gut feel, stakeholder loudness, or first-in-first-out — all of which ignore how much value decays while items wait to be delivered. Cost of Delay puts a price tag on time so teams can make scheduling decisions based on economics rather than politics. 

This skill packages that method, it classifies the value type and urgency of each feature or initiative in context, then builds a simple value model that makes assumptions explicit, calculatse Cost of Delay per time period (month / week), and divides value by time by duration to get Cost of Delay Divided By Duration (CD3), and rank so the highest-value shortest-duration work goes first.

**Repository layout:**

- **[rules/](../practices/idea-shaping/skills/abd-cost-of-delay/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/idea-shaping/skills/abd-cost-of-delay/scanners)** — Folder (4 items).
- **[scripts/](../practices/idea-shaping/skills/abd-cost-of-delay/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/idea-shaping/skills/abd-cost-of-delay/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/idea-shaping/skills/abd-cost-of-delay/SKILL.md) — name: abd-cost-of-delay

### module-partition

- **Directory:** [`practices/domain-driven-design/skills/abd-module-partition/`](../practices/domain-driven-design/skills/abd-module-partition/)

**Summary:**

After domain scan, partition the source corpus into modules by allocating source file references to per-module index files. No classes, no anchors ” only module boundaries and file references to the source that belongs to each. Supports an Unallocated bucket for pending decisions and a Rejected …

**Description (from Purpose / body):**

Produce a root index (module-partition.md) plus per-module files under abd-domain-driven-design/modules/ ” each containing scope, core terms, and source file references (not verbatim copies). No classes, no anchors, no UML, no stereotypes. Just boundaries and pointers to the source text that lives inside them.

This is the scope cut before any class identification. It answers a single question for every chunk of source: which module does this text belong to ” or is it unallocated (pending) or rejected (out of scope)?

### Why references, not verbatim copies

When the source is already structured as individually addressable files (corpus chunks, markdown files, scanned documents), copying their full content into the partition document is pure duplication. The partition's real value is the allocation decision ” which files belong to which module. Downstream agents read the module …

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-module-partition/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-module-partition/scanners)** — Folder (2 items).
- **[templates/](../practices/domain-driven-design/skills/abd-module-partition/templates)** — Authoring templates and structural skeletons.
- [Deploy-ToCursor.ps1](../practices/domain-driven-design/skills/abd-module-partition/Deploy-ToCursor.ps1) — .SYNOPSIS
- [SKILL.md](../practices/domain-driven-design/skills/abd-module-partition/SKILL.md) — name: module-partition

### domain-terms

- **Directory:** [`practices/domain-driven-design/skills/abd-domain-terms/`](../practices/domain-driven-design/skills/abd-domain-terms/)

**Summary:**

Extract domain terms, group them into Key Abstractions, and produce a single domain-terms file — the shared vocabulary and building blocks for the module.

**Description (from Purpose / body):**

Build a shared, rigorous vocabulary for each module — the terms, behaviors, and rules that domain experts and modelers agree on — and immediately structure them into Key Abstractions (named building blocks) so that every conversation, document, and downstream artifact uses the same language without translation.

This is a single-pass skill. It does not produce a flat term list first and a KA file second. It reads source, identifies terms, groups them into KAs, and writes one file.

---

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-domain-terms/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-domain-terms/scanners)** — Folder (3 items).
- **[templates/](../practices/domain-driven-design/skills/abd-domain-terms/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-domain-terms/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [SKILL.md](../practices/domain-driven-design/skills/abd-domain-terms/SKILL.md) — name: domain-terms

### abd-ubiquitous-language

- **Directory:** [`practices/domain-driven-design/skills/abd-ubiquitous-language/`](../practices/domain-driven-design/skills/abd-ubiquitous-language/)

**Summary:**

Build a shared, rigorous vocabulary for the scope you are modeling — extract terms, group them into Key Abstractions, and sketch each concept's behavior — all in one file every downstream artifact can rely on.

**Description (from Purpose / body):**

Build a shared, rigorous vocabulary for the scope you are modeling so that domain experts and modelers agree on what each term means, what each concept does, and which rules must always hold — and capture that agreement in one living document the whole team uses without translation. The scope of one run can be a single module, several modules, or a whole-system sweep; the skill and its output shape stay the same.

This is a three-pass skill. It does not produce a flat term list first, a key-abstractions file second, and a concept-sketch file third. It reads source, extracts terms with definitions, groups them into Key Abstractions, sketches each concept's behavior and properties, and writes one file.

The final output is a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties. The skill applies …

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-ubiquitous-language/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-ubiquitous-language/scanners)** — Folder (2 items).
- **[templates/](../practices/domain-driven-design/skills/abd-ubiquitous-language/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-ubiquitous-language/corrections-log.md) — ﻿# Corrections log
- [SKILL.md](../practices/domain-driven-design/skills/abd-ubiquitous-language/SKILL.md) — name: abd-ubiquitous-language

### class-responsibility-collaborator

- **Directory:** [`practices/domain-driven-design/skills/abd-class-responsibility-collaborator/`](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/)

**Summary:**

For every domain concept: assign responsibilities, name collaborators, and declare invariants — all in one structured pass before object-model.

**Description (from Purpose / body):**

This skill takes domain concepts from a completed Ubiquitous Language and produces a structured CRC model: for each concept, what it is responsible for, who it collaborates with, and what must always remain true. The result is a module file with ### Class Responsibility Collaborator sections appended after the existing Ubiquitous Language content.

CRC (Class-Responsibility-Collaborator) modeling, introduced by Ward Cunningham and Kent Beck, is a lightweight way to explore object-oriented designs. This skill extends the classic technique by requiring explicit property and operation names, inline invariants, and subtype deltas — so the team can reason about ownership and boundaries before writing code.

---

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/scanners)** — Folder (4 items).
- **[templates/](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [skill-errors-log.md](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/skill-errors-log.md) — Skill Errors Log — abd-class-responsibility-collaborator
- [SKILL.md](../practices/domain-driven-design/skills/abd-class-responsibility-collaborator/SKILL.md) — name: class-responsibility-collaborator

### object-model

- **Directory:** [`practices/domain-driven-design/skills/abd-object-model/`](../practices/domain-driven-design/skills/abd-object-model/)

**Summary:**

Build a typed object model for a module. A CRC model makes it faster but is not required. Use when a module needs a typed domain surface before writing production code, or when a module has reached state: crc.

**Description (from Purpose / body):**

Build a typed object model for a module. When a CRC model exists it is the primary input — the skill converts that behavioral model into a typed domain surface with far less effort. Without a CRC the skill can still produce an object model directly from domain knowledge.

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-object-model/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/domain-driven-design/skills/abd-object-model/scanners)** — Folder (7 items).
- **[templates/](../practices/domain-driven-design/skills/abd-object-model/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-object-model/corrections-log.md) — ﻿# Corrections log
- [SKILL.md](../practices/domain-driven-design/skills/abd-object-model/SKILL.md) — name: object-model

### ddd-design-building-blocks

- **Directory:** [`practices/domain-driven-design/skills/abd-ddd-design-building-blocks/`](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/)

**Summary:**

Surface the business questions that DDD building block stereotypes encode — identity, consistency boundaries, ownership, and integration — and classify each domain concept (Entity, Value Object, Aggregate, Service, Domain Event) from a CRC, object model, or ubiquitous language.

**Description (from Purpose / body):**

This skill works through a domain model concept by concept, identifying the right technical constraints through a set of questions that — while technical in framing — can only be answered by business requirements. 

FOr example:
-  if two patients have the same name and date of birth, should we consider them the same patient?  
- If a product changes, when do we update the inventory system? 

This skill answers these questions by introducing Domain Driven Design Building Blocks. Every DDD building block — Entity, Value Object, Aggregate, Service, Domain Event — looks technical but expose a question only the business can answer. 

THis skill models these elements by understanding business requirements for identity semantics, consistency boundaries, immutability guarantees, and integration contracts across business concepts and business systems.

**Repository layout:**

- **[ide-files/](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/ide-files)** — Folder (2 items).
- **[rules/](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/abd-ddd-design-building-blocks/SKILL.md) — name: ddd-design-building-blocks

### drawio-domain-sync

- **Directory:** [`practices/domain-driven-design/skills/drawio-domain-sync/`](../practices/domain-driven-design/skills/drawio-domain-sync/)

**Summary:**

Render Ubiquitous Language, CRC, or object model artifacts to Draw.io class diagrams — one page per Key Abstraction — and sync diagram edits back to the source model.

**Description (from Purpose / body):**

This skill turns any domain model artifact — a Ubiquitous Language, CRC model, or object model — into a Draw.io class diagram the whole team can read, annotate, and edit. Each Key Abstraction in the source file becomes its own page in the diagram, keeping visual scope manageable and per-abstraction structure clear. When the team edits the diagram in Draw.io, the skill syncs those changes back to the source model file, so diagram and text never drift apart.

Positioning and layout are AI-driven: the agent reads the source, reasons about class relationships and inheritance chains, and places elements where the diagram reads best. There are no fixed grid scripts to run.

---

**Repository layout:**

- **[ide-files/](../practices/domain-driven-design/skills/drawio-domain-sync/ide-files)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/drawio-domain-sync/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../practices/domain-driven-design/skills/drawio-domain-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/domain-driven-design/skills/drawio-domain-sync/templates)** — Authoring templates and structural skeletons.
- [diagrams.md](../practices/domain-driven-design/skills/drawio-domain-sync/diagrams.md) — <!-- section: story_synthesizer.diagrams -->
- [skill-errors-log.md](../practices/domain-driven-design/skills/drawio-domain-sync/skill-errors-log.md) — ﻿# drawio-domain-sync — skill errors log
- [SKILL.md](../practices/domain-driven-design/skills/drawio-domain-sync/SKILL.md) — name: drawio-domain-sync

### scenario-walkthrough

- **Directory:** [`practices/domain-driven-design/skills/abd-scenario-walkthrough/`](../practices/domain-driven-design/skills/abd-scenario-walkthrough/)

**Summary:**

Walk concrete scenarios through the object model. Every step maps to a class and operation; lifecycle guards and invariants come from the prior phase. Output is a standalone per-phase file.

**Description (from Purpose / body):**

Walk concrete scenarios through the typed object model (or CRC where the object model is not yet built). Each step must map to a class and an operation from the prior phase's file. When a step crosses a state change or must respect a guard, align with the invariants and interactions captured upstream. If a step has no owner, record a gap and revise upstream artifacts.

**Repository layout:**

- **[rules/](../practices/domain-driven-design/skills/abd-scenario-walkthrough/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/abd-scenario-walkthrough/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/domain-driven-design/skills/abd-scenario-walkthrough/corrections-log.md) — ﻿# Corrections log
- [SKILL.md](../practices/domain-driven-design/skills/abd-scenario-walkthrough/SKILL.md) — name: scenario-walkthrough

### bounded-context-map

- **Directory:** [`practices/domain-driven-design/skills/abd-bounded-context-map/`](../practices/domain-driven-design/skills/abd-bounded-context-map/)

**Summary:**

Map bounded contexts and their relationships so integration strategy, team collaboration, and domain translation are explicit before they are discovered in production.

**Description (from Purpose / body):**

Teams working across multiple models, services, or subsystems need a single shared picture of how those pieces relate — which concepts cross boundaries, how the systems talk to each other, and how the teams will collaborate. Without that picture, integration strategy is discovered in production, translation is ad hoc, and team dependencies are invisible until they block someone. This skill produces a Bounded Context Map: a named inventory of every bounded context with every dependency declared across three explicit dimensions — domain mapping, integration mechanism, and team engagement model — so the architecture is honest and the team structure matches.

---

**Repository layout:**

- **[inputs/](../practices/domain-driven-design/skills/abd-bounded-context-map/inputs)** — Folder (1 items).
- **[markdown/](../practices/domain-driven-design/skills/abd-bounded-context-map/markdown)** — Folder (1 items).
- **[rules/](../practices/domain-driven-design/skills/abd-bounded-context-map/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/domain-driven-design/skills/abd-bounded-context-map/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/domain-driven-design/skills/abd-bounded-context-map/SKILL.md) — name: bounded-context-map
- [stuff.docx](../practices/domain-driven-design/skills/abd-bounded-context-map/stuff.docx) — PK     ! ��4��  ?   [Content_Types].xml …

### abd-story-mapping

- **Directory:** [`practices/story-driven-delivery/skills/abd-story-mapping/`](../practices/story-driven-delivery/skills/abd-story-mapping/)

**Summary:**

Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources.

**Description (from Purpose / body):**

A story map in the Jeff Patton sense is a single shared picture of the product: you organize understanding into a small stack of nested levels—epics (broad capability areas), sub-epics (flows or feature areas within an epic), and stories (leaves: one observable user or system interaction each). The map is not a dump of source material, a WBS, or a list of build tasks; it is outcomes and behaviors—what happens in the product—so product, delivery, and domain people can read the same structure.

Naming is part of the model: epics, sub-epics, and stories use verb–noun titles; who is acting (persona/actor, user vs. system) is carried outside the name (e.g. story_type / diagram convention), not stuffed into the title. Good maps read as a journey (sequence along the backbone) and a skeleton of scope (depth into detail), with consistent language from top to bottom.

This document defines …

**Repository layout:**

- **[rules/](../practices/story-driven-delivery/skills/abd-story-mapping/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-story-mapping/scanners)** — Folder (6 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-story-mapping/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-story-mapping/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [README.md](../practices/story-driven-delivery/skills/abd-story-mapping/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/story-driven-delivery/skills/abd-story-mapping/SKILL.md) — name: abd-story-mapping

### abd-thin-slicing

- **Directory:** [`practices/story-driven-delivery/skills/abd-thin-slicing/`](../practices/story-driven-delivery/skills/abd-thin-slicing/)

**Summary:**

Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates.

**Description (from Purpose / body):**

Define prioritized increments. Group stories in a story map (and any notes on risk, constraints, or learning goals) into prioritized increments that can be delivered together. Each incremement includes its priority order, outcomes, slicing notes, and an ordered list od stories.

**Repository layout:**

- **[rules/](../practices/story-driven-delivery/skills/abd-thin-slicing/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-thin-slicing/scanners)** — Folder (2 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-thin-slicing/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-thin-slicing/corrections-log.md) — Corrections log
- [README.md](../practices/story-driven-delivery/skills/abd-thin-slicing/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/story-driven-delivery/skills/abd-thin-slicing/SKILL.md) — name: abd-thin-slicing

### abd-acceptance-criteria

- **Directory:** [`practices/story-driven-delivery/skills/abd-acceptance-criteria/`](../practices/story-driven-delivery/skills/abd-acceptance-criteria/)

**Summary:**

WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for common.

**Description (from Purpose / body):**

Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit negatives (BUT). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

This skill is the practice standard for that work: templates for deliverables, rules for what “good” means (atomic AC, actor alternation, domain emphasis, channel-specific detail, source evidence when AC come from documents), and scanners that can run predictable mechanical checks alongside human review.

**Repository layout:**

- **[rules/](../practices/story-driven-delivery/skills/abd-acceptance-criteria/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-acceptance-criteria/scanners)** — Folder (14 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-acceptance-criteria/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [README.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/README.md) — One line for catalogue cards and grids (YAML string).
- [skill-errors-log.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/skill-errors-log.md) — Skill Errors Log — abd-acceptance-criteria
- [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-criteria/SKILL.md) — name: abd-acceptance-criteria

### abd-specification-by-example

- **Directory:** [`practices/story-driven-delivery/skills/abd-specification-by-example/`](../practices/story-driven-delivery/skills/abd-specification-by-example/)

**Summary:**

Given/When/Then scenarios with real domain values; plain or outline (data tables) templates.

**Description (from Purpose / body):**

Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

**Repository layout:**

- **[rules/](../practices/story-driven-delivery/skills/abd-specification-by-example/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-specification-by-example/scanners)** — Folder (3 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-specification-by-example/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-specification-by-example/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [README.md](../practices/story-driven-delivery/skills/abd-specification-by-example/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/story-driven-delivery/skills/abd-specification-by-example/SKILL.md) — name: abd-specification-by-example

### abd-acceptance-test-driven-development

- **Directory:** [`practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/`](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/)

**Summary:**

Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR).

**Description (from Purpose / body):**

Write tests first. Write code to pass them.

This skill creates executable test files — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is test-driven: write a test that expresses the expected behavior, run it to confirm it fails (RED), then rely on a  downstream skill or agent to develop the production code skill to implement until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do —  test methods show the Given-When-Then flow and helper functions do the work.

The skill covers the full test quality bar: domain language in names, observable-behavior assertions, coverage of normal and …

**Repository layout:**

- **[rules/](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/scanners)** — Folder (2 items).
- **[templates/](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/corrections-log.md) — ——#   C o r r e c t i o n s   l o g 
- [README.md](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/story-driven-delivery/skills/abd-acceptance-test-driven-development/SKILL.md) — name: abd-acceptance-test-driven-development

### drawio-story-sync

- **Directory:** [`practices/story-driven-delivery/skills/drawio-story-sync/`](../practices/story-driven-delivery/skills/drawio-story-sync/)

**Summary:**

story-graph.json to Draw.io story maps; validated load/save and diagram sync.

**Description (from Purpose / body):**

Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance criteria, prioritization increments) from story-graph.json. Uses story-graph-ops for validated JSON load/save and story_graph_ops (StoryMap, nodes, domain) for the story tree that DrawIO rendering expects. Use when producing or diffing story-map.drawio files, or when wiring CI/scripts for diagram refresh and update reports.

**Repository layout:**

- **[guidance/](../practices/story-driven-delivery/skills/drawio-story-sync/guidance)** — Folder (2 items).
- **[ide-files/](../practices/story-driven-delivery/skills/drawio-story-sync/ide-files)** — Folder (1 items).
- **[scripts/](../practices/story-driven-delivery/skills/drawio-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/drawio-story-sync/tests)** — Folder (3 items).
- [README.md](../practices/story-driven-delivery/skills/drawio-story-sync/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/story-driven-delivery/skills/drawio-story-sync/SKILL.md) — name: drawio-story-sync

### miro-story-sync

- **Directory:** [`practices/story-driven-delivery/skills/miro-story-sync/`](../practices/story-driven-delivery/skills/miro-story-sync/)

**Summary:**

story-graph.json to Miro story maps; validated load and REST-driven board sync.

**Description (from Purpose / body):**

Render and synchronize story-map Miro boards (outline today; exploration with acceptance criteria and prioritization increments planned) from story-graph.json. Reuses the common diagram_story_sync package (DiagramStoryNode ABCs, layout constants, comparison helpers, UpdateReport) and implements Miro-specific element creation, board I/O, and a pluggable MiroTransport (REST API v2 + in-memory fake for tests). Use when producing or refreshing Miro story maps from story-graph.json, or when wiring CI/scripts for Miro board updates.

**Repository layout:**

- **[scripts/](../practices/story-driven-delivery/skills/miro-story-sync/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/miro-story-sync/tests)** — Folder (2 items).
- [README.md](../practices/story-driven-delivery/skills/miro-story-sync/README.md) — catalogue_summary: "Render and synchronize story-map Miro boards (outline today; exploration with acceptance criteria and prioritization increments planned) from story-graph.json …
- [SKILL.md](../practices/story-driven-delivery/skills/miro-story-sync/SKILL.md) — name: miro-story-sync

### story-graph-ops

- **Directory:** [`practices/story-driven-delivery/skills/story-graph-ops/`](../practices/story-driven-delivery/skills/story-graph-ops/)

**Summary:**

CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift.

**Description (from Purpose / body):**

Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after hand-writing JSON from memory or from reading other repositories for “schema hints.” Prefer the story-graph CLI; use story_map and related modules for richer edits. Complements ABD practice skills—ops skill owns the serialized graph lifecycle on disk.

**Repository layout:**

- **[guidance/](../practices/story-driven-delivery/skills/story-graph-ops/guidance)** — Folder (2 items).
- **[ide-files/](../practices/story-driven-delivery/skills/story-graph-ops/ide-files)** — Folder (1 items).
- **[logs/](../practices/story-driven-delivery/skills/story-graph-ops/logs)** — Folder (1 items).
- **[scripts/](../practices/story-driven-delivery/skills/story-graph-ops/scripts)** — Build, catalogue, validation, or packaging automation.
- **[tests/](../practices/story-driven-delivery/skills/story-graph-ops/tests)** — Folder (10 items).
- [MIGRATION_PARITY.md](../practices/story-driven-delivery/skills/story-graph-ops/MIGRATION_PARITY.md) — Story graph parity: agile_bots → story-graph-ops
- [README.md](../practices/story-driven-delivery/skills/story-graph-ops/README.md) — One line for catalogue cards and grids (YAML string).
- [skill-errors-log.md](../practices/story-driven-delivery/skills/story-graph-ops/skill-errors-log.md) — Corrections log
- [SKILL.md](../practices/story-driven-delivery/skills/story-graph-ops/SKILL.md) — name: story-graph-ops

### abd-information-architecture

- **Directory:** [`practices/kanban/user-experience-design/skills/abd-information-architecture/`](../practices/kanban/user-experience-design/skills/abd-information-architecture/)

**Summary:**

Produce a first-pass information architecture for a solution scope — a site map of screens and transitions, the navigational components that connect them, and a content model (types, hierarchy, labels, tags, key actions) for what lives on each screen — saved as a structured markdown spec and a …

**Description (from Purpose / body):**

The purpose of this skill is to produce the initial information architecture for a solution scope.

Information architecture (IA) is the practice of structuring, organizing, and labeling the surfaces and content of a solution so users can find what they need and understand where they are. It covers two dimensions — navigation (how a user moves through the solution and the components that carry that movement) and content (what lives on each surface, how it is grouped, what it is called, and what users can do with it).

A site map — the inventory of screens and the directed transitions between them — is one component of the IA: the navigation backbone. This skill produces it alongside the rest of the IA in a single low-fidelity pass.

Doing this work early, before detailed design or development, flushes out gaps in functional and domain understanding, surfaces disagreements about scope …

**Repository layout:**

- **[rules/](../practices/kanban/user-experience-design/skills/abd-information-architecture/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[screen-templates/](../practices/kanban/user-experience-design/skills/abd-information-architecture/screen-templates)** — Folder (86 items).
- **[scripts/](../practices/kanban/user-experience-design/skills/abd-information-architecture/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/kanban/user-experience-design/skills/abd-information-architecture/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/kanban/user-experience-design/skills/abd-information-architecture/corrections-log.md) — abd-information-architecture — corrections log
- [SKILL.md](../practices/kanban/user-experience-design/skills/abd-information-architecture/SKILL.md) — catalog_garden_tier: practice

### abd-ux-mockup

- **Directory:** [`practices/kanban/user-experience-design/skills/abd-ux-mockup/`](../practices/kanban/user-experience-design/skills/abd-ux-mockup/)

**Summary:**

Precision pass after the initial IA — specify exact controls, interactions, and states for any scope (full site, flow, epic, story), drawn in Draw.io as a lo-fi wireframe and saved as a versioned .drawio artifact.

**Description (from Purpose / body):**

The initial IA established the screen inventory, regions, and story coverage. The lo-fi mockup is the next precision pass: it locks down exactly which control renders each field, exactly what interactions are available in each state, and exactly what the user sees and does — without yet committing to visual design. Every input becomes a specific control type (text field, dropdown, checkbox). Every action becomes a positioned button with a primary/secondary weight. Every conditional state (validation error, empty list, disabled control) is explicitly placed. This skill packages that pass: take one IA screen, resolve its AC and domain terms, build a drawio-mockup.mjs state file, generate the .drawio wireframe, and save it — so interaction decisions are made deliberately and traceable, not invented during implementation.

Critical principle: The lo-fi mockup must faithfully reproduce the …

**Repository layout:**

- **[rules/](../practices/kanban/user-experience-design/skills/abd-ux-mockup/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../practices/kanban/user-experience-design/skills/abd-ux-mockup/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/kanban/user-experience-design/skills/abd-ux-mockup/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/kanban/user-experience-design/skills/abd-ux-mockup/corrections-log.md) — abd-lo-fi — corrections log
- [SKILL.md](../practices/kanban/user-experience-design/skills/abd-ux-mockup/SKILL.md) — catalog_garden_tier: practice

### abd-interface-design

- **Directory:** [`practices/kanban/user-experience-design/skills/abd-interface-design/`](../practices/kanban/user-experience-design/skills/abd-interface-design/)

**Summary:**

Translate the approved hi-fi mockup for a screen into production-grade, functional, accessible interface code in the chosen framework — without changing the domain labels, acceptance criteria, or visual decisions.

**Description (from Purpose / body):**

Hi-fi mockups settle look and feel. The interface stage is where they become real code — and where most teams quietly stop honouring the upstream artifacts because "we're shipping now". This skill keeps that integrity: the implementation renders the same regions, the same affordances, the same labels, the same acceptance criteria, and the same visual decisions as the approved hi-fi, in production-grade code that an end user can actually use. It treats acceptance criteria as the testable surface (every clause is a working behaviour with a check), treats the ubiquitous language as the public vocabulary (labels and copy stay verbatim from the UL and AC), and treats accessibility and performance as constraints that are met, not aspirations that are mentioned. The result is one screen implemented in the chosen framework, traceable end-to-end from story to running interface.

---

**Repository layout:**

- **[rules/](../practices/kanban/user-experience-design/skills/abd-interface-design/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/kanban/user-experience-design/skills/abd-interface-design/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/kanban/user-experience-design/skills/abd-interface-design/corrections-log.md) — abd-interface-design — corrections log
- [SKILL.md](../practices/kanban/user-experience-design/skills/abd-interface-design/SKILL.md) — catalog_garden_tier: practice

### abd-architecture-outline

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-outline/`](../practices/architecture-centric-engineering/skills/abd-architecture-outline/)

**Summary:**

Produce the first architecture artifact for a new or unfamiliar system — a mostly-diagrams document that fixes platform, layering, system context, deployment topology, guiding principles, technology stack, and a brief catalogue of major systems with decision records. The outline answers "what is …

**Description (from Purpose / body):**

A team that cannot draw its system on one page also cannot agree on what to build next. Outlines fix that. This skill produces the first architecture artifact for a system — short on prose, heavy on diagrams — so engineers, product, and stakeholders share a single picture of the platform, the layers, the neighbours, the deployment topology, and the principles in force. When the outline is in place, deeper architecture work (blueprint, reference, mechanisms) can start without re-litigating what the system is.

**Repository layout:**

- **[ide-files/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/ide-files)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scanner-report)** — Folder (1 items).
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scanners)** — Folder (1 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-outline/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/corrections-log.md) — ——#   C o r r e c t i o n s   l o g   —— —   a b d - a r c h i t e c t u r e - o u t l i n e 
- [deployment-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/deployment-architecture.png) — IHDR  *  ~   ��1�   sRGB ��
- [layered-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/layered-architecture.png) — IHDR  �  X   L��P   sRGB ��
- [platform-architecture.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/platform-architecture.png) — IHDR  (  4   P�   sRGB ��
- [process.docx](../practices/architecture-centric-engineering/skills/abd-architecture-outline/process.docx) — PK     ! ——
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md) — catalog_garden_tier: practice
- [system-context.png](../practices/architecture-centric-engineering/skills/abd-architecture-outline/system-context.png) — IHDR    Y   ݸ��   sRGB ��

### abd-architecture-blueprint

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-blueprint/`](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/)

**Summary:**

Produce the second-level architecture document after the outline — a blueprint that names each architectural component in a paragraph or two (purpose, dependencies, interactions, no internal details), names every cross-cutting concern as a typed "architecture mechanism" (security, error handling …

**Description (from Purpose / body):**

The outline shows what a system is; the blueprint shows what it is made of. A blueprint is the document a tech lead opens to answer "where does the order code live? what does it depend on? how does it talk to the catalogue?" without yet drilling into the implementation patterns. It names every architectural component in a paragraph or two, catalogues every cross-cutting concern as an architecture mechanism, shows the data architecture at the model level, captures the common testing strategy, and lists the decisions taken at this level. When the blueprint is in place, the architecture reference can go deep on one mechanism at a time without re-explaining the system to its reader.

**Repository layout:**

- **[ide-files/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/ide-files)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scanner-report)** — Folder (1 items).
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scanners)** — Folder (1 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-blueprint/SKILL.md) — catalog_garden_tier: practice

### abd-architecture-reference

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-reference/`](../practices/architecture-centric-engineering/skills/abd-architecture-reference/)

**Summary:**

Read abd-architecture-template output and produce runnable code files — the actual implementation of one architecture mechanism — either from the current project's stories or from a built-in hello-world scenario.

**Description (from Purpose / body):**

abd-architecture-template produces a reference document that specifies how a mechanism is structured, what files exist, how types collaborate, and how the flow runs. This skill takes that reference document as its blueprint and produces the actual runnable code files that realise the mechanism — domain classes, entry points, and tests — ready to execute.

Two paths are available: use the real project's architecture reference and one in-scope story to generate real implementation files, or use the built-in "Simple Calculator" scenario so any team can see a complete, working three-layer example with zero prior setup.

**Repository layout:**

- **[ide-files/](../practices/architecture-centric-engineering/skills/abd-architecture-reference/ide-files)** — Folder (1 items).
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-reference/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-reference/SKILL.md) — catalog_garden_tier: practice

### abd-architecture-template

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-architecture-template/`](../practices/architecture-centric-engineering/skills/abd-architecture-template/)

**Summary:**

Produce an architecture reference document for a specified architecture — one mechanism (e.g. error handling, caching, persistence, auth) at a time — so a downstream implementation skill can build code that matches. Each mechanism section names its principles and patterns, draws participants as a …

**Description (from Purpose / body):**

Architecture decisions usually live in someone's head, a deck, or a wiki page that nobody opens twice. This skill packages those decisions into a single reference document for the chosen architecture so that any team member can implement the same mechanism the same way the next person did, and the one after that. The reference is the contract: it names the principles the architecture refuses to break, fixes the patterns that satisfy them, draws the participants, shows the flow, and gives code samples a reviewer can compare against. When the reference is done, "how do we do caching here?" has one answer, "where does error handling live?" has one answer, and the team stops re-litigating those questions every sprint.

**Repository layout:**

- **[inputs/](../practices/architecture-centric-engineering/skills/abd-architecture-template/inputs)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-architecture-template/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-architecture-template/scanner-report)** — Folder (1 items).
- **[templates/](../practices/architecture-centric-engineering/skills/abd-architecture-template/templates)** — Authoring templates and structural skeletons.
- [Key Mechanism Design.docx](../practices/architecture-centric-engineering/skills/abd-architecture-template/Key Mechanism Design.docx) — PK     ! —A—y  
- [skill-errors-log.md](../practices/architecture-centric-engineering/skills/abd-architecture-template/skill-errors-log.md) — Skill errors log — abd-architecture-template
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-architecture-template/SKILL.md) — catalog_garden_tier: practice

### abd-clean-code

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-clean-code/`](../practices/architecture-centric-engineering/skills/abd-clean-code/)

**Summary:**

Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS).

**Description (from Purpose / body):**

Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

The skill covers the full implementation quality bar: names that reveal intent, guard-clause control flow, no magic numbers, no swallowed exceptions, no hidden globals, encapsulated internals, and domain vocabulary throughout.

**Repository layout:**

- **[rules/](../practices/architecture-centric-engineering/skills/abd-clean-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-clean-code/scanners)** — Folder (2 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-clean-code/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-clean-code/templates)** — Authoring templates and structural skeletons.
- [corrections-log.md](../practices/architecture-centric-engineering/skills/abd-clean-code/corrections-log.md) — abd-clean-code — corrections log
- [README.md](../practices/architecture-centric-engineering/skills/abd-clean-code/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-clean-code/SKILL.md) — name: abd-clean-code

### abd-secure-code

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-secure-code/`](../practices/architecture-centric-engineering/skills/abd-secure-code/)

**Summary:**

OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write and prove security-sensitive production code before merge.

**Description (from Purpose / body):**

Engineers ship features faster than attackers find gaps — but only when secure defaults are explicit, reviewable, and mechanically checkable. This skill packages Secure Code Warrior guidance into concrete coding rules and automated scanners so teams and agents can write security-sensitive code and prove it meets the same bar before merge.

**Repository layout:**

- **[inputs/](../practices/architecture-centric-engineering/skills/abd-secure-code/inputs)** — Folder (5 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-secure-code/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-secure-code/scanners)** — Folder (5 items).
- **[scripts/](../practices/architecture-centric-engineering/skills/abd-secure-code/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/architecture-centric-engineering/skills/abd-secure-code/templates)** — Authoring templates and structural skeletons.
- **[test/](../practices/architecture-centric-engineering/skills/abd-secure-code/test)** — Automated tests for the agent or skill package.
- [README.md](../practices/architecture-centric-engineering/skills/abd-secure-code/README.md) — catalogue_summary: "OWASP-aligned secure coding rules and Python, Java, and JavaScript scanners — write security-sensitive production code and prove it with mechanical checks …
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-secure-code/SKILL.md) — name: abd-secure-code

### mern-technical-architecture

- **Directory:** [`practices/architecture-centric-engineering/skills/mern-technical-architecture/`](../practices/architecture-centric-engineering/skills/mern-technical-architecture/)

**Summary:**

Domain-first MERN web applications: domain modules, shared logic, Clean Architecture layers, story-driven tests, scanner-verified compliance.

**Description (from Purpose / body):**

Generate production MERN web applications using a domain-first architecture — organizing by business capability, sharing domain logic across tiers, enforcing Clean Architecture layer purity, and testing with story-driven scenarios.

This skill produces real, runnable TypeScript domain modules — each with a shared/ domain core, server/ Express backend, and client/ React frontend. The output follows the architecture defined in inputs/mern-architecture.md: domain entities with business logic, Zod validation schemas shared across tiers, collection classes with domain-oriented query methods, and story-driven tests mirroring Gherkin scenarios.

**Repository layout:**

- **[inputs/](../practices/architecture-centric-engineering/skills/mern-technical-architecture/inputs)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/mern-technical-architecture/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/architecture-centric-engineering/skills/mern-technical-architecture/scanners)** — Folder (1 items).
- **[templates/](../practices/architecture-centric-engineering/skills/mern-technical-architecture/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/mern-technical-architecture/SKILL.md) — name: mern-technical-architecture

### abd-build-architecture-skill

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-build-architecture-skill/`](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/)

**Summary:**

Build a new implementation skill — a full practice-skill package that generates code in a chosen architecture — from an architecture-mechanism reference document. Input is a finished reference (one file with layered description and one section per mechanism, covering principles, patterns, file …

**Description (from Purpose / body):**

A team can write down its architecture and still ship code that drifts from it within a quarter. Documents do not enforce themselves. This skill closes that gap by turning a finished architecture document into an active, automatable practice — a packaged generator that produces real code in the architecture on demand, with checkable rules an agent or reviewer can run against any change. The output is itself a skill: a folder with SKILL.md, templates/, rules/, and ide-files/ ready to be loaded and run. When this skill is done, the architecture is no longer just written down somewhere; it is something the team can invoke — to scaffold a new module, to check a pull request, to onboard a new engineer — and get the same answer every time.

**Repository layout:**

- **[rules/](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/scanner-report)** — Folder (1 items).
- **[templates/](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/templates)** — Authoring templates and structural skeletons.
- [skill-errors-log.md](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/skill-errors-log.md) — Skill errors log — abd-build-architecture-skill
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-build-architecture-skill/SKILL.md) — name: abd-build-architecture-skill

### abd-service-level-objectives

- **Directory:** [`practices/architecture-centric-engineering/skills/abd-service-level-objectives/`](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/)

**Summary:**

Capture the non-functional requirements (NFRs) of a system as concrete Service Level Indicators, Objectives, and Agreements (SLI/SLO/SLA) tied to a specific scope — a story, an epic, a parent epic, or the whole system. NFRs are organised into six categories (Performance & Scalability, Availability …

**Description (from Purpose / body):**

A non-functional requirement that cannot be measured is a wish. Teams that ship without measurable NFRs discover the truth in production — too late, too expensive, sometimes too public. This skill turns each NFR into a concrete Service Level Indicator (what is measured), Service Level Objective (the target on that indicator), and where a customer-facing commitment exists, a Service Level Agreement. Critically, each objective is scoped to the functional area it applies to: a single user story, an epic, a parent epic, or the system as a whole. Read-mostly catalogue browsing does not need the durability guarantee of order-placement, and treating them the same wastes money on the former and risks failure on the latter.

**Repository layout:**

- **[ide-files/](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/ide-files)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/scanner-report)** — Folder (1 items).
- **[scanners/](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/scanners)** — Folder (1 items).
- **[templates/](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/abd-service-level-objectives/SKILL.md) — name: abd-service-level-objectives

### hero-vtt-technical-architecture

- **Directory:** [`practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/`](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/)

**Summary:**

Generate production Hero Virtual Tabletop (WPF C#) modules following the three-layer architecture — Presentation (ViewModel) · Domain · COH Integration. Enforces the Skinny ViewModel, COH Game Bridge Seam, and Direct Memory Manipulation mechanisms from inputs/architecture-reference.md.

**Description (from Purpose / body):**

Generate production Hero Virtual Tabletop modules using the architecture fixed in inputs/architecture-reference.md — organizing by feature folder, enforcing strict layer purity (Presentation → Domain → COH Integration interfaces), and following the three mechanism patterns the reference defines.

This skill produces real, runnable C# files. Code is co-located by feature (Module.HeroVirtualTabletop/{Feature}/). ViewModels are thin binding adapters. Domain classes hold all business rules and call game operations only through injected interfaces. Every concrete COH type lives exclusively in Library/GameCommunicator/ or Library/ProcessCommunicator/.

**Repository layout:**

- **[inputs/](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/inputs)** — Folder (1 items).
- **[rules/](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/architecture-centric-engineering/skills/hero-vtt-technical-architecture/SKILL.md) — name: hero-vtt-technical-architecture

### abd-kanban-planning

- **Directory:** [`practices/kanban/skills/abd-kanban-planning/`](../practices/kanban/skills/abd-kanban-planning/)

**Summary:**

Strategy selection and system of work configuration — no pre-planned runs or slot tables.

**Description (from Purpose / body):**

Select delivery strategy, configure system of work (stages, scope progression, skill order), and define scatter/decomposition rules. Planning drives the Kanban board via strategy — not by pre-authoring runs, slots, or assignments.

**Repository layout:**

- **[rules/](../practices/kanban/skills/abd-kanban-planning/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanners/](../practices/kanban/skills/abd-kanban-planning/scanners)** — Folder (2 items).
- **[scripts/](../practices/kanban/skills/abd-kanban-planning/scripts)** — Build, catalogue, validation, or packaging automation.
- **[strategies/](../practices/kanban/skills/abd-kanban-planning/strategies)** — Folder (10 items).
- **[tests/](../practices/kanban/skills/abd-kanban-planning/tests)** — Folder (3 items).
- [corrections-log.md](../practices/kanban/skills/abd-kanban-planning/corrections-log.md) — abd-kanban-planning — corrections log
- [README.md](../practices/kanban/skills/abd-kanban-planning/README.md) — One line for catalogue cards and grids (YAML string).
- [SKILL.md](../practices/kanban/skills/abd-kanban-planning/SKILL.md) — name: abd-kanban-planning

### kanban-estimation

- **Directory:** [`practices/kanban/skills/kanban-estimation/`](../practices/kanban/skills/kanban-estimation/)

**Summary:**

Collaborative estimation at any scope level — contributing factors, categories, team vote, and recorded rationale.

**Description (from Purpose / body):**

Teams estimate badly not because they lack a formula but because they skip the conversation. Effort gets assigned by one person's hunch, contributing factors go unexamined, and nobody records why a number landed where it did — so every future re-estimate starts from scratch. Delivery estimation packages the facilitation pattern that makes sizing collaborative, factor-aware, and traceable: teams walk through backlog items one at a time, name what drives effort, agree on a category, and save the reasoning alongside the number.

**Repository layout:**

- **[ide-files/](../practices/kanban/skills/kanban-estimation/ide-files)** — Folder (2 items).
- **[rules/](../practices/kanban/skills/kanban-estimation/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scanner-report/](../practices/kanban/skills/kanban-estimation/scanner-report)** — Folder (1 items).
- **[templates/](../practices/kanban/skills/kanban-estimation/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/kanban/skills/kanban-estimation/SKILL.md) — name: kanban-estimation

### abd-kanban

- **Directory:** [`practices/kanban/skills/abd-kanban/`](../practices/kanban/skills/abd-kanban/)

**Summary:**

JIT Kanban board for kanban-lead and role agents. delivery-war-room/ under the engagement workspace is the authoritative source of all delivery progress — board.json, system-of-work.json, metrics, and ticket history. Tickets flow through stages, scatter at scope boundaries, and agents pull …

**Description (from Purpose / body):**

Single on-disk home for progress and handoffs. Models delivery as a JIT Kanban board where work tickets flow through stages defined by a system of work, scatter into finer-grained tickets at scope boundaries, and role agents pull skill-level tasks from active tickets.

**Repository layout:**

- **[rules/](../practices/kanban/skills/abd-kanban/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../practices/kanban/skills/abd-kanban/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../practices/kanban/skills/abd-kanban/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../practices/kanban/skills/abd-kanban/SKILL.md) — name: abd-kanban

### abd-kanban-repo

- **Directory:** [`practices/kanban/skills/abd-kanban-repo/`](../practices/kanban/skills/abd-kanban-repo/)

**Summary:**

Manage git history for a delivery engagement. Commits, branches, pushes, and PRs are driven by ticket state changes on the Kanban board — not by slots or runs. ---

**Description (from Purpose / body):**

Manage git history for a delivery engagement. Commits, branches, pushes, and PRs are driven by ticket state changes on the Kanban board — not by slots or runs.

---

**Repository layout:**

- **[scripts/](../practices/kanban/skills/abd-kanban-repo/scripts)** — Build, catalogue, validation, or packaging automation.
- [SKILL.md](../practices/kanban/skills/abd-kanban-repo/SKILL.md) — abd-kanban-repo

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

Index scattered source content by the kind of context it provides — Story, Domain, Architecture, UX — so you know what you have before deeper analysis begins.

**Description (from Purpose / body):**

Engagements accumulate context from many places — requirements documents, code repositories, design files, meeting notes, technical specs — and nobody knows what they actually have until someone reads it all. This skill scans the full corpus, tags every piece by the kind of context it provides — Story, Domain, Architecture, UX — and produces a coverage index so teams and agents know what evidence exists and where the gaps are, before any deeper analysis begins.

**Repository layout:**

- **[references/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/references)** — Folder (1 items).
- **[rules/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[templates/](../foundational/context-to-memory/skills/abd-semantic-context-chunker/templates)** — Authoring templates and structural skeletons.
- [SKILL.md](../foundational/context-to-memory/skills/abd-semantic-context-chunker/SKILL.md) — name: abd-semantic-context-chunker

### abd-author-practice-skill

- **Directory:** [`foundational/skill-builder/skills/abd-author-practice-skill/`](../foundational/skill-builder/skills/abd-author-practice-skill/)

**Summary:**

Turn collected hub evidence into a finished practice skill: clear instructions and checkable do-and-don't norms that stay true to what you retrieved.

**Description (from Purpose / body):**

Teams need practice skills that people and agents can follow without improvising or drifting away from what the sources actually say. This authoring skill helps you finish such a package after you have already chosen what to keep from the hub: the teaching on the skill page reads clearly, and the norms on the outputs are explicit enough to pass or fail. It guides you from that evidence to aligned prose and checks. Prerequisites, Build, and Not in this pass on this page carry retrieval, bundling, and scanner wiring when you need those steps.

**Repository layout:**

- **[ide-files/](../foundational/skill-builder/skills/abd-author-practice-skill/ide-files)** — Folder (2 items).
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

Respond to client proposals (RFP, Q&A, requirements) by converting materials to memory, creating a response strategy, and answering questions iteratively. Depends on abd-context-to-memory for RAG. Use when responding to proposals, creating response plans, answering RFP questions, or iterating on proposal strategy.

**Repository layout:**

- **[content/](../utilities/skills/abd-proposal-respond/content)** — Source parts merged into agent instructions or outputs.
- **[rules/](../utilities/skills/abd-proposal-respond/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../utilities/skills/abd-proposal-respond/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../utilities/skills/abd-proposal-respond/AGENTS.md) — Core Definitions
- [README.md](../utilities/skills/abd-proposal-respond/README.md) — abd-proposal-respond
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

- **[content/](../foundational/skill-helpers/skills/commit-msg/content)** — Source parts merged into agent instructions or outputs.
- **[docs/](../foundational/skill-helpers/skills/commit-msg/docs)** — Human-oriented documentation for the package.
- **[rules/](../foundational/skill-helpers/skills/commit-msg/rules)** — Practice rules (DO/DON'T) and constraints used with scanners.
- **[scripts/](../foundational/skill-helpers/skills/commit-msg/scripts)** — Build, catalogue, validation, or packaging automation.
- [AGENTS.md](../foundational/skill-helpers/skills/commit-msg/AGENTS.md) — Core Definitions
- [README.md](../foundational/skill-helpers/skills/commit-msg/README.md) — ace-commit-msg
- [skill-config.json](../foundational/skill-helpers/skills/commit-msg/skill-config.json) — "name": "abd-commit-msg",
- [SKILL.md](../foundational/skill-helpers/skills/commit-msg/SKILL.md) — name: abd-commit-msg

### common

- **Directory:** [`foundational/skill-helpers/skills/common/`](../foundational/skill-helpers/skills/common/)

**Summary:**

Run scanners, validate output against rules, fix failures; quality gate before and after work.

**Description (from Purpose / body):**

Read rules before work, validate output (AI pass + scanner pass), and follow the correction process after mistakes.

**Repository layout:**

- **[guidance/](../foundational/skill-helpers/skills/common/guidance)** — Folder (3 items).
- **[ide-files/](../foundational/skill-helpers/skills/common/ide-files)** — Folder (3 items).
- **[scripts/](../foundational/skill-helpers/skills/common/scripts)** — Build, catalogue, validation, or packaging automation.
- **[templates/](../foundational/skill-helpers/skills/common/templates)** — Authoring templates and structural skeletons.
- **[tests/](../foundational/skill-helpers/skills/common/tests)** — Folder (4 items).
- [SKILL.md](../foundational/skill-helpers/skills/common/skill-rule-workflow.md) — name: common

### skill-garden-catalogue

- **Directory:** [`foundational/skill-helpers/skills/skill-garden-catalogue/`](../foundational/skill-helpers/skills/skill-garden-catalogue/)

**Summary:**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML index page. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the inventory current.

**Description (from Purpose / body):**

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML index page. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the inventory current.

**Repository layout:**

- **[agents/](../foundational/skill-helpers/skills/skill-garden-catalogue/agents)** — Folder (2 items).
- **[architecture-centric-engineering/](../foundational/skill-helpers/skills/skill-garden-catalogue/architecture-centric-engineering)** — Folder (2 items).
- **[context-to-memory/](../foundational/skill-helpers/skills/skill-garden-catalogue/context-to-memory)** — Folder (4 items).
- **[delivery/](../foundational/skill-helpers/skills/skill-garden-catalogue/delivery)** — Folder (2 items).
- **[domain-driven-design/](../foundational/skill-helpers/skills/skill-garden-catalogue/domain-driven-design)** — Folder (7 items).
- **[idea shaping/](../foundational/skill-helpers/skills/skill-garden-catalogue/idea shaping)** — Folder (4 items).
- **[scripts/](../foundational/skill-helpers/skills/skill-garden-catalogue/scripts)** — Build, catalogue, validation, or packaging automation.
- **[skill-builder/](../foundational/skill-helpers/skills/skill-garden-catalogue/skill-builder)** — Folder (5 items).
- **[skill-helpers/](../foundational/skill-helpers/skills/skill-garden-catalogue/skill-helpers)** — Folder (7 items).
- **[story-driven-delivery/](../foundational/skill-helpers/skills/skill-garden-catalogue/story-driven-delivery)** — Folder (8 items).
- **[templates/](../foundational/skill-helpers/skills/skill-garden-catalogue/templates)** — Authoring templates and structural skeletons.
- **[utilities/](../foundational/skill-helpers/skills/skill-garden-catalogue/utilities)** — Folder (2 items).
- [index.html](../foundational/skill-helpers/skills/skill-garden-catalogue/index.html) — <!DOCTYPE html>
- [README.md](../foundational/skill-helpers/skills/skill-garden-catalogue/README.md) — One line for catalogue cards and grids (YAML string).
- [skill-inventory.md](../foundational/skill-helpers/skills/skill-garden-catalogue/skill-inventory.md) — Skill Garden — Inventory
- [SKILL.md](../foundational/skill-helpers/skills/skill-garden-catalogue/SKILL.md) — name: skill-garden-catalogue

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

---

## Agents (detail)

### business-expert

- **Directory:** [`practices/kanban/agents/business-expert/`](../practices/kanban/agents/business-expert/)
- **Entry:** [`practices/kanban/agents/business-expert/AGENT.md`](../practices/kanban/agents/business-expert/AGENT.md)

**Summary:**

You are a persistent Business Expert executor — one session, many skills.

**Description:**

# Business Expert — Delivery Executor

You are a persistent Business Expert executor — one session, many skills.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull skill-level work from active tickets on board.json — skills where role: business-expert and status: to_do.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Business Expert (business-expert) |
| slot_type | executor |
| Playbook | ../../content/roles/business-expert.md |

## Work queue

Claiming, skill order, and priority: _shared/work-queue.md

## Workflow

Follow _shared/executor-workflow.md for every claimed skill.

## Relationship to kanban-lead

The lead manages the board, triggers scatters, and scales the agent pool. You pull eligible skills from active tickets …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/business-expert/AGENT.md) — Business Expert — Delivery Executor

### business-expert-reviewer

- **Directory:** [`practices/kanban/agents/business-expert-reviewer/`](../practices/kanban/agents/business-expert-reviewer/)
- **Entry:** [`practices/kanban/agents/business-expert-reviewer/AGENT.md`](../practices/kanban/agents/business-expert-reviewer/AGENT.md)

**Summary:**

You are a persistent Business Expert reviewer — one session, many review tasks.

**Description:**

# Business Expert — Delivery Reviewer

You are a persistent Business Expert reviewer — one session, many review tasks.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull review work from active tickets on board.json — skills where role: business-expert, status: done, and review_status: null.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Business Expert (business-expert) |
| slot_type | reviewer |
| Validates | Business Expert executor artifacts only |

## Work queue

Claiming and priority: _shared/work-queue.md

## Workflow

Follow _shared/reviewer-workflow.md for every claimed review.

The kanban lead logs corrections and marks skills for rework when you report failures.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/business-expert-reviewer/AGENT.md) — Business Expert — Delivery Reviewer

### engineer

- **Directory:** [`practices/kanban/agents/engineer/`](../practices/kanban/agents/engineer/)
- **Entry:** [`practices/kanban/agents/engineer/AGENT.md`](../practices/kanban/agents/engineer/AGENT.md)

**Summary:**

You are a persistent Engineer executor — one session, many skills.

**Description:**

# Engineer — Delivery Executor

You are a persistent Engineer executor — one session, many skills.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull skill-level work from active tickets on board.json — skills where role: engineer and status: to_do.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Engineer (engineer) |
| slot_type | executor |
| Playbook | ../../content/roles/engineer.md |

## Work queue

Claiming, skill order, and priority: _shared/work-queue.md

## Workflow

Follow _shared/executor-workflow.md for every claimed skill.

## Relationship to kanban-lead

The lead manages the board, triggers scatters, and scales the agent pool. You pull eligible skills from active tickets matching your role. The matching …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/engineer/AGENT.md) — Engineer — Delivery Executor

### engineer-reviewer

- **Directory:** [`practices/kanban/agents/engineer-reviewer/`](../practices/kanban/agents/engineer-reviewer/)
- **Entry:** [`practices/kanban/agents/engineer-reviewer/AGENT.md`](../practices/kanban/agents/engineer-reviewer/AGENT.md)

**Summary:**

You are a persistent Engineer reviewer — one session, many review tasks.

**Description:**

# Engineer — Delivery Reviewer

You are a persistent Engineer reviewer — one session, many review tasks.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull review work from active tickets on board.json — skills where role: engineer, status: done, and review_status: null.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Engineer (engineer) |
| slot_type | reviewer |
| Validates | Engineer executor artifacts only |

## Common practice skills

- abd-architecture-blueprint, abd-architecture-template, abd-architecture-reference
- abd-object-model, abd-acceptance-test-driven-development, abd-clean-code
- Stack skills: mern-technical-architecture, hero-vtt-technical-architecture

When running scanners for stack skills, include --language …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/engineer-reviewer/AGENT.md) — Engineer — Delivery Reviewer

### kanban-lead

- **Directory:** [`practices/kanban/agents/kanban-lead/`](../practices/kanban/agents/kanban-lead/)
- **Entry:** [`practices/kanban/agents/kanban-lead/AGENT.md`](../practices/kanban/agents/kanban-lead/AGENT.md)

**Summary:**

> PERSISTENT LOOP — MUST STAY RUNNING UNTIL ALL WORK COMPLETE. > > The kanban lead uses the loop skill to stay alive across the full engagement. A background shell emits a sentinel every N seconds; notify_on_output wakes the agent for a new turn each tick. Each turn is one scan cycle — read board …

**Description:**

# ABD Kanban Lead

> PERSISTENT LOOP — MUST STAY RUNNING UNTIL ALL WORK COMPLETE.
>
> The kanban lead uses the loop skill to stay alive across the full engagement. A background shell emits a sentinel every N seconds; notify_on_output wakes the agent for a new turn each tick. Each turn is one scan cycle — read board, advance tickets, scatter, spawn/nudge role agents, return.
>
> How to start:
>
> 1. Start a background shell loop:
>    powershell
>    while ($true) { Start-Sleep -Seconds 30; Write-Output 'AGENT_LOOP_TICK_kanban_lead {"prompt":"Scan cycle: read board, advance tickets, manage agents."}' }
>    
>    Use block_until_ms: 0 and notify_on_output with pattern ^AGENT_LOOP_TICK_kanban_lead.
>
> 2. Run the first scan cycle immediately.
>
> 3. On each subsequent tick, perform one scan …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/kanban-lead/AGENT.md) — ABD Kanban Lead

### product-owner

- **Directory:** [`practices/kanban/agents/product-owner/`](../practices/kanban/agents/product-owner/)
- **Entry:** [`practices/kanban/agents/product-owner/AGENT.md`](../practices/kanban/agents/product-owner/AGENT.md)

**Summary:**

You are a persistent Product Owner executor — one session, many skills.

**Description:**

# Product Owner — Delivery Executor

You are a persistent Product Owner executor — one session, many skills.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull skill-level work from active tickets on board.json — skills where role: product-owner and status: to_do.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Product Owner (product-owner) |
| slot_type | executor |
| Playbook | ../../content/roles/product-owner.md |

## Work queue

Claiming, skill order, and priority: _shared/work-queue.md

## Workflow

Follow _shared/executor-workflow.md for every claimed skill.

## Relationship to kanban-lead

The lead manages the board, triggers scatters, and scales the agent pool. You pull eligible skills from active tickets matching your …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/product-owner/AGENT.md) — Product Owner — Delivery Executor

### product-owner-reviewer

- **Directory:** [`practices/kanban/agents/product-owner-reviewer/`](../practices/kanban/agents/product-owner-reviewer/)
- **Entry:** [`practices/kanban/agents/product-owner-reviewer/AGENT.md`](../practices/kanban/agents/product-owner-reviewer/AGENT.md)

**Summary:**

You are a persistent Product Owner reviewer — one session, many review tasks.

**Description:**

# Product Owner — Delivery Reviewer

You are a persistent Product Owner reviewer — one session, many review tasks.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull review work from active tickets on board.json — skills where role: product-owner, status: done, and review_status: null.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | Product Owner (product-owner) |
| slot_type | reviewer |
| Validates | PO executor artifacts only |

## Which practice skill?

Per claimed review, the skill name is the key in the ticket's skills object. Resolve scanners to <workspace>/.cursor/skills/<skill-name>.

## Work queue

Claiming and priority: _shared/work-queue.md

## Workflow

Follow _shared/reviewer-workflow.md for every claimed review.

The …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/product-owner-reviewer/AGENT.md) — Product Owner — Delivery Reviewer

### ux-designer

- **Directory:** [`practices/kanban/agents/ux-designer/`](../practices/kanban/agents/ux-designer/)
- **Entry:** [`practices/kanban/agents/ux-designer/AGENT.md`](../practices/kanban/agents/ux-designer/AGENT.md)

**Summary:**

You are a persistent UX Designer executor — one session, many skills.

**Description:**

# UX Designer — Delivery Executor

You are a persistent UX Designer executor — one session, many skills.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull skill-level work from active tickets on board.json — skills where role: ux-designer and status: to_do.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | UX Designer (ux-designer) |
| slot_type | executor |
| Playbook | ../../content/roles/ux-designer.md |

## Work queue

Claiming, skill order, and priority: _shared/work-queue.md

## Workflow

Follow _shared/executor-workflow.md for every claimed skill.

## Relationship to kanban-lead

The lead manages the board, triggers scatters, and scales the agent pool. You pull eligible skills from active tickets matching your role. The …

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/ux-designer/AGENT.md) — UX Designer — Delivery Executor

### ux-designer-reviewer

- **Directory:** [`practices/kanban/agents/ux-designer-reviewer/`](../practices/kanban/agents/ux-designer-reviewer/)
- **Entry:** [`practices/kanban/agents/ux-designer-reviewer/AGENT.md`](../practices/kanban/agents/ux-designer-reviewer/AGENT.md)

**Summary:**

You are a persistent UX Designer reviewer — one session, many review tasks.

**Description:**

# UX Designer — Delivery Reviewer

You are a persistent UX Designer reviewer — one session, many review tasks.

kanban-lead spawns you once as an isolated subagent with bootstrap payload only. You pull review work from active tickets on board.json — skills where role: ux-designer, status: done, and review_status: null.

## Fixed identity

| Field | Value |
| --- | --- |
| team-role | UX Designer (ux-designer) |
| slot_type | reviewer |
| Validates | UX Designer executor artifacts only |

## Work queue

Claiming and priority: _shared/work-queue.md

## Workflow

Follow _shared/reviewer-workflow.md for every claimed review.

The kanban lead logs corrections and marks skills for rework when you report failures.

**Repository layout:**

- [AGENT.md](../practices/kanban/agents/ux-designer-reviewer/AGENT.md) — UX Designer — Delivery Reviewer

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
- **[content/](../foundational/context-to-memory/agents/abd-context-to-memory/content)** — Source parts merged into agent instructions or outputs.
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
