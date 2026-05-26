"""Base scanner for secure Java production code checks."""
from __future__ import annotations

import argparse
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
    "context",
    "scanners",
    "target",
    "gradle",
    ".gradle",
}

_SOURCE_ROOT_NAMES = (
    "packages",
    "src",
    "server",
    "client",
    "app",
    "lib",
    "api",
    "main",
    "java",
)


class JavaCodeScanner:
    """Base class for Java secure-code scanners."""

    JAVA_EXTENSIONS = {".java"}

    def __init__(self, rule: str):
        self.rule = rule

    def scan(self, context: dict) -> list:
        return []

    def _get_java_files(self, context: dict) -> list:
        return [
            f for f in context.get("code_files", [])
            if Path(f).suffix in self.JAVA_EXTENSIONS
        ]

    def _read_file(self, file_path: Path):
        if not file_path.exists():
            return None
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None


def _is_test_file(path: Path) -> bool:
    name = path.name.lower()
    path_str = str(path).replace("\\", "/").lower()
    if name.endswith("test.java") or name.endswith("tests.java"):
        return True
    if name.startswith("test") and name.endswith(".java"):
        return True
    # Standard Java/Gradle test source layouts — not skill `test/fixtures/` trees
    for marker in ("/src/test/", "/test/java/", "/androidtest/", "/tests/"):
        if marker in path_str:
            return True
    return False


def build_code_context(workspace: Path) -> dict:
    """Collect production Java files under common source roots."""
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
        for path in base.rglob("*.java"):
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
