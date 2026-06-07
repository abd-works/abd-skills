<!--  
  Per-module file — reference-based, no verbatim content.  

  Copy to: <workspace>/abd-domain-driven-design/modules/<module-name>.md  

  Contract:  
    - Each file contains scope, core terms, and source file references.  
    - References point to source files on disk (chunk files, documents, etc.)  
      with locators (lines, pages, chapters). No verbatim content is copied.  
    - Downstream agents read this file to learn which source files belong to  
      this module, then read those files directly.  
    - For rejected.md and unallocated.md, each reference includes a Reason: line.  
-->  

## Module: [{{ModuleName}}]  

Scope: {{one or two source-grounded sentences — what bounded scope this module covers}}.  

**Core terms**:  
- {{noun phrase the source uses}}  
- {{noun phrase the source uses}}  
- …  

---  

**Ref — {{short title}}**  
Source: {{relative/path/to/source/file.md}}  
Locator: {{lines, chapter, page — precise}}  
Extract: whole  

**Ref — {{short title}}**  
Source: {{relative/path/to/source/file.md}}  
Locator: {{lines, chapter, page}}  
Extract: partial  
Part: {{which slice is allocated}}  
Also relates to: [{{OtherModule}}] — {{one-line why}}  

---  

<!--  
  For rejected.md / unallocated.md, add Reason: lines:  

  **Ref — {{short title}}**  
  Source: {{path}}  
  Locator: {{locator}}  
  Extract: whole  
  Reason: {{why out of scope or unresolved}}  
-->  
