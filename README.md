# The ABD Foundry

**Version:** <!-- VERSION -->1.0.0<!-- /VERSION -->

Reusable **plugins**, **skills**, and **agents** from [abd.works](https://agilebydesign.com) — story-driven delivery, domain modeling, UX, architecture, delivery orchestration, context engineering, and skill authoring.

| Browse the catalog | |
| --- | --- |
| **HTML hub** (plugins, skills, agents, delivery kanban) | [catalog/index.html](https://htmlpreview.github.io/?https://github.com/abd-works/abd-skills/blob/main/catalog/index.html) |

---

## Repository layout

```text
abd-skills/
├── practices/                         # delivery practice plugins
│   ├── context-driven-delivery/       # context stage: ingest, convert, chunk, embed, search
│   ├── idea-shaping/
│   ├── story-driven-delivery/
│   ├── domain-driven-design/
│   ├── user-experience-design/
│   ├── architecture-centric-engineering/
│   ├── behavior-driven-development/
│   └── kanban/                        # orchestration, board app, stage reference
├── other/
│   └── skills/
│       ├── skill-builder/             # catalog generator, author-practice-skill, scanners
│       ├── ai-research-assistant/     # hypothesis-driven research orchestrator
│       ├── research-problem-validation/
│       ├── research-solution-landscape/
│       ├── research-compare-approach/
│       ├── abd-proposal-respond/
│       ├── abd-mojibake-guard/
│       └── track_task/
├── common/                            # reference/, instructions, templates, scripts, scaffolds
├── utilities/                         # shared utility scripts
├── stages/                            # stage-tier supplemental skills
├── catalog/                           # generated HTML
└── scripts/                           # deploy-skills.ps1/.sh, clean-skills.ps1/.sh
```

**Stage definitions** (source of truth for all practice skills): [`common/reference/stages/`](./common/reference/stages/).

---

## Practice plugins

Deploy with [`common/scripts/deploy-skills.ps1`](common/scripts/deploy-skills.ps1) (Windows) or [`common/scripts/deploy-skills.sh`](common/scripts/deploy-skills.sh) (macOS/Linux).

| Plugin | Folder | Summary |
| --- | --- | --- |
| **Context-driven delivery** | [`practices/context-driven-delivery/`](practices/context-driven-delivery/) | Context stage: convert → chunk → embed → search; app extraction and sandbox; orchestrator skill |
| **Idea shaping** | [`practices/idea-shaping/`](practices/idea-shaping/README.md) | Opportunity framing, cost of delay, validated learning |
| **Story-driven delivery** | [`practices/story-driven-delivery/`](practices/story-driven-delivery/README.md) | Story map → acceptance criteria → specification → acceptance tests; story-graph ops and diagram sync |
| **Domain-driven design** | [`practices/domain-driven-design/`](practices/domain-driven-design/README.md) | Domain glossary, language, model, specification, domain code; DDD building blocks and diagram sync |
| **User experience design** | [`practices/user-experience-design/`](practices/user-experience-design/README.md) | Information architecture, mockups, UX specification / implementation |
| **Architecture-centric engineering** | [`practices/architecture-centric-engineering/`](practices/architecture-centric-engineering/README.md) | Architecture outline → blueprint → specification → architecture code |
| **Behavior-driven development** | [`practices/behavior-driven-development/`](practices/behavior-driven-development/) | BDD behavior authoring, specification, and development cycle |
| **Kanban** | [`practices/kanban/`](practices/kanban/README.md) | Kanban planning, JIT board, git repo policy, estimation, delivery agents |

### Other skills

| Skill / Package | Folder | Summary |
| --- | --- | --- |
| **Skill builder** | [`other/skills/skill-builder/`](other/skills/skill-builder/README.md) | Author practice skills, scanners, Foundry catalog, HTML manuals |
| **AI research assistant** | [`other/skills/ai-research-assistant/`](other/skills/ai-research-assistant/SKILL.md) | Hypothesis-driven research: problem validation → solution landscape → approach comparison |
| **Research sub-skills** | [`other/skills/`](other/skills/) | `research-problem-validation` · `research-solution-landscape` · `research-compare-approach` |
| **Proposal respond** | [`other/skills/abd-proposal-respond/`](other/skills/abd-proposal-respond/) | Strategy + answer workflow for client RFPs |
| **Track task** | [`other/skills/track_task/`](other/skills/track_task/SKILL.md) | Create and track checkbox task lists for any multi-step work |
| **Mojibake guard** | [`other/skills/abd-mojibake-guard/`](other/skills/abd-mojibake-guard/) | Detect and fix double-encoded Unicode in markdown files |

---

## Delivery stages

Six stages × four practice families (DDD · SDD · UXD · ARC). Full skill order per stage:

| Stage | Definition | Primary skills |
| --- | --- | --- |
| **Context** | [context.md](./stages/context.md) | `abd-context-to-markdown`, `abd-context-chunk`, `abd-context-db-embed`, `abd-context-db-ask`, `abd-context-semantic-index`, `abd-context-app-extractor`, `abd-context-app-sandbox` |
| **Shaping** | [shaping.md](./stages/shaping.md) | `abd-domain-glossary`, `abd-story-mapping` (outline), `abd-impact-mapping`, `abd-architecture-outline` |
| **Discovery** | [discovery.md](./stages/discovery.md) | `abd-story-mapping` (full), `abd-domain-language`, `abd-information-architecture`, `abd-architecture-blueprint`, `abd-thin-slicing` |
| **Exploration** | [exploration.md](./stages/exploration.md) | `abd-domain-model`, `abd-story-acceptance-criteria`, `abd-ux-mockup`, `abd-architecture-specification` (document) |
| **Specification** | [specification.md](./stages/specification.md) | `abd-domain-specification`, `abd-story-specification`, `abd-ux-specification` (clickable prototype), `abd-architecture-specification` (template) |
| **Engineering** | [engineering.md](./stages/engineering.md) | `abd-domain-code`, `abd-story-acceptance-test`, `abd-architecture-code` |

Stage extras (supplemental strip): `abd-clean-code`, `abd-secure-code` (engineering); discovery may add `abd-code-research`, `abd-service-level-objectives` from `stages/`.

---

## Agents

| Agent | Plugin | File |
| --- | --- | --- |
| **kanban-lead** | kanban | [`practices/kanban/agents/kanban-lead.md`](practices/kanban/agents/kanban-lead.md) |
| **abd-context-to-memory** | context-driven-delivery | [`practices/context-driven-delivery/agents/abd-context-to-memory.md`](practices/context-driven-delivery/agents/abd-context-to-memory.md) |
| **business-expert** | context-driven-delivery | [`practices/context-driven-delivery/agents/business-expert.md`](practices/context-driven-delivery/agents/business-expert.md) |
| **product-owner** | context-driven-delivery | [`practices/context-driven-delivery/agents/product-owner.md`](practices/context-driven-delivery/agents/product-owner.md) |
| **ux-designer** | context-driven-delivery | [`practices/context-driven-delivery/agents/ux-designer.md`](practices/context-driven-delivery/agents/ux-designer.md) |
| **engineer** | context-driven-delivery | [`practices/context-driven-delivery/agents/engineer.md`](practices/context-driven-delivery/agents/engineer.md) |
| **abd-practice-skill-builder** | skill-builder | [`other/skills/skill-builder/scripts/abd-practice-skill-builder/AGENTS.md`](other/skills/skill-builder/scripts/abd-practice-skill-builder/AGENTS.md) |

---

## Skills by practice plugin

### Context-driven delivery — `practices/context-driven-delivery/`

| Skill | One-liner |
| --- | --- |
| `abd-context-driven-delivery` | Orchestrator — choose context stage, tools, and pipeline |
| `abd-context-to-markdown` | Convert documents (PDF, PPTX, DOCX) to clean markdown |
| `abd-context-chunk` | Split markdown into semantically coherent chunks |
| `abd-context-db-embed` | Embed chunks into a local FAISS vector store |
| `abd-context-db-ask` | Semantic search against the embedded store |
| `abd-context-semantic-index` | Semantic section chunker for long structured docs |
| `abd-context-app-extractor` | Extract context from a running application |
| `abd-context-app-sandbox` | Stub external dependencies and stand up an isolated app |

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
| `abd-domain-specification` | Typed domain specification for implementation |
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

### Behavior-driven development — `practices/behavior-driven-development/`

| Skill | One-liner |
| --- | --- |
| `abd-bdd-behavior` | Author BDD behaviors from acceptance criteria |
| `abd-bdd-specification` | Gherkin feature files with concrete examples |
| `abd-bdd-development` | Implement step definitions (RED-GREEN-REFACTOR) |

### Kanban — `practices/kanban/`

| Skill | One-liner |
| --- | --- |
| `abd-kanban-planning` | Delivery strategy, system of work, scatter rules |
| `abd-kanban` | JIT board, tickets, scattering, metrics |
| `abd-kanban-repo` | Git policy tied to ticket state |
| `abd-kanban-handoff` | Handoff documents between agents |
| `kanban-estimation` | Collaborative estimation sessions |

### Skill builder — `other/skills/skill-builder/`

`abd-author-practice-skill` · `abd-build-practice-scanners` · `abd-skill-catalog`

---

## Deploy to an engagement workspace

One command deploys all family plugins, standalone skills, and guidance:

**Windows (PowerShell):**
```powershell
& common/scripts/deploy-skills.ps1 -Force
```

**macOS / Linux (bash):**
```bash
./common/scripts/deploy-skills.sh
```

Deploy root resolves from `skill-config.json` → `active_skill_workspace`, or pass a custom root:

**PowerShell:**
```powershell
& common/scripts/deploy-skills.ps1 -Force -DeployRoot "C:\dev\my-project"
```

**Bash:**
```bash
./common/scripts/deploy-skills.sh cursor /path/to/project
```

| Parameter | Description |
| --- | --- |
| `ide` (bash) / `-ide` (PS) | `cursor` (default) → `.cursor/` · `vscode` → `.github/` |
| `deploy-root` / `-DeployRoot` | Override workspace root (auto-resolved when omitted) |
| `package` / `-Package` | Specific package like `practices/kanban` or `all` (default) |
| `--skip-checks` / `-SkipChecks` | Skip pre-deploy encoding and structure validation |
| `--status` / `-Status` | Check deploy status without deploying (compare manifest) |

Before deploying, the script runs encoding and structure checks, then compares the source manifest with any existing deploy receipt in the target workspace. A `.abd-deploy.json` receipt is written after each deploy, enabling delta detection on subsequent deploys.

### Always-on instructions (after deploy)

| Instruction | What it does |
| --- | --- |
| **skill-workflow** | Output path resolution, read-gates, validation, diagram delegation, correction loop |
| **log-and-fix-skill-errors** | Log corrections in the target skill's `corrections-log.md` |
| **drawio-story-sync** | Offer to re-render story diagrams when `story-graph.json` changes |
| **drawio-domain-sync** | Offer to re-render domain diagrams when the model changes |
| **sync-upstream** | Offer artifact sync up/down the delivery stack when one layer changes |

---

## Install individual skills (`npx skills`)

```bash
npx skills add abd-works/abd-skills@abd-story-mapping -y
npx skills add abd-works/abd-skills -l
```

Each skill page in the [catalog](catalog/index.html) shows the exact install line.

---

## Encoding guard

Markdown files must be clean UTF-8. This repo includes an automated scanner that catches mojibake (double-encoded Unicode), `U+FFFD` replacement characters, and UTF-8 BOM before they ship.

### What it checks

| Issue | Example | Cause |
| --- | --- | --- |
| **Mojibake** | `â€™` instead of `'` | UTF-8 text misread as Windows-1252 or Latin-1, then re-saved |
| **U+FFFD** | `<?>` | Bytes that couldn't decode; original character lost |
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
