#!/usr/bin/env python3
"""Build AGENTS.md from pieces and build phase files with baked-in rules."""
import json
import re
import shutil
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PIECES_DIR = _SKILL_DIR / "pieces"
_PHASES_DIR = _PIECES_DIR / "phases"
_BUILT_DIR = _PHASES_DIR / "built"
_RULES_DIR = _SKILL_DIR / "rules"

sys.path.insert(0, str(_SKILL_DIR / "scripts"))
from _config import no_tree as _no_tree_from_config

_CONTENT_ORDER = [
    "introduction.md",
    "context_prep.md",
    "process.md",
    "critical_quality_steps.md",
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


def _rules_for_phase(phase_name: str, skip_tree: bool = False) -> list[Path]:
    """Collect only cross-phase rules (no prefix) and rules for this exact phase.

    No accumulation — each phase gets its own rules plus cross-phase rules only.
    When skip_tree is True, rules from the interaction-tree directory are excluded.
    """
    prefix = _PHASE_TO_PREFIX.get(phase_name)
    if prefix is None:
        return []
    artifact_dirs = [_RULES_DIR / "domain"]
    if not skip_tree:
        artifact_dirs.append(_RULES_DIR / "interaction-tree")
    rules: list[Path] = []
    for artifact_dir in artifact_dirs:
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


_TREE_LINE_PATTERNS = [
    re.compile(r"interaction_tree\.md", re.IGNORECASE),
    re.compile(r"interaction_model/", re.IGNORECASE),
    re.compile(r"^\*\*Interaction detail", re.IGNORECASE),
    re.compile(r"^###?\s+Interaction tree\s*$", re.IGNORECASE),
]

_TREE_INLINE_SUBS = [
    (re.compile(r"\s*and Interaction Tree Format", re.IGNORECASE), ""),
    (re.compile(r"Interaction Tree Format and\s*", re.IGNORECASE), ""),
    (re.compile(r"\s*and interaction tree", re.IGNORECASE), ""),
    (re.compile(r",?\s*interaction[_ ]tree\s*\([^)]*\)", re.IGNORECASE), ""),
    (re.compile(r"- examples: list of domain concept tables in interaction tree using this concept", re.IGNORECASE), ""),
    (re.compile(r'in interaction tree', re.IGNORECASE), "in domain model"),
    (re.compile(r'synchronized with interaction tree', re.IGNORECASE), "validated"),
    (re.compile(r'from the interaction tree', re.IGNORECASE), "from the domain model"),
    (re.compile(r',?\s*interaction tree structure', re.IGNORECASE), ""),
    (re.compile(r'Interaction Tree mapping', re.IGNORECASE), "Domain Model mapping"),
]


def _strip_tree_references(text: str) -> str:
    """Remove interaction-tree references from content."""
    lines = text.split("\n")
    filtered = []
    for line in lines:
        if any(p.search(line) for p in _TREE_LINE_PATTERNS):
            continue
        for pat, repl in _TREE_INLINE_SUBS:
            line = pat.sub(repl, line)
        filtered.append(line)
    return "\n".join(filtered)


def _clear_built_dir() -> None:
    """Clear built dir contents without rmtree (avoids Windows PermissionError when files are open)."""
    if not _BUILT_DIR.exists():
        return
    for p in _BUILT_DIR.iterdir():
        try:
            if p.is_file():
                p.unlink()
            else:
                shutil.rmtree(p)
        except OSError:
            pass  # skip locked files


def build_phases(no_tree: bool = False) -> int:
    """Build phase files with baked-in rules into phases/built/."""
    _BUILT_DIR.mkdir(parents=True, exist_ok=True)
    _clear_built_dir()

    count = 0
    for phase_file in sorted(_PHASES_DIR.glob("*.md")):
        phase_name = phase_file.stem
        if phase_name in _CODE_PHASES:
            shutil.copy2(phase_file, _BUILT_DIR / phase_file.name)
            count += 1
            continue

        phase_text = phase_file.read_text(encoding="utf-8").strip()
        if no_tree:
            phase_text = _strip_tree_references(phase_text)
        # Inject critical_quality_steps at the top of every AI phase
        quality_path = _PIECES_DIR / "critical_quality_steps.md"
        if not quality_path.exists():
            quality_path = _PIECES_DIR / "validation.md"
        if quality_path.exists():
            quality_steps = quality_path.read_text(encoding="utf-8").strip()
            parts = [quality_steps, f"\n\n---\n\n{phase_text}"]
        else:
            parts = [phase_text]
        # Inject domain model and interaction tree format specs after phase instructions, before rules
        domain_spec_path = _PIECES_DIR / "domain.md"
        if domain_spec_path.exists():
            domain_spec = domain_spec_path.read_text(encoding="utf-8").strip()
            parts.append(f"\n\n---\n\n# Domain Model Format\n\n{domain_spec}")
        tree_spec_path = _PIECES_DIR / "interaction_tree.md"
        if not no_tree and tree_spec_path.exists():
            tree_spec = tree_spec_path.read_text(encoding="utf-8").strip()
            parts.append(f"\n\n---\n\n# Interaction Tree Format\n\n{tree_spec}")
        rules = _rules_for_phase(phase_name, skip_tree=no_tree)
        if rules:
            domain_rules = [r for r in rules if r.parent.name == "domain"]
            interaction_rules = [r for r in rules if r.parent.name == "interaction-tree"]
            if domain_rules:
                parts.append(f"\n\n---\n\n## Domain Model Rules ({len(domain_rules)})\n")
                parts.append("Apply these rules when producing the domain model output for this phase.\n")
                for r in domain_rules:
                    rule_text = r.read_text(encoding="utf-8").strip()
                    if no_tree:
                        rule_text = _strip_tree_references(rule_text)
                    parts.append(rule_text)
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
        label = f"{phase_name}: {len(rules)} rules"
        if no_tree:
            label += " (no-tree)"
        print(f"  {label}")

    return count


def build_agents(skill_path: Path | None = None, no_tree: bool = False) -> Path:
    """Assemble pieces into AGENTS.md. Returns output path."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    content_dir = skill_path / "pieces"
    output_path = skill_path / "AGENTS.md"

    content_order = list(_CONTENT_ORDER)
    config_path = skill_path / "conf" / "abd-config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            if "content_order" in data:
                content_order = data["content_order"]
        except (json.JSONDecodeError, KeyError):
            pass

    if no_tree:
        content_order = [f for f in content_order if f != "interaction_tree.md"]

    parts: list[str] = []
    for fname in content_order:
        p = content_dir / fname
        if fname == "critical_quality_steps.md" and not p.exists():
            p = content_dir / "validation.md"  # fallback
        if p.exists():
            piece_text = p.read_text(encoding="utf-8").strip()
            if no_tree:
                piece_text = _strip_tree_references(piece_text)
            parts.append(piece_text)
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    no_tree = "--no-tree" in sys.argv or _no_tree_from_config()
    if no_tree:
        print("Mode: --no-tree (interaction tree disabled)\n")

    print("Building phase files...")
    n = build_phases(no_tree=no_tree)
    print(f"Built {n} phase files in {_BUILT_DIR}\n")

    out = build_agents(no_tree=no_tree)
    print(f"Wrote {out}")
