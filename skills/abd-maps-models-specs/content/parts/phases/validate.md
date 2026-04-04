# Validate



**Goal:** Automated checks (scanners, schema) + **manifest and pipeline outputs** (e.g. `context_bundle_manifest.json` from `build.py`); CI on your configured workspace; optional **critic** checklist against the **principles table** in [`principles.md`](../library/principles.md) and applicable **`rules/`** for the scope. (This phase is **not** DrawIO or other diagram rendering; see [`shaped-story-map.md`](../library/shaped-story-map.md).)



**Normative for Phase 10:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Emit manifest and other pipeline outputs as configured (paths under your workspace `output_dir` / fixture root).

3. Optional: critique pass against [`principles.md`](../library/principles.md) and phase **Rules** / `rules/` (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the chosen workspace at the chosen scope.


