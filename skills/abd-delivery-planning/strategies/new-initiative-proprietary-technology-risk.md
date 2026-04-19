# Strategy: New Initiative — Proprietary Technology Risk

**When to use:** Heavy proprietary APIs, internal systems, or custom protocols with little public documentation; high model risk. Greenfield or brownfield.

**Typical scope:** Riskiest **thin slices** first; prove each slice with a repeatable **spec → test → code** rhythm before moving on.

---

### Steps (in order)


| Step | Stage                                                           | Intent                                                                                                                                                                                                     | Scope                                                    | Checkpoint policy                       | Rationale                                                             |
| ---- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------- |
| 1    | Discovery                                                       | Map proprietary systems, integration points, undocumented surfaces, candidate stories, and where the model is likely to fail.                                                                              | Proprietary surface and unknowns                         | When map is reviewable                  | See the landscape before committing build order.                      |
| 2    | Prioritization                                                  | **One** pass — **group** under orthogonal **architecture** categories (e.g. integration surface vs data/migration vs security vs ops — not one shared sort order). **Order thin slices** (riskiest first). | Full backlog for ordering                                | Grouping and thin-slice order agreed    | One ordering decision — not separate “prioritizations” per category.  |
| 3a   | **Exploration**                                                 | **Exploration run for this thin slice:** AC (exploration) for the **whole slice** as one unit — so the slice is understood before you drill into stories.                                                  | Current thin slice                                       | After AC for the slice is reviewed      | One exploration pass per slice; slice is the batch.                   |
| 3b   | Story Definition → Acceptance Tests → Engineering               | **One story first:** specification → acceptance test → code; get each gate right before scaling.                                                                                                           | First story in the current thin slice                    | After that story is done                | Proves spec → test → code on real proprietary behavior.               |
| 3c   | Story Definition → Acceptance Tests → Engineering               | **Remaining stories in the epic** (still inside this slice): spec → test → code; same rhythm, **get each gate right** for each story.                                                                      | Other stories in that epic within the current thin slice | Per story (or small batches if stable)  | Drain the epic without skipping gates.                                |
| 3d   | Story Definition → Acceptance Tests → Engineering               | **One-shot finish:** everything **left in the thin slice** (other epics, stragglers) to **close the slice** — spec, test, code as needed in one coordinated push.                                          | Remainder of the current thin slice                      | After slice is closed                   | Clears the slice so you do not drag partial work into the next slice. |
| —    | *(next thin slice)*                                             | Return to **3a** for the next slice, then **3b** → **3c** → **3d** again.                                                                                                                                  | Next thin slice in priority order                        | Same pattern                            | AC for each slice before story-level work.                            |
| 4    | Discovery                                                       | When riskiest slices are proven, **fill in** deferred map areas that were intentionally out of scope (focused map update).                                                                                 | Deferred areas                                           | After update is reviewable              | Broaden coverage once architectural unknowns are largely removed.   |
| 5    | Prioritization *(optional)*                                     | Re-order only if row **4** changed backlog shape materially.                                                                                                                                               | Affected backlog                                         | New order agreed (or skip)              | Same **Stage** as row **2**, different **Intent** / **Scope**.        |
| 6    | Exploration → Story Definition → Acceptance Tests → Engineering | **Backlog tail:** remaining work by **thin slice** or by value; tighten checkpoints for new proprietary touchpoints.                                                                                       | Remaining stories / slices                               | Per slice or per story as risk dictates | Finishes the initiative after core slices are proven.                 |


**Key constraints:**

- Context analysis must list every proprietary/undocumented system — gaps become plan blind spots.
- **Prioritization is one stage:** grouping by **orthogonal architecture categories** is not three separate “prioritization” exercises — it is **one** ordering decision that respects those categories.
- **Exploration** runs **per thin slice** (AC for the slice) before you spec individual stories in that slice.
- **One story** first in each slice (spec → test → code), then **epic remainder**, then **one-shot** rest of slice — **no** skipping gates to “move faster.”
- **Next thin slice** always starts with **Exploration** (AC) for **that** slice again.
- Internal docs must be read before AC for proprietary behavior; do not rely on generic training data.
- Often **combined** with *New Initiative — Business / User Experience Risk* — see **Combining** in [new-initiative-business-user-experience-risk.md](new-initiative-business-user-experience-risk.md).
