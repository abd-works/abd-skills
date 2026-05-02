<!--
  domain-model.md — typed surface (properties, methods, relationships).

  Canonical layout: skills/ooad/templates/domain model template.md
  This scaffold is the engagement starter; expand using the Example in that file.
-->

## Domain model - {{project}}

One file. Match **Example** and **Conventions** in `skills/ooad/templates/domain model template.md`.

---

## [Module: {{ModuleName}}]

{{Short paragraph: module owns …}}

{{ClassName}} << {{Entity|ValueObject}}? >>
{{What this class owns in one or two sentences.}}
----
+ {{property}}:{{Type}} {{[*..1] optional cardinality}}
+ {{relatedProperty}}:{{Type}} [*..1]
+ {{method}}({{param}}:{{Type}}): {{ReturnType}}
    Invariant: {{declarative rule tied to this member}}
----
+ {{STATE_OR_ENUM_NAME}}:{{Type}} [*..1]
+ {{anotherMethod}}(): {{ReturnType}}
    Invariant: {{...}}

{{ChildClass}} : {{ParentClass}}
{{Delta description.}}
----
+ {{childSpecificProperty}}:{{Type}}

{{ENUM_OR_CONSTANT_GROUP_NAME}}
Typed constants (UPPER_CASE):
    {{CONST_A}} = {{value}}
    {{CONST_B}} = {{value}}

-----

## [Module: {{AnotherModule}}]

{{ClassName}} << {{Entity?}} >>
+ {{property}}:{{Type}}
+ {{method}}(): {{ReturnType}}

-----
