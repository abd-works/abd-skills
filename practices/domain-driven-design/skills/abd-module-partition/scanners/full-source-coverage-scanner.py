#!/usr/bin/env python3
"""Scanner: every source file in the workspace must be referenced across module files."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute-skill-using-skills-rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from scanner_bases import Scanner, Violation  # noqa: E402
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)

_SOURCE_DIRS = ("context", "corpus", "source", "data")

_REF_HEADER_RE = re.compile(
    r"^\*\*(?:Ref|Extract)\s*—\s*(?P<title>.+?)\*\*\s*$", re.MULTILINE
)
_SOURCE_LINE_RE = re.compile(
    r"^Source:\s*(?P<ref>.+)$", re.MULTILINE
)


def _collect_source_files(workspace: Path) -> List[Path]:
    files: List[Path] = []
    for name in _SOURCE_DIRS:
        d = workspace / name
        if d.is_dir():
            for f in sorted(d.rglob("*")):
                if f.is_file():
                    files.append(f)
    return files


def _collect_all_references(module_files: List[Path], workspace: Path) -> Set[str]:
    """Collect all Source: references across all module files."""
    refs: Set[str] = set()
    for fp in module_files:
        if not fp.exists():
            continue
        content = fp.read_text(encoding="utf-8")
        for match in _REF_HEADER_RE.finditer(content):
            start = match.end()
            next_ref = _REF_HEADER_RE.search(content, start)
            end = next_ref.start() if next_ref else len(content)
            block = content[start:end]

            source_match = _SOURCE_LINE_RE.search(block)
            if not source_match:
                continue

            raw_ref = source_match.group("ref").strip()
            clean = raw_ref.split("—")[0].strip().strip('"').strip("'")
            normalised = clean.replace("\\", "/").lower()

            refs.add(normalised)
            parts = normalised.split("/")
            if len(parts) > 1:
                refs.add("/".join(parts[1:]))
                refs.add(parts[-1])
            refs.add(parts[-1])

    return refs


def _file_is_referenced(source_file: Path, workspace: Path, refs: Set[str]) -> bool:
    try:
        rel = source_file.relative_to(workspace)
    except ValueError:
        rel = Path(source_file.name)

    rel_posix = str(rel).replace("\\", "/").lower()

    if rel_posix in refs:
        return True

    parts = rel_posix.split("/")
    if len(parts) > 1 and "/".join(parts[1:]) in refs:
        return True

    filename = parts[-1]
    if filename in refs:
        return True

    stem = source_file.stem.lower()
    for ref in refs:
        if stem in ref:
            return True

    return False


class FullSourceCoverageScanner(Scanner):
    """Flag source files not referenced by any module file."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        if not all_files:
            return violations

        first_file = all_files[0]
        modules_dir = first_file.parent
        if modules_dir.name == "modules":
            workspace = modules_dir.parent.parent
        else:
            workspace = first_file.parent.parent

        source_files = _collect_source_files(workspace)
        if not source_files:
            return violations

        refs = _collect_all_references(all_files, workspace)

        unreferenced: List[Path] = []
        for sf in source_files:
            if not _file_is_referenced(sf, workspace, refs):
                unreferenced.append(sf)

        location = str(workspace / "abd-domain-driven-design" / "modules")
        if unreferenced:
            for sf in unreferenced:
                try:
                    rel = sf.relative_to(workspace)
                except ValueError:
                    rel = sf
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Source file not referenced in any module file: "
                            f"{rel}. Every source file must appear in at "
                            f"least one module, unallocated.md, or rejected.md."
                        ),
                        location=location,
                        severity="error",
                    ).to_dict()
                )

            total = len(source_files)
            covered = total - len(unreferenced)
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Source coverage: {covered}/{total} files referenced "
                        f"({len(unreferenced)} missing). The partition must "
                        f"account for every source file."
                    ),
                    location=location,
                    severity="error",
                ).to_dict()
            )

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    modules_dir = workspace / "abd-domain-driven-design" / "modules"
    files: List[Path] = []
    if modules_dir.is_dir():
        for f in sorted(modules_dir.glob("*.md")):
            if f.is_file():
                files.append(f)
    mp = workspace / "abd-domain-driven-design" / "module-partition.md"
    if mp.is_file():
        files.append(mp)
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            FullSourceCoverageScanner,
            rule_md_name="full-source-coverage",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
