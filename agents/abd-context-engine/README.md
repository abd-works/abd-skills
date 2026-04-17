# abd-context-engine (agent bundle)

Workspace for **context-engine** agents and skills (thin-slicing, story mapping, delivery lead, etc.) plus **offline-friendly** Python dependencies used by the **`abd-context-to-memory`** pipeline (markdown conversion, chunking, embeddings, search, export).

## Python dependencies (markdown / RAG / export)

- **`requirements-all.txt`** — single manifest: `markitdown[all]`, `pymupdf`, `openai`, `faiss-cpu`, `numpy`, `python-dotenv`, `openpyxl`, `pypandoc`.
- **`vendor/wheels/`** — place wheels here for air-gapped installs (see **`vendor/README.md`**).

### Offline quick start

1. On a connected machine: `python -m pip download -r requirements-all.txt -d vendor/wheels`
2. Copy this folder to the firewalled machine.
3. `python -m pip install --no-index --find-links vendor/wheels -r requirements-all.txt`

`pypandoc` still needs the **pandoc** binary installed separately; PDF output may need **pdflatex** or another engine—those are not Python wheels.

### Scripts

- **`scripts/download_vendor_wheels.ps1`** — convenience wrapper around `pip download`.

## Layout

- **`agents/`** — agent definitions (e.g. delivery lead, team member).
- **`skills/`** — skill junctions / copies used by this engine.
- **`docs/`** — optional agent docs.
