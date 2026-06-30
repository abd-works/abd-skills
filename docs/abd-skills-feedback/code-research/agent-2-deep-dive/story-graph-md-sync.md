# Deep Dive: Story Graph Operations & MD ↔ JSON Sync

## Principles & Patterns

- **Graph as single source of truth — for tools**: `story-graph.json` is the machine-readable artifact every downstream tool (story map renderer, AC injector, thin-slice merger) reads and writes.
- **MD as single source of truth — for humans**: `story-map.md` is what product owners author and review; the MD tree is the canonical structural input.
- **Unidirectional MD → JSON pipeline**: `md_story_map_to_story_graph.py` converts MD to JSON. There is no reverse converter and no parity checker.
- **SHA-stamped writes prevent concurrent overwrite, not human/machine drift**: `story_graph_cli.py write --expect-sha $SHA` protects against two writers stomping each other; it does nothing to ensure the JSON matches the MD that produced it.
- **Ad-hoc Python patch scripts mutate the JSON directly**: the session journal documents using `patch_missing_epics.py` to add sub-epics to the JSON without touching the MD (lines 351–353).

## File Structure

```
practices/story-driven-delivery/skills/supporting/story-graph-ops/
├── SKILL.md
├── scripts/
│   ├── story_graph_cli.py                       ← CRUD on JSON; read, write, names, sha
│   ├── md_story_map_to_story_graph.py           ← MD → JSON
│   ├── md_acceptance_criteria_to_story_graph.py ← MD → JSON (AC merge)
│   ├── md_thin_slice_to_story_graph.py          ← MD → JSON (thin-slice merge)
│   ├── story_map.py                              ← shared model
│   ├── story_scanner.py                          ← scanner base
│   ├── story_graph_file.py                       ← load/save with validation
│   └── graph_filters.py                          ← graph query helpers
├── tests/
└── logs/
```

## Participants

| Component | Direction | Notes |
|---|---|---|
| `md_story_map_to_story_graph.py` | MD → JSON | Reads `story-map.md`, emits `story-graph.json` |
| `md_acceptance_criteria_to_story_graph.py` | MD → JSON | Merges AC into existing JSON |
| `md_thin_slice_to_story_graph.py` | MD → JSON | Merges thin-slice plan into JSON |
| `story_graph_cli.py write` | JSON → JSON | Validated write with SHA check |
| *(missing) check-md-graph-parity* | n/a | Would detect divergence |
| *(missing) JSON → MD renderer* | n/a | Would reconcile graph-only edits |

## Flow

**Intended flow:**
1. Author edits `story-map.md`.
2. Author runs `md_story_map_to_story_graph.py` to regenerate `story-graph.json`.
3. Downstream tools (drawio-story-sync, AC merge, etc.) read the JSON.

**Actual flow that broke in the session:**
1. Author edits `story-map.md`.
2. Author runs `md_story_map_to_story_graph.py` to regenerate `story-graph.json`.
3. Some scenarios reveal new sub-epics needed.
4. Author runs `patch_missing_epics.py` to inject sub-epics into the JSON directly.
5. `story-map.md` is now stale.
6. Nothing fails. The session journal calls this out (lines 351–353).

## Walkthrough Example — pml-midtier session

The journal correction at lines 345–369 documents the exact failure pattern:

> Run `patch_missing_epics.py` to add "Resend Password Reset Email" to the graph, then update `story-map.md` as a separate step — leaving a window where the two files are inconsistent.

The corrected procedure is:

> Update `story-map.md` first (add the sub-epic in the correct `(E)` position). Then regenerate `story-graph.json` from the MD, or apply the same mutation to both files atomically in the same script. Validate with `story_graph_cli.py read` before proceeding.

Both the bug and the fix exist in human discipline only. The skill provides no mechanical guard. A `check-parity` mode on `story_graph_cli.py` (re-run the MD-to-JSON conversion in-memory, diff against the on-disk JSON, fail on non-zero diff) would convert this from a discipline problem into a CI-detectable error.
