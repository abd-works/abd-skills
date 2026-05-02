---
---

# Rule: Anti-patterns belong in rules, not skill teaching

The **target** **`SKILL.md`** teaching voice (**Purpose**, **When to use**, **Core concepts**, **Build**) should tell practitioners **what to do** and **how to think**. Sections that list what the skill does **not** do — "What this skill is not," "Anti-patterns," "Common mistakes," "Don'ts" — belong in **`rules/*.md`** as **`## DO NOT`** bullets where they can be checked against real artifacts. Passing means the teaching voice is positive and forward; anti-patterns are enforced through rules. Failing means the skill page spends teaching space listing negatives that duplicate or should be rules.

## DO

- Teach the method positively in **`SKILL.md`**: what to do, how to think, what to produce.

  **Example (pass):** "Write 1–2 paragraphs of flowing prose that define the abstraction." — teaches the positive action.

- Put anti-patterns, forbidden formats, and "don't do X" guidance in **`rules/*.md`** as **`## DO NOT`** bullets with concrete examples.

  **Example (pass):** `rules/no-jargon-added.md` has a `## DO NOT` bullet: "Add `Intent:` lines to any term or KA." — checkable against an artifact.

## DO NOT

- Add a "What this skill is not" or "Anti-patterns" or "Common mistakes" section to the skill's main teaching voice.

  **Example (fail):** **`SKILL.md`** has a `### What this skill is not` section with three bullets listing things to avoid — these are rules, not teaching.

- Duplicate rule content as negative prose in teaching sections when a **`rules/*.md`** file already covers that check.

  **Example (fail):** **`SKILL.md`** says "It does **not** make class-level commitments" in the teaching voice while `rules/no-class-level-commitments.md` already enforces this — the skill page repeats the rule as prose instead of teaching the method.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
