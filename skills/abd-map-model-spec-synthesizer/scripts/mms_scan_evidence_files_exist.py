"""Scanner: all evidence files must exist.

Rule: evidence-files-exist
Rule file: rules/evidence-files-exist.md

Checks that evidence/actions.json, decisions.json, states.json, relationships.json exist.

Usage (standalone):
    python scripts/mms_scan_evidence_files_exist.py [--evidence <dir>]

Default evidence dir: evidence/
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import sys
from pathlib import Path

RULE_ID = "evidence-files-exist"
REQUIRED_FILES = ["actions.json", "decisions.json", "states.json", "relationships.json"]


def scan(evidence_dir: Path) -> list[tuple[str, str]]:
    """Return list of (file, message) for missing files."""
    violations = []
    for fname in REQUIRED_FILES:
        p = evidence_dir / fname
        if not p.exists():
            violations.append((fname, f"Missing: {p}"))
    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    try:
        from _config import default_evidence_dir
        default_evidence = str(default_evidence_dir())
    except ImportError:
        default_evidence = str(skill_dir / "evidence")

    parser = argparse.ArgumentParser(
        description=f"Evidence files exist scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--evidence",
        default=default_evidence,
    )
    args = parser.parse_args()

    evidence_dir = Path(args.evidence)
    violations = scan(evidence_dir)

    if violations:
        for fname, msg in violations:
            print(f"[{RULE_ID}] {msg}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
