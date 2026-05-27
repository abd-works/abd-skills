# Strategy: New Initiative — Business / User Experience Risk

**When to use:** The main uncertainty is whether the **product is right** for people and operations — not (primarily) whether the tech stack integrates. Signals include: new **user experience**, unclear **domain** language and rules, risky **operational flows**, and **data** that must be **correct in meaning**. Greenfield or brownfield.

**Typical scope:** Riskiest **thin slices** first; prove **experience, domain, operations, and data** with the same **specification → engineering** rhythm as the proprietary-tech strategy.

---

### Steps (in order)

Do rows **top to bottom**. **Outcome assessment** and **discovery revisit** run **only after** a thin slice is **through engineering** (after **3c**); they do not run before the first delivery run.


| Step | Stage | Intent | Scope | Checkpoint policy | Rationale |
| ---- | ----- | ------ | ----- | ----------------- | --------- |
| 1 | Shaping → Discovery | **First journey in detail** (personas, domain, UX IA, blueprint); **thin slices last**. Next 1–2 journeys identified only; rest of map at identification depth | First journey; next 1–2 journeys named; remaining map as needed | Pass is reviewable | Assumptions cluster where uncertainty is highest; slice order in same discovery pass |
| 2 | Exploration | **Exploration for this thin slice:** UL, AC, mockups, arch template for the **whole slice** — stakeholders validate where truth is not in docs | Current thin slice | Slice exploration reviewed (business / ops as needed) | Same batching as *Proprietary Technology Risk* |
| 3a | Specification → Engineering | **One story first:** CRC/spec → tests → implementation on **real** domain and UX | First story in the slice | After that story is done | Tight proof before scaling |
| 3b | Specification → Engineering | **Remaining stories in the epic** in this slice | Other stories in that epic within the slice | Per story (or small batches if stable) | Drain the epic |
| 3c | Specification → Engineering | **One-shot finish:** close the rest of the thin slice | Remainder of the current thin slice | After slice is closed | **Engineering done** for this slice — then **4** and **5** apply |
| 4 | Outcome assessment & validation | **Heavy** check: UX, domain, ops, and data outcomes vs intent — not only that software shipped | Thin slice / journey just delivered | Outcome review complete | **Skill TBD** in this repo; still plan the step |
| 5 | Discovery | **Revisit map** from shipped reality; redefine what’s next | Journeys affected by the completed slice | Remap agreed | Map updates from delivery truth |
| 6 | Discovery *(optional)* | Re-slice / re-order **only if** row **5** changed backlog shape materially | Affected backlog | New order agreed (or skip) | Optional — same stage as row 1, different intent |
| — | *(next thin slice)* | Repeat **2 → 3a–3c**, then **4 → 6**, for the next slice | Next thin slice in priority order | Same pattern | Deliver slice → assess → revisit map → re-slice if needed |


---

### Combining with *Proprietary Technology Risk*

These strategies are **often integrated** in real plans. A thin slice can mix **technical risk** and **business risk**. Use this strategy when business validation dominates; use *Proprietary Technology Risk* when integration dominates; **blend** when both matter. See [new-initiative-proprietary-technology-risk.md](new-initiative-proprietary-technology-risk.md).
