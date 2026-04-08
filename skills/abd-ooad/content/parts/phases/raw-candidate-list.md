# Raw candidate list

**Skill:** abd-ooad — **Phase-id:** `raw-candidate-list` (follows **`nouns-verbs-rules-and-states`** in the chronicle).

**What this phase does:** Sort vocabulary into **candidate kinds** — **entities**, **value objects**, **processes**, **policies**, **roles**, **events** — record **why** each candidate matters, early class smell, watch list, and tensions. Update **`term-registry.md`** (**Targets** / **Notes**) and **`terms.md`** under the same anchor modules when needed.

**Focus:** Separation and tensions. Value-object candidates may stay `<< ValueObject >>` / enum / struct until later phases.

---

## Work order (`raw-candidate-list`)

Do **analysis in domain markdown** — **`domain-raw-candidates.md`** (preferred) or **one** tabular file (**`raw-candidate-list.md`** *or* roll-up appended to **`domain-noun-verb.md`**). **Do not** paste the same bucket tables in two places. When the project keeps a class diagram for the slice, update it **after** the markdown matches (**visual twin**).

---

## Deliverables (integrated model — no duplicate tables)

**Preferred:** **`domain-raw-candidates.md`** — every candidate is **`### Name : << kind >>`** under **`## [Anchor module]`**, with **`#### Note :`** lines and **`templates/domain-raw-candidates-template.md`**. Candidate “tables” are **rows in the model** (per class), not a second global grid elsewhere.

**Alternate:** A single **tabular** roll-up (**`raw-candidate-list.md`** *or* appendix to **`domain-noun-verb.md`**) using **`templates/raw-candidate-list-template.md`** — only if the team explicitly wants buckets as one big table. **Do not** also maintain **`domain-raw-candidates.md`** with the **same** bucket blocks repeated.

**Cross-anchor / overflow:** **`## Cross-anchor`** at the **end** of **`domain-raw-candidates.md`** for items that do not fit a module — not a second appendix file with duplicated tables.

**Artifact body:** Domain content only (no skill/process boilerplate in slice files).

---

## Illustrative shape (Check anchor)

From **`domain-noun-verb.md`** (phase-id **`nouns-verbs-rules-and-states`**), re-sort into kinds:

| Kind | Extraction (illustrative) |
|------|---------------------------|
| **Nouns** | Character, Check, DC, bonus, Condition, die roll |
| **Verbs** | roll, compare, apply, succeed, fail |
| **Rules** | Compare total vs DC; bonuses may not stack |
| **States** | Check pending → resolved |

**Buckets (same terms, new shape):**

| Prior term(s) | Likely bucket | Notes |
|-----------------|---------------|-------|
| Character, Check | **Entities** | May merge later. |
| DC, bonus | **Value objects** | VO / enum / struct. |
| roll → resolve | **Processes** | End-to-end flow. |
| stacking, advantage | **Policies** | Modifiers / eligibility. |
| player, GM | **Roles** | Often actors, not classes. |
| “Check resolved” | **Events** | If replay / audit matters. |

Record **tensions** and a **watch list** here; refine in **thing-vs-data-about-a-thing** (Phase 4).

---

## Continual refinement (this phase)

**Delta:** pre-notation — candidate kinds, watch list, tensions; typed members arrive in later phases.

---

## Action Checklist

- Vocabulary rolled into kinds (entities, value objects, processes, policies, roles, events) in **one** chosen artifact — **`domain-raw-candidates.md`** *or* a single tabular file, **not** duplicated.
- Early class smell, watch list, and tensions recorded.
- Entity-like vs value-object hypotheses separated where it matters.
- Tensions noted for **thing-vs-data-about-a-thing** when needed.

---

## Prompt

> When you see bloat, unclear boundaries, missing invariants, naming drift, or spec conflicts, **validate** and **fix** the model (or **map-model-spec.json** / class diagram); record **explicit debt** with a clear follow-up only when you cannot fix yet.
