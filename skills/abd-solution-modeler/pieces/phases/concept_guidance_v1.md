# Phase 2 — Concept Guidance v1

**Actor:** AI | 
## Purpose

Create the **initial domain hypothesis** that will guide extraction.

This phase should identify the domain's likely:
- **Concepts**
- **Modules**
- **Mechanisms**
- **Actors**
- **Epics**

**Interaction detail:** Story Map Skeleton: Epics, Sub-Epics, some stories where possible.

## Trigger

concept scan, first-cut domain, epic skeleton, domain hypothesis

## Domain detail
Only include:
- concept names
- short interaction-oriented concept statements

Do **not** include:
- properties
- operations
- collaborators
- invariants
- final inheritance
- service/manager/resolver concepts unless explicitly present in the source domain

## Interaction detail
Produce:
- **Story Map Skeleton** — Epics, Sub-Epics, some stories where possible
- Epic names and short statements
- Sub-epics under epics where evident
- Stories where evident from context

Add stories where evident from context; defer Trigger, Response, scenarios, steps to later phases.

## Inputs
- `context/context_chunks.json`

## Instructions

Identify:

1. **Candidate Concepts**
   - include only concepts that appear central to the domain
   - prefer concepts that participate in interactions or state changes
   - avoid example-only roles unless they are real domain concepts

2. **Candidate Modules**
   - group concepts around likely mechanisms
   - modules should be broad and provisional

3. **Likely Mechanisms**
   - name mechanisms that appear to organize multiple rules
   - do not convert mechanisms into classes yet

4. **Likely Actors**
   - identify human/system/domain actors only where relevant to interactions

5. **Likely Epics**
   - broad domain interaction areas only
   - epic names should be verb-noun and domain-grounded
   - **scan `context/context_chunks.json` for verb clusters** — groups of action verbs (grab, restrain, redirect, etc.) that don't fit an existing epic suggest a missing epic; do not rely on background knowledge alone to identify epics

## Noise Filter Instructions

Populate `noise_filters` in the JSON output with strings that identify low-value chunks from this specific source material. Always include generic defaults, then add domain-specific terms you observe in the chunks.

**Always include these defaults:**
- `"table of contents"`, `"appendix"`, `"index"`, `"license"`

**Add domain-specific terms** — scan chunks for repeated noise: archetype random-table row labels, second-person tutorial prose, license text, roll-table instructions. 

**CRITICAL:** Only include strings that appear **exclusively** in worthless chunks. Do NOT include strings like chapter headers or book titles that also appear in good rule content — they appear in headers of every chunk and will cause the entire corpus to be filtered out.

## Output quality rules
- stay shallow
- prefer fewer, stronger concepts over long noun lists
- do not include formulas or exact rule math
- if uncertain, mark as **candidate**, not final
- every concept should have a short interaction-oriented statement
- every epic should be grounded in **Concept** language
- every concept named in the interaction skeleton must exist in the guidance output

## Outputs

1. `generated/domain/concept_guidance.md`
2. `generated/domain/concept_guidance.json`
3. `generated/interaction_model/interaction_tree.md` (Story Map Skeleton: Epics, Sub-Epics, some stories)

## Markdown output shape

```text
# Domain Concept Guidance

## Modules

### Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**

## Concepts (candidate)

**ConceptA** — interacts with **ConceptB**
**ConceptB** — modifies **ConceptC**
**ConceptC** — results from **ConceptA**

## Mechanisms (likely)

- **MechanismA** — short description
- **MechanismB** — short description

## Actors (likely)

- **ActorA** — short description

## Extraction Guidance

### Priority Concepts
- **ConceptA**
- **ConceptB**

### Priority Mechanisms
- **MechanismA**
- **MechanismB**

### Variation Axes
- axis a
- axis b

### Synonym Hints
- **ConceptA**: alias 1, alias 2
- **ConceptB**: alias 3, alias 4
```

## Required JSON shape (concept_guidance_v1.json)

```json
{
  "priority_concepts": ["ConceptA", "ConceptB"],
  "concept_aliases": {
    "ConceptA": ["alias 1", "alias 2"],
    "ConceptB": ["alias 3", "alias 4"]
  },
  "priority_mechanisms": ["MechanismA", "MechanismB"],
  "priority_actors": ["ActorA", "ActorB"],
  "variation_axes": ["axis a", "axis b"],
  "noise_filters": [
    "table of contents", "appendix", "index", "license",
    "chapter header repeated", "title page",
    "<domain-specific noise terms you identified from chunks>"
  ],
  "focus_sections": ["section a", "section b"]
}
```

## Checkpoint 1

Human verifies domain framing before proceeding.
