#!/usr/bin/env python3
"""Append rules from rules/*.md into the target skill's SKILL.md (within marker block).

Runs entirely inside the execute_rules skill — does not call scripts/base/build.py.
Idempotent: replaces content between HTML markers so re-runs do not duplicate text.

Usage (from anywhere):
  python skills/execute_rules/scripts/bundle_rules_into_skill_md.py --skill-root /path/to/skill

Optional:
  --skill-md PATH   Path relative to skill root (default: SKILL.md)
  --dry-run         Print planned bundle to stdout; do not write SKILL.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_MARK_BEGIN = "<!-- execute_rules:bundle_rules:begin -->"
_MARK_END = "<!-- execute_rules:bundle_rules:end -->"
_SECTION_INTRO = """## Bundled rules

The following prose is **generated** from `rules/*.md` in this skill. Edit the files under **`rules/`**, then re-run:

`python skills/execute_rules/scripts/bundle_rules_into_skill_md.py --skill-root <this-skill-root>`

"""


def _split_yaml_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            body = "\n".join(lines[i + 1 :])
            if body.startswith("\n"):
                body = body[1:]
            fm = "\n".join(lines[1:i])
            return fm, body
    return "", text


def _title_from_frontmatter(fm: str, stem: str) -> str:
    for line in fm.splitlines():
        m = re.match(r"^title:\s*(.+)\s*$", line.strip(), re.I)
        if m:
            t = m.group(1).strip().strip("\"'")
            return t
    return stem.replace("-", " ").replace("_", " ").title()


def _collect_rule_bodies(rules_dir: Path) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if not rules_dir.is_dir():
        return out
    for path in sorted(rules_dir.glob("*.md")):
        stem = path.stem
        if stem.lower() in ("readme",):
            continue
        raw = path.read_text(encoding="utf-8")
        fm, body = _split_yaml_frontmatter(raw)
        body = body.strip()
        if not body:
            continue
        title = _title_from_frontmatter(fm, stem)
        out.append((title, body))
    return out


def _split_skill_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines()
    if len(lines) < 2 or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_block = "\n".join(lines[: i + 1]) + "\n"
            body = "\n".join(lines[i + 1 :])
            if body.startswith("\n"):
                body = body[1:]
            return fm_block, body
    return "", text


def _build_bundle_markdown(rule_entries: list[tuple[str, str]]) -> str:
    if not rule_entries:
        inner = "*No `rules/*.md` files in this skill (or only empty / README-only).*"
    else:
        chunks = []
        for title, body in rule_entries:
            chunks.append(f"### {title}\n\n{body}")
        inner = "\n\n".join(chunks)
    return f"{_MARK_BEGIN}\n{inner}\n{_MARK_END}"


def _inject_or_replace(body: str, bundle: str) -> str:
    if _MARK_BEGIN in body and _MARK_END in body:
        pre, _, rest = body.partition(_MARK_BEGIN)
        _, _, post = rest.partition(_MARK_END)
        new_body = pre.rstrip() + "\n\n" + bundle + "\n\n" + post.lstrip()
        return new_body.rstrip() + "\n"
    body = body.rstrip()
    if body:
        body += "\n\n"
    body += _SECTION_INTRO.rstrip() + "\n\n" + bundle + "\n"
    return body


def main() -> int:
    p = argparse.ArgumentParser(
        description="Bundle rules/*.md into SKILL.md between execute_rules markers."
    )
    p.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill root (directory with SKILL.md and optional rules/). Default: cwd.",
    )
    p.add_argument(
        "--skill-md",
        default="SKILL.md",
        help="Path to skill markdown relative to skill root (default: SKILL.md).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print result to stdout; do not write SKILL.md.",
    )
    args = p.parse_args()
    root: Path = args.skill_root.resolve()
    skill_md = (root / args.skill_md).resolve()
    rules_dir = root / "rules"

    if not skill_md.is_file():
        print(f"[execute-rules] Missing {skill_md}", file=sys.stderr)
        return 2

    entries = _collect_rule_bodies(rules_dir)
    bundle = _build_bundle_markdown(entries)
    full = skill_md.read_text(encoding="utf-8")
    fm_block, body = _split_skill_frontmatter(full)
    new_body = _inject_or_replace(body, bundle)
    new_full = (fm_block + new_body) if fm_block else new_body

    if args.dry_run:
        out = (new_full if new_full.endswith("\n") else new_full + "\n").encode("utf-8")
        sys.stdout.buffer.write(out)
        return 0

    skill_md.write_text(new_full, encoding="utf-8", newline="\n")
    print(f"[execute-rules] Wrote bundled rules into {skill_md} ({len(entries)} rule file(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
