"""Shared workspace discovery and section helpers for abd-domain-specification scanners."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Set

from scanner_bases.resources.scan_context import FileCollection, ScanFilesContext

_META_SECTION_RE = re.compile(r"^### (references|decisions made)\s*$")
_KA_SECTION_RE = re.compile(r"^## \*\*")
_CLASS_HEADING_RE = re.compile(r"^### \*\*.+\*\*.*<<")


def build_object_model_context(
    workspace: Path,
    story_graph: Path | None = None,
) -> ScanFilesContext:
    """Collect domain-specification markdown files under common engagement layouts."""
    del story_graph  # reserved for future graph-aware scans
    files: List[Path] = []

    direct = workspace / "docs" / "domain" / "domain-specification.md"
    if direct.is_file():
        text = direct.read_text(encoding="utf-8")
        if "state: domain-specification" in text[:300]:
            files.append(direct)

    if not files:
        for search_path in (
            workspace / "abd-domain-driven-design" / "modules",
            workspace / "modules",
            workspace / "docs" / "domain",
        ):
            if not search_path.is_dir():
                continue
            for md in sorted(search_path.glob("*.md")):
                text = md.read_text(encoding="utf-8")
                if "state: domain-specification" in text[:300]:
                    files.append(md)
            if files:
                break

    return ScanFilesContext(files=FileCollection(code_files=files))


def domain_spec_scannable_line_indices(lines: List[str]) -> Set[int]:
    """Line indices inside domain-specification class blocks (excludes meta sections)."""
    indices: Set[int] = set()
    in_meta = False
    for i, line in enumerate(lines):
        if _META_SECTION_RE.match(line):
            in_meta = True
            continue
        if _KA_SECTION_RE.match(line):
            in_meta = False
            continue
        if _CLASS_HEADING_RE.match(line):
            in_meta = False
        if in_meta:
            continue
        if line.strip().startswith("---") and i < 5:
            continue
        indices.add(i)
    return indices
