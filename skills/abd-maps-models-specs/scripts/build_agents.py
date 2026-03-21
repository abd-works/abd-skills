#!/usr/bin/env python3
"""Build AGENTS.md from parts/*.md and parts/steps/built/*.md. Step instructions use built files (base + rules); run build_steps.py first."""
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PARTS_DIR = _SKILL_DIR / "parts"
_STEPS_BUILT_DIR = _SKILL_DIR / "parts" / "steps" / "built"
_OUTPUT_PATH = _SKILL_DIR / "AGENTS.md"

# Prepended to every AI-step prompt bundle (see scripts/get_prompt_bundle.py --operation).
_PROMPT_BUNDLE_SHARED = ("process.md", "domain.md", "story-map.md", "context.md")

# Order: process overview first, then format specs, then step instructions
# Parts that have a built step: use steps/built/<step>.md when present
_CONTENT_ORDER = [
    "process.md",
    "domain.md",
    "story-map.md",
    "context.md",
    "modules-epics-foundational-spine.md",
    "modules-epics-scaffold-breadth.md",
    "concept-classification.md",
    "concept-classes-stories.md",
    "integrate-harmonize.md",
    "evidence.md",
    "structure.md",
    "finalize.md",
]

# Step instruction filenames: same name in parts/steps/built/ as in _CONTENT_ORDER (like solution modeler phases/built/)
_STEP_INSTRUCTION_FILES = frozenset({
    "modules-epics-foundational-spine.md",
    "modules-epics-scaffold-breadth.md",
    "concept-classification.md",
    "concept-classes-stories.md",
    "integrate-harmonize.md",
    "evidence.md",
    "structure.md",
    "finalize.md",
})


def ai_step_slugs() -> tuple[str, ...]:
    """Step ids for get_prompt_bundle --operation (no .md suffix)."""
    return tuple(sorted(f.removesuffix(".md") for f in _STEP_INSTRUCTION_FILES))


def _resolve_content_file(skill_path: Path, fname: str) -> Path | None:
    """Same resolution as build_agents: built step > steps > parts."""
    parts_dir = skill_path / "parts"
    steps_dir = skill_path / "parts" / "steps"
    built_dir = skill_path / "parts" / "steps" / "built"
    if fname in _STEP_INSTRUCTION_FILES:
        if (built_dir / fname).exists():
            return built_dir / fname
        if (steps_dir / fname).exists():
            return steps_dir / fname
        p = parts_dir / fname
        return p if p.exists() else None
    p = parts_dir / fname
    return p if p.exists() else None


def _normalize_part_links_for_stdout(content: str) -> str:
    """Normalize relative links so a pasted bundle reads like AGENTS.md (paths from skill root)."""
    content = content.replace("](../../process.md)", "](parts/process.md)")
    content = content.replace("](../process.md)", "](parts/process.md)")
    content = content.replace("](context.md)", "](parts/context.md)")
    content = content.replace("](steps/built/", "](parts/steps/built/")
    for s in (
        "modules-epics-foundational-spine",
        "modules-epics-scaffold-breadth",
        "concept-classification",
        "concept-classes-stories",
        "integrate-harmonize",
        "evidence",
        "structure",
        "finalize",
    ):
        content = content.replace(f"]({s}.md)", f"](parts/steps/built/{s}.md)")
    return content


def assemble_prompt_bundle(skill_path: Path | None, step_slug: str) -> str:
    """Concatenate shared parts + one step built file (same sources as AGENTS.md, minus other steps)."""
    skill_path = (skill_path or _SKILL_DIR).resolve()
    step_fname = f"{step_slug}.md"
    if step_fname not in _STEP_INSTRUCTION_FILES:
        known = ", ".join(ai_step_slugs())
        raise ValueError(f"Unknown operation {step_slug!r}. Expected one of: {known}")

    sections: list[str] = []
    banner = (
        "<!-- Prompt bundle: process + domain + story-map + context + one built step. "
        "Assembled by scripts/get_prompt_bundle.py via build_agents.assemble_prompt_bundle -->\n\n"
    )
    sections.append(banner)

    order = list(_PROMPT_BUNDLE_SHARED) + [step_fname]
    for fname in order:
        p = _resolve_content_file(skill_path, fname)
        if p is None:
            raise FileNotFoundError(f"Missing file for bundle: {fname} (under {skill_path})")
        body = p.read_text(encoding="utf-8").strip()
        body = _normalize_part_links_for_stdout(body)
        sections.append(f"## {fname}\n\n{body}")

    return "\n\n---\n\n".join(sections).rstrip() + "\n"


def build_agents(skill_path: Path | None = None) -> Path:
    """Assemble parts and steps/built into AGENTS.md. Returns output path."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    parts_dir = skill_path / "parts"
    steps_dir = skill_path / "parts" / "steps"
    built_dir = steps_dir / "built"
    output_path = skill_path / "AGENTS.md"

    parts: list[str] = []
    for fname in _CONTENT_ORDER:
        p = _resolve_content_file(skill_path, fname)
        if p is not None:
            content = p.read_text(encoding="utf-8").strip()
            content = _normalize_part_links_for_stdout(content)
            parts.append(content)
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]

    # Production style: explicit generated-file provenance (do not hand-edit; single rebuild entry point)
    banner = (
        "<!--\n"
        "  AGENTS.md — GENERATED FILE. Do not edit by hand.\n"
        "  Assembled from: parts/*.md and parts/steps/built/*.md (see scripts/build_agents.py).\n"
        "  Regenerate: python scripts/build.py  (from skills/abd-maps-models-specs)\n"
        "-->\n\n"
        "> **Generated document.** This file is built from `parts/` and `parts/steps/built/`. "
        "Edit step sources under `parts/steps/<name>.md` or top-level parts, run `python scripts/build.py`, "
        "then use this file as the agent instruction bundle.\n\n"
        "---\n\n"
    )
    text = banner + text
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    out = build_agents()
    print(f"Wrote {out}")
