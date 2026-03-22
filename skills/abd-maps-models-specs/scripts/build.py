#!/usr/bin/env python3
"""
Skill build (see abd-skill-builder/docs/documentation-standards.md):

1. Merge content/parts/process.md + content/parts/phases/*.md → content/built/agents-staged.md
   (staged: link-rewritten; operator preamble removed from merged output; first # in each file
   demoted to ## under AGENTS).
2. Write AGENTS.md = one title line + same body as staged (no second H1 for "Process").
3. Write content/built/phases/<phase>.md for each phase: operator role + rules/*.md (filtered by YAML
   phase_files / every_phase) + library inlines + phase body (operator block stripped) + **Critical quality steps**
   (from `content/parts/library/critical-quality-steps.md` plus optional per-phase notes). See PHASE_LIBRARY,
   PHASE_CRITICAL_QUALITY_NOTES; see rules/README.md for rule authoring.
4. Run pipeline scripts: Phase 0 → validate context contract → Phase 2 → validate Phase 3 →
   optional map-model-spec chunk scanner → bundle manifest.

Source phase files still contain the full operator block (sync_operator_preamble.py). AGENTS.md points to
operator-role.md once via process.md and does not repeat the preamble per phase.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PARTS = ROOT / "content" / "parts"
PARTS_LIBRARY = PARTS / "library"
RULES_DIR = ROOT / "rules"
BUILT = ROOT / "content" / "built"
BUILT_PHASES = BUILT / "phases"

# Order matches process.md — descriptive slugs only (order is here, not in filenames).
PHASE_FILES = [
    "context-readiness.md",
    "canonical-context.md",
    "terms-mechanisms.md",
    "story-map.md",
    "domain-types.md",
    "variant-classification.md",
    "deepen.md",
    "integrate.md",
    "validate-render.md",
]

# Library markdown (under content/parts/library/) to inline into each built phase bundle for injection / EA context.
PHASE_LIBRARY: dict[str, list[str]] = {
    "context-readiness.md": [
        "principles-and-rules.md",
        "execution-and-success.md",
        "pipeline_invariants.md",
        "context-corpus.md",
    ],
    "canonical-context.md": [
        "principles-and-rules.md",
        "context-package.md",
        "context-corpus.md",
    ],
    "terms-mechanisms.md": [
        "terms-mechanisms-contract.md",
        "pipeline_invariants.md",
        "principles-and-rules.md",
    ],
    "story-map.md": [
        "behavioral-story-map.md",
        "story-map-narrative.md",
        "why-story-mapping-first.md",
    ],
    "domain-types.md": [
        "domain-model.md",
        "terms-mechanisms-contract.md",
    ],
    "variant-classification.md": [
        "domain-model.md",
        "pipeline_invariants.md",
    ],
    "deepen.md": [
        "domain-model.md",
        "terms-mechanisms-contract.md",
    ],
    "integrate.md": [
        "domain-model.md",
        "pipeline_invariants.md",
        "execution-and-success.md",
    ],
    "validate-render.md": [
        "principles-and-rules.md",
        "pipeline_invariants.md",
        "execution-and-success.md",
    ],
}

# Short focus lines appended after `critical-quality-steps.md` in each built bundle (phase filename key).
PHASE_CRITICAL_QUALITY_NOTES: dict[str, str] = {
    "context-readiness.md": (
        "**Focus (this phase):** Phase 0 readiness audit only — metrics, samples, adopt/extend/rebuild. "
        "No terms layer, no story map. Re-run **`validate_context_contract.py`** once `context_index.json` exists."
    ),
    "canonical-context.md": (
        "**Focus (this phase):** Phase 1 frozen package — chunks, `context_index.json`, manifest. "
        "Hard gate: **`validate_context_contract.py`** when the index is present."
    ),
    "terms-mechanisms.md": (
        "**Focus (this phase):** Phase 2 terms/mechanisms — every substantive row cites **`chunk_id`** per contract. "
        "No promoted `concepts[]` yet."
    ),
    "story-map.md": (
        "**Focus (this phase):** Phase 3 **`mm3_story_map.json`** — behavioral stories, **`evidence_chunk_ids[]`**, "
        "validator **`validate_phase3_story_map.py`**. Read **`behavioral-story-map.md`** + rule **`behavioral-story-shape`**."
    ),
    "domain-types.md": (
        "**Focus (this phase):** Phase 4 sparse types — promotion bar, **owns**, evidence; story map precedes types "
        "(rule **`story-map-before-domain-types`**)."
    ),
    "variant-classification.md": (
        "**Focus (this phase):** Phase 5 variant representation — explicit per-family decisions **before** deep property work "
        "(rule **`variant-decisions-before-deepen`**)."
    ),
    "deepen.md": (
        "**Focus (this phase):** Phase 6 deepen — responsibilities, `depends_on`, no anemic/god concepts; "
        "approved tooling only (rule **`deepen-approved-tools-only`**)."
    ),
    "integrate.md": (
        "**Focus (this phase):** Phase 7 integrate — one coherent map/model/spec; drain candidate queue; "
        "cross-cutting resolved or deferred in writing."
    ),
    "validate-render.md": (
        "**Focus (this phase):** Phase 8 gates — **`build.py`** pipeline, **`chunks_must_be_referenced.py`**, "
        "manifest, reproducible reports. Render traces to validated artifacts."
    ),
}

CRITICAL_QUALITY_LIBRARY = "critical-quality-steps.md"


def parse_rule_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter (subset: rule_id, every_phase, phase_files list). Returns (meta, body)."""
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    fm = raw[3:end]
    body = raw[end + 4 :].lstrip("\n")
    meta: dict[str, Any] = {}
    phase_files: list[str] = []
    in_phase_list = False
    for line in fm.splitlines():
        s = line.strip()
        if s.startswith("rule_id:"):
            in_phase_list = False
            meta["rule_id"] = s[8:].strip()
        elif s.startswith("every_phase:"):
            in_phase_list = False
            meta["every_phase"] = s[12:].strip().lower() in ("true", "yes", "1")
        elif s.startswith("phase_files:"):
            rest = line.split(":", 1)[1].strip()
            if rest:
                for part in rest.split(","):
                    p = part.strip()
                    if p:
                        phase_files.append(p)
                in_phase_list = False
            else:
                in_phase_list = True
        elif in_phase_list and s.startswith("- "):
            phase_files.append(s[2:].strip())
    if phase_files:
        meta["phase_files"] = phase_files
    return meta, body


def rule_applies_to_phase(meta: dict[str, Any], phase_fname: str) -> bool:
    if meta.get("every_phase"):
        return True
    phases = meta.get("phase_files") or []
    return phase_fname in phases


def load_rule_files_for_phase(phase_fname: str) -> list[tuple[str, str]]:
    """Rule filename + body (frontmatter stripped) for this phase bundle only."""
    out: list[tuple[str, str]] = []
    if not RULES_DIR.is_dir():
        return out
    for rp in sorted(RULES_DIR.glob("*.md")):
        if rp.name.lower() == "readme.md":
            continue
        raw = rp.read_text(encoding="utf-8")
        meta, body = parse_rule_frontmatter(raw)
        if not rule_applies_to_phase(meta, phase_fname):
            continue
        if not meta.get("phase_files") and not meta.get("every_phase"):
            print(
                f"Warning: rules/{rp.name} has no phase_files / every_phase — skipped. "
                "Set YAML frontmatter (see rules/README.md).",
                flush=True,
            )
            continue
        body = body.strip() + "\n"
        if not body.strip():
            continue
        out.append((rp.name, body))
    return out


def demote_all_headings(md: str, extra_levels: int = 2) -> str:
    """Prefix each markdown heading line with extra # so inlined docs nest under section headers."""
    prefix = "#" * extra_levels
    lines: list[str] = []
    for line in md.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            idx = len(line) - len(stripped)
            lines.append(line[:idx] + prefix + stripped)
        else:
            lines.append(line)
    return "".join(lines)


def rewrite_links_for_agents_md(md: str) -> str:
    """Paths relative to skill root (AGENTS.md and agents-staged.md location)."""
    md = md.replace("../../../docs/", "docs/")
    md = md.replace("../../docs/", "docs/")
    md = md.replace("](../process.md)", "](content/parts/process.md)")
    md = md.replace("](operator-role.md)", "](content/parts/operator-role.md)")
    md = md.replace("](../operator-role.md)", "](content/parts/operator-role.md)")
    md = md.replace("](phases/", "](content/parts/phases/")
    for fname in PHASE_FILES:
        md = md.replace(f"]({fname})", f"](content/parts/phases/{fname})")
    return md


def rewrite_links_for_phase_bundle(md: str) -> str:
    """Links in bundle files live under content/built/phases/ — adjust skill-root paths."""
    md = rewrite_links_for_agents_md(md)
    md = md.replace("](content/parts/", "](../../parts/")
    md = md.replace("](../content/parts/", "](../../parts/")
    md = md.replace("](docs/", "](../../../docs/")
    return md


def demote_first_h1_to_h2(md: str) -> str:
    """Demote the first # heading to ## so content nests under # AGENTS — …"""
    lines = md.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            indent = line[: len(line) - len(stripped)]
            lines[i] = indent + "## " + stripped[2:]
            break
    return "".join(lines)


def strip_operator_block_for_agents(text: str) -> str:
    """Remove operator preamble (markers + body) from merged agent output. Phase source files unchanged."""
    return re.sub(
        r"<!-- operator-role:start -->.*?<!-- operator-role:end -->\s*",
        "",
        text,
        flags=re.DOTALL,
    )


def merge_agents_staged_body() -> str:
    """Single merged body: process + phases, ready for AGENTS.md and content/built/agents-staged.md."""
    process_path = PARTS / "process.md"
    if not process_path.is_file():
        raise FileNotFoundError(f"Missing {process_path}")

    proc = process_path.read_text(encoding="utf-8")
    proc = demote_first_h1_to_h2(proc)
    proc = rewrite_links_for_agents_md(proc)

    chunks: list[str] = [proc.rstrip(), "\n"]
    phases_dir = PARTS / "phases"

    for fname in PHASE_FILES:
        p = phases_dir / fname
        if not p.is_file():
            raise FileNotFoundError(f"Missing phase file: {p}")
        body = p.read_text(encoding="utf-8")
        body = strip_operator_block_for_agents(body)
        body = body.strip() + "\n"
        body = demote_first_h1_to_h2(body)
        body = rewrite_links_for_agents_md(body)
        chunks.append("\n\n---\n\n")
        chunks.append(body)

    return "".join(chunks)


def critical_quality_section_for_phase(phase_fname: str) -> str:
    """Shared library + optional per-phase focus (markdown), headings demoted for nesting under ## Critical quality steps."""
    cq_path = PARTS_LIBRARY / CRITICAL_QUALITY_LIBRARY
    if not cq_path.is_file():
        raise FileNotFoundError(f"Missing {cq_path}")
    cq = demote_all_headings(cq_path.read_text(encoding="utf-8"), 2)
    note = (PHASE_CRITICAL_QUALITY_NOTES.get(phase_fname) or "").strip()
    if note:
        return cq.rstrip() + "\n\n" + note + "\n"
    return cq


def write_phase_bundles() -> None:
    """Emit content/built/phases/<same-as-source>.md: role + rules + library + phase steps + critical quality."""
    BUILT_PHASES.mkdir(parents=True, exist_ok=True)
    operator_path = PARTS / "operator-role.md"
    if not operator_path.is_file():
        raise FileNotFoundError(f"Missing {operator_path}")
    op = operator_path.read_text(encoding="utf-8")
    op = demote_all_headings(op, 2)

    phases_dir = PARTS / "phases"
    for fname in PHASE_FILES:
        p = phases_dir / fname
        if not p.is_file():
            raise FileNotFoundError(f"Missing phase file: {p}")
        phase_body = strip_operator_block_for_agents(p.read_text(encoding="utf-8"))
        phase_body = phase_body.strip() + "\n"
        phase_body = demote_all_headings(phase_body, 2)

        lib_chunks: list[str] = []
        for lib in PHASE_LIBRARY.get(fname, []):
            lp = PARTS_LIBRARY / lib
            if not lp.is_file():
                raise FileNotFoundError(f"Missing library file for phase {fname}: {lp}")
            lib_text = demote_all_headings(lp.read_text(encoding="utf-8"), 2)
            lib_chunks.append(f"### `{lib}`\n\n{lib_text}")

        rules = load_rule_files_for_phase(fname)
        rules_section: str
        if rules:
            rules_section = "\n\n".join(
                f"### `{name}`\n\n{demote_all_headings(text, 2)}" for name, text in rules
            )
        else:
            rules_section = (
                "*No rules mapped to this phase in `rules/*.md`. "
                "Each rule file must declare `phase_files:` (or `every_phase: true`) in YAML frontmatter — see `rules/README.md`.*"
            )

        lib_section = (
            "\n\n".join(lib_chunks)
            if lib_chunks
            else "*No library files listed for this phase in `PHASE_LIBRARY` (see `scripts/build.py`).*"
        )

        cq_block = critical_quality_section_for_phase(fname)

        slug = fname[:-3]
        parts: list[str] = [
            "<!-- Generated by scripts/build.py — do not edit by hand. -->\n\n",
            f"# Built phase bundle — {slug}\n\n",
            "Single-phase context for injection: **operator role**, **rules**, **library** excerpts, "
            "**phase steps** (operator preamble removed), then **critical quality steps** "
            f"(`content/parts/library/{CRITICAL_QUALITY_LIBRARY}` + phase focus).\n\n",
            "## Operator role\n\n",
            op,
            "\n\n## Rules\n\n",
            rules_section,
            "\n\n## Library\n\n",
            lib_section,
            "\n\n## Phase steps (normative)\n\n",
            phase_body,
            "\n\n## Critical quality steps\n\n",
            cq_block,
        ]
        body = rewrite_links_for_phase_bundle("".join(parts))
        out_path = BUILT_PHASES / fname
        out_path.write_text(body, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)}", flush=True)

    readme = BUILT_PHASES / "README.md"
    readme.write_text(
        "# Built phase bundles (`content/built/phases/`)\n\n"
        "Each file mirrors the source name under `content/parts/phases/` and is generated by **`scripts/build.py`**. "
        "Do not edit by hand.\n\n"
        "Every bundle contains:\n\n"
        "1. **Operator role** — full text from `content/parts/operator-role.md` (headings demoted to nest under this section).\n"
        "2. **Rules** — `rules/*.md` whose YAML **`phase_files`** includes this phase (or **`every_phase: true`**), inlined under nested headings.\n"
        "3. **Library** — phase-specific excerpts from `content/parts/library/` as configured in **`PHASE_LIBRARY`** in `scripts/build.py`.\n"
        "4. **Phase steps** — the phase markdown with the operator preamble block removed (same strip as the `AGENTS.md` merge).\n"
        "5. **Critical quality steps** — `content/parts/library/critical-quality-steps.md` (normative advice + mechanical checks + review) plus optional **focus** lines from **`PHASE_CRITICAL_QUALITY_NOTES`** in `scripts/build.py`.\n\n"
        "Use these files when you need **one** self-contained phase context (e.g. EA / agent injection) instead of the full `AGENTS.md` merge.\n\n"
        "**Customizing:** Add or change which library files attach to which phase by editing the **`PHASE_LIBRARY`** map in **`scripts/build.py`**. "
        "Edit **`rules/*.md`** and set **`phase_files`** / **`every_phase`** in frontmatter (see **`rules/README.md`**).\n\n"
        "**Links:** Bundle link rewriting fixes paths to `content/parts/...` and `docs/...` for navigation from `content/built/phases/`. "
        "Inlined library markdown may still use **same-folder** links between library files (e.g. `(context-package.md)`); "
        "resolve those against `content/parts/library/` when following links from a bundle file.\n",
        encoding="utf-8",
    )
    print(f"Wrote {readme.relative_to(ROOT)}", flush=True)


def write_built_and_agents() -> None:
    BUILT.mkdir(parents=True, exist_ok=True)
    body = merge_agents_staged_body()

    staged_path = BUILT / "agents-staged.md"
    staged_path.write_text(
        "<!-- Generated by scripts/build.py — do not edit by hand. -->\n\n"
        "# Staged agent bundle\n\n"
        "Intermediate merge (process + phases, operator blocks stripped). "
        "Same markdown body as `AGENTS.md` below the title line.\n\n"
        "---\n\n"
        + body,
        encoding="utf-8",
    )
    print(f"Wrote {staged_path.relative_to(ROOT)}", flush=True)

    agents_path = ROOT / "AGENTS.md"
    agents_path.write_text(
        "# AGENTS — abd-maps-models-specs\n\n" + body,
        encoding="utf-8",
    )
    print(f"Wrote {agents_path.relative_to(ROOT)}", flush=True)

    write_phase_bundles()


def _run(name: str) -> None:
    path = SCRIPTS / name
    print(f"--- {name} ---")
    subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=True)


def main() -> None:
    write_built_and_agents()
    _run("phase0_context_audit.py")
    _run("validate_context_contract.py")
    _run("build_phase2_artifacts.py")
    _run("validate_phase3_story_map.py")
    _run("scanners/chunks_must_be_referenced.py")
    _run("generate_context_bundle_manifest.py")
    _run("test_rule_examples.py")
    print("build.py: done")


if __name__ == "__main__":
    main()
