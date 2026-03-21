# LangGraph agentic orchestration — agentic-skill-builder plan

**Status:** planning document (implementation lives in `agentic-skill-builder/src/` when built).  
**Audience:** you (product/architecture) + implementers.  
**Not normative for:** `abd-maps-models-specs` — treat that skill’s `plan/` and `scripts/orchestrator_loop.py` as **prior experiments**, not requirements.

---

## 1. Purpose

Deliver a **repeatable pipeline** that:

1. **Builds** new or updated skills **to the same structural and authoring standards** as existing skills in `agilebydesign-skills/skills/*` (reverse-engineered into explicit rules).
2. **Operates** those skills as **structural tests** (syntax, runnable scripts, file layout, rule presence) — **not** outcome quality.
3. **Critiques** artifacts with **domain expertise** (principles, form, fitness to story) using **your** bodies of knowledge + **idealized references / rubrics**.
4. **Deploys** (optional) via git: branches, tags, parallel experiments, rollback story.

Orchestration is implemented with **LangGraph** (LangChain ecosystem) so we get **state**, **checkpoints**, **human-in-the-loop**, and **conditional routing** without ad-hoc shell loops.

---

## 2. External best practices (LangGraph / agentic orchestration)

These are the patterns we intend to follow; pin library versions when coding starts.

| Practice | Why it matters here |
| -------- | ------------------ |
| **Explicit graph state (TypedDict or Pydantic)** | Carries skill target path, build artifacts, operator logs, critic scores, deploy metadata, and **HITL** flags in one reducible structure. |
| **Checkpointers (e.g. Sqlite / Postgres / memory)** | Long runs (multi-phase skill build) can resume; supports review gates. |
| **`interrupt_before` / `interrupt_after` on nodes** | Human approval between “builder produced tree” and “operator runs”, or after critic before deploy. |
| **Reducer fields for append-only logs** | Operator and critic append messages without race issues in concurrent subgraphs (if added later). |
| **Subgraphs** | Optional: isolate “deployer” so it can be skipped in dry-run mode. |
| **Supervisor / router pattern** | A thin **orchestrator** node decides next step from state (re-plan, rebuild, re-run tests, request expert pass, abort). |
| **Tool boundaries** | Builder/operator call **filesystem + subprocess + JSON validators** as tools; LLM nodes only where judgment is required. |
| **Separation of “verifier” vs “judge”** | Structural checks = deterministic or lint-like; **expert critique** = LLM + rubric + retrieved corpora — mirrors your **Operator ≠ Expert** distinction. |

**References (official / ecosystem):** LangGraph “Persistence”, “Human-in-the-loop”, “Subgraphs”, “StateGraph”; LangChain “structured output” for critic JSON when needed.

---

## 3. Reverse-engineered skill standards (what the Builder must know)

The following is distilled from recurring patterns across `abd-context-to-memory`, `abd-solution-modeler`, `abd-story-synthesizer`, `abd-maps-models-specs`, `agile-skill-build`, etc. The **Builder** must encode these as **machine-checkable rules** + **scaffolding templates**, not tribal knowledge.

### 3.1 Directory and content conventions

| Area | Convention | Notes |
| ---- | ---------- | ----- |
| **Normative content** | Under `content/parts/` (or skill-specific `parts/` parallel to `content/`) | Plans, operations, domain narrative — **not** dumped only in chat. |
| **Step markdown** | `parts/steps/` (or `content/parts/steps/`) | Even when execution is code-first, **steps exist as markdown** for traceability and agent consumption. |
| **Atomic rules** | `parts/rules/*.md` (or top-level `rules/` in simpler skills) | One concern per file where possible; **names** should encode **step** and/or **domain concept** + rule name (see §3.2). |
| **Roles** | `roles/*-role.md` | One file per **user/agent role** the skill assumes. |
| **Process** | `parts/process.md` or staged process docs | Often a **summary table** linking **stages → phases → files**. |
| **Built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md` | Frequently produced by **`scripts/build.py`** delegating to shared **ace-shaping** / **engine** (`build_skill(skill_dir, ...)`) or skill-local merge order. |
| **Config** | `skill-config.json` | Name, version, paths — skill-specific knobs. |
| **Scripts** | `scripts/` | Operational entry points; may share `_config.py` patterns. |

### 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{step-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). The Builder should **propose** names from the step + concept + verb, then **check uniqueness** under `parts/rules/`.

### 3.3 Assembly model (static vs dynamic)

| Mode | Mechanism | When |
| ---- | --------- | ----- |
| **Static** | `build.py` merges **built-phases** pieces into `AGENTS.md` / `SKILL.md` | Release, reproducible snapshot. |
| **Dynamic** | Runtime concatenation by **phase** / **operation** from `skill-config` + manifest | Interactive agent sessions, partial rebuild. |

The Builder outputs a **manifest** (JSON or YAML) listing which fragments form which artifact for both modes.

### 3.4 “Standards corpus” for the Builder

Implementation should maintain **`docs/reference/skill-repo-profile.md`** (future) generated from:

- `skills/agile-skill-build` (scaffold + merge order),
- `skills/abd-context-to-memory` (RAG + long `AGENTS.md`),
- `skills/abd-story-synthesizer` / `abd-solution-modeler` (phased pipelines),
- `skills/abd-maps-models-specs` (rules + scanners + orchestration experiment).

This file becomes the **non-LLM** ground truth for Operator checks.

---

## 4. Agents: responsibilities, inputs, outputs

### 4.1 Builder

| Field | Content |
| ----- | ------- |
| **Goal** | Emit a **skill directory tree** + **manifest** that conforms to §3. |
| **Inputs** | Skill name, domain brief, chosen template (maps-model vs memory vs synthesizer-shaped), optional existing repo path to extend. |
| **Outputs** | File tree; `skill-config.json`; rule stubs; `parts/steps/*.md`; `roles/*.md`; runnable `build.py`; optional scanner stubs. |
| **Does not** | Prove semantic correctness of domain content; does not guarantee “good OO” or “good stories”. |

**Constraints:** Must follow **rule naming**, **folder placement**, and **assembly contract**. Should call **scaffold** patterns from `agile-skill-build` where applicable instead of inventing layout.

### 4.2 Operator (tester / runner)

| Field | Content |
| ----- | ------- |
| **Goal** | Answer: **Did we build a skill that runs and complies with repo standards?** |
| **Checks** | `python -m compileall` or equivalent; `build.py` dry-run; required globs present; JSON schema for `skill-config.json`; optional markdown frontmatter; run **existing scanners** if the skill has them; **no** evaluation of business outcomes. |
| **Outputs** | Structured report: pass/fail per check, logs, artifact hashes. |

**Constraints:** Treat **Builder rules** as ORDERS; treat **skill domain** as opaque except where the skill exposes **machine-readable** tests.

### 4.3 Expert critique (domain)

| Field | Content |
| ----- | ------- |
| **Goal** | Answer three orchestration questions (see §6) from a **principal’s** perspective: principles, form, outcome fitness. |
| **Inputs (two mandatory)** | (1) **Body of knowledge** — curated corpus pointers (paths, skills, `abd_content`, `agile_bots/bots` rules). (2) **Idealized reference** — rubric paragraph, gold example artifact, or `docs/reference/*` style exemplar. |
| **Outputs** | Scored dimensions + actionable edits + **citations** into the corpus where possible. |

**Constraints:** May use LLM + retrieval; **must not** leak “private gap analysis” into Builder prompts if we follow the mm3 orchestrator lesson — keep **public** vs **private** separation if critique includes competitive or client-sensitive notes.

### 4.4 Deployer

| Field | Content |
| ----- | ------- |
| **Goal** | Git lifecycle: branch naming, tags, parallel experiment branches, merge, rollback procedures. |
| **Inputs** | Operator pass + optional human approval + version bump policy. |
| **Outputs** | Commit metadata, tag, changelog snippet. |

**Constraints:** No deploy without **explicit gate** in graph (HITL or CI policy).

---

## 5. LangGraph shape (implementation sketch)

### 5.1 State (conceptual)

```text
SkillDeliveryState:
  skill_id, skill_path
  builder_manifest: dict | None
  operator_report: dict | None
  expert_report: dict | None
  deploy_result: dict | None
  iteration: int
  gates: { builder_review: bool, expert_review: bool, deploy: bool }
  trace: list[str]   # append-only
```

### 5.2 Nodes (first cut)

1. **`ingest_request`** — Normalize inputs; resolve corpus paths; fail fast if required HITL inputs missing (§7).
2. **`builder`** — Template expansion + file writes + manifest.
3. **`operator`** — Structural validation suite.
4. **`route_after_operator`** — If fail → loop to `builder` with diff **or** stop; if pass → `expert_critique` **or** skip if configured.
5. **`expert_critique`** — Retrieval-augmented LLM or script-assisted review using §4.3 inputs.
6. **`orchestrator_decide`** — Supervisor: continue, iterate, or request human (interrupt).
7. **`deployer`** — Git operations (optional subgraph).

**Graph-level:** `MemorySaver` or equivalent checkpoint; `interrupt_before` on `deployer` and optionally after `builder`.

### 5.3 Mapping from abd-maps-models-specs experiment

That repo’s `docs/orchestrator.md` describes **Planner / Runner / Critic** with **public vs private** critic fields. We adopt:

- **Public / private split** for critique payloads.
- **Iteration cap** and **stop-on-score** analogs for Expert dimensions (not only numeric — could be rubric thresholds).

We do **not** assume the same scripts — **agentic-skill-builder** generalizes across skills.

---

## 6. Orchestrator validation angles (your three lenses)

Order can change; all three should appear in **`expert_critique`** configuration.

| Lens | Question | Typical signals |
| ---- | -------- | --------------- |
| **A — Principles** | Are relationships and responsibilities sane (no inheritance explosion, no nonsense associations)? | OO smoke tests, CRC alignment, DDD-lite heuristics **from your materials**, not generic textbook boilerplate. |
| **B — Form** | Is textual / structural representation well-formed (Given/When/Then, headings, rule structure, JSON shapes)? | Lint, schema validation, narrative patterns from `agile_bots` story rules. |
| **C — Outcome** | Would this artifact plausibly **realize** the story for a downstream “solution + architecture” pass? | Trace from story map to concepts; scenario coverage; gap list vs idealized exemplar. |

**Operator** covers a **subset** of B (machine checks). **A and C** are primarily Expert (with optional deterministic helpers).

---

## 7. Human-in-the-loop — what I need from you before implementation is “done”

These are **decision points**, not blockers for drafting code skeletons.

1. **Corpus roots for Expert**  
   - Confirm priority order among: `agilebydesign-skills/skills/*`, `skills/abd-maps-models-specs-old`, `C:\dev\abd_content` (after workspace repair), `agile_bots/bots` rules.  
   - Any **excluded** paths (privacy, size).

2. **Idealized references per skill family**  
   - For **maps / models / specs**: is `docs/reference/mm3-map-model-solution-reference.md`-style gold the right **shape** of ideal, or do you want **lighter** exemplars first?

3. **Expert model policy**  
   - Single model vs **small model** for routing + **large model** for critique; **local vs API** — affects cost and where checkpoints matter.

4. **Deployer authority**  
   - May this graph **push** to `origin`, or only **prepare** commits locally / open PRs?

5. **Parallelism**  
   - Do you want **best-of-N** skill trees (multiple builder attempts) before Operator, or serial only?

6. **Naming**  
   - Confirm **`agentic-skill-builder`** as the canonical repo folder (vs display name “Skills Delivery”) — tooling prefers no spaces.

---

## 8. Phased implementation roadmap

| Phase | Deliverable |
| ----- | ----------- |
| **P0** | This plan + repo scaffold (done). |
| **P1** | `SkillDeliveryState` + no-op graph + CLI entrypoint; Operator-only checks on an **existing** skill path. |
| **P2** | Builder templates for **one** skill family (recommend starting from `agile-skill-build` scaffold + `abd-maps-models-specs` rule layout). |
| **P3** | Expert critique node with **retrieval** from approved corpora + rubric YAML. |
| **P4** | Deployer subgraph + HITL gates + checkpointed runs. |
| **P5** | Parallel experiment branches (optional) + reporting. |

---

## 9. Open questions (for discussion)

- Should **Operator** invoke **each skill’s** native scanners only, or also a **global** cross-skill linter maintained in `agentic-skill-builder`?
- How much of **Builder** must be **deterministic code** vs **LLM-authored** file content? (Recommendation: deterministic skeleton + LLM fills **parts/** bodies.)
- Do we publish a **JSON Schema** for `builder_manifest` for third-party skills?

---

## 10. References inside this monorepo

- `agilebydesign-skills/skills/agile-skill-build` — scaffold + build order.  
- `agilebydesign-skills/skills/abd-context-to-memory/scripts/build.py` — engine delegation pattern.  
- `agilebydesign-skills/skills/abd-maps-models-specs/docs/orchestrator.md` — planner/runner/critic split.  
- `agilebydesign-skills/skills/abd-maps-models-specs/plan/pipeline-deep-dive.md` — domain critique of pipeline incentives (inform Expert rubric, not Operator).  
- `agile_bots/bots` — story + CRC rules as **form** and **outcome** hints for Expert.

---

*End of plan v0.1 — revise after your answers to §7.*
