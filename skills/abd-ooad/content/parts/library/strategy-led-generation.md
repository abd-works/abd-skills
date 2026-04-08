# Strategy-led generation

Domain scan (phase-id **`domain-scan`**) does not only produce a single “results” file. It establishes a **small set of workspace files** under `<workspace>/abd-ooad/` that work together. Some are **frozen findings** from the scan; others are **living documents** you update as modeling continues.

**Per-slice extraction** after scan uses the **same phase-id chronicle** as **`process.md`**. The **first** detailed per-slice capture is **`nouns-verbs-rules-and-states`** (then **`raw-candidate-list`**, …) — **not** a second **`domain-scan`**. Use **phase-id** names in strategy and registry (and **`*[Sn · phase-id]*`** tags in the model), not “Phase 1 / Phase 2” as step names. See **`term-registry.md`** and **`process.md` → Capture ladder**.

For the scan procedure itself, see the **Domain scan** phase. This page explains **what each artifact is for** and how **`strategy.md`** relates to **`domain-scan-results.md`**.

**Checkbox discipline:** Live ticks for pipeline position and phase steps belong only under **`<workspace>/abd-ooad/progress/`** — see **`library/strategy-execution-and-checklists.md`**. Do not put tick tables in `strategy.md`.

---

## The five scan outputs (always)

Created during domain scan under `<workspace>/abd-ooad/`:

| File | Role | Updates after scan? |
|------|------|---------------------|
| `domain-scan-results.md` | **Findings snapshot:** source map, anchor table, tensions. | Rarely — only if you correct a scan error. Do not put the forward plan here; that belongs in `strategy.md`. |
| `strategy.md` | **Living strategy:** **modeling scope**; **§1 source slices** (table: Order, Goal, **Source** — chapters, files, modules, or mixed — **Coverage**, **Importance**); **§2 slice plan** (per-slice **goal restated** + **phases**); **coverage across steps**; **cross-slice integration**; **anchor and subdomain elaboration**; **execution plan (normative)** — phase slugs with **slice IDs** on every line; plus **approach** and **dated pivots**. | **Yes** — whenever scope, order, slice depth, subdomain mapping, or integration changes. |
| `domain-scan-model.md` | Class sketch (markdown) at scan fidelity. | Yes, in later phases — not only during scan. |
| `domain-scan-model.drawio` | Diagram at scan fidelity. | Same as model.md. |
| `term-registry.md` | Terms, **Targets** (bulleted typed pointers), **Notes** — seeded at scan. | **Yes** — every later phase-id updates **Targets** and **Notes** as the model evolves. See **`library/term-registry.md`**. |
| `terms.md` (per slice) | Evidence ledger by **`## [Anchor module]`** — quotes, promotion log. | **Yes** — from **`nouns-verbs-rules-and-states`** onward for that slice. Template: **`templates/terms-template.md`**. |

**Plus** (when workspace is configured): **`progress/`** checklists — see **`library/strategy-execution-and-checklists.md`**. **`generate.py`** creates **`process-checklist.md`**, **`<phase>-checklist.md`**, and (abd-ooad) **`strategy-run-checklist.md`** when templates exist and files are missing. Normative phase steps stay in **`content/parts/phases/<phase>.md`**. These are the **only** place for session tick marks.

Walkthrough diagrams (`.md` / `.drawio`) are **not** required at scan fidelity; they start when the skill’s later phases call for them.

---

## What `strategy.md` is for

- Created at the end of domain scan as a **workspace file**, then **kept current** through extraction and later phases.
- **Purpose:** (1) **scope** — what product or corpus you model; (2) **§1 source slices** — ordered table (**Goal**, **Source**, **Coverage**, **Importance**); **Source** is any locator (chapters, page ranges, repo paths, modules — not only document sections); (3) **§2 slice plan** — per slice, **goal restated** and **phases** (execution steps); (4) **coverage across steps** — matrix proving every in-scope slice is addressed or deferred; (5) **cross-slice integration** — handoffs between slices; (6) **anchor and subdomain elaboration** — attached types (e.g. Ability, Skill, Advantage) mapped to **slice IDs** and execution **§**; (7) **execution plan** — each line names **slice IDs**; breadth steps must **include** subdomain slices in **nouns-verbs** / **raw-candidate-list** where relevant; (8) **Approach** + **Ongoing strategic decisions**. Scan mechanics stay in **`domain-scan-results.md`**.
- **Template:** `templates/strategy.md`. Install as **`strategy.md`** (lowercase; avoid duplicate `STRATEGY.md` on case-insensitive disks).
- After you finalize the execution plan, align **`progress/strategy-run-checklist.md`** with it (same phases and scope); that file holds **checkboxes** for “which phase is done,” while **`strategy.md`** stays **normative text** (no `- [ ]`).

---

## Checklist vs results vs strategy

| Question | Answer |
|----------|--------|
| Where is the source map and anchor list? | `domain-scan-results.md` |
| Where do I define **which slices** exist (chapters, files, modules, …), **depth**, **subdomains per anchor**, and **which phases** hit which? | `strategy.md` → **§1 Source slices**, **§2 Slice plan**, **Coverage across steps**, **Cross-slice integration**, **Anchor and subdomain elaboration**, **Execution plan (normative)** |
| Where do I tick **which phases** we ran, **in order**, with **scope**? | **`abd-ooad/progress/strategy-run-checklist.md`** (keep in sync with `strategy.md`) |
| Where do I tick **full** pipeline position (all phases)? | **`abd-ooad/progress/process-checklist.md`** (optional reference) |
| Where do I tick **steps inside** the current phase? | **`abd-ooad/progress/<phase>-checklist.md`** |
| Where do I tick domain-scan action steps? | **`abd-ooad/progress/domain-scan-checklist.md`** |
| Can I merge checklist into strategy? | **No** — strategy holds the plan; ticks only under **`progress/`** |

---

## Going forward (phases after scan)

1. **Strategy** — Keep **`strategy.md`** aligned with reality; append *Ongoing strategic decisions* when you pivot.
2. **Strategy execution** — Tick **`progress/strategy-run-checklist.md`** as you **complete** each phase for its declared scope.
3. **Phase work** — For the active phase-id, run **`generate.py --phase <phase-id>`** (or **`generate.py --stage <A|B|…|F>`** for a stage) and tick **`progress/<phase-id>-checklist.md`** for action steps.
4. **Registry** — Keep `term-registry.md` aligned with the current phase-id (**Targets** + **Notes**); keep slice **`terms.md`** in sync for verbatim evidence.
5. **Results** — Touch `domain-scan-results.md` only for corrections to the original scan snapshot.

---

## References

- Templates: `templates/domain-scan-results.md`, `templates/strategy.md`, `templates/strategy-run-checklist.md`
- Strategy vs checklists: **`library/strategy-execution-and-checklists.md`**
- Anchors: `anchors` in this library
- Term registry: `term-registry` in this library
- Checklist norm: `library/strategy-execution-and-checklists.md`
