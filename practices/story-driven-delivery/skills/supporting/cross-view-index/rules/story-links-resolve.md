---
name: story-links-resolve
description: Every story_links entry references only node IDs that exist in domain_nodes, ux_nodes, or arch_nodes.
severity: error
---

# Story links must resolve

Every entry in `story_links[*].domain`, `story_links[*].ux`, and `story_links[*].arch` must be a key that exists in the corresponding `domain_nodes`, `ux_nodes`, or `arch_nodes` section of the same `artifact-graph.json` file.

## Why

A story link pointing to an unregistered node ID is invisible drift — the graph claims a connection exists but provides no path to the artifact. Skills following the link will silently fail or fall back to loading full files, defeating the purpose of the index.

## How to fix

1. Add the missing node to the appropriate section (`domain_nodes`, `ux_nodes`, or `arch_nodes`) with its `file` path.
2. Run `artifact_graph_cli.py validate --file <path>` to confirm the error is resolved.

## Checked by

```bash
python artifact_graph_cli.py validate --file <path>
```
