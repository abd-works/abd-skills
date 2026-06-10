# AGENTS — abd-practice-skill-builder

Edit **`AGENTS.md`** for normative agent prose. Rules live only in **`rules/*.md`** — there is no bundle step and no inlined block here.

---

## Purpose

**Goal:** Produce **practice skills** under the **agilebydesign-skills** repository, in **`skills/<skill-name>/`**, grounded in **abd-answers** (Pinecone RAG): **retrieve** evidence, **author** the package (**SKILL.md** starter from **abd-author-practice-skill** template + **`rules/*.md`**), optional **scanners**, **abd-skill-catalog**, then an **HTML manual** (vendored shell assets in **abd-practice-skill-manual**).

Orchestrate using the agent-local packages in **`skills/`** under this agent (same idea as **abd-context-to-memory** routing to nested **`skills/abd-*/SKILL.md`**).

---

## Agent Instructions

You run the **practice skill builder** pipeline. Before each stage, read that stage's **`SKILL.md`** and every file in its **`rules/`** and **`reference/`** folders. Rules live only in **`rules/*.md`** — there is no bundle step; do not run or reference `bundle_rules_into_skill_md.py`. For validating output and scanner commands, use **`skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md`** (**Commands** section).

**Stage boundary (retrieve vs author):** During **abd-query-practice-sources**, you only work under **`skills/<skill-name>/inputs/`** — mainly **`abd-answers-retrieval.md`**. **Do not** create or edit the target's **`rules/*.md`**, **`SKILL.md`**, **`templates/`**, or run **`bundle_rules_into_skill_md.py`** on the target in that step. Normative rules and **SKILL.md** prose come from **abd-author-practice-skill** using the retrieval log as evidence. If you mixed stages, run the corrections workflow below: fix **`inputs/`** first and log it; do **not** jump to editing maintainer **SKILL.md** to justify bad output.

**Teaching voice:** In the **target** **`SKILL.md`**, teach the method with **concepts and how they relate** (outcomes, who, behaviour change, options). Keep **diagram symbols, map placement, indentation-as-meaning, file prefix labels, and template positioning** (which line or field holds what) in **templates**, the **Agent Instructions** table, **Build**, **Validate**, and **`rules/*.md`** — see **abd-author-practice-skill** (bundled **Core sections teach ideas before file prefixes and diagram notation**). Do **not** pad body prose with provenance throat-clearing (for example "from the training wording", "training-aligned", "tightened for this notation"); use **`Source:`** on **rules** when lineage must be auditable (bundled **Clear English in every skill section**).

### Corrections workflow (mandatory)

When any deliverable is wrong, a rule was missed, or stages were mixed, you **follow execute-skill-using-skills-rules item 4 in full** — read **`skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md`** ( **What you can do**, item **4** ) and use the field table and markdown shape in **`skill-helpers/skills/execute-skill-using-skills-rules/templates/corrections-log.md`**. **No shortcuts:** you do not skip the log or go straight to editing **`rules/`** / **`SKILL.md`** / this agent's sources.

**Log location:** Under the engagement or project tree ( **`active_skill_workspace`** when **`skill-config.json`** sets **`workspace`** ), e.g. **`logs/corrections-log.md`**, **`progress/corrections-log.md`**, or **`.skill-builder/corrections-log.md`**. **Not** inside **`agents/abd-practice-skill-builder/`** or an installed skill package as the canonical log.

**Fix the output only** (complete all of these before **Fix the skill**):

1. **Identify** — Note the problem; **open or create** the corrections log file.
2. **Log (initial)** — Add an entry: **Rule**, **Affects** (include **`stage:`** using practice-builder stages: **`retrieve`**, **`author`**, **`scanners`**, **`catalog`**, **`manual`**, or **`*`** when cross-cutting), **DO / DO NOT**, **Example (wrong)**; leave **Example (correct)** blank and **Status: open**. **DO / DO NOT** must state **altered behavior** (what to do next); the mistake lives in **Example (wrong)** — see **`skill-helpers/skills/execute-skill-using-skills-rules/templates/corrections-log.md`** **Phrasing**.
3. **Re-generate** — Fix the **artifact on disk** (retrieval log, **SKILL.md**, rules, manual, etc.) per the violated rule; expect **multiple** iterations.
4. **Review** — Repeat until the deliverable is **actually** acceptable, not after one quick edit.
5. **Confirm** — Fill **Example (correct)**; set **Status: confirmed** for that entry.

**Fix the skill** — only **after** the output steps above for that issue, or when the user **explicitly** asks to change maintainer sources. Then follow item 4 **Fix the skill** substeps **a** through **f** in **`skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md`** (read log as a set, root causes, propose and agree, edit **`rules/*.md`** directly, validate with per-rule verdicts + scanner pass, archive).

- Use the **track_task** skill; track steps in **`progress/`** per **track_task**.
- Example layout references: `abd-clean-code`, `abd-story-mapping`, `abd-story-acceptance-criteria`, `abd-story-specification`, `abd-thin-slicing`, `abd-story-acceptance-test`.

Keep **one canonical narrative** in the new skill and manual; RAG hits are **evidence**, not a second master.

### Commands (repo root)

```bash
python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root skills/<skill-name> --workspace <path-to-output-or-folder>
```


## Pipeline

Typical order (adjust per engagement):

1. **Retrieve** — **abd-query-practice-sources** — read that skill first; **`inputs/`** only on the target package (no **`rules/`** or **SKILL.md** here); structured queries against abd-answers (`npm run rag:query` from **`agents/abd-answers/`** in this repo, or a standalone **abd-answers** clone); ensure **`skills/<name>/`** and **`inputs/`** exist; write **`inputs/abd-answers-retrieval.md`** with **Kept chunks** (verbatim fenced bodies) per **abd-query-practice-sources** template — not summary-only tables.
2. **Author SKILL + rules** — **abd-author-practice-skill** — read that skill first; if **`SKILL.md`** is missing, copy **`templates/SKILL_template.md`** from that skill, add **Manual:** line and bundle markers, ensure **`rules/`** and **`templates/`**; fill **`SKILL.md`** from **`inputs/abd-answers-retrieval.md`**, write **`rules/*.md`**, run **`bundle_rules_into_skill_md.py`** on the **new** skill (no scanners in this step).
3. **Scanners** — **abd-build-practice-scanners** — read that skill first; optional **`scanners/*.py`**, **`scanner:`** on rules; **`run_scanners.py`** when scanners exist (per **execute-skill-using-skills-rules**).
4. **AI Garden site** — **abd-skill-catalog** — maintain **`skills/<name>/README.md`** AI Garden card copy (`catalogue_summary`, **`## Overview`**, optional **`## How it fits together`** + ascii); from **agilebydesign-skills** repo root run **`python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py`**.
5. **Manual** — **abd-practice-skill-manual** — **`manual/<skill-name>/`** HTML, link from **`SKILL.md`** top and in-body section refs.

**Skill index (this agent):**

| Skill | Path |
| --- | --- |
| Query sources | [skill-builder/skills/abd-query-practice-sources/SKILL.md](../../skill-builder/skills/abd-query-practice-sources/SKILL.md) |
| Author SKILL + rules | [skill-builder/skills/abd-author-practice-skill/SKILL.md](../../skill-builder/skills/abd-author-practice-skill/SKILL.md) |
| Scanners | [skill-builder/skills/abd-build-practice-scanners/SKILL.md](../../skill-builder/skills/abd-build-practice-scanners/SKILL.md) |
| AI Garden (`abd-skill-catalog`) | [skill-builder/skills/abd-skill-catalog/SKILL.md](../../skill-builder/skills/abd-skill-catalog/SKILL.md) |
| HTML manual | [skill-builder/skills/abd-practice-skill-manual/SKILL.md](../../skill-builder/skills/abd-practice-skill-manual/SKILL.md) |
| execute-skill-using-skills-rules (quality + corrections) | [../../skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md](../../skill-helpers/skills/execute-skill-using-skills-rules/SKILL.md) |
| track_task | [../../skill-helpers/skills/track_task/SKILL.md](../../skill-helpers/skills/track_task/SKILL.md) |

---

## Workspace

**Delivery target is always the agilebydesign-skills repo:** new and updated practice skills live in **`agilebydesign-skills/skills/<skill-name>/`**, not only under this agent folder. This agent holds orchestration SKILLS and templates; generated packages are real repo skills.

- **agilebydesign-skills** repo — outputs under **`skills/<skill-name>/`**; canonical **`SKILL.md`** skeleton: **`skill-builder/skills/abd-author-practice-skill/templates/SKILL_template.md`**.
- **abd-answers** repo — **`npm run rag:query`** (see **abd-query-practice-sources**); **`conf/.secrets`** per abd-answers docs.

## Cursor (workspace-local)

Use a **Windows directory junction** (not a symlink): this agent is linked into **`<repo>\.cursor\agents\abd-practice-skill-builder\`** so **`AGENTS.md`** and the nested **`skills/`** tree resolve from this workspace with no duplicate copy. From this agent root:

```powershell
.\scripts\Deploy-AgentToCursor.ps1 -Force
```

Pipeline **skills** use the same mechanism under **`<repo>\.cursor\skills\`** via **`skill-helpers/skills/deploy-skill-to-cursor/scripts/Deploy-SkillToCursor.ps1`** and **`-SkillSourcePath`** (see **deploy-skill-to-cursor**).

---

## Process

### End-to-end

1. Confirm **topic** and **skill name** (kebab-case under **`agilebydesign-skills/skills/`**).
2. Run **abd-query-practice-sources** — read that skill first; **`inputs/`** only (no target **`rules/`** or **SKILL.md**); structured query plan; ensure **`skills/<skill-name>/`** and **`inputs/`**; write **`inputs/abd-answers-retrieval.md`** using **`skill-builder/skills/abd-query-practice-sources/templates/abd-answers-retrieval-input.md`** (**Kept chunks** with verbatim bodies). If the log is wrong, run **Corrections workflow** (log + fix **`inputs/`** through **Confirm**) before authoring rules from it.
3. Run **abd-author-practice-skill** — read that skill first; if needed, copy **`abd-author-practice-skill/templates/SKILL_template.md`** to **`SKILL.md`**, ensure **`rules/`**, **`reference/`**, **`templates/`**; fill **SKILL.md** as a thin router, write **`rules/*.md`**, move concept/example prose to **`reference/`** (no scanners, no bundling).
4. Run **abd-build-practice-scanners** (optional) — **`scanners/*.py`**, **`scanner:`** on rules; **`run_scanners.py`** when applicable.
5. Run **abd-skill-catalog** — **`skills/<skill-name>/README.md`** for the AI Garden; from repo root **`python skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py`**.
6. Run **abd-practice-skill-manual** — copy **`assets/`** from **abd-practice-skill-manual** into **`manual/<skill-name>/`**; HTML sections; **SKILL.md** **Manual:** links.

### When hub content changes

Re-run retrieval; update **`inputs/abd-answers-retrieval.md`**, rules, **README.md**, **catalog/** if needed, then manual; bump **Revision** in the manual footer.

---
