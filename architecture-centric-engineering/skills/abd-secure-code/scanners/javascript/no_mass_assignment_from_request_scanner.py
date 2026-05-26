"""Scanner: No Mass Assignment From Request (javascript)."""
from __future__ import annotations

import sys
from pathlib import Path

_common = Path(__file__).resolve().parent.parent / "common"
if str(_common) not in sys.path:
    sys.path.insert(0, str(_common))

from catalog_scanner import run_catalog_scan
from js_code_scanner import JsCodeScanner, run_scanner_main

RULE_SLUG = "no-mass-assignment-from-request"


class NoMassAssignmentFromRequestScanner(JsCodeScanner):
    def scan(self, context) -> list:
        files = (
            self._get_js_files(context)
            if hasattr(self, "_get_js_files")
            else self._get_java_files(context)
            if hasattr(self, "_get_java_files")
            else context.get("code_files", [])
        )
        return run_catalog_scan(RULE_SLUG, "javascript", self.rule, files)


if __name__ == "__main__":
    run_scanner_main(NoMassAssignmentFromRequestScanner, RULE_SLUG)
