<!--  
  Normative shape for the class-model phase output.  

  Output: <deliverables-folder>/[<name>-]class-model.md  
          (or <deliverables-folder>/modules/<module-name>-class-model.md  
           for multi-module engagements)  

  This skill produces a STANDALONE file. It does not enrich the prior phase's  
  file in place. It is a fresh artifact in the same flat heading shape every  
  other DDD phase skill uses.  

  Consistent shape across every DDD phase skill:  

    ## **{{KAName}}**  

    [Optional 1—2 sentence intro]  

    ### **{{ka_name as a Class}}** << Stereotype >>      ? MUST appear first  
    + Constructor(param: Type)  
    ------  
    + property: Type  
    	Invariant: rule  
    + << composition >> ownedProperty: Type  
    ----  
    + operation(param: Type): ReturnType  
    	Invariant: rule  
    	Interaction:  
    		variable: Type = expression  
    		return variable  

    ### **{{another Class}} : {{BaseClass}}** << Stereotype >>  
    + deltaProperty: Type  

    ### references                                       ? one per KA, peer to classes  
    **Ref — title**  
    Source: ...  
    Locator: ...  
    Extract: whole  

    ```source  
    verbatim  
    ```  

    ### decisions made                                   ? one per KA  
    - decision rationale  

  Class member format:  
    ------ (six dashes)        constructor / init separator  
    ----   (four dashes)       property / operation separator (or operation cluster separator)  

  For classes with no constructor (factory method, internal init, pre-defined instances):  
    Initialisation: <explanation>  
    ------  
    + property: Type  
    ...  

  Contract:  
    - One file per phase. Do not enrich a prior file in place.  
    - The KA's own class is listed FIRST under the ## **KA** heading.  
    - Class members live directly under each ### **Class** heading.  
    - Subtypes use ### **Child : Parent** notation; deltas only.  
    - Every class has a stereotype (<< Entity >>, << ValueObject >>, etc.).  
    - One ### references and one ### decisions made per KA.  
-->  

---  
---  

# Module: [{{ModuleName}}]  

Scope: {{bounded slice or engagement scope}}  

---  

# Core Domain  

## **{{KAName}}**  

{{Optional 1—2 sentence intro: what this KA owns at the typed-model level.}}  

### **{{ka_name_as_a_Class}}** << {{Entity|ValueObject|Service|Factory|Repository|DomainEvent}} >>  

+ {{ka_name_as_a_Class}}({{param}}: {{Type}})  
------  
+ {{property}}: {{Type}}  
	Invariant: {{declarative rule tied to this member}}  
+ << composition >> {{ownedProperty}}: {{Type}}  
----  
+ {{operation}}({{param}}: {{Type}}): {{ReturnType}}  
	Invariant: {{...}}  
	Interaction:  
		{{variable}}: {{Type}} = {{expression}}  
		return {{variable}}  

### **{{ChildClass}} : {{ParentClass}}** << {{Stereotype}} >>  

+ {{ChildClass}}({{param}}: {{Type}})  
------  
+ {{childSpecificProperty}}: {{Type}}  
	Invariant: {{...}}  

### references  

**Ref — {{ref_title}}**  
Source: {{source_path}}  
Locator: {{locator}}  
Extract: {{whole or partial}}  

```source  
{{verbatim text}}  
```  

### decisions made  

- {{constructor injection vs internal init vs factory; relationship flavor; Entity vs Value Object; collaborator-omission decisions; lifecycle observation}}  

---  

# Boundary Domain  

### **{{BoundaryClass}}** << {{Stereotype}} >>  

Initialisation: {{factory method | internal | pre-defined instances — explanation}}  
------  
+ {{property}}: {{Type}}  
----  
+ {{operation}}(): {{ReturnType}}  

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
