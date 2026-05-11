<!--  
  Normative shape for the domain-language phase output.  

  Output: <deliverables-folder>/[<name>-]domain-language.md  
          (or <deliverables-folder>/modules/<module-name>-domain-language.md  
           for multi-module engagements with a partition file)  

  This skill produces a STANDALONE file. It is not enriched in place by later  
  phase skills. Each later DDD phase skill (key-abstractions, domain-sketch,  
  CRC, object-model) writes its own file using the same flat shape.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**            (h2 — only present from key-abstractions onwards)  

    [optional intro paragraph]  

    ### **{{term/concept/class/object}}**    (h3 — name evolves stage-to-stage)  
    - bullet  
    - bullet  

    ### **{{another term}}**  
    - bullet  

    ### references                            (h3 — peer to terms; one per group)  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

  In the domain-language phase no KAs have been identified yet, so terms are  
  flat under # Core Domain (no ## **KA** wrapper). The key-abstractions phase  
  introduces the wrappers in its own file.  

  Contract:  
    - One file per phase. Do not enrich this file in place.  
    - Bullets live directly under each ### **term** heading.  
    - No #### Domain Language, #### References, or other sub-headings.  
    - One ### references section per group (Core Domain, Boundary Domain).  
-->  

---  
state: domain-language  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope}}  

**Core terms**:  
- {{term1}}  
- {{term2}}  
- …  

---  

# Core Domain  

### **{{term_name}}**  
- {{behavioral line: what it does, interactions, rules, flows}}  
- {{behavioral line}}  

### **{{another_term}}**  
- {{behavioral line}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{line_range or section pointer}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text copied byte-for-byte from the source}}  
```  

**Ref — {{another_ref_title}}**  
Source: {{source_path}}  
Locator: {{line_range}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

---  

# Boundary Domain  

### **{{boundary_term_name}}** *(owned by: {{owning_module}})*  
- {{behavioral line: how this module sees or depends on the concept}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{line_range}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

---  

<!-- EXAMPLE — delete this section after using the template. -->  

## Example (filled — Check Resolution module)  

```markdown  
---  
state: domain-language  
---  

# Module: [Check Resolution]  

Scope: The d20 resolution mechanic, checks, degrees, conditions.  

**Core terms**:  
- check  
- Difficulty Class (DC)  
- trait  
- condition  

---  

# Core Domain  

### **check**  
- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.  
- Whenever a character attempts something where outcome is in doubt, it requires a check.  
- The GM decides what kind of check applies and sets the DC.  

### **Difficulty Class (DC)**  
- The DC is a number set by the GM that a check result must equal or exceed.  
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).  

### references  

**Ref — Game Play**  
Source: context/rules/HeroesHandbook-rules__chunk_009.md  
Locator: lines 809–874  
Extract: whole  

```source  
GAME PLAY  
…verbatim text from chunk…  
```  

**Ref — Ch1 The Basics**  
Source: context/rules/HeroesHandbook-rules__chunk_005.md  
Locator: lines 244–284  
Extract: whole  

```source  
CH1 THE BASICS  
…verbatim text from chunk…  
```  

---  

# Boundary Domain  

### **Power Effect** *(owned by: Power)*  
- An effect is the basic building block of a power; it describes what a power does in game terms.  
- Resistance check DC is typically 10 + effect rank.  

### references  

**Ref — Attack Checks**  
Source: context/rules/HeroesHandbook-rules__chunk_016.md  
Locator: lines 1195–1237  
Extract: whole  

```source  
ATTACK CHECKS  
…verbatim text from chunk…  
```  
```  
