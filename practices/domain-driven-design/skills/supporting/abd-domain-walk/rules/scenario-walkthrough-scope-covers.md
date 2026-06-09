---
rule_id: scenario-walkthrough-scope-covers
---

## Scenario walkthrough: scope covers the graph

**Scope** must be a **declared set** of real nodes from the workspace story graph:

- **Required:** at least one **epic** (or module-level epic in **`map-model-spec.json`**) and **story** that exist in **`shaped_story_map.json`** (at the root of **`output_dir`**). List **exact names** (`epics[].name`, `stories[].name`).
- **Optional:** **sub-epic** and/or **scenario** names when the workspace uses a second graph (e.g. **`docs/story/story-graph.json`**) and the walk targets a specific scenario — same spelling as in that file.

**Covers** (per walk) must relate to **those** nodes: the shaped story’s **trigger** / **response** / **anchor**, and/or the named scenario’s behavior — not a different story’s anchor unless **Scope** explicitly includes both and the walk says which slice is which.

**DO**

- Copy identifiers from the JSON (no paraphrase).
- If the walk only exercises one story but mentions another concept, either add that story to **Scope** or state **cross-cutting** and name the **minimum** extra story node(s) from the graph.

**DON'T**

- Claim coverage of story A while only narrating behavior that belongs to story B without adding B to **Scope** or labeling the walk as a boundary cross-check.
- Invent epic/story/scenario names that do not appear in the graph files you list under Scope.
