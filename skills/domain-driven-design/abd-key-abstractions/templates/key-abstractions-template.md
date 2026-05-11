<!--  
  Normative shape for the key-abstractions phase output.  

  Output: <deliverables-folder>/[<name>-]key-abstractions.md  
          (or <deliverables-folder>/modules/<module-name>-key-abstractions.md  
           for multi-module engagements)  

  This skill produces a STANDALONE file. It is not enriched in place by later  
  phase skills (domain-sketch, CRC, object-model). Each later DDD phase skill  
  writes its own file using the same flat heading shape.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**  

    [1–2 paragraph KA prose definition — role, boundary, responsibilities,  
     relationships, invariants — woven naturally]  

    ### **{{ka_name as a term}}**       ← MUST appear first; matches the KA  
    - bullet describing the KA itself  

    ### **{{another term in this KA}}**  
    - bullet  

    ### references                       ← one per KA, peer to terms  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

    ### decisions made                   ← one per KA, peer to terms  
    - judgment call with reasoning  

  Contract:  
    - One file per phase. Do not enrich a prior file in place.  
    - The KA's own term is listed FIRST under the ## **KA** heading.  
    - Bullets live directly under each ### **term** heading — no sub-headings.  
    - One ### references and one ### decisions made per KA.  
    - The flat **Core terms** list stays as the inventory in the header.  
    - A separate **Key Abstractions (term grouping)** list shows the structure.  
-->  

---  
state: key-abstractions  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope — same as domain-language}}  

**Core terms**:  
- {{term1}}  
- {{term2}}  
- …  

**Key Abstractions (term grouping)**:  
- **{{KAName}}**: {{ka_name_as_a_term}}, {{term1}}, {{term2}}, …  
- **{{AnotherKAName}}**: {{another_ka_as_a_term}}, {{term3}}, {{term4}}, …  

**Moved to other modules**:  
- {{moved_term}} → {{DestinationModule}}  

---  

# Core Domain  

## **{{KAName}}**  

{{1–2 paragraphs of flowing prose defining this Key Abstraction. Covers what  
unique role it plays, what it owns (boundary), what it does (responsibilities),  
its relationships with other KAs, and what must always be true (rules /  
invariants). Woven together naturally — not as labeled sections.}}  

### **{{ka_name_as_a_term}}**  
- {{behavioral line about the KA itself: what it owns, what it enforces, how it relates to other KAs}}  
- {{behavioral line}}  

### **{{another_term}}**  
- {{behavioral line — carried from domain-language, unchanged in meaning}}  

### **{{another_term}}**  
- {{behavioral line}}  

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

- {{independence-test result}}  
- {{module-fit result}}  
- {{grouping call or open question}}  

---  

## **{{AnotherKAName}}**  

{{Prose definition}}  

### **{{another_ka_as_a_term}}**  
- {{behavioral line about the KA itself}}  

### **{{term}}**  
- {{behavioral line}}  

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

### **{{boundary_term}}** *(owned by: {{owning_module}})*  
- {{behavioral line: how this module sees or depends on it}}  

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
state: key-abstractions  
---  

# Module: [Check Resolution]  

Scope: The d20 resolution mechanic, checks, degrees, conditions.  

**Core terms**:  
- check  
- Difficulty Class (DC)  
- trait  
- modifier  
- degree of success  
- condition  

**Key Abstractions (term grouping)**:  
- **Check**: check, Difficulty Class (DC), trait, modifier, degree of success  
- **Condition**: condition  

---  

# Core Domain  

## **Check**  

A check is the core resolution mechanic — the single mechanism through which  
any uncertain outcome in the game is determined. It owns the  
roll-plus-modifier-versus-DC formula and serves as the single source of truth  
for whether an action succeeds or fails. A check must always produce a binary  
success/failure result; when graded, it must yield a degree downstream  
abstractions can interpret.  

### **check**  
- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.  
- Whenever a character attempts something where the outcome is in doubt, it requires a check.  

### **Difficulty Class (DC)**  
- The DC is a number set by the GM that a check result must equal or exceed.  
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).  

### **trait**  
- A trait is the character attribute (e.g. Strength, a Skill rank) that supplies the check's modifier.  

### **modifier**  
- The modifier is the numeric contribution of a trait (and circumstance) added to the d20 roll.  

### **degree of success**  
- A degree grades how far the check beat or missed the DC, used by downstream effects.  

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

### decisions made  

- Degree of success is a part of Check, not its own KA — it has no meaning outside a check (independence test).  
- DC is kept under Check rather than made standalone — it is always set in the context of a check.  
- Modifier stays under Check — it is the numeric contribution of a trait to a specific check, not an independent concept.  

---  

# Boundary Domain  

### **Power Effect** *(owned by: Power)*  
- An effect is the basic building block of a power; it describes what a power does in game terms.  

### references  

**Ref — Attack Checks**  
Source: context/rules/HeroesHandbook-rules__chunk_016.md  
Locator: lines 1195–1237  
Extract: whole  

```source  
ATTACK CHECKS  
…verbatim text from chunk…  
```  

### decisions made  

- Power Effect is owned by the Power module — this module only consumes its resistance check DC.  
```  
