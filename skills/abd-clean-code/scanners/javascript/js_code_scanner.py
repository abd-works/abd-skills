"""Base scanner for JavaScript/TypeScript production code quality checks."""
import re
from pathlib import Path


class JsCodeScanner:
    """Base class for clean code JS scanners using regex analysis."""

    JS_EXTENSIONS = {'.js', '.mjs', '.ts', '.tsx', '.jsx'}

    def __init__(self, rule):
        self.rule = rule

    def scan(self, context) -> list:
        return []

    def _get_js_files(self, context) -> list:
        return [
            f for f in context.get('code_files', [])
            if Path(f).suffix in self.JS_EXTENSIONS
        ]

    def _read_file(self, file_path: Path):
        if not file_path.exists():
            return None
        try:
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return None

    def _count_function_lines(self, content: str, func_start: int) -> int:
        """Estimate line count of a function starting at func_start (0-indexed)."""
        lines = content.split('\n')
        depth = 0
        for i, line in enumerate(lines[func_start:], start=func_start):
            depth += line.count('{') - line.count('}')
            if i > func_start and depth <= 0:
                return i - func_start + 1
        return len(lines) - func_start
