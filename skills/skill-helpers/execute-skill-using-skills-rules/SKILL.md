---
name: execute-skill-using-skills-rules
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Run scanners, validate output against rules, fix failures; quality gate before and after work.
description: Read rules before work, validate output (AI pass + scanner pass), and follow the correction process after mistakes.
---

# execute-skill-using-skills-rules

## What you can do

**execute-skill-using-skills-rules** gives you **three** practices you can drop into **any** agent or repo layout.

**What to point at:** Treat the skill being directly executed by the user or the agent as the center of attention — the **`--skill-root`** package. Read **its** **`rules/`**, run scanners against **that** skill, and validate **its** output.

1. **When an agent uses a skill to produce output, have it read that skill's rules first** — Before substantive work, go through **`rules/*.md`** and the **Bundled rules** block in **`SKILL.md`**. The point is not "I saw the headings"; it is **using the skill according to those rules** (constraints, DO/DON'T, examples), not generic habits or a skim of **`SKILL.md`** alone. You can make that a **hard gate**: no main task until the pass is done. Walk it with [**quality-steps-checklist.md**](./templates/quality-steps-checklist.md) § Step 1.

2. **Validate output against the rules** — Do **both**: an **AI / rules pass** (read **`rules/*.md`** and bundled rules; judge whether the deliverable fits — not only "scanners green") **and** a **scanner pass** (**`run_scanners.py`** on **`--workspace`**). Treat that pair as the normal "does this match the rules?" workflow. Save scanner output somewhere durable (for example **`scanner-report/`**); fix failures and re-run; the rules pass still matters even when scanners pass.

3. **After something is wrong, follow the correction process** — See **`guidance/log-and-fix-skill-errors`** for the full loop: identify, log, re-generate, iterate on the **output** until correct, then optionally improve the source. Put the log under the engagement or project tree — not inside the installed skill package.


## The Target Skill Layout

For this skill to work the **target skill** must have **`rules/*.md`** — the rule files produced when you build the skill with the flow that **creates** those rules. Otherwise the executor has nothing real to run.

| Piece | Role |
| --- | --- |
| **`SKILL.md`** | Instructions for the agent; may include rule prose **between** `execute_rules:bundle_rules` markers (filled by the skill builder) |
| **`rules/<name>.md`** | **Source of truth** for rule prose — edit here, not inside the bundled block |
| **`scanners/*-scanner.py`** | Optional: CLI entrypoint per concern (beside scanner modules); linked from rule frontmatter via **`scanner:`** |
| **`scripts/scanner_bases/`** | Shared **Python** package: abstract **`Scanner`**, **`Violation`**, **`EvalPaths`**, scan-context dataclasses, **`SimpleRule`**, **`vocabulary_helper`**. Story-domain types (**`StoryScanner`**, **`StoryMap`**, …) live in sibling **[story-graph-ops](../story-graph-ops/)** (**`story_map`**, **`story_scanner`**, … on **`PYTHONPATH`**). See **`scripts/scanner_bases/README.md`**. **`scripts/scanner_runner.py`** runs any scanner with a caller-built **`ScanFilesContext`**. **`run_scanners.py`** prepends **`…/story-graph-ops/scripts`** then **`…/execute-skill-using-skills-rules/scripts`** to **`PYTHONPATH`**. |

Rule file → scanner: put **`scanner: <stem>`** in the YAML frontmatter of **`rules/<stem>.md`** (or equivalent); the CLI script is expected at **`scanners/<stem>-scanner.py`** (next to scanner modules under **`scanners/`**).

Text **between** the **`execute_rules:bundle_rules`** markers in **`SKILL.md`** is **generated** — editing it by hand is wasted work. Always change **`rules/*.md`**, then use the skill builder to re-bundle.

## Commands

`<execute-skill-using-skills-rules_root>` = directory that contains this skill's **`scripts/`** (same folder as **`SKILL.md`** for **execute-skill-using-skills-rules**). Substitute your real path or `cd` there first.

**1. Validate output (AI pass + scanner pass)** — Treat this as **one** intent: check a deliverable against the **target** skill's rules **and** run mechanical scanners. Do **not** skip straight to the script; the AI pass catches what scanners miss.

- **A — Rules / AI pass:** With **`rules/*.md`** and the **Bundled rules** in **`SKILL.md`** for **`--skill-root`** in context, decide whether the output (the **`--workspace`** tree, or whatever the user points at) **matches** those rules — constraints, DO/DON'T, examples. Say what passes, what fails, and what is unclear.

- **B — Scanner pass:** Then run **`run_scanners.py`** with the same **`--skill-root`** and **`--workspace`** so automated checkers run on disk.

- **User can say (examples):** "Validate this output against the rules." · "Does this match the rules?" · "Rules check plus scanners on `<path>`." · "Full validation for this skill and workspace."

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

---

## For agents (terminology)

- **Target / active skill** — The directory passed as **`--skill-root`**: the skill package you are maintaining or using.
- **execute-skill-using-skills-rules** — This skill package (these **`scripts/`**).
- **Workspace / engagement tree** — Where the user's project and artifacts (and often the corrections log) live — passed as **`--workspace`** for scanners when checking **output**, not the skill install root.
---
