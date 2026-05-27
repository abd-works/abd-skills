# `scanner_bases` — shared scanner infrastructure

Python package used by:

- **`run_scanners.py`** — prepends **`…/story-graph-ops/scripts`** then **`…/execute-skill-using-skills-rules/scripts`** to **`PYTHONPATH`** for each scanner subprocess.
- **`scanner_runner.py`** (beside this package) — **one** driver for every scanner: build a **`ScanFilesContext`** (call site chooses `files`, `story_graph` JSON payload, or both) → **`SimpleRule`** → **`scan_with_context`** → violations / exit code. Helpers: **`execute_scan_with_workspace`**, **`load_workspace_graph_json`** (file paths only; no story domain types).
- **[abd-story-mapping](../../abd-story-mapping/scanners/)** — imports **`scanner_bases`** for **`Scanner`**, **`Violation`**, **`ScanFilesContext`**, …; imports **`story_map`**, **`story_scanner`**, … from **[story-graph-ops](../../story-graph-ops/scripts/)** — not in **`scanner_bases`**.

## Contents

| Module | Role |
| --- | --- |
| `scanner.py` | Abstract `Scanner` |
| *(see [story-graph-ops](../../story-graph-ops/scripts/README.md))* | **`StoryScanner`**, **`StoryMap`**, epics/stories, **`DomainConceptNode`**, **`graph_filters`** |
| `violation.py` | Violation DTO + `to_dict()` |
| `simple_rule.py` | `RuleLike` protocol + `SimpleRule` (standalone; no dependency on a host bot’s `actions.rules`) |
| `eval_paths.py` | Paths from rule file (workspace, baseline, behavior dir) |
| `resources/scan_context.py` | `ScanFilesContext`, `FileScanContext`, … |
| `vocabulary_helper.py` | **`VocabularyHelper`** — NLTK WordNet / POS-tag helpers for naming rules (verb/noun, actors, passive voice). Import as **`scanner_bases.vocabulary_helper`** (not re-exported from **`scanner_bases.__init__`** to avoid NLTK import side effects). Requires **`nltk`**. |

## Layout note

The **`agile_bots`** repo may use a top-level package named **`scanners`** on **`PYTHONPATH`**. This skills repo uses **`scanner_bases`** as the import name so it does not clash with a different **`scanners`** folder on disk.

## Verify after edits

```powershell
cd skills/execute-skill-using-skills-rules/scripts
$env:PYTHONPATH = (Get-Location).Path
python -c "import scanner_bases; print('ok')"
```
