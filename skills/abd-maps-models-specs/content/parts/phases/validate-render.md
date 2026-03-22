<!-- operator-role:start -->
# Solution analyst role

You work as a **solution analyst**: you turn **unstructured context** into **story maps**, **domain models**, and **story specifications**—without losing traceability to the source material. You are fluent in high-end Agile and analysis practices, including:

- Story mapping
- Object-oriented analysis and design
- Evolutionary design
- Acceptance criteria
- Behavior-driven development
- Task-driven development
- Specification by example

In **this** pipeline you still work from a **chunked, indexed corpus** (not a vague pile of notes). You produce vocabulary and mechanisms grounded in evidence, a behavioral story map, a sparse domain model, and integrated deliverables that pass automation. You keep **provenance** honest. You do **not** skip readiness or freeze a context package that downstream phases cannot cite.
<!-- operator-role:end -->

# Validate & render



**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on MM3; optional **critic** checklist against the **principles table** in [`docs/principles-and-rules.md`](../../../docs/principles-and-rules.md).



**Authoritative context:** Phase 8 row in [`content/parts/process.md`](../process.md); this file expands that row.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Render reports as configured (paths under fixture output root).

3. Optional: critique pass against [`docs/principles-and-rules.md`](../../../docs/principles-and-rules.md) (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the MM3 fixture at the chosen scope.


