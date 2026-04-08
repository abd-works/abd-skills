# {{SliceLabel}}: Raw candidates

## What this file is

One **integrated domain model** for the slice: candidates are **`### ClassName : << kind >>`** under **`## [AnchorName] module`**, not separate global bucket tables.

**Kinds:** `<< Entity >>` | `<< ValueObject >>` | `<< Process >>` | `<< Policy >>` | `<< Role >>` | `<< Event >>` | `<< >>` (open).

**Tables:** Put table-shaped facts **on the class** they belong to. If a table truly spans anchors, use **`## Cross-anchor`** at the **bottom** of this file — do **not** duplicate the same rows under multiple modules.

---

## Note lines under `#### Note :`

Lead with a **phase tag in italics**, then prose.

- General: **`*[{{SliceId}} · Phase 3]*`** — then your sentence (tension, evidence, trace, or **`*[{{SliceId}} · Phase 3]* Likely class : …`** for early class judgment — see **`term-registry`**).

Keep **`term-registry.md`** as the cross-file index; do **not** add a second “master tension table” at EOF here.

---

## [{{AnchorName}} module]

### {{ClassName}} : << {{Stereotype}} >>

+ {{property}}: {{Type}}  
  Invariant: …

#### Note :

- *[{{SliceId}} · Phase 3]* …

---

## Cross-anchor

*Only for items that do not fit a single module.*

- …
