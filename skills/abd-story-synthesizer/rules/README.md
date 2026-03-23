# Rules (`rules/`)

Governance rules for the story synthesizer: **DO** / **DO NOT** pairs, optional **scanner** hooks, and **operation-scoped injection** into prompts.

## Canonical frontmatter (new format)

Every rule file **`*.md`** except this README uses **YAML frontmatter** followed by markdown body. **`scripts/instructions.py`** strips frontmatter when merging rules into **`story_synthesizer.validation.rules`**.

```yaml
---
title: Short title
impact: HIGH | MEDIUM | LOW
tags: [discovery, story_map, domain, ...]
scanner: logical_domain          # key in scripts/scanners/registry.py SCANNER_BY_NAME; or null
rule_id: domain-logical-domain-level   # optional; default = filename stem (hyphens)
every_operation: false           # true = inject for every operation that loads validation.rules
operations:                      # optional; explicit list — overrides prefix defaults below
  - run_slice
  - validate_slice
pipeline_phases: [7, 8]          # optional doc only — aligns with pieces/process.md slice/validate stages
---
```

### Defaults when `operations` is omitted

If **`every_operation`** is false and **`operations`** is absent, **`scripts/rule_frontmatter.py`** infers from the **filename stem** (longest prefix wins):

| Prefix | Default operations (injected when listed in `skill-config` for that op) |
|--------|------------------------------------------------------------------------|
| `context-slice-` | `create_strategy`, `validate_session`, `run_slice`, `generate_slice`, `validate_run`, `validate_slice` |
| `context-` | `concept_scan`, `model_discovery`, `model_validation` |
| `domain-` | `model_discovery`, `model_validation`, `create_strategy`, `run_slice`, `generate_slice`, `validate_run`, `validate_slice` |
| `interaction-` | same as `domain-` |
| `session-` | `create_strategy`, `validate_session`, `run_slice`, `generate_slice`, `validate_slice` |
| `correction-` | none (add explicit `operations:` if you wire these into prompts) |
| `verb-` | `run_slice`, `generate_slice`, `validate_run`, `validate_slice`, `model_discovery`, `model_validation` |
| `scaffold-` | `model_discovery`, `run_slice`, `generate_slice`, `validate_run`, `validate_slice` |
| *(other stems)* | all operations that include `story_synthesizer.validation.rules` in **`skill-config.json`** |

Override with explicit **`operations:`** when a rule should attach to a different set.

### Pipeline phases (documentation)

Cross-reference **`pieces/process.md`** (Overall context → Session → Slice-runs):

| Process stages (summary) | Typical operations using rules |
|--------------------------|----------------------------------|
| Phases 1–5 (overall context) | `concept_scan`, `model_discovery`, `model_validation` |
| Session (strategy) | `create_strategy`, `validate_session`, `improve_strategy` |
| Slice-runs (build / validate) | `run_slice`, `generate_slice`, `validate_run`, `validate_slice` |

`pipeline_phases` in frontmatter is **not** interpreted by code; it documents intent for authors.

## Tag format (required)

Keep **`tags:`** as today — session/strategy scoping and strategy documents; see the table in the previous README version. **`session`** / **`slices`** tags describe slice/session concerns; they are **not** the same as **`operations`** (which gate **injection**).

## Scanners

- **Code dispatch:** **`scripts/scanners/registry.py`** — **`SCANNER_BY_NAME`**, **`RULE_TO_SCANNER`**, **`get_ordered_scanners`**, **`run_scanners`**.
- **JSON mirror:** **`rules/scanners.json`** — lists **`rule_to_scanner`** and **`scanner_names`** for tooling; **registry.py stays authoritative** — update both when you add a rule with a scanner or rename a stem.
- **Registry without a rule file:** e.g. **`session-slice-not-epic-by-epic`** appears in **`RULE_TO_SCANNER`** but there is no matching **`rules/*.md`** yet; add the markdown rule or remove the mapping when you consolidate scanners.
- **Rule file:** optional **`scanner:`** in frontmatter must match a key in **`SCANNER_BY_NAME`**, or **`null`** / omitted for AI-only rules.
- **`python scripts/build.py validate`** runs scanners from the registry against `story-synthesizer/interaction-tree.md` and `domain-model.md` (see **`scripts/build.py`**).

## How rules get injected

**`get_instructions <operation>`** (via **`scripts/build.py`**) assembles sections from **`skill-config.json`** → **`operation_sections`**. When **`story_synthesizer.validation.rules`** is listed, **`rules/`** is merged with **frontmatter stripped** and **operation filter** applied (`rule_frontmatter.merge_rules_markdown_for_operation`).

You **must** run **`get_instructions`** before synthesis; rules are **not** only in `AGENTS.md`.

## Body format

Each rule: **`##` title**, then **`**DO**`** / **`**DO NOT**`** (or **`**DO NOT**`**) sections with examples — unchanged from before.

## Index maintenance

When adding a rule:

1. Name file **`{area}-{rule-slug}.md`** (hyphens) — **`rule_id`** defaults to stem.
2. Set **`scanner:`** or **`null`**; add **`RULE_TO_SCANNER`** in **`registry.py`** if a new mapping; refresh **`rules/scanners.json`** (or run the generator from `registry` imports).
3. Set **`operations:`** or rely on **prefix defaults**; use **`every_operation: true`** only for global rules.
