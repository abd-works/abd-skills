"""
Append pipeline-style log lines (same family as ``data/pipeline-full.log``) and tee stdout/stderr.

Use ``--log-file <path>`` from convert or chunk so each stage writes its own file (no interleaving).
"""

from __future__ import annotations

import io
import shlex
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, TextIO


def get_optional_log_file(argv: list[str] | None = None) -> Path | None:
    """Return path after ``--log-file`` if present and valid; does not mutate ``argv``."""
    argv = argv if argv is not None else sys.argv
    if "--log-file" not in argv:
        return None
    i = argv.index("--log-file")
    if i + 1 >= len(argv) or argv[i + 1].startswith("-"):
        return None
    return Path(argv[i + 1])


def _now_iso_local() -> str:
    """Similar to PowerShell ``Get-Date -Format o`` (round-trip ISO with offset)."""
    return datetime.now(timezone.utc).astimezone().isoformat()


def _wrap_stream_utf8(stream: TextIO) -> TextIO:
    """Replace a text stream with UTF-8 over the same buffer (Windows fallback)."""
    buf = getattr(stream, "buffer", None)
    if buf is None:
        return stream
    try:
        return io.TextIOWrapper(
            buf,
            encoding="utf-8",
            errors="replace",
            line_buffering=getattr(stream, "line_buffering", False),
        )
    except (OSError, ValueError, AttributeError, TypeError):
        return stream


def configure_stdio_utf8() -> None:
    """
    Use UTF-8 for stdout/stderr when supported (notably Windows, default cp1252).

    Avoids ``UnicodeEncodeError`` when printing paths that contain Greek, CJK, emoji, etc.
    Safe to call more than once.
    """
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, AttributeError, TypeError):
            pass
        enc = getattr(stream, "encoding", None) or ""
        if enc.lower() != "utf-8":
            try:
                setattr(sys, name, _wrap_stream_utf8(stream))
            except (OSError, ValueError, AttributeError, TypeError):
                pass


def _ascii_fallback(s: str) -> str:
    return s.encode("ascii", errors="backslashreplace").decode("ascii")


class _Utf8LogSink:
    """
    Append-only log: every write is encoded as UTF-8 bytes.

    Avoids TextIOWrapper/platform quirks (e.g. Windows) that can produce mojibake or
    mixed encodings when the same path is teed from stdout/stderr.
    """

    __slots__ = ("_fh",)

    def __init__(self, path: Path) -> None:
        self._fh = open(path, "ab")

    def write(self, s: str) -> int:
        if not s:
            return 0
        self._fh.write(s.encode("utf-8", errors="replace"))
        self._fh.flush()
        return len(s)

    def flush(self) -> None:
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()


def safe_print(*args, **kwargs) -> None:
    """
    Print like ``print`` but never raise ``UnicodeEncodeError`` (e.g. cp1252 console + Greek paths).
    """
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = tuple(_ascii_fallback(str(a)) for a in args)
        try:
            print(*safe_args, **kwargs)
        except Exception:
            pass


class _Tee:
    __slots__ = ("_primary", "_secondary")

    def __init__(self, primary, secondary) -> None:
        self._primary = primary
        self._secondary = secondary

    def write(self, s: str) -> int:
        n = 0
        for target in (self._primary, self._secondary):
            try:
                n = target.write(s)
            except UnicodeEncodeError:
                try:
                    n = target.write(_ascii_fallback(s))
                except Exception:
                    n = len(s)
            try:
                target.flush()
            except Exception:
                pass
        return n

    def flush(self) -> None:
        self._primary.flush()
        self._secondary.flush()

    def isatty(self) -> bool:
        return self._primary.isatty()


@contextmanager
def pipeline_log_session(
    log_path: Path | str,
    stage_name: str,
    argv_list: list[str] | None = None,
) -> Iterator[None]:
    """
    Append START line, tee stdout/stderr to the log file, then append END line with exit code.

    Log bytes are always UTF-8 (binary append + explicit encode). Unbuffered process output
    (``python -u`` or ``PYTHONUNBUFFERED=1``) keeps the console current under Tee.
    """
    configure_stdio_utf8()
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    argv_list = argv_list if argv_list is not None else sys.argv
    argv_repr = " ".join(shlex.quote(a) for a in argv_list)
    start = f"=== {_now_iso_local()} START {stage_name} {argv_repr} ===\n"
    sink: _Utf8LogSink | None = None
    code = 0
    try:
        sink = _Utf8LogSink(log_path)
        sink.write(start)
        saved_out, saved_err = sys.stdout, sys.stderr
        sys.stdout = _Tee(saved_out, sink)
        sys.stderr = _Tee(saved_err, sink)
        try:
            yield
        except SystemExit as e:
            if isinstance(e.code, int):
                code = e.code
            elif e.code is None:
                code = 0
            else:
                code = 1
            raise
        except Exception:
            code = 1
            raise
        finally:
            sys.stdout = saved_out
            sys.stderr = saved_err
    finally:
        end = f"=== {_now_iso_local()} END {stage_name} (exit {code}) ===\n"
        if sink is not None:
            try:
                sink.write(end)
            finally:
                sink.close()
