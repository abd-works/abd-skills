"""Miro board transport seam.

Lets the rest of this skill stay backend-agnostic: the orchestrator and
node classes call ``MiroTransport.create_item`` / ``list_items`` /
``delete_item`` without knowing whether the calls hit the real Miro API or
an in-memory fake. Production runs use ``RestMiroTransport``; tests and
``--dry-run`` use ``InMemoryMiroTransport``.

Two implementations are provided:

- ``RestMiroTransport`` — wraps Miro v2 board items
  (``https://api.miro.com/v2/boards/{board_id}/items``). Auth is a Bearer
  token from ``MIRO_ACCESS_TOKEN``. Network calls use ``urllib`` so the
  skill has no third-party dependency. Swap in ``requests`` later if you
  prefer richer error handling.
- ``InMemoryMiroTransport`` — keeps items in a dict keyed by a
  monotonically-increasing id; ``list_items`` returns them in insertion
  order. No network. Used by every test in ``tests/miro_story_sync``.
"""
from __future__ import annotations

import json
import os
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

__all__ = [
    'MiroItem',
    'MiroTransport',
    'InMemoryMiroTransport',
    'RestMiroTransport',
    'MiroTransportError',
]


@dataclass
class MiroItem:
    """A single Miro board item, normalized across transports.

    ``id`` is opaque — REST returns the Miro id; the in-memory transport
    issues sequential strings. ``cell_id`` is the cross-render stable key
    we set in metadata so re-rendering can match items by structural id.
    """

    id: str
    item_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    cell_id: str = ''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MiroItem':
        meta = data.get('metadata') or {}
        return cls(
            id=str(data.get('id', '')),
            item_type=str(data.get('type', '')),
            payload=data,
            cell_id=str(meta.get('story_sync_cell_id', '')),
        )


class MiroTransportError(RuntimeError):
    """Raised when a transport call fails."""


class MiroTransport(ABC):
    """Abstract Miro board transport.

    Concrete subclasses implement create / list / delete on a single board.
    Multi-board operations are out of scope (a Synchronizer talks to one
    board at a time).
    """

    @abstractmethod
    def create_item(self, item_type: str, payload: Dict[str, Any], *,
                    cell_id: str = '') -> MiroItem:
        """Create a single item; return the normalized ``MiroItem``."""

    @abstractmethod
    def list_items(self, *, cursor: Optional[str] = None) -> List[MiroItem]:
        """List every item on the board (handles pagination internally)."""

    @abstractmethod
    def delete_item(self, item_id: str) -> None:
        """Delete a single item by Miro id (no-op if missing)."""

    def replace_all(self, items_to_create: Iterable[Dict[str, Any]]) -> List[MiroItem]:
        """Convenience: clear the board, then create every item.

        Used by the outline render path. Subclasses that can do this more
        efficiently in a single call may override.
        """
        for existing in list(self.list_items()):
            self.delete_item(existing.id)
        specs = list(items_to_create)
        total = len(specs)
        created: List[MiroItem] = []
        for i, spec in enumerate(specs, 1):
            item = self.create_item(
                spec['item_type'],
                spec['payload'],
                cell_id=spec.get('cell_id', ''),
            )
            created.append(item)
            if i % 10 == 0 or i == total:
                print(f'[miro-story-sync] {i}/{total} items created', flush=True)
        return created


class InMemoryMiroTransport(MiroTransport):
    """In-process fake. Stores items in a dict; deterministic ids.

    Useful in two places: the test suite (no network, no token), and CLI
    ``--dry-run`` (lets you verify rendering without touching Miro).
    """

    def __init__(self) -> None:
        self._next_id = 0
        self._items: Dict[str, MiroItem] = {}

    @property
    def items(self) -> List[MiroItem]:
        return list(self._items.values())

    def create_item(self, item_type: str, payload: Dict[str, Any], *,
                    cell_id: str = '') -> MiroItem:
        self._next_id += 1
        item_id = f'mem-{self._next_id}'
        item = MiroItem(
            id=item_id,
            item_type=item_type,
            payload={**payload, 'id': item_id, 'type': item_type,
                     'metadata': {**(payload.get('metadata') or {}),
                                  'story_sync_cell_id': cell_id}},
            cell_id=cell_id,
        )
        self._items[item_id] = item
        return item

    def list_items(self, *, cursor: Optional[str] = None) -> List[MiroItem]:
        return list(self._items.values())

    def delete_item(self, item_id: str) -> None:
        self._items.pop(item_id, None)


class RestMiroTransport(MiroTransport):
    """Miro v2 REST transport using ``urllib`` (no third-party dependency).

    The board id is required at construction; the access token comes from
    ``MIRO_ACCESS_TOKEN`` unless explicitly passed. The base URL defaults to
    ``https://api.miro.com`` and is overridable so a local mock or proxy can
    be injected if needed.
    """

    DEFAULT_BASE_URL = 'https://api.miro.com'

    def __init__(self, board_id: str, *, access_token: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        if not board_id:
            raise ValueError('board_id is required')
        self._board_id = board_id
        self._token = access_token or os.environ.get('MIRO_ACCESS_TOKEN', '')
        if not self._token:
            raise MiroTransportError(
                'MIRO_ACCESS_TOKEN is not set; pass access_token= or use --dry-run.'
            )
        self._base_url = base_url or os.environ.get(
            'MIRO_API_BASE_URL', self.DEFAULT_BASE_URL
        )
        self._timeout = timeout
        self._checkpoint_path: Optional[Path] = None
        self._graph_hash: Optional[str] = None
        self._checkpoint_mode: Optional[str] = None
        self._resume_flag: bool = False

    @property
    def board_id(self) -> str:
        return self._board_id

    # ------------------------------------------------------------------
    # Checkpoint / resume
    # ------------------------------------------------------------------

    def setup_checkpoint(self, checkpoint_path: Path, graph_hash: str,
                         mode: str, resume: bool = False) -> None:
        """Configure checkpoint/resume for ``replace_all``.

        Call once from the CLI after building the transport, before rendering.
        Without calling this method ``replace_all`` behaves exactly as before.
        """
        self._checkpoint_path = checkpoint_path
        self._graph_hash = graph_hash
        self._checkpoint_mode = mode
        self._resume_flag = resume

    def _load_checkpoint(self) -> Optional[Dict[str, Any]]:
        if not self._checkpoint_path or not self._checkpoint_path.exists():
            return None
        try:
            return json.loads(self._checkpoint_path.read_text(encoding='utf-8'))
        except Exception:
            return None

    def _write_checkpoint(self, data: Dict[str, Any]) -> None:
        if not self._checkpoint_path:
            return
        try:
            self._checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            self._checkpoint_path.write_text(
                json.dumps(data, indent=2) + '\n', encoding='utf-8'
            )
        except Exception as exc:
            print(f'[miro-story-sync] WARNING: could not write checkpoint: {exc}', flush=True)

    def _checkpoint_matches(self, checkpoint: Dict[str, Any]) -> bool:
        return (
            checkpoint.get('board_id') == self._board_id
            and checkpoint.get('mode') == self._checkpoint_mode
            and checkpoint.get('graph_hash') == self._graph_hash
        )

    def replace_all(self, items_to_create: Iterable[Dict[str, Any]]) -> List[MiroItem]:
        """Clear board + create every item, with checkpoint/resume support.

        When ``setup_checkpoint`` has been called before this run:
        - A fresh run writes ``miro-sync-checkpoint.json`` and updates it after
          each successful create; if the process dies, the next run continues
          from where it left off without clearing already-created items.
        - When a matching ``in_progress`` checkpoint is found (same board, mode,
          and graph hash) the board-clear is skipped and creation resumes from
          the first un-created item.
        - A ``complete`` checkpoint is treated as a fresh run unless
          ``--resume`` was passed.
        """
        specs = list(items_to_create)
        total = len(specs)

        checkpoint = self._load_checkpoint() if self._checkpoint_path else None
        resume_ids: List[str] = []

        should_resume = (
            checkpoint is not None
            and self._checkpoint_matches(checkpoint)
            and (checkpoint.get('status') == 'in_progress' or self._resume_flag)
        )

        if should_resume:
            resume_ids = list(checkpoint.get('created_items') or [])
            resume_from = len(resume_ids)
            print(
                f'[miro-story-sync] Resuming from item {resume_from}/{total}',
                flush=True,
            )
            specs_to_create = specs[resume_from:]
        else:
            for existing in list(self.list_items()):
                self.delete_item(existing.id)
            resume_from = 0
            specs_to_create = specs
            self._write_checkpoint({
                'board_id': self._board_id,
                'mode': self._checkpoint_mode,
                'graph_hash': self._graph_hash,
                'total_items': total,
                'created_items': [],
                'status': 'in_progress',
            })

        created_ids = list(resume_ids)
        new_items: List[MiroItem] = []

        for i, spec in enumerate(specs_to_create, resume_from + 1):
            item = self.create_item(
                spec['item_type'],
                spec['payload'],
                cell_id=spec.get('cell_id', ''),
            )
            new_items.append(item)
            created_ids.append(item.id)
            self._write_checkpoint({
                'board_id': self._board_id,
                'mode': self._checkpoint_mode,
                'graph_hash': self._graph_hash,
                'total_items': total,
                'created_items': created_ids,
                'status': 'in_progress',
            })
            if i % 10 == 0 or i == total:
                print(f'[miro-story-sync] {i}/{total} items created', flush=True)

        self._write_checkpoint({
            'board_id': self._board_id,
            'mode': self._checkpoint_mode,
            'graph_hash': self._graph_hash,
            'total_items': total,
            'created_items': created_ids,
            'status': 'complete',
        })
        print(f'[miro-story-sync] Complete. {total} items on board.', flush=True)

        stubs = [MiroItem(id=mid, item_type='', payload={}, cell_id='') for mid in resume_ids]
        return stubs + new_items

    # Item types that support the Miro v2 'metadata' field.
    _METADATA_SUPPORTED = frozenset({'app_card'})

    def create_item(self, item_type: str, payload: Dict[str, Any], *,
                    cell_id: str = '') -> MiroItem:
        body = dict(payload)
        # Miro v2 only supports 'metadata' on app_card items.
        if item_type in self._METADATA_SUPPORTED:
            meta = dict(body.get('metadata') or {})
            if cell_id:
                meta['story_sync_cell_id'] = cell_id
            if meta:
                body['metadata'] = meta
        else:
            body.pop('metadata', None)
        url = f'{self._base_url}/v2/boards/{self._board_id}/{_endpoint_for(item_type)}'
        data = self._post(url, body)
        return MiroItem.from_dict(data)

    def list_items(self, *, cursor: Optional[str] = None) -> List[MiroItem]:
        items: List[MiroItem] = []
        next_cursor = cursor
        while True:
            url = f'{self._base_url}/v2/boards/{self._board_id}/items?limit=50'
            if next_cursor:
                url = f'{url}&cursor={next_cursor}'
            data = self._get(url)
            for raw in data.get('data') or []:
                items.append(MiroItem.from_dict(raw))
            next_cursor = (data.get('cursor') or '').strip()
            if not next_cursor:
                break
        return items

    def delete_item(self, item_id: str) -> None:
        url = f'{self._base_url}/v2/boards/{self._board_id}/items/{item_id}'
        try:
            self._delete(url)
        except MiroTransportError as exc:  # 404 is acceptable for delete-if-exists
            if '404' not in str(exc):
                raise

    # ------------------------------------------------------------------
    # HTTP plumbing
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self._token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def _post(self, url: str, body: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib_request.Request(
            url, data=json.dumps(body).encode('utf-8'),
            headers=self._headers(), method='POST',
        )
        return self._send(req)

    def _get(self, url: str) -> Dict[str, Any]:
        req = urllib_request.Request(url, headers=self._headers(), method='GET')
        return self._send(req)

    def _delete(self, url: str) -> Dict[str, Any]:
        req = urllib_request.Request(url, headers=self._headers(), method='DELETE')
        return self._send(req)

    def _send(self, req: urllib_request.Request, _retries: int = 3) -> Dict[str, Any]:
        for attempt in range(1, _retries + 1):
            try:
                with urllib_request.urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read().decode('utf-8') or '{}'
                if not raw.strip():
                    return {}
                return json.loads(raw)
            except urllib_error.HTTPError as exc:
                detail = ''
                try:
                    detail = exc.read().decode('utf-8')
                except Exception:
                    pass
                # 429 Too Many Requests — back off and retry with longer waits
                if exc.code == 429 and attempt < _retries:
                    wait = 15 * attempt  # 15s, 30s
                    print(f'[miro-story-sync] rate-limited, waiting {wait}s (attempt {attempt}/{_retries})', flush=True)
                    time.sleep(wait)
                    continue
                raise MiroTransportError(
                    f'Miro {req.get_method()} {req.full_url} failed '
                    f'with HTTP {exc.code}: {detail}'
                ) from exc
            except (urllib_error.URLError, TimeoutError, OSError) as exc:
                if attempt < _retries:
                    wait = 2 ** attempt
                    print(f'[miro-story-sync] network error ({exc}), retrying in {wait}s (attempt {attempt}/{_retries})', flush=True)
                    time.sleep(wait)
                    continue
                raise MiroTransportError(
                    f'Miro {req.get_method()} {req.full_url} failed: {exc}'
                ) from exc
        return {}


def _endpoint_for(item_type: str) -> str:
    """Map an item-type string to the Miro v2 endpoint suffix.

    Miro splits item creation across per-type endpoints: shapes go to
    ``/items``, sticky notes go to ``/sticky_notes``, etc. We default to the
    plural / generic ``/items`` endpoint, which covers shapes; per-type
    endpoints are wired here when needed.
    """
    if item_type == 'sticky_note':
        return 'sticky_notes'
    if item_type == 'shape':
        return 'shapes'
    if item_type == 'text':
        return 'texts'
    if item_type == 'frame':
        return 'frames'
    return 'items'
