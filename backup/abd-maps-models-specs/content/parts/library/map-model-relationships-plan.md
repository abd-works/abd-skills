# Plan — domain relationships and collaboration validation

**Status:** Implemented in the skill repo — rule **`map-model-relationships`** + scanner, four **`scenario-walkthrough-***` rules, template, example sidecar under the active workspace’s **`spec/.../maps-models-specs/`**, **`skill-config.json`** bindings, **`process.md`** / **`phases/deepen.md`** exit text.

**Source of truth for this initiative.** The skill pipeline phases below are **`generate_prompt.py` slugs** and match **`content/parts/process.md`** (Stage 3–4: Deepen → Integrate → Validate).

---

## 1. What the pipeline phases do (this thread)

This is the mapping we kept circling: **relationship work is not one blob** — it **splits across phases**.

| Process # | Phase slug | `generate_prompt --phase …` | Relationships & collaboration — **practitioner work** |
|-----------|------------|------------------------------|------------------------------------------------------|
| **8** | **`deepen`** | `deepen` | **Author** **`depends_on`** and cross-concept edges in **`map-model-spec.json`**. **Write scenario walkthroughs** (object-flow; **Scope** = explicit epic/story[/scenario] set from **`shaped_story_map.json`** and, if used, e.g. **`docs/story/story-graph.json`**). **Walks + Gaps** → patch spec (**`scenario-walkthrough-update-spec-on-gap`**) then **revisit `depends_on`** in the same phase. **Optional** sidecar **`spec/maps-models-specs/scenario_walkthroughs.json`** (Option B). **Cite `chunk_id`** when adding claims. Exit: relationships + collaboration depth addressed for in-scope concepts **or** explicit waiver. |
| **9** | **`integrate`** | `integrate` | **Reconcile** one coherent **`map-model-spec`**: synonyms, references, drained candidate queue. **Align** walkthrough narrative / sidecar with merged spec. **Do not** treat Integrate as “first time you think about edges” — edges should be argued in Deepen. |
| **10** | **`validate`** | `validate` | Run **`python scripts/build.py`** (full pipeline). **Structural gate:** once implemented, **`map_model_relationships`** scanner **fails the build** if **`depends_on`** / module concept refs **don’t resolve**. Reports, manifest, CI. |

| Mechanism | Validates | Fails when |
|-----------|-----------|------------|
| **Declared graph** (scanner) | JSON **`depends_on`** graph | Dangling concept name; **subset sync** when class-level + members exist; optional reachability/orphan per rule |
| **Scenario walkthrough** (rules + prose) | Story-level **collaboration plausibility** | Walkthrough shows gap → **update spec** (and evidence) before signing off Deepen |

**Why you need both:** Passing **validate** (graph) only means **names resolve**. Passing **Deepen** walkthrough review means **behavior** across those names is **argued**. Neither replaces the other.

---

## 2. Skill implementation order (maintainers — build the gates)

Do this **sequence** to ship the plan into the repo.

### Structural graph (automated in `build.py`)

| Step | Action | Proof |
|------|--------|--------|
| **S1** | Add **`rules/map-model-relationships.md`** | Rule file merged |
| **S2** | Add **`scripts/scanners/map_model_relationships.py`** | Non-zero exit on bad spec; test or sample workspace |
| **S3** | **`rules/scanners.json`** + **`skill-config.json`** (`build_pipeline`, **`phase_rules`** for **`validate`**, optionally **`integrate`**) | `build.py` invokes scanner |
| **S4** | Run **`build.py`** on **sample-workspace** / **abd-answers** spec; fix spec or scanner | Green or documented waivers |
| **S5** | **`domain-model.md`** — what the scanner enforces | Short paragraph + **pre/post-property** and **subset sync** (`depends_on` on members vs optional class-level summary) |

### Narrative walkthroughs (rules inlined into **`deepen`**)

| Step | Action | Proof |
|------|--------|--------|
| **N1** | **`content/parts/library/scenario-walkthrough-template.md`** | File exists |
| **N2** | Example **`scenario_walkthroughs.json`** beside **`map-model-spec`** path pattern | Valid JSON |
| **N3** | Four rules: align-spec, trace-complete, scope-covers, update-spec-on-gap | Four **`rules/*.md`** |
| **N4** | **`skill-config.json`** → **`phase_rules.deepen`** (+ **`integrate`** if needed) | `generate_prompt --phase deepen` inlines rules |
| **N5** | **`process.md`** + **`phases/deepen.md`** — **exit criteria** tied to §1 table | Prescriptive text |
| **N6** | **`python scripts/build.py --merge-only`** | Built bundles updated |

**Recommended order:** **S1→S5** first, then **N1→N6**. (Parallel possible after S1.)

### Optional later

| Step | Action |
|------|--------|
| **O1** | Walkthrough **coverage** scanner + binding + **`validate`** |

---

## 3. Done (definition)

1. **`build.py`** fails on unresolved **`depends_on`** (per **S3–S4**).
2. Template + four rules + sidecar pattern exist (**N1–N2–N3**); **`deepen`** bundle includes walkthrough rules (**N4**).
3. **§1** is reflected in **`process.md`** / **`deepen.md`** exit criteria (**N5**).

---

## 4. Why the model “missed” this (and how you beat that)

- **Conversation context is not reliable storage.** Put the **phase mapping** (§1) **only** in this file (and process/deepen when edited). Re-open this file or paste §1 at the start of a session when driving implementation.
- **Optional:** Cursor **project rule** one line: “When changing relationships or walkthroughs for abd-maps-models-specs, follow **`content/parts/library/map-model-relationships-plan.md`** §1.”

---

## 5. Existing scanners (unchanged)

`stage-1-context-decisions`, `shaped-story-shape`, `evidence-citations-required` — they do **not** replace the graph scanner or walkthrough rules.

---

## 6. Out of scope

CRC **bot** / **agile_bots** `story-graph.json` as SoT for this skill. Replacing **`chunk_id`** with walkthrough prose.

---

## See also

- `[process.md](../process.md)` — full pipeline table
- `[domain-model.md](domain-model.md)`
- `[../rules/scanners.json](../../rules/scanners.json)`
