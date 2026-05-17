### Rule: Scanner YAML field appears only when the scanner script exists

A generated rule may declare `scanner: <stem>` in its YAML frontmatter **only** when the file `scanners/<stem>-scanner.py` exists in the generated skill on disk. The frontmatter is a claim that an automated check exists; lying about that check breaks `run_scanners.py` and erodes trust in the skill. If a useful scanner is planned but not yet written, the rule sits under **Manual review** and a `# TODO scanner: <stem>` comment is added near the bottom of the rule body to record the intent. Passing means every `scanner:` value points at a real `.py` file with the same stem; missing scanners are tracked as TODOs in the rule body rather than as fake YAML fields. Failing means a rule advertises a scanner the skill does not actually ship.

#### DO

- Before adding `scanner: layer_purity` to `rules/maintain-layer-purity.md`, confirm `scanners/typescript/layer_purity_scanner.py` (or the language-appropriate path) exists and exits with a sensible code.

  **Example (pass):** `rules/maintain-layer-purity.md` opens with frontmatter `scanner: layer_purity_scanner` and the file `scanners/typescript/layer_purity_scanner.py` exists and contains a `main()` function.

- For rules that **should** have a scanner but don't yet, leave the frontmatter clean (no `scanner:` line) and add a body line `**Scanner:** Manual review (TODO: write scanners/<stem>-scanner.py).`

  **Example (pass):** `rules/keep-application-unaware-of-cache.md` body line reads `**Scanner:** Manual review (TODO: write scanners/python/cache_unawareness_scanner.py).` — the maintainer can grep for `TODO: write scanners` to find work.

- Run the bundle script after adding or removing a `scanner:` field so the inlined block in `SKILL.md` stays in sync.

  **Example (pass):** After adding the scanner field, `python skills/skill-builder/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root skills/engineering/<arch>-technical-architecture` is run, and the inlined rule block now shows the new line.

#### DO NOT

- Add `scanner: layer_purity` to a rule when no `layer_purity_scanner.py` exists.

  **Example (fail):** `rules/maintain-layer-purity.md` declares `scanner: layer_purity` but `scanners/` is empty. Running `run_scanners.py` fails with "scanner stem not found".

- Rename a scanner script without updating the YAML field.

  **Example (fail):** `scanners/python/cache_scanner.py` is renamed to `cache_awareness_scanner.py`; the rule still declares `scanner: cache_scanner`. The scanner runs zero rules.

- Use one `scanner:` stem for unrelated rules to look more "covered" than the skill actually is.

  **Example (fail):** Both `rules/maintain-layer-purity.md` and `rules/handle-errors-at-boundary.md` declare `scanner: layer_purity`. The error-handling rule is not really enforced; the field is decoration.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); aligns with `skill-md-bundle-matches-rules-md-files-scanner-stem-matches-py-filename` bundled in `abd-author-practice-skill`.
