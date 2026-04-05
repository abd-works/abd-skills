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

# Concept-anchored pipeline phases (must match pipeline.py)
_PHASES = [
    "normalize", "configure_concept_extraction_parameters", "concept_extraction", "concept_index",
    "concept_synthesis",
    "evidence_extraction", "evidence_index", "structure", "behavior", "variation",
    "consolidate", "assess", "finalize",
]

_CODE_PHASES = {"normalize", "concept_index", "evidence_extraction", "evidence_index"}

# Phases that produce config/hypothesis only — no domain model, no interaction tree.
# Build injects only the phase content; no critical_quality_steps, domain spec, interaction spec, or rules.
_PHASES_PHASE_ONLY = {"configure_concept_extraction_parameters"}

# Phases that should keep quality steps and rules, but should NOT inject
# domain/solution/interaction format spec files into the built phase prompt.
_PHASES_NO_FORMAT_SPECS = {"concept_synthesis"}

# Phase -> (label, output_file) for generated rules section
_GENERATED_OUTPUT = {
    "concept_synthesis": ("Hypothesis", "hypothesis.json"),
    "concept_extraction": ("Extraction Config", "extraction_config.json"),
    "assess": ("Assessment", "assessment.json"),
}
_DEFAULT_GENERATED_OUTPUT = ("Solution Model", "solution_model.json")


def _generated_output_for_phase(phase_name: str) -> tuple[str, str]:
    return _GENERATED_OUTPUT.get(phase_name, _DEFAULT_GENERATED_OUTPUT)


from _rules import rules_for_phase as _rules_for_phase


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
    for phase_name in _PHASES:
        phase_file = _PHASES_DIR / f"{phase_name}.md"
        if not phase_file.exists():
            continue
        if phase_name in _CODE_PHASES:
            shutil.copy2(phase_file, _BUILT_DIR / f"{phase_name}.md")
            count += 1
            continue

        phase_text = phase_file.read_text(encoding="utf-8").strip()
        if phase_name in _PHASES_PHASE_ONLY:
            if no_tree:
                phase_text = _strip_tree_references(phase_text)
            (_BUILT_DIR / f"{phase_name}.md").write_text(phase_text + "\n", encoding="utf-8")
            count += 1
            print(f"  {phase_name}: phase-only (no domain, interaction, quality)")
            continue

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
        # Inject format specs after phase instructions, before rules
        if phase_name not in _PHASES_NO_FORMAT_SPECS:
            solution_model_phases = {"structure", "behavior", "variation", "consolidate", "assess", "finalize"}
            if phase_name in solution_model_phases:
                solution_spec_path = _PIECES_DIR / "solution_model.md"
                if solution_spec_path.exists():
                    solution_spec = solution_spec_path.read_text(encoding="utf-8").strip()
                    parts.append(f"\n\n---\n\n# Solution Model Format\n\n{solution_spec}")
            else:
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
            generated_rules = [r for r in rules if r.parent.name == "generated"]
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
            if generated_rules:
                out_label, out_file = _generated_output_for_phase(phase_name)
                parts.append(f"\n\n## {out_label} Rules ({len(generated_rules)})\n")
                parts.append(f"Apply these rules when producing {out_file} for this phase.\n")
                for r in generated_rules:
                    rule_text = r.read_text(encoding="utf-8").strip()
                    if no_tree:
                        rule_text = _strip_tree_references(rule_text)
                    parts.append(rule_text)
                    parts.append("\n\n---\n")

        output = _BUILT_DIR / f"{phase_name}.md"
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
    config_path = skill_path / "skill-config.json"
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
