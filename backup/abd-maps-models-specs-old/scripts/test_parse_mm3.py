#!/usr/bin/env python3
"""Quick test: delete context output, run parser, verify chunk count and structure."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MM3 = SCRIPT_DIR.parent / "test" / "mm3"
CTX = MM3 / "context"
CHUNKS = CTX / "chunks"
IDX = CTX / "context_index.json"


def main() -> int:
    # 1. Delete chunks and index
    for f in CHUNKS.glob("*.md"):
        f.unlink()
    if IDX.exists():
        IDX.unlink()

    # 2. Run parser
    r = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "parse_and_curate.py"), "--path", str(MM3), "--config", str(MM3 / "solution.conf"), "--force"],
        cwd=str(SCRIPT_DIR),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if r.returncode != 0:
        print("Parser failed:", r.stderr or r.stdout)
        return 1

    # 3. Verify
    if not IDX.exists():
        print("FAIL: context_index.json not created")
        return 1
    data = json.loads(IDX.read_text(encoding="utf-8"))
    manifest = data.get("manifest", {})
    total = manifest.get("total_chunks", 0)
    if total < 100:
        print(f"FAIL: total_chunks={total}")
        return 1

    md_count = len(list(CHUNKS.glob("*.md")))
    if md_count != total:
        print(f"FAIL: chunk files={md_count} vs manifest total_chunks={total}")
        return 1

    # At least one chunk has list section_path
    sample = next(CHUNKS.glob("*.md"), None)
    if not sample:
        print("FAIL: no chunk files")
        return 1
    text = sample.read_text(encoding="utf-8")
    if "section_path:" not in text:
        print("FAIL: sample chunk has no section_path")
        return 1

    print("OK: parser ran, chunk count matches, section_path present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
