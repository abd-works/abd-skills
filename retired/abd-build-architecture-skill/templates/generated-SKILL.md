<!--
  Template: SKILL.md for an ARCHITECTURE IMPLEMENTATION SKILL.
  This file is the OUTPUT of abd-build-architecture-skill: a skill that
  generates code in a specific architecture. The shape below is the full
  contract for what such a skill must contain.

  Replace every {{PLACEHOLDER}} from the architecture-reference.md the
  generated skill was built from. Delete this comment block before shipping.
  Keep the bundled-rules markers at the bottom; the bundling script
  populates them from rules/*.md.
-->

---
name: {{ARCH_NAME}}-technical-architecture
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  {{ARCH_ONE_LINER}}
description: >-
  Generate production {{ARCH_NAME}} ({{ARCH_TECH_SUMMARY}}) modules using
  the architecture defined in `inputs/architecture-reference.md`. Code is
  organized {{ARCH_ORGANIZATION_SUMMARY}}, with the principles and
  patterns the reference fixes for each mechanism. This skill covers the
  full structure: {{LAYER_LIST_INLINE}}, plus mechanism-specific patterns
  for {{MECHANISM_LIST_INLINE}}. Use it when scaffolding a new
  {{ARCH_NAME}} project, adding a domain module, reviewing architecture
  compliance, or transforming a technically-organized codebase into the
  shape this reference prescribes. Produces module output from templates
  and validates against rule files traced back to the reference.
---

# {{ARCH_NAME}}-technical-architecture

## Purpose

Generate production {{ARCH_NAME}} modules using the **architecture fixed in `inputs/architecture-reference.md`** — organizing by {{ORGANIZING_PRINCIPLE}}, enforcing {{LAYER_PURITY_DESCRIPTION}}, and following the mechanism patterns the reference names for {{MECHANISM_LIST_INLINE}}.

This skill produces real, runnable modules. The output follows the architecture defined in [`inputs/architecture-reference.md`](inputs/architecture-reference.md): {{ONE_PARAGRAPH_TYING_LAYERS_TO_FILES}}.

## When to use this skill

Load this skill when **any** of the following apply:

- You are **scaffolding a new {{ARCH_NAME}} project** and need the architecture-prescribed folder structure.
- You are **adding a new module** to an existing {{ARCH_NAME}} project.
- You are **reviewing compliance** against the reference's principles and patterns.
- You are **transforming** an existing codebase into the shape this reference prescribes.
- You are **implementing one mechanism** (e.g. caching, error handling) on top of an existing module.

---

## Agent Instructions

1. **Read the reference first.** Load [`inputs/architecture-reference.md`](inputs/architecture-reference.md) to understand the authoritative architecture: layers, principles, patterns, file structure, participants, flow, walkthrough, testing.

2. **Templates.** Generate content using **every** template file in this skill's `templates/` folder.

   | Template | What to produce |
   | --- | --- |
   | `{{TEMPLATE_1_PATH}}` | {{TEMPLATE_1_DESCRIPTION}} |
   | `{{TEMPLATE_2_PATH}}` | {{TEMPLATE_2_DESCRIPTION}} |

3. **Rules.** Generate content following the rules attached to this skill, listed below. After writing, take on the role of a *Peer Reviewer* and walk each rule's `DO` / `DO NOT` / Examples against the generated code.

4. **Coding and testing standards.** Code generated under this skill follows the project's coding standard ({{CODING_STANDARD_IN_SCOPE}} — typically `abd-clean-code` in an agilebydesign-skills-anchored project: domain language, small functions, constructor injection, no anemic data bags). Test code follows the project's testing standard ({{TESTING_STANDARD_IN_SCOPE}} — typically `abd-acceptance-test-driven-development`: class per story, Given/When/Then helpers, no defensive checks). Do not re-define those rules here — cite them by name.

5. **Scanners.** {{SCANNER_INSTRUCTIONS_OR_NONE_YET}}

6. **Compilation verification.** {{COMPILE_VERIFY_OR_RUN_TESTS_INSTRUCTIONS}}

7. **Assembling this skill.** Reassemble with `bundle_rules_into_skill_md.py` after editing `rules/` or `templates/`.

---

## What is {{ARCH_NAME}}?

{{ONE_PARAGRAPH_ARCH_SUMMARY}}

The architecture is guided by {{N}} principles:

- **{{Principle1}}** — {{gloss}}.
- **{{Principle2}}** — {{gloss}}.
- **{{Principle3}}** — {{gloss}}.
- **{{Principle4}}** — {{gloss}}.

---

## Core concepts

### Layers

| Layer | Tech | Location | Responsibility |
|-------|------|----------|----------------|
| **{{Layer1}}** | {{tech}} | `{{path}}` | {{role}} |
| **{{Layer2}}** | {{tech}} | `{{path}}` | {{role}} |
| **{{Layer3}}** | {{tech}} | `{{path}}` | {{role}} |
| **{{Layer4}}** | {{tech}} | `{{path}}` | {{role}} |

### Mechanisms covered

| Mechanism | Principle | Pattern |
|---|---|---|
| **{{Mechanism1}}** | {{principle line}} | {{pattern name}} |
| **{{Mechanism2}}** | {{principle line}} | {{pattern name}} |
| **{{Mechanism3}}** | {{principle line}} | {{pattern name}} |

(See the matching section in `inputs/architecture-reference.md` for the full participants, flow, walkthrough, and tests.)

---

## Example

**Domain: {{ExampleDomain}}** (drawn from the reference's walkthrough).

```{{language}}
{{ONE_FILLED_MINI_MODULE}}
```

---

## The shape of a {{ARCH_NAME}} module

```
{{FOLDER_TREE_FROM_REFERENCE_FILE_STRUCTURE_BLOCK}}
```

Key structural rules (lifted from the reference's principles):

- {{Rule1}}
- {{Rule2}}
- {{Rule3}}

---

## Build

**Goal:** Author one module that obeys every mechanism principle in the reference.

- **Outputs:** {{OUTPUTS_DESCRIPTION}}.
- **Per format:** {{PER_FORMAT_DESCRIPTION}}.
- **While writing:** {{WHILE_WRITING_DESCRIPTION}}.

**Build steps:**

1. Identify the domain entity / capability from the story or requirements.
2. {{BUILD_STEP_2_TIED_TO_FIRST_LAYER}}.
3. {{BUILD_STEP_3_TIED_TO_NEXT_LAYER}}.
4. {{BUILD_STEP_4_FOR_EACH_MECHANISM_THE_MODULE_TOUCHES}}.
5. Add tests at the tiers the reference's **Testing the mechanism** subsections require.
6. Run scanners (if present) and bundle rules.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers, not a second authoring pass.

- **Who is checking:** Software Architect (layer purity, dependency direction), Domain Expert (Domain Language), Tech Lead (interfaces fully implemented), QA Lead (test structure).
- **Cross-artifact parity:** Same domain entities used identically by every layer; same schemas validate at every boundary; same collection methods produce the same results regardless of tier.

**Validation checklist:**

- {{CHECKLIST_1}}
- {{CHECKLIST_2}}
- {{CHECKLIST_3}}
- {{CHECKLIST_4}}
- {{CHECKLIST_5}}

---

<!-- execute_rules:bundle_rules:begin -->
<!-- execute_rules:bundle_rules:end -->
