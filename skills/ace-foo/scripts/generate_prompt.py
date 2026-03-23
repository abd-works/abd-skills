#!/usr/bin/env python3
"""Emit instruction text for a phase slug (minimal ace-foo implementation).

Reads ``content/parts/phases/<slug>.md``. See ``content/parts/library/process-approach.md``
in **abd-skill-builder** for the full contract used by production skills.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "content" / "parts" / "phases"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Print phase markdown for --phase <slug>.")
    p.add_argument("--phase", required=True, dest="slug", help="Phase slug (filename without .md).")
    p.add_argument(
        "--mode",
        choices=("static", "dynamic"),
        default="dynamic",
        help="Ignored in this minimal skill; reserved for parity with generate_prompt contract.",
    )
    ns = p.parse_args()
    path = PHASE_DIR / f"{ns.slug}.md"
    if not path.is_file():
        print(f"Phase not found: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
