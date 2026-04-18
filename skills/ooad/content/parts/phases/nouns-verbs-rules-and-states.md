# Nouns, verbs, rules, and states

**Skill:** abd-ooad — **Phase-id:** `nouns-verbs-rules-and-states` (see **`process.md`** chronicle — do not call this "Phase 2" as a step name).

**What you produce:** **domain-noun-verb.md** on disk (one per source slice): structured extraction by anchor — one **## [AnchorName module]** per backbone anchor; **Candidate …** lists; **full** class boxes (`+` / **opt** / **Invariant:**) or pared **`### … : << … >>`** where the source supports it; **#### Note :** when useful.

Use **## Cross-anchor notes** for unsettled or cross-cutting hooks. The slice file is **domain content only** — do not paste skill paths, template filenames, or process-only labels into the artifact.

**Focus here:** candidates and tensions; which nouns become classes is decided in later steps.

For the full anchor definition and the three-part anchor test — see `anchors` in this library.

---

## Deliverable — `domain-noun-verb.md` (normative)

**One file per slice:** **domain-noun-verb.md** in the **slice folder** (e.g. `abd-ooad/1 - basics-checks-conditions/`). Canonical **first detailed** extraction for that slice (after workspace-wide **`domain-scan`**). **Also maintain `terms.md`** in the slice folder (**`templates/terms-template.md`**) for long quotes and promotion history by **`## [Anchor module]`**.

| Item | Rule |
|------|------|
| **Path** | `<workspace>/<slice-folder>/domain-noun-verb.md` |
| **H1** | `# <SliceLabel>: Noun Verb Domain` — **SliceLabel** from the slice plan or folder slug. |
| **Structure** | Per anchor: **## [Anchor module]** → **### Note :** → **Candidate …** lists → class boxes (**full** `+` / **opt** / **Invariant:** or pared **`### … : << … >>`**). Optional **## Cross-anchor notes**. |
| **Artifact body** | Domain content only — no skill paths, template filenames, or process meta in the file. |
| **Elsewhere** | Methodology and plans stay in **strategy.md** / **term-registry.md** / phase docs — not in the slice artifact. |
| **`terms.md`** | Same slice folder; evidence quotes — see **`library/term-capture`** for format. |
| **`raw-candidates` in the same file** | Optional: append bucket roll-up, watch list, and tensions to **domain-noun-verb.md** (see **`raw-candidates`** phase-id) instead of a second markdown file. |


Align **term-registry.md** (slice / anchor context in **Notes**; **Targets** per **`library/term-capture`**) with the **`## [… module]`** headings in **domain-noun-verb.md** and **`terms.md`**.

| Artifact | Role |
|----------|------|
| **term-registry.md** | Term-centric **Targets** + **Notes** — sparse rows at first; deepens each phase-id. |
| **terms.md** (slice folder) | Verbatim / module-scoped evidence — **not** duplicated as walls of prose in the domain model. |
| **domain-noun-verb.md** (slice folder) | Structured extraction: candidates and **full** class boxes **by anchor** (pared-down only in Cross-anchor / boundary notes), structured as above. |


**Traceability:** the registry states **what** you claim; **domain-noun-verb.md** holds **what the source said**. Every new term found in this phase gets a row in `term-registry.md`. Use Notes labels to capture analysis (see **`library/term-capture`** for the full label list). Tag model notes with `[p1]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Anchor Boundary - {{challenge_or_support}} {{evidence_summary}}` — when a term challenges or reinforces an anchor's scope
- `Sibling Candidate - {{anchor_term}} {{why_related}}` — terms that appear alongside an anchor
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — terms whose boundary is unclear or contested
- `High Confidence Anchor - {{why_this_module_or_class_is_central}}` — terms that clearly anchor a module
- `Follow-up - {{question_or_action}}` — open questions for later phases

---

## Anchor boundaries under test

This phase-id is the first time anchors are tested by the full vocabulary of the source. As you extract nouns and verbs, actively watch for:

- **Evidence that supports an anchor** — terms that clearly belong inside an anchor's module frame (future supporting classes or properties of the core class)
- **Evidence that challenges an anchor** — a term that is referenced independently by multiple other concepts, suggesting it may need to be elevated to its own anchor
- **Evidence that an anchor should be split** — the core class is doing two different things and the nouns in this pass separate cleanly into two groups

Keep the anchor set stable for this phase. Record boundary questions in the term registry (`Anchor Boundary` note); resolve at `raw-candidates` (p3).

**At the end of Phase 2, re-apply the anchor test** (from **`anchors`**) to any anchor whose boundary was challenged. Promote, demote, or split if the test now fails. Update **`term-registry.md`** and any scan diagram if the workspace still uses them.

---

## Work order

Analysis lives in **`domain-noun-verb.md`** (per slice) — **only**. Methodology stays in **phase docs** and **strategy**; do not paste skill boilerplate into the slice file. When the project also keeps a class diagram for this slice, update it **after** the markdown reflects the same facts (**visual twin** — see **class-diagrams**, **using-diagram-cli**).

---

## Illustrative shape (short)

Work **section-by-section** in the source. Under each **`## [Anchor module]`**, list **Candidate** nouns, verbs, rules, states; add **`### ClassName`** boxes when the text supports it. The **raw-candidates** phase doc shows a tiny **Check**-anchor excerpt for bucket shape.

---

## Continual refinement (this step)

**Delta:** pre-notation — nouns, verbs, rules, states, tensions; typed members arrive in later phases.

---

## Action Checklist

- Have you created **domain-noun-verb.md** in the slice folder with H1 `# <SliceLabel>: Noun Verb Domain`, anchors, Candidate lists, and class boxes — with methodology outside the slice file?
- Have you extracted candidate nouns from every major section of the source material?
- Have you extracted domain verbs (actions, operations, state changes)?
- Have you identified at least three domain rules or constraints?
- Have you recorded lifecycle states for at least the key candidate classes?
- Have you noted synonyms, naming conflicts, and scope boundary noise for later steps?
- Have you updated `term-registry.md` with all new terms found in this phase, with Notes labels (`Anchor Boundary`, `Sibling Candidate`, `Tension`, `High Confidence Anchor`) applied where relevant?
- Have you set each row's slice anchor context in the Notes column to point at the right **`## [… module]`** heading in **domain-noun-verb.md**?

---

## Prompt

> **Validate and fix when you find problems.** Surface bloat, unclear boundaries, missing invariants, naming drift, or spec conflicts — **validate** and **fix** the model (or **map-model-spec.json** / class diagram) before moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
