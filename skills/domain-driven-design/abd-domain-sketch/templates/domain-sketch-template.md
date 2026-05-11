<!--  
  Normative shape for the domain-sketch phase output.  

  Output: <deliverables-folder>/[<name>-]domain-sketch.md  
          (or <deliverables-folder>/modules/<module-name>-domain-sketch.md  
           for multi-module engagements)  

  This skill produces a STANDALONE file. It does not enrich the prior phase's  
  file in place. It is a fresh artifact in the same flat heading shape.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**  

    [Optional 1–2 sentence intro]  

    ### **{{ka_name as a concept}}**         ← MUST appear first; matches the KA  
    - verb-led behavior bullet  
    - **Invariant:** rule that must always hold  

    ### **{{another concept}}**  
    - verb-led behavior bullet  
    - **Invariant:** rule  

    ### **{{SubtypeName}}** *is a type of* **{{BaseName}}**  
    - delta behavior  

    ### references                            ← one per KA, peer to concepts  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

    ### decisions made                        ← one per KA, peer to concepts  
    - typing call, scope call, structural call, or open question  

  Contract:  
    - One file per phase. Do not enrich a prior file in place.  
    - The KA's own concept is listed FIRST under the ## **KA** heading.  
    - Bullets live directly under each ### **concept** heading — no sub-headings.  
    - One ### references and one ### decisions made per KA.  
    - Subtypes use the English heading form *is a type of*.  
    - Behavior + produced result on the same bullet (", producing a [result]").  
-->  

---  
state: domain-sketch  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope}}  

**Core terms**:  
- {{term1}}  
- {{term2}}  
- …  

**Key Abstractions (term grouping)**:  
- **{{KAName}}**: {{ka_name_as_a_term}}, {{term1}}, {{term2}}, …  
- **{{AnotherKAName}}**: …  

---  

# Core Domain  

## **{{KAName}}**  

{{Optional 1–2 sentence intro: what this KA is for, who it cooperates with.}}  

### **{{ka_name_as_a_concept}}**  
- {{verb-led behavior: what the KA itself does, owns, enforces}}  
- {{verb-led behavior, producing a {{result}} when relevant}}  
- **Invariant:** {{rule that must always hold}}  

### **{{another_concept}}**  
- {{verb-led behavior bullet}}  
- {{verb-led behavior bullet}}  
- **Invariant:** {{rule}}  

### **{{SubtypeName}}** *is a type of* **{{BaseName}}**  
- {{delta behavior — only what the subtype adds beyond the base}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text copied byte-for-byte from the source}}  
```  

**Ref — {{another_ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

### decisions made  

- {{boundary call, scope call, structural call, or open question with reasoning}}  

---  

## **{{AnotherKAName}}**  

### **{{another_ka_as_a_concept}}**  
- {{verb-led behavior}}  
- **Invariant:** {{rule}}  

### **{{concept}}**  
- {{verb-led behavior}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

### decisions made  

- {{…}}  

---  

# Boundary Domain  

### **{{boundary_concept}}** *(owned by: {{owning_module}})*  
- {{verb-led behavior bullet describing what this module sees of it}}  

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
state: domain-sketch  
---  

# Module: [Check Resolution]  

Scope: The d20 resolution mechanic, checks, degrees, conditions.  

**Core terms**:  
- check  
- Difficulty Class (DC)  
- trait  
- modifier  
- condition  

**Key Abstractions (term grouping)**:  
- **Check**: check, Difficulty Class (DC), trait, modifier  
- **Condition**: condition  

---  

# Core Domain  

## **Check**  

A check is the core resolution mechanic — it owns the  
roll-plus-modifier-versus-DC formula and works with Trait, DC, and Degree.  

### **check**  
- is resolved by rolling a d20, adding the trait rank and circumstance modifier, comparing the roll total to the difficulty class, producing a check result  
- may have a circumstance modifier applied (±2 minor, ±5 major)  
- **Invariant:** always roll total versus DC; subtypes only vary how total or DC is produced  

### **Difficulty Class (DC)**  
- is set by the GM at the start of each check using the standard difficulty scale  
- **Invariant:** every check has exactly one DC at the moment of resolution  

### **trait**  
- supplies the rank that contributes to the roll modifier on a check  

### **modifier**  
- combines the trait rank with circumstance bonuses or penalties to produce the modifier added to the roll  

### **Opposed Check** *is a type of* **Check**  
- is made against an opposing character's check result as the difficulty class  
- on a tie, the higher bonus wins; if bonuses also tie, a tie-break d20 decides  

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

- Opposed Check is a subtype — it reuses the base resolution but changes what the DC is.  
- Degree of success is a property carried on the check result, not a separate concept.  

---  

# Boundary Domain  

### **Power Effect** *(owned by: Power)*  
- has a rank that determines the resistance check DC (DC = rank + 10)  
- may impose one or more conditions on a character based on degree of failure  
- when ended, all conditions it imposed are removed  

### references  

**Ref — Resistance and Ongoing Effects**  
Source: context/rules/HeroesHandbook-rules__chunk_209.md  
Locator: lines 14791–14830  
Extract: whole  

```source  
…verbatim text…  
```  

### decisions made  

- Power Effect is a boundary concept — condition-selection rules belong to the Power module.  
```  
