#!/usr/bin/env python3
"""Scanner: source blocks must trace to disk files, not agent memory."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute_using_rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from markdown_artifact_scanner import (  # noqa: E402
    MarkdownArtifactScanner,
    ParsedArtifact,
    ParsedKeyAbstraction,
    ParsedExtract,
    build_ka_context,
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


class VerbatimSourceBlocksScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")
        workspace = parsed.file_path.parent.parent if parsed.file_path else None

        for ka in self._all_kas(parsed):
            for ext in ka.extracts:
                if not ext.source_ref:
                    continue
                ref_lower = ext.source_ref.lower()
                for marker in GENERATED_SOURCE_MARKERS:
                    if marker in ref_lower:
                        violations.append(self._violation(
                            f'Key Abstraction "{ka.name}", extract "{ext.title}": '
                            f'Source line contains generated-content marker "{marker}" — '
                            f'"{ext.source_ref}". Extracts must reference a file on disk.',
                            location, ext.line_number,
                        ))
                        break
                else:
                    if workspace and not self._can_resolve(ext.source_ref, workspace):
                        violations.append(self._violation(
                            f'Key Abstraction "{ka.name}", extract "{ext.title}": '
                            f'Source reference "{ext.source_ref}" could not be resolved '
                            f'to a file on disk under the workspace.',
                            location, ext.line_number, severity="warning",
                        ))

        return violations

    def _can_resolve(self, ref: str, workspace: Path) -> bool:
        """Check if a Source: reference resolves to a file or known partition."""
        clean = ref.split("—")[0].strip().strip('"').strip("'")

        if "module-partitioning.md" in clean.lower():
            mp = workspace / "abd-ooad" / "module-partitioning.md"
            return mp.is_file()

        candidate = workspace / clean
        if candidate.is_file():
            return True

        for subdir in ("context", "corpus", "source", "data"):
            d = workspace / subdir
            if d.is_dir():
                c = d / clean
                if c.is_file():
                    return True

        parts = clean.replace("\\", "/").split("/")
        filename = parts[-1] if parts else clean
        for subdir in ("context", "corpus", "source", "data"):
            d = workspace / subdir
            if d.is_dir():
                for f in d.rglob("*"):
                    if f.is_file() and f.name.lower() == filename.lower():
                        return True

        return False

    @staticmethod
    def _all_kas(parsed: ParsedArtifact) -> List[ParsedKeyAbstraction]:
        kas: List[ParsedKeyAbstraction] = []
        if parsed.has_modules:
            for mod in parsed.modules:
                kas.extend(mod.key_abstractions)
        else:
            kas.extend(parsed.flat_abstractions)
        return kas


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            VerbatimSourceBlocksScanner,
            rule_md_name="verbatim-source-blocks",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
