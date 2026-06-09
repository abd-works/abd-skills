# Scenario Walkthrough � Concepts

## Prerequisites

This skill **requires a typed model or domain model** to walk through. If neither exists, run `abd-domain-model` and (optionally) `abd-domain-specification` first. Do not invent scenarios disconnected from the modeled classes.

## Consistent shape

```
## **{{KAName}}**

[Optional 1�2 sentence intro: which scenarios live under this KA]

### **{{Scenario Name}}**
**Purpose:** what this scenario validates
**Concepts traced:** Class, Class, Class

#### Walk 1 � Covers: {walk scope}
```
object: ReturnType = new Class(param: Type, param: Type)
result: Type = object.someMethod()
    variable: CollaboratingClass = getter_or_lookup
    inner: InnerType = variable.method(parameter: Type)
        nested: NestedType = AnotherClass.method(param: Type)
        return nested
    return result
return
```

#### Walk 2 � Covers: {alternate / failure path}
```
�
```

### **{{Another Scenario}}**
**Purpose:** �
**Concepts traced:** �

#### Walk 1 � Covers: �
```
�
```

### references                              ? one per KA, peer to scenarios
**Ref � title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made                          ? one per KA, peer to scenarios
- gap recorded, ownership decision, alternate-path trade-off, or open question
```

The Boundary Domain is one flat group with shared `### references` and `### decisions made`.
