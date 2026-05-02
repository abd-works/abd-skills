<!--
  Parameterized SKILL.md skeleton for agilebydesign-skills.
  Canonical copy: agents/abd-practice-skill-builder/skills/abd-author-practice-skill/templates/SKILL_template.md
  Copy to skills/<your-skill>/SKILL.md and replace every {{PLACEHOLDER}}.
  Suggested order: Purpose, When to use, teaching front-matter, Core concepts, Example, Build, Validate, bundled-rules trailer (`execute_rules` markers).
-->

---
name: {{SKILL_NAME}}
description: >-
  {{SKILL_DESCRIPTION}}
---
# {{SKILL_DISPLAY_NAME}}

## Purpose

{{SKILL_PURPOSE_ONE_PARAGRAPH}}

**Authoring note:** Write **one** paragraph only — **why** this packaged practice exists, **who** it helps, **what** becomes possible when the method is used well, and **how** this page supports that — in plain language. Do **not** put repository paths, **`Manual:`**, **`execute_rules`** HTML markers (`execute_rules:bundle_rules`), which template to copy, hub retrieval filenames, bundle commands, scanner wiring, or other **package / agent mechanics** here; those belong in **Prerequisites** and **Build**. When you use **abd-author-practice-skill** to finish the page, the bundled rule **Opening sections give outcomes not package mechanics** states the same bar.

---

## Example: how the opening can read (fictional practice)

**For authors only:** Mirror this for **tone and depth**, then **delete this whole section** from the **`SKILL.md`** you ship so practitioners see one real practice, not a sample.

### Purpose (illustrative — replace `{{SKILL_PURPOSE_ONE_PARAGRAPH}}`)

Release train planning helps teams sequence work across fixed dates so dependencies and scope stay honest before anyone commits. This skill packages that facilitation pattern so product owners and delivery leads can run the same conversations (with or without an agent) and leave with a comparable, board-ready plan.

### When to use this skill (illustrative — replace the bullets under `{{WHEN_TO_USE_BULLET_*}}`)

Load this skill when **any** of the following apply:

- You have a backlog slice and need to **map it to calendar milestones** without hiding risk.
- Stakeholders are **trading scope for date** and need a **single shared picture** of what can ship when.
- You are **standing up a release train** and want **one** method page instead of ad hoc slide decks.

---

## When to use this skill

Load this skill when **any** of the following apply:

- {{WHEN_TO_USE_BULLET_1}}
- {{WHEN_TO_USE_BULLET_2}}
- {{WHEN_TO_USE_BULLET_3}}
- {{WHEN_TO_USE_BULLET_4}}

## What is a {{SKILL_FOCUS}}

{{SKILL_FOCUS_INTRO_PARAGRAPHS}}

{{SKILL_FOCUS_BULLETS}}

---

## Core concepts

### Practice skill

A **practice skill** is the packaged method—the artifact readers open when they want to perform this practice. It should let a person or agent follow the method **without inventing steps** and recognize **when** this practice is the right tool. Open with purpose and fit, then carry the method through procedures, examples, promised outputs when the practice has them, and a clear validation mindset. Keep mechanics, file paths, and agent-or-package runbooks out of **Purpose** and the first teaching screens; they belong in **Prerequisites**, **Build**, and **Validate**.

### Rules

**`rules/*.md`** **validate outputs** (generated or filled artifacts): pass/fail, not **order of operations**. Each normative rule file should include **`## DO`**, **`## DO NOT`**, **`## Examples`**, enough text to decide true vs false, and **hub** **`Source:`** when enforcing corpus content. Workflow order lives in **Build** in **`SKILL.md`**.

### Template

A **template** is a fixed output shape the practice promises—usually a file under **`templates/`**—that practitioners complete when they apply the method. It should make deliverables **comparable**, **complete**, and **easy to find**, and the skill should name every template shape it expects without ambiguity. When the skill names a template, either ship that file (filled or sensibly minimal), defer it in the skill text with a stated reason, or remove it from what the skill promises so scope stays honest.

### Sections and rules

**`SKILL.md`** carries **teaching and workflow order**. **`rules/*.md`** carry **validators** for outputs (grouped by concern, not one file per heading).

---

## Example
{{GENERATED_EXAMPLE}}

## The shape of {{GOOD_ARTIFACT_PHRASE}}

```
{{EXAMPLE_BLOCK}}
```

{{SHAPE_NOTES_BELOW_EXAMPLE}}

---

## Build

**Goal:** Carry out the practice in order — author every artifact this skill's templates define, apply bundled rules, and keep the **`rules/`** bundle in sync with disk. Write numbered items in **full sentences** (readable on their own) while naming real folders, files, and commands where they matter.

1. **Produce outputs from every template.** Generate content using **every** file in this skill's **`templates/`** folder. Do **not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format. Use the table below to know what each template is for; keep paired formats consistent.

| Template | What to produce |
| --- | --- |
| {{TEMPLATE_ROW_1}} | {{TEMPLATE_ROW_1_DESC}} |
| {{TEMPLATE_ROW_2}} | {{TEMPLATE_ROW_2_DESC}} |

When you **create or rewrite** {{SKILL_OUTPUT_ARTIFACTS}}, deliver **one output artifact per file** in **`templates/`**. If new files appear under **`templates/`** later, produce a matching artifact for **each** one the same way. **Consistency:** {{CONSISTENCY_BETWEEN_TEMPLATES}}

2. **Apply the rules, then review like a peer.** Follow the normative **`rules/`** prose that is bundled at the end of this **`SKILL.md`**. After you generate content, act as a **peer reviewer**: walk each rule file in turn, read its **DO** and **DO NOT** and **Examples**, and look for concrete violations. Be strict but fair—compare real output against what the rule says, not against what you wish it said.

3. **Keep the bundled rules block honest.** This **`SKILL.md`** includes rules inlined from **`rules/*.md`**. Whenever you change a file under **`rules/`**, run **`bundle_rules_into_skill_md.py`** from the **agilebydesign-skills** repo so the HTML-comment bundle at the bottom of this file matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/<this-skill-folder>
```

{{BUILD_EXTRA_NUMBERED_ITEMS_OR_DELETE_THIS_LINE}}

- **Outputs:** {{BUILD_OUTPUTS_LINE}} Deliver one file per template unless the user explicitly asked for a single format.
- **Per format:** {{BUILD_PER_FORMAT_LINE}} What each output file must contain (e.g. Markdown sections vs plain text) — skill-specific.
- **While writing:** {{BUILD_WHILE_WRITING_LINE}} Naming, parity across paired files if you emit more than one, and depth — tie to **Core concepts** and **The shape of** above.
- **Persistence (optional):** {{BUILD_PERSISTENCE_OR_OMIT}} e.g. `story-graph.json` / workspace conventions. Use *N/A* or delete this bullet if this skill is files-only.

{{BUILD_SECTION_BODY}}

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers, not a second authoring pass.

- **Who is checking:** {{VALIDATE_WHO_LINE}} Name the perspectives (e.g. product owner, developer, domain expert) and what each one verifies for *this* skill.
- **Cross-artifact parity (if multiple outputs):** {{VALIDATE_PARITY_LINE}} Same tree or semantics across paired formats. Use *N/A* or delete if this skill emits a single file.

{{VALIDATE_CHECKLIST_INTRO}}

- {{VALIDATE_BULLET_1}}
- {{VALIDATE_BULLET_2}}
- {{VALIDATE_BULLET_3}}

{{VALIDATE_CLOSING_PARAGRAPH}}

---

## Deploy

This skill ships IDE-deployable files under **`ide-files/`**. Deploy them to any project:

```powershell
.\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/{{SKILL_FOLDER_NAME}} -ProjectRoot <target-project> -Force
```

Default **`-IDE Cursor`**. Use **`-IDE Both`** when the target project should also receive **`.vscode/*.instructions.md`** and **`.github/prompts/*.prompt.md`**.

| File | Deploy target |
| --- | --- |
| `ide-files/{{SKILL_NAME}}.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/{{SKILL_NAME}}.instructions.md` | `.vscode/` when deploy uses **`-IDE Both`** (VS Code — **same body** as `.mdc` after frontmatter; see **mdc-instructions-parity** rule in **abd-author-practice-skill**) |
| `ide-files/{{SKILL_NAME}}.prompt.md` | `.cursor/commands/` (always); also `.github/prompts/` when deploy uses **`-IDE Both`** |

After editing `.mdc` or `.instructions.md`, validate parity (use an **absolute** `--workspace` path):

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root agents/abd-practice-skill-builder/skills/abd-author-practice-skill \
  --workspace /absolute/path/to/repo/skills/{{SKILL_FOLDER_NAME}}
```

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root <this-skill-dir>
-->
<!-- execute_rules:bundle_rules:end -->
