#!/usr/bin/env python3
"""Scanner: source blocks must trace to real files on disk, not generated content."""
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

GENERATED_MARKERS = [
    "domain-knowledge",
    "from memory",
    "reconstructed",
    "agent knowledge",
    "training data",
    "application-requirements",
]


class VerbatimSourceBlocksScanner(ModuleFileScanner):
    rule = "verbatim-source-blocks"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        for term in parsed.terms:
            for ref in term.refs:
                if ref.source_ref is None:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' has no "
                        f"Source: line",
                        fname,
                        ref.line_number,
                    ))
                    continue

                src_lower = ref.source_ref.lower()
                for marker in GENERATED_MARKERS:
                    if marker in src_lower:
                        violations.append(self._violation(
                            f"Ref '{ref.title}' under term '{term.name}' uses "
                            f"generated-content marker '{marker}' in Source: line",
                            fname,
                            ref.line_number,
                        ))
                        break

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            VerbatimSourceBlocksScanner,
            rule_md_name="verbatim-source-blocks",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
