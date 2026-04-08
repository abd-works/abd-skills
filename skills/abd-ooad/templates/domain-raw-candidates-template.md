# {{SliceLabel}}: Raw candidates

## What this file is

A **single integrated domain model** for the slice: candidates appear as **classes** under **`## [AnchorName] module`**, not as separate Phase 3 bucket tables.

**Candidate kinds** (pick one stereotype per class, or `<< >>` if still open):

| Kind | Stereotype in the heading |
| ---- | ------------------------- |
| Entity | `<< Entity >>` |
| Value object | `<< ValueObject >>` |
| Process | `<< Process >>` |
| Policy | `<< Policy >>` |
| Role | `<< Role >>` |
| Event | `<< Event >>` |

**Do not** use **bucket tables** (entities | value objects | processes | policies | roles | events) as a separate artifact, and do **not** append them to the bottom of **`domain-noun-verb.md`**. That tabular Phase 3 path is **retired**. Integrated Phase 3 is **only** this file: **`### ClassName : << kind >>`** under **`## [AnchorName] module`**, with **`#### Note :`** (typed lines per below). Nothing to “paste in” from another roll-up doc.

---

## Note lines under `#### Note :` (required shape)

One pattern for **every** note line — no variants, no shorthand:

1. **`[{{SliceId}} · Phase n]`** in italics first (slice + phase tag).
2. Then the **label** (`Trace`, `Evidence`, `Tension`, or `Does it deserve a class?`).
3. Then **`—`** and the prose.

**`*[{{SliceId}} · Phase n]* Trace — …`**  
**`*[{{SliceId}} · Phase n]* Evidence — …`**  
**`*[{{SliceId}} · Phase n]* Tension — …`**  
**`*[{{SliceId}} · Phase n]* Does it deserve a class? — …`**

**Wrong (label before slice — do not use):** `*Trace — [{{SliceId}} · Phase n]* — …`, `*Evidence — [{{SliceId}} · Phase n]* — …`, `*Tension — [{{SliceId}} · Phase n]* — …`, `*Does it deserve a class? — [{{SliceId}} · Phase n]* — …`

**Wrong:** `*[{{SliceId}} · Phase n]* — …` with **no** label after the bracket (every line names its kind).

| Note kind | Lead-in (only valid shape) | Typical source of the content |
| --------- | --------------------------- | ------------------------------ |
| **Trace** | `*[{{SliceId}} · Phase 2]* Trace — …` or `*[{{SliceId}} · Phase 3]* Trace — …` | Phase 2 **`domain-noun-verb.md`** or Phase 3 integrated judgment. |
| **Class decision** | `*[{{SliceId}} · Phase 3]* Does it deserve a class? — …` | Phase 3 judgment in this file + Phase 2 **`domain-noun-verb.md`** Candidate blocks. |
| **Evidence** | `*[{{SliceId}} · Phase 2]* Evidence — …` (use Phase 3 in the bracket if the cite exists only in integrated work) | Pointer or verbatim cite to **`domain-noun-verb.md`**, manual, spec, or code (path + §). |
| **Tension** | `*[{{SliceId}} · Phase 3]* Tension — …` (Phase **2** in the bracket if the fork appeared in noun-verb / scan first) | **`term-registry.md`** (**T1** / **T3**), **`domain-scan-model.md`**, or shared term across classes. **Same** `*[{{SliceId}} · Phase n]* Tension —` lead-in on **each** owning class. |

**Tension** lines must include the word **`Tension`** after **`[slice · phase]`** — never a bare `*[S# · Phase n]* — …` for a fork, and never **`*Tension — [S# · Phase n]*`**.

Do **not** duplicate tensions in a tail **index table** at EOF — workshop or **`term-registry.md`** can hold cross-file indexes; this file stays domain + typed notes only.

**Appendix / cross-anchor:** Use **`## Cross-anchor`** for a **watch list** only (candidates that may collapse to narrative). Avoid **`## Appendix A`** unless something truly cannot live under a class.

**Do not** put skill/process boilerplate in this file (see **`SKILL.md`**).

---

## [{{AnchorName}} module]

### {{ClassName}} : << {{Stereotype}} >>

+ {{property}}: {{Type}}  
  Invariant: …
+ {{method}}({{params}}): {{Type}}  
  Invariant: …

#### Note :

- *[{{SliceId}} · Phase 3]* Trace — …
- *[{{SliceId}} · Phase 2]* Trace — …
- *[{{SliceId}} · Phase 3]* Does it deserve a class? — …
- *[{{SliceId}} · Phase 2]* Evidence — …
- *[{{SliceId}} · Phase 3]* Tension — … *(repeat the same slice·phase + Tension lead-in on each owning class)*

---

### {{ClassName}} : << {{Stereotype}} >>

- {{member}}: {{Type}}

#### Note :

- *[{{SliceId}} · Phase 3]* Trace — …
- *[{{SliceId}} · Phase 3]* Tension — … *(only if this class owns part of a fork)*

---

## Cross-anchor

*Watch list only; notes use **`*[S# · Phase n]* <label> —`** on classes above.*

- …

---

## Appendix A — {{AppendixTitle}} (optional)

*Rare. Prefer the same **`*[S# · Phase n]* <label> —`** pattern under class **`#### Note :`**.*

- …
