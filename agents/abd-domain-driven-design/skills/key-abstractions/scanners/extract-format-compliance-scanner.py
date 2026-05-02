#!/usr/bin/env python3
"""Scanner: every **Ref —** must have Source:, Locator:, and Extract: whole|partial."""
from __future__ import annotations

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
from markdown_artifact_scanner import (  # noqa: E402
    ModuleFileScanner,
    ParsedModuleFile,
    build_module_context,
)


class ExtractFormatComplianceScanner(ModuleFileScanner):
    rule = "extract-format-compliance"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        for term in parsed.terms:
            for ref in term.refs:
                if ref.source_ref is None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' missing "
                        f"Source: line",
                        fname,
                        ref.line_number,
                    ))
                if ref.locator is None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' missing "
                        f"Locator: line",
                        fname,
                        ref.line_number,
                    ))
                if ref.extract_type is None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' missing "
                        f"Extract: line",
                        fname,
                        ref.line_number,
                    ))
                elif ref.extract_type not in ("whole", "partial"):
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' has invalid "
                        f"Extract: '{ref.extract_type}' — must be 'whole' or "
                        f"'partial'",
                        fname,
                        ref.line_number,
                    ))
        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ExtractFormatComplianceScanner,
            rule_md_name="extract-format-compliance",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
