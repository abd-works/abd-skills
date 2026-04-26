---
catalogue_summary: >-
  Source docs to Markdown, then labeled chunks in memory/, then FAISS vectors and
  semantic search. Optional: review context_chunking_spec.yaml before chunk+embed.
---

# abd-context-to-memory

## Overview

**Pipeline:** source documents → **Markdown** (`markdown/`) → **chunking spec** + **chunks** (`memory/`) → **embed** (`memory/rag/`, FAISS) → **search**. You can stop after drafting the spec to tune chunk boundaries (**strategy pass**) or run end-to-end in one go.

Stage commands and flags: **`skills/abd-*/SKILL.md`** and each skill's **`references/`**. Behaviour and checklists: build **`AGENTS.md`** from **`content/`** (`python scripts/build.py`).

## How it fits together

```ascii
source docs / assets
           |
           v
     Markdown (markdown/)
           |
           v
  chunking spec + chunks (memory/)
           |
           v
     FAISS index + search (memory/rag/)
```

## Source

- [AGENTS.md](AGENTS.md) (generated from `content/`)
- Regenerate catalogue: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
