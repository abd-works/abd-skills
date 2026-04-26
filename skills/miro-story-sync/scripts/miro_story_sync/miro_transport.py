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
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
        created: List[MiroItem] = []
        for spec in items_to_create:
            created.append(self.create_item(
                spec['item_type'],
                spec['payload'],
                cell_id=spec.get('cell_id', ''),
            ))
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
                 timeout: float = 15.0) -> None:
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

    @property
    def board_id(self) -> str:
        return self._board_id

    def create_item(self, item_type: str, payload: Dict[str, Any], *,
                    cell_id: str = '') -> MiroItem:
        body = dict(payload)
        # Embed the cross-render stable key as a metadata tag so re-renders
        # and `report` can match items even when Miro reissues IDs.
        meta = dict(body.get('metadata') or {})
        if cell_id:
            meta['story_sync_cell_id'] = cell_id
        if meta:
            body['metadata'] = meta
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

    def _send(self, req: urllib_request.Request) -> Dict[str, Any]:
        try:
            with urllib_request.urlopen(req, timeout=self._timeout) as resp:
                raw = resp.read().decode('utf-8') or '{}'
        except urllib_error.HTTPError as exc:
            detail = ''
            try:
                detail = exc.read().decode('utf-8')
            except Exception:
                pass
            raise MiroTransportError(
                f'Miro {req.get_method()} {req.full_url} failed '
                f'with HTTP {exc.code}: {detail}'
            ) from exc
        except urllib_error.URLError as exc:
            raise MiroTransportError(
                f'Miro {req.get_method()} {req.full_url} failed: {exc.reason}'
            ) from exc
        if not raw.strip():
            return {}
        return json.loads(raw)


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
