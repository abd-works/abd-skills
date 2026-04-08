# Nouns, verbs, rules, and states

**Skill:** abd-ooad — **Phase-id:** `nouns-verbs-rules-and-states` (see **`process.md`** chronicle — do not call this “Phase 2” as a step name).

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
| **`terms.md`** | Same slice folder; evidence quotes and promotion log — see **`library/term-registry.md`**. |
| **`raw-candidate-list` in the same file** | Optional: append bucket roll-up, watch list, and tensions to **domain-noun-verb.md** (see **`raw-candidate-list`** phase-id) instead of a second markdown file. |


Align **term-registry.md** (slice / anchor context in **Notes**; **Targets** bullets per **`library/term-registry.md`**) with the **`## [… module]`** headings in **domain-noun-verb.md** and **`terms.md`**.

| Artifact | Role |
|----------|------|
| **term-registry.md** | Term-centric **Targets** + **Notes** — sparse rows at first; deepens each phase-id. |
| **terms.md** (slice folder) | Verbatim / module-scoped evidence — **not** duplicated as walls of prose in the domain model. |
| **domain-noun-verb.md** (slice folder) | Structured extraction: candidates and **full** class boxes **by anchor** (pared-down only in Cross-anchor / boundary notes), structured as above. |


**Anchor column** (single cell per term in the registry table) — one code cell per term, **slice-keyed**:

- **S1=<heading>** — primary anchor where this term is evidenced in **slice 1**, matching the **## [… module]** label in **domain-noun-verb.md** (e.g. `Character`, `Check`). Use **S1=—** if no hook in slice 1.
- **Optional suffix** on the same `S1=` value when evidence is thin: **(partial)**, **(gaps)**, or **Character+Effect** when the text spans anchors.
- **S2=…** — add when slice 2 exists; keep **`S2=—`** out of the registry until slice 2 is in play.

**Traceability:** the registry states **what** you claim; **domain-noun-verb.md** holds **what the source said**. Rows should be defensible from `S1=` (and later `S2=`) where not `—`.

---

## Anchor boundaries under test

This phase-id is the first time anchors are tested by the full vocabulary of the source. As you extract nouns and verbs, actively watch for:

- **Evidence that supports an anchor** — terms that clearly belong inside an anchor's module frame (future supporting classes or properties of the core class)
- **Evidence that challenges an anchor** — a term that is referenced independently by multiple other concepts, suggesting it may need to be elevated to its own anchor
- **Evidence that an anchor should be split** — the core class is doing two different things and the nouns in this pass separate cleanly into two groups

Keep the anchor set stable for this phase. Record boundary questions in the term registry (`Status: Ambiguous`, note the challenge); resolve at **Phase 3** (`raw-candidate-list` / **CANDS**).

**At the end of Phase 2, re-apply the anchor test** (from **`anchors`**) to any anchor whose boundary was challenged. Promote, demote, or split if the test now fails. Update **`term-registry.md`** and any scan diagram if the workspace still uses them.

---

## Work order (Phase 2)

Analysis lives in **`domain-noun-verb.md`** (per slice) — **only**. Methodology stays in **phase docs** and **strategy**; do not paste skill boilerplate into the slice file. When the project also keeps a class diagram for this slice, update it **after** the markdown reflects the same facts (**visual twin** — see **class-diagrams**, **using-diagram-cli**).

---

## Illustrative shape (short)

Work **section-by-section** in the source. Under each **`## [Anchor module]`**, list **Candidate** nouns, verbs, rules, states; add **`### ClassName`** boxes when the text supports it. The **raw-candidate-list** phase doc shows a tiny **Check**-anchor excerpt for bucket shape.

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
- Have you updated the term registry with all new terms found in this phase?
- Have you set each row’s **Anchor** cell (`S1=…`; add **S2=…** only after slice 2 exists) to point at the right **slice** anchor in the slice’s **domain-noun-verb.md**?

---

## Prompt

> **Validate and fix when you find problems.** Surface bloat, unclear boundaries, missing invariants, naming drift, or spec conflicts — **validate** and **fix** the model (or **map-model-spec.json** / class diagram) before moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.

