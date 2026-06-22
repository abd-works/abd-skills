#!/usr/bin/env python3
"""Scanner: cd3-ranking-by-highest-first.

Checks every cd3-ranking file in --workspace for:
  1. A ranked items table exists with CoD, Duration, CD3 columns
  2. CD3 arithmetic is correct (CoD / Duration = CD3)
  3. Items are ordered by CD3 descending (or override rationale present)
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

RULE_NAME = "cd3-ranking-by-highest-first"
RANKING_GLOB = "*ranking*.md"
RANKING_HEADER = re.compile(r"rank.*cod.*duration.*cd3", re.IGNORECASE)


def _parse_money(s: str) -> float | None:
    """Parse '$1,000' or '1000' into a float."""
    cleaned = re.sub(r"[,$]", "", s.strip())
    try:
        return float(cleaned)
    except ValueError:
        return None


class CD3RankingScanner(Scanner):
    def scan_with_context(self, context: ScanFilesContext) -> list:
        violations: list[Violation] = []
        for fp in context.files.all_files:
            violations.extend(self._check_ranking(fp))
        return violations

    def _check_ranking(self, path: Path) -> list[Violation]:
        violations: list[Violation] = []
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        rows = parse_table(lines, RANKING_HEADER)
        if not rows:
            violations.append(Violation(
                self.rule,
                f"No ranked items table found in {path.name}. "
                "Expected a table with Rank, CoD, Duration, CD3 columns.",
                location=str(path),
            ))
            return violations

        prev_cd3: float | None = None
        for i, row in enumerate(rows, start=1):
            cod_col = next((v for k, v in row.items() if "cod" in k and "duration" not in k), None)
            dur_col = next((v for k, v in row.items() if "duration" in k), None)
            cd3_col = next((v for k, v in row.items() if "cd3" in k.replace(" ", "")), None)

            if cod_col is None or dur_col is None or cd3_col is None:
                continue

            cod = _parse_money(cod_col)
            dur = _parse_money(dur_col)
            cd3 = _parse_money(cd3_col)

            if cod is None or dur is None or cd3 is None:
                continue

            if dur > 0:
                expected = cod / dur
                tolerance = max(abs(expected) * 0.01, 0.5)
                if abs(cd3 - expected) > tolerance:
                    feature = row.get("feature / epic", row.get("item", f"row {i}"))
                    violations.append(Violation(
                        self.rule,
                        f"CD3 arithmetic error for '{feature}' in {path.name}: "
                        f"CoD {cod_col} / Duration {dur_col} = {expected:,.0f}, but CD3 shows {cd3_col}.",
                        location=str(path),
                    ))

            if prev_cd3 is not None and cd3 > prev_cd3:
                override_col = next(
                    (v for k, v in row.items() if "override" in k or "rationale" in k),
                    None,
                )
                has_override = override_col and override_col.strip() not in ("", "-", "\u2014")
                if not has_override:
                    feature = row.get("feature / epic", row.get("item", f"row {i}"))
                    prev_feature = rows[i - 2].get("feature / epic", rows[i - 2].get("item", f"row {i-1}"))
                    violations.append(Violation(
                        self.rule,
                        f"CD3 order violation in {path.name}: "
                        f"'{feature}' (CD3 {cd3:,.0f}) is ranked below "
                        f"'{prev_feature}' (CD3 {prev_cd3:,.0f}) without override rationale.",
                        location=str(path),
                    ))
            prev_cd3 = cd3

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    rankings = find_markdown_files(workspace, RANKING_GLOB)
    return ScanFilesContext(files=FileCollection(code_files=rankings))


if __name__ == "__main__":
    sys.exit(execute_scan_with_workspace(
        CD3RankingScanner,
        RULE_NAME,
        _build_context,
        skill_root=_SKILL_ROOT,
    ))
