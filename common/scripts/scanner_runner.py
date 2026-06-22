#!/usr/bin/env python3
"""Single scanner driver: load rule → build :class:`ScanFilesContext` → run → report.

Call sites are identical for every scanner: pass a *context factory*
``Callable[[Path], ScanFilesContext]`` that fills whatever the implementation needs
(``files`` only, ``story_graph`` JSON only, or both). No separate “story runner” type —
only different context payloads.
"""
from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Type

# This file lives in …/execute-skill-using-skills-rules/scripts
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


def load_workspace_graph_json(workspace: Path, story_graph: Path | None = None) -> Dict[str, Any]:
    """Load story-graph.json.

    Uses *story_graph* path directly when provided (passed in by the runner).
    Falls back to recursive search under *workspace* so the function still
    works when called standalone.
    Returns ``{"epics": [], "increments": []}`` when no file is found.
    """
    if story_graph and story_graph.is_file():
        return json.loads(story_graph.read_text(encoding="utf-8"))
    matches = sorted(workspace.rglob("story-graph.json"))
    if matches:
        return json.loads(matches[0].read_text(encoding="utf-8"))
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


def _invoke_build_context(
    build_context: Callable[..., Any],
    workspace: Path,
    story_graph: Path | None,
) -> Any:
    """Call *build_context* with (workspace,) or (workspace, story_graph) as supported."""
    params = inspect.signature(build_context).parameters
    if len(params) >= 2:
        return build_context(workspace, story_graph)
    return build_context(workspace)


def execute_scan_with_workspace(
    scanner_class: Type[Any],
    rule_md_name: str,
    build_context: Callable[[Path, Path | None], Any],
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
    parser.add_argument(
        "--story-graph",
        type=Path,
        default=None,
        help="Explicit path to story-graph.json (passed by the runner).",
    )
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    story_graph: Path | None = args.story_graph.resolve() if args.story_graph else None
    root = (skill_root or Path.cwd()).resolve()

    from scanner_bases.simple_rule import SimpleRule

    rule_path = root / "rules" / f"{rule_md_name}.md"
    rule_file = str(rule_path) if rule_path.is_file() else f"{rule_md_name}.md"
    rule = SimpleRule(name=rule_md_name, rule_file=rule_file)

    context = _invoke_build_context(build_context, workspace, story_graph)
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
        lambda ws, sg: ScanFilesContext(
            story_graph=load_workspace_graph_json(ws, sg),
            files=FileCollection(),
        ),
        argv=argv,
    )
