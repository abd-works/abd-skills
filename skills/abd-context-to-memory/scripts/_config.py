"""Shared config: ROOT and MEMORY paths. Env CONTENT_MEMORY_ROOT overrides skill-config."""
import json
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPTS.parent
# Repo root: agilebydesign-skills/ (parent of skills/)
_SKILLS_REPO_ROOT = _SKILL_ROOT.parent.parent

# Load env: repo conf/ (.secrets, .env), then skill .env, then cwd .env (overrides)
try:
    from dotenv import load_dotenv

    # Repo conf wins over stale OPENAI_API_KEY inherited from the shell / OS env.
    _conf_dir = _SKILLS_REPO_ROOT / "conf"
    for fname in (".secrets", ".env"):
        _env_path = _conf_dir / fname
        if _env_path.exists():
            load_dotenv(_env_path, override=True)
    _skill_env = _SKILL_ROOT / ".env"
    if _skill_env.exists():
        load_dotenv(_skill_env, override=True)
    # Project cwd .env last — overrides repo conf for per-project keys
    _cwd_env = Path.cwd() / ".env"
    if _cwd_env.exists():
        load_dotenv(_cwd_env, override=True)
except ImportError:
    pass


def _expand_path(p: str) -> Path:
    """Expand ~ for portability (each user's home). Supports %VAR% on Windows."""
    s = p.strip()
    # Expand %VAR% (Windows)
    while "%" in s:
        i = s.find("%")
        j = s.find("%", i + 1)
        if j == -1:
            break
        var = s[i + 1 : j]
        val = os.environ.get(var, "")
        s = s[:i] + val + s[j + 1 :]
    return Path(s).expanduser()


def _get_root() -> Path:
    if "CONTENT_MEMORY_ROOT" in os.environ:
        return _expand_path(os.environ["CONTENT_MEMORY_ROOT"])
    config_path = _SKILL_ROOT / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            if "content_memory_root" in cfg:
                return _expand_path(str(cfg["content_memory_root"]))
        except (json.JSONDecodeError, OSError):
            pass
    return Path.cwd()


def _get_skill_space_path() -> Path | None:
    """Skill workspace root (mandatory for cross-skill resolution when set). Priority:
    1. SOLUTION_WORKSPACE env
    2. SKILL_SPACE_PATH env (legacy alias)
    3. Project conf/abd-config.json (cwd or parents) — active_skill_workspace, then solution_workspace, skill_space_path
    4. skill-config.json — same keys
    5. abd-story-synthesizer conf/abd-config.json (skills repo fallback)
    """
    if "SOLUTION_WORKSPACE" in os.environ:
        return _expand_path(os.environ["SOLUTION_WORKSPACE"])
    if "SKILL_SPACE_PATH" in os.environ:
        return _expand_path(os.environ["SKILL_SPACE_PATH"])

    def _root_from_abd(cfg: dict) -> str | None:
        sw = cfg.get("solution_workspace") or cfg.get("skill_space_path")
        if sw is None or (isinstance(sw, str) and not str(sw).strip()):
            return None
        return str(sw).strip()

    # Check project config: conf/abd-config.json in cwd or parent dirs (when running from project)
    for check in [Path.cwd(), Path.cwd().parent]:
        abd_config = check / "conf" / "abd-config.json"
        if abd_config.exists():
            try:
                with open(abd_config, encoding="utf-8") as f:
                    cfg = json.load(f)
                r = _root_from_abd(cfg)
                if r:
                    return _expand_path(r)
            except (json.JSONDecodeError, OSError):
                pass
    config_path = _SKILL_ROOT / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            for key in ("active_skill_workspace", "solution_workspace", "skill_space_path"):
                if key in cfg and str(cfg[key]).strip():
                    return _expand_path(str(cfg[key]))
        except (json.JSONDecodeError, OSError):
            pass
    # Fallback: sibling abd-story-synthesizer conf (skills repo)
    abd_config = _SKILL_ROOT.parent / "abd-story-synthesizer" / "conf" / "abd-config.json"
    if abd_config.exists():
        try:
            with open(abd_config, encoding="utf-8") as f:
                cfg = json.load(f)
            r = _root_from_abd(cfg)
            if r:
                return _expand_path(r)
        except (json.JSONDecodeError, OSError):
            pass
    return None


def get_default_context_folder() -> Path | None:
    """When solution workspace (see `_get_skill_space_path`) is set and no folder specified, use `<workspace>/context`.

    Returns None if no workspace is resolved."""
    base = _get_skill_space_path()
    if base is None:
        return None
    return base / "context"


def ensure_root() -> None:
    """If ROOT does not exist, prompt user to set CONTENT_MEMORY_ROOT. Exit if unclear."""
    if ROOT.exists():
        return
    print("Memory path not found:", ROOT, file=sys.stderr)
    print("\nSet CONTENT_MEMORY_ROOT to the folder where memory should be stored.", file=sys.stderr)
    print("  Typically: the parent of your context/source folder (e.g. project root).", file=sys.stderr)
    print("  Example: set CONTENT_MEMORY_ROOT=C:\\dev\\my-project", file=sys.stderr)
    print("\nWhen running the full pipeline with --path, ROOT is derived from the source path.", file=sys.stderr)
    sys.exit(1)


ROOT = _get_root()
MEMORY = ROOT / "memory"


def _paths_same(a: Path, b: Path) -> bool:
    """Best-effort same path on Windows (case, resolve)."""
    try:
        return str(a.resolve()).casefold() == str(b.resolve()).casefold()
    except OSError:
        return str(a).strip().casefold() == str(b).strip().casefold()


def _walk_up_find_existing(rel_paths: tuple[str, ...], *, max_depth: int = 48) -> Path | None:
    """From cwd, walk parents; return first path that exists."""
    cur = Path.cwd().resolve()
    for _ in range(max_depth):
        for rel in rel_paths:
            p = cur / rel
            if p.is_file():
                return p
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def _resolve_content_memory_roots_path() -> Path | None:
    """Path to the workspace hub list JSON.

    **Production hubs belong in the workspace** (e.g. ``<workspace>/conf/content_memory_roots.json``),
    not in the skill repo. Resolution order:

    1. ``CONTENT_MEMORY_ROOTS_CONFIG`` — absolute path to the JSON file.
    2. ``CONTENT_MEMORY_WORKSPACE`` — directory; then ``<dir>/conf/content_memory_roots.json``
       or ``<dir>/content_memory_roots.json``.
    3. ``CONTENT_MEMORY_ROOT`` — hub root; then ``<root>/conf/content_memory_roots.json`` or
       ``<root>/content_memory_roots.json`` (typical when running embed with hub env set).
    4. Walk **cwd** upward for ``conf/content_memory_roots.json``, then ``content_memory_roots.json``.
    5. Walk **cwd** for ``conf/content_memory_workspace.json``; if found, read ``workspace_root``
       (or ``root`` / ``path``) and load ``<that>/conf/content_memory_roots.json``.
    6. No file in the skill package (use ``content_memory_roots.example.json`` as a template only).
    """
    e = os.environ.get("CONTENT_MEMORY_ROOTS_CONFIG", "").strip()
    if e:
        p = _expand_path(e)
        return p if p.is_file() else None

    ws = os.environ.get("CONTENT_MEMORY_WORKSPACE", "").strip()
    if ws:
        base = _expand_path(ws)
        for rel in ("conf/content_memory_roots.json", "content_memory_roots.json"):
            cand = base / rel
            if cand.is_file():
                return cand

    if "CONTENT_MEMORY_ROOT" in os.environ:
        base = _expand_path(os.environ["CONTENT_MEMORY_ROOT"])
        for rel in ("conf/content_memory_roots.json", "content_memory_roots.json"):
            cand = base / rel
            if cand.is_file():
                return cand

    found = _walk_up_find_existing(
        ("conf/content_memory_roots.json", "content_memory_roots.json")
    )
    if found is not None:
        return found

    ptr = _walk_up_find_existing(("conf/content_memory_workspace.json",))
    if ptr is not None and ptr.is_file():
        try:
            with open(ptr, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                raw = data.get("workspace_root") or data.get("root") or data.get("path")
                if raw:
                    base = _expand_path(str(raw))
                    for rel in ("conf/content_memory_roots.json", "content_memory_roots.json"):
                        cand = base / rel
                        if cand.is_file():
                            return cand
        except (json.JSONDecodeError, OSError):
            pass

    return None


def _load_roots_entries() -> list[dict]:
    """Entries from workspace ``content_memory_roots.json`` (optional)."""
    path = _resolve_content_memory_roots_path()
    if path is None or not path.is_file():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("roots") if isinstance(data, dict) else []
    except (json.JSONDecodeError, OSError):
        return []


def hub_entry_for_root(root: Path) -> dict | None:
    """Matching row from ``content_memory_roots.json`` for this hub root, or None."""
    root = root.resolve()
    for entry in _load_roots_entries():
        if not isinstance(entry, dict):
            continue
        p = entry.get("path")
        if not p:
            continue
        if _paths_same(_expand_path(str(p)), root):
            return entry
    return None


def junctions_dir_for_root(root: Path) -> str:
    """Subdirectory under the hub where topic junctions live (not SharePoint).

    **Junction-only hubs:** each entry in ``content_memory_roots.json`` may set
    ``junctions_dir`` (default ``assets``). Override for a run with
    ``CONTENT_MEMORY_JUNCTIONS_DIR`` (applies to current ``CONTENT_MEMORY_ROOT``).
    """
    env = os.environ.get("CONTENT_MEMORY_JUNCTIONS_DIR", "").strip()
    if env:
        s = env.replace("\\", "/").strip("/")
        return s.split("/")[-1] if s else "assets"
    entry = hub_entry_for_root(root)
    if entry:
        jd = entry.get("junctions_dir")
        if isinstance(jd, str):
            t = jd.strip().strip("/\\")
            if t:
                return t
    return "assets"


# Topic junctions + legacy convert/chunk paths under hub (name is historical).
ASSETS = ROOT / junctions_dir_for_root(ROOT)


def aggregate_rag_dir_for_root(root: Path) -> Path:
    """Where the **hub** (aggregate) FAISS bundle lives — configurable so it can sit on OneDrive/SharePoint.

    Priority:
    1. ``CONTENT_MEMORY_RAG_PATH`` env (absolute folder for ``index.faiss``, etc.).
    2. ``content_memory_rag_path`` in ``skill-config.json``.
    3. ``rag_path`` on the entry in ``conf/content_memory_roots.json`` whose ``path`` matches ``root``.
    4. Default: ``<root>/<junctions_dir>/rag`` (local fallback; production usually sets ``rag_path`` off-repo).

    Per-topic indexes (``--memory``) still use ``<root>/memory/rag`` — only the aggregate index is relocated.
    """
    if "CONTENT_MEMORY_RAG_PATH" in os.environ:
        return _expand_path(os.environ["CONTENT_MEMORY_RAG_PATH"])
    config_path = _SKILL_ROOT / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            if cfg.get("content_memory_rag_path"):
                return _expand_path(str(cfg["content_memory_rag_path"]))
        except (json.JSONDecodeError, OSError):
            pass
    root = root.resolve()
    for entry in _load_roots_entries():
        if not isinstance(entry, dict):
            continue
        p = entry.get("path")
        rp = entry.get("rag_path")
        if not p or not rp:
            continue
        if _paths_same(_expand_path(str(p)), root):
            return _expand_path(str(rp))
    return root / junctions_dir_for_root(root) / "rag"


def rag_dir_for_embed(memory_name: str | None) -> Path:
    """Where FAISS + embeddings are written.

    - **Aggregate** (no ``--memory``): configurable via :func:`aggregate_rag_dir_for_root`
      (default ``<ROOT>/<junctions_dir>/rag`` when no ``rag_path`` match).
    - **Per-topic** (``--memory <name>``): ``<ROOT>/memory/rag`` — index for that memory slice
      only (typical ``index_memory --path`` flow).
    """
    if memory_name:
        return MEMORY / "rag"
    return aggregate_rag_dir_for_root(ROOT)


def resolve_search_rag_dir() -> Path:
    """Which index ``search_memory`` should load: configured aggregate dir, else local hub fallback."""
    configured = aggregate_rag_dir_for_root(ROOT)
    if (configured / "index.faiss").exists():
        return configured
    local_hub_rag = ROOT / junctions_dir_for_root(ROOT) / "rag" / "index.faiss"
    legacy = MEMORY / "rag" / "index.faiss"
    if local_hub_rag.exists():
        return local_hub_rag.parent
    if legacy.exists():
        return MEMORY / "rag"
    return configured
