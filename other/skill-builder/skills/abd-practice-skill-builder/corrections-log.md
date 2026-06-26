# Corrections log

Engagement: practice-skill-builder — norms for finishing **any** abd.works **practice skill** (`skills/<practice>/`: `SKILL.md`, `rules/`, `templates/`).

---

## Themes of mistakes (cross-practice)

These recur regardless of whether the practice is story mapping, impact mapping, specification-by-example, or something else. The numbered **entries** below are concrete instances; the themes are the analysis layer.

| Theme | What goes wrong | Why it matters |
|--------|-----------------|----------------|
| **A. Wrong normative home** | Facilitation, attendance, or “how to run the session” is written as **`rules/*.md`** pass/fail, or rules open with meta that only says what they are *not* (e.g. “not about facilitating”). | **`rules/`** must judge **named outputs** from **text alone**. Process belongs in **`SKILL.md`** teaching and **Build** order. |
| **B. Not enforceable** | A **DO** bullet has no observable condition on a file, section, or pattern; reviewers cannot mark pass/fail. | Agents and humans cannot apply or automate the rule; it reads as philosophy. |
| **C. One surface, too many roles** | One line or slot carries **name + measure + timing + threshold** (or idea + metadata + internal label) because it was faster to type once. | The artifact becomes hard to scan, diff, or validate; scanners and readers cannot rely on stable slots. |
| **D. Duplicated structure in prose** | The template already has a **field, row, or labeled line** for a fact, but instructions or examples still put the same fact as a **parenthetical tail** in a sentence. | Noise, inconsistency, and double maintenance; looks like a form filled twice. |
| **E. Literal placeholders** | Final copy still reads like **schema** (*achieve **Grow …***), **internal tags** in running text, or **inconsistent `{{names}}`** across paired outputs. | Breaks trust with human readers; breaks sync between `.md` / `.txt` / tools. |
| **F. Incoherent artifact** | Two parts of the **same** deliverable imply different intent (e.g. a child bullet does not match the parent it hangs under). | Usually **copy-paste** or **partial edit**; breaks traceability inside one file. |
| **G. Weak exemplars** | **Templates** ship examples that are only tokens or generic steps, so nobody sees what “good” looks like for that audience. | Agents imitate the weak example; reviewers have no anchor. |
| **H. Practice leakage into author kit** | A **cross-practice** authoring rule is drafted from **one** practice’s notation (specific prefixes, map geometry, hypothesis shape). | Other practices inherit irrelevant or misleading norms; later retracted (see below). |
| **I. Mechanical hygiene** | Spacing, agreement, awkward numeric phrasing — real defects but **not** conceptual. | Still worth fixing on inspection; distinguish from A–H. |

**Mapping (old entry numbers to themes):**  
1 → A, B · 2 → A, B · 3–4 → C, D (practice-specific illustration) · 5 → F · 6 → E · 7 → G · 8 → E · 9 → I.

---

## Retracted norm (author skill): `rules/template-readable-prose.md`

- **Theme:** H (practice leakage).
- **What happened:** One engagement mixed **general** “readable template” guidance with **impact-mapping-only** layout (headlines vs metric lines, hypothesis clauses).
- **Note:** The bundled rule **Evidence, templates, and gaps** was later removed from **abd-author-practice-skill**. Theme **D** (structure vs prose) remains a useful idea for target packages; put it in **that** practice’s **`rules/`** or **`SKILL.md`** if you want it normative.

---

## Entries (normative targets in this repo)

### Entry 1 — rules must be generation-enforceable, not facilitation process

- **Status:** confirmed
- **Themes:** A, B
- **Norm:** `rules/valid-rule-file-shape.md` (abd-author-practice-skill); **Build** / **Validate** in same skill
- **DO / DO NOT:** Target **`rules/*.md`** must be checkable on **artifact text alone**. **DO NOT** put workshop facilitation, participation, or session-only process in **`rules/`** when pass/fail cannot be decided from the generated file.
- **Illustration (wrong):** **DO** bullets that only say **who runs the meeting** or **who must attend**, with no condition on output text.
- **Illustration (correct):** **DO** scoped to a **named artifact** (e.g. “every story title in `story-map.md` is verb–noun”); facilitation in **`SKILL.md`**.
- **Likely cause:** Treating **`rules/`** as the full method write-up instead of the **check layer**.

### Entry 2 — rules as positive artifact specs, not anti-process lectures

- **Status:** confirmed
- **Themes:** A, B
- **Norm:** `rules/valid-rule-file-shape.md`; target practice **`rules/*.md`** and authoring **SKILL.md** tone
- **DO / DO NOT:** State **what to verify on the artifact**. **DO NOT** pad with lines that only negate facilitation or restate scope without a checkable condition.
- **Illustration (wrong):** Opening a rule with “these checks are not about how to facilitate.”
- **Illustration (correct):** First normative block is **## DO** with concrete pass conditions on a **named output**; **Build** owns step order.
- **Likely cause:** Defensive writing after a workshop-centric source; no translation into output specs.

### Entry 7 — templates: instructions and examples that model the bar

- **Status:** confirmed
- **Themes:** G (and supports D, E when examples are weak)
- **Norm:** target **`templates/*`**, **`SKILL.md`**
- **DO / DO NOT:** Say what **readable / audience-appropriate** output means for this practice; ship **examples** that could pass as a real draft for that audience, not only mechanical scaffolding — unless the practice is explicitly a lab.
- **Likely cause:** Rushed first draft; placeholders never replaced with a gold-standard snippet.

### Entry 8 — parallel placeholder naming across paired templates

- **Status:** confirmed
- **Theme:** E
- **Norm:** target **`templates/*`**
- **DO / DO NOT:** Use **parallel stems** for the same semantic slot across `.md`, `.txt`, and related outputs so refactors do not split meaning.
- **Likely cause:** Incremental renames without a single pass across all template siblings.

### Entry 9 — mechanical hygiene

- **Status:** confirmed
- **Theme:** I
- **DO / DO NOT:** Fix **double spaces**, agreement, and clumsy numeric phrasing where the practice expects clean copy — on **Validate**, not as a substitute for A–H.
- **Likely cause:** Merge edits, speed.

---

## Appendix: Instance log — impact-mapping engagement

Concrete fixes that belong under **`skills/abd-impact-mapping/`** (templates and **`rules/*.md`** there), illustrating themes **C–F** above — **not** general author-skill norms.

| # | Theme | Note |
|---|--------|------|
| A3 | C, D | Hypothesis and map **narrative** slots: natural sentences; no label-y parentheticals when the format already has fields/lines for those roles. |
| A4 | C | Tree / outline **head** lines stay short on **meaning**; measures and cadence live in the slots the skill defines for them. |
| A5 | F | Child **build** lines stay aligned with the parent **impact / intent** they sit under; connectors readable (not copy-pasted from another branch). |
| A6 | E | **Then** / outcome clause: idiomatic verb phrase + measure — not *achieve* + pasted title-case placeholder headline. |

Use this appendix when auditing **that** package; do not lift row text verbatim into **abd-author-practice-skill** as if it applied to every practice.

---

## Entry 10 — ubiquitous-language skill must teach OO modeling decisions, not just list formatting rules

- **Status:** confirmed
- **Theme:** G (Weak exemplars), new theme **J** (missing modeling guidance)
- **Artifact:** `agents/abd-domain-driven-design/skills/ubiquitous-language/SKILL.md` — Core concepts section
- **What went wrong:** The skill taught **what a concept block looks like** (headings, separators, subtypes) but never told the modeler **how to decide** whether a term is a concept, subtype, property, instance, invariant, or relationship. Every term got promoted to its own `### Concept` heading — producing flat, class-per-term sketches with no real modeling.
- **Fix:** Added "Modeling each term: concept, subtype, property, instance, or invariant" section under Core concepts with prose guidance and a quick decision guide (distinct behavior → concept; specialized behavior → subtype; data-only variation → instance/property; value slot → property; always-true rule → invariant; connects two concepts → relationship).
- **Why it matters:** Without this gate the skill produces inventories, not models. Downstream CRC and scenario walks inherit the same flat structure and waste effort assigning responsibilities to things that are just properties.

## Entry 11 — ubiquitous-language must require OOA on the source, not surface-level classification

- **Status:** confirmed
- **Theme:** J (missing modeling guidance)
- **Artifact:** `agents/abd-domain-driven-design/skills/ubiquitous-language/SKILL.md` — "Modeling each term" section and new validation rules
- **What went wrong (run: Check Resolution ubiquitous-language):** Five corrections (21–24 plus team-check discovery) in a single run exposed gaps:
  1. Terms were classified (type property, instance, role) without reading the source for those terms — surface similarity ("they all have ranks") led to wrong calls (Correction 21).
  2. The output of a concept (Check Result) was hidden as a property instead of modeled as its own concept with identity, state, and behavior (Correction 22).
  3. A role (GM) was excluded without tracing the mechanics it referenced — the mechanics nearly got lost (Corrections 16–17).
  4. Boundary relationships (who defines vs who enforces a game modifier) were not captured (Correction 24).
  5. A behavior bullet on Check ("team helpers each roll...") hid a subtype with its own distinct DC, roles, and result-flow — discovered only when applying the "active verb with hidden subject" test.
- **Fix:** Updated SKILL.md:
  - "Read the source material for that term and do proper OOA" replaces "ask what it actually is."
  - Added concept-emergence guidance: outputs, inputs, properties, behaviors can all become concepts when they have distinct identity, state, behavior, structure, or interactions.
  - Added role guidance: roles are domain objects if they have system-level identity/state/behavior; when excluding, preserve the mechanics.
  - Added second-pass validation step and AI validation rules (typing checks, hidden-concept detection, active-verb form).
- **Why it matters:** Without source-grounded OOA the modeler guesses from labels. Without hidden-concept detection, behaviors accumulate on parent concepts until the model is a god object.
