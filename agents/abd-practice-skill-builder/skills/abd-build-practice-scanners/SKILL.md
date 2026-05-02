---
name: abd-build-practice-scanners
description: >-
  Turn written rules into checks a machine can run, so drift is caught early instead
  of debated in chat.
---

# abd-build-practice-scanners

## Purpose

Written **DO / DO NOT** rules are easy to **ignore** or **misread**. Small **automated checks** (scripts tied to those rules) make the same expectations **repeatable**: a failure means something concrete to fix, not a vague "are we sure?" moment.

## When to use

- The **target** practice already has **`SKILL.md`** and **`rules/*.md`** in **stable** shape.
- Some rules are **checkable** mechanically (patterns, files, forbidden phrases).
- You are ready to wire **`scanner:`** in rule frontmatter **only** where a matching **`scanners/<stem>-scanner.py`** exists.

## Not in this pass

**Authoring** or **rewriting** normative prose in **SKILL.md** or **`rules/*.md`** for meaning — only **scanners**, **`scanner:`** hooks, **`run_scanners.py`**, and **re-bundle**.

## Prerequisites

- **`skills/<skill-name>/`** with finalized (or stable draft) **`SKILL.md`** and **`rules/*.md`**.
- **`bundle_rules_into_skill_md.py`** has been run at least once after the latest rule edits.

Read **`skills/execute-skill-using-skills-rules/SKILL.md`** sections **Target Skill Layout** and **Commands**.

## Agent instructions

Apply the **bundled rules** at the end of this file so **`scanner:`** and scripts stay honest.

1. **Choose checkable rules** — Pick **`rules/*.md`** concerns that can be enforced mechanically (regex, file presence, forbidden phrases).

2. **Implement scanners** — Under **`scanners/`**:
   - **`scanners/<stem>-scanner.py`** — executable CLI; follow **`skills/abd-story-mapping/scanners/`** import pattern (`execute-skill-using-skills-rules/scripts`, `scanner_runner`, `scanner_bases`).

3. **Wire frontmatter** — Set **`scanner: <stem>`** on **`rules/<stem>.md`** (stem matches script name without `-scanner.py`).

4. **Re-bundle** — After editing rules:

   ```bash
   python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/<skill-name>
   ```

5. **Run checks** — Run **`run_scanners.py`** with **`--workspace`** when the skill produces files to scan; compare rule **intent** to scanner **coverage** as a critic.

## Template starter

Practice **`SKILL.md`** skeleton (new packages) lives with **abd-author-practice-skill**: **`agents/abd-practice-skill-builder/skills/abd-author-practice-skill/templates/SKILL_template.md`**. For scanners only: copy **`templates/scanner-readme-snippet.md`** from **this** skill into **`references/`** or **`scanners/README.md`**. Use **`templates/rule-stub.md`** only when **adding** a new **scanner-backed** rule; finish normative prose in **`rules/*.md`** before **`scanner:`** if needed.

## Validate

**Goal:** No false confidence from **scanner:** labels.

- **Parity** — Every **`scanner:`** has **`scanners/<stem>-scanner.py`**; no **`scanner:`** without a script.
- **Messages** — Failures are **actionable**; output points to what to change.
- **Bundle** — **`SKILL.md`** bundled block matches **`rules/*.md`** after edits.
- **Coverage** — Spot-check: each scanner still matches the **rule** it claims to enforce.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Scanner wiring

**Scanner:** Manual review

#### DO

- **Implement first, then tag** — **`scanners/<stem>-scanner.py`** exists and runs before **`scanner: <stem>`** appears in **`rules/<stem>.md`**.
- **Re-bundle** after any **`rules/*.md`** or scanner change so **SKILL.md** stays truthful.

#### DO NOT

- Add **`scanner:`** to **sell** rigor when the script is missing or stub-only.
- Use this pass to **rewrite** rule meaning — fix scanners or rule text in **small**, reviewable steps.

**Source:** Practice-skill builder convention (abd-build-practice-scanners).
<!-- execute_rules:bundle_rules:end -->
