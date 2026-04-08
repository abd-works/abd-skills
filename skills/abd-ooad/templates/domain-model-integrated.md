<!--
  Integrated domain model (structural) — parallel to terms.md by module
  Copy per slice or workspace as your layout requires.
-->

<!--
  Slice: {{slice_id}}
  Last stage completed: {{e.g. D}}
  terms.md: {{path/to/slice/terms.md}}
-->

# Domain model — {{project_or_slice_name}}

**Companion evidence:** **`terms.md`** (same **`## [Anchor module]`** order as this file). **Registry:** `term-registry.md` (term-centric **Targets** + **Notes**).

**Markers:** Under **`#### Note :`**, use **one** puncture-test line plus **`*[Sn · phase-id]*`** (e.g. **`*[S1 · refine-names]*`**) — **phase-id** from **`process.md`**, not a numeric step. Optional HTML comment for grep: `<!-- stage:D -->`.

---

## [{{Anchor module name}}]

### {{ClassName}} : << {{Entity|Value object|…}} >>

#### Properties

| Name | Type | Note |
|------|------|------|
| … | … | … |

#### Operations

- …

#### Invariants

- …

#### Note :

- *{{One puncture-test sentence — why VO vs property vs entity.}}* *[{{Sn}} · {{phase-id}}]*
- → Evidence / quotes: `terms.md#{{anchor-module-heading}}` / term *{{name}}* — do not duplicate verbatim paragraphs here.

---

## [{{Next anchor module}}]

…
