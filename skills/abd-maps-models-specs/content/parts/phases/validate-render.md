# Validate & render



**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on MM3; optional **critic** checklist against the **principles table** in [`principles-and-rules.md`](../library/principles-and-rules.md).



**Normative for Phase 8:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Render reports as configured (paths under fixture output root).

3. Optional: critique pass against [`principles-and-rules.md`](../library/principles-and-rules.md) (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the MM3 fixture at the chosen scope.


