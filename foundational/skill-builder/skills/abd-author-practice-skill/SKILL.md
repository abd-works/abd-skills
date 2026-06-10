---
name: abd-author-practice-skill
description: >-
  Turn collected hub evidence into a finished practice skill: clear instructions and
  checkable do-and-don't norms that stay true to what you retrieved.
---
# abd-author-practice-skill

## Purpose

Teams need **practice skills** that people and agents can follow without improvising or drifting away from what the sources actually say. This authoring skill helps you **finish** such a package after you have already chosen what to keep from the hub: the teaching on the skill page reads clearly, and the norms on the outputs are explicit enough to pass or fail. It guides you from that evidence to aligned prose and checks. **Prerequisites**, **Build**, and **Not in this pass** on this page carry retrieval and scanner wiring when you need those steps.

## When to use

- You **already gathered** the hub material for a practice and want to **produce the skill** itself—not run more searches.
- The practice is still a **rough draft** and you want it **finished**: readable instructions and **explicit** what-to-do / what-not-to-do norms.
- You care that the **finished guidance matches** what you collected, without invented process or hand-waving.

## Not in this pass

Wiring **Python scanners** on the **target** package belongs in a **later** pass, and only after **`scanners/*.py`** exist for any **`scanner:`** you add to rules.

## Prerequisites

- **Target:** `agilebydesign-skills/skills/<skill-name>/` (the practice package you are finishing, not this authoring skill).
- **`inputs/abd-answers-retrieval.md`** — every **Kept chunk** has a verbatim fenced **body** plus **Relevance**, query, rank, and source (see **abd-query-practice-sources**); legacy summary-only tables are not enough.
- **`SKILL.md`** — may be missing or still full of **`{{PLACEHOLDER}}`** until you finish authoring; if it is missing, start from **`templates/SKILL_template.md`** in this skill (see **Build**, item 1).

## Core concepts (for the target package)

### Practice skill

A **practice skill** is the packaged method—the artifact readers open when they want to perform this practice. It should let a person or agent follow the method **without inventing steps** and recognize **when** this practice is the right tool. Open with purpose and fit, then carry the method through procedures, examples, promised outputs when the practice has them, and a clear validation mindset. Keep mechanics and file paths out of that opening voice; they belong in later parts of the same document. **Purpose** on the target page should be **one** short paragraph about **why** the practice exists and what it helps people do, not a runbook for paths and tooling (see rule **Opening sections give outcomes not package mechanics** in `rules/`).

### Rules

**Normative rules** exist so the practice does not dissolve into taste and improvisation. They answer: *would we accept this concrete output as "good enough" for this method?* Without that shared bar, every run of an agent (or every reviewer) reinvents quality, outputs stop being comparable, and the package quietly drifts away from what the sources actually support. Rules are how you make **quality legible** and **repeatable**.

**Build** in **`SKILL.md`** carries **step order** and the main teaching voice. **Rules** under **`rules/*.md`** judge **real artifacts** — a filled template, a section of a file, a pattern in text — with explicit **pass** and **fail**. Same package, two jobs: **Build** walks the method; **rules** say whether the outputs meet the bar.

Each rule should read like a **small spec**: what must hold for **pass**, what counts as **fail**, with enough concrete examples that nobody has to guess. Hub-backed lines trace to **`inputs/abd-answers-retrieval.md`** when provenance matters. The full shape is in `rules/target-rule-files-are-checkable-specs-for-named-artifacts.md`; per-bullet examples are required by `rules/rule-dos-and-donts-must-each-have-examples.md`.

**Where it shows up on disk:** the **target** practice keeps those checks in **`rules/*.md`** and concept/example teaching in **`reference/*.md`**. The **`rules/*.md`** that ship **inside this authoring skill** must stay **practice-agnostic**; anything that only fits one method belongs under **`skills/<that-practice>/rules/`** and that practice's **`templates/`**, not here.

### Template

A **template** is a fixed output shape the practice promises—usually a file under **`templates/`**—that practitioners complete when they apply the method. It should make deliverables **comparable**, **complete**, and **easy to find**, and the skill should name every template shape it expects without ambiguity. When the skill names a template, either ship that file (filled or sensibly minimal), defer it in the skill text with a stated reason, or remove it from what the skill promises so scope stays honest. The starter **`SKILL_template.md`** in **abd-author-practice-skill** is a **parameterized seed**: it keeps **`{{PLACEHOLDER}}`** slots until you replace them and includes a short **filled example** (fictional practice) for tone; delete that example section from the copied **`SKILL.md`** once the real opening is written.

### Sections and rules

**`SKILL.md`** carries **teaching and workflow order** — it is a **thin router**: purpose, when-to-use, output resolution, and the read-gates that drive generate and validate. **`rules/*.md`** are the **check layer** on real artifacts: pass/fail on outputs (phrasing, shape, trace, assumptions, and the like). **`reference/*.md`** hold concept teaching, examples, and heuristics — they are loaded on demand, not inlined. **Build** sequences the work; **rules** define acceptable output. The same split appears in skills such as **abd-story-mapping** and **abd-story-specification**.

## Build

Work on **one** practice under **`skills/<skill-name>/`**. The **quality bar** for that package is in this skill's **`rules/`** — read every file there before starting and before validating. Follow these items **in order**.

When you **maintain `abd-author-practice-skill`**, keep its **`rules/`** generic for **any** practice; move or add method-specific checks only on the **target** skill under **`skills/<skill-name>/`** (see **Core concepts**, **Rules**).

1. **Create a starter skill page when the target has none yet.** If **`SKILL.md`** is not there, copy **`templates/SKILL_template.md`** from **abd-author-practice-skill** into the target folder, create empty **`rules/`**, **`reference/`**, **`templates/`**, and **`ide-files/`**, and set the YAML **`name`** and **`description`**. The file you copy is a **skeleton plus one filled example block** (fictional practice) for tone; remove that example section after your real **Purpose** and **When to use** are in place. Immediately after the frontmatter, add the **Manual:** line that points at **`./manual/index.html`**. Also scaffold **`ide-files/`** and the deployable IDE files there (see step 8). If **`SKILL.md`** already exists, skip this step.

2. **Read this skill's `rules/*.md` as the contract for the target.** Every file in `rules/` defines what "done" means for how the **target** practice should read and how its **`rules/*.md`** should behave. Read them all now. Also read **`reference/`** for concept guidance.

3. **Map hub evidence to the right parts of the target skill page.** Use the **Relevance** tag on each **Kept chunk** in **`inputs/abd-answers-retrieval.md`**: treat **`core_concept`** and **`glossary`** chunks as fuel for opening sections and **`reference/`** files; **`procedure`** and **`rule`** for how-to and **Validate**-style checks; **`example`** for examples and template hints; **`diagram_ref`** for manual or figure notes. Do not add **`scanners/*.py`** in this pass.

4. **Rewrite the target `SKILL.md` as a thin router.** Replace placeholder voice with plain **Purpose** and **When to use**, then the Agent Instructions block with explicit read-gates, then the Validate section. Move concept teaching and examples to **`reference/*.md`** — they do not belong in the SKILL body. Where you claim something is hub-backed, cite retrieval row and source when that helps a reviewer. Either fill every **`{{PLACEHOLDER}}`**, defer it in writing with a reason, or narrow what the skill promises.

5. **Author `rules/*.md` on the target as output validators.** Each file targets a **named artifact**; every **DO** must be **decidable** from that artifact without extra context. Keep **step order** in **Build** in **`SKILL.md`**, not in rules. Every normative file needs **`## DO`**, **`## DO NOT`**, per-bullet **Example (pass)** / **Example (fail)**, plus enough condition text to mark pass vs fail. Point **`Source:`** at **`inputs/abd-answers-retrieval.md`** only for **hub-backed** lines; do not fake hub sources for chat-only norms. Add **`scanner:`** in front matter only if **`scanners/<stem>-scanner.py`** already exists on that package.

6. **Confirm `SKILL.md` is a thin router — no rule or concept prose inlined.** Rules live only in **`rules/*.md`**; concept and example prose lives only in **`reference/*.md`**. **`SKILL.md`** must contain no `<!-- execute_rules:bundle_rules -->` markers and no inlined rule or concept text. Verify the Agent Instructions block contains explicit read-gates for **`rules/`** and **`reference/`** (MANDATORY before generating and before validating), and that the Validate section requires a per-rule verdict.

7. **Inspect the package instead of rewriting it from scratch.** Walk the **Validate** checklist in this file against the **target** folder, fix drift and weak spots, and stop when a careful reviewer would accept the package—unless new evidence forces a larger rewrite.

8. **Create IDE files only when the skill enforces a real always-on behavioral constraint.** IDE files are **not** required for every skill — skills are discovered contextually through the agent skills system. Do **not** create a `.mdc` that just says "read skill X when the user asks for Y"; that is noise, not a constraint.

   Only create **`ide-files/`** when the skill enforces a **non-negotiable behavioral guard** that must hold in every conversation regardless of context (a quality gate, a process invariant, a "never do X" rule). When that bar is met:

   - **`ide-files/<skill-name>.mdc`** — Cursor rule. YAML frontmatter with `description:` and `alwaysApply: true`; body states the constraint in DO / DO NOT terms.
   - **`ide-files/<skill-name>.instructions.md`** — VS Code parity: the **exact same markdown body** as the `.mdc` (everything after the closing `---`) with **no** YAML header. The **`mdc-instructions-parity`** scanner fails if they drift.

   **Do not create a `.prompt.md`** by default. Slash commands are for workflows a practitioner explicitly invokes — only add one when there is a clear user-facing invocation reason.

9. **Deploy the skill outputs to the target project.** Run **`Deploy-SkillOutputs.ps1`** from this skill's `scripts/` to link the authored skill's IDE files into the target project:

   ```powershell
   .\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/<skill-name> -ProjectRoot <target-project> -Force
   ```

   `-IDE` defaults to **`Cursor`** (`.mdc` → **`.cursor/rules/`**, `.prompt.md` → **`.cursor/commands/`**, plus the **`~/.cursor/skills/`** junction). Add **`-IDE Both`** when **`<target-project>`** should also get **`.vscode/`** and **`.github/prompts/`**.

10. **Check `.mdc` / `.instructions.md` parity on the target.** From the **agilebydesign-skills** repo root, run **`run_scanners.py`** with **`--skill-root`** pointing at **this authoring skill** and **`--workspace`** as an **absolute** path to the target skill root (relative paths resolve against the authoring skill folder and will not work):

   ```bash
   python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
     --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill \
     --workspace /absolute/path/to/agilebydesign-skills/skills/<skill-name>
   ```

### Quick reference

- **Target root:** **`agilebydesign-skills/skills/<skill-name>/`**
- **Starter template:** **`skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md`**
- **Terse order:** seed **`SKILL.md`** if needed; read all `rules/*.md` and `reference/` files; map retrieval by relevance; fill **`SKILL.md`** as a thin router; write **`rules/*.md`**; move concept/example prose to **`reference/*.md`**; run **Validate** checklist.

## Validate

**Goal:** Inspect the **target** package as a reviewer. Read every file in `rules/` for this skill before running this checklist.

Checklist for the **target** **`skills/<skill-name>/`**:

- **Readable English** — **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, and the rest of the target **`SKILL.md`** use **clear, grammatical prose** for humans, not only a polished opening followed by rough notes; paths and commands appear where expected, with enough sentence context that the page teaches the method (see `rules/clear-english-throughout-skill-page.md`).
- **Purpose is outcome not mechanics** — **Purpose** is **one** short paragraph about **why** the practice exists and what it helps people do; opening blocks do **not** front-load paths, markers, template-copy steps, or pipeline detail before that outcome is clear (see `rules/opening-sections-give-outcomes-not-package-mechanics.md`).
- **Concepts before notation** — **Core concepts** explain **ideas and relationships** first; diagram symbols, file prefix serialisation, and template positioning live in **templates**, **Agent Instructions**, **Build**, **Validate**, and **`rules/*.md`** (see `rules/core-sections-teach-ideas-before-file-prefixes-and-diagram-notation.md`).
- **YAML** — **`description`** is a **one-line outcome**, not a repeat of the file pipeline.
- **Placeholders** — no **`{{PLACEHOLDER}}`** unless the engagement **explicitly** defers that slice.
- **Evidence** — what you call **hub-backed** ties to **`inputs/abd-answers-retrieval.md`**; chat/engagement norms are not forced to; gaps are **documented**, not invented.
- **Templates** — every file the **target** **SKILL.md** promises under **`templates/`** is **filled**, **stubbed with a stated reason**, or **removed from the promise**; each promised template includes **at least one audience-appropriate filled example** (see `rules/templates-include-ideal-filled-examples-for-the-audience.md`).
- **Rule file shape** — target **`rules/*.md`** are checkable specs for named artifacts (decidable **DO** / **DO NOT**, per-bullet examples, **Source** when hub-backed); **Build** in **`SKILL.md`** remains the step-order doc (see `rules/target-rule-files-are-checkable-specs-for-named-artifacts.md`).
- **Rules are external, not inlined** — **`rules/*.md`** match **execute-skill-using-skills-rules** shape; **`SKILL.md`** contains **no** `<!-- execute_rules:bundle_rules -->` markers and no inlined rule prose; **`scanner:`** only where the script exists (see `rules/skill-md-contains-no-inlined-rules-read-gates-reference-rules-and-reference.md`).
- **Thin router shape** — **`SKILL.md`** Agent Instructions block contains explicit read-gates: MANDATORY read of every **`rules/`** file before generating, MANDATORY read of every **`reference/`** file before authoring, MANDATORY per-rule verdict at validation; concept teaching and examples live in **`reference/*.md`**, not in **`SKILL.md`** body.
- **Teaching is positive, anti-patterns live in rules** — the target **`SKILL.md`** does **not** have "Anti-patterns," "Common mistakes," or "What this is not" sections; negatives are **`## DO NOT`** bullets in **`rules/*.md`** (see `rules/anti-patterns-belong-in-rules-not-skill-teaching.md`).
- **Validate section** — the **target** **SKILL.md** **Validate** list matches what that skill **actually** ships (templates, scanners, citations, read-gates).
- **Per-rule verdict** — when validating the target, enumerate every rule in **`rules/`** and emit `Rule: <name> -> PASS` or `Rule: <name> -> FAIL <reason>`. No silent skips.

---
