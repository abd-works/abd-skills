#!/usr/bin/env python3
"""
Scanner: Phase 1 chunk/index contract (context_index.json ↔ chunks/*.md).

Rule: **stage-1-context-decisions** + norms in ``content/parts/library/context-spec.md``

- Bidirectional alignment: every ``blocks[]`` row has ``chunks/{chunk_id}.md``; every ``chunks/*.md`` is
  indexed or listed under ``excluded``.
- Optional: front matter contains ``chunk_id`` (lightweight parse, no PyYAML).
- ``manifest.sources[]`` sha256 checked against files resolved from solution.conf workspace paths.

Exit 0 if ``context_index.json`` is missing (greenfield). Exit 1 on contract violations when index exists.
Exit 0 on pass.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

RULE_ID = "context-index-contract"


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_config_path() -> None:
    sd = _scripts_dir()
    if str(sd) not in sys.path:
        sys.path.insert(0, str(sd))


def _read_front_matter_keys(path: Path) -> dict[str, str]:
    """Return flat string keys from first YAML front matter block (simple parser)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = text[3:end]
    out: dict[str, str] = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z0-9_]+):\s*(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def main() -> int:
    _ensure_config_path()
    from _config import CHUNKS_DIR, CONTEXT_INDEX, SKILL_ROOT, workspace_root

    if not CONTEXT_INDEX.is_file():
        print(f"PASS [{RULE_ID}] — no context_index.json (Phase 1 not built yet; skip)")
        return 0
    try:
        data = json.loads(CONTEXT_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL [{RULE_ID}]: invalid JSON in {CONTEXT_INDEX}: {e}", file=sys.stderr)
        return 1

    blocks = data.get("blocks")
    if not isinstance(blocks, list):
        print(f"FAIL [{RULE_ID}]: context_index.json must have blocks[] array", file=sys.stderr)
        return 1

    excluded = data.get("excluded") or []
    excluded_ids: set[str] = set()
    for ex in excluded:
        if isinstance(ex, dict) and ex.get("chunk_id"):
            excluded_ids.add(str(ex["chunk_id"]))

    indexed_ids: set[str] = set()
    for b in blocks:
        if not isinstance(b, dict):
            continue
        cid = b.get("chunk_id") or b.get("block_id")
        if not cid:
            print(f"FAIL [{RULE_ID}]: block entry missing chunk_id and block_id", file=sys.stderr)
            return 1
        cid = str(cid)
        indexed_ids.add(cid)
        chunk_path = CHUNKS_DIR / f"{cid}.md"
        if not chunk_path.is_file():
            print(
                f"FAIL [{RULE_ID}]: index references missing chunk file "
                f"{chunk_path.relative_to(SKILL_ROOT)}",
                file=sys.stderr,
            )
            return 1
        keys = _read_front_matter_keys(chunk_path)
        if "chunk_id" not in keys:
            print(
                f"FAIL [{RULE_ID}]: {chunk_path.relative_to(SKILL_ROOT)} front matter missing chunk_id",
                file=sys.stderr,
            )
            return 1
        if keys.get("chunk_id") != cid:
            print(
                f"FAIL [{RULE_ID}]: {chunk_path.relative_to(SKILL_ROOT)} chunk_id mismatch "
                f"index={cid!r} file={keys.get('chunk_id')!r}",
                file=sys.stderr,
            )
            return 1

    if CHUNKS_DIR.is_dir():
        for p in sorted(CHUNKS_DIR.glob("*.md")):
            stem = p.stem
            if stem in indexed_ids or stem in excluded_ids:
                continue
            print(
                f"FAIL [{RULE_ID}]: chunk file not in index blocks[] or excluded: "
                f"{p.relative_to(SKILL_ROOT)}",
                file=sys.stderr,
            )
            return 1

    manifest = data.get("manifest") or {}
    sources = manifest.get("sources") if isinstance(manifest, dict) else None
    root = workspace_root()
    if isinstance(sources, list):
        for s in sources:
            if not isinstance(s, dict):
                continue
            rel = str(s.get("path", "")).replace("\\", "/").strip()
            if not rel:
                continue
            resolved = (root / rel).resolve()
            if not resolved.is_file():
                continue
            if s.get("sha256"):
                h = hashlib.sha256(resolved.read_bytes()).hexdigest()
                if h != s["sha256"]:
                    print(
                        f"WARN [{RULE_ID}]: sha256 differs from manifest.sources[] ({rel}) — re-pin after edit",
                        file=sys.stderr,
                    )

    print(f"PASS [{RULE_ID}] — {CONTEXT_INDEX.relative_to(SKILL_ROOT)} blocks={len(blocks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
