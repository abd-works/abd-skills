"""Shared lock and digest helpers for story/domain/ux graph CLIs."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

STALE_LOCK_SECONDS = 300


def parse_json_text(text: str) -> Any:
    return json.loads(text)


def read_json_text_file(target: Path) -> Any:
    return parse_json_text(target.read_text(encoding="utf-8"))


def write_json_text_file(target: Path, graph: Dict[str, Any]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(target: Path) -> str:
    digest = hashlib.sha256()
    with target.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lock_path_for(target: Path) -> Path:
    return target.with_name(target.name + ".lock")


def read_lock_payload(lock: Path) -> Dict[str, Any]:
    try:
        return json.loads(lock.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def release_write_lock(lock: Path | None) -> None:
    if lock is None:
        return
    try:
        lock.unlink()
    except FileNotFoundError:
        return


def _lock_payload_bytes() -> bytes:
    host = os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or ""
    return json.dumps({
        "pid": os.getpid(),
        "acquired_at": time.time(),
        "host": host,
    }).encode("utf-8")


def _create_exclusive_lock(lock: Path) -> int:
    return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)


def _write_lock_descriptor(lock_fd: int, payload: bytes) -> None:
    try:
        os.write(lock_fd, payload)
    finally:
        os.close(lock_fd)


def _lock_age_seconds(existing: Dict[str, Any]) -> float:
    if "acquired_at" not in existing:
        return 0.0
    return time.time() - float(existing["acquired_at"] or 0)


def _refuse_live_lock(lock: Path, existing: Dict[str, Any], age_seconds: float) -> None:
    print(
        f"[error] concurrent write refused: lock {lock} is held by "
        f"pid={existing.get('pid')} (age={int(age_seconds)}s).",
        file=sys.stderr,
    )
    sys.exit(4)


def _refuse_stale_retry(lock: Path, existing: Dict[str, Any], age_seconds: float) -> None:
    print(
        f"[error] could not acquire lock {lock} "
        f"(held by pid={existing.get('pid')}, age={int(age_seconds)}s).",
        file=sys.stderr,
    )
    sys.exit(4)


def _open_lock_after_stale_removal(lock: Path) -> None:
    lock_fd = _create_exclusive_lock(lock)
    _write_lock_descriptor(lock_fd, _lock_payload_bytes())


def _handle_existing_lock(lock: Path, *, force: bool) -> None:
    existing = read_lock_payload(lock)
    age_seconds = _lock_age_seconds(existing)
    if age_seconds > STALE_LOCK_SECONDS or force:
        try:
            lock.unlink()
        except FileNotFoundError:
            return
        try:
            _open_lock_after_stale_removal(lock)
        except FileExistsError:
            _refuse_stale_retry(lock, existing, age_seconds)
        return
    _refuse_live_lock(lock, existing, age_seconds)


def acquire_write_lock(target: Path, *, force: bool) -> Path:
    lock = lock_path_for(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock_fd = _create_exclusive_lock(lock)
    except FileExistsError:
        _handle_existing_lock(lock, force=force)
        return lock
    _write_lock_descriptor(lock_fd, _lock_payload_bytes())
    return lock


def names_matching_substring(names: list[str], substring: str) -> list[str]:
    needle = (substring or "").lower()
    return [name for name in names if needle in name.lower()]
