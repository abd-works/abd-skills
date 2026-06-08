#!/usr/bin/env python3
"""
generate-skill-catalog.py

Scans practices/*/skills/*/SKILL.md, reads front-matter (name, catalogue_one_liner),
derives SkillFamily from the practice folder name, and writes:
  packages/kanban/shared/skill-catalog.json

Run from the app root:
  python scripts/generate-skill-catalog.py

Or from repo root:
  python practices/kanban/apps/abd-delivery-agent-kanban/scripts/generate-skill-catalog.py
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve roots
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
APP_ROOT = SCRIPT_DIR.parent                           # abd-delivery-agent-kanban/
REPO_ROOT = APP_ROOT.parents[3]                        # agilebydesign-skills/
PRACTICES_ROOT = REPO_ROOT / "practices"
OUT_FILE = APP_ROOT / "packages" / "kanban" / "shared" / "skill-catalog.json"

# Practice folder name → SkillFamily
FOLDER_TO_FAMILY: dict[str, str] = {
    "architecture-centric-engineering": "architecture-centric-engineering",
    "domain-driven-design":             "domain-driven-design",
    "idea-shaping":                     "idea-shaping",
    "kanban":                           "delivery",
    "story-driven-delivery":            "story-driven-delivery",
    "user-experience-design":           "user-experience-design",
    "context-to-memory":                "context-to-memory",
    "utilities":                        "context-to-memory",
}

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
FIELD_RE        = re.compile(r"^(\w[\w_-]*):\s*(.+)$", re.MULTILINE)


def parse_front_matter(text: str) -> dict[str, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    # strip YAML multi-line continuations (lines that start with spaces after a key)
    # Simple key: value extraction — enough for our front matter shape
    result: dict[str, str] = {}
    current_key = None
    current_val: list[str] = []
    for line in block.splitlines():
        key_m = re.match(r"^(\w[\w_-]*):\s*(.*)", line)
        if key_m:
            if current_key:
                result[current_key] = " ".join(current_val).strip()
            current_key = key_m.group(1)
            current_val = [key_m.group(2).strip(">").strip()]
        elif current_key and line.startswith("  "):
            current_val.append(line.strip())
    if current_key:
        result[current_key] = " ".join(current_val).strip()
    return result


def skill_id_to_label(skill_id: str) -> str:
    """Default label: strip 'abd-', replace '-' with space, title-case."""
    label = re.sub(r"^abd-", "", skill_id).replace("-", " ")
    return label


def scan_practices(practices_root: Path) -> list[dict]:
    entries: list[dict] = []
    for practice_dir in sorted(practices_root.iterdir()):
        if not practice_dir.is_dir():
            continue
        family = FOLDER_TO_FAMILY.get(practice_dir.name)
        if family is None:
            continue  # not a known practice family
        skills_dir = practice_dir / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = parse_front_matter(text)
            skill_id = skill_dir.name  # folder name is the canonical skill ID
            label = fm.get("catalogue_one_liner") or skill_id_to_label(skill_id)
            # Truncate long one-liners to a short label
            if len(label) > 40:
                label = skill_id_to_label(skill_id)
            entries.append({
                "skillId": skill_id,
                "family":  family,
                "label":   label,
            })
    return entries


def main() -> None:
    if not PRACTICES_ROOT.exists():
        print(f"ERROR: practices root not found: {PRACTICES_ROOT}", file=sys.stderr)
        sys.exit(1)

    entries = scan_practices(PRACTICES_ROOT)

    catalog = {e["skillId"]: {"family": e["family"], "label": e["label"]} for e in entries}

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(catalog)} skills -> {OUT_FILE.relative_to(APP_ROOT)}")
    for e in entries:
        print(f"  {e['skillId']:50s} {e['family']}")


if __name__ == "__main__":
    main()
