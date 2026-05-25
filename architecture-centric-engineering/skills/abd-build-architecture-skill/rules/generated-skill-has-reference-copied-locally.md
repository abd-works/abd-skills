### Rule: Generated skill ships its own copy of the architecture reference

The generated implementation skill must contain its own copy of the architecture reference at `inputs/architecture-reference.md` — a single file, mechanisms organized inside it as the upstream authoring chose (combined section or one section per mechanism). The generated skill is the source of truth for the architecture it implements; depending on a link to another skill folder is brittle, and a copy guarantees the generated skill stays self-contained when it is deployed or moved. Passing means a reviewer can open the generated skill, read `inputs/architecture-reference.md`, and recover the full reference. Failing means the generated skill only links out, copies a partial reference, or splits the file into pieces it was not authored as.

#### DO

- Copy the **entire** reference document into the generated skill's `inputs/architecture-reference.md` exactly as it was authored. Do not reformat, split, or merge sections.

  **Example (pass):** The reference covers six mechanisms in per-mechanism sections. The generated skill's `inputs/architecture-reference.md` contains the same TOC, Overview, Architecture Layers, six `## Mechanism: <Name>` sections, Testing Architecture, and References — byte-for-byte the same body.

- In the generated `SKILL.md`'s Agent Instructions step 1, point readers at `inputs/architecture-reference.md` by relative path.

  **Example (pass):** Agent Instructions step 1 reads: "Load [`inputs/architecture-reference.md`](inputs/architecture-reference.md) to understand the authoritative architecture: layers, principles, patterns, file structure, participants, flow, walkthrough, testing."

- Document the source so a maintainer can resync if the reference is updated upstream.

  **Example (pass):** A note at the top of `inputs/architecture-reference.md` reads: `Source: skills/engineering/abd-architecture-template output for {{ArchName}} produced on YYYY-MM-DD.`

#### DO NOT

- Leave `inputs/` empty in the generated skill and rely on the absolute path to where the reference happens to live today.

  **Example (fail):** The generated `SKILL.md` step 1 says "Read `C:/dev/some-project/architecture-reference.md`". When that machine path changes, the skill silently breaks.

- Copy only the Overview and skip the mechanism sections.

  **Example (fail):** `inputs/architecture-reference.md` contains the Table of Contents and Overview, but every mechanism section is replaced with `<!-- See original document -->`.

- Allow the generated skill's rules to cite mechanisms that are not in the copied reference.

  **Example (fail):** `rules/cache-via-side-car.md` cites `inputs/architecture-reference.md` "Mechanism: Caching", but the copy of the reference in `inputs/` does not contain a Caching section.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill).
