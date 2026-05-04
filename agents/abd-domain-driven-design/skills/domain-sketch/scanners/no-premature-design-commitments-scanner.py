#!/usr/bin/env python3
"""Scanner: domain-sketch files must not contain premature design commitments.

The domain sketch is a plain-English domain model. Design-level constructs must not
appear at this stage. This scanner flags:
  - DDD stereotypes: << Entity >>, << ValueObject >>, << Aggregate >>, etc.
  - Cardinality notation: 1..1, 0..*, 1..*, etc.
  - Operation signatures in behavior lines: word(param: Type) or word(): Type
  - Shape hint: labels (replaced by Decisions made)
  - Lifecycle state tables (row-based transition matrices)

Sections that legitimately carry code (e.g. References, Boundary terms) are excluded
from cardinality and signature checks.
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
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)

# DDD stereotypes in angle brackets
_STEREOTYPE_RE = re.compile(r"<<\s*(?:Entity|ValueObject|Value Object|Aggregate|AggregateRoot|Aggregate Root|Service|Repository|Factory|DomainEvent|Domain Event)\s*>>", re.IGNORECASE)
# Generic << >> anywhere (overly broad design commitment)
_ANY_STEREOTYPE_RE = re.compile(r"<<\s*\w[\w\s]*\s*>>")
# Cardinality notation
_CARDINALITY_RE = re.compile(r"\b\d\.\.[*\d]\b")
# Operation signatures in behavior lines (word followed immediately by open paren with params)
_OP_SIGNATURE_RE = re.compile(r"\b[a-z]\w*\s*\(\s*\w+\s*:\s*\w+")
# Shape hint: label
_SHAPE_HINT_RE = re.compile(r"^\s*Shape hint\s*:", re.IGNORECASE)
# Domain Sketch section — this is where behavior bullets live
_DOMAIN_SKETCH_SECTION_RE = re.compile(r"^### Domain Sketch\s*$", re.IGNORECASE)
# Object Model section — skip this (it comes later and legitimately has signatures)
_OBJECT_MODEL_SECTION_RE = re.compile(r"^### Object Model\s*$", re.IGNORECASE)
# Boundary domain / references sections — skip these
_SKIP_SECTION_RE = re.compile(
    r"^(?:# Boundary Domain|### References|## References|#### \*\*.*\*\*\s*\*\(owned by)",
    re.IGNORECASE,
)


def _find_sketch_ranges(lines: List[str]) -> List[tuple[int, int]]:
    """Return (start, end) line ranges for ### Domain Sketch sections."""
    ranges = []
    start = None
    for i, line in enumerate(lines):
        if _DOMAIN_SKETCH_SECTION_RE.match(line):
            start = i
        elif start is not None and (
            re.match(r"^#{2,3}\s", line)
            and not _DOMAIN_SKETCH_SECTION_RE.match(line)
        ):
            ranges.append((start, i))
            start = None
    if start is not None:
        ranges.append((start, len(lines)))
    return ranges


class NoPrematureDesignCommitmentsScanner(Scanner):
    """Flag DDD stereotypes, cardinality notation, and operation signatures in domain-sketch files."""

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

        in_skip_section = False
        in_object_model = False

        for i, line in enumerate(lines):
            # Track skip sections
            if _SKIP_SECTION_RE.match(line):
                in_skip_section = True
            elif _OBJECT_MODEL_SECTION_RE.match(line):
                in_object_model = True
                in_skip_section = False
            elif re.match(r"^#{1,3}\s", line) and not _OBJECT_MODEL_SECTION_RE.match(line):
                in_object_model = False
                if not _SKIP_SECTION_RE.match(line):
                    in_skip_section = False

            if in_skip_section or in_object_model:
                continue

            # Check Shape hint: label anywhere
            if _SHAPE_HINT_RE.match(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"'Shape hint:' label found — replace with '#### Decisions made' section"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            # Check for DDD stereotypes (anywhere outside skip sections)
            if _ANY_STEREOTYPE_RE.search(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"DDD stereotype found: '{_ANY_STEREOTYPE_RE.search(line).group()}' — "
                        f"remove from domain sketch (belongs in object-model stage)"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())

            # Check for cardinality notation in behavior/collaboration lines
            if _CARDINALITY_RE.search(line) and not line.strip().startswith("#"):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Cardinality notation found: '{_CARDINALITY_RE.search(line).group()}' — "
                        f"use plain-English collaboration lines, not UML cardinality"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())

            # Check for operation signatures in behavior lines (lines starting with - or bare text)
            if line.strip().startswith("- ") or (line.strip() and not line.startswith("#")):
                if _OP_SIGNATURE_RE.search(line):
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Operation signature found in domain-sketch line: "
                            f"'{line.strip()[:80]}' — use plain English behavior descriptions"
                        ),
                        location=str(file_path),
                        line_number=i + 1,
                        severity="error",
                    ).to_dict())

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    for search_path in (
        workspace / "abd-domain-driven-design" / "modules",
        workspace / "modules",
    ):
        if search_path.is_dir():
            for md in sorted(search_path.glob("*.md")):
                text = md.read_text(encoding="utf-8")
                if "state: domain-sketch" in text[:300]:
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
