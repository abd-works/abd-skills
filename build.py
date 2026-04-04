#!/usr/bin/env python3
"""Repository root build: sync shared vendor files (e.g. DrawIO) into skill directories."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def main() -> int:
    sync = _ROOT / "scripts" / "sync_drawio_vendor.py"
    if not sync.is_file():
        print(f"ERROR: {sync} not found", file=sys.stderr)
        return 1
    argv = sys.argv[1:]
    if argv[:1] == ["check"]:
        result = subprocess.run(
            [sys.executable, str(sync), "--check"],
            cwd=str(_ROOT),
        )
        return int(result.returncode)
    result = subprocess.run([sys.executable, str(sync)], cwd=str(_ROOT))
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
