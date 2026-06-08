#!/usr/bin/env python3
"""Scanner: no property, parameter, or return type may use raw String.

Domain models should use domain-specific value types instead of raw String.
This scanner checks property lines, method signatures (params and return),
and constructor lines for the raw String type.  Prose text, invariants, and
decision sections are excluded.
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

_CLASS_HEADER_RE = re.compile(r"^### \*\*[^*]+\*\*")
_PROPERTY_STRING_RE = re.compile(r"^\w+\s*:\s*String\s*$")
_METHOD_RE = re.compile(r"^[-]?\s*\w+\s*\(([^)]*)\)\s*(?::\s*(\S+))?")
_CTOR_RE = re.compile(r"^[A-Z]\w+\(([^)]*)\)")
_INVARIANT_RE = re.compile(r"^\t?Invariant:", re.IGNORECASE)
_DECISION_HEADER_RE = re.compile(r"^##?\s+Decision", re.IGNORECASE)

_STRING_TOKEN_RE = re.compile(r"\bString\b")


class NoRawStringScanner(Scanner):
    """Flag any property, parameter, or return typed as raw String."""

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

        in_class_block = False
        in_decisions = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if _DECISION_HEADER_RE.match(stripped):
                in_decisions = True
                continue
            if in_decisions:
                if re.match(r"^#{1,3}\s", stripped) and not _DECISION_HEADER_RE.match(stripped):
                    in_decisions = False
                else:
                    continue

            if _CLASS_HEADER_RE.match(stripped):
                in_class_block = True
                continue

            if not in_class_block:
                continue

            if _INVARIANT_RE.match(stripped):
                continue
            if stripped.startswith("\t") and not stripped.lstrip("\t").startswith(("-", "+")):
                if _INVARIANT_RE.match(stripped):
                    continue

            if _PROPERTY_STRING_RE.match(stripped):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Property '{stripped}' uses raw String — "
                        f"use a domain-specific value type"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            ctor_m = _CTOR_RE.match(stripped)
            if ctor_m:
                params = ctor_m.group(1)
                if _STRING_TOKEN_RE.search(params):
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Constructor '{stripped[:60]}' has raw String parameter — "
                            f"use a domain-specific value type"
                        ),
                        location=str(file_path),
                        line_number=i + 1,
                        severity="error",
                    ).to_dict())
                continue

            method_m = _METHOD_RE.match(stripped)
            if method_m:
                params = method_m.group(1) or ""
                ret = method_m.group(2) or ""
                reasons: List[str] = []
                if _STRING_TOKEN_RE.search(params):
                    reasons.append("parameter")
                if _STRING_TOKEN_RE.search(ret):
                    reasons.append("return type")
                if reasons:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Method '{stripped[:60]}' has raw String as {' and '.join(reasons)} — "
                            f"use a domain-specific value type"
                        ),
                        location=str(file_path),
                        line_number=i + 1,
                        severity="error",
                    ).to_dict())

        return violations


from domain_model_context import build_domain_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            NoRawStringScanner,
            rule_md_name="no-raw-string-types",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
