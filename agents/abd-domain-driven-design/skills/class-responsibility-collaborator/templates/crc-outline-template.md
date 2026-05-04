<!--
  class-responsibility-collaborator.md

  Append a ### Class Responsibility Collaborator section after ### Domain Sketch
  within each knowledge-area (## **KA Name**) section of the module file.

  Format per block:
    #### **ConceptName**
    responsibility name         | Collaborator, Another Collaborator
    another responsibility      | (value description for primitives/enums)
                                |   invariant: declarative constraint

  Subtypes:
    #### **ConceptName : BaseConcept**
    delta responsibility only   | Collaborator
-->

## **{{KnowledgeAreaName}}**

### Class Responsibility Collaborator

#### **{{ConceptName}}**
{{noun phrase property}}            | {{Collaborator}}
{{verb phrase operation}}           | {{Collaborator, Collaborator}}
                                    |   invariant: {{declarative constraint}}

#### **{{SubtypeName}} : {{BaseConcept}}**
{{delta responsibility only}}       | {{Collaborator}}
                                    |   invariant: {{constraint specific to this subtype}}

---

# Boundary Domain

### Class Responsibility Collaborator

#### **{{BoundaryConcept}}**
{{responsibility}}                  | {{Collaborator}}

---

## Instructions

- One `#### **ConceptName**` block per concept — including state-carrier classes and collection classes introduced during CRC.
- Left column: noun phrase for properties, verb phrase for operations. Vocabulary tight to the behavior bullet that inspired it. No technical terms (flag, boolean, list, own).
- Right column: comma-separated collaborator class names. Use parenthetical value description `(active or ended)` for primitives/enums.
- Invariants: `|   invariant:` indented continuation rows under the responsibility they constrain.
- Subtypes: `#### **ConceptName : BaseConcept**` — delta responsibilities only; do not repeat parent entries.
- Slash terms (`A / B`) must be resolved to one name before writing any block.
- `|` separators: align consistently within each block.
- Boundary Domain: all boundary concepts share one `### Class Responsibility Collaborator` section — not split by concept.

---

## Filled example (Check Resolution module)

```markdown
## **Check**

### Class Responsibility Collaborator

#### **Check**
use trait                   | Trait
use difficulty class        | Difficulty Class, Difficulty Stage
apply circumstance          | Circumstance Modifier
is routine                  | (active or inactive — when active, d20 fixed at 10)
resolve                     | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result
                            |   invariant: d20 + trait rank + circumstance modifier >= difficulty class

#### **Opposed Check : Check**
use opposing trait          | Trait
                            |   invariant: both sides resolve as standard Checks; higher result wins
                            |   invariant: tie — higher bonus wins; bonus tie — d20 (1–10 vs 11–20)
                            |   invariant: passive opposition DC = opposing modifier + 10

#### **Team Check : Check**
use helper traits           | Trait
resolve helper              | D20, Trait, Check Result
                            |   invariant: each helper rolls same Trait vs DC 10
apply helper outcome        | Circumstance Modifier
                            |   invariant: 1 success → +2; 3+ successes → +5; cap +5
                            |   invariant: 2+ failures → −2; cap −2

---

## **Condition**

### Class Responsibility Collaborator

#### **Condition**
label                       | (name of the condition, e.g. dazed, stunned)
game modifier               | (penalty value or restriction description)
supersedes                  | Condition
superseded by               | Condition

#### **Imposed Condition**
imposing source             | Condition Source
condition type              | Condition
active status               | (active or inactive)
suppressing condition       | Imposed Condition
                            |   invariant: set when parked inactive by a different-source more-severe condition

#### **Imposed Conditions**
applied conditions          | Imposed Condition
apply new condition         | Condition Source, Condition, Imposed Condition
                            |   invariant: same-source more-severe — remove lesser imposed condition
                            |   invariant: same-source less-severe — do nothing
                            |   invariant: different-source more-severe — park lesser as inactive, set suppressing condition

#### **Condition Source**
imposing identity           | (name, reference, or descriptor of the effect, attacker, or event)

---

# Boundary Domain

### Class Responsibility Collaborator

#### **Power Effect : Trait**
resistance trait            | Trait
is ongoing                  | (active or ended)
condition on failure        | Condition, Degree of Failure
                            |   invariant: which conditions are imposed is defined by the effect type
end                         | Imposed Conditions
                            |   invariant: on end — all conditions imposed by this effect are removed

#### **Ongoing Effects**
active effects              | Power Effect
ongoing targets             | Character
make resistance check       | Character, Check
                            |   invariant: check made at end of each ongoing target's turn
end effect                  | Power Effect, Imposed Conditions
                            |   invariant: clears only the conditions that this effect imposed

#### **Character**
traits                      | Trait
imposed conditions          | Imposed Conditions
ongoing effects             | Ongoing Effects
```
