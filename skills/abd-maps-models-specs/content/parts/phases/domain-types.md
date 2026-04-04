# Domain types (`concepts[]`)

**Goal:** **Sparse** types grounded in **full behavioral evidence**; **reject gate** ("not just a property on a broader type").

**Normative for Phase 6:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.

## Prerequisite

`candidate_queue.json` must be **populated** by the mandatory candidate extraction sweep (see [terms-mechanisms.md](terms-mechanisms.md) — Candidate extraction). An empty queue means extraction was skipped — do not proceed.

## Steps

### Step 0 — Read source evidence (mandatory before any decision)

For **each candidate** in the queue, before deciding its fate:

1. **Read `shaped_story_map.json`** — find every story where the candidate appears in `anchor`, `trigger`, `response`, `steps[]`, or `term_refs`. Read the full story context: what actor triggers it, what state the anchor describes, what steps the process follows. Stories reveal behavioral participation that the candidate name alone cannot convey.

2. **Read the original chunk `.md` files** — for every `evidence_chunk_id` cited on the candidate (from the candidate queue, from mechanisms, from the story map), **open and read the actual markdown body**. The chunk text contains domain language, entities, verbs, and relationships that JSON metadata summaries cannot capture. Do not make promotion decisions based on chunk IDs or previews alone.

3. **Read `mechanisms.json`** — find any mechanism whose description names the candidate or whose `realized_by` paths include stories that reference the candidate. Mechanism participation is strong evidence of behavioral contract.

### Step 1 — Decide each candidate via the promotion ledger

Every candidate **must** receive an explicit decision. No candidate may be silently ignored. Record each decision in `promotion_ledger.json` (see [domain-model.md](../library/domain-model.md) — Promotion ledger).

**Decision taxonomy:**

| Decision | When to use | Action on `map-model-spec.json` |
|---|---|---|
| **`promote`** | Entity holds state, makes decisions, has a distinct lifecycle, or owns a behavioral boundary | Add to `concepts[]` with `owns` sentence, evidence chunks, rationale |
| **`absorb`** | Entity is real but has no independent lifecycle — it is a property or operation on an existing concept | Add as property/operation on the absorbing concept; ledger records which concept absorbed it and why |
| **`merge`** | Identity match — same entity, different names. One name survives; the other becomes a synonym | Keep one concept; add alias to `terms_layer.json`; ledger records merge rationale |
| **`extend`** | Specialization — entity is a subtype with distinct behavior that justifies inheritance | Promote child with `Base:Extension` naming and shared `owns`/evidence on subtype; ledger records LSP justification |
| **`defer`** | Insufficient evidence today — but specific trigger for revisiting | Move to deferred section with trigger: "promote when [specific evidence arrives]" |
| **`reject`** | True noise — not a domain entity at all (UI label, implementation detail, etc.) | Ledger records reason; no model change |

**`modeling_kind` weighting (from `context_index.json`):**

Each candidate's `source_chunks[]` carry `modeling_kind` from the context index. Use the composition to bias decisions:

- **Rule-backed** (majority `rule` or `definition` chunks): default bias toward **promote** unless specific absorb/merge/extend rationale exists.
- **Definition-backed** (only `definition`, no `rule`): default bias toward **absorb as term** or **promote** if mechanism coverage exists.
- **Example-only** (all chunks are `example`): default bias toward **defer** — examples illustrate but do not establish behavioral contracts.
- **Mixed** (rule + example): treat as **rule-backed**.

### Step 2 — Record per-type rationale

For each promoted concept, record rationale grounded in the evidence you read in Step 0. Keep type count tractable for the fixture depth.

### Step 3 — Align with domain-model contract

Align prose and JSON with [`domain-model.md`](../library/domain-model.md) (modules, properties, **`Base:Extension`** in `concepts[].name` for inheritance — no separate `extends` field — examples).

**Continual refinement:** For each **promoted** or **absorbed-as-member** concept, **start** the domain-model **class-shaped** block (heading + properties/operations) **where evidence allows** a typed line. Where you only have **`owns`** / rationale, **do not** force placeholder operations — Deepen will fold those into the [domain concept format](../library/domain-model.md#domain-concept). When you **do** add new property/operation lines in this phase, you may suffix **`**newly added**`** on those lines (first appearance in the model narrative).

## Output

- **`promotion_ledger.json`** — persisted alongside `map-model-spec.json`; every candidate from the queue has an entry.
- **Updated `map-model-spec.json`** — promoted concepts added to `concepts[]`; absorbed entities added as properties/operations; merged concepts aliased.

## Exit

- Every candidate in `candidate_queue.json` has a corresponding entry in `promotion_ledger.json`.
- Type count and rationale remain reviewable for the chosen workspace depth.
- No candidate was decided without reading its associated stories, chunk files, and mechanisms (Step 0).
