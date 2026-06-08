<!--  
  Normative shape for the scenario-walkthrough phase output.  

  Output: <deliverables-folder>/[<name>-]walkthrough.md  
          (or <deliverables-folder>/modules/<module-name>-walkthrough.md  
           for multi-module engagements)  

  This skill produces a STANDALONE file. It does not enrich the prior phase's  
  file in place. It is a fresh artifact in the same flat heading shape every  
  other DDD phase skill uses.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**  

    [Optional 1–2 sentence intro]  

    ### **{{Scenario Name}}**  
    **Purpose:** what this scenario validates  
    **Concepts traced:** Class, Class  

    #### Walk 1 — Covers: {walk scope}  
    ```  
    object: ReturnType = new Class(param: Type)  
    result: Type = object.someMethod()  
        variable: CollaboratingClass = getter_or_lookup  
        return result  
    return  
    ```  

    ### **{{Another Scenario}}**  
    **Purpose:** ...  
    **Concepts traced:** ...  

    #### Walk 1 — Covers: ...  
    ```  
    ...  
    ```  

    ### references                            ← one per KA, peer to scenarios  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

    ### decisions made                        ← one per KA, peer to scenarios  
    - gap recorded, ownership decision, alternate-path trade-off, or open question  

  Minimum coverage per KA (adapt to domain):  
    - One happy path  
    - One failure or edge path  
    - One path involving cooperation or shared resources  

  Contract:  
    - One file per phase. Do not enrich a prior file in place.  
    - Use real domain values, not placeholders.  
    - Every pseudocode line that performs domain logic ties to a class and  
      operation from the prior-phase file.  
    - Untraceable lines are recorded as gaps under ### decisions made.  
-->  

---  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope}}  

---  

# Core Domain  

## **{{KAName}}**  

### **{{Scenario Name}}**  

**Purpose:** {{what this scenario validates}}  
**Concepts traced:** {{Class}}, {{Class}}, {{Class}}  

#### Walk 1 — Covers: {{happy path scope}}  

```  
{{object}}: {{ReturnType}} = new {{Class}}({{param}}: {{Type}}, {{param}}: {{Type}})  
{{result}}: {{Type}} = {{object}}.{{someMethod}}()  
    {{variable}}: {{CollaboratingClass}} = {{getter_or_lookup}}  
    {{inner}}: {{InnerType}} = {{variable}}.{{method}}({{parameter}}: {{Type}})  
        {{nested}}: {{NestedType}} = {{AnotherClass}}.{{method}}({{param}}: {{Type}})  
        return {{nested}}  
    return {{result}}: {{actual_value}}  
return  
```  

#### Walk 2 — Covers: {{failure or edge path}}  

```  
{{...}}  
```  

### **{{Another Scenario}}**  

**Purpose:** {{...}}  
**Concepts traced:** {{...}}  

#### Walk 1 — Covers: {{cooperation or shared resource path}}  

```  
{{...}}  
```  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text grounding the scenario in source material}}  
```  

### decisions made  

- {{gap recorded; ownership decision; alternate-path trade-off; open question}}  

---  

# Boundary Domain  

### **{{Boundary Scenario}}**  

**Purpose:** {{what cross-module flow this validates}}  
**Concepts traced:** {{Class}} (boundary)  

#### Walk 1 — Covers: {{...}}  

```  
{{...}}  
```  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

### decisions made  

- {{boundary scenario notes}}  
