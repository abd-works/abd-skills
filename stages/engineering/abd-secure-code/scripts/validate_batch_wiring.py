"""Validate batch-wiring.json: context paths and fixture files exist under corpus root."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
WIRING = SKILL / "inputs" / "batch-wiring.json"
CORPUS_CONFIG = SKILL / "inputs" / "corpus-root.json"


def corpus_root() -> Path:
    if CORPUS_CONFIG.is_file():
        data = json.loads(CORPUS_CONFIG.read_text(encoding="utf-8"))
        root = data.get("secure_code_warrior_root")
        if root:
            return Path(root)
    env = __import__("os").environ.get("SECURE_CODE_WARRIOR_ROOT")
    if env:
        return Path(env)
    # Sibling checkout: agilebydesign-skills + secure-code-warrior under same parent
    sibling = SKILL.resolve().parents[3] / "secure-code-warrior"
    if sibling.is_dir():
        return sibling
    raise SystemExit(
        "Set secure_code_warrior_root in inputs/corpus-root.json or SECURE_CODE_WARRIOR_ROOT"
    )


def main() -> int:
    repo = corpus_root()
    data = json.loads(WIRING.read_text(encoding="utf-8"))
    errors: list[str] = []

    batch = data["green_belt_batches"]["e0523"]
    for ch in batch["challenges"]:
        ctx = repo / ch["context"]
        fix = repo / ch["fixture"]
        if not ctx.is_file():
            errors.append(f"Missing context: {ch['context']} (under {repo})")
        if not fix.is_file():
            errors.append(f"Missing fixture: {ch['fixture']} (under {repo})")

    for ex in data.get("exercise_batches", []):
        ctx = repo / ex["context"]
        if not ctx.is_file():
            errors.append(f"Missing exercise context: {ex['context']} (under {repo})")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    n = len(batch["challenges"])
    print(f"OK: {n} green-belt challenges wired; {len(data['exercise_batches'])} exercise batches.")
    print(f"Corpus root: {repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
