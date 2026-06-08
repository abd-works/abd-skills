#!/usr/bin/env python3
"""Scanner: every Source: line in module files must resolve to a file on disk."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

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

GENERATED_SOURCE_MARKERS = [
    "domain-knowledge",
    "domain knowledge",
    "application-requirements",
    "application requirements",
    "training data",
    "from memory",
    "user requirements",
    "agent knowledge",
    "reconstructed",
]

_REF_HEADER_RE = re.compile(
    r"^\*\*(?:Ref|Extract)\s*\u2014\s*(?P<title>.+?)\*\*\s*$", re.MULTILINE
)
_SOURCE_LINE_RE = re.compile(
    r"^Source:\s*(?P<ref>.+)$", re.MULTILINE
)


def _find_context_dirs(workspace: Path) -> List[Path]:
    candidates = []
    for name in ("context", "context/rules", "corpus", "source", "data"):
        d = workspace / name
        if d.is_dir():
            candidates.append(d)
    return candidates


def _has_source_files(workspace: Path) -> bool:
    for d in _find_context_dirs(workspace):
        for f in d.rglob("*"):
            if f.is_file():
                return True
    return False


def _resolve_source_ref(ref: str, workspace: Path) -> Path | None:
    clean = ref.split("\u2014")[0].strip().strip('"').strip("'")
    candidate = workspace / clean
    if candidate.is_file():
        return candidate
    for d in _find_context_dirs(workspace):
        candidate = d / clean
        if candidate.is_file():
            return candidate
    return None


class VerbatimSourceOnlyScanner(Scanner):
    """Flag references whose Source: line cannot be traced to a file on disk."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        for fp in all_files:
            if fp and fp.exists() and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        content = file_path.read_text(encoding="utf-8")

        modules_dir = file_path.parent
        if modules_dir.name == "modules":
            workspace = modules_dir.parent.parent
        else:
            workspace = file_path.parent.parent

        refs = list(_REF_HEADER_RE.finditer(content))
        if not refs:
            return violations

        if not _has_source_files(workspace):
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=(
                        f"{file_path.name} has {len(refs)} reference(s) "
                        f"but no source files found under workspace. "
                        f"Every reference must trace to a file on disk."
                    ),
                    location=str(file_path),
                    severity="error",
                ).to_dict()
            )

        for match in refs:
            title = match.group("title").strip()
            start = match.end()
            next_ref = _REF_HEADER_RE.search(content, start)
            end = next_ref.start() if next_ref else len(content)
            block = content[start:end]
            line_number = content[:match.start()].count("\n") + 1

            source_match = _SOURCE_LINE_RE.search(block)
            if not source_match:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Ref "{title}": missing Source: line in header.'
                        ),
                        line_number=line_number,
                        location=str(file_path),
                        severity="error",
                    ).to_dict()
                )
                continue

            source_ref = source_match.group("ref").strip()
            source_ref_lower = source_ref.lower()

            for marker in GENERATED_SOURCE_MARKERS:
                if marker in source_ref_lower:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Ref "{title}": Source line contains '
                                f'generated-content marker "{marker}" \u2014 '
                                f'"{source_ref}". '
                                f"References must point to a file on disk."
                            ),
                            line_number=line_number,
                            location=str(file_path),
                            severity="error",
                        ).to_dict()
                    )
                    break
            else:
                resolved = _resolve_source_ref(source_ref, workspace)
                if resolved is None:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Ref "{title}": Source reference '
                                f'"{source_ref}" could not be resolved to a '
                                f"file on disk under the workspace."
                            ),
                            line_number=line_number,
                            location=str(file_path),
                            severity="warning",
                        ).to_dict()
                    )

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    modules_dir = workspace / "domain" / "modules"
    files: List[Path] = []
    if modules_dir.is_dir():
        for f in sorted(modules_dir.glob("*.md")):
            if f.is_file():
                files.append(f)
    mp = workspace / "domain" / "module-partition.md"
    if mp.is_file():
        files.append(mp)
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            VerbatimSourceOnlyScanner,
            rule_md_name="verbatim-source-only",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
