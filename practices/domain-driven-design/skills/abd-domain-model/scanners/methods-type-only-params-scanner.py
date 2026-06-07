#!/usr/bin/env python3
"""Scanner: method and constructor signatures must use types only, not param: Type.

Domain-model format requires type-only parameter lists — e.g. method(Type, Type),
not method(param: Type, param: Type).  This scanner flags any line with parentheses
whose content contains word-colon-word notation inside the parens.
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
_SIGNATURE_RE = re.compile(r"^[-]?\s*\w+\s*\(([^)]*)\)")
_CTOR_RE = re.compile(r"^[A-Z]\w+\(([^)]*)\)")
_PARAM_NAME_TYPE_RE = re.compile(r"\b\w+\s*:\s*\w+")
_INVARIANT_RE = re.compile(r"^\t?Invariant:", re.IGNORECASE)


class MethodsTypeOnlyParamsScanner(Scanner):
    """Flag method/constructor signatures that use param: Type instead of Type only."""

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

        for i, line in enumerate(lines):
            stripped = line.strip()

            if _CLASS_HEADER_RE.match(stripped):
                in_class_block = True
                continue

            if not in_class_block:
                continue

            if _INVARIANT_RE.match(stripped):
                continue

            sig_m = _SIGNATURE_RE.match(stripped) or _CTOR_RE.match(stripped)
            if not sig_m:
                continue

            params_text = sig_m.group(1).strip()
            if not params_text:
                continue

            if _PARAM_NAME_TYPE_RE.search(params_text):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Signature '{stripped[:60]}' uses param: Type notation — "
                        f"use type-only params (e.g. method(Type, Type))"
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
            MethodsTypeOnlyParamsScanner,
            rule_md_name="methods-use-type-only-params",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
