"""
Incremental ``--update`` helpers: manifests and pruning chunk outputs.

Manifests live under ``PIPELINE_ROOT`` (convert + chunk). Vector search uses Pinecone only (TypeScript); there is no local FAISS index in this repo.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def convert_manifest_path(pipeline_root: Path) -> Path:
    return pipeline_root / "convert_manifest.json"


def chunk_manifest_path(pipeline_root: Path) -> Path:
    return pipeline_root / "chunk_manifest.json"


def delete_chunk_outputs_for_stem(chunk_dir: Path, stem: str) -> int:
    """Remove ``stem.md`` and ``stem__*.md`` under chunk_dir. Returns files removed."""
    n = 0
    if not chunk_dir.is_dir():
        return 0
    for pattern in (f"{stem}.md", f"{stem}__*.md"):
        for p in chunk_dir.glob(pattern):
            if p.is_file():
                p.unlink()
                n += 1
    return n
