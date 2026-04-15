---
name: execute-rules
description: Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.
---

# Execute rules

## What you can do

**execute_rules** gives you **four** practices you can drop into **any** agent or repo layout.

**What to point at:** Treat the skill being directlye executed by user or the agent as the center of attention — the **`--skill-root`** package. Read **its** **`rules/`**, run bundle and scanners against **that** skill, and validate **its** output.

1. **Refresh the “bundled rules” section inside a target skill’s `SKILL.md`** — Your real rule text lives in **`rules/*.md`**. A script copies that text into **`SKILL.md`** between fixed markers so agents see the rules in one place. Run it after you edit any rule file.

2. **When an agent uses a skill to produce output, have it read that skill’s rules first** — Before substantive work, go through **`rules/*.md`** and the **Bundled rules** block in **`SKILL.md`**. The point is not “I saw the headings”; it is **using the skill according to those rules** (constraints, DO/DON’T, examples), not generic habits or a skim of **`SKILL.md`** alone. You can make that a **hard gate**: no main task until the pass is done. Walk it with [**quality-steps-checklist.md**](./templates/quality-steps-checklist.md) § Step 1.

3. **Validate output against the rules** — Do **both**: an **AI / rules pass** (read **`rules/*.md`** and bundled rules; judge whether the deliverable fits — not only “scanners green”) **and** a **scanner pass** (**`run_scanners.py`** on **`--workspace`**). Treat that pair as the normal “does this match the rules?” workflow. Save scanner output somewhere durable (for example **`scanner-report/`**); fix failures and re-run; the rules pass still matters even when scanners pass.

4. **After something is wrong, follow the correction process** — This starts **once there is a mistake** (rule miss, bad deliverable, failed check). **Output first, skill second:** do **not** jump straight to editing **`rules/`**, **`SKILL.md`**, or **`skill-config.json`**. Keep the **deliverable** right before you treat the skill’s sources as the fix. Field definitions and examples for the log: [**templates/corrections-log.md**](./templates/corrections-log.md). Put the log under the engagement or project tree (use the **workspace** skill configuration when present), e.g. **`logs/corrections-log.md`** next to that workspace — not inside the installed skill package.

   **Fix the output only** — until you and the user are satisfied with the deliverable:

   1. **Identify** — Note the problem; open or start the [**corrections log**](./templates/corrections-log.md).
   2. **Log (initial)** — Capture DO / DO NOT + **Example (wrong)**; leave **Example (correct)** blank until you are done iterating.
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
| **`SKILL.md`** | Instructions for the agent; includes a generated **Bundled rules** section |
| **`rules/<name>.md`** | **Source of truth** for rule prose — edit here, not inside the bundled block |
| **`scripts/scanners/*-scanner.py`** | Optional: one checker per concern; linked from rule frontmatter via **`scanner:`** |

Rule file → scanner: put **`scanner: <stem>`** in the YAML frontmatter of **`rules/<stem>.md`** (or equivalent); the script is expected at **`scripts/scanners/<stem>-scanner.py`**. Merge order, **`build.build_pipeline`**, and extra vocabulary: see **`rules-and-scanners.md`** (or equivalent) **in the repo that ships your agent docs** — not required for a minimal copy of **execute_rules** alone.

The **Bundled rules** section in **`SKILL.md`** is **generated**. Editing it by hand is wasted work — the next bundle run overwrites it. Always change **`rules/*.md`**, then run **`bundle_rules_into_skill_md.py`**.

## Commands

`<execute_rules_root>` = directory that contains this skill’s **`scripts/`** (same folder as **`SKILL.md`** for **execute_rules**). Substitute your real path or `cd` there first.

**1. `bundle_rules_into_skill_md.py`** — Writes the **Bundled rules** block in the target **`SKILL.md`** from **`rules/*.md`**. Run after you edit any rule file.

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


**3. `rule_inventory.py`** (optional) — Summarizes **`rules/`** and bindings; **`--list-scanners`** prints the same scanner paths **`run_scanners.py`** would run.

- **User can say (examples):** “Show the rules for `<path-to-skill>` in order.” · “List which scanners would run for this skill.” · “Run `rule_inventory` with `--by-order` or `--list-scanners`.”

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
