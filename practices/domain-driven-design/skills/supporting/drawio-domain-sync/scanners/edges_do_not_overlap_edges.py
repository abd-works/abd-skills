#!/usr/bin/env python3
"""
Scanner: edges_do_not_overlap_edges

Verifies that no two edges run on top of each other for more than a small
shared span. Reuses ``check_edge_on_edge_overlaps`` from drawio_tools.

Usage:
  python edges_do_not_overlap_edges.py <file.drawio> [--page PAGE]

Exit codes:
  0  no violations found
  1  one or more overlaps detected (or file error)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from drawio_tools import (  # noqa: E402
    load_drawio,
    get_page,
    check_edge_on_edge_overlaps,
)


def scan(path: Path, page: str | None = None) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    _, mxfile = load_drawio(str(path))

    if page:
        pages = [(page,)]
    else:
        pages = [(d.get("name"),) for d in mxfile.findall("diagram")]

    total_violations = 0
    for (pname,) in pages:
        _, root = get_page(mxfile, pname)
        if root is None:
            print(f"  [{pname}] page not found", file=sys.stderr)
            total_violations += 1
            continue

        overlaps = check_edge_on_edge_overlaps(root)
        if not overlaps:
            print(f"[PASS] {pname}: no edges overlap other edges")
            continue

        total_violations += len(overlaps)
        print(f"[FAIL] {pname}: {len(overlaps)} edge_on_edge_overlap violation(s)")
        for desc_a, desc_b, detail in overlaps:
            print(f"  - {desc_a} overlaps {desc_b}: {detail}")

    return 0 if total_violations == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Path to .drawio file")
    parser.add_argument("--page", default=None, help="Optional page name to limit scan")
    args = parser.parse_args()

    sys.exit(scan(args.file, args.page))


if __name__ == "__main__":
    main()
