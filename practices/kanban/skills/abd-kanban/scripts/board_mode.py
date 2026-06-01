"""Board mode setting for the kanban board.

Domain area   : Kanban Board — Board Mode
Responsibilities: read, set, and query the board mode (automatic or manual);
                  raise InvalidBoardModeError for unknown modes
"""
from __future__ import annotations

BOARD_MODE_AUTOMATIC = "automatic"
BOARD_MODE_MANUAL = "manual"
_VALID_MODES = frozenset({BOARD_MODE_AUTOMATIC, BOARD_MODE_MANUAL})
_BOARD_MODE_KEY = "board_mode"


class InvalidBoardModeError(Exception):
    """Raised when an unrecognised board mode is requested."""


def read_board_mode(board: dict) -> str:
    """Read board_mode from board dict. Defaults to automatic."""
    return board.get(_BOARD_MODE_KEY, BOARD_MODE_AUTOMATIC)


def set_board_mode(board: dict, mode: str) -> dict:
    """Set board_mode on board dict. Raises InvalidBoardModeError for unknown modes."""
    if mode not in _VALID_MODES:
        raise InvalidBoardModeError(
            f"Unknown board mode '{mode}'. Valid: {sorted(_VALID_MODES)}"
        )
    board[_BOARD_MODE_KEY] = mode
    return board


def is_manual_mode(board: dict) -> bool:
    """True when board_mode is manual."""
    return read_board_mode(board) == BOARD_MODE_MANUAL
