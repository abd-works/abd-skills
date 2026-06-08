"""Scanner: No Os Command Injection (java)."""
from __future__ import annotations

import sys
from pathlib import Path

_common = Path(__file__).resolve().parent.parent / "common"
if str(_common) not in sys.path:
    sys.path.insert(0, str(_common))

from catalog_scanner import run_catalog_scan
from java_code_scanner import JavaCodeScanner, run_scanner_main

RULE_SLUG = "no-os-command-injection"


class NoOsCommandInjectionScanner(JavaCodeScanner):
    def scan(self, context) -> list:
        files = (
            self._get_js_files(context)
            if hasattr(self, "_get_js_files")
            else self._get_java_files(context)
            if hasattr(self, "_get_java_files")
            else context.get("code_files", [])
        )
        return run_catalog_scan(RULE_SLUG, "java", self.rule, files)


if __name__ == "__main__":
    run_scanner_main(NoOsCommandInjectionScanner, RULE_SLUG)
