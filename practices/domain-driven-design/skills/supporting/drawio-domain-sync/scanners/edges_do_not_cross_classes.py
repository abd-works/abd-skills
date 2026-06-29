#!/usr/bin/env python3
"""
Scanner: edges_do_not_cross_classes

Verifies that no edge's routed segments pass through a class it is not
connected to. Reuses ``check_edges_crossing_classes`` from drawio_tools.

Usage:
  python edges_do_not_cross_classes.py <file.drawio> [--page PAGE]

Exit codes:
  0  no violations found
  1  one or more crossings detected (or file error)
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
    check_edges_crossing_classes,
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

        crossings = check_edges_crossing_classes(root)
        # We report only definitive (non-approx) crossings as failures.
        definitive = [(edge, cls) for edge, cls in crossings if "(approx)" not in edge]

        if not definitive:
            print(f"[PASS] {pname}: no edges cross non-endpoint classes")
            continue

        total_violations += len(definitive)
        print(f"[FAIL] {pname}: {len(definitive)} edge_crosses_class violation(s)")
        for edge, cls in definitive:
            print(f"  - {edge} crosses {cls}")

    return 0 if total_violations == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Path to .drawio file")
    parser.add_argument("--page", default=None, help="Optional page name to limit scan")
    args = parser.parse_args()

    sys.exit(scan(args.file, args.page))


if __name__ == "__main__":
    main()
