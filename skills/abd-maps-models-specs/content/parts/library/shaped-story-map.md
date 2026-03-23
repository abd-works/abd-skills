# Shaped story map

Enduring reference for Phase 3 **`shaped_story_map.json`**: epics and stories expressed as **actor → behavior → anchor**, with traceability to the chunked corpus. The **prose** interaction tree (epic → scenario → step, Trigger/Response wording) lives in [`story-map.md`](story-map.md).

See [`content/parts/process.md`](../content/parts/process.md) and [`principles.md`](principles.md).

---

## Purpose

The **shaped story map** is the JSON projection of the same interaction ideas as [`story-map.md`](story-map.md): **who** does **what**, **which** domain state or read path is involved (**anchor**), and **evidence** for substantive claims. It lands **before** sparse **`concepts[]`** so capability stays **behavior- and evidence-first**, not type-first.

---

## What goes in the shaped story map

- **Epics** — Group stories; naming and scope follow the same discipline as [`story-map.md`](story-map.md) (capabilities, verb–noun stories, real domain language).
- **Stories** — The backbone unit: each story states **anchor**, **trigger** / **response** (actor + behavior), optional links to Phase 2 **terms**, and **evidence** where the story is substantive.
- **Out of scope here** — Implementation (APIs, services, UI). This file is the **shape** of the Phase 3 artifact, not deployment detail.

Stories must **not** exist solely to match strings in a future type list.

---

## Artifact location

**Path:** `phase3/shaped_story_map.json` under the workspace’s configured output root (`OUT_ROOT` from `solution.conf` → `output_dir`, conventionally `<skill_name>/`). The repo’s bundled example workspace uses `test/sample-workspace/` when `conf/abd-config.json` points there.

---

## JSON shape (minimal contract)

- **`schema_version`** — When your pipeline or generators require a version stamp.
- **`epics[]`** — Each epic has a name and **`stories[]`**. Nested sub-epics or extra grouping levels are allowed **per project convention** as long as stories remain the unit that carries **anchor** + **trigger** / **response**.
- Each **story** includes at minimum:
  - **`name`**
  - **`anchor`** — What state or projection is read, passed, forwarded, written, or which constraint applies. Stories need a clear anchor; **query/read/forward** paths are first-class (mutation is not required).
  - **`trigger`** — Object `{ "actor": "<string>", "behavior": "<string>" }`: who starts the interaction and what they do. Fold qualifying state into **behavior** text (and examples elsewhere), not parallel “state” fields.
  - **`response`** — Object `{ "actor": "<string>", "behavior": "<string>" }`: who responds and what they do.
  - **`term_refs`** — Optional strings referencing Phase 2 terms where the story depends on shared vocabulary.
  - **`evidence_chunk_ids[]`** — For **substantive** stories: cite at least one **`chunk_id`** that exists in Phase 1 **`context_index.json`** / chunk set.

**Legacy:** Older files may use top-level **`actor`** / **`behavior`** on a story instead of nested **trigger** / **response**. Prefer **trigger** / **response** for new work.

---

## Alignment with [`story-map.md`](story-map.md)

**Trigger** and **response** in JSON correspond to prose **Trigger** and **Response** (triggering actor + behavior, responding actor + behavior). The shaped story map does **not** introduce separate “triggering state” / “resulting state” JSON fields—state is carried in **anchor** and **behavior** text, consistent with the interaction-tree spec.

**Phase 3 JSON** uses the same pairing as the prose examples in [`story-map.md`](story-map.md) (see **Example 1** and **Per Interaction** there).

---

## Why story shaping before domain types

The full rationale (interaction tree + ordering) is in [`story-map.md`](story-map.md#why-story-mapping-before-domain-types) under **Why story mapping before domain types**. This document defines the **Phase 3 JSON artifact**; that section defines **why** the pipeline orders story shaping before **`concepts[]`**.

---

## Validation checklist

**Epics**

- **`epics[]`** present at the top level; epic names read as capabilities, not empty buckets.
- Nested structure (sub-epics, etc.) matches your project convention and still rolls up to **stories** that carry the fields below.

**Each substantive story**

- **`name`** — Behaviorally legible; not a vague label or a type name pasted as a title.
- **`anchor`** — Declares what is read, written, queried, forwarded, or constrained; silent or anchor-free “stories” fail intent.
- **`trigger`** / **`response`** — Each `{ "actor", "behavior" }` (or accepted legacy **`actor`** / **`behavior`**); **behavior** uses domain language; no extra parallel state columns.
- **`evidence_chunk_ids[]`** — At least one id for substantive stories; each id must correspond to the Phase 1 corpus (same package downstream phases cite).
- **`term_refs[]`** — Present when the story depends on Phase 2 terms; omit when not applicable.

**Quality**

- No story exists **only** to align with a **`concepts[]`** row or a heading string.
- **Query/read/forward** stories are as valid as mutating stories when **anchor** is explicit.
- The map reads as **capabilities and interactions**, not a noun checklist.
