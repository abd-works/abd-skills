### Rule: Section organization matches mechanism count

The reference is **always one file** (`architecture-reference.md`). What varies is how the mechanisms inside that file are organized — and the choice is **decidable from the mechanism count**, not author taste. With **2–3 mechanisms that are tightly related**, the reference can use **one combined `## Mechanisms` section** that weaves the five-part shape (Principles & Patterns, File Structure, Participants, Flow, Walkthrough Example) across all of them. With **4+ mechanisms** (or any set whose mechanisms are not tightly related), each mechanism gets its own `## Mechanism: <Name>` section with the five-part shape as `###` subsections. The rule has one explicit override: if the user (or an enclosing skill) **states a section organization**, that choice wins and the reference includes a one-line note at the top saying so. Passing means the organization matches the count, or the override is documented. Failing means the file splits into multiple files, or a 10-mechanism architecture is crammed into one combined section, or the five-part shape is dropped to "save space".

#### DO

- Count the mechanisms first; pick the section organization from the count using the rule above. Always produce one file at `inputs/architecture-reference.md`.

  **Example (pass):** Three tightly-related mechanisms (`Error Handling`, `Retries`, `Idempotency`) → one `## Mechanisms` section in `architecture-reference.md` that weaves Principles & Patterns, File Structure, Participants, Flow, and a Walkthrough across all three.

- For 4+ mechanisms (or non-tightly-related sets), give each mechanism its own `## Mechanism: <Name>` H2 with the five-part shape as `###` subsections.

  **Example (pass):** Six mechanisms (`Error Handling`, `Caching`, `Persistence`, `Authorization`, `Validation`, `Observability`) → six H2 sections in the same `architecture-reference.md`, each with the same `### Principles & Patterns` / `### File Structure` / `### Participants` / `### Flow` / `### Walkthrough Example` / `### Testing the mechanism` shape.

- Honour an explicit user override and document it at the top of the file.

  **Example (pass):** Five mechanisms but the user asks for the combined section. Below the title: `> Organization: combined (user override; default for 5 mechanisms would be per-mechanism sections).`

#### DO NOT

- Split the reference across multiple files (e.g. a `mechanisms/` folder with `mechanisms/caching.md`, `mechanisms/error-handling.md`).

  **Example (fail):** The skill ships `architecture-reference.md` plus three files under `mechanisms/`. Multi-file is not a layout this skill produces — the contract with downstream consumers (a build skill, a reviewer) is one file.

- Cram 10 mechanisms into one combined `## Mechanisms` section to "keep it tight".

  **Example (fail):** A combined section runs 2000 lines because the author refused to give each mechanism its own H2. Readers cannot scan; the TOC cannot help.

- Drop the five-part shape to make the combined section shorter.

  **Example (fail):** The combined section has Principles & Patterns and Walkthrough but skips Participants and Flow because "the diagrams take too much space". The downstream implementation skill now has nothing to render the participants from.

**Source:** Practice-skill authoring convention (abd-architecture-reference). One-file rule keeps the contract simple for downstream consumers; section-organization rule keeps the file scannable as the mechanism set grows.
