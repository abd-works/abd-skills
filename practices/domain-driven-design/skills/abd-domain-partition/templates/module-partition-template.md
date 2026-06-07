<!--  
  Module Partitioning — root index (reference-based).  

  Copy to: <workspace>/abd-domain-driven-design/module-partition.md  

  Contract:  
    - This is the ROOT INDEX — it lists all modules with scope, chunk ranges,  
      and links to per-module files. No verbatim source content lives here.  
    - Per-module detail (scope, core terms, source file references) lives in  
      abd-domain-driven-design/modules/<module-name>.md files.  
    - Reserved sections [Unallocated] and [Rejected] link to their own files  
      under modules/.  
-->  

# Module Partitioning — {{project_name}}  

Source: {{source directory or scan-map reference}}  
Modules: {{N}}  Unallocated: {{count}}  Rejected: {{count}}  

---  

## Module: [{{ModuleName}}]  
File: modules/{{module-name}}.md  
Chunks: {{range}} ({{count}} files)  
Scope: {{one or two source-grounded sentences}}.  

## Module: [{{AnotherModule}}]  
File: modules/{{another-module}}.md  
Chunks: {{range}} ({{count}} files)  
Scope: {{one or two source-grounded sentences}}.  

---  

## [Unallocated]  
{{either: "File: modules/unallocated.md" or "No unallocated source files."}}  

## [Rejected]  
File: modules/rejected.md  
Chunks: {{range}} ({{count}} files)  
