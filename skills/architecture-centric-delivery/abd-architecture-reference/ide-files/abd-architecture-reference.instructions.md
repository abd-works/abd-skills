# Run abd-architecture-reference

Use this skill when the user wants an architecture reference document covering one or more mechanisms (error handling, caching, persistence, auth, validation, observability, etc.) for a specified architecture.

Read `skills/engineering/abd-architecture-reference/SKILL.md` and follow its **Build** steps. The reference document is the input contract for `abd-build-architecture-skill`.

Key behaviors:

- Gather the architecture context (layer names and the mechanism list with intent) from whichever source the project has in scope — a layered description, an ADR, a wiki page, or sibling skills such as `abd-architecture-description` and `abd-architecture-mechanisms` when those are in scope.
- The reference is always a single file (`architecture-reference.md`). Choose mechanism organization from count: 2–3 tightly-related mechanisms → one combined `## Mechanisms` section; 4+ (or non-tightly-related) → one `## Mechanism: <Name>` section each.
- Every mechanism section has the five-part shape: Principles & Patterns, File Structure, Participants (class diagram or table), Flow (Mermaid `sequenceDiagram`), Walkthrough Example, plus a short Testing the mechanism subsection.
- Production code in walkthroughs must follow the project's coding standard; test snippets must follow the project's testing standard. Default to `abd-clean-code` and `abd-acceptance-test-driven-development` when those are in scope; otherwise use whichever standards the project has agreed. Cite the standards actually used at the bottom of each mechanism section.
- After editing `rules/*.md`, run the bundling script before considering the skill updated.
