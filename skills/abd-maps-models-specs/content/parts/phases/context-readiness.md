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

# Context readiness (Stage 1 — assessment)



**Goal:** Answer whether the **evidence package** supports downstream modeling **honestly**—traceability, promotion gates, right grain—not to tick a “maturity” box.



**0.1–0.3** are **questions** answered with documents, metrics, and samples—not a numeric “maturity” ladder. If the corpus is **already** inadequate, **record that** and move to **rebuild** ([canonical-context](canonical-context.md), Phase 1 in [`content/parts/process.md`](../process.md)).



When **`chunks/` do not exist yet**, you may **skip** a formal audit; the **same criteria** become **acceptance tests** for the **first** chunking output from Phase 1.



**MM3 fixture (current):** Treat **qualitative spot-check** as **no** (metadata alone does not tell you what **not** to subclass) until a rebuilt package proves otherwise → outcome **insufficient** → **rebuild**.



**Authoritative context:** Phase 0 row in [`content/parts/process.md`](../process.md); this file expands that row.



## Actor



**Human** judges; **Code** may emit metrics (e.g. `scripts/phase0_context_audit.py`) into `test/mm3/abd-maps-models-specs/phase0/`. When `test/mm3/context/context_index.json` exists, **`scripts/validate_context_contract.py`** runs as part of `scripts/build.py` and enforces the **Phase 1 package** ([`docs/context-package.md`](../../../docs/context-package.md)).



---



## 0.1 Map the plumbing



1. **ID mapping** — Document how chunk files relate to index rows (e.g. `unit_*.md` ↔ `blk_*`). If implicit or missing, **record debt**.

2. **Coverage** — Every chunk in the index; every domain-relevant block has a chunk or **explicit** exclusion.

3. **Version pin** — Hash/date for canonical Markdown and for the index **generator** (if known).



---



## 0.2 Corpus profile (quantitative)



Short report — see plan table: counts by `evidence_type`, `reason` distribution, section spread, `%` noise.



---



## 0.3 Qualitative spot-check



Sample **N** chunks (definitions, tables, examples, rules). **Would a modeler know, from metadata alone, what not to subclass?** If **no** → Phase 1 must supply `modeling_kind` (or equivalent) via schema + chunking +/or re-extraction.



---



## 0.4 Outcomes



| Outcome | Action |

| --- | --- |

| **Sufficient** | Adopt / small schema extension; then **freeze** v1 in Phase 1. |

| **Insufficient** | **Rebuild** in Phase 1 (chunking spec from Markdown—often after **PDF → MD**). |



---



## Exit



Readiness **finding** recorded (adopt vs rebuild). If rebuild: Phase 1 produces the new package; **freeze** contract there.



**See also:** [`docs/context-corpus.md`](../../../docs/context-corpus.md).


