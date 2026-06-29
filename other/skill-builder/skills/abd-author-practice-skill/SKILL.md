---
name: abd-author-practice-skill
description: >-
  Turn collected hub evidence into a finished practice skill with clear instructions and checkable do-and-don't norms. Use when hub material has been gathered and you want to produce a skill package that reads clearly and can be validated.
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

### Practice-level reference folder

Practice skills belong to a **practice family** — a named folder under `practices/<family-name>/` that holds multiple skills. The family has its own `reference/` folder at that level (not inside any individual skill) for two shared artifacts every skill in the family can link to instead of repeating:

**`reference/<family>-perspective.md`** — the fidelity ladder for this practice: which skill maps to which fidelity level and mode. This is the single authoritative picture of how the practice progresses from shaping to engineering. Every skill in the family has `context-perspective` and `context-fidelity` in its front matter; the perspective file is the readable version.

```markdown
# BDD Perspective

**Key:** `engineering`

**What it answers:** How is behavior discovered, structured, and implemented as tested code?

**Skills by fidelity:**

| Fidelity    | Skill                  | Mode           |
|-------------|------------------------|----------------|
| Exploration | `abd-bdd-behavior`     | bdd-scaffold   |
| Spec        | `abd-bdd-specification`| bdd-signature  |
| Engineering | `abd-bdd-development`  | bdd-development|
```

**Shared cross-skill reference files** — concepts, vocabulary, or rules that more than one skill in the family needs but that don't belong inside a single skill. For example: OO concepts shared across all DDD skills live in `practices/domain-driven-design/reference/oo-concepts.md`; incomplete-context handling shared across all story-driven skills lives in `practices/story-driven-delivery/reference/handling-incomplete-context.md`. Skills `reference/concepts.md` links to the practice-level file rather than duplicating the content.

See rule **Practice level reference folder has perspective and shared concepts** in `rules/`.

### Input traps

Every practice skill that produces artifacts from ambiguous input ships **`reference/input-traps.md`** — silent pre-flight in every run, not grill questions. Ship **`reference/grill-me.md`** separately for grill interview questions. [`common/reference/grill-me-with-practice-skill.md`](../../../../common/reference/grill-me-with-practice-skill.md) is mechanics only.

### Diagram workflow

Some practice skills produce **diagram outputs**. When a skill generates a diagram, the diagram is a **required deliverable** — the CDD cell is not done until the file exists on disk.

- **`reference/diagram-workflow.md`** on the skill — mode and output path for this skill; links to practice-level shared CLI when applicable.
- **Practice `reference/diagram-workflow.md`** — shared commands when multiple skills in the family use the same tooling (see `practices/story-driven-delivery/reference/diagram-workflow.md`).
- **`common/reference/skill-workflow.md`** § Diagram workflow — background sub-agent runs after scanner pass when `reference/diagram-workflow.md` exists.

Do **not** put `## Diagram workflow` in `SKILL.md`. See `abd-story-mapping/reference/diagram-workflow.md` for the thin skill-level pattern.

### Front matter — description

The `description` field in a skill's YAML front matter is two sentences:

1. **What it does** — a compact, present-tense verb phrase: what the skill produces and what that gives people.
2. **Use when** — starts with `Use when` and names a real-world situation the practitioner recognizes from their own work — the circumstances that make this skill the right tool.

The `Use when` sentence describes the **practitioner's situation**, never the name of another skill or the output artifact of another skill. A practitioner reading a catalog must be able to understand the trigger without knowing anything about the skill family. See rule **Description front matter has "Use when" in situation language** in `rules/`.

**Example (pass):**
```yaml
description: >-
  State exactly what must be true for a story to be done — so everyone agrees on 'finished'. Use when writing or reviewing exploration-phase behavior for stories.
```

**Example (fail):**
```yaml
description: >-
  Turn a BDD scaffold into an executable test skeleton with empty markers. Use when a scaffold has been approved.
```
"scaffold" is the output of another skill; a reader who hasn't run that skill doesn't know what it means.

### Sections and rules

**`SKILL.md`** carries **teaching and workflow order** — it is a **thin router**: purpose, when-to-use, output resolution, and the read-gates that drive generate and validate. **`rules/*.md`** are the **check layer** on real artifacts: pass/fail on outputs (phrasing, shape, trace, assumptions, and the like). **`reference/*.md`** hold concept teaching, examples, and heuristics — they are loaded on demand, not inlined. **Build** sequences the work; **rules** define acceptable output. The same split appears in skills such as **abd-story-mapping** and **abd-story-specification**.

## Build

Work on **one** practice under **`skills/<skill-name>/`**. The **quality bar** for that package is in this skill's **`rules/`** — read every file there before starting and before validating. Follow these items **in order**.

When you **maintain `abd-author-practice-skill`**, keep its **`rules/`** generic for **any** practice; move or add method-specific checks only on the **target** skill under **`skills/<skill-name>/`** (see **Core concepts**, **Rules**).

1. **Create a starter skill page when the target has none yet.** If **`SKILL.md`** is not there, copy **`templates/SKILL_template.md`** from **abd-author-practice-skill** into the target folder, create empty **`rules/`**, **`reference/`**, **`templates/`**, and **`ide-files/`**, and set the YAML **`name`** and **`description`**. The file you copy is a **skeleton plus one filled example block** (fictional practice) for tone; remove that example section after your real **Purpose** and **When to use** are in place. Immediately after the frontmatter, add the **Manual:** line that points at **`./manual/index.html`**. Also scaffold **`ide-files/`** and the deployable IDE files there (see step 8). If **`SKILL.md`** already exists, skip this step.

2. **Read this skill's `rules/*.md` as the contract for the target.** Every file in `rules/` defines what "done" means for how the **target** practice should read and how its **`rules/*.md`** should behave. Read them all now. Also read **`reference/`** for concept guidance.

3. **Map hub evidence to the right parts of the target skill page.** Use the **Relevance** tag on each **Kept chunk** in **`inputs/abd-answers-retrieval.md`**: treat **`core_concept`** and **`glossary`** chunks as fuel for opening sections and **`reference/`** files; **`procedure`** and **`rule`** for how-to and **Validate**-style checks; **`example`** for examples and template hints; **`diagram_ref`** for manual or figure notes. Do not add **`scanners/*.py`** in this pass.

4. **Rewrite the target `SKILL.md` as a thin router.** **Purpose**, **When to use**, and **Agent Instructions** (mandatory `common/reference/skill-workflow.md` read-gates only). Put orchestration in **`reference/generate.md`** when needed; put practice links in **`reference/concepts.md`**. No template tables, no `## Validate` section when the skill has `rules/` and scanners — validation is [`common/reference/rule-checklist.md`](../../../../common/reference/rule-checklist.md) (linked from `skill-workflow` § Validate output).

4a. **Create or verify the practice-level `reference/` folder.** Under `practices/<family-name>/reference/`, ensure two things exist:
   - **`<family>-perspective.md`** — the fidelity ladder table (fidelity, skill, mode) for this practice family. Create it if it does not exist; update it if a new skill has been added.
   - **Shared cross-skill concept files** — any concept or vocabulary that more than one skill in the family needs. If two or more skills would duplicate the same concept prose, extract it here and have each skill's `reference/concepts.md` link to it instead (see rule **Practice level reference folder has perspective and shared concepts**).

4b. **Set the front matter `description` correctly.** Two sentences: first says what the skill produces (compact, present tense); second starts with `Use when` and names the practitioner's situation in plain language. The `Use when` clause must describe circumstances the practitioner recognizes from their own work — never the name of another skill or that skill's output artifact (see rule **Description front matter has "Use when" in situation language**).

4c. **Write `reference/input-traps.md`.** At least three bold-labeled traps — pre-flight only, not grill questions (see rule **Input traps reference surfaces input ambiguities**).

4g. **Write `reference/grill-me.md`.** At least three interview questions for grill mode — separate from input traps (see rule **Grill me reference holds interview questions**). Link mechanics to `common/reference/grill-me-with-practice-skill.md` inside that file, not in `SKILL.md`.

4d. **Ask whether this skill produces diagram outputs.** If yes: add **`reference/diagram-workflow.md`** with mode and output path; put shared CLI in practice `reference/diagram-workflow.md` when multiple skills share tooling. Do not add `## Diagram workflow` or a Read context file list to `SKILL.md` — read-gates are in `common/reference/skill-workflow.md`.

4e. **Register output in `folder-conventions.md`; add `reference/output.md` only when non-default.** Look up or add the canonical path and file name for this skill in [`common/reference/folder-conventions.md`](../../../../common/reference/folder-conventions.md). Do **not** add a `## Output file` section to `SKILL.md` — [`common/reference/skill-workflow.md`](../../../../common/reference/skill-workflow.md) § Output file resolution handles folder and file name (check `reference/output.md` if present; otherwise use `folder-conventions.md`). Add `reference/output.md` only when the skill breaks the default (e.g. tests in the project tree, multiple named outputs, non-`.md` deliverable).

5. **Author `rules/*.md` on the target as output validators.** Each file targets a **named artifact**; every **DO** must be **decidable** from that artifact without extra context. Keep **step order** in **Build** in **`SKILL.md`**, not in rules. Every normative file needs **`## DO`**, **`## DO NOT`**, per-bullet **Example (pass)** / **Example (fail)**, plus enough condition text to mark pass vs fail. Point **`Source:`** at **`inputs/abd-answers-retrieval.md`** only for **hub-backed** lines; do not fake hub sources for chat-only norms. Add **`scanner:`** in front matter only if **`scanners/<stem>-scanner.py`** already exists on that package.

4f. **Add `reference/generate.md` only when orchestration is non-obvious** — fidelity branching, cross-skill pipeline order, pre-scanner sequencing, diagnose flip. Do **not** restate rules or template shape. Skip the file when `rules/` + `templates/` are enough (e.g. acceptance-criteria).

6. **Confirm `SKILL.md` is a thin router.** No `## Validate` when scanners exist; no § Generate template tables; orchestration in `reference/generate.md` if present.

7. **Inspect the package instead of rewriting it from scratch.** Walk the **Validate** checklist in this file against the **target** folder, fix drift and weak spots, and stop when a careful reviewer would accept the package—unless new evidence forces a larger rewrite.

8. **Create IDE files where they fit — instructions for always-on guards, prompts for explicit invocations.** Three distinct file types; each has a different bar:

   **`.mdc` + `.instructions.md` — always-on behavioral guards** (create these together):
   - Use when the skill enforces a **non-negotiable constraint that must hold in every conversation** regardless of context: a quality gate, a process invariant, a "never do X" rule. These fire automatically and cannot be turned off by the user.
   - Do **not** create these just to say "read skill X when the user asks for Y" — that is noise. The constraint must alter behavior unconditionally.
   - `ide-files/<skill-name>.mdc` — Cursor rule, YAML frontmatter `description:` + `alwaysApply: true`; body states the constraint in DO / DO NOT terms.
   - `ide-files/<skill-name>.instructions.md` — VS Code parity: **exact same markdown body** as the `.mdc` (everything after `---`) with no YAML header. The `mdc-instructions-parity` scanner fails if they drift.

   **`.prompt.md` — explicit practitioner invocations** (create when there is a clear slash-command use case):
   - Use when the skill has a workflow a practitioner **explicitly calls by name** — something they type as `/skill-name` to kick off a session. Not every skill needs this; don't create one just because the skill exists.
   - `ide-files/<skill-name>.prompt.md` — the prompt body the slash command executes. No YAML frontmatter beyond what the target IDE requires.

9. **Deploy the skill outputs to the target project.** Run **`Deploy-SkillOutputs.ps1`** from this skill's `scripts/` to link the authored skill's IDE files into the target project:

   ```powershell
   .\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/<skill-name> -ProjectRoot <target-project> -Force
   ```

   `-IDE` defaults to **`Cursor`** (`.mdc` → **`.cursor/rules/`**, `.prompt.md` → **`.cursor/commands/`**, plus the **`~/.cursor/skills/`** junction). Add **`-IDE Both`** when **`<target-project>`** should also get **`.vscode/`** and **`.github/prompts/`**.

10. **Check `.mdc` / `.instructions.md` parity on the target.** From the **agilebydesign-skills** repo root, run **`run_scanners.py`** with **`--skill-root`** pointing at **this authoring skill** and **`--workspace`** as an **absolute** path to the target skill root (relative paths resolve against the authoring skill folder and will not work):

   ```bash
   python skills/common/scripts/run_scanners.py \
     --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill \
     --workspace /absolute/path/to/agilebydesign-skills/skills/<skill-name>
   ```

### Quick reference

- **Target root:** **`agilebydesign-skills/skills/<skill-name>/`**
- **Starter template:** **`skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md`**
- **Scaffold + output paths:** **[`common/reference/folder-conventions.md`](../../../../common/reference/folder-conventions.md)** — canonical `docs/` subtree for every practice skill family. Add a new row if the skill is new. Output resolution lives in **[`common/reference/skill-workflow.md`](../../../../common/reference/skill-workflow.md)**; add **`reference/output.md`** on the skill only when it breaks the default.
- **Terse order:** seed **`SKILL.md`** if needed; read all `rules/*.md` and `reference/` files; map retrieval by relevance; fill **`SKILL.md`** as a thin router; write **`rules/*.md`**; move concept/example prose to **`reference/*.md`**; register output in `folder-conventions.md` (and `reference/output.md` if non-default); run **Validate** checklist.

## Validate

**Goal:** Inspect the **target** package as a reviewer. Read every file in `rules/` for this skill before running this checklist.

Checklist for the **target** **`skills/<skill-name>/`**:

- **Readable English** — **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, and the rest of the target **`SKILL.md`** use **clear, grammatical prose** for humans, not only a polished opening followed by rough notes; paths and commands appear where expected, with enough sentence context that the page teaches the method (see `rules/clear-english-throughout-skill-page.md`).
- **Purpose is outcome not mechanics** — **Purpose** is **one** short paragraph about **why** the practice exists and what it helps people do; opening blocks do **not** front-load paths, markers, template-copy steps, or pipeline detail before that outcome is clear (see `rules/opening-sections-give-outcomes-not-package-mechanics.md`).
- **Concepts before notation** — **Core concepts** explain **ideas and relationships** first; diagram symbols, file prefix serialisation, and template positioning live in **templates**, **Agent Instructions**, **Build**, **Validate**, and **`rules/*.md`** (see `rules/core-sections-teach-ideas-before-file-prefixes-and-diagram-notation.md`).
- **Practice-level reference folder** — `practices/<family-name>/reference/` exists and contains a `<family>-perspective.md` fidelity ladder; shared cross-skill concepts are in that folder rather than duplicated per skill (see `rules/practice-level-reference-folder-has-perspective-and-shared-concepts.md`).
- **YAML front matter** — **`description`** is two sentences: what the skill produces, then `Use when [situation]`. The `Use when` clause names the practitioner's circumstances in plain language — no other skill names, no other skill's output artifacts (see `rules/description-front-matter-has-use-when-in-situation-language.md`).
- **Input traps** — `reference/input-traps.md` exists with at least three method-specific bold-labeled traps (see `rules/grill-prompts-section-surfaces-input-traps.md`).
- **Grill me** — `reference/grill-me.md` exists with interview questions; `SKILL.md` § Grill me points there only (see `rules/grill-me-reference-holds-interview-questions.md`).
- **Placeholders** — no **`{{PLACEHOLDER}}`** unless the engagement **explicitly** defers that slice.
- **Evidence** — what you call **hub-backed** ties to **`inputs/abd-answers-retrieval.md`**; chat/engagement norms are not forced to; gaps are **documented**, not invented.
- **Templates** — every file the **target** **SKILL.md** promises under **`templates/`** is **filled**, **stubbed with a stated reason**, or **removed from the promise**; each promised template includes **at least one audience-appropriate filled example** (see `rules/templates-include-ideal-filled-examples-for-the-audience.md`).
- **Rule file shape** — target **`rules/*.md`** are checkable specs for named artifacts (decidable **DO** / **DO NOT**, per-bullet examples, **Source** when hub-backed); **Build** in **`SKILL.md`** remains the step-order doc (see `rules/target-rule-files-are-checkable-specs-for-named-artifacts.md`).
- **Rules are external, not inlined** — **`rules/*.md`** match **common** shape; **`SKILL.md`** contains **no** `<!-- execute_rules:bundle_rules -->` markers and no inlined rule prose; **`scanner:`** only where the script exists (see `rules/skill-md-contains-no-inlined-rules-read-gates-reference-rules-and-reference.md`).
- **Thin router shape** — **`SKILL.md`**: Purpose + mandatory `common/reference/skill-workflow.md` read-gates only; orchestration in **`reference/generate.md`**; **Validate** links [`common/reference/rule-checklist.md`](../../../../common/reference/rule-checklist.md) only.
- **Teaching is positive, anti-patterns live in rules** — the target **`SKILL.md`** does **not** have "Anti-patterns," "Common mistakes," or "What this is not" sections; negatives are **`## DO NOT`** bullets in **`rules/*.md`** (see `rules/anti-patterns-belong-in-rules-not-skill-teaching.md`).
- **Diagram workflow declared when needed** — if the skill produces `.drawio` or other diagram outputs, `reference/diagram-workflow.md` exists with mode and output path; practice shared CLI in practice `reference/` when applicable. `SKILL.md` has no `## Diagram workflow` section.
- **Validate section** — the **target** **`SKILL.md`** **`## Validate`** links only [`common/reference/rule-checklist.md`](../../../../common/reference/rule-checklist.md).
- **Per-rule verdict** — when validating the target, enumerate every rule in **`rules/`** and emit `Rule: <name> -> PASS` or `Rule: <name> -> FAIL <reason>`. No silent skips.

---
