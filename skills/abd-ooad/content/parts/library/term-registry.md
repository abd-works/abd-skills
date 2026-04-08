# Term Registry

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At identification time it is not committed to a model role — it might become a class, a property, a value type, an association, or nothing. The registry tracks Terms as modeling **phase-ids** (see **`process.md` → Phase chronicle**) determine what each one actually is.

This is distinct from other domain uses of overloaded words (e.g. in some systems “Actor” is a system type). In the registry, everything is a Term until the model says otherwise.

**File:** `<workspace>/abd-ooad/term-registry.md` (or per-slice path if your workspace layout nests slices).

**Never embed** the full registry inside step outputs — it lives in its own file and is referenced from each phase’s model doc.

---

## Relationship to `terms.md` (per slice)

- **`terms.md`** (alongside `domain-noun-verb.md` in a slice folder) holds **module-scoped evidence**: quotes, raw extractions, promotion history under **`## [Anchor module]`** headings aligned with the integrated domain model.
- **`term-registry.md`** remains the **term-centric analysis record**: one row per Term; **Targets** = where the term landed; **Notes** = substantive reasoning (anchor tests, classification, tensions) — **full paragraphs are fine** when the work needs them.
- **Principle:** Notes depth is **not** reduced because `terms.md` exists. `terms.md` reduces **duplication of verbatim source text** and organizes evidence by module; it does **not** justify one-line registry Notes unless the term truly needs only one line.
- **Avoid duplicate verbatim quotes:** keep the quote in **`terms.md`** and in **Notes** point to `terms.md#anchor-module` (or the term subsection); keep analysis-only text in Notes as today.

---

## Phase IDs (normative references)

Refer to pipeline steps **only** by **`phase-id`** — the short **kebab-case** slug matching **`skill-config.json` → `phase_files`** and the **`process.md`** chronicle (e.g. `domain-scan`, `nouns-verbs-rules-and-states`, `refine-names`). Do **not** use “Phase 1 / Phase 2” as **names** for steps; those ordinals drift. Optional **model tags** in the domain model use **`*[Sn · phase-id]*`** (e.g. **`*[S1 · refine-names]*`**) — see **`library/domain-model`**.

---

## Registry columns

| Column | Role |
|--------|------|
| **Term** | Concept name from the source — exact word or phrase as found; rename in **`refine-names`** if needed. |
| **Targets** | Where this term **landed** in the model: a **bulleted list inside the table cell** (Markdown list), **one typed pointer per line**. Unallocated / not yet placed → leave empty or **—**. |
| **Notes** | Anchor-test results, slice/anchor context (**`S1=…`** style if useful), competing interpretations, tensions, pointers to **`terms.md`** when verbatim evidence lives there — same substance as historical scan/noun-verb rows. |

**Optional:** If you need a single “primary kind” for tooling, add one optional column **after** Term (e.g. **Kind**) — otherwise prefer **Targets**-only for a slim table.

---

## Targets — typed pointers (one per bullet)

**Normative style:** each bullet is **one** typed target. **Do not** concatenate targets with `|` or `;` on one run-on line.

Examples of pointer forms (extend as your model needs):

- `entity:Payment`
- `vo:Money`
- `property:Payment.amount`
- `operation:Order.submit`
- `invariant:…`
- `policy:…`
- `relationship:Customer — Order`

**Renders in Markdown tables** — use `<br>` between bullets if your renderer collapses list-in-cell (GitHub-style often accepts list-in-cell; validate in your preview):

```markdown
| Term   | Targets |
|--------|---------|
| amount | - `entity:Payment`<br>- `vo:Money`<br>- `property:Payment.amount` |
```

---

## Notes — still substantive

Notes remain the place for **classification reasoning**, anchor tests, tensions, and follow-ups. **Do not** make Notes sparse by default. When raw quotes live in **`terms.md`**, write in Notes: *“Verbatim quote in `terms.md` → [Anchor module] / term …”* and keep analysis here.

**Slice / anchor:** You may record **`S1=Character`** (or similar) in **Notes** or a minimal **Slice** column if the table template adds one — your engagement may require it for MM3E-style multi-slice tables.

---

## Classification (reference — not required as its own column)

If you **merge** the old **Classification** column into **Targets**, use typed pointers (`entity:…`, `property:…`, …) so the table stays one row per Term. The **meaning** of former classification values is unchanged:

| Former value | Meaning |
|--------------|--------|
| **anchor (class + module)** | Passes the anchor test: core class owns a **module** (frame + same-named core class). |
| **class** | Domain class not its own module yet — supporting class, or expected class without module. |
| **property** | Modeled as semantic property on a class. |
| **field** | Typed field / slot. |
| **example (instance)** | Illustrative instance — not a type. |
| **relationship** | Association, link, dependency. |
| **invariant (rule)** | Domain rule, constraint, policy. |

---

## Registry format (HTML table recommended for Notes width)

Prefer an HTML `<table>` with `<colgroup>` so **Notes** gets most width (~50–55%). **Targets** can be ~18–22%.

```html
<table>
<colgroup>
  <col style="width:12%" />
  <col style="width:22%" />
  <col style="width:66%" />
</colgroup>
<thead>
<tr>
  <th>Term</th>
  <th>Targets</th>
  <th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
  <td>Character</td>
  <td>- <code>entity:Character</code><br>- <code>property:Character.powerLevel</code></td>
  <td>Central entity; anchor test ✓. Slice <code>S1=Character</code>. Long quotes in <code>terms.md</code> → Character module.</td>
</tr>
</tbody>
</table>
```

Small registries: Markdown pipe table is acceptable.

---

## Migration from legacy wide tables

If you have **Step**, **Confidence**, **Status**, and **Classification** columns:

1. **Term** → keep.
2. **Classification** + committed placements → **Targets** bullets (`entity:…`, `property:…`, …).
3. **Step** → fold into **Notes** as *“First touched at phase-id `domain-scan`”* or leave implicit if noisy.
4. **Confidence / Status** → merge into **Notes** (*“Legacy: was High / Active”*) only if still useful; otherwise drop.
5. **Notes** → preserve text; add pointer to **`terms.md`** where verbatim evidence moved.

---

## Slices and `domain-scan` vs per-slice work

- **`domain-scan`** runs **workspace-wide** (or once per strategy engagement): seeds **`term-registry.md`**, anchors, **`strategy.md`**, scan artifacts. It is **not** “each slice’s first phase” by name — use **phase-id** `domain-scan` only.
- Per-slice deep extraction aligns with **`nouns-verbs-rules-and-states`** and **`raw-candidate-list`** in **chronicle order** after scan. **`terms.md`** evolves from those phase-ids onward for that slice.

---

## References

- **`process.md`** — Phase chronicle, stages A–F, capture ladder  
- **`terms.md`** template — `templates/terms-template.md`  
- **Strategy / revisits** — `library/strategy-execution-and-checklists.md`
