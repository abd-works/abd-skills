# Rule: Clear English in every skill section

**Scanner:** Manual review

The **target** **`SKILL.md`** should read in **clear, grammatical English** from start to finish: **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, and other teaching blocks use full sentences and a colleague-level voice. Paths and commands belong where readers expect them, with a line or two of prose so the page teaches instead of dumping scripts. YAML **`description`** stays one short outcome line. Failure is a polished opening followed by brittle note fragments, a **Purpose** that is only file operations when readers wanted the practice, or a **description** that repeats the whole **Build** pipeline.

## DO

- Write **every** narrative section in **direct, grammatical prose** — **Core concepts** and procedures included, not only **Purpose** / **When to use**.

  **Example (pass):** **Build** step 1: “If **`SKILL.md`** is missing, copy the starter template, add **`Manual:`**, and create empty **`rules/`** and **`templates/`**.” — full sentence.

- Keep **Purpose** and **When to use** as the short *why* and *when*; **When to use** uses real triggers (for example evidence already gathered, need a finished package).

  **Example (pass):** **When to use:** “You already have **`abd-answers-retrieval.md`** and need **`SKILL.md`** plus **`rules/`** finished for reviewers.”

- For **abd-author-practice-skill** itself, **Purpose** may state plainly that this step finishes the target page and **`rules/`** — that **is** the user-facing outcome here.

  **Example (pass):** “This skill authors the target **`rules/*.md`** and finishes **`SKILL.md`** from retrieval.”

- Keep YAML **`description`** to **one line** about the outcome, not every path touched.

  **Example (pass):** `description: Finish a practice skill package from hub retrieval evidence.`

- Put commands in **Prerequisites** / **Build** / **Validate** with a short intro sentence so lists are not orphaned.

  **Example (pass):** “From repo root, bundle rules after edits:” then the **`python ... bundle_rules...`** line.

- Use **clear phrases** in **Agent Instructions** table cells; terse is fine, broken grammar is not.

  **Example (pass):** “Read **`inputs/abd-answers-retrieval.md`** before editing **`SKILL.md`**.”

- Put provenance in **`Source:`** on **rules** or a **Sources:** note — not long “from the training / tightened for…” meta in body prose.

  **Example (pass):** Body says what the practice **is**; **`rules/foo.md`** ends a bullet with **Source:** Kept chunk #3.

## DO NOT

- Polish **Purpose** only while **Core concepts** or **Build** read like a rough internal checklist with no real sentences.

  **Example (fail):** **Purpose** is two paragraphs; **Build** is “1. copy 2. bundle 3. done” with no connecting text.

- Open the **target practice** with **Purpose** that is only an IT runbook when readers expect the **practice** itself.

  **Example (fail):** Story-mapping skill: “**Purpose:** Copy **`SKILL.md`** and run **`bundle_rules...`**” as the first line.

- Paste the full **Build** pipeline into **`description`**.

  **Example (fail):** **`description`** lists six file paths and two shell commands — belongs in **Build** only.

- Pad teaching with provenance throat-clearing (“training-aligned”, “tightened for this notation”) instead of substance; put audit trail on **rules**.

  **Example (fail):** **Core concepts** paragraph 1 explains where wording came from; still no explanation of the method.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
