### Rule: Generated skill inherits the project's coding and testing standards by reference

The generated implementation skill must **inherit** the **project's chosen coding standard and testing standard** by **naming them explicitly** in `SKILL.md` and citing the relevant rule basenames — **not** by copying those rule files in. Whichever guides are in scope (in an agilebydesign-skills-anchored project these will typically be `abd-clean-code` and `abd-acceptance-test-driven-development`; in another project they may be a different skill, a style guide, or a corporate standard) already enforce naming, function size, dependency injection, encapsulation, test-class-per-story, and Given/When/Then helpers — duplicating those rules creates drift the moment the upstream guide is updated. Passing means the generated `SKILL.md` calls out both standards in its Agent Instructions and Validate sections, and the generated rules block does not re-implement rules that already exist upstream. Failing means the generated skill silently re-defines `use-domain-language.md` or `test-story-driven.md`, contradicts the upstream guide, or never mentions either upstream standard.

#### DO

- In the generated `SKILL.md` Agent Instructions, name the **coding standard in scope** for the project (typically `abd-clean-code` in an agilebydesign-skills-anchored project) and state that all generated production code follows it. Name the **testing standard in scope** (typically `abd-acceptance-test-driven-development`) and state that all generated test code follows it.

  **Example (pass):** Agent Instructions step 3 reads: "Code generated under this skill follows the project's coding standard (`abd-clean-code` in scope here: domain language, small functions, constructor injection, no anemic data bags). Test code follows the project's testing standard (`abd-acceptance-test-driven-development` in scope here: class per story, Given/When/Then helpers, no defensive checks)."

- In the generated `Validate` checklist, reference the upstream rule basenames by name.

  **Example (pass):** "Code passes the project's coding rules — e.g. when `abd-clean-code` is in scope: `use-domain-language`, `keep-functions-small-focused`, `enforce-encapsulation`."

- When the architecture has an **architecture-specific** twist on one of those rules (e.g. "in this architecture, ALL helpers extend a tier-base helper"), express that twist as a new rule file in the generated skill — and make the rule's opening paragraph cite the upstream rule it specializes.

  **Example (pass):** `rules/extend-tier-base-helper.md` opens: "This rule specializes `abd-acceptance-test-driven-development/rules/object-oriented-test-helpers.md` for this architecture: every tier helper extends a single base class so test data is shared."

- When the project uses a non-agilebydesign standard, cite *that* by name and link to it — same structure, different upstream.

  **Example (pass):** Agent Instructions step 3 reads: "Code generated under this skill follows the project's coding standard at `docs/coding-standards.md`. Test code follows the project's testing standard at `docs/test-style.md`."

#### DO NOT

- Copy `use-domain-language.md` from `abd-clean-code` (or the equivalent rule from whichever guide is in scope) into the generated skill's `rules/`.

  **Example (fail):** Generated `rules/use-domain-language.md` is a byte-for-byte copy of `agilebydesign-skills/skills/engineering/abd-clean-code/rules/use-domain-language.md`. Updates upstream will not propagate.

- Generate a `SKILL.md` that never names the coding standard or testing standard the project is operating under.

  **Example (fail):** The generated SKILL.md describes how to build domain modules and walkthrough tests but never mentions `abd-clean-code`, `abd-acceptance-test-driven-development`, or any other style/testing guide. Reviewers have no anchor.

- Re-define a rule in the generated skill in a way that contradicts the upstream guide.

  **Example (fail):** Generated `rules/test-style.md` says "tests may use `try/catch` to guard against environment flakiness." The project's testing standard (`abd-acceptance-test-driven-development` or otherwise) says the opposite. Future code authors do not know which rule wins.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill). The generated skill inherits the project's existing code-style and test-style decisions rather than duplicating or contradicting them.
