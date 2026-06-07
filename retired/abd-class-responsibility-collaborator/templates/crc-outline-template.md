<!--  
  Normative shape for the domain model phase output.  

  Output: <deliverables-folder>/[<name>-]crc.md  
          (or <deliverables-folder>/modules/<module-name>-crc.md  
           for multi-module engagements)  

  This skill produces a STANDALONE file. It does not enrich the prior phase's  
  file in place. It is a fresh artifact in the same flat heading shape every  
  other DDD phase skill uses.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**  

    [Optional 1–2 sentence intro]  

    ### **{{ka_name as a Class}}**            ← MUST appear first; matches the KA  
    property name              | Collaborator  
    operation name             | Collaborator  
                               |   invariant: rule that must always hold  

    ### **{{another Class}}**  
    property name              | Collaborator  
    operation name             | Collaborator, Collaborator  

    ### **{{SubtypeName}} : {{BaseClass}}**  
    delta responsibility       | Collaborator  

    ### references                             ← one per KA, peer to classes  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

    ### decisions made                         ← one per KA, peer to classes  
    - decision rationale  

  Contract:  
    - One file per phase. Do not enrich a prior file in place.  
    - The KA's own class is listed FIRST under the ## **KA** heading.  
    - Responsibility tables live directly under each ### **Class** heading.  
    - One ### references and one ### decisions made per KA.  
    - Subtypes use ### **Subtype : BaseClass** notation; deltas only.  
    - Boundary Domain is one flat group with shared references and decisions.  

  Format per CRC table:  
    Left column  — noun phrase for properties, verb phrase for operations.  
                   Vocabulary tight to the inspiring sketch behavior.  
                   No technical terms (flag, boolean, list, type, own).  
    Right column — comma-separated collaborator class names, or a parenthetical  
                   value description for primitives/enums.  
    Invariants   — `|   invariant:` indented continuation rows under the  
                   responsibility they constrain.  
    `|` separators — align consistently within each block.  
-->  

---  
state: domain-model  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope}}  

**Core terms**:  
- {{term1}}  
- {{term2}}  
- …  

**Key Abstractions (term grouping)**:  
- **{{KAName}}**: …  
- **{{AnotherKAName}}**: …  

---  

# Core Domain  

## **{{KAName}}**  

### **{{ka_name_as_a_Class}}**  
{{noun phrase property}}            | {{Collaborator}}  
{{verb phrase operation}}           | {{Collaborator, Collaborator}}  
                                    |   invariant: {{declarative constraint}}  

### **{{AnotherClass}}**  
{{property}}                        | {{Collaborator}}  
{{operation}}                       | {{Collaborator}}  

### **{{SubtypeName}} : {{BaseClass}}**  
{{delta responsibility only}}       | {{Collaborator}}  
                                    |   invariant: {{constraint specific to this subtype}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text copied byte-for-byte from the source}}  
```  

### decisions made  

- {{slash-term resolution, state-carrier or collection-class introduction, Liskov decision, dependency-magnet split, or open question}}  

---  

# Boundary Domain  

### **{{BoundaryClass}} : {{BaseClass}}**  
{{responsibility}}                  | {{Collaborator}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

### decisions made  

- {{boundary placement reasoning}}  

---  

<!-- EXAMPLE — delete this section after using the template. -->  

## Example (filled — Check Resolution module)  

```markdown  
---  
state: domain-model  
---  

# Module: [Check Resolution]  

Scope: The d20 resolution mechanic, checks, degrees, conditions.  

---  

# Core Domain  

## **Check**  

### **Check**  
use trait                   | Trait  
use difficulty class        | Difficulty Class, Difficulty Stage  
apply circumstance          | Circumstance Modifier  
is routine                  | (active or inactive — when active, d20 fixed at 10)  
resolve                     | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result  
                            |   invariant: d20 + trait rank + circumstance modifier >= difficulty class  

### **Opposed Check : Check**  
use opposing trait          | Trait  
                            |   invariant: both sides resolve as standard Checks; higher result wins  
                            |   invariant: tie — higher bonus wins; bonus tie — d20 (1–10 vs 11–20)  

### **Difficulty Class**  
numeric threshold           | (integer 0–40)  

### **Trait**  
effective rank              | (integer)  

### references  

**Ref — Game Play**  
Source: context/rules/HeroesHandbook-rules__chunk_009.md  
Locator: lines 809–874  
Extract: whole  

```source  
GAME PLAY  
…verbatim text from chunk…  
```  

### decisions made  

- Opposed Check is a subtype — base resolution contract holds (Liskov).  
- Routine check expressed as state on Check rather than its own subtype — same resolution contract with d20 pinned.  

---  

## **Condition**  

### **Condition**  
label                       | (name of the condition, e.g. dazed, stunned)  
game modifier               | (penalty value or restriction description)  
supersedes                  | Condition  
superseded by               | Condition  

### **Imposed Condition**  
imposing source             | Condition Source  
condition type              | Condition  
active status               | (active or inactive)  
suppressing condition       | Imposed Condition  
                            |   invariant: set when parked inactive by a different-source more-severe condition  

### **Imposed Conditions**  
applied conditions          | Imposed Condition  
apply new condition         | Condition Source, Condition, Imposed Condition  
                            |   invariant: same-source more-severe — remove lesser imposed condition  
                            |   invariant: different-source more-severe — park lesser as inactive, set suppressing condition  

### references  

**Ref — Conditions**  
Source: context/rules/HeroesHandbook-rules__chunk_201.md  
Locator: lines 14000–14200  
Extract: whole  

```source  
CONDITIONS  
…verbatim text from chunk…  
```  

### decisions made  

- Introduced Imposed Condition as state-carrier — per-application state does not belong on Condition or Character.  
- Introduced Imposed Conditions as collection class — supersession behavior is collection-level, not entity-level.  

---  

# Boundary Domain  

### **Power Effect : Trait**  
resistance trait            | Trait  
is ongoing                  | (active or ended)  
condition on failure        | Condition, Degree of Failure  
                            |   invariant: which conditions are imposed is defined by the effect type  
end                         | Imposed Conditions  
                            |   invariant: on end — all conditions imposed by this effect are removed  

### **Ongoing Effects**  
active effects              | Power Effect  
ongoing targets             | Character  
make resistance check       | Character, Check  
                            |   invariant: check made at end of each ongoing target's turn  

### references  

**Ref — Resistance and Ongoing Effects**  
Source: context/rules/HeroesHandbook-rules__chunk_209.md  
Locator: lines 14791–14830  
Extract: whole  

```source  
…verbatim text…  
```  

### decisions made  

- Power Effect's resistance/ongoing rules are owned by the Power module — this module only owns the check-resolution behavior.  
```  
