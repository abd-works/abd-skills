"""Shared workspace discovery for abd-object-model scanners."""
from __future__ import annotations

from pathlib import Path
from typing import List

from scanner_bases.resources.scan_context import FileCollection, ScanFilesContext


def build_object_model_context(
    workspace: Path,
    story_graph: Path | None = None,
) -> ScanFilesContext:
    """Collect object-model markdown files under common engagement layouts."""
    del story_graph  # reserved for future graph-aware scans
    files: List[Path] = []

    direct = workspace / "docs" / "domain" / "object-model.md"
    if direct.is_file():
        text = direct.read_text(encoding="utf-8")
        if "state: domain-model" in text[:300]:
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
                if "state: domain-model" in text[:300]:
                    files.append(md)
            if files:
                break

    return ScanFilesContext(files=FileCollection(code_files=files))
