<!--
  Normative shape for the domain-model phase output.

  Output: <deliverables-folder>/[<name>-]domain-model.md
          <deliverables-folder>/[<name>-]domain-model.json   (abd-domain-model/v1 — parallel to story-graph.json)
          (or <deliverables-folder>/modules/<module-name>-domain-model.md|.json
           for multi-module engagements)

  Machine-readable spine: see ../../references/domain-model-json.md and ../../references/domain-model-template.json.
  domain.json is a flat scanner vocabulary index derived from domain-model.json.

  This skill produces a STANDALONE file. It does not enrich the prior phase's
  file in place. It is a fresh artifact in the same flat heading shape every
  other DDD phase skill uses.

  Consistent shape across every DDD phase skill:

    ## **{{KAName}}**

    ### **{{ka_name as a Class}}**            ← MUST appear first; matches the KA

    ClassName(Type, Type)
    ------
    propertyName: Type
    	Invariant: rule
    ----
    methodName(Type): ReturnType
    	CollaboratorType
    	Invariant: rule

    ### **{{ChildClass}} : {{ParentClass}}**
    ChildClass(Type)
    ------
    ----
    deltaMethod(Type): ReturnType

    ### references                             ← one per KA, peer to classes
    **Ref — title**
    Source: ...
    Locator: ...
    Extract: whole

    ### decisions made                         ← one per KA, peer to classes
    - decision rationale

  Class block format:
    Constructor(Type, Type)       ← types only, no param names; omit line if no constructor
    ------  (six dashes)          ← constructor / properties separator
    propertyName: Type            ← no + prefix, no stereotypes
    	Invariant: ...
    ----    (four dashes)         ← properties / methods separator
    methodName(Type): ReturnType  ← types only, no param names, no + prefix
    	CollaboratorType          ← hidden collaborators BEFORE invariants
    	Invariant: ...
    - privateMethod(Type): Type   ← - prefix for private only

  Type rules:
    - Domain types: Stage, Ticket, Skill, etc.
    - Constrained enums: DeliveryRole, ScopeLevel, ExecutionStatus, etc.
    - Typed primitives: Timestamp, FilePath, Identifier, FreeText, etc.
    - Standard types: Boolean, Integer
    - NEVER raw String

  Contract:
    - One file per phase. Do not enrich a prior file in place.
    - The KA's own class is listed FIRST under the ## **KA** heading.
    - Class members live directly under each ### **Class** heading.
    - Subtypes use ### **Child : Parent** notation; deltas only.
    - One ### references and one ### decisions made per KA.
    - Boundary Domain is one flat group with shared references and decisions.
-->

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

{{ClassName}}({{Type}}, {{Type}})
------
{{propertyName}}: {{Type}}
	Invariant: {{declarative constraint}}
{{anotherProperty}}: {{Type}}
----
{{methodName}}({{Type}}): {{ReturnType}}
	{{CollaboratorType}}
	Invariant: {{declarative constraint}}
{{anotherMethod}}(): void

### **{{AnotherClass}}**

{{ClassName}}({{Type}})
------
{{property}}: {{Type}}
----
{{method}}({{Type}}): {{ReturnType}}

### **{{ChildClass}} : {{ParentClass}}**

{{ChildClass}}({{Type}})
------
----
{{deltaMethod}}({{Type}}): {{ReturnType}}
	Invariant: {{constraint specific to this subtype}}

### references

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

### decisions made

- {{constrained enum values, state-carrier or collection-class introduction, Liskov decision, dependency-magnet split, typed-primitive introduction, or open question}}

---

# Boundary Domain

### **{{BoundaryClass}}**

------
{{property}}: {{Type}}
----
{{method}}({{Type}}): {{ReturnType}}

### references

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

### decisions made

- {{boundary placement reasoning}}

---
