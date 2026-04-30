<!--
  Parameterized SKILL.md skeleton for agilebydesign-skills.
  Copy to skills/<your-skill>/SKILL.md and replace every {{PLACEHOLDER}}.
  Based on: skills/abd-story-mapping/SKILL.md, skills/abd-acceptance-criteria/SKILL.md
  Same section order and H2 headings as those skills; "Steps" is **Agent Instructions** here.
-->

---
name: {{SKILL_NAME}}
description: >-
  {{SKILL_DESCRIPTION}}
---
# {{SKILL_DISPLAY_NAME}}

## Purpose: {{SKILL_PURPOSE_LINE}}

## When to use this skill

Load this skill when **any** of the following apply:

- {{WHEN_TO_USE_BULLET_1}}
- {{WHEN_TO_USE_BULLET_2}}
- {{WHEN_TO_USE_BULLET_3}}
- {{WHEN_TO_USE_BULLET_4}}

---
## Agent Instructions

1. **Templates**
 Generate content using **every** template file in this skill’s `templates/` folder.
**Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

| Template | What to produce |
| --- | --- |
| {{TEMPLATE_ROW_1}} | {{TEMPLATE_ROW_1_DESC}} |
| {{TEMPLATE_ROW_2}} | {{TEMPLATE_ROW_2_DESC}} |

**Consistency:** {{CONSISTENCY_BETWEEN_TEMPLATES}}

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

When you **create or rewrite** {SKILL_OUTPUT_ARTIFACTS}, you **must** deliver **one output artifact per file** in `templates/`. 

2. **Rules**
- Generate content following rules attached to this skill, listed below, assembled from rule files in `rules/`.
- Validate - once content is generated, take on the role of a *Peer Reviewer*  and validate that the content is correct by going through each of the skills rules one at a time and looking deeply for violations. Be helpful but critccal - compare contenct againstg each rules constraints, DO/DON’T sections and examples.

- **Who is checking:** {{WHO_IS_CHECKING}}{{WHAT ARE_THEY_CHECKING_FOR}},  {{WHO_IS_CHECKIN_2}}{{WHAT ARE_THEY_CHECKING_FOR_2}}, ...

3. **Assembling this Skill**
This Skill file is  assembled from all template files  `templates/` and all rules in `rules/`. Use **`bundle_rules_into_skill_md.py`** to reassemble this skill. When ever rules or templates change.


---



## What is a {{SKILL_FOCUS}}

{{SKILL_FOCUS_INTRO_PARAGRAPHS}}

{{SKILL_FOCUS_BULLETS}}

---

## Core concepts

{{CORE_CONCEPTS_SECTIONS}}

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

**Goal:** Author the outputs — turn sources into every artifact this skill’s templates define (see **Use every template file**).

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

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root <this-skill-dir>
-->
<!-- execute_rules:bundle_rules:end -->