---
name: node-files-exist
description: Every node registered in domain_nodes, ux_nodes, and arch_nodes must have a file path that exists on disk.
severity: error
---

# Node file paths must exist

Every `domain_nodes`, `ux_nodes`, and `arch_nodes` entry must have a `file` field pointing to a real file (or directory for architecture specification folders) at the workspace root.

## Why

A node with a non-existent file path means the artifact was deleted, moved, or renamed without updating the graph. Skills following the link will fail to load the artifact — the index becomes misleading rather than helpful.

## How to fix

- If the file was moved: update the `file` field in the node entry to the new path.
- If the file was deleted: remove the node from the graph and remove all story links referencing it.
- If the file hasn't been created yet: create it first, then register the node.

Run `artifact_graph_cli.py drift --file <path> --root <workspace-root>` to detect all node file issues in one pass.

## Checked by

```bash
python artifact_graph_cli.py validate --file <path> --root <workspace-root>
python artifact_graph_cli.py drift    --file <path> --root <workspace-root>
```
