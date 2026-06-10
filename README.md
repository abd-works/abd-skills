# abd.works AI Garden

Reusable **plugins**, **skills**, and **agents** from [abd.works](https://agilebydesign.com) — story-driven delivery, domain modeling, UX, architecture, delivery orchestration, and skill authoring.

| Browse the catalog | |
| --- | --- |
| **HTML hub** (plugins, skills, agents, kanban) | [Preview](https://htmlpreview.github.io/?https://github.com/abd-works/agilebydesign-skills/blob/main/catalog/index.html) · [`catalog/index.html`](catalog/index.html) |
| **Markdown outline** (same content, diffable; renders on GitHub) | [`catalog/outline.md`](catalog/outline.md) |
| **Delivery kanban** (stages × practice plugins) | [Preview](https://htmlpreview.github.io/?https://github.com/abd-works/agilebydesign-skills/blob/main/catalog/kanban-layout/index.html) · [`catalog/kanban-layout/index.html`](catalog/kanban-layout/index.html) |

_HTML preview opens in Engineer (dark) mode by default._

## Plugins

Repo-root capability **plugins** deploy with `deploy_family_package.py` or the full deploy script. Each plugin bundles some of: `agents/`, `skills/`, `content/`, `instructions/`, `prompts/`, `lib/`, `scripts/`.

### Practice plugins

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Idea shaping** | [`idea-shaping/`](idea-shaping/README.md) | Opportunity framing, impact mapping, cost of delay, and validated learning — before delivery work begins |
| **Story-driven delivery** | [`story-driven-delivery/`](story-driven-delivery/README.md) | Story map → acceptance criteria → specification by example → acceptance tests; plus story-graph ops and diagram sync |
| **Domain-driven design** | [`domain-driven-design/`](domain-driven-design/README.md) | Module partition, domain terms, ubiquitous language, CRC, object model, DDD building blocks, bounded contexts, and domain diagram sync |
| **User experience design** | [`user-experience-design/`](user-experience-design/README.md) | Information architecture, lo-fi wireframe mockups, and production interface design — from screen inventory to accessible running code |
| **Architecture-centric engineering** | [`architecture-centric-engineering/`](architecture-centric-engineering/README.md) | Architecture outline → blueprint → template → reference → generated code; clean code, secure code, SLOs, and stack-specific skills |
| **Kanban** | [`kanban/`](kanban/README.md) | Kanban planning, JIT ticket orchestration, git repo management, and collaborative estimation — the operational backbone for ticket flow and scattering |
### Foundational plugins

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Context to memory** | [`context-to-memory/`](context-to-memory/README.md) | Convert → chunk → embed → search (local FAISS) |
| **Skill builder** | [`skill-builder/`](skill-builder/README.md) | Author practice skills, scanners, catalog, HTML manuals |
| **Skill helpers** | [`skill-helpers/`](skill-helpers/README.md) | Workspace, deploy, execute-rules, commit-msg, track-task, garden catalogue |
| **Utilities** | [`utilities/`](utilities/README.md) | Proposal respond, research assistant skills |

Stage × plugin mapping (source of truth for kanban): [`kanban/content/stages/`](kanban/content/stages/README.md).

Plugin migration notes (Cursor Marketplace / Open Plugin Spec): [`migrated-to-plugin.md`](migrated-to-plugin.md).

### Always-on instructions

After deploying, run **`/refresh_all_instructions`** to load every active rule into the agent's context so it remembers all project guidance before starting work. VSCode shouldnt need this, but eh I find this be spotty.

| Instruction | What it does |
| --- | --- |
| **execute-skill-using-skills-rules** | Read a skill's `rules/*.md` before generating output, then validate against those rules and run scanners after — every time |
| **log-and-fix-skill-errors** | When skill output is wrong or the user corrects it, log the error as a DO/DO NOT entry inside the skill's own `corrections-log.md` |
| **workspace** | Resolve the engagement workspace root from `skill-config.json` so deploy, scripts, and agents target the right project tree |
| **drawio-story-sync** | Automatically offer to re-render Draw.io story diagrams whenever `story-graph.json` changes |
| **drawio-domain-sync** | Automatically offer to re-render Draw.io domain class diagrams whenever the ubiquitous language, CRC, or object model changes |
| **sync-upstream** | When any artifact changes, offer to sync related artifacts in both directions (e.g. production code changed → offer to update tests and object model) |
---

## Agents

| Agent | Plugin | Open |
| --- | --- | --- |
| **kanban-lead** | `kanban` | [`kanban/agents/kanban-lead/AGENT.md`](kanban/agents/kanban-lead/AGENT.md) |
| **product-owner** · **product-owner-reviewer** | `kanban` | [`product-owner/AGENT.md`](kanban/agents/product-owner/AGENT.md) · [`product-owner-reviewer/AGENT.md`](kanban/agents/product-owner-reviewer/AGENT.md) |
| **business-expert** · **business-expert-reviewer** | `kanban` | [`business-expert/AGENT.md`](kanban/agents/business-expert/AGENT.md) · [`business-expert-reviewer/AGENT.md`](kanban/agents/business-expert-reviewer/AGENT.md) |
| **ux-designer** · **ux-designer-reviewer** | `kanban` | [`ux-designer/AGENT.md`](kanban/agents/ux-designer/AGENT.md) · [`ux-designer-reviewer/AGENT.md`](kanban/agents/ux-designer-reviewer/AGENT.md) |
| **engineer** · **engineer-reviewer** | `kanban` | [`engineer/AGENT.md`](kanban/agents/engineer/AGENT.md) · [`engineer-reviewer/AGENT.md`](kanban/agents/engineer-reviewer/AGENT.md) |
| **abd-context-to-memory** | `context-to-memory` | [`context-to-memory/agents/abd-context-to-memory/AGENTS.md`](context-to-memory/agents/abd-context-to-memory/AGENTS.md) |
| **abd-practice-skill-builder** | `skill-builder` | [`skill-builder/agents/abd-practice-skill-builder/AGENTS.md`](skill-builder/agents/abd-practice-skill-builder/AGENTS.md) |
| **ai-research-assistant** | `utilities` | [`utilities/agents/ai-research-assistant/AGENTS.md`](utilities/agents/ai-research-assistant/AGENTS.md) |

All skills (50+ practice packages across plugins): see **[Summary — Skills](catalog/outline.md#summary--skills)** in `catalog/outline.md`.

---

## Practice Skills

### Idea Shaping

Opportunity framing, impact mapping, cost of delay, and validated learning — before delivery work begins.

| Skill | One-liner |
| --- | --- |
| `abd-opportunity-generation` | Frame a candidate opportunity and make assumptions explicit before committing to build |
| `abd-impact-mapping` | Layered goals, actors, impacts, and deliverable options to connect outcomes to scope |
| `abd-cost-of-delay` | Estimate Cost of Delay, classify urgency, calculate CD3, and rank by economic impact |
| `abd-simple-validated-learning` | Surface assumptions as falsifiable hypotheses and work each through Plan, Validate, Learn |

### Story-Driven Delivery

Story map → acceptance criteria → specification by example → acceptance tests; plus story-graph ops and diagram sync.

| Skill | One-liner |
| --- | --- |
| `abd-story-mapping` | Patton-style story map: epics, sub-epics, stories with verb-noun naming and actors |
| `abd-story-acceptance-criteria` | WHEN/THEN/AND/BUT behavioral acceptance criteria per story using domain terms |
| `abd-story-specification` | Concrete Given/When/Then scenarios with real domain values and named outcomes |
| `abd-thin-slicing` | Vertical MVIs, spine vs optional paths, and marketable increment planning |
| `abd-story-acceptance-test` | Write executable tests first from behavioral context, then drive code to pass them |
| `story-graph-ops` | CRUD operations on story-graph.json — the serialized graph lifecycle on disk |
| `drawio-story-sync` | Render and sync story-map DrawIO diagrams from story-graph.json |
| `miro-story-sync` | Render and sync story-map Miro boards from story-graph.json |

### Domain-Driven Design

Module partition, domain terms, ubiquitous language, CRC, object model, DDD building blocks, bounded contexts, and domain diagram sync.

| Skill | One-liner |
| --- | --- |
| `abd-domain-glossary` | Partition source into modules and extract domain terms grouped by Key Abstraction — one pass |
| `abd-ubiquitous-language` | Rigorous shared vocabulary: terms, behaviors, collaborators, and invariants in one file |
| `abd-class-responsibility-collaborator` | Assign responsibilities, collaborators, and invariants for every domain concept |
| `abd-object-model` | Build a typed object model from CRC or domain knowledge before writing production code |
| `abd-scenario-walkthrough` | Walk concrete scenarios through the object model mapping steps to classes and operations |
| `abd-ddd-design-building-blocks` | Classify each concept as Entity, Value Object, Aggregate, Service, or Domain Event |
| `abd-bounded-context-map` | Map bounded contexts and their relationships for integration strategy and team collaboration |
| `abd-module-partition` | Partition source corpus into modules by allocating file references to per-module boundaries |
| `drawio-domain-sync` | Render domain model artifacts to Draw.io class diagrams and sync edits back |

### User Experience Design

Information architecture, lo-fi wireframe mockups, and production interface design — from screen inventory to accessible running code.

| Skill | One-liner |
| --- | --- |
| `abd-information-architecture` | Site map of screens, transitions, navigational components, and content model |
| `abd-ux-mockup` | Lo-fi Draw.io wireframes specifying exact controls, interactions, and states per screen |
| `abd-ux-specification` | Production-grade accessible interface code from approved hi-fi mockups |

### Architecture-Centric Engineering

Architecture outline → blueprint → template → reference → generated code; clean code, secure code, SLOs, and stack-specific skills.

| Skill | One-liner |
| --- | --- |
| `abd-architecture-outline` | First architecture artifact: platform, layers, context, topology, and principles |
| `abd-architecture-blueprint` | Second-level doc: components, mechanisms, data architecture, testing strategy, decisions |
| `abd-architecture-template` | Reference document for one mechanism: principles, patterns, participants, flow, code samples |
| `abd-architecture-reference` | Produce runnable code files implementing one architecture mechanism from a reference doc |
| `abd-build-architecture-skill` | Turn a finished architecture reference into a full practice-skill package that generates code |
| `abd-clean-code` | Production code with domain language, clean functions, explicit dependencies, observable design |
| `abd-secure-code` | OWASP-aligned secure code rules and language-specific scanners for Python, Java, JS |
| `abd-service-level-objectives` | Concrete SLI/SLO/SLA tied to functional scope with measurable targets |
| `mern-technical-architecture` | Domain-first MERN stack: shared schemas, Clean Architecture layers, story-driven testing |
| `hero-vtt-technical-architecture` | Hero VTT (WPF C#) three-layer architecture: Presentation, Domain, COH Integration |

### Delivery

Delivery planning, war room orchestration, git repo management, and collaborative estimation — the operational backbone for runs and slots.

| Skill | One-liner |
| --- | --- |
| `abd-kanban-planning` | Strategy selection, system of work, scope progression, scatter rules |
| `abd-kanban` | JIT Kanban board: tickets, scattering, per-skill tracking, board.json, metrics |
| `abd-kanban-repo` | Git history driven by ticket state changes: commit, push, branch per granularity |
| `kanban-estimation` | Collaborative estimation sessions: contributing factors, categories, and recorded rationale |

---

## Deploy to an engagement workspace

One command deploys all family plugins, standalone skills, and guidance:

```powershell
& scripts/deploy-skills.ps1 -Force
```

Deploy root resolves from `skill-config.json` → `active_skill_workspace`, or pass `-DeployRoot`:

```powershell
& scripts/deploy-skills.ps1 -Force -DeployRoot "C:\dev\abd-pet-store-demo"
```

Single family:

```bash
python scripts/deploy_family_package.py --package story-driven-delivery --to <workspace>
```

| `--ide` | Target |
| --- | --- |
| `cursor` (default) | `.cursor/` (skills, agents, rules, commands, content) |
| `vscode` | `.github/` (instructions, prompts, content) |
| `both` | both trees |

Workspace helper: [`skill-helpers/reference/workspace.md`](skill-helpers/reference/workspace.md) · scripts `skill-helpers/scripts/get_workspace.py` / `set_workspace.py`.

---

## Install individual skills (`npx skills`)

Practice skills can be installed by name from this repo (see each skill page in the catalog for the exact command):

```bash
npx skills add agilebydesign/agilebydesign-skills@abd-story-mapping -y
npx skills add agilebydesign/agilebydesign-skills -l
```

Publish skill index to agentskillhub (after pushing to GitHub):

```bash
./skills.sh
```

---

## Repository layout

```text
agilebydesign-skills/
├── kanban/                      # plugin: orchestration + stages
├── story-driven-delivery/       # plugin: SDD practice skills
├── domain-driven-design/        # plugin: DDD practice skills
├── user-experience-design/      # plugin: UX practice skills
├── architecture-centric-engineering/
├── context-to-memory/
├── idea-shaping/
├── skill-builder/
├── skill-helpers/
├── utilities/
├── catalog/                     # generated — run abd-skill-catalog to refresh
├── scripts/                     # deploy-skills.ps1, deploy_family_package.py
└── skill-config.json            # active_skill_workspace (engagement root)
```

Legacy standalone paths under repo-root `skills/` and `agents/` are junction-deployed where they still exist; **family plugins are the primary layout.**
