---
name: track-task
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Create a checkbox task list for any multi-step work and track progress through it.
description: >-
  Build a markdown checkbox list for any workflow, skill, or ad-hoc steps.
  Track what is done, what is next, and what is blocked — in any file the user chooses.
---

# Track Task

Use this skill when you need to track execution of multi-step work: what step are we on, mark this done, what's next, resume after a break.

## When to activate

- User says: *track this*, *checkpoint*, *what's next*, *mark step N done*, *track [X]*, *progress on …*
- You are about to run a multi-step process and want a persistent record of where you are.

## What to do

1. **Build the checklist** from the steps in scope — a skill's process, a user-described plan, or any numbered list. Each step becomes one `- [ ]` line.

2. **Ask where to save it** if the user hasn't said. Default: a `progress/` subfolder wherever the work output is going. Any path is fine.

3. **Each turn:**
   - Open the checklist file.
   - First unchecked `- [ ]` is "next" unless the user names a specific step.
   - After work completes, flip that line to `- [x]`.
   - Report: done / next / blocked.

4. **Never edit normative source files** (skill content, phase docs, rules). The checklist is session state only.

## Format

```markdown
## Progress: <task or skill name>

- [x] Step one — done
- [x] Step two — done
- [ ] Step three ← next
- [ ] Step four
- [ ] Step five
```

That is all this skill does.
