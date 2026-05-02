#!/usr/bin/env python3
"""Scanner: Extract: partial must have Part: line; Extract: whole must not."""
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


class PartialExtractsHavePartLineScanner(ModuleFileScanner):
    rule = "partial-extracts-have-part-line"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        for term in parsed.terms:
            for ref in term.refs:
                if ref.extract_type == "partial" and ref.part is None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' is "
                        f"Extract: partial but has no Part: line",
                        fname,
                        ref.line_number,
                    ))
                elif ref.extract_type == "whole" and ref.part is not None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' is "
                        f"Extract: whole but has a Part: line (contradicts "
                        f"'whole')",
                        fname,
                        ref.line_number,
                    ))
        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            PartialExtractsHavePartLineScanner,
            rule_md_name="partial-extracts-have-part-line",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
