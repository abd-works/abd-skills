#!/usr/bin/env python3
"""Verify *.mdc body matches sibling *.instructions.md under ide-files/ (or skill root legacy)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# run_scanners.py prepends execute-skill-using-skills-rules/scripts to PYTHONPATH
from scanner_bases.simple_rule import SimpleRule  # noqa: E402
from scanner_bases.violation import Violation  # noqa: E402

RULE_STEM = "mdc-instructions-parity"

_FM = re.compile(r"^\ufeff?---\s*\n.*?\n---\s*\n?", re.DOTALL)


def _strip_yaml_frontmatter(text: str) -> str:
    m = _FM.match(text)
    if m:
        return text[m.end() :]
    return text.lstrip("\ufeff")


def _normalize_body(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in s.split("\n")]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _instructions_stem(path: Path) -> str:
    name = path.name
    suffix = ".instructions.md"
    if name.endswith(suffix):
        return name[: -len(suffix)]
    return path.stem


def _ide_payload_dir(workspace: Path) -> Path:
    ide = workspace / "ide-files"
    if ide.is_dir():
        return ide
    return workspace


def scan_workspace(workspace: Path) -> list[Violation]:
    rule = SimpleRule(name=RULE_STEM, rule_file=f"rules/{RULE_STEM}.md")
    violations: list[Violation] = []

    payload = _ide_payload_dir(workspace)
    mdc_by_stem = {p.stem: p for p in payload.glob("*.mdc") if p.is_file()}
    instr_by_stem: dict[str, Path] = {}
    for p in payload.glob("*.instructions.md"):
        if p.is_file():
            instr_by_stem[_instructions_stem(p)] = p

    if not mdc_by_stem:
        violations.append(
            Violation(
                rule,
                f"No .mdc files found in {payload} — every skill must have at least one "
                f"Cursor rule file under ide-files/ (or skill root as legacy fallback)",
                location=str(payload),
            )
        )
        return violations

    for stem, mdc_path in sorted(mdc_by_stem.items()):
        instr_path = instr_by_stem.get(stem)
        if not instr_path:
            violations.append(
                Violation(
                    rule,
                    f"Missing paired .instructions.md for {mdc_path.name} "
                    f"(expected {stem}.instructions.md in {payload})",
                    location=str(mdc_path),
                )
            )
            continue
        mdc_body = _normalize_body(_strip_yaml_frontmatter(mdc_path.read_text(encoding="utf-8")))
        instr_body = _normalize_body(instr_path.read_text(encoding="utf-8"))
        if mdc_body != instr_body:
            violations.append(
                Violation(
                    rule,
                    f"Body mismatch: {mdc_path.name} vs {instr_path.name} "
                    f"(.mdc body after frontmatter must equal .instructions.md)",
                    location=str(workspace),
                )
            )

    for stem, instr_path in sorted(instr_by_stem.items()):
        if stem not in mdc_by_stem:
            violations.append(
                Violation(
                    rule,
                    f"Orphan .instructions.md: {instr_path.name} has no paired {stem}.mdc",
                    location=str(instr_path),
                )
            )

    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mdc / .instructions.md body parity")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Target skill root (directory containing SKILL.md and ide-files/, or legacy *.mdc in root).",
    )
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"Not a directory: {workspace}", file=sys.stderr)
        return 2

    violations = scan_workspace(workspace)
    if not violations:
        return 0
    for v in violations:
        print(v.to_dict(), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
