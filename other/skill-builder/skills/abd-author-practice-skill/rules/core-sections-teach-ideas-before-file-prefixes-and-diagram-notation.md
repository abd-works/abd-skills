# Rule: Core sections teach ideas before file prefixes and diagram notation

**Scanner:** Manual review

**Purpose** and **Core concepts** on the **target** **`SKILL.md`** should explain **what things mean and how they relate** — outcomes, who is involved, behaviour, options — in plain language first. **Prefix tags**, **ASCII tree layout**, **diagram geometry**, and **which file line holds what** belong in **templates**, **Agent Instructions**, **Build**, **Validate**, and **`rules/*.md`**, not as the main front-door to the method. You fail when **Core concepts** opens as a symbol legend or tells people which **`FOO:`** line to use before the ideas exist.

## DO

- Teach **relationships** in plain language (for example broader outcomes decompose into finer ones; actors attach to the outcome in focus; behaviours and options hang under those).

  **Example (pass):** “Goals form a hierarchy from organisation-level outcomes down to impacts you can observe in behaviour.” — no `GOAL:` prefix in **Core concepts**.

- Put **exact markers**, **column names**, **diagram shape**, and **canvas placement** only in **templates**, **Agent Instructions**, **Build** / **Validate**, and **rules** that judge outputs.

  **Example (pass):** **`templates/impact-map.md`** shows `GOAL:` lines; **Core concepts** says “goals sit at the top of the map” without copying the prefix block.

- Keep **Core concepts** examples **conceptual** (outcome + proof, behaviour + proxy); **templates** show row/field layout.

  **Example (pass):** “An impact is observable behaviour change; a trailing metric is how you know it moved.” — template shows **`IMPACT:`** / **`TRAILING_METRIC:`** lines.

- When the hub uses a picture, translate to **concepts** in **`SKILL.md`**; cite figures in **manual** / **references** without turning the skill into a symbol glossary.

  **Example (pass):** “The training figure shows three levels of outcome; see **manual** figure 2.” — not a fenced block of every glyph.

## DO NOT

- Use **Core concepts** mainly to rehearse **prefix tags**, **tree ASCII**, **indent rules**, or **spatial layout** when plain language could state relationships first.

  **Example (fail):** First screen of **Core concepts** is a fenced block of `EPIC:` / `STORY:` lines and “indent means subordinate” before “what an epic is”.

- Put **template positioning** in **Core concepts** (“use the `FOO:` line”, “in column 3 of the table”).

  **Example (fail):** “Core concepts” says “put the metric on **`TRAILING_METRIC:`** next to **`GOAL:`**” — belongs in **template** / **Agent Instructions**.

- Add **package-structure meta** to the **target** **Core concepts** (“meaning layer vs check layer”, “where teaching lives”) — that is **abd-author-practice-skill** guidance only.

  **Example (fail):** Target **Core concepts** explains how **`rules/`** differ from **Build** for package authors — practitioners need the method, not package anatomy.

- Train readers on **notation** before they know **what each node type means** in the real world.

  **Example (fail):** “Learn these seven prefixes” before “what is an actor vs an outcome”.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
