#!/usr/bin/env python3
"""Scanner: every core term from the Core terms list must appear as a #### heading
under exactly one ### KA inside ## Key Abstractions, OR as a ### heading under
## Boundary terms, OR in the **Moved to other modules** list with a valid
destination. No drops, no duplicates, no vanishing terms."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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

CORE_TERMS_BULLET_RE = re.compile(r"^- (.+)$", re.MULTILINE)
CORE_TERMS_BLOCK_RE = re.compile(
    r"\*\*Core terms\*\*:\s*\n((?:- .+\n?)+)", re.MULTILINE
)
MOVED_BLOCK_RE = re.compile(
    r"\*\*Moved to other modules\*\*:\s*\n((?:- .+\n?)+)", re.MULTILINE
)
MOVED_ENTRY_RE = re.compile(r"^- (.+?)\s*→\s*(.+)$", re.MULTILINE)


def _find_module_dir(file_path: Path) -> Optional[Path]:
    """Walk up from file_path to find the modules directory."""
    candidate = file_path.parent
    if candidate.name == "modules":
        return candidate
    return None


def _destination_has_term(modules_dir: Path, dest_module: str, term: str) -> bool:
    """Check if destination module's Core terms list contains the term."""
    slug = dest_module.strip().lower().replace(" ", "-")
    for md in modules_dir.glob("*.md"):
        if md.stem.lower() == slug:
            text = md.read_text(encoding="utf-8")
            block_m = CORE_TERMS_BLOCK_RE.search(text)
            if block_m:
                for bullet in CORE_TERMS_BULLET_RE.finditer(block_m.group(1)):
                    if bullet.group(1).strip().lower() == term.lower():
                        return True
            return False
    return False


class EveryTermUnderOneKaScanner(ModuleFileScanner):
    rule = "every-term-under-one-ka"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        block_m = CORE_TERMS_BLOCK_RE.search(parsed.content)
        if not block_m:
            return violations

        expected_terms = set()
        for bullet in CORE_TERMS_BULLET_RE.finditer(block_m.group(1)):
            expected_terms.add(bullet.group(1).strip())

        if not expected_terms:
            return violations

        # Collect moved terms and their destinations
        moved_terms: Dict[str, str] = {}
        moved_m = MOVED_BLOCK_RE.search(parsed.content)
        if moved_m:
            for entry in MOVED_ENTRY_RE.finditer(moved_m.group(1)):
                moved_terms[entry.group(1).strip()] = entry.group(2).strip()

        # Collect KA terms and boundary terms from parsed structure
        core_term_names: List[str] = []
        boundary_term_names: set[str] = set()
        for term in parsed.terms:
            if term.is_boundary:
                boundary_term_names.add(term.name)
            else:
                core_term_names.append(term.name)

        found_terms = set(core_term_names)

        # Check every expected term is accounted for
        for expected in expected_terms:
            if expected not in found_terms and expected not in boundary_term_names:
                violations.append(self._violation(
                    f"Core term '{expected}' from the bullet list is missing "
                    f"as a #### heading under ## Key Abstractions or "
                    f"as a ### heading under ## Boundary terms",
                    fname,
                    1,
                ))

        # Check no duplicates in KA terms
        seen = set()
        for name in core_term_names:
            if name in seen:
                violations.append(self._violation(
                    f"Core term '{name}' appears under multiple KA sections",
                    fname,
                    1,
                ))
            seen.add(name)

        # Verify moved terms actually landed in destination modules
        if moved_terms and parsed.file_path:
            modules_dir = _find_module_dir(parsed.file_path)
            if modules_dir:
                for term_name, dest in moved_terms.items():
                    if not _destination_has_term(modules_dir, dest, term_name):
                        violations.append(self._violation(
                            f"Moved term '{term_name}' → {dest}: "
                            f"not found in {dest}'s Core terms list",
                            fname,
                            1,
                        ))

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            EveryTermUnderOneKaScanner,
            rule_md_name="every-term-under-one-ka",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
