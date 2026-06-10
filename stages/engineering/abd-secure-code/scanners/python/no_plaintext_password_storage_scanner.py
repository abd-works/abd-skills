"""Scanner: No Plaintext Password Storage (python)."""
from __future__ import annotations

import sys
from pathlib import Path

_common = Path(__file__).resolve().parent.parent / "common"
if str(_common) not in sys.path:
    sys.path.insert(0, str(_common))

from catalog_scanner import run_catalog_scan
from code_scanner import CodeScanner, run_scanner_main

RULE_SLUG = "no-plaintext-password-storage"


class NoPlaintextPasswordStorageScanner(CodeScanner):
    def scan(self, context) -> list:
        files = (
            self._get_js_files(context)
            if hasattr(self, "_get_js_files")
            else self._get_java_files(context)
            if hasattr(self, "_get_java_files")
            else context.get("code_files", [])
        )
        return run_catalog_scan(RULE_SLUG, "python", self.rule, files)


if __name__ == "__main__":
    run_scanner_main(NoPlaintextPasswordStorageScanner, RULE_SLUG)
