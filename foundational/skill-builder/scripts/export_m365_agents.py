#!/usr/bin/env python3
"""Export a skill package to M365 declarative agent format.

For each skill under a practice package (practices/{name}/skills/*), produces:
  {package}/m365-agents/{skill-short-name}/
    instructions.txt           (compressed SKILL.md for the 8,000-char instruction field)
    knowledge-*.txt            (rules, reference, templates chunked for upload)
    conversation-starters.txt  (suggested prompts)

Usage:
  python export_m365_agents.py --package practices/story-driven-delivery
  python export_m365_agents.py --package practices/domain-driven-design
  python export_m365_agents.py --package practices/story-driven-delivery --skill abd-story-mapping
  python export_m365_agents.py --package practices/story-driven-delivery --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAX_INSTRUCTION_CHARS = 7500
MAX_KNOWLEDGE_FILE_CHARS = 30_000
MAX_KNOWLEDGE_FILES = 20

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def _repo_root() -> Path:
    p = SCRIPT_DIR.resolve()
    for _ in range(16):
        if (p / "practices").is_dir() and (p / "foundational").is_dir():
            return p
        if (p / "scripts" / "deploy-skills.ps1").is_file():
            return p
        parent = p.parent
        if parent == p:
            break
        p = parent
    raise RuntimeError("Could not find repository root")


def parse_frontmatter(content: str) -> dict[str, str]:
    match = FRONTMATTER_RE.search(content)
    if not match:
        return {}
    block = match.group(1)
    result: dict[str, str] = {}
    for line in block.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip().lower()] = v.strip()
    return result


def strip_frontmatter(content: str) -> str:
    return FRONTMATTER_RE.sub("", content, count=1).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def discover_skills(package_dir: Path, filter_skill: str | None = None) -> list[Path]:
    skills_dir = package_dir / "skills"
    if not skills_dir.is_dir():
        print(f"  [warn] No skills/ directory in {package_dir}", file=sys.stderr)
        return []
    results = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").is_file():
            continue
        if filter_skill and child.name != filter_skill:
            continue
        results.append(child)
    return results


def build_instructions(skill_dir: Path) -> str:
    """Compress SKILL.md + reference/concepts.md into instruction text."""
    skill_md = read_text(skill_dir / "SKILL.md")
    fm = parse_frontmatter(skill_md)
    name = fm.get("name", skill_dir.name)
    description = fm.get("description", "").strip(">- \n")

    concepts_path = skill_dir / "reference" / "concepts.md"
    concepts_summary = ""
    if concepts_path.is_file():
        raw = strip_frontmatter(read_text(concepts_path))
        lines = raw.split("\n")
        summary_lines = []
        for line in lines[:80]:
            summary_lines.append(line)
        concepts_summary = "\n".join(summary_lines).strip()

    templates_summary = ""
    templates_dir = skill_dir / "templates"
    if templates_dir.is_dir():
        for tpl in sorted(templates_dir.glob("*.md")):
            raw = read_text(tpl)
            cleaned = strip_frontmatter(raw)
            instr_idx = cleaned.find("## Instructions")
            if instr_idx > 0:
                cleaned = cleaned[:instr_idx].strip()
            templates_summary += f"\nOUTPUT TEMPLATE ({tpl.stem}):\n{cleaned[:1500]}\n"

    rules_dir = skill_dir / "rules"
    rule_names = []
    if rules_dir.is_dir():
        for r in sorted(rules_dir.glob("*.md")):
            rule_names.append(r.stem.replace("-", " ").title())

    instruction = f"""You are a {name.replace("abd-", "").replace("-", " ").title()} assistant. {description}

KNOWLEDGE FILES: Your uploaded knowledge files contain detailed rules with DO/DON'T examples. Consult them when producing or reviewing output.

"""
    if concepts_summary:
        trimmed = concepts_summary[:3000]
        instruction += f"CORE CONCEPTS:\n{trimmed}\n\n"

    if templates_summary:
        instruction += f"{templates_summary.strip()[:1500]}\n\n"

    if rule_names:
        instruction += "RULES TO FOLLOW (details in knowledge files):\n"
        for rn in rule_names:
            instruction += f"- {rn}\n"
        instruction += "\n"

    instruction += "INTERACTION STYLE:\n- Ask clarifying questions when scope is ambiguous\n- Present output progressively\n- Record gaps honestly — never fabricate to fill missing information\n- Revise rather than work around stale structure\n"

    if len(instruction) > MAX_INSTRUCTION_CHARS:
        instruction = instruction[:MAX_INSTRUCTION_CHARS - 50] + "\n\n[Truncated — see knowledge files for full rules]\n"

    return instruction.strip()


def build_knowledge_files(skill_dir: Path) -> list[tuple[str, str]]:
    """Produce (filename, content) tuples for knowledge file upload."""
    files: list[tuple[str, str]] = []
    file_idx = 1

    # Reference files
    ref_dir = skill_dir / "reference"
    if ref_dir.is_dir():
        for ref_file in sorted(ref_dir.glob("*.md")):
            content = strip_frontmatter(read_text(ref_file))
            title = ref_file.stem.replace("-", " ").title()
            fname = f"knowledge-{file_idx:02d}-reference-{ref_file.stem}.txt"
            files.append((fname, f"REFERENCE: {title}\n\n{content}"))
            file_idx += 1

    # Rules — group into chunks to stay under 20 files
    rules_dir = skill_dir / "rules"
    if rules_dir.is_dir():
        rule_files = sorted(rules_dir.glob("*.md"))
        chunk: list[str] = []
        chunk_size = 0
        chunk_idx = 1

        for rf in rule_files:
            content = strip_frontmatter(read_text(rf))
            title = rf.stem.replace("-", " ").title()
            entry = f"RULE: {title}\n\n{content}\n\n{'=' * 60}\n\n"

            if chunk_size + len(entry) > MAX_KNOWLEDGE_FILE_CHARS and chunk:
                fname = f"knowledge-{file_idx:02d}-rules-{chunk_idx}.txt"
                files.append((fname, "".join(chunk)))
                file_idx += 1
                chunk_idx += 1
                chunk = []
                chunk_size = 0

            chunk.append(entry)
            chunk_size += len(entry)

        if chunk:
            fname = f"knowledge-{file_idx:02d}-rules-{chunk_idx}.txt"
            files.append((fname, "".join(chunk)))
            file_idx += 1

    # Templates
    templates_dir = skill_dir / "templates"
    if templates_dir.is_dir():
        tpl_content = ""
        for tpl in sorted(templates_dir.glob("*.md")):
            raw = strip_frontmatter(read_text(tpl))
            tpl_content += f"TEMPLATE: {tpl.stem}\n\n{raw}\n\n{'=' * 60}\n\n"
        if tpl_content.strip():
            fname = f"knowledge-{file_idx:02d}-templates.txt"
            files.append((fname, tpl_content))
            file_idx += 1

    # Examples
    examples_path = skill_dir / "reference" / "examples.md"
    if examples_path.is_file():
        pass  # already included via reference loop above


    if len(files) > MAX_KNOWLEDGE_FILES:
        print(f"  [warn] {len(files)} knowledge files exceeds M365 limit of {MAX_KNOWLEDGE_FILES}",
              file=sys.stderr)

    return files


def build_conversation_starters(skill_dir: Path) -> str:
    """Generate conversation starters from SKILL.md description."""
    skill_md = read_text(skill_dir / "SKILL.md")
    fm = parse_frontmatter(skill_md)
    description = fm.get("description", "").strip(">- \n")
    name = fm.get("name", skill_dir.name).replace("abd-", "").replace("-", " ")

    starters = [
        f"Create a {name} from this description",
        f"Review my {name} for quality issues",
        f"What context do you need to produce a {name}?",
        f"Deepen this {name} with more detail",
        f"Identify gaps in this {name}",
    ]
    return "CONVERSATION STARTERS (paste into agent builder)\n\n" + "\n".join(
        f"{i}. {s}" for i, s in enumerate(starters, 1)
    )


def export_skill(skill_dir: Path, output_dir: Path, dry_run: bool = False) -> None:
    """Export a single skill to M365 agent format."""
    short_name = skill_dir.name.replace("abd-", "")
    agent_dir = output_dir / short_name

    print(f"  Exporting: {skill_dir.name} -> {agent_dir.relative_to(output_dir.parent.parent)}")

    instructions = build_instructions(skill_dir)
    knowledge_files = build_knowledge_files(skill_dir)
    starters = build_conversation_starters(skill_dir)

    print(f"    instructions.txt: {len(instructions):,} chars")
    for fname, content in knowledge_files:
        print(f"    {fname}: {len(content):,} chars")
    print(f"    conversation-starters.txt: {len(starters):,} chars")

    if dry_run:
        print("    [dry-run] skipping file writes")
        return

    agent_dir.mkdir(parents=True, exist_ok=True)

    (agent_dir / "instructions.txt").write_text(instructions, encoding="utf-8")
    for fname, content in knowledge_files:
        (agent_dir / fname).write_text(content, encoding="utf-8")
    (agent_dir / "conversation-starters.txt").write_text(starters, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export skill package to M365 declarative agent format"
    )
    parser.add_argument(
        "--package", required=True,
        help="Relative path to package (e.g. practices/story-driven-delivery)"
    )
    parser.add_argument(
        "--skill", default=None,
        help="Export only this skill (folder name, e.g. abd-story-mapping)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be produced without writing files"
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Override output directory (default: {package}/m365-agents/)"
    )
    args = parser.parse_args()

    repo_root = _repo_root()
    package_dir = repo_root / args.package
    if not package_dir.is_dir():
        print(f"Error: package directory not found: {package_dir}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir) if args.output_dir else package_dir / "m365-agents"
    print(f"Package: {package_dir.relative_to(repo_root)}")
    print(f"Output:  {output_dir.relative_to(repo_root) if output_dir.is_relative_to(repo_root) else output_dir}")
    print()

    skills = discover_skills(package_dir, args.skill)
    if not skills:
        print("No skills found to export.", file=sys.stderr)
        return 1

    print(f"Found {len(skills)} skill(s) to export:\n")
    for skill_dir in skills:
        export_skill(skill_dir, output_dir, dry_run=args.dry_run)
        print()

    if not args.dry_run:
        print(f"Done. Upload files from: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
