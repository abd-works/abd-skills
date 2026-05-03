# Corrections log

Project: mm3e-online-holistic
Source: abd-acceptance-criteria skill (pipeline runs)

---

## Entry: AC invented domain term not present in domain sketch

- **Status:** confirmed
- **Context:** abd-acceptance-criteria — check-resolution module, story "Make Resistance Check Against Effect"
- **DO:** Only use domain terms in AC `#### Domain terms` sections that are explicitly defined in the domain sketch. If a concept is needed to express AC behavior but has no concept block in the sketch, add the concept block to the sketch first — do not invent a term in the AC to fill the gap.
- **Example (wrong):**
  AC domain terms included `*Condition Track* — the sequence of conditions the effect imposes at each degree of failure`. This term does not appear anywhere in the domain sketch or source material; it was fabricated to bridge a modeling gap.
- **Example (correct):**
  The fabricated term was removed. The degree-of-failure → condition mapping is expressed using terms already in the domain sketch (`*Degree of Failure*`, the effect defines which condition applies). The related concept `*Supersession Chain*` was extracted from `### condition` into its own `### supersession chain` concept block in the domain sketch before being referenced in the AC.
- **Likely source:** prompt gap — the AC skill does not explicitly require cross-checking every domain term in `#### Domain terms` against an existing concept block in the domain sketch before writing it.

---

## Entry: AC restates already-specified mechanic from another story

- **Status:** confirmed
- **Context:** abd-acceptance-criteria — check-resolution module, story "Roll Resistance Check Against Ongoing Effect to Remove Conditions"
- **DO:** Each AC must specify behavior unique to its story's context. Do not open with an AC that restates a mechanic (e.g. check resolution formula) already fully specified in a prior story — it adds no behavioral value and dilutes the spec.
- **Example (wrong):**
  AC 1: "WHEN a character makes a Resistance Check against an Ongoing Effect THEN the system resolves the check as d20 + Defense Bonus vs Effect DC (10 + Effect Rank)" — identical to the mechanic already covered in "Make Resistance Check Against Effect". Says nothing about what makes the Ongoing Effect story distinct.
- **Example (correct):**
  AC 1 now opens with what is unique to the Ongoing Effect story: the effect ending and all its conditions being removed, plus the promotion of any inactive conditions that were blocked by those removed conditions.
- **Likely source:** prompt gap — the AC skill does not instruct checking whether a given AC adds new behavioral specificity vs restating a mechanic covered in a prior story.

---
