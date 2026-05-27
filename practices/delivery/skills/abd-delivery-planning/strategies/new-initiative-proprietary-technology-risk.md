# Strategy: New Initiative — Proprietary Technology Risk

**When to use:** Heavy proprietary APIs, internal systems, or custom protocols with little public documentation; high model risk. Greenfield or brownfield.

**Typical scope:** Riskiest **thin slices** first; prove each slice with a repeatable **specification → engineering** rhythm before moving on.

---

### Steps (in order)


| Step | Stage | Intent | Scope | Checkpoint policy | Rationale |
| ---- | ----- | ------ | ----- | ----------------- | --------- |
| 1 | Shaping → Discovery | Map proprietary surfaces; full discovery pass with **thin slices ordered last** | Proprietary surface and unknowns | When map + slice order is reviewable | Landscape before build order |
| 2 | Exploration | **Exploration for this thin slice:** UL, AC, mockups, arch template for the **whole slice** before story-level spec | Current thin slice | After slice exploration is reviewed | One exploration pass per slice |
| 3a | Specification → Engineering | **One story first:** CRC/spec → acceptance tests → implementation; get each gate right | First story in the current thin slice | After that story is done | Proves spec → engineering on real proprietary behavior |
| 3b | Specification → Engineering | **Remaining stories in the epic** in this slice: same rhythm per story | Other stories in that epic within the slice | Per story (or small batches if stable) | Drain the epic without skipping gates |
| 3c | Specification → Engineering | **One-shot finish:** everything **left in the thin slice** to close it | Remainder of the current thin slice | After slice is closed | No partial carryover to the next slice |
| — | *(next thin slice)* | Return to **Exploration** for the next slice, then **3a → 3b → 3c** | Next thin slice in priority order | Same pattern | Exploration per slice before story work |
| 4 | Discovery | When riskiest slices are proven, **fill in** deferred map areas | Deferred areas | After update is reviewable | Broaden once unknowns are largely removed |
| 5 | Discovery *(optional)* | Re-slice / re-order only if row **4** changed backlog shape materially | Affected backlog | New order agreed (or skip) | Same stage as row 1, different intent |
| 6 | Exploration → Specification → Engineering | **Backlog tail** by thin slice or value; tighten checkpoints for new proprietary touchpoints | Remaining stories / slices | Per slice or per story as risk dictates | Finish initiative after core slices proven |


**Key constraints:**

- Context analysis must list every proprietary/undocumented system — gaps become plan blind spots.
- **Thin slicing is one discovery outcome** — grouping by orthogonal architecture categories is **one** ordering decision, not multiple prioritization passes.
- **Exploration** runs **per thin slice** before specification for individual stories in that slice.
- **One story** first (spec → engineering), then **epic remainder**, then **one-shot** rest of slice — no skipping gates.
- Internal docs must be read before AC for proprietary behavior; do not rely on generic training data.
- Often **combined** with *New Initiative — Business / User Experience Risk* — see **Combining** in [new-initiative-business-user-experience-risk.md](new-initiative-business-user-experience-risk.md).
