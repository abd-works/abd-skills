"""
scanner_{{rule_id}}.py — enforces rules/{{rule_id}}.md

Usage:
    python scripts/scanners/scanner_{{rule_id}}.py [--workspace <path>]

Exit 0  — no violations found
Exit 1  — violations found (details printed to stdout)

Replace {{rule_id}} with the actual rule id (matches the 'id' field
in the rule's front-matter and in skill-config.json → workspace.rule_scanner_bindings).
"""
from __future__ import annotations

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def scan(workspace: Path) -> list[str]:
    """
    Return a list of violation messages.
    Empty list = pass.

    Implement your check here. Examples:
    - Parse files in workspace for forbidden patterns.
    - Check that required headings exist.
    - Verify naming conventions.
    """
    violations: list[str] = []

    # --- YOUR CHECK LOGIC HERE ---
    # example_file = workspace / "some_output.md"
    # if not example_file.exists():
    #     violations.append(f"MISSING: {example_file}")
    # ---------------------

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Scanner: {{rule_id}}")
    parser.add_argument("--workspace", default=str(ROOT), help="Path to skill workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    violations = scan(workspace)

    if violations:
        print(f"[FAIL] scanner_{{rule_id}} — {len(violations)} violation(s):")
        for v in violations:
            print(f"  • {v}")
        return 1

    print("[PASS] scanner_{{rule_id}} — no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
