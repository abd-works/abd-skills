#!/usr/bin/env python3
"""Single scanner driver: load rule → build :class:`ScanFilesContext` → run → report.

Call sites are identical for every scanner: pass a *context factory*
``Callable[[Path], ScanFilesContext]`` that fills whatever the implementation needs
(``files`` only, ``story_graph`` JSON only, or both). No separate “story runner” type —
only different context payloads.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Type

# This file lives in …/execute-skill-using-skills-rules/scripts
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


def load_workspace_graph_json(workspace: Path) -> Dict[str, Any]:
    """Load graph-shaped JSON from conventional workspace paths (file I/O only).

    Returns ``{"epics": [], "increments": []}`` when no file is found.
    """
    for rel in (
        ("docs", "story", "story-graph.json"),
        ("story-graph.json",),
    ):
        p = workspace.joinpath(*rel)
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    return {"epics": [], "increments": []}


def execute_scan(
    scanner_class: Type[Any],
    rule: Any,
    context: Any,
) -> list:
    """Run ``scanner_class(rule).scan_with_context(context)``; return violations list."""
    scanner = scanner_class(rule)
    return scanner.scan_with_context(context)


def _violations_exit_code(violations: list) -> int:
    if not violations:
        return 0
    for v in violations:
        if isinstance(v, dict):
            print(v, file=sys.stderr)
        else:
            print(getattr(v, "to_dict", lambda: v)(), file=sys.stderr)
    return 1


def execute_scan_with_workspace(
    scanner_class: Type[Any],
    rule_md_name: str,
    build_context: Callable[[Path], Any],
    argv: list[str] | None = None,
    *,
    skill_root: Path | None = None,
) -> int:
    """CLI: ``--workspace`` → ``build_context(workspace)`` → rule + scan → exit code.

    *build_context* supplies the full :class:`~scanner_bases.resources.scan_context.ScanFilesContext`
    (or compatible) instance — e.g. graph JSON only, files only, or both.
    """
    parser = argparse.ArgumentParser(description="execute-skill-using-skills-rules: run one scanner")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Project tree (default: cwd).",
    )
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    root = (skill_root or Path.cwd()).resolve()

    from scanner_bases.simple_rule import SimpleRule

    rule_path = root / "rules" / f"{rule_md_name}.md"
    rule_file = str(rule_path) if rule_path.is_file() else f"{rule_md_name}.md"
    rule = SimpleRule(name=rule_md_name, rule_file=rule_file)

    context = build_context(workspace)
    violations = execute_scan(scanner_class, rule, context)
    return _violations_exit_code(violations)


def main_with_scanner(
    scanner_class: Type[Any],
    *,
    rule_md_name: str,
    argv: list[str] | None = None,
    **_legacy: Any,
) -> int:
    """Backward-compatible entry: graph JSON from workspace + empty :class:`FileCollection`.

    Extra keyword arguments (e.g. old flags) are ignored.
    """
    from scanner_bases.resources.scan_context import FileCollection, ScanFilesContext

    return execute_scan_with_workspace(
        scanner_class,
        rule_md_name,
        lambda ws: ScanFilesContext(
            story_graph=load_workspace_graph_json(ws),
            files=FileCollection(),
        ),
        argv=argv,
    )
