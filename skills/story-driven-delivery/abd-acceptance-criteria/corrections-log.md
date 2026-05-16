# Corrections log

Project: abd-acceptance-criteria skill
Source: abd-acceptance-criteria skill (pipeline runs)

---

## Entry: AC invented domain term not present in Ubiquitous Language

- **Status:** confirmed
- **Context:** abd-acceptance-criteria — check-resolution module, story "Make Resistance Check Against Effect"
- **DO:** Only use terms in `#### Domain terms` sections that have a corresponding concept block in the module's Ubiquitous Language. If a concept is needed but missing from the sketch, add the concept block to the sketch first — do not invent a term in the AC to fill the gap.
- **Example (wrong):**
  `*Condition Track* — the sequence of conditions the effect imposes at each degree of failure` — this term had no concept block in the Ubiquitous Language; it was fabricated to bridge a modeling gap.
- **Example (correct):**
  The fabricated term was removed. The related concept `*Supersession Chain*` was extracted into its own `### supersession chain` concept block in the Ubiquitous Language before being referenced in the AC.
- **Likely source:** prompt gap — the skill does not require cross-checking every `#### Domain terms` entry against an existing concept block in the Ubiquitous Language before writing it.

---

## Entry: AC restates already-specified mechanic from another story

- **Status:** confirmed
- **Context:** abd-acceptance-criteria — check-resolution module, story "Roll Resistance Check Against Ongoing Effect to Remove Conditions"
- **DO:** Each AC must specify behavior unique to its story's context. Do not open with an AC that restates a mechanic already fully specified in a prior story — it adds no behavioral value and dilutes the spec.
- **Example (wrong):**
  AC 1: "WHEN a character makes a Resistance Check against an Ongoing Effect THEN the system resolves the check as d20 + Defense Bonus vs Effect DC (10 + Effect Rank)" — identical to the mechanic already covered in "Make Resistance Check Against Effect". Says nothing unique to the Ongoing Effect story.
- **Example (correct):**
  AC 1 now opens with what is specific to this story: the effect ending, all its conditions removed, and any inactive conditions that were blocked by those removed conditions becoming active.
- **Likely source:** prompt gap — the skill does not instruct checking whether a given AC adds new behavioral specificity vs restating a mechanic covered in a prior story.

---

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** story-driven phase output filename
- **DO / DO NOT:** DO default to the template filename � `story-map.md`, `thin-slicing.md`, `acceptance-criteria.md`, `specification-by-example.md` (and their `.txt` partners where applicable). DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, multiple stories sharing one folder, or the user asks for it. DO NOT mandate the prefix as the only valid form, and DO NOT invent a sub-folder like `stories/`, `specs/`, `slices/`, `docs/` � write next to other engagement deliverables.
- **Example (wrong, forced prefix and folder):** Writing `docs/paw-place-thin-slicing.md` when the engagement workspace already keeps deliverables in `docs/` and only hosts one product. The `paw-place-` prefix is noise.
- **Example (correct):** Default to `thin-slicing.md` written next to existing engagement deliverables. Add a prefix only when disambiguation is needed.
- **Likely source:** earlier in this session the skill emitted `<name>-<phase>.md` unconditionally, then writing into a hardcoded folder; the user moved the files manually and asked that the prefix be optional and the folder driven by where other deliverables already live.