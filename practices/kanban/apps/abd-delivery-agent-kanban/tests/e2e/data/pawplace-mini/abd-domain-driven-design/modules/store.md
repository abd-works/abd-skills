## Module: [Store]

Scope: Customer finds a PawPlace store (map, list, distance) and selects a store for click-and-collect checkout. Increment 1 walk-in driver and increment 2 store selection.

**Core terms**:
- store
- store map
- store list
- distance to store
- click-and-collect store

---

**Ref â€” Engagement scope (store finding)**
Source: context/CONTEXT.md
Locator: lines 3–7, 13
Extract: partial
Part: PawPlace product description and walk-in / store spine; out-of-scope note excludes adoption only.

**Ref â€” Increment 1 store outcome**
Source: context/stories/thin-slicing.md
Locator: lines 11–22
Extract: partial
Part: Increment 1 outcome and store-finding story names.

**Ref â€” Find a Store epic**
Source: context/stories/story-graph.json
Locator: epics[0] "Find a Store"
Extract: partial
Part: View Store Map, View Store List, Calculate Distance to Store.

**Ref â€” Click-and-collect store selection**
Source: context/stories/story-graph.json
Locator: epics[2].sub_epics[1] "Checkout & Payment", story "Select Click-and-Collect Store"
Extract: partial
Also relates to: [Order] — store choice gates checkout destination.
