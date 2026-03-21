#!/usr/bin/env python3
"""
Autonomous orchestration loop (builder / runner / critic).

- **Runner (role 2):** executes Phase 0 audit, modeling_kind heuristics, validator (--golden), bundle manifest.
- **Critic (role 3):** domain + OO heuristics via `critic_mm3_domain.py` + `rules/mm3_domain_critic.json`.
- **Planner (role 1):** next-step plan — either deterministic markdown, or HTTP POST to ORCHESTRATOR_AGENT_URL.

Environment (optional API — you host the server that calls your LLM agents):

- ORCHESTRATOR_AGENT_URL — POST JSON `{ "role": "planner"|"critic_review", "iteration": N, "critic": {...}, "runner_log": [...] }`
  Response: `{ "plan_markdown": "..." }` for planner; critic_review is optional.

Without the URL, planner/critic_review fall back to built-in templates so the loop never blocks.

Runs **min_iterations**–**max_iterations** (default 10–20) or stops early if **--stop-on-score** threshold met.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ORCH = ROOT / "test" / "mm3" / "orchestration"
DEFAULT_MODEL_GLOB = [
    ROOT / "test" / "mm3" / "maps-models-specs" / "map-model-spec.md",
    ROOT / "test" / "mm3" / "maps-models-specs" / "map-model-spec.json",
]


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd= cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out[-8000:]


def _remote_planner(iteration: int, critic: dict, runner_log: list[dict]) -> str | None:
    url = os.environ.get("ORCHESTRATOR_AGENT_URL")
    if not url:
        return None
    payload = {
        "role": "planner",
        "iteration": iteration,
        "critic": critic,
        "runner_log": runner_log,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            body = json.loads(r.read().decode("utf-8"))
        return body.get("plan_markdown") or body.get("plan") or ""
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as e:
        return f"*API planner failed ({e}); using deterministic plan.*\n\n"


def deterministic_plan(iteration: int, critic: dict, pipeline_ok: bool) -> str:
    score = critic.get("overall_score", 0)
    lines = [
        f"## Plan — iteration {iteration}",
        f"- **Time:** {datetime.now(timezone.utc).isoformat()}",
        f"- **Pipeline OK:** {pipeline_ok}",
        f"- **Critic overall_score:** {score}",
        "",
        "### Next actions",
        "1. Keep runner green: `phase0_audit` → `apply_modeling_kind_heuristics` → `validate` (--golden) → `generate_context_bundle_manifest`.",
        "2. Add or extend `test/mm3/maps-models-specs/map-model-spec.md` (or `.json`) so **checks / traits / powers / effects** separation can be scored against `rules/mm3_domain_critic.json`.",
        "3. Align promoted types with `test/mm3/maps-models-specs/mm3_target_ontology.json` (reference, not TOC).",
        "",
        "### Critic recommendations",
    ]
    for r in critic.get("recommendations", [])[:12]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("### Invariant status")
    for inv in critic.get("invariants", []):
        lines.append(f"- **{inv['id']}**: {inv['status']} (score {inv.get('score')})")
    return "\n".join(lines)


def run_pipeline() -> tuple[bool, list[dict]]:
    log: list[dict] = []
    ok = True
    steps = [
        [sys.executable, str(SCRIPTS / "phase0_audit.py")],
        [sys.executable, str(SCRIPTS / "apply_modeling_kind_heuristics.py")],
        [sys.executable, str(SCRIPTS / "validate_modeling_kind_sidecar.py"), "--golden"],
        [sys.executable, str(SCRIPTS / "generate_context_bundle_manifest.py")],
    ]
    for cmd in steps:
        code, out = _run(cmd, ROOT)
        log.append({"cmd": cmd, "exit": code, "tail": out[-2000:]})
        if code != 0:
            ok = False
    return ok, log


def critic_command(model_paths: list[Path], pipeline_ok: bool, out_json: Path) -> tuple[int, dict]:
    cmd = [
        sys.executable,
        str(SCRIPTS / "critic_mm3_domain.py"),
        "--json-out",
        str(out_json),
    ]
    if pipeline_ok:
        cmd.append("--pipeline-ok")
    for mp in model_paths:
        if mp.is_file():
            cmd.extend(["--model", str(mp)])
    code, _ = _run(cmd, ROOT)
    data = json.loads(out_json.read_text(encoding="utf-8")) if out_json.is_file() else {}
    return code, data


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-iterations", type=int, default=10)
    ap.add_argument("--max-iterations", type=int, default=20)
    ap.add_argument("--stop-on-score", type=float, default=0.92, help="Stop early if critic score >= this and pipeline OK")
    ap.add_argument("--no-early-stop", action="store_true", help="Always run max-iterations")
    args = ap.parse_args()

    if args.min_iterations < 1 or args.max_iterations < args.min_iterations:
        print("Invalid iteration range", file=sys.stderr)
        return 2

    ORCH.mkdir(parents=True, exist_ok=True)
    plans = ORCH / "plans"
    critic_dir = ORCH / "critic"
    runner_dir = ORCH / "runner"
    plans.mkdir(exist_ok=True)
    critic_dir.mkdir(exist_ok=True)
    runner_dir.mkdir(exist_ok=True)

    state_path = ORCH / "state.json"
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    model_paths: list[Path] = []
    for p in DEFAULT_MODEL_GLOB:
        if p.is_file():
            model_paths.append(p)

    summary: list[dict] = []
    stop_reason: str | None = None

    for it in range(1, args.max_iterations + 1):
        pipeline_ok, runner_log = run_pipeline()
        (runner_dir / f"runner_{it:03d}.json").write_text(
            json.dumps({"iteration": it, "pipeline_ok": pipeline_ok, "log": runner_log}, indent=2),
            encoding="utf-8",
        )

        critic_json = critic_dir / f"critic_{it:03d}.json"
        ccode, critic = critic_command(model_paths, pipeline_ok, critic_json)

        prefix = _remote_planner(it, critic, runner_log)
        plan_body = deterministic_plan(it, critic, pipeline_ok)
        if prefix:
            plan_body = prefix + "\n" + plan_body
        (plans / f"plan_{it:03d}.md").write_text(plan_body, encoding="utf-8")

        row = {
            "iteration": it,
            "pipeline_ok": pipeline_ok,
            "critic_exit": ccode,
            "overall_score": critic.get("overall_score"),
            "critic_json": str(critic_json),
        }
        summary.append(row)

        score = float(critic.get("overall_score") or 0)
        if (
            not args.no_early_stop
            and it >= args.min_iterations
            and pipeline_ok
            and score >= args.stop_on_score
        ):
            stop_reason = "score_threshold"
        else:
            stop_reason = None

        state_path.write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "last_iteration": it,
                    "last_summary": row,
                    "stop_reason": stop_reason,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        if stop_reason:
            break

    if stop_reason is None and summary:
        stop_reason = "max_iterations"
        state_path.write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "last_iteration": summary[-1]["iteration"],
                    "last_summary": summary[-1],
                    "stop_reason": stop_reason,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    (ORCH / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Orchestration complete. Summary:", json.dumps(summary[-3:], indent=2))
    print("State:", state_path)
    return 0 if summary and summary[-1].get("pipeline_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
