# Deepen



**Goal:** Responsibilities and evidence on **approved** types only; **topological** `depends_on`.



**Normative for Phase 6:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. Attach evidence citations to approved types; citations **support** claims—they do not **auto-create** types.

1b. **Refine class definitions:** Move narrative-only responsibilities toward the [domain concept format](../library/domain-model.md#domain-concept) — **`- <type> property`** and **`- <type> operation(<param>, ...) → <return>`** with collaborating concepts and **Invariant:** lines where checkable. Mark **`**newly added**`** immediately after each property or operation line **first introduced in this Deepen pass** (or state “unchanged” if the pass only added evidence/`depends_on`).

2. Model `depends_on` where appropriate (acyclic, reviewable). Pin collaborations to **properties** and **operations** once those exist; optional **`concept.depends_on`** only as a **subset** of member-level peers (see **`domain-model.md`** → map-model-spec relationships, rule **`map-model-relationships`**).

3. **Scenario walkthroughs + relationship pass (when in scope):** Author object-flow walkthroughs per **`scenario-walkthrough-template.md`** (**Scope** = epic/story[/scenario] set from the graph files). After each walkthrough’s **Gaps** section, **update `map-model-spec.json`** for in-scope findings ( **`depends_on`**, responsibilities, evidence) per **`scenario-walkthrough-update-spec-on-gap`**, or record deferrals in **`open_questions`** / the candidate queue. **Revisit Step 2** if walks added or changed collaborations. This is the **same Deepen phase** — not deferred to Integrate for first-time edges.



## Exit



Every type has **evidence** citations; relationships follow explicit gates from the principles table.

**Relationships and walkthroughs (when in scope):** For each module or slice you treated as done for Deepen, either (1) **`depends_on`** edges in **`map-model-spec.json`** reference only declared concept names (validated in **`validate`** by **`map-model-relationships`**) and any **scenario walkthrough** for that slice lists **Scope** from the story graph per **`scenario-walkthrough-scope-covers`** and is aligned with **`shaped_story_map.json`** (and any listed second graph) per **`scenario-walkthrough-*** rules, **or** (2) you record an explicit **waiver** / deferral in **`open_questions`** or the candidate queue. Do not finish Deepen with walkthrough prose that contradicts the spec without reconciling.

