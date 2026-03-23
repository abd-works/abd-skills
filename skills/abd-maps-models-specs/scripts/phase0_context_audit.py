#!/usr/bin/env python3
"""
Phase 0 — Context chunking approach audit (see content/parts/process.md and phases/context-chunking-approach.md).

Canonical source paths and roles come from solution.conf → manifest_sources[] (see conf/README.md).
Writes metrics + decision gate under output_dir/phase0/.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from _config import (
    CHUNKS_DIR,
    CONTEXT_INDEX,
    OUT_ROOT,
    PHASE0,
    SKILL_ROOT,
    resolved_manifest_sources,
)


SCHEMA_VERSION = "phase0/v1"


def _sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    PHASE0.mkdir(parents=True, exist_ok=True)
    canonical_sources_sha256: dict[str, str | None] = {}
    rms = resolved_manifest_sources()
    all_hashes_ok = bool(rms)
    for abs_p, _role, rel in rms:
        canonical_sources_sha256[rel] = _sha256_file(abs_p)
        if canonical_sources_sha256[rel] is None:
            all_hashes_ok = False

    chunk_files = sorted(CHUNKS_DIR.glob("unit_*.md")) if CHUNKS_DIR.is_dir() else []
    index_blocks: list = []
    if CONTEXT_INDEX.is_file():
        try:
            data = json.loads(CONTEXT_INDEX.read_text(encoding="utf-8"))
            index_blocks = data.get("blocks") or data.get("sections") or []
        except (json.JSONDecodeError, OSError):
            index_blocks = []

    evidence_types = Counter()
    reasons = Counter()
    for b in index_blocks:
        if isinstance(b, dict):
            et = b.get("evidence_type") or "unknown"
            evidence_types[str(et)] += 1
            r = b.get("reason") or "unspecified"
            reasons[str(r)] += 1

    decision = "insufficient"
    if chunk_files and CONTEXT_INDEX.is_file() and all_hashes_ok:
        decision = "sufficient"

    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_sources_sha256": canonical_sources_sha256,
        "chunk_file_count": len(chunk_files),
        "context_index_block_count": len(index_blocks),
        "evidence_type_counts": dict(evidence_types),
        "reason_counts": dict(reasons),
        "decision": decision,
        "notes": "Per Phase 0 (context readiness) — adopt or rebuild context package; sources from solution.conf manifest_sources.",
    }
    out = PHASE0 / "phase0_audit_metrics.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out.relative_to(SKILL_ROOT)} decision={decision}")


if __name__ == "__main__":
    main()
