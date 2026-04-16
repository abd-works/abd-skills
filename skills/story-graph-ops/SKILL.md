---
name: story-graph-ops
description: >-
  Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics,
  stories, AC, scenarios) as a **standalone artifact**—no host app required. **Agents must complete
  the ops loop**: use this skill’s CLI or Python modules under scripts/, then validate the
  file—do not stop after hand-writing JSON from memory or from reading other repositories for “schema hints.”
  Prefer the story-graph CLI; use story_map and related modules for richer edits. Complements
  ABD practice skills—ops skill owns the serialized graph lifecycle on disk.
---

# story-graph-ops

## Agent obligations (do not skip)

This skill is **not** satisfied by “I read some other project’s graph code and emitted JSON.” That is a **supplement** at most—and **out of scope** for claiming this skill is done.

| Must | Detail |
| --- | --- |
| **Use this skill’s tooling** | Run **`scripts/story_graph_cli.py`** and/or import from **`story_map`** with **`PYTHONPATH`** including **`…/story-graph-ops/scripts`** (path below). |
| **Finish with validation** | After creating or changing a graph file, run at least: **`story_graph_cli.py read --file <path>`** so a bad structure fails early. Prefer **`names`** or **`search`** when checking coverage. |
| **Declare completion** | Say what you ran (e.g. “validated with `read`”)—not only “wrote JSON.” |

**Anti-patterns (reject):**

- Hand-rolling JSON and stopping without **`read`** (or equivalent load via `story_map`).
- Using **another codebase’s** loaders or domain classes as the *only* authority while ignoring this skill’s CLI—those are not proof the serialized file is valid for **story-graph-ops** tooling.
- Skipping **`PYTHONPATH`** then claiming the skill was followed.

**When converting from Markdown, `.txt`, or chat:** build or edit JSON using **`story_map`** in Python **or** write JSON and pipe through **`write`**, then **`read`**—same validation rule.

## Skill root and PYTHONPATH

From the **agilebydesign-skills** repo, this skill’s scripts live next to this file:

- **Skill directory:** `skills/story-graph-ops/`
- **Scripts:** `skills/story-graph-ops/scripts/`

```text
# Windows PowerShell example (adjust drive/path to your clone):
$env:PYTHONPATH = "C:\dev\agilebydesign-skills\skills\story-graph-ops\scripts"
cd C:\dev\agilebydesign-skills\skills\story-graph-ops
python scripts/story_graph_cli.py read --file C:\path\to\story-graph.json
```

Add **`…/execute_using_rules/scripts`** only if you import **`scanner_bases`** in the same process.

## Mandatory workflow (checklist)

Use this whenever **`story-graph.json`** (or any graph path) is created or meaningfully edited:

1. **Set `PYTHONPATH`** to include **`story-graph-ops/scripts`**.
2. **Produce JSON** via CLI `write`, or Python (`story_map`, etc.), or a careful hand-edit.
3. **Validate:** `python scripts/story_graph_cli.py read --file <path>` (must succeed).
4. **Optional checks:** `names`, `search`, `filter` as needed.
5. **Report** the validation command you ran.

## When to use this skill

Load **story-graph-ops** whenever work touches **`story-graph.json`** as an artifact:

| Operation | Examples |
| --- | --- |
| **Create** | New graph from scratch; minimal/empty scaffold; build structure from structured input; first save after shaping content. |
| **Read** | Inspect graph, dump JSON, list names, search substring. |
| **Update** | Add/rename/reorder nodes; fix acceptance criteria or scenarios; examples; associate test files, test classes or methods; merge branches of the tree; patch one story or one epic. |
| **Delete** | Remove a story, sub-epic, or epic subtree; strip AC; **replace entire graph** by writing new JSON (delete all prior content). |

Typical situations:

- Turning a story map in any form into **concrete graph JSON**—create/update nodes until the file matches intent.
- Output of ABD practice skills (e.g. abd-story-mapping) cleaned up in MD, txt, or other format and the graph must be updated: rename stories, fix AC, reorder nodes.
- **Mechanical passes**: list story names, subset by story name, dump JSON, write through.
- A filtered view: filter by node type, increments, etc.
- **Rules/scanners** on the graph: validators extend **`StoryScanner`** from **`story_scanner`** (on **`PYTHONPATH`** with **`story-graph-ops/scripts`**).

## Relationship to ABD practice skills

| Piece | Role |
| --- | --- |
| **ABD practice skills** | **Guidance and best practices** for Agile by Design work: how to frame problems, name and structure artifacts, use templates, run quality passes, and apply bundled rules or scanners. They answer *what good looks like* and *which conventions apply*—not the mechanical layer of reading or writing `story-graph.json` on disk. |
| **story-graph-ops** | **Lifecycle on disk**: create, read, update, and delete the **serialized graph** (`story-graph.json`, in whole or in part)—encoding, mutating, and tooling against the file. |

**Same complementary relationship** in every case: use **practice skills** for *how the work should read* and *which quality bars to hit*; use **story-graph-ops** to *create and edit the graph file* **and validate it with this skill’s tools**. Whenever the deliverable includes **creating or changing** `story-graph.json`, load **story-graph-ops** and **complete the checklist above**.

## CLI

Implementation: **`scripts/story_graph_cli.py`**.

```text
python scripts/story_graph_cli.py read --file <path/to/story-graph.json> [--pretty]
python scripts/story_graph_cli.py names --file <path>
python scripts/story_graph_cli.py search --file <path> --substring <text>
python scripts/story_graph_cli.py filter --file <path> --stories "A","B" [--pretty]
python scripts/story_graph_cli.py write --file <out.json> [--input <in.json>|stdin]
```

**Create / delete via CLI:** `write` accepts JSON on stdin or `--input`—you can emit a **full replacement** graph (effectively delete everything not in the new JSON) or a **filtered** subgraph. Finer-grained create/update/delete often uses **`story_map`** types in Python, then **`read`** to validate after saving.

## Relationship to other skills

| Piece | Role |
| --- | --- |
| **execute_using_rules** | Base rules bundler: **`run_scanners.py`**, violations, scan context. Prepends **`story-graph-ops/scripts`** then **`execute_using_rules/scripts`** on **`PYTHONPATH`** for scanners. |

Practice skills that ship graph-aware rules or scanners (importing **`story_map`** / **`StoryScanner`**): see **Relationship to ABD practice skills** above; **`execute_using_rules`** runs the scanner pipeline.

**Rules that need the graph:** declare `scanner:` in rule frontmatter; scanner modules use **`from story_map import …`**, **`from story_scanner import StoryScanner`**, plus **`scanner_bases`**. Shared graph code lives only in **story-graph-ops** — not under **`scanner_bases`**.

## Sources

- Python modules: **`scripts/story_map.py`**, **`scripts/story_scanner.py`**, **`scripts/graph_filters.py`**, …
- CLI: **`scripts/story_graph_cli.py`**
- Details: **`scripts/README.md`**
