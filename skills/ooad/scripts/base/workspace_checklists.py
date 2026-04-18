"""
Ensure live workflow checklists under active_skill_workspace/<skill_name>/progress/.

**Normative rules** (strategy vs ticks, layers, revisits, flags) live only in the skill repo:
``content/parts/library/strategy-execution-and-checklists.md``. That file is authored; this module
never writes it and ``generate.py`` does not create it.

**Workspace routing** (``skill_name``, ``active_skill_workspace``, path resolution):
``content/parts/library/base/workspace-and-config.md``.

**This module creates** (when missing, on ``generate.py --phase <slug> [--slice <id>]``):

- ``README.md`` — from ``templates/progress-README.md`` when present (explains the tree).
- ``strategy-run-checklist.md`` — from ``templates/strategy-run-checklist.md`` when present (vs ``strategy.md``).
- ``slices/<slice-id>/<phase-slug>-checklist.md`` — steps from ``## Action Checklist`` in ``phases/<slug>.md``.
  **Slice IDs** match **strategy.md** §1; default CLI slice is ``main`` for single-slice engagements.
- ``process-checklist.md`` — legacy: one box per ``phase_files`` slug.

Does not overwrite existing files.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skill import Skill


def _parts_dir(skill_path: Path) -> Path:
    p = skill_path / "content" / "parts"
    if (p / "process.md").is_file():
        return p
    return skill_path / "parts"


def progress_dir(workspace: Path, skill_name: str) -> Path:
    """Live checklists root: ``<active_skill_workspace>/<skill_name>/progress``."""
    return workspace / skill_name / "progress"


def sanitize_slice_id(raw: str) -> str:
    """Safe folder name under progress/slices/. Defaults to main if empty or invalid."""
    s = (raw or "").strip()
    if not s:
        return "main"
    parts: list[str] = []
    for c in s:
        if c.isalnum() or c in "-_":
            parts.append(c)
        elif c in " /":
            parts.append("-")
    slug = "".join(parts).strip("-")
    if not slug:
        return "main"
    return slug[:120]


def extract_action_checklist_lines(phase_body: str) -> list[str]:
    """Return markdown task lines under ``## Action Checklist``, else all task lines in file."""
    lines = phase_body.splitlines()
    start: int | None = None
    heading = re.compile(r"^##\s+Action Checklist\s*$", re.IGNORECASE)
    for i, line in enumerate(lines):
        if heading.match(line.strip()):
            start = i + 1
            break
    task_re = re.compile(r"^\s*-\s*\[[ xX]\]\s*")
    if start is not None:
        out: list[str] = []
        for line in lines[start:]:
            if line.startswith("## ") and not line.startswith("###"):
                break
            if task_re.match(line):
                out.append(line.strip())
        if out:
            return out
    return [ln.strip() for ln in lines if task_re.match(ln)]


def render_process_checklist(
    skill_name: str,
    phase_files: tuple[str, ...],
    phase_section_headings: dict[str, str],
) -> str:
    """Markdown body for ``process-checklist.md``."""
    lines = [
        f"# Pipeline — {skill_name}",
        "",
        "Live workflow position. **Resume at the first unchecked phase.**",
        "",
        "This file is created when you run `python scripts/base/generate.py --phase <slug>` and it did not "
        "exist yet. Tick boxes **here** only — not in `content/parts/process.md`.",
        "",
    ]
    for slug in phase_files:
        title = phase_section_headings.get(slug) or slug.replace("-", " ").title()
        lines.append(f"- [ ] **{slug}** — {title}")
    lines.append("")
    return "\n".join(lines)


def render_phase_checklist(
    skill_name: str, slug: str, task_lines: list[str], slice_id: str
) -> str:
    """Markdown body for ``slices/<slice-id>/<slug>-checklist.md``."""
    src = f"`content/parts/phases/{slug}.md`"
    lines = [
        f"# Live checklist — {slug} — slice `{slice_id}`",
        "",
        f"**Normative steps** live under **## Action Checklist** in {src}. "
        "Track progress **here**; do not tick boxes in the repo copy.",
        "",
        f"**Skill:** {skill_name}",
        "",
        "---",
        "",
    ]
    if not task_lines:
        lines.extend(
            [
                "*No `- [ ]` lines were found under ## Action Checklist in the phase file.*",
                "*Add steps to the phase doc, then delete this file and re-run "
                "`python scripts/base/generate.py --phase "
                f"{slug} --slice {slice_id}` to regenerate.*",
                "",
            ]
        )
    else:
        for t in task_lines:
            # Normalize to unchecked for a fresh file
            t2 = re.sub(r"^-\s*\[[xX ]\]", "- [ ]", t, count=1)
            lines.append(t2)
        lines.append("")
    return "\n".join(lines)


def ensure_progress_readme(skill_path: Path, workspace: Path, skill_name: str) -> Path | None:
    """Copy templates/progress-README.md to progress/README.md when missing."""
    tpl = skill_path / "templates" / "progress-README.md"
    if not tpl.is_file():
        return None
    prog = progress_dir(workspace, skill_name)
    prog.mkdir(parents=True, exist_ok=True)
    out = prog / "README.md"
    if out.is_file():
        return None
    out.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
    return out


def ensure_strategy_run_checklist(skill_path: Path, workspace: Path, skill_name: str) -> Path | None:
    """
    If the skill ships ``templates/strategy-run-checklist.md``, copy it to
    ``progress/strategy-run-checklist.md`` when that file is missing.
    """
    tpl = skill_path / "templates" / "strategy-run-checklist.md"
    if not tpl.is_file():
        return None
    prog = progress_dir(workspace, skill_name)
    prog.mkdir(parents=True, exist_ok=True)
    out = prog / "strategy-run-checklist.md"
    if out.is_file():
        return None
    out.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
    return out


def ensure_workspace_checklists(
    skill: "Skill", phase_slug: str, slice_id: str = "main"
) -> tuple[Path | None, Path | None]:
    """
    If ``active_skill_workspace`` is set, create missing files under ``progress/`` (see module docstring).
    Normative documentation is not emitted here — only workspace checklist markdown.

    Phase action checklists are written to ``progress/slices/<slice-id>/<phase>-checklist.md``.

    Returns ``(process_path_or_none, phase_path_or_none)`` for paths written this call.
    """
    wp = skill.instructions.context.workspace_path
    if not wp:
        return None, None
    workspace = Path(wp)
    cfg = skill.skill_config
    skill_name = str(cfg.get("name") or skill.path.name).strip() or "skill"
    phase_files: tuple[str, ...] = tuple(cfg.get("phase_files") or ())
    headings: dict[str, str] = dict(cfg.get("phase_section_headings") or {})

    sid = sanitize_slice_id(slice_id)

    prog = progress_dir(workspace, skill_name)
    prog.mkdir(parents=True, exist_ok=True)

    written_process: Path | None = None
    written_phase: Path | None = None

    p_process = prog / "process-checklist.md"
    if not p_process.is_file() and phase_files:
        p_process.write_text(
            render_process_checklist(skill_name, phase_files, headings),
            encoding="utf-8",
        )
        written_process = p_process

    phase_path = _parts_dir(skill.path) / "phases" / f"{phase_slug}.md"
    body = phase_path.read_text(encoding="utf-8") if phase_path.is_file() else ""
    tasks = extract_action_checklist_lines(body)

    slice_dir = prog / "slices" / sid
    slice_dir.mkdir(parents=True, exist_ok=True)
    p_phase = slice_dir / f"{phase_slug}-checklist.md"
    if not p_phase.is_file():
        p_phase.write_text(
            render_phase_checklist(skill_name, phase_slug, tasks, sid),
            encoding="utf-8",
        )
        written_phase = p_phase

    ensure_progress_readme(skill.path, workspace, skill_name)
    ensure_strategy_run_checklist(skill.path, workspace, skill_name)

    return written_process, written_phase
