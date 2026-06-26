# Rule: Target rule files are checkable specs for named artifacts

**Scanner:** Manual review

A **`rules/*.md`** on the **target** skill names a **named output** (file, section, marker pattern) and states **pass** conditions a reviewer can apply from text alone. It has **`## DO`** and **`## DO NOT`** with decidable bullets, each with **Example (pass)** / **Example (fail)** as required by **Rule DOs and DON'Ts must each have examples**. Hub-backed bullets need **`Source:`** to **`inputs/abd-answers-retrieval.md`**. **Build** in **`SKILL.md`** owns step order. You fail when the file is workshop facilitation, a pointer-only stub, **DO** lines that need “you had to be there”, fake hub **Source:**, or when **`rules/`** replace **Build** as the numbered how-to list.

## DO

- Treat each **`rules/*.md`** as a **spec for judging one kind of artifact**, not a second copy of the whole **`SKILL.md`** story.

  **Example (pass):** **`rules/story-title-shape.md`** applies only to story titles in **`story-map.md`** / **`story-map.txt`**; it does not repeat the full story-mapping method.

- Make **every** **`## DO`** bullet **decidable** from the named file or string (no “team felt aligned”).

  **Example (pass):** “**DO** Every story title is verb–noun” — open **`story-map.md`**, scan titles, mark pass/fail.

- Put **`Source:`** on hub-backed bullets pointing to **Kept chunk #** (or row) in **`inputs/abd-answers-retrieval.md`**. Use **`Source:** Engagement** or omit for chat-only norms — do not invent hub rows.

  **Example (pass):** “**DO** Assumptions list includes owner and review date **Source:** Kept chunk #4 …”

- Prefer **one validation concern per file**; name the file after the check (**`naming.md`**, **`story-title-shape.md`**), not after a random **`SKILL.md`** heading.

  **Example (pass):** **`rules/acceptance-criteria-format.md`** only checks AC line format; ordering of work stays in **Build**.

## DO NOT

- Use **`rules/*.md`** as the **primary step sequence** for the practice; **Build** in **`SKILL.md`** owns order.

  **Example (fail):** **`rules/how-to.md`** with **DO** “Step 1 run retrieval, Step 2 author SKILL” — belongs in **Build**, not **`rules/`**.

- Ship a normative rule with **no** **`## DO NOT`**, or with **DO** items that do not attach to any **named** file or pattern.

  **Example (fail):** “Stories should be good” — no **DO NOT**, no artifact, no way to score an output.

- Label a bullet as from the hub **without** a retrieval row that supports it.

  **Example (fail):** “**DO** Use Patton’s exact workshop timings **Source:** hub” — no chunk in **`inputs/`** says that.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
