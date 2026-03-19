---
rule_id: no-junk-concepts
phases: [step1]
order: 40
scanner: mms_scan_no_junk_concepts.py
impact: HIGH
---

## Concept names must be domain nouns — not labels, headers, or garbage

Concept names that are section headers, all-caps labels, proper nouns, truncations, or instruction phrases indicate that document structure leaked into the domain model. These are not domain concepts — they are artifacts of how the source was written.

The scanner (`mms_scan_no_junk_concepts.py`) flags concept names that match known bad patterns. It does not determine whether a specific name is valid — names that are borderline or context-dependent require AI judgment.

**DO** name concepts as domain nouns that hold state or own decisions.
- Right: "Check", "Ability", "PowerLevel", "Condition", "Modifier"

**DO NOT** use section headers or all-caps document labels as concept names.
- Wrong: "THE BASICS", "CHAPTER 6", "POWERS", "GAME PLAY", "EFFECTS", "ACTION"

**DO NOT** use proper nouns — character names, setting names, organization names, product names.
- Wrong: "Paragon", "Speedster", "Freedom City", "Green Ronin"

**DO NOT** use instruction phrases, connectors, or single common words that are not domain terms.
- Wrong: "Choose", "Choose One", "Although", "Because", "Select", "Apply"

**DO NOT** use truncations or fragments.
- Wrong: "Insub", "Aff", "Dam", "Init", "Abil"
