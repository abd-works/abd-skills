# Rule: Research path count is bounded

`research-paths.md` must contain between 5 and 10 research paths. Fewer than 5 indicates under-coverage. More than 10 top-level paths indicates over-partitioning; related mechanisms should be grouped before Pass 2 begins.

## DO

- Aim for 6–8 paths as the working target for most codebases of any size.
- Group closely related mechanisms under one path name with a parenthetical note (e.g. *Entity State Sync (covers both read and write paths)*).
- Include a path for each layer boundary, major mechanism, and cross-cutting concern that the downstream architecture skills will need to document.

## DO NOT

- Do not produce fewer than 5 paths for any codebase larger than 500 lines.
- Do not produce more than 10 top-level paths without grouping — Pass 2 becomes unmanageable with more than 10 deep dives.
- Do not create a path that duplicates a concern already covered by another path.

## Examples

**DO** — 7 paths covering the key concerns of a WPF desktop client:
```
1. MVVM Binding
2. ViewModel Coordination
3. COH Bridge Seam
4. Entity State Sync
5. Costume Loading
6. Command Dispatch
7. Crowd / Roster Management
```

**DO NOT** — 14 micro-paths that should be grouped under *COH Bridge Seam*:
```
1. Memory Read
2. Memory Write
3. Offset Table
4. P/Invoke Declarations
5. Handle Management
6. ...
```
