<!--
  Template: mechanism-tier architecture-context.md
  Use for FOLDERS THAT HOST A REUSABLE, TEMPLATED PATTERN — one that you expect
  multiple new features to extend in the same shape (e.g. Partner Integrations,
  Identity Setup, Failure Handling, Configuration & Secrets).

  PLACEMENT: this file lives in the folder it documents, NEXT TO the code it describes
  (e.g. src/integrations/architecture-context.md). It is referenced by the main spec
  using a workspace-root link like [src/integrations/](/src/integrations/architecture-context.md).

  USE WHEN: the folder defines a pattern other developers will copy. There IS a
  recipe. The recipe has a fixed skeleton + optional parts + canonical code.

  DELETE the leading "Template:" instruction block before shipping. Keep the
  section headings; remove any section that genuinely does not apply to your
  mechanism (but if you're cutting more than one, it is probably a Package, not
  a Mechanism — switch templates).
-->

# Mechanism: {{MechanismName}}

### Overview

{{One short paragraph that answers: what is this mechanism for, what does it
own, and what does nothing else in the codebase own.}}

{{One short paragraph that names the composition root (or equivalent
registration point), the file skeleton each instance follows, and the role of
the central type (e.g. "the handler orchestrates the call").}}

### File Structure

```
{{folder tree showing the universal files (always present) and the optional
files (annotated "optional"). Use placeholder names like {System} or {Feature}
for the parts that vary per instance.}}
```

### Participants

{{One sentence anchoring where every file lives.}}

**{{Role}}** -- {{what it does in one sentence}}. [`{{file/path}}`](/{{file/path}})

**{{Role}}** *(optional)* -- {{what it does in one sentence; when it is present}}. [`{{file/path}}`](/{{file/path}})

{{...one paragraph per participant in the skeleton.}}

### Class Specification

```
## {{Class1Name}}  << {{Stereotype}} >>
Initialisation: {{when and how}}
------
+ {public method}({params}): {return}
    Interaction:
        {step}
        {step}
    catch (error) -> {{handler}}
----
- {private method}({params}): {return}
    Interaction:
        {step}
----

## {{Class2Name}}  << {{Stereotype}} >>  [optional]
...
```

### Rules

- **{{Rule that constrains how new instances of the mechanism are added}}** -- {{rationale or what failure looks like}}.
- **{{Rule that names what must always happen}}** -- {{...}}.
- **{{Rule that names what must never happen}}** -- {{...}}.
- {{...add as many as the mechanism needs; each rule is enforceable by reading code.}}

### Canonical Patterns

```{{language}}
// {{file in the skeleton}} -- one-line purpose
{{minimal code showing the canonical shape; uses placeholder names like
{System}, {operation}, {Domain}; readers copy + rename}}
```

{{Repeat one code block per file in the skeleton that has a non-trivial shape.}}

### Across the Codebase

{{Optional but recommended when there are multiple existing instances. Table
listing each instance and which optional parts it uses, plus any deviation from
the canonical pattern. The point is to make drift visible.}}

| Instance | {{optional1}} | {{optional2}} | Deviation |
|---|:---:|:---:|---|
| {{Name1}} | yes | - | {{what is different and why; or "none"}} |
| {{Name2}} | - | yes | {{...}} |
