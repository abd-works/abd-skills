"""Scanner: SQL string concatenation (Python AST + catalog)."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

_common = Path(__file__).resolve().parent.parent / "common"
if str(_common) not in sys.path:
    sys.path.insert(0, str(_common))

from catalog_scanner import run_catalog_scan
from code_scanner import CodeScanner, run_scanner_main

RULE_SLUG = "no-sql-string-concatenation"
_SQL_KEYWORDS = re.compile(
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|WHERE|FROM|ALTER|CREATE)\b", re.I
)


class NoSqlStringConcatenationScanner(CodeScanner):
    def scan(self, context) -> list:
        violations = run_catalog_scan(
            RULE_SLUG, "python", self.rule, context.get("code_files", [])
        )
        seen = {(v["location"], v["line"]) for v in violations}
        for file_path in context.get("code_files", []):
            result = self._read_and_parse_file(Path(file_path))
            if result is None:
                continue
            _, _, tree = result
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    v = self._check_execute_call(node, file_path)
                    if v and (v["location"], v["line"]) not in seen:
                        violations.append(v)
                        seen.add((v["location"], v["line"]))
        return violations

    def _check_execute_call(self, node: ast.Call, file_path):
        func = node.func
        name = func.attr.lower() if isinstance(func, ast.Attribute) else (
            func.id.lower() if isinstance(func, ast.Name) else ""
        )
        if name not in {"execute", "executemany", "raw", "query", "executesql"}:
            return None
        if not node.args:
            return None
        sql_arg = node.args[0]
        if self._sql_has_dynamic_parts(sql_arg):
            return {
                "rule": self.rule,
                "message": (
                    "SQL embeds dynamic values via concatenation or f-string. "
                    "Use parameterized queries."
                ),
                "location": str(file_path),
                "line": getattr(sql_arg, "lineno", node.lineno),
            }
        return None

    def _sql_has_dynamic_parts(self, node: ast.AST) -> bool:
        if isinstance(node, (ast.JoinedStr, ast.BinOp)):
            text = ast.unparse(node) if hasattr(ast, "unparse") else ""
            return bool(_SQL_KEYWORDS.search(text))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "format" and node.args:
                inner = node.args[0]
                if isinstance(inner, ast.Constant) and isinstance(inner.value, str):
                    return bool(_SQL_KEYWORDS.search(inner.value))
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return False
        if isinstance(node, ast.Name):
            return True
        return False


if __name__ == "__main__":
    run_scanner_main(NoSqlStringConcatenationScanner, RULE_SLUG)
