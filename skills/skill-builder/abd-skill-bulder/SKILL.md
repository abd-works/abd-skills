---
name: abd-skill-bulder
description: Build a clear, checkable skill package from a simple local template-and-rules workflow.
---
# abd-skill-bulder

## Purpose

Create or refine a skill package so it is readable, actionable, and reviewable without extra tooling setup.

## When to use

- You need a new skill package quickly.
- A skill page exists but is inconsistent or unclear.
- You want a lightweight rule-and-bundle workflow with minimal structure.

## Core concepts

### Skill page

`SKILL.md` teaches the method: what the skill does, when to use it, and how to apply it.

### Rules

`rules/*.md` define checkable quality expectations with pass/fail examples.

### Templates

`templates/*.md` provide reusable starting structures for consistent authoring.

### Bundle

The bundle step inlines rule files into the `SKILL.md` bundle block so reviewers can read one assembled document.

## Build

1. Start from `templates/SKILL_template.md` when creating a new skill page.
2. Fill every placeholder with concrete, reader-focused guidance.
3. Add or refine `rules/*.md` so each rule is decidable from the artifact being reviewed.
4. Run the local bundler from this skill folder:

```bash
python scripts/bundle_rules_into_skill_md.py --skill-root .
```

## Validate

- `SKILL.md` is clear and complete in plain English.
- Every rule has `## DO`, `## DO NOT`, and pass/fail examples.
- Bundle block matches current `rules/*.md` content.
- No placeholder tokens remain unless explicitly deferred.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md -->
<!-- execute_rules:bundle_rules:end -->
