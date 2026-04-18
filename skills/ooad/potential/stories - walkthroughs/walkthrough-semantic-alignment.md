# Walkthrough ↔ map-model-spec alignment (semantic check)

**Rule (authoritative):** [`scenario-walkthrough-align-spec`](../../../rules/scenario-walkthrough-align-spec.md) — any **concept** name used in scenario walkthrough prose (bold `**ConceptName**` or CamelCase in flows) must match a **`concept.name`** in **`map-model-spec.json`**. Same idea — no shadow synonyms unless Integrate has recorded a merge.

**Index vs narrative:** Under your workspace **`output_dir`** (often `spec/`): **`scenario_walkthroughs.json`** holds metadata and a short **`summary`** only. Long-form walkthrough bodies live in markdown files (e.g. **`walkthroughs/*.md`**) referenced by **`narrative_markdown`** paths in that index — paths are relative to **`output_dir`**, not to a nested vendor folder.

**What `map-model-spec.json` is:** The **domain** object model for the product slice (concepts, properties, operations). It is **not** the agile_bots **behavior** graph (CLI/panel story-bot workflows). Walkthrough prose should stay in product/domain terms; meta notes about the spec format belong in skill docs or workspace notes — not inside each walkthrough `*.md` unless a gap forces it.

**Optional automation:** A workspace may ship a scanner (for example **abd-answers** `scripts/scanners/walkthrough_concept_alignment.py`) that checks bold/CamelCase tokens and **`map_model_spec_module`** in the index against **`map-model-spec.json`**. That script is **repository-specific**; the rule and this page are the portable contract.

**Template:** See [`scenario-walkthrough-template.md`](scenario-walkthrough-template.md).
