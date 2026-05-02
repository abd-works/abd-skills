#!/usr/bin/env python3
"""Scanner: front matter must contain state: key-abstractions."""
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
from markdown_artifact_scanner import (  # noqa: E402
    ModuleFileScanner,
    ParsedModuleFile,
)
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)


def _build_context_all_modules(workspace: Path) -> ScanFilesContext:
    """Check all module .md files, not just those already at key-abstractions."""
    modules_path = workspace / "abd-domain-driven-design" / "modules"
    files: List[Path] = []
    if modules_path.is_dir():
        for md in modules_path.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            if "state:" in text[:200]:
                files.append(md)
    return ScanFilesContext(files=FileCollection(code_files=files))


class StateMarkerScanner(ModuleFileScanner):
    rule = "state-marker-correct"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        if parsed.state is None:
            violations.append(self._violation(
                "No state: marker found in front matter",
                fname,
                1,
            ))
        elif parsed.state != "key-abstractions":
            violations.append(self._violation(
                f"State marker is '{parsed.state}', expected 'key-abstractions'",
                fname,
                1,
            ))
        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            StateMarkerScanner,
            rule_md_name="state-marker-correct",
            build_context=_build_context_all_modules,
            skill_root=_ROOT,
        )
    )
