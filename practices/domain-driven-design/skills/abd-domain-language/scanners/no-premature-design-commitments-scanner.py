#!/usr/bin/env python3
"""Scanner: domain-language files must not contain premature design commitments.

Flags:
  - DDD stereotypes: <<Entity>>, <<ValueObject>>, <<Aggregate>>, etc.
  - Cardinality notation: 1..1, 0..*, 1..*, etc.
  - Operation signatures in concept bullets: word(param: Type) or word(): Type
  - Shape hint: labels
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_REPO = _ROOT.parent.parent.parent.parent
for _p in (
    _REPO / "skills" / "execute-skill-using-skills-rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from scanner_bases import Scanner, Violation  # noqa: E402
from scanner_bases.resources.scan_context import FileCollection, ScanFilesContext  # noqa: E402

_ANY_STEREOTYPE_RE = re.compile(r"<<\s*\w[\w\s]*\s*>>")
_CARDINALITY_RE = re.compile(r"\b\d\.\.[*\d]\b")
_OP_SIGNATURE_RE = re.compile(r"\b[a-z]\w*\s*\(\s*\w+\s*:\s*\w+")
_SHAPE_HINT_RE = re.compile(r"^\s*Shape hint\s*:", re.IGNORECASE)
_SKIP_SECTION_RE = re.compile(
    r"^(?:# Boundary Domain|### References|## References)",
    re.IGNORECASE,
)


class NoPrematureDesignCommitmentsScanner(Scanner):
    """Flag DDD stereotypes, cardinality notation, and operation signatures."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        in_skip = False

        for i, line in enumerate(lines):
            if _SKIP_SECTION_RE.match(line):
                in_skip = True
            elif re.match(r"^#{1,2}\s", line) and not _SKIP_SECTION_RE.match(line):
                in_skip = False

            if in_skip:
                continue

            if _SHAPE_HINT_RE.match(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message="'Shape hint:' label found — use '### Decisions made' instead",
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            if _ANY_STEREOTYPE_RE.search(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"DDD stereotype found: '{_ANY_STEREOTYPE_RE.search(line).group()}' — "
                        "remove from Domain Language (belongs at domain-specification stage)"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())

            if _CARDINALITY_RE.search(line) and not line.strip().startswith("#"):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Cardinality notation found: '{_CARDINALITY_RE.search(line).group()}' — "
                        "use plain-English bullets, not UML cardinality"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())

            if line.strip().startswith("- ") and _OP_SIGNATURE_RE.search(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Operation signature in concept bullet: '{line.strip()[:80]}' — "
                        "use plain-English behavior descriptions"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    for search_path in (workspace / "modules", workspace):
        if search_path.is_dir():
            for md in sorted(search_path.glob("*domain-language.md")):
                text = md.read_text(encoding="utf-8")
                if "state: domain-language" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            NoPrematureDesignCommitmentsScanner,
            rule_md_name="no-premature-design-commitments",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
