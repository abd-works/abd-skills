# Corrections log

Project: abd-acceptance-criteria skill
Source: abd-acceptance-criteria skill (pipeline runs)

---

## Entry: AC invented domain term not present in domain sketch

- **Status:** confirmed
- **Context:** abd-acceptance-criteria — check-resolution module, story "Make Resistance Check Against Effect"
- **DO:** Only use terms in `#### Domain terms` sections that have a corresponding concept block in the module's domain sketch. If a concept is needed but missing from the sketch, add the concept block to the sketch first — do not invent a term in the AC to fill the gap.
- **Example (wrong):**
  `*Condition Track* — the sequence of conditions the effect imposes at each degree of failure` — this term had no concept block in the domain sketch; it was fabricated to bridge a modeling gap.
- **Example (correct):**
  The fabricated term was removed. The related concept `*Supersession Chain*` was extracted into its own `### supersession chain` concept block in the domain sketch before being referenced in the AC.
- **Likely source:** prompt gap — the skill does not require cross-checking every `#### Domain terms` entry against an existing concept block in the domain sketch before writing it.

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
