<!--
  Domain Scan — root index.

  Copy to: <workspace>/domain/module-partition.md

  Contract:
    - Lists all modules with scope, KA summary, and links to per-module files.
    - Per-module detail (scope, KAs, terms, source refs) lives in
      domain/modules/<module-name>.md files.
    - Reserved sections [Unallocated] and [Rejected] link to their own files.
-->

# Domain Scan — {{project_name}}

Source: {{source directory or scan-map reference}}
Modules: {{N}}  Unallocated: {{count}}  Rejected: {{count}}

---

## Module: [{{ModuleName}}]
File: modules/{{module-name}}.md
Chunks: {{range}} ({{count}} files)
Scope: {{one or two source-grounded sentences}}.
Key Abstractions: {{KA1}}, {{KA2}}, {{KA3}}, …

## Module: [{{AnotherModule}}]
File: modules/{{another-module}}.md
Chunks: {{range}} ({{count}} files)
Scope: {{one or two source-grounded sentences}}.
Key Abstractions: {{KA1}}, {{KA2}}, …

---

## [Unallocated]
{{either: "File: modules/unallocated.md" or "No unallocated source files."}}

## [Rejected]
File: modules/rejected.md
Chunks: {{range}} ({{count}} files)
