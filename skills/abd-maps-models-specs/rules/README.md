# Rules (`rules/`)

These are **atomic governance rules** for **this** skill only (`abd-maps-models-specs`). They are **not** a dump of legacy “step1–step6” rules from other pipelines.

## Canonical rule format (non-negotiable)

Every **`rules/*.md`** (except this README) must follow the **same structure as `abd-maps-models-specs-old/rules`:**

1. **YAML frontmatter** — `rule_id` only (phase attachment is **not** here — see below).
2. **`##` Title** — one line naming the rule.
3. **Guidance** — prose that explains intent, scope, scanners, and links to library docs. Use short paragraphs and bullets as needed (**no** separate “Intent” / “Examples” / **Bad:** / **Good:** headings—those are not the legacy shape).
4. **`**DO**`** — on its own line (section header). Below it: bullets and/or **fenced examples** showing what to do (JSON, text, or pseudocode—match the old rules).
5. **`**DON'T**`** *or* **`**DO NOT**`** — on its own line (section header). Below it: bullets and/or **fenced examples** showing what not to do.

**Normative + mechanical:** Rules tell the AI how to **author** artifacts; where `scripts/` implements a check, say so. Scanners catch gaps when the AI misses something—the **DO** / **DON'T** examples still define what “good” and “bad” look like for humans and for review.

**`scripts/test_rule_examples.py`** runs at the end of **`build.py`** and fails if any rule is missing a line-start **`**DO**`** or **`**DON'T**`** / **`**DO NOT**`**.

## How they attach to phases

**Authoritative mapping:** **`skill-config.json`** at the skill root, same pattern as **abd-skill-builder**:

- **`phase_rules`** — object whose keys are **phase slugs** (same strings as **`phase_files`**, without `.md`). Each value is an ordered list of **rule stems**: the rule filename **without** `.md` (e.g. `shaped-story-shape` → `rules/shaped-story-shape.md`).
- **`every_phase_rules`** — optional list of stems prepended to **every** phase’s rule list (deduplicated in order). Use sparingly.

`scripts/build.py` / **`MapsInstructions`** load those files in list order, **strip** YAML frontmatter from the inlined body, and emit them under **Rules** in each built bundle (`content/built/phases/<slug>.md`).

If a rule file is **not** mentioned in `every_phase_rules` or any `phase_rules[...]` entry, **`build.py`** prints a **warning** (the rule would never be inlined).

## Relationship to other repos

- **abd-solution-modeler** and similar skills may use **different** phase names and JSON shapes. When a *concept* aligns (e.g. “cite chunks on substantive claims”), we **rewrite** the rule here for **our** artifacts (`terms_layer.json`, `shaped_story_map.json`, `map-model-spec`, `context_index.json`, …), not copy their prose.
- **Scanners:** Automated checks are **bound to rules** in **`rules/scanners.json`** → **`rule_scanner_bindings`**. **`python scripts/build.py`** runs the ordered **`skill-config.json`** → **`operator.build_pipeline`**, which includes those scanner scripts (plus emitters, manifest, rule-example lint). Rules describe **solution analyst + AI** obligations; scripts enforce **what is implemented**.

## Index

| Rule file | Phases (see `skill-config.json` → `phase_rules`) | Intent |
|-----------|--------------------------------------------------|--------|
| [stage-1-context-decisions.md](stage-1-context-decisions.md) | context-chunking-approach, canonical-context | Readiness audit + Phase 1 context package before vocabulary work |
| [evidence-citations-required.md](evidence-citations-required.md) | terms-mechanisms → validate-render | Substantive claims cite `chunk_id` / evidence fields |
| [story-map-before-domain-types.md](story-map-before-domain-types.md) | shaped-story-map, domain-types | Shaped story map precedes sparse `concepts[]` |
| [variant-decisions-before-deepen.md](variant-decisions-before-deepen.md) | variant-classification, deepen | Variant representation chosen before heavy property work |
| [shaped-story-shape.md](shaped-story-shape.md) | shaped-story-map | Actor, anchor, evidence for stories |
| [naming-module-epic-story.md](naming-module-epic-story.md) | shaped-story-map, domain-types, integrate | Verb–noun discipline and alignment |
| [domain-types-and-deepen-quality.md](domain-types-and-deepen-quality.md) | domain-types, variant-classification, deepen | Promotion bar: owns, evidence, not anemic / centralized |
| [integrate-coherence.md](integrate-coherence.md) | integrate | One coherent map / model / spec |
| [deepen-approved-tools-only.md](deepen-approved-tools-only.md) | deepen | No ad-hoc merge scripts outside approved workflow |
| [validate-and-manifest-gates.md](validate-and-manifest-gates.md) | validate-render | Contract validators, story map check, manifest, CI |

When you add a phase or change which rules apply, edit **`phase_rules`** / **`every_phase_rules`** in **`skill-config.json`** and run **`python scripts/build.py`**.
