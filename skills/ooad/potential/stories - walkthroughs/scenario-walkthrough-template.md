# Scenario walkthrough (object-flow)

Use this template for **narrative collaboration checks** tied to **`map-model-spec.json`**. **Story / interaction scope** must come from your workspace’s **story graph** (see **Scope** below)—not invented labels. Optional machine-readable index: **`scenario_walkthroughs.json`** under your workspace **`output_dir`** (often next to `map-model-spec.json`) — see [`map-model-relationships-plan.md`](map-model-relationships-plan.md) and [`walkthrough-semantic-alignment.md`](walkthrough-semantic-alignment.md).

---

## Purpose

One or two sentences: what collaboration this walkthrough stress-tests (which graph nodes, which concepts).

## Strategy

How you chose **Scope** (which epics / stories / scenarios) and which concepts you expect to participate.

---

## Walkthrough: &lt;scenario name&gt;

**Scope (required):** A **finite set** of nodes copied **verbatim** from the workspace story graph so reviewers can verify them:

1. **Always** list at least one **epic** and **story** from **`phase3/shaped_story_map.json`** (`epics[].name` → `stories[].name`). That file is the skill’s canonical interaction map (trigger/response, anchor, evidence links).

2. **If** your workspace also maintains a richer graph (e.g. **`docs/story/story-graph.json`** with sub-epics and **scenario** names under stories), list **those** nodes too when the walk is about a specific scenario — same spelling as in that JSON.

**Format (example):**

```text
- Epics: <name>
- Stories: <name> [, <name> …]
- Scenarios (if applicable): <story> / <scenario name> [, …]
- Source files: phase3/shaped_story_map.json [; docs/story/story-graph.json]
```

Do not paraphrase story or scenario titles.

**Language:** Reuse the graph’s **interaction vocabulary** — for shaped stories, **trigger** / **response** **behavior** strings and **anchor**; for BDD scenarios, **scenario name** and step intent. Do **not** introduce parallel product wording unless the walkthrough explicitly maps it to a graph node.

### Walks

Repeat per collaboration slice you want to check.

#### Walk 1 — &lt;short label&gt;

**Covers:** Which responsibility or interaction path this walk exercises (must align with **Scope** nodes — see rule **`scenario-walkthrough-scope-covers`**).

**Object flow** (pseudocode / bullet flow):

```
ActorOrConcept
  -> message or state
  -> CollaboratorConcept
  -> ...
```

**Covers (summary):** One line tying to **`depends_on`** or operations if relevant.

### Gaps

What the flow exposed (missing edge, weak evidence, open question). **If the gap belongs in the spec,** update **`map-model-spec.json`** (and evidence) — do not leave the gap only in prose.

### Model updates

Optional bullets: what changed or should change in the spec after this pass.

---

## Relationship pass (post-walkthrough, still Deepen)

After you finish **Walks** / **Gaps** for this document, **apply discoveries to the relationship graph** in the same Deepen cycle:

1. For each **Gap** that is in scope, patch **`map-model-spec.json`** (`depends_on`, responsibilities, operations) per **`scenario-walkthrough-update-spec-on-gap`**, or record a **deferral** in **`open_questions`** / the candidate queue.
2. Reconcile any new collaborations with **Step 2** in **`phases/deepen.md`** (topological `depends_on`).
3. Do **not** treat **Integrate** as the first time edges appear — Integrate merges and aligns; **Deepen** is where walkthrough findings land in the spec.

---

## Model updates (cross-scenario)

Optional: consolidated **`depends_on`**, rename, or deferrals across walks.
