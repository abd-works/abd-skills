#!/usr/bin/env python3
"""Scanner: assumptions-explicit-with-confidence.

Checks every cost-of-delay canvas in --workspace for:
  1. An assumptions table with Factor, Unit, Confidence columns
  2. Every Confidence cell is Strong / Reasonable / Uncertain
  3. A CoD formula line is present
  4. No bare CoD result without a formula
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_EXECUTE_RULES_SCRIPTS = _SKILL_ROOT.parent / "execute_using_rules" / "scripts"
if str(_EXECUTE_RULES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_EXECUTE_RULES_SCRIPTS))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from scanner_bases import Scanner, Violation, SimpleRule, ScanFilesContext, FileCollection  # noqa: E402
from scanner_runner import execute_scan_with_workspace  # noqa: E402
from md_tables import find_markdown_files, parse_table  # noqa: E402

RULE_NAME = "assumptions-explicit-with-confidence"
VALID_CONFIDENCE = {"strong", "reasonable", "uncertain"}
CANVAS_GLOB = "*canvas*.md"
ASSUMPTIONS_HEADER = re.compile(r"assumption.*factor.*unit.*confidence", re.IGNORECASE)
FORMULA_PATTERN = re.compile(r"(CoD\s*=|Formula:)", re.IGNORECASE)
COD_RESULT_PATTERN = re.compile(
    r"\*?\*?Cost of Delay\*?\*?\s*\(?.*\)?\s*\|\s*\$[\d,]+", re.IGNORECASE
)


class AssumptionsScanner(Scanner):
    def scan_with_context(self, context: ScanFilesContext) -> list:
        violations: list[Violation] = []
        for fp in context.files.all_files:
            violations.extend(self._check_canvas(fp))
        return violations

    def _check_canvas(self, path: Path) -> list[Violation]:
        violations: list[Violation] = []
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        rows = parse_table(lines, ASSUMPTIONS_HEADER)
        if not rows:
            violations.append(Violation(
                self.rule,
                f"No assumptions table found in {path.name}. "
                "Every canvas must have a table with Assumption, Factor, Unit, Confidence columns.",
                location=str(path),
            ))
            return violations

        for i, row in enumerate(rows, start=1):
            conf = row.get("confidence", "").strip().lower()
            if not conf:
                violations.append(Violation(
                    self.rule,
                    f"Assumption row {i} in {path.name} has blank Confidence. "
                    f"Must be Strong / Reasonable / Uncertain.",
                    location=str(path),
                ))
            elif conf not in VALID_CONFIDENCE:
                violations.append(Violation(
                    self.rule,
                    f"Assumption row {i} in {path.name} has invalid Confidence '{conf}'. "
                    f"Must be Strong / Reasonable / Uncertain.",
                    location=str(path),
                ))

        has_formula = any(FORMULA_PATTERN.search(line) for line in lines)
        if not has_formula:
            violations.append(Violation(
                self.rule,
                f"No CoD formula found in {path.name}. "
                "Show CoD as a product of the assumption factors.",
                location=str(path),
            ))

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    canvases = find_markdown_files(workspace, CANVAS_GLOB)
    return ScanFilesContext(files=FileCollection(code_files=canvases))


if __name__ == "__main__":
    sys.exit(execute_scan_with_workspace(
        AssumptionsScanner,
        RULE_NAME,
        _build_context,
        skill_root=_SKILL_ROOT,
    ))
