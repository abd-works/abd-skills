---
description: >-
  Add or change a single scenario step or AC item on an existing story.
  Runs 3 steps (test → code → run) or up to 5 when specs or domain model exist.
mode: agent
---

This is a **single-scenario-step change** on an existing story. Follow the steps below in order. Read each skill fully before acting. If the user provided text after the command, treat it as the story name, scenario step, or AC item to add or change.

**Before starting:** locate the existing story in the project's story graph or acceptance-criteria doc. Do not create a new story — stop and ask if none matches.

---

**If Spec by Example exists for this story → do step 1, skip step 2.**
**If only Acceptance Criteria exists → skip step 1, do step 2.**
**If neither exists → do step 2 (add the AC item first).**

1. **Spec by Example** _(if exists)_ — add or update the single scenario step (Given/When/Then with real values): `.cursor/skills/abd-story-specification/SKILL.md`
2. **Acceptance Criteria** _(if no specs)_ — add or correct the single WHEN/THEN item: `.cursor/skills/abd-story-acceptance-criteria/SKILL.md`
3. **Acceptance Test (RED)** — write one failing test method that captures the new or changed step; run it and confirm FAILED: `.cursor/skills/abd-story-acceptance-test/SKILL.md`
4. **Production Code (GREEN)** — change the smallest surface that makes the test pass; re-run until green: `.cursor/skills/abd-clean-code/SKILL.md`
5. **Domain Model** _(if exists, and the step touches a concept or responsibility)_ — apply small targeted updates only; do not redesign: `.cursor/skills/abd-domain-model/SKILL.md`

Run all tests for the story after step 4 to confirm nothing regressed.
