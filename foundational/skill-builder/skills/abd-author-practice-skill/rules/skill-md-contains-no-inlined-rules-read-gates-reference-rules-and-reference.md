# Rule: SKILL.md contains no inlined rules; read-gates reference rules/ and reference/

**Scanner:** Manual review

On the **target** package, rule prose lives only in **`rules/*.md`** and concept/example prose lives only in **`reference/*.md`**. **`SKILL.md`** must never contain `<!-- execute_rules:bundle_rules -->` markers or inlined rule text. The Agent Instructions block in **`SKILL.md`** must contain explicit **MANDATORY read-gates**: one before generating (read every `rules/` file + every `reference/` file) and one at validation (re-read every `rules/` file, emit a per-rule verdict for each). **`scanner:`** in rule YAML is allowed only if `scanners/<stem>-scanner.py` exists.

Failure is a `SKILL.md` that still has bundle markers, inlined rule prose, or an Agent Instructions block with no read-gates. A missing `reference/` folder is fine when the skill has no concept teaching to externalise; the gate instruction should still be present.

## DO

- Keep **`SKILL.md`** as a thin router: purpose, when-to-use, output file resolution, Agent Instructions with read-gates, Validate with per-rule verdict.

  **Example (pass):** Agent Instructions says "MANDATORY: Before authoring, read every file in `rules/` and every file in `reference/`. At validation, re-read every `rules/` file and emit a PASS/FAIL verdict for each."

- Set **`scanner: <stem>`** in the **rule file's YAML** only when **`scanners/<stem>-scanner.py`** exists on that package (stem repeated exactly in the scanner Python filename).

  **Example (pass):** `rules/titles.md` has frontmatter `scanner: titles` and the file `scanners/titles-scanner.py` is present beside `rules/`.

- Keep **one** `rules/<topic>.md` per validation concern; align `scanner:` stem with the topic and the `scanners/<stem>-scanner.py` filename.

  **Example (pass):** `rules/story-title-shape.md` owns title-shape checks; `scanner: story-title-shape` and `scanners/story-title-shape-scanner.py` use the same stem.

## DO NOT

- Include `<!-- execute_rules:bundle_rules:begin -->` or `<!-- execute_rules:bundle_rules:end -->` markers in `SKILL.md`.

  **Example (fail):** `SKILL.md` has a block between bundle markers containing a copy of `rules/naming.md` — rule prose inlined.

- Write an Agent Instructions block that does not mention `rules/` or `reference/` as mandatory reads.

  **Example (fail):** Agent Instructions says only "Generate content following the rules attached to this skill" with no explicit read-gate pointing at `rules/*.md` and `reference/`.

- Declare `scanner: layout` in `rules/layout.md` (or any rule) when `scanners/layout-scanner.py` is missing.

  **Example (fail):** `rules/layout.md` has `scanner: layout` but there is no `layout-scanner.py` under `scanners/`.

**Source:** ABD disclosure refactor — thin-router contract.
