"""One-shot helper to strip a .drawio multi-page file down to selected page names.

Used only to build the initial fixture set under eval/fail/ and eval/pass/. Keep around
for reproducibility when future fixtures are promoted from new runs.

Usage:
    python extract_pages.py <source.drawio> <dest.drawio> <page-name> [<page-name>...]

Page name matches the `name` attribute of <diagram>. Whole-file copy if no
page names are given.
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def extract(src: Path, dest: Path, pages: list[str]) -> None:
    tree = ET.parse(src)
    root = tree.getroot()
    if pages:
        keep = set(pages)
        for diagram in list(root.findall("diagram")):
            if diagram.get("name") not in keep:
                root.remove(diagram)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tree.write(dest, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    pages = sys.argv[3:]
    extract(src, dest, pages)
    print(f"wrote {dest} ({len(pages) or 'all'} page(s))")
