<!--
  OOAD STRATEGY — workspace template
  Copy to: <workspace>/abd-ooad/strategy.md
  Canonical filename: strategy.md (lowercase).

  Structure:
  §1 Source slices — *what* we cover, *where* it lives (not always book sections), *priority order*.
  §2 Slice plan — per-slice goal restated + phases (maps to execution steps below).
-->

# OOAD Strategy — {{project_name}}

**Progress and ticks (only place for checkboxes):** [`abd-ooad/progress/`](abd-ooad/progress/) — see **`library/strategy-execution-and-checklists.md`**.

---

## Modeling scope

*High-level engagement outcome. **Detailed slicing** is in **§1** and **§2** below — do not leave chapters, packages, files, or anchors implicit.*

- **Primary focus:** {{e.g. payment reconciliation; anchors Payment + Ledger; module `billing/`}}
- **In scope (summary):** {{one line — full spec, or named product area}}
- **Out of scope for now:** {{explicit deferrals}}
- **Source type:** {{e.g. book chapters \| repo tree \| API specs \| mixed}}

---

## 1. Source slices (coverage order)

*Ordered view of **what** you will model from **which** sources. **Source** is intentionally flexible: book chapters, page ranges, files, directories, services, epics, or code modules. Use stable **slice IDs** (e.g. `S1`, `pkg-auth`, `api-v2`) everywhere: **coverage matrix**, **slice plan**, **execution plan**, **checklists**.*

| Order | Slice ID | Goal | Source | Coverage (this pass) | Importance |
|-------|----------|------|--------|------------------------|------------|
| {{1}} | {{S1}} | {{Why this slice exists — one line}} | {{e.g. Ch.1 — The Basics; or `src/auth/`; or `openapi/payments.yaml` §4–7}} | {{reference-only \| light \| standard \| deep}} | {{High \| Medium \| Low \| narrative why}} |
| {{2}} | {{S2}} | … | … | … | … |

**Column hints:**

- **Order** — Sequence you **prioritize** through the corpus (may differ from document order: e.g. deep-dive **S6** before **S7**).
- **Goal** — Modeling outcome for this slice (vocabulary, anchor, tension, integration point).
- **Source** — Concrete locator: chapter + title, page range, file path(s), module glob, ticket epic — whatever the team uses.
- **Coverage (this pass)** — Same depth scale as **Coverage across steps** below.
- **Importance** — Scan signal, risk, or dependency driver (not duplicate of Coverage).

*Legacy alias:* older strategies called this table **“Section strategy”**; **slice** = one row here.

---

## 2. Slice plan (goal restated + phases)

*Per **slice ID**: restate the goal, then **which execution steps / phase slugs** apply, outputs, and upstream/downstream slices. Order subsections by **Order** above (or by slice ID).*

### {{Slice ID}} — {{short title}}

- **Slice goal (restated):** {{One sentence — same intent as the Goal column in §1, expanded if needed.}}
- **Unit kind:** {{chapter \| directory \| anchor \| module \| file \| API surface \| …}}
- **Phase-ids (execution — use slugs from `process.md`):** {{e.g. `domain-scan`; `nouns-verbs-rules-and-states` → `raw-candidate-list`; …}} — or **stages** (A–F) if you batch by stage.
- **Produces / updates:** {{artifacts, term-registry rows, diagram}}
- **Reads / depends on:** {{other slice IDs}}

*(Repeat one `###` block per in-scope slice.)*

---

## Coverage across steps

*Prove **every** in-scope slice is either touched by a planned execution step or **explicitly deferred**.*

| Slice ID | Touched in execution plan (phase-ids) | Depth this pass | Deferred? |
|----------|----------------------------------------|-----------------|-----------|
| {{S1}} | {{e.g. domain-scan, nouns-verbs-rules-and-states, thing-vs-data-about-a-thing}} | {{light \| standard \| deep \| reference-only}} | {{no — or yes, why}} |

**Depth (pick one per slice for this pass):**

- **reference-only** — Cited by other slices; no dedicated extraction step.
- **light** — Nouns/verbs + raw candidate list at most.
- **standard** — Responsibilities, properties, relationships for types anchored here.
- **deep** — Full vertical slice including validation scenarios / tensions.

---

## Cross-slice integration

*Cross-boundary contracts: shared concepts, call/data direction, ordering constraints **between** slices.*

| From → To | Shared or dependent concept | Rule / handoff |
|-----------|----------------------------|----------------|
| {{S1 → S6}} | {{e.g. DC formula}} | {{e.g. Effect rank must align with Check DC table in S1}} |

*Narrative (optional):* {{1–3 bullets on end-to-end flow across slices.}}

---

## Anchor and subdomain elaboration

*Required when an **anchor** (e.g. `Character`, `Order`) owns **subdomains** — types or packages that attach to it (`Ability`, `Skill`, line items, …). Maps subdomains to **slice IDs** and **execution §** so traits are not “implied by Character” only.*

| Anchor (core class) | Subdomain / attached types | Source slices (IDs) | First elaboration beyond scan (execution §) | Later steps (§) | Notes |
|---------------------|-----------------------------|----------------------|--------------------------------------------|-----------------|-------|
| {{e.g. Character}} | {{Ability, Skill, Advantage}} | {{S3, S4, S5}} | {{e.g. nouns-verbs-rules-and-states + responsibilities-before-operations}} | {{e.g. add-properties-semantically-tight}} | |

**Rules:**

- Every **subdomain row** must map to **at least one phase-id** in the execution plan where nouns/candidates/responsibilities/properties are **explicit** (not only “implied by anchor”).
- **Codebases:** subdomains may be **packages** under an anchor module — same table, different slice IDs.
- If **nouns-verbs** / **raw-candidate-list** names only one slice while others stay at scan fidelity, **widen** those steps’ slice IDs or add **separate execution lines** per subdomain.

---

## Execution plan (normative)

*Ordered **phase-id** strings (same as **`process.md`** chronicle / **`skill-config.json` → `phase_files`**). Each line names **slice IDs**. **No checkboxes here** — ticks in **`progress/strategy-run-checklist.md`**. Align with **§1**, **§2**, **Coverage across steps**, and **Anchor and subdomain elaboration**. You may batch by **stage A–F** using **`generate.py --stage`** — see **`process.md` → Stage map**.*

1. **`domain-scan`** — slices: {{all S\* or listed IDs}} — {{what the scan bounded}}
2. **`nouns-verbs-rules-and-states`** — slices: {{…}} — {{what you extract}}
3. **`raw-candidate-list`** — slices: {{…}} — {{…}}
4. {{continue until the pass is fully described}}

*Patterns:* single vertical slice; package ladder; breadth-then-depth; anchor + subdomains (see template **Anchor** section above).

**Revisits:** If you must go **backward** (e.g. from **`refine-names`** to earlier structure), **do not** create a separate rerun doc — add rows to **`strategy-run-checklist.md`** (see **`library/strategy-execution-and-checklists.md`**).

When this plan changes, update **`strategy-run-checklist.md`**, then log under *Ongoing strategic decisions*.

---

## After each stage (optional but recommended)

*For each **stage A–F** you complete in a pass:*

- **Completed:** {{short bullet — which phase-ids ran}}
- **Tensions / open points:** {{…}}
- **New checklist items:** {{e.g. revisit rows added — or “none”}}
- **Audit:** Append a dated line under *Ongoing strategic decisions* if scope or depth changed.

---

## Approach going forward

*Why this slice order and depth — not a duplicate of `domain-scan-results.md`.*

- **Next focus:** {{slice ID + reason}}
- **Sequencing:** {{what must settle before what}}
- **Defer / skip:** {{slices or phases explicitly later}}

---

## Ongoing strategic decisions

*Dated log when you pivot, re-scope a slice, or change depth.*

### {{YYYY-MM-DD}}

- {{What changed and why}}
