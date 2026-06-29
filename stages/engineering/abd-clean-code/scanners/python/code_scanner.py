"""Base scanner for production code quality checks."""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scanner_bases.scanner import Scanner
    from scanner_bases.violation import Violation

_SKIP_DIRS = {"node_modules", ".git", "dist", "build", "coverage", "__pycache__", ".venv", "venv"}


class CodeScanner:
    """Base class for clean code production code scanners."""

    PY_EXTENSIONS = {".py"}

    def __init__(self, rule):
        self.rule = rule

    def scan(self, context) -> list:
        return []

    def _read_and_parse_file(self, file_path: Path):
        """Read and parse a Python file, returning (content, lines, tree) or None."""
        if not file_path.exists():
            return None
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            tree = ast.parse(content, filename=str(file_path))
            return (content, lines, tree)
        except (SyntaxError, UnicodeDecodeError):
            return None

    def _function_line_count(self, node: ast.FunctionDef) -> int:
        """Count lines spanned by a function definition."""
        if not hasattr(node, "end_lineno") or not hasattr(node, "lineno"):
            return 0
        return node.end_lineno - node.lineno + 1


def _is_production_py_file(path: Path) -> bool:
    if path.suffix != ".py" or not path.is_file():
        return False
    if any(part in _SKIP_DIRS for part in path.parts):
        return False
    if "tests" in path.parts:
        return False
    name = path.name.lower()
    return not (name.startswith("test_") or name.endswith("_test.py"))


def _collect_py_files(search_roots: list[Path]) -> list[str]:
    code_files: list[str] = []
    seen: set[str] = set()
    for base in search_roots:
        if base.is_file():
            candidates = [base]
        elif base.is_dir():
            candidates = list(base.rglob("*.py"))
        else:
            continue
        for path in candidates:
            if not _is_production_py_file(path):
                continue
            resolved = str(path.resolve())
            if resolved not in seen:
                seen.add(resolved)
                code_files.append(resolved)
    return sorted(code_files)


def build_code_context(
    workspace: Path,
    code_dirs: list[Path] | None = None,
) -> dict:
    """Collect production Python files for scanning.

  When ``code_dirs`` is set, only those paths are scanned (relative to
  ``workspace`` unless absolute). Otherwise: ``packages/``, then ``scripts/``,
  then the workspace root itself.
    """
    root = workspace.resolve()
    if code_dirs:
        search_roots = [
            d.resolve() if d.is_absolute() else (root / d).resolve()
            for d in code_dirs
        ]
    else:
        search_roots = []
        for sub in ("packages", "scripts"):
            candidate = root / sub
            if candidate.is_dir():
                search_roots.append(candidate)
        if not search_roots:
            search_roots = [root]

    code_files = _collect_py_files(search_roots)
    return {
        "code_files": code_files,
        "project_root": str(root),
        "scan_roots": [str(p) for p in search_roots],
    }


def run_scanner_main(scanner_class, rule_name: str) -> None:
    """CLI entrypoint: --workspace → scan → violations on stderr → exit code."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--story-graph", type=Path, default=None)
    parser.add_argument(
        "--code-dir",
        action="append",
        default=None,
        metavar="DIR",
        help=(
            "Explicit folder or .py file to scan (repeatable). "
            "Paths are relative to --workspace unless absolute."
        ),
    )
    args = parser.parse_args()

    code_dirs = [Path(d) for d in args.code_dir] if args.code_dir else None
    context = build_code_context(args.workspace, code_dirs=code_dirs)
    if not context["code_files"]:
        print(
            f"[WARN] {rule_name}: no Python files to scan "
            f"(workspace={args.workspace}, code-dir={args.code_dir})",
            file=sys.stderr,
        )

    scanner = scanner_class(rule_name)
    violations = scanner.scan(context)

    for v in violations:
        out = {
            "violation_message": v.get("message", str(v)),
            "severity": v.get("severity", "error"),
            "location": v.get("location", ""),
            "line": v.get("line", 0),
        }
        print(out, file=sys.stderr)

    sys.exit(1 if violations else 0)
