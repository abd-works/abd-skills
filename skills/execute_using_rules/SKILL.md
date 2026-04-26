---
name: execute-rules
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Bundle rules into SKILL.md, run scanners, fix failures; quality gate before and after work.
description: Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.
---

# Execute rules

## Deploy to Cursor

Cursor loads **Agent Skills** from **`~/.cursor/skills/<skill-name>/`** (all workspaces) and **`<repo>/.cursor/skills/<skill-name>/`** (this repo only). This package should appear as **`execute-rules`** so the model can discover it by name.

**Windows (recommended):** create a **directory junction** to this folder (`skills/execute_using_rules`) so there is a single source of truth — no copying `SKILL.md` by hand.

From the **`agilebydesign-skills` repo root**:

```powershell
powershell -ExecutionPolicy Bypass -File skills/execute_using_rules/scripts/deploy-cursor-skill.ps1
```

That creates:

| Location | Path |
| -------- | ---- |
| **Personal** | `%USERPROFILE%\.cursor\skills\execute-rules` → `skills/execute_using_rules` |
| **Project** | `<repo>\.cursor\skills\execute-rules` → `skills/execute_using_rules` |

- **`--ProjectOnly`** — only the project junction (for CI or shared clone).  
- **`--UserOnly`** — only your user profile (global Cursor).

Junctions are **not committed** (see repo `.gitignore` under `.cursor/skills/execute-rules/`). After a fresh clone, run the script again. On macOS/Linux, symlink instead:  
`ln -s "$(pwd)/skills/execute_using_rules" ~/.cursor/skills/execute-rules`

---

## What you can do

**execute_rules** gives you **four** practices you can drop into **any** agent or repo layout.

**What to point at:** Treat the skill being directly executed by the user or the agent as the center of attention — the **`--skill-root`** package. Read **its** **`rules/`**, run bundle and scanners against **that** skill, and validate **its** output.

1. **Refresh the “bundled rules” section inside a target skill’s `SKILL.md`** — Your real rule text lives in **`rules/*.md`**. A script copies that text into **`SKILL.md`** between fixed markers so agents see the rules in one place. Run it after you edit any rule file.

2. **When an agent uses a skill to produce output, have it read that skill’s rules first** — Before substantive work, go through **`rules/*.md`** and the **Bundled rules** block in **`SKILL.md`**. The point is not “I saw the headings”; it is **using the skill according to those rules** (constraints, DO/DON’T, examples), not generic habits or a skim of **`SKILL.md`** alone. You can make that a **hard gate**: no main task until the pass is done. Walk it with [**quality-steps-checklist.md**](./templates/quality-steps-checklist.md) § Step 1.

3. **Validate output against the rules** — Do **both**: an **AI / rules pass** (read **`rules/*.md`** and bundled rules; judge whether the deliverable fits — not only “scanners green”) **and** a **scanner pass** (**`run_scanners.py`** on **`--workspace`**). Treat that pair as the normal “does this match the rules?” workflow. Save scanner output somewhere durable (for example **`scanner-report/`**); fix failures and re-run; the rules pass still matters even when scanners pass.

4. **After something is wrong, follow the correction process** — This starts **once there is a mistake** (rule miss, bad deliverable, failed check). **Output first, skill second:** do **not** jump straight to editing **`rules/`**, **`SKILL.md`**, or **`skill-config.json`**. Keep the **deliverable** right before you treat the skill’s sources as the fix. Field definitions and examples for the log: [**templates/corrections-log.md**](./templates/corrections-log.md). Put the log under the engagement or project tree (use the **workspace** skill configuration when present), e.g. **`logs/corrections-log.md`** next to that workspace — not inside the installed skill package.

   **Fix the output only** — until you and the user are satisfied with the deliverable:

   1. **Identify** — Note the problem; open or start the [**corrections log**](./templates/corrections-log.md).
   2. **Log (initial)** — Capture DO / DO NOT + **Example (wrong)**; leave **Example (correct)** blank until you are done iterating. **Phrasing:** Write **DO / DO NOT** (and later **Fix the skill** edits) as **altered behavior** — what to do next — not as a long restatement of the mistake. **Example (wrong)** carries the failure; normative text should stay **forward-looking** (see [**corrections-log.md**](./templates/corrections-log.md) **Phrasing**).
   3. **Re-generate** — Apply the rule explicitly; expect **multiple chat turns** before the output is good enough.
   4. **Review** — Refine the deliverable and log notes as you go; repeat until you are **actually satisfied**, not after the first fix attempt.
   5. **Confirm** — Only then fill **Example (correct)** and mark the entry done.

   **Fix the skill** — only after the steps above (or when the user explicitly asks to change the skill). After several log entries, the user may ask you to analyze patterns and edit sources.

   - **a.** Read the log as a **set** of issues.
   - **b.** Find **root causes** (missing rule, vague instruction, missing scanner, etc.).
   - **c.** **Propose** source changes; agree before editing.
   - **d.** Edit **`rules/*.md`** and other sources — **not** the bundled block as your main edit.
   - **e.** Run **`bundle_rules_into_skill_md.py`** and a **full validation** (**Commands §2**: AI pass + **`run_scanners.py`**) as needed; confirm clean.
   - **f.** Clear or archive resolved log entries.


## The Target Skill Layout

For this skill to work the **target skill** must have **`rules/*.md`** — the rule files produced when you build the skill with the flow that **creates** those rules. Otherwise the executor has nothing real to bundle or run.

| Piece | Role |
| --- | --- |
| **`SKILL.md`** | Instructions for the agent; may include rule prose **between** `execute_rules:bundle_rules` markers (filled by **`bundle_rules_into_skill_md.py`**) |
| **`rules/<name>.md`** | **Source of truth** for rule prose — edit here, not inside the bundled block |
| **`scanners/*-scanner.py`** | Optional: CLI entrypoint per concern (beside scanner modules); linked from rule frontmatter via **`scanner:`** |
| **`scripts/scanner_bases/`** | Shared **Python** package: abstract **`Scanner`**, **`Violation`**, **`EvalPaths`**, scan-context dataclasses, **`SimpleRule`**, **`vocabulary_helper`**. Story-domain types (**`StoryScanner`**, **`StoryMap`**, …) live in sibling **[story-graph-ops](../story-graph-ops/)** (**`story_map`**, **`story_scanner`**, … on **`PYTHONPATH`**). See **`scripts/scanner_bases/README.md`**. **`scripts/scanner_runner.py`** runs any scanner with a caller-built **`ScanFilesContext`**. **`run_scanners.py`** prepends **`…/story-graph-ops/scripts`** then **`…/execute_using_rules/scripts`** to **`PYTHONPATH`**. |

**abd-story-mapping:** validators live under **`skills/abd-story-mapping/scanners/`** — **`scanner_bases`** for generic types, **`story_map`** / **`story_scanner`** (story-graph-ops **scripts/**) for graph scanners; refresh **`scanner_bases`** from **`execute_using_rules/scripts/scanner_bases/`**, not duplicated inside abd-story-mapping.

Rule file → scanner: put **`scanner: <stem>`** in the YAML frontmatter of **`rules/<stem>.md`** (or equivalent); the CLI script is expected at **`scanners/<stem>-scanner.py`** (next to scanner modules under **`scanners/`**). Scanner merge / **`build.build_pipeline`** / extra vocabulary: see **`rules-and-scanners.md`** (or equivalent) **in the repo that ships your agent docs** — not required for a minimal copy of **execute_rules** alone.

Text **between** the **`execute_rules:bundle_rules`** markers in **`SKILL.md`** is **generated** from **`rules/*.md`**. Editing it by hand is wasted work — the next bundle run overwrites it. Always change **`rules/*.md`**, then run **`bundle_rules_into_skill_md.py`**.

## Commands

`<execute_rules_root>` = directory that contains this skill’s **`scripts/`** (same folder as **`SKILL.md`** for **execute_rules**). Substitute your real path or `cd` there first.

**1. `bundle_rules_into_skill_md.py`** — Replaces the content **between** `<!-- execute_rules:bundle_rules:begin -->` and `<!-- execute_rules:bundle_rules:end -->` in the target **`SKILL.md`** with prose from **`rules/*.md`** (sorted by filename). **YAML frontmatter** on each rule file is **dropped** (use it for `scanner:` and other machine fields only). Body text is copied **verbatim** after heading demotion — keep **`rules/*.md`** free of third-repo sync instructions or other maintainer-only noise; authors read the bundled block as the rule set. It does **not** add a separate “how to re-run” intro — keep that in the skill author’s text if you want it. Headings in each rule file are **depth-bumped** (+2 `#` levels, capped at six) so `# Rule:` becomes **`### Rule:`** and `## DO` becomes **`#### DO`** when inlined. Run after you edit any rule file.

- **User can say (examples):** “Bundle rules into `SKILL.md` for `<path-to-skill>`.” · “Re-bundle the skill after I changed `rules/*.md`.” · “Refresh the bundled rules section for this skill.”

```bash
python <execute_rules_root>/scripts/bundle_rules_into_skill_md.py --skill-root <path-to-skill>
```

**2. Validate output (AI pass + scanner pass)** — Treat this as **one** intent: check a deliverable against the **target** skill’s rules **and** run mechanical scanners. Do **not** skip straight to the script; the AI pass catches what scanners miss.

- **A — Rules / AI pass:** With **`rules/*.md`** and the **Bundled rules** in **`SKILL.md`** for **`--skill-root`** in context, decide whether the output (the **`--workspace`** tree, or whatever the user points at) **matches** those rules — constraints, DO/DON’T, examples. Say what passes, what fails, and what is unclear.

- **B — Scanner pass:** Then run **`run_scanners.py`** with the same **`--skill-root`** and **`--workspace`** so automated checkers run on disk.

- **User can say (examples):** “Validate this output against the rules.” · “Does this match the rules?” · “Rules check plus scanners on `<path>`.” · “Full validation for this skill and workspace.”

```bash
python <execute_rules_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output-or-folder>
```

Add `--language <lang>` (e.g. `--language python`, `--language javascript`) when the skill organises scanners into language-specific subfolders under `scanners/<lang>/`. The flag:
- resolves scanner scripts from `scanners/<lang>/` instead of `scanners/`
- adds `scanners/<lang>/` to `PYTHONPATH` so language base classes are importable without package prefixes

```bash
python <execute_rules_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path> --language python
```

Scanner subprocesses receive **`PYTHONPATH`** including **`<execute_rules_root>/scripts`**, so scripts may **`import scanner_bases`** (shared bases) when implementing checks.

**Pytest / skill tests:** From the **agilebydesign-skills** repo root, `pytest` discovers **`skills/*/tests`**. Use **`scripts/scanner_test_helper.py`** so in-process tests get the same path order as **`run_scanners.py`**: call **`prepend_scanner_pythonpath(skill_root=...)`** before importing **`story_map`** or a skill **`scanners/*`** module; for subprocesses use **`build_scanner_env(...)`** or **`run_scanner_script(...)`**.


**3. `rule_inventory.py`** (optional) — Summarizes **`rules/`** and bindings; **`--by-order`** prints a **`rule_id | title`** table sorted **alphabetically by rule file name** (no ranking column); **`--list-scanners`** prints the same scanner paths **`run_scanners.py`** would run.

- **User can say (examples):** “Show the rules table for `<path-to-skill>`.” · “List which scanners would run for this skill.” · “Run `rule_inventory` with `--by-order` or `--list-scanners`.”

```bash
python <execute_rules_root>/scripts/rule_inventory.py --skill-root <path-to-skill> --by-order
python <execute_rules_root>/scripts/rule_inventory.py --skill-root <path-to-skill> --list-scanners
```


---

## For agents (terminology)

- **Target / active skill** — The directory passed as **`--skill-root`**: the skill package you are maintaining or using.
- **execute_rules** — This skill package (these **`scripts/`**); 
- **Workspace / engagement tree** — Where the user’s project and artifacts (and often the corrections log) live — passed as **`--workspace`** for scanners when checking **output**, not the skill install root.
---
