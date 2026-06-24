# Rule: Description front matter has "Use when" in situation language

**Purpose:** The `description` field is the first thing a catalog or agent sees about a skill. It must tell readers what the skill produces **and** when to reach for it — in one compact pair of sentences. The second sentence must start with `Use when` and describe the practitioner's circumstances, not the names or outputs of other skills.

## DO

- Write `description` as two sentences: the first says what the skill does (present-tense verb phrase, compact); the second starts with `Use when` and names a real-world situation the practitioner recognizes from their own work.

  **Example (pass):**
  ```yaml
  description: >-
    State exactly what must be true for a story to be done — so everyone agrees on 'finished'. Use when writing or reviewing exploration-phase behavior for stories.
  ```

  **Example (pass):**
  ```yaml
  description: >-
    Define each domain term precisely — name, meaning, boundaries, and relationships — so models, stories, and code share one vocabulary. Use when source material exists but no agreed domain vocabulary yet.
  ```

- Make the `Use when` condition describe the **team's situation** or **what they want to achieve** — a trigger the practitioner can recognize without knowing anything about the skill family.

  **Example (pass):** `Use when you want to agree on what the system should do before writing any test code.`

  **Example (pass):** `Use when the test structure is in place and you are ready to implement and drive production code.`

  **Example (pass):** `Use when source material exists but no agreed domain vocabulary yet.`

## DO NOT

- Name another skill or that skill's output artifact in the `Use when` clause.

  **Example (fail):** `Use when a scaffold has been approved` — "scaffold" is the output of `abd-bdd-behavior`; a practitioner reading a catalog doesn't know what that is.

  **Example (fail):** `Use when a test file with BDD: SIGNATURE markers exists` — `BDD: SIGNATURE` markers are the output of `abd-bdd-specification`.

  **Example (fail):** `Use when the user has run abd-bdd-behavior` — names another skill directly.

- Write the `Use when` clause in terms of what artifact the preceding skill produced. The condition must make sense on its own.

  **Example (fail):** `Use when the behavior hierarchy file is ready` — "behavior hierarchy file" is a deliverable of another skill.

- Write more than one compact sentence of what-it-does before the `Use when` clause.

  **Example (fail):**
  ```yaml
  description: >-
    Complete the RED-GREEN cycle: implement test bodies from signatures,
    then write minimal production code until every test passes. Tests observe
    behavior through the public API; code does only what the tests demand.
    Use when a test file with BDD: SIGNATURE markers exists.
  ```
  Three sentences of what + a Use when that references another skill's output.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
