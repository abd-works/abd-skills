"""Generate language scanner entrypoints from the pattern catalog."""
from __future__ import annotations

from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
LANGS = ("python", "javascript", "java")
BASE_IMPORT = {
    "python": "code_scanner",
    "javascript": "js_code_scanner",
    "java": "java_code_scanner",
}
RULES = [
    "no-hardcoded-secrets",
    "no-sql-string-concatenation",
    "no-os-command-injection",
    "no-eval-dynamic-code-execution",
    "no-dangerous-xss-sinks",
    "no-plaintext-password-storage",
    "no-sensitive-error-disclosure",
    "no-unsafe-deserialization",
    "no-mass-assignment-from-request",
    "no-weak-crypto-algorithms",
    "no-predictable-session-token",
    "no-unsafe-file-upload-handling",
    "no-path-traversal-in-paths",
    "no-secrets-in-log-output",
    "no-ldap-filter-injection",
    "no-xxe-unsafe-xml-parser",
    "no-untrusted-component-sources",
    "no-insufficient-login-rate-limiting",
    "no-toctou-outside-lock",
    "no-missing-security-event-logging",
    "no-excessive-response-data",
    "no-plaintext-sensitive-data-at-rest",
    "no-client-side-auth-trust",
    "no-jwt-none-algorithm",
]

TEMPLATE = '''\
"""Scanner: {title} ({lang})."""
from __future__ import annotations

import sys
from pathlib import Path

_common = Path(__file__).resolve().parent.parent / "common"
if str(_common) not in sys.path:
    sys.path.insert(0, str(_common))

from catalog_scanner import run_catalog_scan
from {base_import} import {base_class}, run_scanner_main

RULE_SLUG = "{rule_slug}"


class {class_name}({base_class}):
    def scan(self, context) -> list:
        files = (
            self._get_js_files(context)
            if hasattr(self, "_get_js_files")
            else self._get_java_files(context)
            if hasattr(self, "_get_java_files")
            else context.get("code_files", [])
        )
        return run_catalog_scan(RULE_SLUG, "{lang}", self.rule, files)


if __name__ == "__main__":
    run_scanner_main({class_name}, RULE_SLUG)
'''

SPECIAL_PYTHON_SQL = '''\
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
    r"\\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|WHERE|FROM|ALTER|CREATE)\\b", re.I
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
'''


def _class_name(rule_slug: str) -> str:
    parts = rule_slug.replace("-", "_").split("_")
    return "".join(p.capitalize() for p in parts) + "Scanner"


def _file_stem(rule_slug: str) -> str:
    return rule_slug.replace("-", "_") + "_scanner.py"


def main() -> None:
    for lang in LANGS:
        base_import = BASE_IMPORT[lang]
        base_class = "JsCodeScanner" if lang == "javascript" else (
            "JavaCodeScanner" if lang == "java" else "CodeScanner"
        )
        out_dir = SKILL / "scanners" / lang
        for rule in RULES:
            stem = _file_stem(rule)
            path = out_dir / stem
            if lang == "python" and rule == "no-sql-string-concatenation":
                path.write_text(SPECIAL_PYTHON_SQL, encoding="utf-8")
                continue
            title = rule.replace("-", " ").title()
            path.write_text(
                TEMPLATE.format(
                    title=title,
                    lang=lang,
                    base_import=base_import,
                    base_class=base_class,
                    rule_slug=rule,
                    class_name=_class_name(rule),
                ),
                encoding="utf-8",
            )
            print(f"Wrote {path}")


if __name__ == "__main__":
    main()
