# Rule: Research paths cite real file evidence

Every research path in `research-paths.md` must name at least one file that exists on disk and must specify where in that file the architectural concern is visible.

## DO

- Name specific files with paths relative to the project root.
- Include line numbers or line ranges when the concern is localized to a section of a file.
- When an entire file is relevant, write the path without line numbers — that is acceptable.

## DO NOT

- Do not create a research path that names only a folder or module without a concrete file.
- Do not reference files that have not been opened and verified to exist on disk.
- Do not describe the architectural concern in abstract terms without pointing to where in the codebase it is visible.

## Examples

**DO** — ties concern to specific files and line ranges:
```markdown
Files:
  - src/Crowds/CharacterExplorerViewModel.cs (lines 42–58)
  - src/Identities/Camera.cs
```

**DO NOT** — names only a directory, no file evidence:
```markdown
Files: src/Crowds/ (all ViewModel files)
```
