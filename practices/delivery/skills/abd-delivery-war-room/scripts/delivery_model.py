#!/usr/bin/env python3
"""Shared delivery model: system of work, run catalog, run state, slot generation.

**Owned by delivery-lead + skills** — not by sync_kanban_board.py or the Kanban UI.

Machine files live under `<workspace>/docs/planning/delivery-war-room/`:

  - `system-of-work.json` — named stage + skill orders (and optional parallel profiles)
  - `run-catalog.json` — planned runs (scope, stages, system-of-work ref); no slot rows
  - `run-state.json` — runtime: which runs have materialized slots, next slot id

Legacy plan slot-table parsing was removed. **`run-catalog.json`** and **`run-state.json`** are required.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from slot_paths import find_slot_start, max_existing_slot_id, slot_path_for

STAGE_ORDER = ["shaping", "discovery", "exploration", "specification", "engineering"]

SLOT_START_TEMPLATE = """# Slot {slot_id:03d} — Start ({run_title} — {skill_label} {slot_type})

```yaml
team-role: {team_role}
slot_type: {slot_type}
workspace: {workspace}
run: "{run_title}"
ticket_run: {run_num}
stage: {stage}
depends_on:
{depends_on_yaml}
run_scope: {run_scope}
skills:
{skills_yaml}
{prior_executor_line}checkpoint: {checkpoint}
entry_conditions_met:
  - Generated from system-of-work `{system_of_work}` at run open
```

{body_notes}

Write `slot-{slot_id:03d}-finished.md`.
"""


@dataclass
class SkillStep:
    skill: str
    role: str
    label: str = ""


@dataclass
class SystemOfWork:
    name: str
    label: str = ""
    source_strategy: str = ""
    stages: dict[str, list[SkillStep]] = field(default_factory=dict)
    parallel_profiles: dict[str, dict[str, list[str]]] = field(default_factory=dict)


@dataclass
class RunCatalogEntry:
    run: int
    title: str
    scope: str = ""
    stages: list[str] = field(default_factory=list)
    system_of_work: str = ""
    discovery_precompleted: bool = False
    waived_skills: dict[str, list[str]] = field(default_factory=dict)
    opens_after: dict[str, Any] = field(default_factory=dict)
    parallel_profile: str = ""
    status: str = "planned"


@dataclass
class RunMeta:
    run: int
    title: str
    first_slot: int | None = None
    last_slot: int | None = None
    stages: list[str] = field(default_factory=list)
    system_of_work: str = ""
    discovery_precompleted: bool = False
    slots_generated: bool = False


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def war_room_dir(workspace: Path) -> Path:
    return workspace / "docs" / "planning" / "delivery-war-room"


def load_system_of_work(workspace: Path) -> dict[str, SystemOfWork]:
    path = war_room_dir(workspace) / "system-of-work.json"
    if not path.is_file():
        return {}
    raw = _read_json(path)
    out: dict[str, SystemOfWork] = {}
    for name, block in raw.get("definitions", {}).items():
        stages: dict[str, list[SkillStep]] = {}
        for stage_id, skills in (block.get("stages") or {}).items():
            steps: list[SkillStep] = []
            for item in skills:
                steps.append(
                    SkillStep(
                        skill=str(item["skill"]),
                        role=str(item["role"]),
                        label=str(item.get("label", item["skill"])),
                    )
                )
            stages[stage_id] = steps
        out[name] = SystemOfWork(
            name=name,
            label=str(block.get("label", name)),
            source_strategy=str(block.get("source_strategy", "")),
            stages=stages,
            parallel_profiles=block.get("parallel_profiles") or {},
        )
    return out


def load_run_catalog(workspace: Path) -> list[RunCatalogEntry]:
    path = war_room_dir(workspace) / "run-catalog.json"
    if not path.is_file():
        return []
    raw = _read_json(path)
    entries: list[RunCatalogEntry] = []
    for item in raw.get("runs", []):
        entries.append(
            RunCatalogEntry(
                run=int(item["run"]),
                title=str(item["title"]),
                scope=str(item.get("scope", "")),
                stages=list(item.get("stages") or []),
                system_of_work=str(item.get("system_of_work", "")),
                discovery_precompleted=bool(item.get("discovery_precompleted")),
                waived_skills=dict(item.get("waived_skills") or {}),
                opens_after=dict(item.get("opens_after") or {}),
                parallel_profile=str(item.get("parallel_profile", "")),
                status=str(item.get("status", "planned")),
            )
        )
    return sorted(entries, key=lambda e: e.run)


def load_run_state(workspace: Path) -> dict[str, Any]:
    path = war_room_dir(workspace) / "run-state.json"
    if not path.is_file():
        return {"schema": "abd-delivery-run-state/v1", "next_slot_id": 1, "runs": {}}
    return _read_json(path)


def save_run_state(workspace: Path, state: dict[str, Any]) -> None:
    _write_json(war_room_dir(workspace) / "run-state.json", state)


def catalog_to_run_meta(
    entries: list[RunCatalogEntry], state: dict[str, Any]
) -> dict[int, RunMeta]:
    runs: dict[int, RunMeta] = {}
    state_runs = state.get("runs") or {}
    for entry in entries:
        rs = state_runs.get(str(entry.run)) or {}
        runs[entry.run] = RunMeta(
            run=entry.run,
            title=entry.title,
            first_slot=rs.get("first_slot"),
            last_slot=rs.get("last_slot"),
            stages=list(entry.stages),
            system_of_work=entry.system_of_work,
            discovery_precompleted=entry.discovery_precompleted,
            slots_generated=bool(rs.get("slots_generated")),
        )
    return runs


def _resolve_opens_after_dep(
    opens_after: dict[str, Any], state: dict[str, Any]
) -> list[int]:
    if not opens_after:
        return []
    if "slot" in opens_after:
        return [int(opens_after["slot"])]
    prior_run = opens_after.get("run")
    if prior_run is None:
        return []
    rs = (state.get("runs") or {}).get(str(prior_run)) or {}
    gate = str(opens_after.get("gate", "specification")).lower()
    if gate == "specification" and rs.get("spec_exit_slot"):
        return [int(rs["spec_exit_slot"])]
    if rs.get("last_slot"):
        return [int(rs["last_slot"])]
    return []


def _skill_waived(entry: RunCatalogEntry, stage: str, skill: str) -> bool:
    waived = entry.waived_skills.get(stage) or []
    return skill in waived


def _format_depends(deps: list[int]) -> str:
    if not deps:
        return "  []"
    return "\n".join(f'  - "{d:03d}"' if d < 1000 else f'  - "{d}"' for d in deps)


def _format_skills(skills: list[str]) -> str:
    return "\n".join(f"  - {s}" for s in skills)


def generate_run_slots(
    workspace: Path,
    run_num: int,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[Path]:
    """Materialize slot-NN-start.md for a run from catalog + system-of-work."""
    war_room = war_room_dir(workspace)
    if not war_room.is_dir():
        raise FileNotFoundError(f"War room missing: {war_room}")

    catalog = load_run_catalog(workspace)
    entry = next((e for e in catalog if e.run == run_num), None)
    if entry is None:
        raise ValueError(f"Run {run_num} not in run-catalog.json")

    sow_map = load_system_of_work(workspace)
    sow = sow_map.get(entry.system_of_work)
    if sow is None:
        raise ValueError(f"System of work `{entry.system_of_work}` not found")

    state = load_run_state(workspace)
    rs = (state.get("runs") or {}).get(str(run_num)) or {}
    if rs.get("slots_generated") and not force:
        raise ValueError(
            f"Run {run_num} already has slots_generated=true in run-state.json "
            "(use --force to regenerate)"
        )

    next_id = int(state.get("next_slot_id") or 1)
    disk_max = max_existing_slot_id(war_room)
    slot_id = max(next_id, disk_max + 1)

    profile_name = entry.parallel_profile or str(
        (sow.parallel_profiles.get("default") or "")
    )
    profile: dict[str, list[str]] = {}
    if profile_name:
        raw_sow = _read_json(war_room / "system-of-work.json")
        block = raw_sow.get("definitions", {}).get(entry.system_of_work, {})
        profile = (block.get("parallel_profiles") or {}).get(profile_name) or {}

    written: list[Path] = []
    first_slot: int | None = None
    last_slot: int | None = None
    stage_last_reviewer: dict[str, int] = {}
    slot_by_key: dict[str, int] = {}
    prior_stage_last: int | None = None
    opens_deps = _resolve_opens_after_dep(entry.opens_after, state)

    def _resolve_profile_deps(key: str, linear_fallback: list[int]) -> list[int]:
        if key not in profile:
            return linear_fallback
        out: list[int] = []
        for ref in profile[key]:
            if str(ref).isdigit():
                out.append(int(ref))
            elif ref in slot_by_key:
                out.append(slot_by_key[ref])
        return out or linear_fallback

    for stage in entry.stages:
        steps = sow.stages.get(stage) or []
        stage_prev: int | None = prior_stage_last
        for step in steps:
            if _skill_waived(entry, stage, step.skill):
                continue
            key = f"{stage}:{step.skill}:executor"
            linear_exec_deps: list[int] = []
            if stage_prev is not None:
                linear_exec_deps = [stage_prev]
            elif opens_deps and stage == entry.stages[0]:
                linear_exec_deps = list(opens_deps)
            exec_deps = _resolve_profile_deps(key, linear_exec_deps)

            exec_id = slot_id
            slot_id += 1
            if first_slot is None:
                first_slot = exec_id
            slot_by_key[key] = exec_id

            rev_key = f"{stage}:{step.skill}:reviewer"
            rev_deps = _resolve_profile_deps(rev_key, [exec_id])

            rev_id = slot_id
            slot_id += 1
            slot_by_key[rev_key] = rev_id
            last_slot = rev_id
            stage_last_reviewer[stage] = rev_id
            stage_prev = rev_id

            for slot_type, sid, deps, skills in (
                ("executor", exec_id, exec_deps, [step.skill]),
                ("reviewer", rev_id, rev_deps, [step.skill]),
            ):
                prior_line = ""
                if slot_type == "reviewer":
                    prior_line = f"prior_executor_slot: {exec_id}\n"
                content = SLOT_START_TEMPLATE.format(
                    slot_id=sid,
                    run_title=entry.title,
                    skill_label=step.label or step.skill,
                    slot_type=slot_type,
                    team_role=step.role if slot_type == "executor" else step.role,
                    workspace=str(workspace.resolve()),
                    run_num=run_num,
                    stage=stage,
                    depends_on_yaml=_format_depends(deps),
                    run_scope=entry.scope or entry.title,
                    skills_yaml=_format_skills(skills),
                    prior_executor_line=prior_line,
                    checkpoint="none",
                    system_of_work=entry.system_of_work,
                    body_notes=(
                        f"Auto-generated at run open from `{entry.system_of_work}` "
                        f"({stage} / {step.skill} / {slot_type})."
                    ),
                )
                out_path = slot_path_for(
                    war_room,
                    sid,
                    f"slot-{sid:03d}-start.md",
                    run_num=run_num,
                    stage=stage,
                )
                if not dry_run:
                    out_path.write_text(content, encoding="utf-8")
                written.append(out_path)

        prior_stage_last = stage_last_reviewer.get(stage)

    if not dry_run:
        state.setdefault("runs", {})[str(run_num)] = {
            **rs,
            "slots_generated": True,
            "first_slot": first_slot,
            "last_slot": last_slot,
            "system_of_work": entry.system_of_work,
            "spec_exit_slot": _infer_spec_exit_slot(war_room, run_num, first_slot, last_slot),
        }
        state["next_slot_id"] = slot_id
        save_run_state(workspace, state)

    return written


def _infer_spec_exit_slot(
    war_room: Path, run_num: int, first_slot: int | None, last_slot: int | None
) -> int | None:
    """Last specification reviewer slot for this run (for opens_after on next run)."""
    if first_slot is None or last_slot is None:
        return None
    best: int | None = None
    for sid in range(first_slot, last_slot + 1):
        path = find_slot_start(war_room, sid)
        if path is None:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"^stage:\s*specification", text, re.M) and re.search(
            r"^slot_type:\s*reviewer", text, re.M
        ):
            best = sid
    return best


def resolve_runs(workspace: Path) -> dict[int, RunMeta]:
    """Load runs from run-catalog.json + run-state.json (required)."""
    war_room = workspace / "docs" / "planning" / "delivery-war-room"
    catalog_path = war_room / "run-catalog.json"
    if not catalog_path.is_file():
        raise FileNotFoundError(
            f"run-catalog.json missing at {catalog_path}. "
            "Create it via delivery-lead Step 2b; legacy agile-delivery-plan slot tables are no longer supported."
        )
    catalog = load_run_catalog(workspace)
    state = load_run_state(workspace)
    return catalog_to_run_meta(catalog, state)


def parent_discovery_from_catalog(catalog: list[RunCatalogEntry]) -> set[int]:
    return {e.run for e in catalog if e.discovery_precompleted}
