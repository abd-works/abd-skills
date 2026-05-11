### Scenario: {scenario_name}  

**Purpose:** {what_this_validates}    
**Concepts traced:** {primary_concepts}  

---  

#### Walk 1 — Covers: {walk_scope}  

Indented walkthrough (aligns with lifelines and activations in the paired `.drawio` domain realization diagram):  

```  
{{object}}: {{ReturnType}} = new {{Class}}({{param}}: {{Type}}, {{param}}: {{Type}})  
{{result}}: {{Type}} = {{object}}.{{someMethod}}()  
    {{variable}}: {{CollaboratingClass}} = {{getter_or_lookup}}  
    {{inner}}: {{InnerType}} = {{variable}}.{{method}}({{parameter}}: {{Type}})  
        {{nested}}: {{NestedType}} = {{nested_value}} = {{AnotherClass}}.{{method}}({{param}}: {{Type}})  
        {{sibling}}: {{Type}} = {{sibling_value}} = {{AnotherCollaborator}}.{{method}}({{param}}: {{Type}})  
        return {{nested}}  
    return {{result}}: {{actual_value}}  
return  
```  

---  

#### Walk 2 — Covers: {walk_scope}  

```  
{... same pattern for another path through the objects ...}  
```  

---  

#### Walk N — Covers: {walk_scope}  

```  
{...}  
```  
