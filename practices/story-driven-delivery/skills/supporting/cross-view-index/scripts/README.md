# cross-view-index scripts

## artifact_graph_cli.py

Maintains `artifact-graph.json` — the cross-view index connecting stories to domain concepts, UX screens, and architecture mechanisms.

### Requirements

Python 3.8+. No external dependencies — uses only the standard library.

### PYTHONPATH

No special PYTHONPATH is required. Run from any directory:

```bash
python /path/to/cross-view-index/scripts/artifact_graph_cli.py <command> --file <path>
```

### Quick start

```bash
# Create an empty graph
python artifact_graph_cli.py init --file docs/artifact-graph.json --product "My Product"

# Link a story to domain/UX/arch nodes
python artifact_graph_cli.py link \
  --file docs/artifact-graph.json \
  --story "Search Products by Keyword" \
  --epic "Shop in store" \
  --sub-epic "Find products and check stock" \
  --domain Catalog.Product Catalog.SearchResult \
  --ux product-search \
  --arch catalog-api

# Look up what a story needs
python artifact_graph_cli.py lookup \
  --file docs/artifact-graph.json \
  --story "Search Products by Keyword"

# Find all stories touching a domain concept
python artifact_graph_cli.py reverse \
  --file docs/artifact-graph.json \
  --domain "Catalog.Product"

# Validate all links and file paths
python artifact_graph_cli.py validate \
  --file docs/artifact-graph.json \
  --root .

# Check for drift (missing files, dangling links)
python artifact_graph_cli.py drift \
  --file docs/artifact-graph.json \
  --root .

# Print link coverage statistics
python artifact_graph_cli.py stats \
  --file docs/artifact-graph.json
```

### Commands

| Command | Purpose |
|---|---|
| `init` | Create an empty `artifact-graph.json` from the built-in template |
| `read` | Load and pretty-print the graph (also validates schema) |
| `validate` | Check all node file paths exist and all story links resolve to registered nodes |
| `link` | Add or update cross-view links for a single story |
| `lookup` | Show all artifacts (domain, UX, arch) linked to a story |
| `reverse` | Show all stories that link to a given domain concept, UX screen, or arch mechanism |
| `drift` | Report missing files and dangling story links |
| `stats` | Print link coverage statistics (total stories, how many have domain/UX/arch links) |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure, missing file, or bad input |
