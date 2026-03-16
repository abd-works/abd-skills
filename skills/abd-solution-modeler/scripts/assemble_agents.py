#!/usr/bin/env python3
"""Build AGENTS.md from pieces and build phase files with baked-in rules."""
import json
import shutil
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PIECES_DIR = _SKILL_DIR / "pieces"
_PHASES_DIR = _PIECES_DIR / "phases"
_BUILT_DIR = _PHASES_DIR / "built"
_RULES_DIR = _SKILL_DIR / "rules"

_CONTENT_ORDER = [
    "introduction.md",
    "context_prep.md",
    "process.md",
    "validation.md",
    "domain.md",
    "interaction_tree.md",
    "drawio.md",
    "scripts.md",
]

_PHASE_PREFIXES = [
    "concept-guidance", "concept-model", "structural",
    "behavior", "variation", "refined", "validated",
]

_PHASE_TO_PREFIX = {
    "concept_guidance_v1": "concept-guidance",
    "concept_guidance_v2": "concept-guidance",
    "concept_model": "concept-model",
    "structural_model": "structural",
    "behavior_model": "behavior",
    "variation_model": "variation",
    "refined_domain_model": "refined",
    "model_assessment": "validated",
    "final_domain_model": "validated",
}

_CODE_PHASES = {"normalize_context", "evidence_extraction", "evidence_graph"}


def _parse_order(rule_path: Path) -> int:
    """Extract order from YAML frontmatter. Default 999."""
    text = rule_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return 999
    end = text.index("---", 3)
    for line in text[3:end].splitlines():
        if line.strip().startswith("order:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
    return 999


def _rules_for_phase(phase_name: str) -> list[Path]:
    """Collect only cross-phase rules (no prefix) and rules for this exact phase.

    No accumulation — each phase gets its own rules plus cross-phase rules only.
    """
    prefix = _PHASE_TO_PREFIX.get(phase_name)
    if prefix is None:
        return []
    rules: list[Path] = []
    for artifact_dir in (_RULES_DIR / "domain", _RULES_DIR / "interaction-tree"):
        if not artifact_dir.exists():
            continue
        for rule_file in sorted(artifact_dir.glob("*.md")):
            has_prefix = False
            for known in _PHASE_PREFIXES:
                if rule_file.stem.startswith(known + "-"):
                    has_prefix = True
                    if known == prefix:
                        rules.append(rule_file)
                    break
            if not has_prefix:
                rules.append(rule_file)
    rules.sort(key=lambda r: (_parse_order(r), r.name))
    return rules


def build_phases() -> int:
    """Build phase files with baked-in rules into phases/built/."""
    if _BUILT_DIR.exists():
        shutil.rmtree(_BUILT_DIR)
    _BUILT_DIR.mkdir(parents=True)

    count = 0
    for phase_file in sorted(_PHASES_DIR.glob("*.md")):
        phase_name = phase_file.stem
        if phase_name in _CODE_PHASES:
            shutil.copy2(phase_file, _BUILT_DIR / phase_file.name)
            count += 1
            continue

        parts = [phase_file.read_text(encoding="utf-8").strip()]
        rules = _rules_for_phase(phase_name)
        if rules:
            domain_rules = [r for r in rules if r.parent.name == "domain"]
            interaction_rules = [r for r in rules if r.parent.name == "interaction-tree"]
            if domain_rules:
                parts.append(f"\n\n---\n\n## Domain Model Rules ({len(domain_rules)})\n")
                parts.append("Apply these rules when producing the domain model output for this phase.\n")
                for r in domain_rules:
                    parts.append(r.read_text(encoding="utf-8").strip())
                    parts.append("\n\n---\n")
            if interaction_rules:
                parts.append(f"\n\n## Interaction Tree Rules ({len(interaction_rules)})\n")
                parts.append("Apply these rules when producing the interaction tree output for this phase.\n")
                for r in interaction_rules:
                    parts.append(r.read_text(encoding="utf-8").strip())
                    parts.append("\n\n---\n")

        output = _BUILT_DIR / phase_file.name
        output.write_text("\n".join(parts) + "\n", encoding="utf-8")
        count += 1
        print(f"  {phase_name}: {len(rules)} rules")

    return count


def build_agents(skill_path: Path | None = None) -> Path:
    """Assemble pieces into AGENTS.md. Returns output path."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    content_dir = skill_path / "pieces"
    output_path = skill_path / "AGENTS.md"

    content_order = _CONTENT_ORDER
    config_path = skill_path / "conf" / "abd-config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            if "content_order" in data:
                content_order = data["content_order"]
        except (json.JSONDecodeError, KeyError):
            pass

    parts: list[str] = []
    for fname in content_order:
        p = content_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print("Building phase files...")
    n = build_phases()
    print(f"Built {n} phase files in {_BUILT_DIR}\n")

    out = build_agents()
    print(f"Wrote {out}")
