"""CLI entry for running the delivery graph — ``run`` and ``resume``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic_skill_builder.graph import build_checkpointer, compile_delivery_graph
from agentic_skill_builder.state import initial_state


def _parse_interrupt(s: str | None) -> list[str] | None:
    if not s:
        return None
    return [x.strip() for x in s.split(",") if x.strip()]


def _cmd_run(ns: argparse.Namespace) -> int:
    cp = build_checkpointer(ns.sqlite)
    ib = _parse_interrupt(ns.interrupt_before)
    app = compile_delivery_graph(checkpointer=cp, interrupt_before=ib)

    state = initial_state(
        ns.skill_id,
        ns.skill_path,
        strategy_path=ns.strategy_file,
    )
    cfg = {"configurable": {"thread_id": ns.thread_id}}
    out = app.invoke(state, config=cfg)

    if ns.json_out:
        print(json.dumps(out, indent=2))
    else:
        print("Final trace:")
        for line in out.get("trace", []):
            print(f"  {line}")
        op = out.get("operator_report") or {}
        print("operator_report ok:", op.get("ok"))
        ex = out.get("expert_report") or {}
        if ex.get("skipped"):
            print("expert_report: skipped ({})".format(ex.get("reason", "n/a")))
        else:
            print("expert_report: model=", ex.get("model", "?"))
        sc = out.get("strategy_complete")
        if sc is not None:
            print("strategy_complete:", sc)

    return 0


def _cmd_resume(ns: argparse.Namespace) -> int:
    if ns.sqlite is None:
        print("resume requires --sqlite", file=sys.stderr)
        return 2
    cp = build_checkpointer(ns.sqlite)
    ib = _parse_interrupt(ns.interrupt_before)
    app = compile_delivery_graph(checkpointer=cp, interrupt_before=ib)
    cfg = {"configurable": {"thread_id": ns.thread_id}}
    out = app.invoke(None, config=cfg)

    if ns.json_out:
        print(json.dumps(out, indent=2))
    else:
        print("Resume trace:")
        for line in out.get("trace", []):
            print(f"  {line}")
        op = out.get("operator_report") or {}
        print("operator_report ok:", op.get("ok"))

    return 0


def _add_run_flags(sp: argparse.ArgumentParser) -> None:
    sp.add_argument(
        "--skill-id",
        default="stub-skill",
        help="Identifier for this run (default: stub-skill).",
    )
    sp.add_argument(
        "--skill-path",
        default=".",
        help="Target skill directory path (default: current directory).",
    )
    sp.add_argument(
        "--sqlite",
        type=Path,
        metavar="PATH",
        help="SQLite checkpoint file for durable resume; omit for in-memory only.",
    )
    sp.add_argument(
        "--thread-id",
        default="cli-main",
        help="Checkpoint thread id (default: cli-main). Use same id for resume.",
    )
    sp.add_argument(
        "--interrupt-before",
        metavar="NODES",
        help="Comma-separated node names to interrupt before (HITL), e.g. strategize,builder",
    )
    sp.add_argument(
        "--strategy-file",
        metavar="PATH",
        default=None,
        help="JSON file with build intent (overrides <skill-path>/conf/build-strategy.json).",
    )
    sp.add_argument("--json", action="store_true", dest="json_out")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # Default subcommand: ``run`` (same CLI as before: ``--skill-path`` without ``run``).
    if not argv:
        argv = ["run"]
    elif argv[0] not in ("run", "resume"):
        argv = ["run"] + argv

    p = argparse.ArgumentParser(
        description="Agentic skill builder — LangGraph delivery pipeline (builder / operator / expert).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Start a new delivery run.")
    _add_run_flags(run_p)

    res_p = sub.add_parser(
        "resume",
        help="Continue after interrupt_before (same --sqlite and --thread-id as the paused run).",
    )
    res_p.add_argument(
        "--sqlite",
        type=Path,
        required=True,
        metavar="PATH",
        help="Same SQLite file used for the interrupted run.",
    )
    res_p.add_argument(
        "--thread-id",
        default="cli-main",
        help="Same thread id as the interrupted run (default: cli-main).",
    )
    res_p.add_argument(
        "--interrupt-before",
        metavar="NODES",
        help="Must match the interrupt list used when the graph was compiled for the paused run.",
    )
    res_p.add_argument("--json", action="store_true", dest="json_out")

    args = p.parse_args(argv)
    if args.command == "run":
        return _cmd_run(args)
    if args.command == "resume":
        return _cmd_resume(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
