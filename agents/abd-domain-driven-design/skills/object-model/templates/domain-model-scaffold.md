<!--
  domain-model.md — typed surface (constructors, properties, operations, interactions).

  Format per class block:
    #### **ClassName**  << Stereotype >>
    + Constructor(param: Type)              ← one or more constructors (omit if factory/internal)
    ------                                  ← six dashes: constructor/init separator
    + property: Type                        ← properties and their invariants
      Invariant: ...
    ----                                    ← four dashes: property/operation separator
    + operation(param: Type): ReturnType    ← operations, invariants, and interaction blocks
      Invariant: ...
      Interaction:
        variable: Type = expression
        return variable
    ----                                    ← four dashes between operation clusters (optional)

  For classes with no constructor (factory method, internal init, pre-defined instances):
    Initialisation: <explanation>
    ------
    + property: Type
    ...
-->

## Domain model — {{project}}

---

## [Module: {{ModuleName}}]

{{Short paragraph: module owns …}}

#### **{{ClassName}}**  << {{Entity|ValueObject}} >>

+ {{ClassName}}({{param}}: {{Type}})
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

-----

#### **{{ChildClass}} : {{ParentClass}}**

+ {{ChildClass}}({{param}}: {{Type}})
------
+ {{childSpecificProperty}}: {{Type}}
	Invariant: {{...}}

-----

## [Module: {{AnotherModule}}]

#### **{{ClassName}}**  << {{Entity|ValueObject}} >>

Initialisation: {{factory method | internal | pre-defined instances — explanation}}
------
+ {{property}}: {{Type}}
----
+ {{operation}}(): {{ReturnType}}

-----
