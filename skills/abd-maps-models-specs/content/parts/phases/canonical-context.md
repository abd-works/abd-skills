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

# Canonical context layer (Stage 1 — build or freeze the contract)



**Goal:** A **single, versioned** contract for “what evidence is,” independent of map/model/spec JSON.



**Normal path** when `chunks/` are not present yet:



1. **Canonical Markdown** — Declare paths in **`solution.conf` → `manifest_sources[]`** (resolved by `_config.py`). The MM3 fixture lists `docs/HeroesHandbook.md` from **PDF → MD** (or other conversion); pin versions.

2. **Chunking + index** — **Written chunking spec first** (grain, metadata, exclusions), then scripts—aligned with **principles** (provenance-first, evidence typing for promotion gates, explicit noise). See Phase 1 in [`content/parts/process.md`](../process.md) and [`docs/context-corpus.md`](../../../docs/context-corpus.md) *First chunking is more than…*.



If an existing package is **adopted** after [context-readiness](context-readiness.md), this phase **migrates / extends** schema and **freezes** v1.



**Authoritative context:** Phase 1 row in [`content/parts/process.md`](../process.md); this file expands that row.

**Normative file/schema detail:** [`docs/context-package.md`](../../../docs/context-package.md) — chunk front matter, `context_index.json`, chunking spec path from `solution.conf`, validators, single script surface.



---



## 1.1 Artifacts



- `context_index.json` with at minimum: `chunk_id`, `source_anchor`, `modeling_kind`, `evidence_type`, `modeling_priority`, optional `candidate_terms[]`.

- **Rules:** Promotion of `example` / `narrative_aside` / `metadata/noise` into `extends` or `concepts[]` uses an explicit **promotion** record.



---



## 1.2 Validation



- **`scripts/validate_context_contract.py`** — bidirectional alignment: every `blocks[]` row has `chunks/{chunk_id}.md`; every chunk file is indexed or listed under `excluded[]`; required front matter `chunk_id`. Rules evolve with [`docs/context-package.md`](../../../docs/context-package.md).

- **Relationship edges** (e.g. `extends`, `inherits`) enter the model through **explicit** later phases with stated criteria.



---



## 1.3 Exit criteria



- Readiness outcome **documented** ([context-readiness](context-readiness.md)).

- Index schema **frozen** as v1 of the **context package** for this skill.



### 1.4 Where the full schema lives



Phase 1 **provenance** (files, validators, config, runnable pipeline) is specified in [`docs/context-package.md`](../../../docs/context-package.md). Phases 2–3 have their own docs ([`terms-mechanisms-contract.md`](../../../docs/terms-mechanisms-contract.md), [`behavioral-story-map.md`](../../../docs/behavioral-story-map.md)); they are not “extra steps before Phase 1.”



---



**See also:** [`docs/context-corpus.md`](../../../docs/context-corpus.md).

