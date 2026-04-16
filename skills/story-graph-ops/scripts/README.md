# story-graph-ops scripts

Python modules live **directly in this folder** (no nested package). With **`…/story-graph-ops/scripts`** on **`PYTHONPATH`**:

| Module | Role |
| --- | --- |
| `story_map.py` | `StoryMap`, `Epic`, `SubEpic`, `Story`, `StoryGroup`, `Scenario`, node walk |
| `domain_concept_node.py` | `DomainConceptNode` for domain-concept placement |
| `story_scanner.py` | Abstract **`StoryScanner`** (extends `scanner_bases.Scanner`) |
| `graph_filters.py` | `filter_story_graph_to_story_names` (subset graph by story name) |

**Import:** `from story_map import StoryMap, …`, `from story_scanner import StoryScanner`, …  
**Scanners:** use **`scanner_bases`** for generic types (`Scanner`, `Violation`, …) and **`story_map`** / **`story_scanner`** for graph types — graph types are **not** re-exported from **`scanner_bases.__init__`**.

## `story_scanner_runner.py` (shim)

Re-exports **`scanner_runner`** from **execute_using_rules** (`execute_scan_with_workspace`, `load_workspace_graph_json`, `main_with_scanner`, …) so older imports keep working. Prefer **`from scanner_runner import …`** in **`execute_using_rules/scripts`**.

## `story_graph_cli.py`

Command-line access to read / list names / search / filter / write JSON. See **`../SKILL.md`**.

## PYTHONPATH

For subprocesses that import only **`story_map`** / **`story_scanner`** (no `scanner_bases`), prepend:

`skills/story-graph-ops/scripts`

For **`StoryScanner`**, you also need:

`skills/execute_using_rules/scripts`

**`run_scanners.py`** sets both for scanner CLIs.
