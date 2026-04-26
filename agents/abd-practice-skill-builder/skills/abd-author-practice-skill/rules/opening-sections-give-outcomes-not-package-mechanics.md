# Rule: Opening sections give outcomes not package mechanics

**Scanner:** Manual review

**Purpose**, **When to use**, and the first teaching blocks on a **`SKILL.md`** should read like **why the packaged method matters**, **who it helps**, and **what becomes possible** when the practice is done well. They stay in **human outcome language**. **Package mechanics** — repo paths, **`Manual:`**, **`execute_rules`** markers, which template to copy, bundling commands, retrieval filenames, scanner wiring, or “how an agent runs this skill” — belong in **Prerequisites**, **Build**, **Validate**, **Agent Instructions**, or **`rules/*.md`**, not in the opening voice. Failure is a **Purpose** that reads like a runbook or file checklist before the reader knows **why** the practice exists.

## DO

- Write **Purpose** as **one** short paragraph (or at most two if the practice truly needs a problem/solution split) that answers **why** this skill exists, **what** finishing it helps people do, and **how** the skill supports that — without naming concrete paths or tooling steps.

  **Example (pass):** “This skill helps teams agree on thin vertical slices so delivery order matches risk and learning. It packages that thinking so facilitators and agents can run the same method and produce comparable maps.” — outcome only.

- Keep **When to use** as **triggers in plain language** (situations readers recognize), not a recap of **Build** or folder layout.

  **Example (pass):** “You have a story map and need to name the first shippable slice.” — no paths.

- Put **file names**, **copy steps**, **bundle commands**, and **what this skill does not include** (retrieval, scanners) in **Prerequisites**, **Build**, or **Not in this pass**.

  **Example (pass):** **Purpose** stays outcome-only; **Build** item 1 says “If **`SKILL.md`** is missing, copy from **`templates/SKILL_template.md`**…”

## DO NOT

- Open **Purpose** with retrieval paths, **`inputs/...`**, **`rules/*.md`**, **`Manual:`**, **`execute_rules`**, or “start from **`templates/...`**” before stating **why** the practice matters.

  **Example (fail):** “You use this skill after hub evidence is in **`inputs/abd-answers-retrieval.md`**. It authors **`rules/*.md`** and finishes **`SKILL.md`**…” as the **whole** purpose — mechanics first, no **why**.

- Use **Purpose** to explain **agent choreography** or **another skill’s** pipeline (“load X then run Y”) when that is not the **substance** of the practice itself.

  **Example (fail):** “**Purpose:** Invoke **abd-query-practice-sources** then run **`bundle_rules_into_skill_md.py`** with **`--skill-root`**…” — operator steps, not the method’s value.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
