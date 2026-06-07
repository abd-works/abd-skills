#!/usr/bin/env python3
"""Scanner: slash terms (A / B) must be resolved before domain model.

Any concept named A / B in the Domain Language must be resolved to one
canonical name before writing domain-model blocks.  This scanner finds
### **A / B** heading lines and flags them, and also checks property names
and method names for slash notation.
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

_SLASH_HEADING_RE = re.compile(r"^#{2,6}\s+\*\*[^*]+\s*/\s*[^*]+\*\*")
_CLASS_HEADER_RE = re.compile(r"^### \*\*[^*]+\*\*")
_PROPERTY_RE = re.compile(r"^(\w[\w\s]*/\s*\w[\w\s]*):")
_METHOD_SLASH_RE = re.compile(r"^(\w[\w\s]*/\s*\w[\w\s]*)\(")
_PRIVATE_METHOD_SLASH_RE = re.compile(r"^-\s+(\w[\w\s]*/\s*\w[\w\s]*)\(")


class SlashTermsResolvedScanner(Scanner):
    """Flag A/B slash notation in headings, property names, and method names."""

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

        for i, line in enumerate(lines):
            stripped = line.strip()

            if _SLASH_HEADING_RE.match(stripped):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Heading '{stripped}' uses slash notation — "
                        f"resolve to one canonical name before domain model"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            if _PROPERTY_RE.match(stripped):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Property name uses slash notation: '{stripped[:60]}' — "
                        f"use one canonical name"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            m = _METHOD_SLASH_RE.match(stripped) or _PRIVATE_METHOD_SLASH_RE.match(stripped)
            if m:
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Method name uses slash notation: '{m.group(1).strip()}' — "
                        f"use one canonical name"
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
            SlashTermsResolvedScanner,
            rule_md_name="slash-terms-resolved-before-model",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
