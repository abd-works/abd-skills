# Strategy: New Thin Slice

**When to use:** Medium-to-large change on an existing solution: new stories, maybe a new sub-epic; cuts across features or layers (e.g. new payment method, new role, new integration).

**Typical scope:** ~5–15 stories forming one vertical slice.

**Pass shape:** **Discovery** in one pass — extend the map, then **thin-slice last** (`abd-thin-slicing` after domain, story, UX IA, and blueprint align). Then **explore one epic at a time**, then **specification → engineering** story-by-story for that epic, then handle **everything remaining** with **exploration → specification → engineering** per chunk.


| Step | Stage | Intent | Scope | Checkpoint policy | Rationale |
| ---- | ----- | ------ | ----- | ----------------- | --------- |
| 1 | Discovery | **Single pass:** extend full map (domain, story, UX IA, blueprint), then **order thin slices** — one checkpoint after discovery completes | New stories + slice boundaries | **After discovery completes** — not mid-pass between map and slicing | Coherent map + slice order before exploration or build |
| 2 | Exploration | **One epic’s worth:** UL refresh, AC, mockups, arch template for **all stories in the first epic** in the slice | First epic inside the thin slice | After that **entire epic** is explored to the agreed bar | Batch exploration per epic |
| 3 | Specification → Engineering | **Prove the pipeline on one story:** CRC/spec scenarios → acceptance tests → implementation | First story in that epic | After that story is done | Tight proof before repeating |
| 4 | Specification → Engineering | **Finish the epic:** same chain for **each remaining story** in that epic | Remaining stories in that epic | Per-story or small batches | Drain the epic with a stable pattern |
| 5 | Exploration → Specification → Engineering | **Everything left** in the slice — per epic/chunk: explore, then spec → engineering for each story | Remaining epics and stories in thin slice | Per-epic exploration where helpful; per-story spec → engineering | Full vertical depth for backlog outside the first epic |


**Key constraints:**

- The thin slice stays **end-to-end** (UI, API, logic, persistence) — row 1 must not define a horizontal-only increment.
- Do **not** checkpoint between full map and thin-slicing within discovery unless the user explicitly wants a mid-pass stop.
- If row 1 changes existing upstream stories or AC, do it openly — no silent forks.
- Assign **Business Expert**, **UX Designer**, and **Engineer** extension slots in discovery per [discovery.md](../../../content/stages/discovery.md).
