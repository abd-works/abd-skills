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

**Authoring** or **rewriting** normative prose in **SKILL.md** or **`rules/*.md`** for meaning — only **scanners**, **`scanner:`** hooks, and **`run_scanners.py`**.

## Prerequisites

- **`skills/<skill-name>/`** with finalized (or stable draft) **`SKILL.md`** and **`rules/*.md`**.

Read [`common/skill-package-layout.md`](../../../../common/skill-package-layout.md) and [`common/skill-workflow.md`](../../../../common/skill-workflow.md) § Validate output.

## Agent Instructions

> **MANDATORY — read every file in `rules/` for this skill before starting. Rules/*.md are the source of truth; nothing is inlined here.**

1. **Choose checkable rules** — Pick **`rules/*.md`** concerns that can be enforced mechanically (regex, file presence, forbidden phrases).

2. **Implement scanners** — Under **`scanners/`**:
   - **`scanners/<stem>-scanner.py`** — executable CLI; follow **`skills/abd-story-mapping/scanners/`** import pattern (`common/scripts`, `scanner_runner`, `scanner_bases`).

3. **Wire frontmatter** — Set **`scanner: <stem>`** on **`rules/<stem>.md`** (stem matches script name without `-scanner.py`).

4. **Run checks** — Run **`run_scanners.py`** with **`--workspace`** when the skill produces files to scan; compare rule **intent** to scanner **coverage** as a critic.

## Template starter

Practice **`SKILL.md`** skeleton (new packages) lives with **abd-author-practice-skill**: **`skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md`**. For scanners only: copy **`templates/scanner-readme-snippet.md`** from **this** skill into **`references/`** or **`scanners/README.md`**. Use **`templates/rule-stub.md`** only when **adding** a new **scanner-backed** rule; finish normative prose in **`rules/*.md`** before **`scanner:`** if needed.

## Validate

**Goal:** No false confidence from **scanner:** labels. For each rule below, emit `Rule: <name> -> PASS` or `Rule: <name> -> FAIL <reason>`.

- **Parity** — Every **`scanner:`** has **`scanners/<stem>-scanner.py`**; no **`scanner:`** without a script.
- **Messages** — Failures are **actionable**; output points to what to change.
- **Coverage** — Spot-check: each scanner still matches the **rule** it claims to enforce.
- **No inlined rules** — **`SKILL.md`** contains no `<!-- execute_rules:bundle_rules -->` markers.

---
