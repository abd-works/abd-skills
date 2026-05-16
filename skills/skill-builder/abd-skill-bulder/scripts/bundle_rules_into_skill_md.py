from __future__ import annotations

import argparse
from pathlib import Path

BEGIN_MARKER = "<!-- execute_rules:bundle_rules:begin -->"
END_MARKER = "<!-- execute_rules:bundle_rules:end -->"


def collect_rules(rules_dir: Path) -> str:
    files = sorted(rules_dir.glob("*.md"))
    chunks: list[str] = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            chunks.append(text)
    return "\n\n".join(chunks)


def bundle(skill_root: Path) -> None:
    skill_md = skill_root / "SKILL.md"
    rules_dir = skill_root / "rules"

    if not skill_md.exists():
        raise FileNotFoundError(f"Missing SKILL.md at: {skill_md}")
    if not rules_dir.exists():
        raise FileNotFoundError(f"Missing rules directory at: {rules_dir}")

    source = skill_md.read_text(encoding="utf-8")
    start = source.find(BEGIN_MARKER)
    end = source.find(END_MARKER)

    if start == -1 or end == -1 or end < start:
        raise ValueError("Bundle markers not found or out of order in SKILL.md")

    start_block_end = start + len(BEGIN_MARKER)
    before = source[:start_block_end]
    after = source[end:]

    rules_text = collect_rules(rules_dir)
    injected = "\n\n" + (rules_text if rules_text else "<!-- No rules found in rules/*.md -->") + "\n\n"

    updated = before + injected + after
    skill_md.write_text(updated, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inline rules/*.md into SKILL.md bundle block")
    parser.add_argument(
        "--skill-root",
        default=".",
        help="Path to skill root containing SKILL.md and rules/ (default: current directory)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bundle(Path(args.skill_root).resolve())
