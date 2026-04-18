"""Base scanner for production code quality checks."""
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from scanner_bases.scanner import Scanner
    from scanner_bases.violation import Violation


class CodeScanner:
    """Base class for clean code production code scanners."""

    def __init__(self, rule):
        self.rule = rule

    def scan(self, context) -> list:
        return []

    def _read_and_parse_file(self, file_path: Path):
        """Read and parse a Python file, returning (content, lines, tree) or None."""
        if not file_path.exists():
            return None
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            tree = ast.parse(content, filename=str(file_path))
            return (content, lines, tree)
        except (SyntaxError, UnicodeDecodeError):
            return None

    def _function_line_count(self, node: ast.FunctionDef) -> int:
        """Count lines spanned by a function definition."""
        if not hasattr(node, 'end_lineno') or not hasattr(node, 'lineno'):
            return 0
        return node.end_lineno - node.lineno + 1
