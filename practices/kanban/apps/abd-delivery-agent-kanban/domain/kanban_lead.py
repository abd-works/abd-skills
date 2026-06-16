"""
kanban_lead.py

Domain area   : Kanban Board — Kanban Lead: Agent
Responsibilities: manage kanban board, detect stage completion, trigger scatter,
                  monitor heartbeats, pull tickets from backlog, dispatch claims,
                  release orphan claims, operate board in manual mode
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .delivery_model import (
    KanbanBoard,
    Stage,
    SkillProgress,
    Ticket,
    _read_json,
    append_metrics_log,
    backlog_sort_key,
    count_in_progress_for_role,
    count_live_agents,
    count_working_agents,
    is_fixture_mode,
    purge_unregistered_heartbeats,
    register_executor_spawn,
    find_ticket_in_board,
    list_heartbeat_files,
    load_board,
    load_kanban_board,
    load_team,
    now_iso,
    read_heartbeat_age_seconds,
    save_board,
    save_ticket_in_board,
    select_backlog_for_stage,
    war_room_dir,
    write_heartbeat,
)
from .board_mode import is_manual_mode as _board_is_manual, read_board_mode
from .action_state import (
    ActionIntent,
    load_action_intents,
    action_state_file_exists,
    NoActionStateFileError,
    count_intents_by_role,
    remove_action_intent,
)

_KANBAN_CLI_SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "abd-kanban"
    / "scripts"
    / "kanban_cli.py"
)


class NoBoardConfigurationError(Exception):
    """Raised when the board references a stage_configuration not found in kanban.json."""


ROLES = ("business-expert", "product-owner", "ux-designer", "engineer")


class KanbanLead:
    """Orchestrates the kanban board: pull, scatter, advance, dispatch, release.

    domain model responsibilities:
      - manage kanban board        → KanbanBoard
      - move ticket to done when complete → Stage, Ticket
      - trigger scatter            → Ticket, KanbanBoard, Stage
      - monitor heartbeats         → Heartbeat, Agent
      - pull ticket to Stage       → Ticket, Stage
      - assign Agent to Ticket     → Ticket, Stage, Team Member
    """

    def __init__(self, workspace: Path) -> None:
        self._workspace = workspace
        self._wr = war_room_dir(workspace)

    @property
    def workspace(self) -> Path:
        return self._workspace

    # ------------------------------------------------------------------
    # Board + config resolution
    # ------------------------------------------------------------------

    def _resolve_board_and_config(self) -> tuple[dict, KanbanBoard, dict]:
        board = load_board(self._workspace)
        config_name = board.get("stage_configuration") or board.get("system_of_work", "")
        kb_map = load_kanban_board(self._workspace)
        kb = kb_map.get(config_name)
        if kb is None:
            raise NoBoardConfigurationError(f"Unknown stage_configuration: {config_name}")
        kb_block = self._raw_kb_block(config_name)
        return board, kb, kb_block

    def _raw_kb_block(self, config_name: str) -> dict:
        path = self._wr / "kanban.json"
        if not path.is_file():
            return {}
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw.get("definitions", {}).get(config_name, {})

    # ==================================================================
    # PULL TICKETS FROM BACKLOG
    # ==================================================================

    def pull_backlog(self) -> list[str]:
        """Pull backlog tickets to active for every stage up to WIP limits."""
        board, kb, kb_block = self._resolve_board_and_config()
        team = load_team(board, kb_block)
        actions: list[str] = []

        for stage_def in kb.stages:
            actions.extend(self._pull_for_stage(board, kb, stage_def, team))
            board = load_board(self._workspace)

        return actions

    def _pull_for_stage(
        self,
        board: dict,
        kb: KanbanBoard,
        stage_def: Stage,
        team: dict[str, int],
    ) -> list[str]:
        slots = kb.pull_slots_for_stage(board, stage_def, team)
        if slots <= 0:
            return []

        candidates = select_backlog_for_stage(board, stage_def.name, slots)
        if not candidates:
            return []

        actions: list[str] = []
        backlog = board.get("backlog", [])

        for raw in candidates:
            ticket = Ticket.from_dict(raw)
            backlog = [t for t in backlog if t.get("ticket_id") != ticket.ticket_id]
            ticket.entered_stage = now_iso()
            ticket.notes = f"Lead pulled to {stage_def.name} active"
            board.setdefault("active", []).append(ticket.to_dict())
            actions.append(f"pulled:{ticket.ticket_id}:{stage_def.name}:{stage_def.scope}")
            append_metrics_log(self._workspace, {
                "event": "ticket_pulled",
                "agent": "kanban-lead",
                "ticket_id": ticket.ticket_id,
                "from": "backlog",
                "to": "active",
                "scope_level": ticket.scope_level,
                "stage": stage_def.name,
            })

        board["backlog"] = backlog
        save_board(self._workspace, board)
        return actions

    # ==================================================================
    # DETECT STAGE COMPLETION / ADVANCE OR FLAG
    # ==================================================================

    def advance_or_flag(self, ticket: Ticket, kb: KanbanBoard) -> str:
        """Check if ticket stage is complete; advance or flag for scatter."""
        current_def = kb.get_stage(ticket.stage)
        if not current_def:
            return "no_change"

        if not ticket.is_stage_complete(current_def):
            return "no_change"

        nxt = kb.next_stage(ticket.stage)
        if nxt is None:
            ticket.completed_stage = now_iso()
            append_metrics_log(self._workspace, {
                "event": "ticket_complete",
                "ticket_id": ticket.ticket_id,
                "lineage": ticket.lineage,
                "stage": ticket.stage,
            })
            return "complete"

        if nxt.scope != current_def.scope:
            ticket.completed_stage = now_iso()
            append_metrics_log(self._workspace, {
                "event": "scatter_needed",
                "ticket_id": ticket.ticket_id,
                "from_scope": current_def.scope,
                "to_scope": nxt.scope,
                "next_stage": nxt.name,
            })
            return "scatter_needed"

        old_stage = ticket.stage
        ticket.advance_to_next_stage(nxt)
        append_metrics_log(self._workspace, {
            "event": "stage_advance",
            "ticket_id": ticket.ticket_id,
            "lineage": ticket.lineage,
            "from_stage": old_stage,
            "to_stage": nxt.name,
        })
        return "advanced"

    # ==================================================================
    # SYNC BOARD
    # ==================================================================

    def _done_ticket_should_archive(self, ticket: Ticket, kb: KanbanBoard, board: dict) -> bool:
        if ticket.needs_scatter(kb):
            return False
        return bool(ticket.completed_stage)

    def sync_board(self, dry_run: bool = False) -> dict:
        """Sync the board: check every active ticket for completion/advance."""
        board, kb, _ = self._resolve_board_and_config()

        active_tickets = [Ticket.from_dict(t) for t in board.get("active", [])]
        done_tickets = [Ticket.from_dict(t) for t in board.get("done", [])]
        backlog_tickets = [Ticket.from_dict(t) for t in board.get("backlog", [])]
        archived = board.get("archived", [])

        new_active: list[Ticket] = []
        new_done: list[Ticket] = []

        for ticket in active_tickets:
            action = self.advance_or_flag(ticket, kb)
            if action == "complete":
                archived.append(ticket.to_dict())
            elif action == "scatter_needed":
                new_done.append(ticket)
            else:
                new_active.append(ticket)

        for ticket in done_tickets:
            if self._done_ticket_should_archive(ticket, kb, board):
                archived.append(ticket.to_dict())
            else:
                new_done.append(ticket)

        board["active"] = [t.to_dict() for t in new_active]
        board["done"] = [t.to_dict() for t in new_done]
        board["backlog"] = [t.to_dict() for t in backlog_tickets]
        board["archived"] = archived
        board["synced_at"] = now_iso()

        if not dry_run:
            save_board(self._workspace, board)

        return board

    # ==================================================================
    # TRIGGER SCATTER
    # ==================================================================

    def scatter_pending(self) -> list[str]:
        """Scatter every done ticket at a scope boundary."""
        board, kb, _ = self._resolve_board_and_config()
        actions: list[str] = []

        for ticket in kb.tickets_needing_scatter(board):
            try:
                children_spec = self._children_spec_for_ticket(ticket)
            except (FileNotFoundError, ValueError) as e:
                actions.append(f"scatter_failed:{ticket.ticket_id}:{e}")
                append_metrics_log(self._workspace, {
                    "event": "scatter_failed",
                    "ticket_id": ticket.ticket_id,
                    "error": str(e),
                })
                continue

            children = self._execute_scatter(ticket, kb, children_spec)
            child_ids = [c.ticket_id for c in children]
            actions.append(f"scatter:{ticket.ticket_id}->{','.join(child_ids)}")
            board = load_board(self._workspace)

        return actions

    def _execute_scatter(
        self,
        parent: Ticket,
        kb: KanbanBoard,
        children_spec: list[dict],
    ) -> list[Ticket]:
        from .delivery_model import DuplicateTicketIdError

        board = load_board(self._workspace)

        existing_ids = frozenset(
            t.get("ticket_id", "")
            for bucket in ("active", "backlog", "done")
            for t in board.get(bucket, [])
        )

        done_list = [Ticket.from_dict(t) for t in board.get("done", [])]
        parent_idx = next(
            (i for i, t in enumerate(done_list) if t.ticket_id == parent.ticket_id),
            None,
        )
        if parent_idx is not None:
            done_list.pop(parent_idx)
            board["done"] = [t.to_dict() for t in done_list]
        else:
            board["active"] = [
                t for t in board.get("active", [])
                if t.get("ticket_id") != parent.ticket_id
            ]

        children = parent.scatter_into_children(kb, children_spec, existing_ids=existing_ids)

        archived_list = board.get("archived", [])
        archived_list.append(parent.to_dict())
        board["archived"] = archived_list

        backlog = [Ticket.from_dict(t) for t in board.get("backlog", [])]
        backlog.extend(children)
        backlog.sort(key=backlog_sort_key)
        board["backlog"] = [t.to_dict() for t in backlog]

        save_board(self._workspace, board)
        append_metrics_log(self._workspace, {
            "event": "scatter",
            "parent_ticket": parent.ticket_id,
            "parent_lineage": parent.lineage,
            "children": [c.ticket_id for c in children],
            "from_stage": parent.stage,
            "to_stage": children[0].stage if children else "",
            "from_scope": parent.scope_level,
            "to_scope": children[0].scope_level if children else "",
        })
        return children

    def _children_spec_for_ticket(self, ticket: Ticket) -> list[dict]:
        if self._is_increment_scatter_parent(ticket.ticket_id):
            groupings = self._workspace / "docs/end-to-end/discovery/stories/sprint-groupings.md"
            if groupings.is_file():
                return self._sprints_from_sprint_groupings(groupings, ticket.ticket_id)
            raise FileNotFoundError(
                f"No sprint-groupings.md for scatter from {ticket.ticket_id}"
            )

        from .delivery_model import module_number_from_ticket_id
        thin = self._workspace / "docs/end-to-end/discovery/stories/thin-slicing.md"
        mod: int | None
        try:
            mod = module_number_from_ticket_id(ticket.ticket_id)
        except ValueError:
            mod = None

        if mod is not None:
            try:
                return self._increments_from_thin_slicing(thin, mod, parent_id=ticket.ticket_id)
            except (FileNotFoundError, ValueError):
                pass

        slug = ticket.ticket_id.split("-", 1)[1] if "-" in ticket.ticket_id else ticket.ticket_id
        per_module = self._workspace / f"docs/end-to-end/discovery/stories/{slug}-thin-slicing.md"
        if per_module.is_file():
            return self._increments_from_per_module_thin_slicing(per_module, parent_id=ticket.ticket_id)

        if ticket.scope_level == "all":
            partition = self._workspace / "docs/end-to-end/shaping/module-partition.md"
            if partition.is_file():
                return self._modules_from_module_partition(partition)

        mod_label = mod if mod is not None else "?"
        raise FileNotFoundError(
            f"No scatter spec for {ticket.ticket_id}: tried {thin}, {per_module}, module {mod_label}"
        )

    @staticmethod
    def _is_increment_scatter_parent(ticket_id: str) -> bool:
        return bool(re.search(r"-inc-\d+-", ticket_id, re.I))

    @staticmethod
    def _increment_number_from_ticket_id(ticket_id: str) -> int | None:
        m = re.search(r"-inc-(\d+)-", ticket_id, re.I)
        if m:
            return int(m.group(1))
        head = ticket_id.split("-", 1)[0]
        if head.isdigit():
            return int(head)
        return None

    def _sprints_from_sprint_groupings(self, path: Path, parent_ticket_id: str) -> list[dict]:
        inc_num = self._increment_number_from_ticket_id(parent_ticket_id)
        if inc_num is None:
            raise ValueError(f"Cannot infer increment number from ticket_id: {parent_ticket_id}")

        text = path.read_text(encoding="utf-8")
        section = re.search(
            rf"## Increment {inc_num}:.*?(?=\n## Increment \d+:|$)",
            text,
            re.DOTALL,
        )
        if not section:
            raise ValueError(f"No Increment {inc_num} section in {path}")

        slug_match = re.search(r"`([^`]+)`", section.group(0))
        increment_slug = slug_match.group(1) if slug_match else f"inc-{inc_num}"

        children: list[dict] = []
        for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", section.group(0), re.M):
            sprint_num = int(m.group(1))
            label = m.group(2).strip()
            if not label or label.lower() == "label":
                continue
            children.append({
                "id": f"{increment_slug}-sprint-{sprint_num}",
                "name": label,
                "priority": sprint_num,
            })
        if not children:
            raise ValueError(f"No sprint rows in sprint-groupings for {increment_slug}")
        return children

    def _increments_from_per_module_thin_slicing(
        self,
        path: Path,
        parent_id: str | None = None,
    ) -> list[dict]:
        text = path.read_text(encoding="utf-8")
        prefix = parent_id if parent_id else "module"
        children: list[dict] = []
        for m in re.finditer(r"### Increment (\d+): (.+)", text):
            inc_num = int(m.group(1))
            title = m.group(2).strip()
            slug = self._slugify(title)
            children.append({
                "id": f"{prefix}-inc-{inc_num}-{slug}",
                "name": title,
                "priority": inc_num,
            })
        if not children:
            raise ValueError(f"No increments in {path}")
        return children

    def _increments_from_thin_slicing(
        self,
        thin_slicing: Path,
        module_num: int,
        parent_id: str | None = None,
    ) -> list[dict]:
        if not thin_slicing.is_file():
            raise FileNotFoundError(f"thin-slicing not found: {thin_slicing}")

        text = thin_slicing.read_text(encoding="utf-8")
        section = re.search(
            rf"## Module {module_num}:.*?(?=\n## Module \d+:|\Z)",
            text,
            re.DOTALL,
        )
        if not section:
            raise ValueError(f"No Module {module_num} section in {thin_slicing}")

        prefix = parent_id if parent_id else str(module_num)
        children: list[dict] = []
        for m in re.finditer(r"### Increment (\d+): (.+)", section.group(0)):
            inc_num = int(m.group(1))
            title = m.group(2).strip()
            slug = self._slugify(title)
            children.append({
                "id": f"{prefix}-inc-{inc_num}-{slug}",
                "name": title,
                "priority": inc_num,
            })
        if not children:
            raise ValueError(f"No increments under Module {module_num} in {thin_slicing}")
        return children

    @staticmethod
    def _slugify(title: str) -> str:
        s = title.lower().strip()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        return s.strip("-")

    def _modules_from_module_partition(self, path: Path) -> list[dict]:
        text = path.read_text(encoding="utf-8")
        children: list[dict] = []
        for i, m in enumerate(re.finditer(r"## Module:\s*\[([^\]]+)\]", text), start=1):
            name = m.group(1).strip()
            slug = self._slugify(name)
            children.append({
                "id": f"{i}-{slug}",
                "name": name,
                "priority": i,
            })
        if not children:
            raise ValueError(f"No modules in {path}")
        return children

    # ==================================================================
    # DISPATCH ELIGIBLE CLAIMS
    # ==================================================================

    def dispatch_claims(self, roles: tuple[str, ...] = ROLES) -> list[str]:
        """Reserve eligible skills up to team capacity per role."""
        board, kb, kb_block = self._resolve_board_and_config()
        team = load_team(board, kb_block)
        actions: list[str] = []

        for role in roles:
            actions.extend(self._dispatch_for_role(role, team, kb))

        return actions

    def _dispatch_for_role(self, role: str, team: dict[str, int], kb: KanbanBoard) -> list[str]:
        capacity = team.get(role, 0)
        if capacity <= 0:
            return []

        live = count_live_agents(self._wr, role)
        if live <= 0:
            return []

        actions: list[str] = []
        effective_cap = min(capacity, live)

        for instance in range(1, capacity + 1):
            board = load_board(self._workspace)
            active = [Ticket.from_dict(t) for t in board.get("active", [])]
            eligible = kb.count_eligible_claims(active, role)
            if not eligible:
                break
            in_progress = count_in_progress_for_role(active, role)
            if in_progress >= effective_cap:
                break

            proc = subprocess.run(
                [
                    sys.executable,
                    str(_KANBAN_CLI_SCRIPT),
                    "member", "pull",
                    "--workspace", str(self._workspace),
                    "--role", role,
                    "--instance", str(instance),
                    "--reserve",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode != 0:
                actions.append(f"dispatch_failed:{role}:{instance}")
                break

            result = self._parse_json_output(proc.stdout)
            if result is None:
                actions.append(f"dispatch_failed:{role}:{instance}")
                break

            if result.get("action") == "claimed":
                ticket_id = result.get("ticket_id")
                skill = result.get("skill")
                actions.append(f"auto_claim:{role}:{ticket_id}:{skill}")
                append_metrics_log(self._workspace, {
                    "event": "auto_claim",
                    "agent_role": role,
                    "instance": instance,
                    "ticket_id": ticket_id,
                    "skill": skill,
                })
            elif result.get("action") == "none":
                break
            else:
                break

        return actions

    @staticmethod
    def _parse_json_output(stdout: str) -> dict | None:
        try:
            return json.loads(stdout.strip() or "{}")
        except json.JSONDecodeError:
            return None

    # ==================================================================
    # MONITOR HEARTBEATS / RELEASE ORPHAN CLAIMS
    # ==================================================================

    def release_stale_reserved(self, roles: tuple[str, ...] = ROLES, stale_seconds: float = 30.0) -> list[str]:
        actions: list[str] = []
        for role in roles:
            if self._role_has_working_executor(role):
                continue
            if self._has_fresh_reserve(role, stale_seconds):
                continue
            actions.extend(self._release_role_claims(role, "release_stale"))
            self._purge_reserved_heartbeats(role)
        return actions

    def release_orphan_claims(self, roles: tuple[str, ...] = ROLES, stale_seconds: float = 120.0) -> list[str]:
        actions: list[str] = []

        for role in roles:
            board = load_board(self._workspace)
            active = [Ticket.from_dict(t) for t in board.get("active", [])]
            in_progress = count_in_progress_for_role(active, role)
            if in_progress <= 0:
                continue

            working = count_working_agents(self._wr, role, stale_seconds)

            if working == 0 and not self._has_fresh_working(role, stale_seconds):
                actions.extend(self._release_role_claims(role, "release_orphan"))
                continue

            excess = in_progress - max(working, 0)
            if excess <= 0:
                continue

            released = self._release_excess_claims(role, excess, "release_excess_orphan")
            actions.extend(released)

        return actions

    def _role_has_working_executor(self, role: str, stale_seconds: float = 120.0) -> bool:
        return count_working_agents(self._wr, role, stale_seconds) > 0

    def _has_fresh_reserve(self, role: str, stale_seconds: float) -> bool:
        for path in list_heartbeat_files(self._wr, role):
            age = read_heartbeat_age_seconds(path)
            if age is None or age > stale_seconds:
                continue
            try:
                if _read_json(path).get("status") == "reserved":
                    return True
            except (OSError, ValueError):
                continue
        return False

    def _has_fresh_working(self, role: str, stale_seconds: float) -> bool:
        for path in list_heartbeat_files(self._wr, role):
            age = read_heartbeat_age_seconds(path)
            if age is None or age > stale_seconds:
                continue
            try:
                if _read_json(path).get("status") == "working":
                    return True
            except (OSError, ValueError):
                continue
        return False

    def _has_fresh_ready(self, role: str, stale_seconds: float) -> bool:
        for path in list_heartbeat_files(self._wr, role):
            age = read_heartbeat_age_seconds(path)
            if age is None or age > stale_seconds:
                continue
            try:
                if _read_json(path).get("status") == "ready":
                    return True
            except (OSError, ValueError):
                continue
        return False

    def _release_role_claims(self, role: str, prefix: str) -> list[str]:
        board = load_board(self._workspace)
        active = board.get("active", [])
        actions: list[str] = []
        changed = False
        for index, raw in enumerate(active):
            ticket = Ticket.from_dict(raw)
            released: list[str] = []
            for skill_id, sp in list(ticket.skill_progress.items()):
                if sp.agent != role or sp.execution_status != "in_progress":
                    continue
                del ticket.skill_progress[skill_id]
                released.append(skill_id)
            if not released:
                continue
            for skill_id in released:
                actions.append(f"{prefix}:{role}:{ticket.ticket_id}:{skill_id}")
            save_ticket_in_board(board, "active", index, ticket)
            changed = True
        if changed:
            save_board(self._workspace, board)
        return actions

    def _release_excess_claims(self, role: str, count: int, prefix: str) -> list[str]:
        board = load_board(self._workspace)
        kb_map = load_kanban_board(self._workspace)
        config_name = board.get("stage_configuration") or board.get("system_of_work", "")
        kb = kb_map.get(config_name)
        if kb is None:
            return self._release_role_claims(role, prefix)

        claims: list[tuple[int, str, str, str]] = []
        for index, raw in enumerate(board.get("active", [])):
            ticket = Ticket.from_dict(raw)
            for skill_id, sp in ticket.skill_progress.items():
                if sp.agent == role and sp.execution_status == "in_progress":
                    claims.append((index, ticket.ticket_id, skill_id, ticket.stage))

        stage_order = [s.name for s in kb.stages]
        claims.sort(key=lambda c: stage_order.index(c[3]) if c[3] in stage_order else 0)

        to_release = claims[:count]
        actions: list[str] = []
        changed = False
        for index, ticket_id, skill_id, stage in to_release:
            raw = board["active"][index]
            ticket = Ticket.from_dict(raw)
            if skill_id in ticket.skill_progress:
                del ticket.skill_progress[skill_id]
                save_ticket_in_board(board, "active", index, ticket)
                changed = True
                actions.append(f"{prefix}:{role}:{ticket_id}:{skill_id}")
                append_metrics_log(self._workspace, {
                    "event": prefix,
                    "agent_role": role,
                    "ticket_id": ticket_id,
                    "skill": skill_id,
                    "stage": stage,
                })
        if changed:
            save_board(self._workspace, board)
        return actions

    def _purge_reserved_heartbeats(self, role: str) -> None:
        for path in list_heartbeat_files(self._wr, role):
            try:
                raw = _read_json(path)
            except (OSError, ValueError):
                continue
            if raw.get("status") == "reserved":
                path.unlink(missing_ok=True)

    # ==================================================================
    # DETECT DUPLICATE TICKET IDS
    # ==================================================================

    def _detect_duplicate_ids(self) -> list[str]:
        from collections import Counter
        board = load_board(self._workspace)
        all_ids: list[str] = []
        for bucket in ("active", "backlog", "done"):
            for t in board.get(bucket, []):
                all_ids.append(t.get("ticket_id", ""))
        dupes = {k: v for k, v in Counter(all_ids).items() if v > 1}
        if not dupes:
            return []
        actions: list[str] = []
        for tid, count in sorted(dupes.items()):
            actions.append(f"DUPLICATE_ID:{tid}:x{count}")
        append_metrics_log(self._workspace, {
            "event": "duplicate_ticket_ids_detected",
            "duplicates": dupes,
        })
        return actions

    # ==================================================================
    # RUN FULL SCAN CYCLE
    # ==================================================================

    def run_scan(self) -> dict:
        """One full scan cycle: sync, scatter, pull, release, dispatch."""
        session = self._read_lead_session()
        cycle = int(session.get("cycle", 0)) + 1
        actions: list[str] = []

        write_heartbeat(self._wr, "kanban-lead", "working", f"Scan cycle {cycle} started")

        self.sync_board(dry_run=False)
        actions.append("board_sync")

        dupe_actions = self._detect_duplicate_ids()
        actions.extend(dupe_actions)

        scatter_actions = self.scatter_pending()
        actions.extend(scatter_actions)

        pull_actions = self.pull_backlog()
        actions.extend(pull_actions)

        board, kb, kb_block = self._resolve_board_and_config()
        team = load_team(board, kb_block)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        backlog = board.get("backlog", [])

        release_actions = self.release_stale_reserved(ROLES)
        actions.extend(release_actions)
        orphan_actions = self.release_orphan_claims(ROLES)
        actions.extend(orphan_actions)
        if release_actions or orphan_actions:
            board = load_board(self._workspace)
            active = [Ticket.from_dict(t) for t in board.get("active", [])]

        dispatch_actions = self.dispatch_claims(ROLES)
        actions.extend(dispatch_actions)
        if dispatch_actions:
            board = load_board(self._workspace)
            active = [Ticket.from_dict(t) for t in board.get("active", [])]

        role_report = self._build_role_report(active, kb, team)
        spawns = self._compute_spawns(role_report)
        for s in spawns:
            actions.append(f"spawn_{s['role']}_{s['instance']}")

        report = {
            "cycle": cycle,
            "timestamp": now_iso(),
            "active_tickets": len(active),
            "backlog_count": len(backlog),
            "roles": role_report,
            "spawns": spawns,
            "actions": actions,
        }

        append_metrics_log(self._workspace, {
            "event": "scan_cycle",
            "cycle": cycle,
            "agent": "kanban-lead",
            "actions": actions,
            "active_tickets": len(active),
            "backlog_count": len(backlog),
            "eligible_by_role": {r: len(role_report[r]["eligible_claims"]) for r in role_report},
            "spawn_needed_by_role": {r: role_report[r]["spawn_needed"] for r in role_report},
        })

        write_heartbeat(self._wr, "kanban-lead", "working", f"Scan cycle {cycle}; spawns={len(spawns)}")
        session.update({
            "cycle": cycle,
            "last_scan": report["timestamp"],
            "last_spawns": spawns,
        })
        self._write_lead_session(session)
        return report

    def _build_manual_role_report(self, active: list[Ticket], team: dict[str, int]) -> dict[str, dict]:
        intent_counts = count_intents_by_role(self._wr)
        report: dict[str, dict] = {}
        for role in ROLES:
            if role not in team:
                continue
            capacity = team[role]
            pending = intent_counts.get(role, 0)
            in_progress = count_in_progress_for_role(active, role)
            working = count_working_agents(self._wr, role)
            live = count_live_agents(self._wr, role)
            work_units = pending + in_progress

            dead_slots = max(0, capacity - live)
            spawn_need = min(dead_slots, work_units) if work_units > 0 else 0

            idle_live = max(0, live - working)
            dispatch_need = min(idle_live, pending + in_progress) if work_units > 0 else 0

            report[role] = {
                "team": capacity,
                "live_agents": live,
                "working_agents": working,
                "in_progress": in_progress,
                "pending_intents": pending,
                "eligible_claims": [],
                "spawn_needed": spawn_need,
                "dispatch_needed": dispatch_need,
            }
        return report

    def _build_role_report(self, active: list[Ticket], kb: KanbanBoard, team: dict[str, int]) -> dict[str, dict]:
        report: dict[str, dict] = {}
        for role in ROLES:
            if role not in team:
                continue
            capacity = team[role]
            eligible = kb.list_eligible_pulls(active, role)
            in_progress = count_in_progress_for_role(active, role)
            working = count_working_agents(self._wr, role)
            live = count_live_agents(self._wr, role)
            unclaimed = max(0, len(eligible) - in_progress)

            dead_slots = max(0, capacity - live)
            spawn_need = min(dead_slots, unclaimed)

            idle_live = max(0, live - working)
            dispatch_need = min(idle_live, unclaimed)

            report[role] = {
                "team": capacity,
                "live_agents": live,
                "working_agents": working,
                "in_progress": in_progress,
                "eligible_claims": eligible,
                "spawn_needed": spawn_need,
                "dispatch_needed": dispatch_need,
            }
        return report

    def _compute_spawns(self, role_report: dict[str, dict]) -> list[dict]:
        spawns: list[dict] = []
        for role in ROLES:
            if role not in role_report:
                continue
            data = role_report[role]
            need = data["spawn_needed"]
            working = data["working_agents"]
            for _ in range(need):
                instance = working + len([s for s in spawns if s["role"] == role]) + 1
                epoch = register_executor_spawn(self._wr, role, instance)
                spawns.append({
                    "role": role,
                    "instance": instance,
                    "reason": "pool_fill",
                    "spawn_epoch": epoch,
                })
        return spawns

    # ------------------------------------------------------------------
    # Lead session persistence
    # ------------------------------------------------------------------

    def _read_lead_session(self) -> dict:
        path = self._wr / "lead-session.json"
        if not path.is_file():
            return {"cycle": 0}
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_lead_session(self, data: dict) -> None:
        path = self._wr / "lead-session.json"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    # ==================================================================
    # MANUAL MODE
    # ==================================================================

    def is_manual_mode(self) -> bool:
        board = load_board(self._workspace)
        return _board_is_manual(board)

    def run_scan_with_mode(self) -> dict:
        if not self.is_manual_mode():
            return self.run_scan()
        return self._run_manual_scan()

    def _run_manual_scan(self) -> dict:
        session = self._read_lead_session()
        cycle = int(session.get("cycle", 0)) + 1
        actions: list[str] = []

        write_heartbeat(self._wr, "kanban-lead", "working", f"Manual scan cycle {cycle}")

        for role in ROLES:
            purged = purge_unregistered_heartbeats(self._wr, role)
            if purged:
                actions.append(f"purged_ghost_heartbeats:{role}:{purged}")

        self.sync_board(dry_run=False)
        actions.append("board_sync")

        scatter_actions = self.scatter_pending()
        actions.extend(scatter_actions)

        intent_actions = self.process_action_intents()
        actions.extend(intent_actions)

        board, kb, kb_block = self._resolve_board_and_config()
        team = load_team(board, kb_block)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        backlog = board.get("backlog", [])

        role_report = self._build_manual_role_report(active, team)
        spawns = self._compute_spawns(role_report)
        for s in spawns:
            actions.append(f"spawn_{s['role']}_{s['instance']}")

        mode = read_board_mode(board)

        report = {
            "cycle": cycle,
            "timestamp": now_iso(),
            "board_mode": mode,
            "active_tickets": len(active),
            "backlog_count": len(backlog),
            "roles": role_report,
            "spawns": spawns,
            "actions": actions,
        }

        append_metrics_log(self._workspace, {
            "event": "manual_scan_cycle",
            "cycle": cycle,
            "agent": "kanban-lead",
            "board_mode": mode,
            "actions": actions,
            "eligible_by_role": {r: len(role_report[r]["eligible_claims"]) for r in role_report},
            "spawn_needed_by_role": {r: role_report[r]["spawn_needed"] for r in role_report},
        })

        write_heartbeat(self._wr, "kanban-lead", "working", f"Manual scan cycle {cycle}; spawns={len(spawns)}")
        session.update({
            "cycle": cycle,
            "last_scan": report["timestamp"],
            "last_spawns": spawns,
        })
        self._write_lead_session(session)
        return report

    def process_action_intents(self) -> list[str]:
        """Validate queued operator drops; remove invalid ones. Intents remain until agent claims."""
        if not action_state_file_exists(self._wr):
            return []

        try:
            intents = load_action_intents(self._wr)
        except NoActionStateFileError:
            return []

        if not intents:
            return []

        actions: list[str] = []
        for intent in intents:
            skip_reason = self._skip_reason_for_intent(intent)
            if skip_reason:
                remove_action_intent(self._wr, intent)
                actions.append(
                    f"skipped:{intent.ticket_id}:{intent.skill}:{intent.agent_role}:{skip_reason}",
                )
                continue
            actions.append(f"queued:{intent.ticket_id}:{intent.skill}:{intent.agent_role}")

        return actions

    def _skip_reason_for_intent(self, intent: ActionIntent) -> str | None:
        board = load_board(self._workspace)
        match = find_ticket_in_board(board, intent.ticket_id)
        if match is None:
            return "ticket_not_found"
        bucket, _, ticket = match
        if bucket != "active":
            return "ticket_not_active"
        sp = ticket.skill_progress.get(intent.skill)
        if sp is not None and sp.execution_status == "done":
            return "skill_done"
        if sp is not None and sp.execution_status == "in_progress":
            return "skill_in_progress"
        return None

    def delegate_manual_skill(
        self, ticket_id: str, skill: str, role: str,
    ) -> str | None:
        """Deprecated: manual drops no longer write in_progress on delegate."""
        board = load_board(self._workspace)
        match = find_ticket_in_board(board, ticket_id)
        if match is None:
            return None

        bucket, index, ticket = match
        if bucket != "active":
            return None

        ticket.skill_progress[skill] = SkillProgress(
            execution_status="in_progress",
            agent=role,
            start=now_iso(),
        )
        save_ticket_in_board(board, bucket, index, ticket)
        save_board(self._workspace, board)

        append_metrics_log(self._workspace, {
            "event": "manual_delegate",
            "ticket_id": ticket_id,
            "skill": skill,
            "agent_role": role,
        })
        return f"delegated:{ticket_id}:{skill}:{role}"

    # ==================================================================
    # TICK — scan + spawn prompt generation (domain model: manage kanban board)
    # ==================================================================

    LEAD_STALE_SECS: float = 90.0
    EXECUTOR_STALE_SECS: float = 120.0

    def run_tick(self) -> dict:
        """Run one lead tick: scan + add spawn prompts and orchestrator rule to report."""
        report = self.run_scan_with_mode()
        spawns = report.get("spawns", [])
        roles = report.get("roles", {})

        dispatch_summary = {
            role: data.get("dispatch_needed", 0)
            for role, data in roles.items()
            if data.get("dispatch_needed", 0) > 0
        }

        report["must_spawn"] = len(spawns) > 0
        report["dispatch_summary"] = dispatch_summary
        report["spawn_prompts"] = [
            self.spawn_prompt(s["role"], s["instance"], s.get("spawn_epoch"))
            for s in spawns
        ]
        report["orchestrator_rule"] = (
            "Dispatch already handled by scan (reserved skills for idle agents). "
            "If must_spawn is true, spawn every entry in spawn_prompts NOW "
            "(Task/subagent, run_in_background). Spawns are ONLY for dead/missing "
            "agent slots — live idle agents already got work dispatched."
        )
        return report

    def spawn_prompt(self, role: str, instance: int, spawn_epoch: int | None = None) -> dict:
        """Build the bootstrap prompt dict for a newly spawned team member executor."""
        board = load_board(self._workspace)
        fixture = is_fixture_mode(self._workspace)
        manual = _board_is_manual(board)

        inst_line = f"  instance: {instance}\n" if instance > 1 else ""
        seed_path = self._workspace / "AGENT-SEED.md"
        first_read = (
            f"Read {seed_path} FIRST (fixture mode — team member executor).\n\n"
            if fixture and seed_path.is_file()
            else "Read practices/kanban/agents/reference/session-bootstrap.md FIRST.\n\n"
        )

        _cli = "python practices/kanban/skills/abd-kanban/scripts/kanban_cli.py"
        fixture_block = ""
        if fixture:
            if manual:
                fixture_block = (
                    "\nFIXTURE MODE + MANUAL BOARD: team member executor — NOT kanban-lead.\n"
                    "Do NOT run kanban_cli.py member pull to self-assign.\n"
                    "When operator has dropped work (action-state intent), start with:\n"
                    f"  {_cli} member intent --workspace {self._workspace} --role {role}\n"
                    "Then apply fixture:\n"
                    f"  {_cli} member fixture --workspace {self._workspace} --role {role}\n"
                    "On idle ticks: heartbeat ready — do not claim without a pending intent.\n"
                    "See agents/reference/skill-fixture-mode.md.\n"
                )
            else:
                fixture_block = (
                    "\nFIXTURE MODE (mandatory): You are a team member executor — NOT kanban-lead. "
                    "Do NOT read practice skill SKILL.md or run scanners.\n"
                    "After kanban_cli.py member pull (or resume manual assignment), run:\n"
                    f"  {_cli} member fixture --workspace {self._workspace} --role {role} --ticket <id> --skill <name>\n"
                    "Or if skill is already in_progress from manual drop:\n"
                    f"  {_cli} member fixture --workspace {self._workspace} --role {role}\n"
                    "Then pull again. See agents/reference/skill-fixture-mode.md.\n"
                )

        epoch_line = (
            f"\nExecutor spawn_epoch: {spawn_epoch} "
            "(registered by kanban-lead — your heartbeats must carry this epoch).\n"
            if spawn_epoch is not None else ""
        )

        if manual:
            work_loop = (
                f"Arm AGENT_LOOP_TICK_{role} on turn 1 (30s, notify_on_output). "
                f"MANUAL MODE: on each tick run `{_cli} member intent` when idle — "
                f"never `{_cli} member pull`. Idle with no intent → `{_cli} member ready`."
            )
        else:
            work_loop = (
                f"Arm AGENT_LOOP_TICK_{role} on turn 1. "
                f"Pull via `{_cli} member pull` (never hand-edit board.json)."
            )

        prompt = (
            f"{first_read}"
            f"Bootstrap:\n  workspace: {self._workspace}\n  delivery-role: {role}\n"
            f"{inst_line}{epoch_line}\n"
            f"Then read agents/{role}/AGENT.md, agents/reference/pull-model.md, "
            "agents/reference/work-queue.md, and reference/artifact-layout.md.\n"
            f"{work_loop}"
            f"{fixture_block}"
            "\nNever exit after one skill."
        )
        if not fixture:
            prompt += " Execute and review per executor-workflow.md."

        return {"role": role, "instance": instance, "prompt": prompt}

    # ==================================================================
    # WAKE CHECK — monitor heartbeats (domain model: monitor heartbeats)
    # ==================================================================

    def check_wake(self, *, apply_tick: bool = False) -> dict:
        """Determine whether the kanban-lead session must wake.

        Returns a dict with wake_lead, must_spawn, lead_stale, reasons,
        and an optional tick report when apply_tick is True or activity warrants it.
        """
        board_path = self._wr / "board.json"
        action_path = self._wr / "action-state.json"
        lead_hb_path = self._wr / "heartbeat-kanban-lead.json"
        session_path = self._wr / "lead-cursor-session.json"

        reasons: list[str] = []
        intents = (_read_json(action_path) or {}) if action_path.is_file() else {}
        pending = intents.get("intents") or []
        if pending:
            reasons.append(f"action_intents:{len(pending)}")

        board = _read_json(board_path) or {}
        in_progress_roles: set[str] = set()
        for ticket in board.get("active") or []:
            for skill_id, prog in (ticket.get("skill_progress") or {}).items():
                if prog.get("execution_status") == "in_progress":
                    role = prog.get("agent")
                    if role:
                        in_progress_roles.add(role)
                        hb_path = self._wr / f"heartbeat-{role}.json"
                        hb_raw = _read_json(hb_path)
                        hb = hb_raw if isinstance(hb_raw, dict) else None
                        if hb is None:
                            reasons.append(f"no_heartbeat:{role}:{skill_id}")
                        else:
                            age = self._hb_age(hb.get("ts"))
                            status = hb.get("status")
                            if age is None or age > self.EXECUTOR_STALE_SECS:
                                reasons.append(f"stale_executor:{role}")
                            elif status not in ("working", "reserved", "ready"):
                                reasons.append(f"executor_not_working:{role}:{status}")

        lead_hb = _read_json(lead_hb_path)
        lead_age = self._hb_age(lead_hb.get("ts") if isinstance(lead_hb, dict) else None)
        lead_stale = lead_age is None or lead_age > self.LEAD_STALE_SECS

        tick_report: dict | None = None
        if apply_tick or pending or in_progress_roles:
            tick_report = self.run_tick()

        must_spawn = bool(tick_report and tick_report.get("must_spawn"))
        if must_spawn:
            for s in (tick_report.get("spawns") or []):
                reasons.append(f"must_spawn:{s.get('role')}")

        wake_lead = bool(pending) or must_spawn or lead_stale or any(
            r.startswith("no_heartbeat:") or r.startswith("stale_executor:") for r in reasons
        )

        cursor_session: str | None = None
        if session_path.is_file():
            raw = _read_json(session_path)
            cursor_session = (raw or {}).get("cursor_agent_id") if isinstance(raw, dict) else None

        return {
            "wake_lead": wake_lead,
            "must_spawn": must_spawn,
            "lead_stale": lead_stale,
            "lead_age_seconds": lead_age,
            "reasons": reasons,
            "cursor_agent_id": cursor_session,
            "tick": tick_report,
        }

    @staticmethod
    def _hb_age(ts: str | None) -> float | None:
        if not ts:
            return None
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return (datetime.now(timezone.utc) - dt).total_seconds()
        except ValueError:
            return None

    # ==================================================================
    # PULL DIAGNOSTICS — explain eligibility per role (domain model: manage kanban board)
    # ==================================================================

    def pull_diagnostics(self) -> dict:
        """Return per-role pull eligibility report for all active tickets."""
        board, kb, kb_block = self._resolve_board_and_config()
        team = load_team(board, kb_block)
        active = [Ticket.from_dict(t) for t in board.get("active", [])]
        backlog = board.get("backlog", [])

        report: dict = {
            "active_tickets": len(active),
            "backlog_tickets": len(backlog),
            "roles": {},
        }

        for role in ROLES:
            if role not in team:
                continue
            eligible = kb.list_eligible_pulls(active, role)
            in_prog = count_in_progress_for_role(active, role)
            working = count_working_agents(self._wr, role)
            live = count_live_agents(self._wr, role)
            ticket_detail = [self._explain_pull_eligibility(t, kb, role) for t in active]

            report["roles"][role] = {
                "team": team[role],
                "live_agents": live,
                "working_agents": working,
                "in_progress": in_prog,
                "eligible_pulls": eligible,
                "dead_slots_need_spawn": max(0, team[role] - live),
                "idle_agents_need_dispatch": max(0, live - working),
                "active_tickets": ticket_detail,
            }

        return report

    @staticmethod
    def _explain_pull_eligibility(ticket: Ticket, kb: KanbanBoard, role: str) -> dict:
        """Explain why a ticket is or is not pullable for a role."""
        stage_def = next((s for s in kb.stages if s.name == ticket.stage), None)
        if stage_def is None:
            return {
                "ticket_id": ticket.ticket_id,
                "stage": ticket.stage,
                "next_for_role": None,
                "blockers": ["unknown_stage"],
            }

        blockers: list[str] = []
        next_skill: str | None = None
        for skill_def in stage_def.stage_work_required:
            if skill_def.role != role:
                continue
            sp = ticket.skill_progress.get(skill_def.skill)
            if not stage_def.priors_done(ticket, skill_def.skill):
                blockers.append(f"priors_incomplete_before:{skill_def.skill}")
                break
            if sp is not None and sp.is_done():
                continue
            if sp is None or sp.is_claimable():
                next_skill = skill_def.skill
                break
            blockers.append(f"in_progress:{skill_def.skill}")
            break

        return {
            "ticket_id": ticket.ticket_id,
            "stage": ticket.stage,
            "priority": ticket.priority,
            "scope_level": ticket.scope_level,
            "any_in_progress": ticket.has_skill_in_progress(),
            "next_for_role": next_skill,
            "blockers": blockers,
        }

    # ==================================================================
    # METRICS — compute delivery cycle metrics (domain model: manage kanban board)
    # ==================================================================

    def compute_metrics(self) -> dict:
        """Compute cycle time, bottleneck, and throughput metrics from board state."""
        from collections import defaultdict
        board, kb, _ = self._resolve_board_and_config()

        all_tickets: list[Ticket] = []
        for lst in ("active", "done", "archived"):
            for raw in board.get(lst, []):
                if isinstance(raw, dict) and "ticket_id" in raw:
                    all_tickets.append(Ticket.from_dict(raw))

        stage_cycle_times: dict[str, list[float]] = defaultdict(list)
        skill_durations: dict[str, list[float]] = defaultdict(list)
        scope_cycle_times: dict[str, list[float]] = defaultdict(list)

        for ticket in all_tickets:
            entered = self._parse_iso(ticket.entered_stage)
            completed = self._parse_iso(ticket.completed_stage)
            if entered and completed:
                hours = (completed - entered).total_seconds() / 3600.0
                stage_cycle_times[ticket.stage].append(hours)
                scope_cycle_times[ticket.scope_level].append(hours)
            for skill_name, sp in ticket.skill_progress.items():
                start = self._parse_iso(sp.start)
                end = self._parse_iso(sp.end)
                if start and end:
                    skill_durations[skill_name].append(
                        (end - start).total_seconds() / 3600.0
                    )

        active_tickets = [Ticket.from_dict(t) for t in board.get("active", [])]
        stage_wip: dict[str, int] = defaultdict(int)
        skill_wip: dict[str, int] = defaultdict(int)
        bottlenecks: list[dict] = []

        for ticket in active_tickets:
            stage_wip[ticket.stage] += 1
            stage_def = kb.get_stage(ticket.stage)
            if stage_def:
                for skill_def in stage_def.stage_work_required:
                    sp = ticket.skill_progress.get(skill_def.skill)
                    if sp is None or sp.execution_status == "not_started":
                        skill_wip[f"{ticket.stage}:{skill_def.skill}"] += 1

        if stage_wip:
            max_stage = max(stage_wip, key=stage_wip.__getitem__)
            if stage_wip[max_stage] > 1:
                bottlenecks.append({"type": "stage_wip", "stage": max_stage, "count": stage_wip[max_stage]})
        if skill_wip:
            max_skill = max(skill_wip, key=skill_wip.__getitem__)
            if skill_wip[max_skill] > 2:
                bottlenecks.append({"type": "skill_waiting", "skill": max_skill, "count": skill_wip[max_skill]})

        def _stats(values: list[float]) -> dict:
            if not values:
                return {"count": 0}
            return {
                "count": len(values),
                "avg_hours": round(sum(values) / len(values), 2),
                "min_hours": round(min(values), 2),
                "max_hours": round(max(values), 2),
            }

        return {
            "stage_cycle_times": {k: _stats(v) for k, v in stage_cycle_times.items()},
            "scope_cycle_times": {k: _stats(v) for k, v in scope_cycle_times.items()},
            "skill_durations": {k: _stats(v) for k, v in skill_durations.items()},
            "bottlenecks": bottlenecks,
            "active_tickets": len(active_tickets),
            "backlog_tickets": len(board.get("backlog", [])),
            "archived_tickets": len(board.get("archived", [])),
        }

    @staticmethod
    def _parse_iso(s: str | None) -> datetime | None:
        if not s:
            return None
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None

    # ==================================================================
    # REPAIR SCATTER — fix incomplete parent scatters (domain model: trigger scatter)
    # ==================================================================

    def repair_partial_scatter(self, parent_id: str) -> list[str]:
        """Add any missing child tickets when a scatter left children out."""
        board = load_board(self._workspace)
        parent: Ticket | None = None
        for raw in board.get("archived", []):
            if raw.get("ticket_id") == parent_id:
                parent = Ticket.from_dict(raw)
                break
        if parent is None:
            raise ValueError(f"Archived parent not found: {parent_id}")

        spec = self._children_spec_for_ticket(parent)
        existing = (
            {t.get("ticket_id") for t in board.get("backlog", [])}
            | {t.get("ticket_id") for t in board.get("active", [])}
            | {t.get("ticket_id") for t in board.get("done", [])}
        )

        added: list[str] = []
        backlog = board.get("backlog", [])
        ts = now_iso()

        for child in spec:
            cid = child["id"]
            if cid in existing:
                continue
            ticket = Ticket(
                ticket_id=cid,
                lineage=parent.lineage + [child.get("name", cid)],
                scope_level="increment",
                stage="exploration",
                priority=child.get("priority", 1),
                created=ts,
                scatter_from=parent_id,
                entered_stage=ts,
            )
            backlog.append(ticket.to_dict())
            added.append(cid)

        if added:
            backlog.sort(key=lambda t: t.get("priority", 99))
            board["backlog"] = backlog
            parent.scatter_to = [c["id"] for c in spec]
            for i, raw in enumerate(board["archived"]):
                if raw.get("ticket_id") == parent_id:
                    board["archived"][i] = parent.to_dict()
                    break
            save_board(self._workspace, board)

        return added
