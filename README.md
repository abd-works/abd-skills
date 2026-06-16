# The ABD Foundry

**Version:** <!-- VERSION -->1.0.0<!-- /VERSION -->

Reusable **plugins**, **skills**, and **agents** from [abd.works](https://agilebydesign.com) — story-driven delivery, domain modeling, UX, architecture, delivery orchestration, and skill authoring.

| Browse the catalog | |
| --- | --- |
| **HTML hub** (plugins, skills, agents, delivery kanban) | [catalog/index.html](https://htmlpreview.github.io/?https://github.com/abd-works/abd-skills/blob/main/catalog/index.html) |

---

## Repository layout

Capability **plugins** live under **`practices/`** (delivery practice families), **`foundational/`** (authoring and infra), and **`utilities/`**. Each plugin bundles some of: `agents/`, `skills/`, `content/`, `instructions/`, `prompts/`, `lib/`, `scripts/`.

```text
abd-skills/
├── practices/                   # delivery practice plugins
│   ├── idea-shaping/
│   ├── story-driven-delivery/
│   ├── domain-driven-design/
│   ├── user-experience-design/
│   ├── architecture-centric-engineering/
│   └── kanban/                  # orchestration, board app, stage reference
├── foundational/
│   ├── context-to-memory/
│   ├── skill-builder/           # catalog generator, author-practice-skill, manuals
│   └── skill-helpers/           # deploy, workspace, execute-rules, commit-msg
├── utilities/                   # proposal respond, research skills
├── stages/                      # stage-tier skills
├── catalog/                     # generated HTML
├── scripts/                     # deploy-skills.ps1 / .sh, clean-skills.ps1 / .sh
└── skill-config.json            # active_skill_workspace (engagement root)
```

**Kanban stage definitions** (source of truth for the board): [`practices/kanban/reference/stages/`](practices/kanban/reference/stages/).

---

## Practice plugins

Deploy with [`scripts/deploy-skills.ps1`](scripts/deploy-skills.ps1) (Windows) or [`scripts/deploy-skills.sh`](scripts/deploy-skills.sh) (macOS/Linux).

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Idea shaping** | [`practices/idea-shaping/`](practices/idea-shaping/README.md) | Opportunity framing, cost of delay, validated learning |
| **Story-driven delivery** | [`practices/story-driven-delivery/`](practices/story-driven-delivery/README.md) | Story map → acceptance criteria → specification → acceptance tests; story-graph ops and diagram sync |
| **Domain-driven design** | [`practices/domain-driven-design/`](practices/domain-driven-design/README.md) | Domain glossary, language, model, specification, domain code; supporting DDD and diagram sync |
| **User experience design** | [`practices/user-experience-design/`](practices/user-experience-design/README.md) | Information architecture, mockups, UX specification / implementation |
| **Architecture-centric engineering** | [`practices/architecture-centric-engineering/`](practices/architecture-centric-engineering/README.md) | Architecture outline → blueprint → specification → architecture code |
| **Kanban** | [`practices/kanban/`](practices/kanban/README.md) | Kanban planning, JIT board, git repo policy, estimation, delivery agents |

### Foundational & utilities

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Context to memory** | [`foundational/context-to-memory/`](foundational/context-to-memory/README.md) | Convert → chunk → embed → search (local FAISS) |
| **Skill builder** | [`foundational/skill-builder/`](foundational/skill-builder/README.md) | Author practice skills, scanners, Foundry catalog, HTML manuals |
| **Skill helpers** | [`foundational/skill-helpers/`](foundational/skill-helpers/README.md) | Workspace, deploy rules, execute-rules, commit-msg, track-task |
| **Utilities** | [`utilities/`](utilities/README.md) | Proposal respond, research assistant skills |

---

## Delivery stages (kanban)

Five stages × four practice families (DDD · SDD · UXD · ARC). Full skill order per stage:

| Stage | Definition | Primary skills |
| --- | --- | --- |
| **Shaping** | [shaping.md](practices/kanban/reference/stages/shaping.md) | `abd-domain-glossary`, `abd-story-mapping` (outline), `abd-impact-mapping`, `abd-architecture-outline` |
| **Discovery** | [discovery.md](practices/kanban/reference/stages/discovery.md) | `abd-story-mapping` (full), `abd-domain-language`, `abd-information-architecture`, `abd-architecture-blueprint`, `abd-thin-slicing` |
| **Exploration** | [exploration.md](practices/kanban/reference/stages/exploration.md) | `abd-domain-model`, `abd-story-acceptance-criteria`, `abd-ux-mockup`, `abd-architecture-specification` (document) |
| **Specification** | [specification.md](practices/kanban/reference/stages/specification.md) | `abd-domain-specification`, `abd-story-specification`, `abd-ux-specification` (clickable prototype), `abd-architecture-specification` (template) |
| **Engineering** | [engineering.md](practices/kanban/reference/stages/engineering.md) | `abd-domain-code`, `abd-story-acceptance-test`, `abd-architecture-code` |

Stage extras (supplemental strip): `abd-clean-code`, `abd-secure-code` (engineering); discovery may add `abd-code-research`, `abd-service-level-objectives` from `stages/`.

---

## Agents

Role agents live under **`practices/kanban/agents/`** (orchestrated by **kanban-lead**):

| Agent | Plugin | Open |
| --- | --- | --- |
| **kanban-lead** | kanban | [`practices/kanban/agents/kanban-lead/AGENT.md`](practices/kanban/agents/kanban-lead/AGENT.md) |
| **product-owner** | kanban | [`practices/kanban/agents/product-owner/AGENT.md`](practices/kanban/agents/product-owner/AGENT.md) |
| **business-expert** | kanban | [`practices/kanban/agents/business-expert/AGENT.md`](practices/kanban/agents/business-expert/AGENT.md) |
| **ux-designer** | kanban | [`practices/kanban/agents/ux-designer/AGENT.md`](practices/kanban/agents/ux-designer/AGENT.md) |
| **engineer** | kanban | [`practices/kanban/agents/engineer/AGENT.md`](practices/kanban/agents/engineer/AGENT.md) |
| **abd-context-to-memory** | context-to-memory | [`foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md`](foundational/context-to-memory/agents/abd-context-to-memory/AGENTS.md) |
| **abd-practice-skill-builder** | skill-builder | [`foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md`](foundational/skill-builder/agents/abd-practice-skill-builder/AGENTS.md) |
| **ai-research-assistant** | utilities | [`utilities/agents/ai-research-assistant/AGENTS.md`](utilities/agents/ai-research-assistant/AGENTS.md) |

All skills (57+ packages in the catalog): **[skills grid](catalog/skills.html)**.

---

## Skills by practice plugin

Core skills per plugin (supporting skills in `skills/supporting/` — see [catalog/skills.html](catalog/skills.html)).

### Idea shaping — `practices/idea-shaping/`

| Skill | One-liner |
| --- | --- |
| `abd-opportunity-generation` | Frame a candidate opportunity; make assumptions explicit before build |
| `abd-cost-of-delay` | Cost of Delay, CD3 ranking, urgency × value |
| `abd-simple-validated-learning` | Falsifiable hypotheses; Plan, Validate, Learn |

Also used in shaping (stage-tier): `abd-impact-mapping` — [`stages/idea-shaping/skills/abd-impact-mapping/`](stages/idea-shaping/skills/abd-impact-mapping/SKILL.md)

### Story-driven delivery — `practices/story-driven-delivery/`

| Skill | One-liner |
| --- | --- |
| `abd-story-mapping` | Patton-style story map; outline or full mode |
| `abd-story-acceptance-criteria` | WHEN/THEN/AND/BUT acceptance criteria |
| `abd-story-specification` | Given/When/Then with real domain values |
| `abd-story-acceptance-test` | Executable acceptance tests (RED-GREEN-REFACTOR) |
| `abd-thin-slicing` | Vertical MVIs and slice ordering *(supporting)* |
| `story-graph-ops` | CRUD on `story-graph.json` *(supporting)* |
| `drawio-story-sync` | Story-map Draw.io ↔ graph *(supporting)* |
| `miro-story-sync` | Story-map Miro ↔ graph *(supporting)* |

### Domain-driven design — `practices/domain-driven-design/`

| Skill | One-liner |
| --- | --- |
| `abd-domain-glossary` | Module boundaries + domain terms (Key Abstractions) |
| `abd-domain-language` | Shared vocabulary, behaviors, invariants |
| `abd-domain-model` | Typed domain model from Domain Language |
| `abd-domain-specification` | Typed class model for implementation |
| `abd-domain-code` | Pure domain code from specification |
| `abd-bounded-context-map` | Context map and integration *(supporting)* |
| `abd-ddd-design-building-blocks` | Entity / VO / aggregate stereotypes *(supporting)* |
| `abd-domain-walk` | Scenario walkthrough against model *(supporting)* |
| `drawio-domain-sync` | Domain diagrams ↔ model *(supporting)* |

### User experience design — `practices/user-experience-design/`

| Skill | One-liner |
| --- | --- |
| `abd-information-architecture` | Site map, navigation, content model |
| `abd-ux-information-architecture` | IA variant aligned to UX plugin layout |
| `abd-ux-mockup` | Lo-fi Draw.io wireframes |
| `abd-ux-specification` | Clickable hi-fi prototype — real HTML/CSS/JS, stubbed logic |
| `abd-ux-user-impact-map` | Impact mapping from UX practice family |

### Architecture-centric engineering — `practices/architecture-centric-engineering/`

| Skill | One-liner |
| --- | --- |
| `abd-architecture-outline` | Platform, layers, context, topology |
| `abd-architecture-blueprint` | Components, mechanisms, data architecture |
| `abd-architecture-specification` | Mechanism docs (exploration) and templates (specification) |
| `abd-architecture-code` | Production code from architecture spec |

### Kanban — `practices/kanban/`

| Skill | One-liner |
| --- | --- |
| `abd-kanban-planning` | Delivery strategy, system of work, scatter rules |
| `abd-kanban` | JIT board, tickets, scattering, metrics |
| `abd-kanban-repo` | Git policy tied to ticket state |
| `abd-kanban-handoff` | Handoff documents between agents |
| `kanban-estimation` | Collaborative estimation sessions |

### Context to memory — `foundational/context-to-memory/`

`abd-convert-to-markdown` · `abd-chunk-markdown` · `abd-embed-vectors` · `abd-search-memory` · `abd-semantic-context-chunker`

### Skill builder — `foundational/skill-builder/`

`abd-author-practice-skill` · `abd-query-practice-sources` · `abd-build-practice-scanners` · `abd-skill-catalog` · `abd-practice-skill-manual`

### Skill helpers — `foundational/skill-helpers/`

`execute-skill-using-skills-rules` · `commit-msg` · `track_task`

### Utilities — `utilities/`

`abd-proposal-respond` · `research-problem-validation` · `research-solution-landscape` · `research-compare-approach`

---

## Deploy to an engagement workspace

One command deploys all family plugins, standalone skills, and guidance:

**Windows (PowerShell):**
```powershell
& scripts/deploy-skills.ps1 -Force
```

**macOS / Linux (bash):**
```bash
./scripts/deploy-skills.sh
```

Deploy root resolves from `skill-config.json` → `active_skill_workspace`, or pass a custom root:

**PowerShell:**
```powershell
& scripts/deploy-skills.ps1 -Force -DeployRoot "C:\dev\abd-pet-store-demo"
```

**Bash:**
```bash
./scripts/deploy-skills.sh cursor /path/to/project
```

| Parameter | Description |
| --- | --- |
| `ide` (bash) / `-ide` (PS) | `cursor` (default) → `.cursor/` · `vscode` → `.github/` |
| `deploy-root` / `-DeployRoot` | Override workspace root (auto-resolved when omitted) |
| `package` / `-Package` | Specific package like `practices/kanban` or `all` (default) |
| `--skip-checks` / `-SkipChecks` | Skip pre-deploy encoding and structure validation |
| `--status` / `-Status` | Check deploy status without deploying (compare manifest) |

Before deploying, the script runs encoding and structure checks, then compares the source manifest with any existing deploy receipt in the target workspace. A `.abd-deploy.json` receipt is written after each deploy, enabling delta detection on subsequent deploys.

Workspace helper: [`foundational/skill-helpers/reference/workspace.md`](foundational/skill-helpers/reference/workspace.md) · scripts `foundational/skill-helpers/scripts/get_workspace.py` / `set_workspace.py`.

### Always-on instructions (after deploy)

| Instruction | What it does |
| --- | --- |
| **execute-skill-using-skills-rules** | Read skill `rules/*.md` before generating; validate + run scanners after |
| **log-and-fix-skill-errors** | Log corrections in the target skill's `corrections-log.md` |
| **workspace** | Resolve engagement root from `skill-config.json` |
| **drawio-story-sync** | Offer to re-render story diagrams when `story-graph.json` changes |
| **drawio-domain-sync** | Offer to re-render domain diagrams when the model changes |
| **sync-upstream** | Offer artifact sync up/down the delivery stack when one layer changes |

---

## Install individual skills (`npx skills`)

```bash
npx skills add abd-works/abd-skills@abd-story-mapping -y
npx skills add abd-works/abd-skills -l
```

Each skill page in the [catalog](catalog/index.html) shows the exact install line. Publish the index to agentskillhub (after pushing to GitHub):

```bash
./skills.sh
```

---

## Encoding guard

Markdown files must be clean UTF-8. This repo includes an automated scanner that catches mojibake (double-encoded Unicode), `` U+FFFD replacement characters, and UTF-8 BOM before they ship.

### What it checks

| Issue | Example | Cause |
| --- | --- | --- |
| **Mojibake** | `â€™` instead of `'` | UTF-8 text misread as Windows-1252 or Latin-1, then re-saved |
| **U+FFFD** | `` | Bytes that couldn't decode; original character lost |
| **UTF-8 BOM** | `EF BB BF` at file start | Windows editors inserting byte-order mark |

### Run manually

```bash
# Report all issues
python3 scripts/scan_encoding.py

# Exit non-zero if any issues (for CI or hooks)
python3 scripts/scan_encoding.py --check

# Auto-fix: mojibake → correct Unicode, U+FFFD → em-dash, strip BOM
python3 scripts/scan_encoding.py --fix

# Strip BOM only
python3 scripts/scan_encoding.py --fix-bom

# Scan only staged files (used by pre-commit hook)
python3 scripts/scan_encoding.py --staged --check
```

### Pre-commit hook

Install once after cloning:

```bash
./scripts/install-hooks.sh
```

The hook runs `scan_encoding.py --check --staged` before every commit. If any staged `.md` / `.mdc` file has encoding issues, the commit is blocked.

### CI (GitHub Actions)

`.github/workflows/encoding-guard.yml` runs on every push and PR that touches `.md` / `.mdc` / `tests/` files:

1. **Encoding scan** — `python3 scripts/scan_encoding.py --check`
2. **Deploy-path & structure validation** — `python3 tests/test_deploy_paths.py`

### Validation test

`tests/test_deploy_paths.py` enforces IDE-agnostic conventions for all new content:

| Check | What it catches |
|---|---|
| **No hardcoded `.cursor/skills/`** | Prompt/instruction files with Cursor-only paths |
| **No bare `skills/` paths** | Missing `../` prefix that breaks deploy resolution |
| **No `~/../skills/` paths** | Incorrect home-relative paths |
| **No mojibake** | Double-encoded Unicode (smart quotes, em-dashes) |
| **No U+FFFD** | Irrecoverable encoding corruption |
| **No UTF-8 BOM** | Byte-order mark at file start |
| **SKILL.md frontmatter** | Missing `name` or `description` fields |
| **Agent entry files** | Agent dirs without `AGENT.md` / `AGENTS.md` |

Run locally:
```bash
python3 tests/test_deploy_paths.py
```

### Codespaces note

Skills are deployed to the target workspace by `scripts/deploy-skills.sh` (or `.ps1`). In Codespaces, run the deploy script after opening the workspace so that `.github/skills/` and `.github/prompts/` are populated for Copilot slash-command discovery.
