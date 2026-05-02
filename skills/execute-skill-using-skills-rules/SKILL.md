---
name: execute-skill-using-skills-rules
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Bundle rules into SKILL.md, run scanners, fix failures; quality gate before and after work.
description: Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.
---

# execute-skill-using-skills-rules

## Deploy to Cursor

Cursor loads **Agent Skills** from **`~/.cursor/skills/<skill-name>/`** (all workspaces) and **`<repo>/.cursor/skills/<skill-name>/`** (this repo only). This package should appear as **`execute-skill-using-skills-rules`** so the model can discover it by name.

**Windows (recommended):** from **`agilebydesign-skills` repo root**, run **`Deploy-SkillOutputs.ps1`** — it creates the **`execute-skill-using-skills-rules`** skill junction and links **`ide-files/`** into **`.cursor/`** (rules + slash commands). **Default is Cursor only** (see **`-IDE`** on the script). Pass **`-IDE Both`** when the target repo should also get **`.vscode/*.instructions.md`** and **`.github/prompts/*.prompt.md`** (for example an engagement workspace using VS Code / GitHub Copilot). **This repo’s `.gitignore` ignores `.cursor/`, `.github/`, and `.vscode/` everywhere** — nothing from those trees is source; redeploy locally after clone (canonical text stays under each skill’s **`ide-files/`**).

Alternatively, use the shared **`deploy-skill-to-cursor`** script with an explicit junction name:

```powershell
powershell -ExecutionPolicy Bypass -File skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 `
  -SkillName execute-skill-using-skills-rules -SkillSourcePath skills\execute-skill-using-skills-rules -Force
```

That creates:

| Location | Path |
| -------- | ---- |
| **Personal** | `%USERPROFILE%\.cursor\skills\execute-skill-using-skills-rules` → `skills/execute-skill-using-skills-rules` |
| **Project** | (same as **Deploy-SkillOutputs** when `-ProjectRoot` is this repo) |

- Older docs mentioned **`--ProjectOnly`** / **`--UserOnly`** on a separate script; use **`-ProjectRoot`** on **Deploy-SkillOutputs** to scope rule links, and **`~/.cursor/skills`** for the junction unless you customize **`CursorSkillsRoot`**.

Junctions under **`%USERPROFILE%\.cursor\skills`** are **not committed** (outside this repo). After a fresh clone, run **`Deploy-SkillOutputs.ps1`** again. On macOS/Linux, symlink instead:  
`ln -s "$(pwd)/skills/execute-skill-using-skills-rules" ~/.cursor/skills/execute-skill-using-skills-rules`

### IDE helpers (`ide-files/`)

The workspace **quality gate** rule (**`execute-rules-gate.*`** — short handle), matching VS Code instruction, and slash command live under **`ide-files/`** (same pattern as other ABD skills). Canonical files:

| File | Role |
| --- | --- |
| **`execute-rules-gate.mdc`** | Cursor always-on rule — points at **this skill’s `SKILL.md`** and **`correct_output`** (no duplicated steps). |
| **`execute-rules-gate.instructions.md`** | Same body as the `.mdc` (VS Code). |
| **`execute-rules-gate.prompt.md`** | Slash command — open **execute-skill-using-skills-rules** + gate reminder. |

Deploy into **this repo** or another project:

```powershell
.\skills\execute-skill-using-skills-rules\scripts\Deploy-SkillOutputs.ps1 -ProjectRoot <repo-root> -Force
```

`-IDE` defaults to **`Cursor`**. Use **`-IDE Both`** if `<repo-root>` should also receive VS Code instructions and Copilot prompts.

That creates hard links from **`ide-files/`** into **`.cursor/rules/`** and **`.cursor/commands/`** (and **`.vscode/`** + **`.github/prompts/`** when **`-IDE Both`**), and ensures the **`execute-skill-using-skills-rules`** skill junction exists.

## What you can do

**execute-skill-using-skills-rules** gives you **four** practices you can drop into **any** agent or repo layout.

**What to point at:** Treat the skill being directly executed by the user or the agent as the center of attention — the **`--skill-root`** package. Read **its** **`rules/`**, run bundle and scanners against **that** skill, and validate **its** output.

1. **Refresh the “bundled rules” section inside a target skill’s `SKILL.md`** — Your real rule text lives in **`rules/*.md`**. A script copies that text into **`SKILL.md`** between fixed markers so agents see the rules in one place. Run it after you edit any rule file.

2. **When an agent uses a skill to produce output, have it read that skill’s rules first** — Before substantive work, go through **`rules/*.md`** and the **Bundled rules** block in **`SKILL.md`**. The point is not “I saw the headings”; it is **using the skill according to those rules** (constraints, DO/DON’T, examples), not generic habits or a skim of **`SKILL.md`** alone. You can make that a **hard gate**: no main task until the pass is done. Walk it with [**quality-steps-checklist.md**](./templates/quality-steps-checklist.md) § Step 1.

3. **Validate output against the rules** — Do **both**: an **AI / rules pass** (read **`rules/*.md`** and bundled rules; judge whether the deliverable fits — not only “scanners green”) **and** a **scanner pass** (**`run_scanners.py`** on **`--workspace`**). Treat that pair as the normal “does this match the rules?” workflow. Save scanner output somewhere durable (for example **`scanner-report/`**); fix failures and re-run; the rules pass still matters even when scanners pass.

4. **After something is wrong, follow the correction process** — Use the **correct_output** skill. It provides the full loop: identify, log, re-generate, iterate on the **output** until correct, then optionally improve the source. See **[skills/correct_output/SKILL.md](../correct_output/SKILL.md)** for the process and **[skills/correct_output/templates/corrections-log.md](../correct_output/templates/corrections-log.md)** for the log template. Put the log under the engagement or project tree — not inside the installed skill package.


## The Target Skill Layout

For this skill to work the **target skill** must have **`rules/*.md`** — the rule files produced when you build the skill with the flow that **creates** those rules. Otherwise the executor has nothing real to bundle or run.

| Piece | Role |
| --- | --- |
| **`SKILL.md`** | Instructions for the agent; may include rule prose **between** `execute_rules:bundle_rules` markers (filled by **`bundle_rules_into_skill_md.py`**) |
| **`rules/<name>.md`** | **Source of truth** for rule prose — edit here, not inside the bundled block |
| **`scanners/*-scanner.py`** | Optional: CLI entrypoint per concern (beside scanner modules); linked from rule frontmatter via **`scanner:`** |
| **`scripts/scanner_bases/`** | Shared **Python** package: abstract **`Scanner`**, **`Violation`**, **`EvalPaths`**, scan-context dataclasses, **`SimpleRule`**, **`vocabulary_helper`**. Story-domain types (**`StoryScanner`**, **`StoryMap`**, …) live in sibling **[story-graph-ops](../story-graph-ops/)** (**`story_map`**, **`story_scanner`**, … on **`PYTHONPATH`**). See **`scripts/scanner_bases/README.md`**. **`scripts/scanner_runner.py`** runs any scanner with a caller-built **`ScanFilesContext`**. **`run_scanners.py`** prepends **`…/story-graph-ops/scripts`** then **`…/execute-skill-using-skills-rules/scripts`** to **`PYTHONPATH`**. |

**abd-story-mapping:** validators live under **`skills/abd-story-mapping/scanners/`** — **`scanner_bases`** for generic types, **`story_map`** / **`story_scanner`** (story-graph-ops **scripts/**) for graph scanners; refresh **`scanner_bases`** from **`execute-skill-using-skills-rules/scripts/scanner_bases/`**, not duplicated inside abd-story-mapping.

Rule file → scanner: put **`scanner: <stem>`** in the YAML frontmatter of **`rules/<stem>.md`** (or equivalent); the CLI script is expected at **`scanners/<stem>-scanner.py`** (next to scanner modules under **`scanners/`**). Scanner merge / **`build.build_pipeline`** / extra vocabulary: see **`rules-and-scanners.md`** (or equivalent) **in the repo that ships your agent docs** — not required for a minimal copy of **execute-skill-using-skills-rules** alone.

Text **between** the **`execute_rules:bundle_rules`** markers in **`SKILL.md`** is **generated** from **`rules/*.md`**. Editing it by hand is wasted work — the next bundle run overwrites it. Always change **`rules/*.md`**, then run **`bundle_rules_into_skill_md.py`**.

## Commands

`<execute-skill-using-skills-rules_root>` = directory that contains this skill’s **`scripts/`** (same folder as **`SKILL.md`** for **execute-skill-using-skills-rules**). Substitute your real path or `cd` there first.

**1. `bundle_rules_into_skill_md.py`** — Replaces the content **between** `<!-- execute_rules:bundle_rules:begin -->` and `<!-- execute_rules:bundle_rules:end -->` in the target **`SKILL.md`** with prose from **`rules/*.md`** (sorted by filename). **YAML frontmatter** on each rule file is **dropped** (use it for `scanner:` and other machine fields only). Body text is copied **verbatim** after heading demotion — keep **`rules/*.md`** free of third-repo sync instructions or other maintainer-only noise; authors read the bundled block as the rule set. It does **not** add a separate “how to re-run” intro — keep that in the skill author’s text if you want it. Headings in each rule file are **depth-bumped** (+2 `#` levels, capped at six) so `# Rule:` becomes **`### Rule:`** and `## DO` becomes **`#### DO`** when inlined. Run after you edit any rule file.

- **User can say (examples):** “Bundle rules into `SKILL.md` for `<path-to-skill>`.” · “Re-bundle the skill after I changed `rules/*.md`.” · “Refresh the bundled rules section for this skill.”

```bash
python <execute-skill-using-skills-rules_root>/scripts/bundle_rules_into_skill_md.py --skill-root <path-to-skill>
```

**2. Validate output (AI pass + scanner pass)** — Treat this as **one** intent: check a deliverable against the **target** skill’s rules **and** run mechanical scanners. Do **not** skip straight to the script; the AI pass catches what scanners miss.

- **A — Rules / AI pass:** With **`rules/*.md`** and the **Bundled rules** in **`SKILL.md`** for **`--skill-root`** in context, decide whether the output (the **`--workspace`** tree, or whatever the user points at) **matches** those rules — constraints, DO/DON’T, examples. Say what passes, what fails, and what is unclear.

- **B — Scanner pass:** Then run **`run_scanners.py`** with the same **`--skill-root`** and **`--workspace`** so automated checkers run on disk.

- **User can say (examples):** “Validate this output against the rules.” · “Does this match the rules?” · “Rules check plus scanners on `<path>`.” · “Full validation for this skill and workspace.”

```bash
python <execute-skill-using-skills-rules_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output-or-folder>
```

Add `--language <lang>` (e.g. `--language python`, `--language javascript`) when the skill organises scanners into language-specific subfolders under `scanners/<lang>/`. The flag:
- resolves scanner scripts from `scanners/<lang>/` instead of `scanners/`
- adds `scanners/<lang>/` to `PYTHONPATH` so language base classes are importable without package prefixes

```bash
python <execute-skill-using-skills-rules_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path> --language python
```

Scanner subprocesses receive **`PYTHONPATH`** including **`<execute-skill-using-skills-rules_root>/scripts`**, so scripts may **`import scanner_bases`** (shared bases) when implementing checks.

**Pytest / skill tests:** From the **agilebydesign-skills** repo root, `pytest` discovers **`skills/*/tests`**. Use **`scripts/scanner_test_helper.py`** so in-process tests get the same path order as **`run_scanners.py`**: call **`prepend_scanner_pythonpath(skill_root=...)`** before importing **`story_map`** or a skill **`scanners/*`** module; for subprocesses use **`build_scanner_env(...)`** or **`run_scanner_script(...)`**. The module exposes **`execute_skill_using_skills_rules_scripts()`** for the canonical **`…/execute-skill-using-skills-rules/scripts`** path.


**3. `rule_inventory.py`** (optional) — Summarizes **`rules/`** and bindings; **`--by-order`** prints a **`rule_id | title`** table sorted **alphabetically by rule file name** (no ranking column); **`--list-scanners`** prints the same scanner paths **`run_scanners.py`** would run.

- **User can say (examples):** “Show the rules table for `<path-to-skill>`.” · “List which scanners would run for this skill.” · “Run `rule_inventory` with `--by-order` or `--list-scanners`.”

```bash
python <execute-skill-using-skills-rules_root>/scripts/rule_inventory.py --skill-root <path-to-skill> --by-order
python <execute-skill-using-skills-rules_root>/scripts/rule_inventory.py --skill-root <path-to-skill> --list-scanners
```


---

## For agents (terminology)

- **Target / active skill** — The directory passed as **`--skill-root`**: the skill package you are maintaining or using.
- **execute-skill-using-skills-rules** — This skill package (these **`scripts/`**); 
- **Workspace / engagement tree** — Where the user’s project and artifacts (and often the corrections log) live — passed as **`--workspace`** for scanners when checking **output**, not the skill install root.
---
