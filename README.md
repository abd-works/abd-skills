# abd.works AI Garden

Reusable **plugins**, **skills**, and **agents** from [abd.works](https://agilebydesign.com) — story-driven delivery, domain modeling, UX, architecture, delivery orchestration, and skill authoring.

**Do not hand-maintain skill or agent lists in this file.** The full inventory is generated under [`catalog/`](catalog/index.html) from repo packages. Regenerate after adding or renaming packages:

```bash
python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py
```

| Browse | Location |
| --- | --- |
| **HTML hub** (plugins, skills, agents, kanban) | [`catalog/index.html`](catalog/index.html) |
| **Markdown outline** (same content, diffable) | [`catalog/outline.md`](catalog/outline.md) |
| **Plugins grid** | [`catalog/plugins.html`](catalog/plugins.html) |
| **Skills grid** | [`catalog/skills.html`](catalog/skills.html) |
| **Agents grid** | [`catalog/agents.html`](catalog/agents.html) |
| **Delivery kanban** (stages × practice plugins) | [`catalog/kanban-layout/index.html`](catalog/kanban-layout/index.html) |

Optional: scaffold missing package READMEs before generate:

```bash
python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py --scaffold-readmes
```

### Bootcamp and gardener training (same approach — do not duplicate by hand)

The catalog is **not** copied wholesale into the bootcamp repo. **`generate_abd_catalog.py` is the single refresh** for catalog HTML and for bootcamp sync:

| What | Where it lives | On `generate_abd_catalog.py` |
| --- | --- | --- |
| Full AI Garden (hub, grids, detail pages) | `catalog/` in this repo | **Regenerated** (overwrite) |
| Delivery kanban deck | `catalog/kanban-layout/index.html` | **Regenerated** |
| Part 3 delivery kanban | `abd-works/abd-ai-augmented-bootcamp/slides/part3/part3.html` | **Synced** — kb-slides copied from `catalog/kanban-layout` on generate (offline Reveal; no iframe) |
| Skill / plugin / agent **links** on other bootcamp slides | Files under `abd-ai-augmented-bootcamp/slides/` (not part3 kanban) | **Patched** — relative links to `../../../../agilebydesign-skills/catalog/...` |
| Agile Garden prelude excerpt | `abd-works/abd-ai-gardener-training/context/fragments/agile-garden-catalog-prelude.html` | **Written** (auto-generated fragment) |

**One kanban source, two outputs:** `generate_abd_catalog.py` builds `catalog/kanban-layout/index.html`, then copies the same kb-slide stack into bootcamp `part3.html` (between `<!-- KANBAN_SLIDES -->` markers) so the deck works offline via `file://`.

After catalog generate, embed the prelude into the public gardener lesson (abd-works repo):

```bash
python abd-works/scripts/sync-agile-garden-into-lesson.py
```

Requires sibling checkout: `agilebydesign-skills` and `abd-works` under the same parent (e.g. `c:\dev\`).

---

## Plugins

Repo-root capability **plugins** deploy with `deploy_family_package.py` or the full deploy script. Each plugin bundles some of: `agents/`, `skills/`, `content/`, `instructions/`, `prompts/`, `lib/`, `scripts/`.

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Delivery** | [`delivery/`](delivery/README.md) | Delivery lead, team member, reviewer; shared stages and roles; planning, war room, estimation |
| **Story-driven delivery** | [`story-driven-delivery/`](story-driven-delivery/README.md) | Story map → AC → spec-by-example → ATDD; story-graph-ops; Draw.io / Miro sync |
| **Domain-driven design** | [`domain-driven-design/`](domain-driven-design/README.md) | Module partition, domain terms, UL, CRC, object model, DDD building blocks, bounded contexts |
| **User experience design** | [`user-experience-design/`](user-experience-design/README.md) | Information architecture, lo-fi mockups, interface design |
| **Architecture-centric engineering** | [`architecture-centric-engineering/`](architecture-centric-engineering/README.md) | Architecture outline → blueprint → template → reference; clean code; SLOs; stack skills |
| **Context to memory** | [`context-to-memory/`](context-to-memory/README.md) | Convert → chunk → embed → search (local FAISS) |
| **Idea shaping** | [`idea-shaping/`](idea-shaping/README.md) | Opportunity framing, impact mapping, cost of delay, validated learning |
| **Skill builder** | [`skill-builder/`](skill-builder/README.md) | Author practice skills, scanners, catalog, HTML manuals |
| **Skill helpers** | [`skill-helpers/`](skill-helpers/README.md) | Workspace, deploy, execute-rules, commit-msg, track-task, garden catalogue |
| **Utilities** | [`utilities/`](utilities/README.md) | Proposal respond, research assistant skills |

Stage × plugin mapping (source of truth for delivery): [`delivery/content/stages/`](delivery/content/stages/README.md).

Plugin migration notes (Cursor Marketplace / Open Plugin Spec): [`migrated-to-plugin.md`](migrated-to-plugin.md).

---

## Agents

| Agent | Plugin | Open |
| --- | --- | --- |
| **delivery-lead** | `delivery` | [`delivery/agents/delivery-lead/AGENT.md`](delivery/agents/delivery-lead/AGENT.md) |
| **delivery-team-member** | `delivery` | [`delivery/agents/delivery-team-member/AGENT.md`](delivery/agents/delivery-team-member/AGENT.md) |
| **delivery-team-reviewer** | `delivery` | [`delivery/agents/delivery-team-reviewer/AGENT.md`](delivery/agents/delivery-team-reviewer/AGENT.md) |
| **abd-context-to-memory** | `context-to-memory` | [`context-to-memory/agents/abd-context-to-memory/AGENTS.md`](context-to-memory/agents/abd-context-to-memory/AGENTS.md) |
| **abd-practice-skill-builder** | `skill-builder` | [`skill-builder/agents/abd-practice-skill-builder/AGENTS.md`](skill-builder/agents/abd-practice-skill-builder/AGENTS.md) |
| **ai-research-assistant** | `utilities` | [`utilities/agents/ai-research-assistant/AGENTS.md`](utilities/agents/ai-research-assistant/AGENTS.md) |

All skills (50+ practice packages across plugins): see **[Summary — Skills](catalog/outline.md#summary--skills)** in `catalog/outline.md`.

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

Workspace helper: [`skill-helpers/content/workspace.md`](skill-helpers/content/workspace.md) · scripts `skill-helpers/scripts/get_workspace.py` / `set_workspace.py`.

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
├── delivery/                    # plugin: orchestration + stages
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
