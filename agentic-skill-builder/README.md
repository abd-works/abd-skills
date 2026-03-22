# Agentic skill builder

Sub-project under **`agilebydesign-skills/agentic-skill-builder/`** for **agentic orchestration** of skill authoring: **building [skills.sh](https://skills.sh)-style Open Agent Skills** (same packaging family as the rest of the monorepo), operating them as structural tests, critiquing outputs with domain expertise, and (optionally) deploying to git with versioning.

This is **not** a Cursor “skill” package. It is a normal Python project (library + CLI + docs).

*(This folder was previously scaffolded as `skills-delivery`; all project files now live here.)*

## Layout

| Path | Purpose |
| ---- | ------- |
| `src/agentic_skill_builder/` | Application code (LangGraph graphs, agents, CLIs) |
| `docs/` | Plans, architecture, runbooks |
| `scripts/` | **`notify_slack.py`** — optional HITL / completion ping (when webhook exists); **`diagnose_connectivity.py`** — OpenAI + optional Slack checks |
| `.cursor/rules/` | e.g. **`slack-notify-after-work.mdc`** — optional **`notify_slack.py`** when Slack is enabled (see plan **Execution status — Slack**) |
| `conf/` | Example configs; **secrets** in gitignored **`conf/.secrets`** — see **`conf/.secrets.example`** and `conf/README.md` |
| `test/` | Pytest tests |
| `log/` | Runtime logs (gitignored contents; folder may exist) |
| `requirements/` | Pinned dependency sets for this project only |

Python dependencies are managed with **`pyproject.toml`** + **`uv`/`pip`**; use a **local virtual environment** (`.venv/`) — see `docs/development/python-environment.md`.

## First read

- **`docs/plans/langgraph-agentic-orchestration-plan.md`** — master plan for LangGraph-based builder / operator / critic / deployer and human-in-the-loop gates. **Rollout:** validate on a **trivial reference skill** (four-stage polite dialogue) **before** `abd-maps-models-specs`-shaped templates — see **§7–§8**. **Process:** **§1.2** — step-by-step **human gates**; **§1.3** — first builds **especially** need review (standards + critique calibration); **stop after first test and first critique**; feedback includes **orchestration** of agents/subgraphs; after several manual runs, capture **dimensions of improvement** not only point fixes; **autopilot only after** scaffold + rubric trust.
- **See also — standalone standards + scaffold:** **`../skills/abd-skill-builder/`** — condensed layout rules, builder vs operator notes, **`scripts/scaffold_skill.py`** + templates for new skills, **`scripts/build.py`** for AGENTS assembly. Use when you need a compliant skill tree without running the LangGraph CLI.
- **Slack (deferred):** **Incoming Webhook** and **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`** are **optional** until api.slack.com access exists — see plan **Execution status — Slack** and **§5.4**. HITL uses **interrupts + IDE/CLI** without Slack.

### Connectivity check (OpenAI + optional Slack)

After **`OPENAI_API_KEY`** is set in **`conf/.secrets`** (or the environment), run (Slack lines **SKIP** if **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`** is unset):

```bash
python scripts/diagnose_connectivity.py
```

The script calls **`GET https://api.openai.com/v1/models`** and, if **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`** is set, **`POST`**s a short test message to the Slack Incoming Webhook. Skipped checks (missing variable) are reported as **SKIP** and do not fail the run; failed HTTP or network errors exit **1**.

### Slack completion ping (optional — when webhook exists)

```bash
python scripts/notify_slack.py "What changed — reply **keep going** in Cursor when ready."
```

Omit the argument for a default message. Implementation: **`src/agentic_skill_builder/slack_notify.py`** (`notify_slack`) — reuse from LangGraph nodes instead of duplicating HTTP.

Set **`AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID`** in **`conf/.secrets`** to Jeff’s Slack member ID (`U…`) so every message **@mentions** `@jeff.anderson` (Slack requires the ID, not the handle — see **`conf/README.md`**).

## Status

**§7.1 toy skill:** canonical copy under **`../skills/abd-skill-builder/test/fixture/toy-polite-dialogue/`** (repo root: `skills/abd-skill-builder/...`) — minimal phases (greet → introduce → converse → close), **`scripts/build.py`**, **`skill-config.json`** `operator` block (compileall paths, build script, scanners), **`rules/*.md`** (example rules with YAML frontmatter), **`rules/scanners.json`** with **`rule_scanner_bindings`** plus **`scanners`** (merged and deduped in **`operator._merge_scanner_paths`**; bindings are verified before scanners run). Owned by **`abd-skill-builder`** so this package does not ship a duplicate fixture.

**Strategizer:** After ingest, the graph runs **`strategize`** — it loads human-authored **build intent** from **`--strategy-file PATH`** or **`<skill-path>/conf/build-strategy.json`**. If neither exists, the trace lists the questionnaire fields (copy **`docs/templates/build-strategy.example.json`**).

- **`strategy_complete`** is **`true`** when **`skill_purpose`** is non-empty — in practice, filling **`skill_purpose`** is the **minimum** to mark the strategize step as complete in the delivery graph.
- The same JSON holds **other build-intent fields** (e.g. `target_audience`, `scope_in` / `scope_out`, `pipeline_phases`, …). They are **separate keys** in the file — **not** part of the **`skill_purpose`** string — and they **enrich** the **`strategy`** object that the stub **builder** passes into **`builder_manifest`** for downstream tooling.
- When someone says **“skill_purpose and related build-intent fields for strategize / delivery graph”**, they mean **this whole JSON** the strategize node loads, with **`skill_purpose`** as the **required headline** field — not that the other fields are *contained in* or *appended to* **`skill_purpose`**.

**Greenfield skills (human + AI):** Use **`../skills/abd-skill-builder/content/parts/library/authoring-checklist.md`** — copy to **`<your-skill>/docs/authoring-checklist.md`** (or your workspace) when tracking work; ask / AI-suggest / track checkboxes for rules & scanners, library parts, cross-cutting concepts, **`delivery.mode`**, and operator sign-off.

**Operator / Expert:** **`operator.run_operator()`** runs `compileall`, `python scripts/build.py`, then declared scanner scripts. **`expert.run_expert()`** calls OpenAI with **`conf/expert_rubric.yaml`** (skipped or API-safe fallback if no key / auth failure).

**CLI:** `run` (default when flags are used without a subcommand) and **`resume`** for **`interrupt_before`** + SQLite — same **`--thread-id`** and **`--interrupt-before`** list as the paused run. Example:

```bash
# From repo root (agilebydesign-skills): use path to abd-skill-builder fixture.
agentic-skill-builder run --skill-id demo --skill-path ../skills/abd-skill-builder/test/fixture/toy-polite-dialogue --json
agentic-skill-builder run --skill-path ../skills/abd-skill-builder/test/fixture/toy-polite-dialogue --sqlite log/cp.sqlite --interrupt-before ingest_request
agentic-skill-builder resume --sqlite log/cp.sqlite --thread-id cli-main --interrupt-before ingest_request
```
