#!/usr/bin/env python3
"""Inspect rules/*.md and rules/scanners.json; optional table sorted by rule file name."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import frontmatter_tags


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    result: dict[str, str] = {}
    for line in block.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip().lower()] = v.strip()
    tags_ordered = frontmatter_tags.ordered_tags_from_frontmatter_block(block)
    if tags_ordered:
        result["tags"] = tags_ordered
    elif result.get("tags"):
        result["tags"] = frontmatter_tags.normalize_tags_scalar(result["tags"])
    return result


def tags_contain(tags_val: str, tag: str) -> bool:
    return frontmatter_tags.tags_contain(tags_val, tag)


def print_rules_table(rules_dir: Path, filter_tag: str | None) -> None:
    rows: list[tuple[str, str]] = []
    for md in sorted(rules_dir.glob("*.md")):
        if md.name == "README.md":
            continue
        content = md.read_text(encoding="utf-8")
        meta = parse_frontmatter(content)
        if filter_tag and not tags_contain(meta.get("tags", ""), filter_tag):
            continue
        rule_id = md.stem
        title = meta.get("title", rule_id)
        rows.append((rule_id, title))
    rows.sort(key=lambda x: x[0].lower())
    print("rule_id | title")
    print("--------|------")
    for rule_id, title in rows:
        t = title[:60] + ("..." if len(title) > 60 else "")
        print(f"{rule_id} | {t}")


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
    )
    p.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill package root (skill-config.json, rules/). Default: current directory.",
    )
    p.add_argument(
        "--by-order",
        action="store_true",
        help="Print rules as a table (sorted alphabetically by rule file name).",
    )
    p.add_argument(
        "--list-scanners",
        action="store_true",
        help="Print merged scanner paths (one per line); same set run_scanners.py would run.",
    )
    p.add_argument(
        "--tag",
        default=None,
        metavar="TAG",
        help="With --by-order: only rules whose frontmatter tags include TAG.",
    )
    ns = p.parse_args()
    root = ns.skill_root.resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    if ns.list_scanners:
        cfg: dict = {}
        cfg_path_ls = root / "skill-config.json"
        if cfg_path_ls.is_file():
            cfg = json.loads(cfg_path_ls.read_text(encoding="utf-8"))
        _sd = Path(__file__).resolve().parent
        if str(_sd) not in sys.path:
            sys.path.insert(0, str(_sd))
        import scanner_paths  # noqa: E402

        for rel in scanner_paths.list_scanner_scripts(root, cfg):
            print(rel)
        return 0

    cfg_path = root / "skill-config.json"
    rules_dir = root / "rules"
    sj = rules_dir / "scanners.json"

    print(f"skill root: {root}")
    if cfg_path.is_file():
        print("skill-config.json: yes")
    else:
        print("skill-config.json: MISSING", file=sys.stderr)

    if rules_dir.is_dir():
        if ns.by_order:
            print()
            print("rules (table, sorted by rule file name):")
            print_rules_table(rules_dir, ns.tag)
        else:
            md = sorted(rules_dir.glob("*.md"))
            print(f"rules/*.md ({len(md)}):")
            for f in md:
                print(f"  - {f.name}")
    else:
        print("rules/: (missing)")

    if sj.is_file():
        data = json.loads(sj.read_text(encoding="utf-8"))
        binds = data.get("rule_scanner_bindings") or []
        flat = data.get("scanners") or []
        print(f"rules/scanners.json: rule_scanner_bindings={len(binds)}, scanners={len(flat)}")
        for b in binds:
            rid = b.get("rule_id", "?")
            scanner = b.get("scanner", "?")
            print(f"  {rid} -> {scanner}")
        for s in flat:
            print(f"  (flat) {s}")
    else:
        print("rules/scanners.json: (missing)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
