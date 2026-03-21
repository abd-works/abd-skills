#!/usr/bin/env python3
"""Build parts/steps/built/ from parts/steps/<name>.md + rules (same pattern as solution modeler pieces/phases/*.md → pieces/phases/built/)."""
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_STEPS_DIR = _SKILL_DIR / "parts" / "steps"
_BUILT_DIR = _STEPS_DIR / "built"
_RULES_DIR = _SKILL_DIR / "rules"


def _rewrite_relative_links_for_built_file(content: str) -> str:
    """Built files live under parts/steps/built/ — fix links authored for parts/steps/ or rules/."""
    content = content.replace("](../parts/process.md)", "](../../process.md)")
    content = content.replace("](../process.md)", "](../../process.md)")
    return content


# Step folder name (matches part name) -> list of rule filenames (in rules/) to bake in
STEP_RULES: dict[str, list[str]] = {
    "modules-epics-foundational-spine": [
        "foundational-spine-and-evidence-stage.md",
        "verb-noun-module-epic-story.md",
        "scaffold-concept-story-name-alignment.md",
        "chunks-must-be-referenced.md",
        "no-junk-concepts.md",
        "no-duplicates.md",
        "classify-variants-before-modeling.md",
        "epic-requires-confirming-stories.md",
    ],
    "modules-epics-scaffold-breadth": [
        "foundational-spine-and-evidence-stage.md",
        "verb-noun-module-epic-story.md",
        "concept-layering-scaffold.md",
        "module-depends-on.md",
        "chunks-must-be-referenced.md",
        "scaffold-concept-story-name-alignment.md",
        "no-junk-concepts.md",
        "no-duplicates.md",
        "classify-variants-before-modeling.md",
        "epic-requires-confirming-stories.md",
    ],
    "concept-classification": [
        "no-duplicates.md",
        "no-junk-concepts.md",
    ],
    "concept-classes-stories": [
        "step6-deepen-ai-only-no-merge-scripts.md",
        "foundation-coverage-before-deepen.md",
        "chunks-must-be-referenced.md",
        "no-duplicates.md",
        "epic-requires-confirming-stories.md",
        "no-junk-concepts.md",
        "concepts-must-have-owns.md",
        "stories-must-have-trigger-response.md",
        "domain-interaction-sync.md",
        "hierarchy-approximately-4-to-9-children.md",
    ],
    "integrate-harmonize": [
        "cross-cutting-resolved.md",
        "no-duplicates.md",
        "domain-interaction-sync.md",
    ],
    "evidence": [
        "evidence-scaffold-refs.md",
        "evidence-files-exist.md",
        "evidence-schema-valid.md",
    ],
    "structure": [
        "no-anemia.md",
        "no-over-centralization.md",
        "domain-interaction-sync.md",
    ],
    "finalize": [
        "assessment-complete.md",
    ],
}


def build_steps(skill_path: Path | None = None) -> int:
    """Build step files with baked-in rules into parts/steps/built/. Returns count of built files."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    steps_dir = skill_path / "parts" / "steps"
    built_dir = steps_dir / "built"
    rules_dir = skill_path / "rules"

    built_dir.mkdir(parents=True, exist_ok=True)
    for p in built_dir.iterdir():
        try:
            p.unlink()
        except OSError:
            pass

    count = 0
    for step_name, rule_filenames in STEP_RULES.items():
        base_file = steps_dir / f"{step_name}.md"
        if not base_file.exists():
            continue

        base_text = base_file.read_text(encoding="utf-8").strip()
        parts = [base_text]

        rule_texts: list[str] = []
        for rname in rule_filenames:
            rpath = rules_dir / rname
            if rpath.exists():
                rule_texts.append(rpath.read_text(encoding="utf-8").strip())
            else:
                rule_texts.append(f"<!-- Rule not found: {rname} -->")

        if rule_texts:
            parts.append("\n\n---\n\n## Rules (baked in)\n\nApply these rules when producing output for this step.\n")
            for rt in rule_texts:
                parts.append(rt)
                parts.append("\n\n---\n")

        out_text = "\n".join(parts).rstrip() + "\n"
        out_text = _rewrite_relative_links_for_built_file(out_text)
        out_file = built_dir / f"{step_name}.md"
        out_file.write_text(out_text, encoding="utf-8")
        count += 1
        print(f"  {step_name}: base + {len(rule_filenames)} rules -> built/{step_name}.md")

    return count


if __name__ == "__main__":
    n = build_steps()
    print(f"Built {n} step file(s) in parts/steps/built/")
