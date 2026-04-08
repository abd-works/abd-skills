# Term Registry

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At the time of identification, a Term is not committed to a model role — it might become a class, a property, a value type, an association, or nothing at all. The registry tracks Terms as the modeling phases determine what each one actually is.

This is distinct from other uses of "actor" in this domain:
- In MM3E and FoundryVTT, "Actor" has a specific system meaning (a character, creature, or entity in the game world).
- In the registry, everything is a Term until the model says otherwise.

**File:** `<workspace>/abd-ooad/term-registry.md`
**Never embedded** inside step outputs — it lives in its own file and is referenced from each step's model doc.

---

## Step Reference — Short Names

Use these short names in the **Step** column of the registry when adding or updating a row.

| Short Name | Phase | Description |
|-----------|-------|-------------|
| SETUP | workspace-and-config | Workspace initialization |
| SCAN | domain-scan | Source scan and anchor identification |
| NOUNS | nouns-verbs-rules-and-states | Extract nouns, verbs, rules, states |
| CANDS | raw-candidate-list | Raw candidate class list |
| THINGS | thing-vs-data-about-a-thing | Separate things from data-about-things |
| RESP | responsibilities-before-operations | Assign responsibilities |
| PROPS | add-properties-semantically-tight | Add semantically tight properties |
| OPS | turn-verbs-into-operations | Turn verbs into operations |
| RELS | relationships-and-cardinality | Relationships and cardinality |
| INV | invariants-in-the-model | Identify invariants |
| BLOAT | watch-for-bloated-classes | Detect bloated classes |
| ROLES | smashed-abstractions-and-hidden-roles | Uncover hidden roles |
| INHERIT | inheritance-when-behavior-generalizes | Apply inheritance |
| ABST | abstract-classes-and-interfaces | Abstract classes and interfaces |
| COMP | prefer-composition | Prefer composition over inheritance |
| STATES | model-state-transitions | Model state transitions |
| ITER | iterative-refinement | Iterative refinement pass |
| TENSION | tension-as-a-signal | Resolve tensions |
| COHESION | what-changes-together | What changes together |
| VALIDATE | validate-with-scenarios | Validate with scenarios |
| NAMES | refine-names | Refine class and concept names |
| LAYERS | model-in-layers | Model in layers |

---

## Slices and global phase numbers (normative)

The **OOAD process table** (see **`process.md`** / built **AGENTS.md** — “Process Table”) assigns **global phase numbers** **0–21** to phase **slugs** (e.g. **Phase 2** = `nouns-verbs-rules-and-states`, **Phase 3** = `raw-candidate-list`, **Phase 4** = `thing-vs-data-about-a-thing`).

- **Phase 1** (`domain-scan`, short name **SCAN**) runs **once per workspace** (or once per strategy engagement). It produces anchors, `strategy.md`, `domain-scan-results.md`, and seeds **`term-registry.md`**. It is **not** repeated as “each slice’s Phase 1.”
- **Per-slice modeling** (folders or **Anchor** columns **`S1=…`**, **`S2=…`**, …) **aligns with the same global numbers from Phase 2 onward:** the **first** extraction artifact in a slice is always **Phase 2** (**NOUNS**), then **3** (**CANDS**), **4** (**THINGS**), etc. Do **not** label slice-local nouns-verbs files as Phase 1 — that collides with **SCAN**.
- **Phase notes** in italics (optional): `*[Sn · Phase N]*` where **N** is the **global** process-table number. Add slug, tension id, or short reminder *after* the tag on the same line if needed (e.g. *thing-vs-data*, *registry Tn*). For early “likely class” judgments: `*[S1 · Phase 3]* Likely class : …`.

---

## Registry Columns

| Column | Values | Notes |
|--------|--------|-------|
| **Term** | Concept name from the source | Exact word or phrase as found — rename in the NAMES step if needed |
| **Classification** | See **Classification** below | **What we want to model this as** — target shape in the domain model (not lifecycle) |
| **Step** | Short name from table above (SCAN, NOUNS, …) | Step that first identified or last materially updated this Term |
| **Confidence** | High / Medium / Low | How sure we are this belongs in the model |
| **Status** | See **Status (OOAD scale)** below | Where this Term sits in the modeling workflow |
| **Notes** | Free text | Anchor-test results, owning module for supporting classes (`Supporting class — X module`), competing interpretations, pointers to tensions in `domain-scan-results.md`, and follow-ups |

---

## Classification — what we want to model this as

Use **one** value per row. This is the **intended model role**, not how “mature” the idea is (that is **Status**).

| Value | Meaning |
|--------|---------|
| **anchor (class + module)** | Passes the anchor test: this concept is a **core class** and owns a **module** (dashed frame + same-named core class). Use only for backbone modules. |
| **class** | A domain **class** that is not its own module yet — e.g. supporting class inside a frame, or a type you expect to become a class without its own module. |
| **property** | Modeled as a **semantic property** (attribute / value on a class), not a separate type. |
| **field** | Modeled as a **typed field / slot** (data member, possibly simple type or value object). |
| **example (instance)** | An **illustrative instance**, sample, or scenario object — not a type in the model. |
| **relationship** | An **association**, link, or dependency between concepts — may become an association, association class, or navigable role. |
| **invariant (rule)** | A **domain rule**, constraint, or policy — often becomes behavior, guard, or explicit rule text on a class. |

**Diagram mapping (when relevant):** `anchor (class + module)` → module frame + core class; `class` → class box; `relationship` → association; `invariant (rule)` → note, constraint, or operation; `property` / `field` → attributes on a class.

---

## Status (OOAD scale)

**Status** is **lifecycle / confidence in the workflow**, not the model shape. Pick the value that best fits; states are **not** always a strict left-to-right pipeline.

| Status | When to use |
|--------|-------------|
| **Ambiguous** | You cannot yet say what the Term is or how it sits next to others. |
| **Tension** | Competing interpretations, overlapping boundaries, or conflicting source pulls — needs resolution before the model can commit. |
| **Candidate** | Plausible model role; narrowed but not yet locked (often after scan, before THINGS/RELS). |
| **Deferred** | Explicitly parked — revisit in a named later step or phase. |
| **Active** | In current modeling scope; being updated in this pass. |
| **Solidified** | Named, placed, and stable in the model for the current iteration — ready to treat as “done” unless source or scope changes. |

**Typical (non-binding) progression:** Ambiguous → Tension or Candidate → Active → Solidified. **Deferred** can apply after any stage. A Term can return from Deferred to Active when scope returns to it.

---

## Registry format (wide Notes)

**Prefer an HTML `<table>` with `<colgroup>`** so the **Notes** column gets most of the width (~50–55%). **Classification** labels can be long — give that column ~12–14% if needed. Plain Markdown pipe tables allocate columns evenly and make long Notes hard to read in the editor and in preview.

Use this skeleton (adjust `width` percentages if needed):

```html
<table>
<colgroup>
  <col style="width:9%" />
  <col style="width:14%" />
  <col style="width:6%" />
  <col style="width:9%" />
  <col style="width:9%" />
  <col style="width:53%" />
</colgroup>
<thead>
<tr>
  <th>Term</th>
  <th>Classification</th>
  <th>Step</th>
  <th>Confidence</th>
  <th>Status</th>
  <th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
  <td>Character</td>
  <td>anchor (class + module)</td>
  <td>SCAN</td>
  <td>High</td>
  <td>Active</td>
  <td>Central entity; all rules attach to it</td>
</tr>
<tr>
  <td>Power</td>
  <td>class</td>
  <td>SCAN</td>
  <td>High</td>
  <td>Active</td>
  <td>Supporting class — Character module. Core capability unit.</td>
</tr>
<tr>
  <td>Device</td>
  <td>class</td>
  <td>SCAN</td>
  <td>Medium</td>
  <td>Tension</td>
  <td>Removable Power vs Equipment? Boundary unclear — see T2.</td>
</tr>
</tbody>
</table>
```

For very small registries only, a Markdown pipe table is acceptable:

```markdown
| Term | Classification | Step | Confidence | Status | Notes |
|------|----------------|------|------------|--------|-------|
| Character | anchor (class + module) | SCAN | High | Active | Short note only |
```
