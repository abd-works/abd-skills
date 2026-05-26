"""Base scanner for secure production Python code checks."""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

_COMMON = Path(__file__).resolve().parent.parent / "common"
if str(_COMMON) not in sys.path:
    sys.path.insert(0, str(_COMMON))
_SKIP_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    "context",
    "scanners",
}

_SOURCE_ROOT_NAMES = ("packages", "src", "server", "client", "app", "lib", "api")


class CodeScanner:
    """Base class for Python secure-code scanners."""

    PY_EXTENSIONS = {".py"}

    def __init__(self, rule: str):
        self.rule = rule

    def scan(self, context: dict) -> list:
        return []

    def _read_and_parse_file(self, file_path: Path):
        if not file_path.exists():
            return None
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            tree = ast.parse(content, filename=str(file_path))
            return content, lines, tree
        except (SyntaxError, UnicodeDecodeError):
            return None


def _is_test_file(path: Path) -> bool:
    name = path.name.lower()
    return name.startswith("test_") or name.endswith("_test.py") or "/tests/" in str(path).replace("\\", "/")


def build_code_context(workspace: Path) -> dict:
    """Collect production Python files under common source roots."""
    root = workspace.resolve()
    code_files: list[str] = []
    search_roots: list[Path] = []

    for name in _SOURCE_ROOT_NAMES:
        candidate = root / name
        if candidate.is_dir():
            search_roots.append(candidate)

    if not search_roots:
        search_roots = [root]

    for base in search_roots:
        for path in base.rglob("*.py"):
            if not path.is_file():
                continue
            if any(part in _SKIP_DIRS for part in path.parts):
                continue
            if _is_test_file(path):
                continue
            code_files.append(str(path))

    return {"code_files": sorted(set(code_files)), "project_root": str(root)}


def run_scanner_main(scanner_class, rule_name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--story-graph", type=Path, default=None)
    args = parser.parse_args()

    context = build_code_context(args.workspace)
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
