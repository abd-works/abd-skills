# Run abd-build-architecture-skill

Use this skill when the user has a finished architecture-mechanism reference document and wants the **implementation skill** that produces code in that architecture.

Read `skills/engineering/abd-build-architecture-skill/SKILL.md` and follow its **Build** steps.

Key behaviors:

- Confirm the reference document is a single, finished `architecture-reference.md` (mechanisms organized inside it in one combined section or one section per mechanism). Copy it into the generated skill at `inputs/architecture-reference.md` so the generated skill is self-contained.
- Generate one `rules/<principle-slug>.md` per principle in the reference. The principle's named pattern is the `Example (pass)`; the reference walkthrough's anti-pattern is the `Example (fail)`.
- Generate `templates/` that cover every file path in the reference's File Structure blocks, with at least one filled mini-example per template.
- Generate the `ide-files/` triple (`.mdc`, `.instructions.md`, `.prompt.md`); the `.mdc` and `.instructions.md` bodies must match after normalization.
- Inherit conventions from the project's coding standard and testing standard by reference; do not copy their rules in. When `abd-clean-code` and `abd-acceptance-test-driven-development` are in scope, those are the standards; otherwise name whichever guides the project uses.
- Add `scanner:` YAML fields only when the matching `scanners/<stem>-scanner.py` exists.
- After generation, run `bundle_rules_into_skill_md.py` on the generated skill and the `mdc-instructions-parity` scanner.
