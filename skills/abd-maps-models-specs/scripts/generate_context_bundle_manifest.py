#!/usr/bin/env python3
"""Record hashes for workspace sources and phase outputs — bundle manifest."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from _config import (
    CANDIDATE_QUEUE_JSON,
    CONTEXT_INDEX,
    MECHANISMS_JSON,
    OUT_ROOT,
    SKILL_ROOT,
    TERMS_LAYER_JSON,
    resolved_manifest_sources,
    workspace_root,
)


def _path_for_log(path: Path) -> str:
    try:
        return str(path.relative_to(SKILL_ROOT))
    except ValueError:
        try:
            return str(path.relative_to(workspace_root()))
        except ValueError:
            return str(path)


def _hash_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    sources: dict[str, str | None] = {}
    for abs_p, _role, rel in resolved_manifest_sources():
        sources[rel] = _hash_file(abs_p)
    try:
        idx_rel = CONTEXT_INDEX.relative_to(workspace_root())
    except ValueError:
        idx_rel = CONTEXT_INDEX
    sources[str(idx_rel).replace("\\", "/")] = _hash_file(CONTEXT_INDEX)

    manifest = {
        "schema": "bundle_manifest/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "outputs": {
            TERMS_LAYER_JSON: _hash_file(OUT_ROOT / TERMS_LAYER_JSON),
            MECHANISMS_JSON: _hash_file(OUT_ROOT / MECHANISMS_JSON),
            CANDIDATE_QUEUE_JSON: _hash_file(OUT_ROOT / CANDIDATE_QUEUE_JSON),
        },
    }
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    out = OUT_ROOT / "context_bundle_manifest.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {_path_for_log(out)}")


if __name__ == "__main__":
    main()
