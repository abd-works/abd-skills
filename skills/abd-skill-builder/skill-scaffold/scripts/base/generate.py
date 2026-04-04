"""
generate.py — generate a phase bundle and print it for injection into AI chat.

Usage:
    python scripts/base/generate.py --phase <phase-slug>

Reads skill-config.json and content/parts/ to assemble the phase prompt:
    principles → role → phase body → library shards → rules for that phase

Output is printed to stdout. Copy it into your AI chat session.

Copy this file from abd-skill-builder's scripts/generate.py and adjust
paths if needed.
"""
import sys
import argparse
from pathlib import Path
from skill_root import SKILL_ROOT

sys.path.insert(0, str(SKILL_ROOT / "scripts" / "base"))

try:
    from instructions import build_phase  # type: ignore
except ImportError:
    raise ImportError(
        "instructions.py not found. Copy scripts/base/instructions.py (and its dependencies) "
        "from abd-skill-builder into this skill's scripts/base/ folder."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate phase bundle for AI injection")
    parser.add_argument("--phase", required=True, help="Phase slug (matches content/parts/phases/<slug>.md)")
    args = parser.parse_args()

    output = build_phase(skill_root=SKILL_ROOT, phase_slug=args.phase)
    print(output)


if __name__ == "__main__":
    main()
