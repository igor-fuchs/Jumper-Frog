"""Progress tracker — keeps track of unlocked and completed levels.

This module provides simple functions to query and advance the
player's progression.  State is kept in-memory (resets on restart).

Usage
-----
* ``get_unlocked()`` → ``int``  — highest level the player may play.
* ``unlock_next(current)``      — unlock the level after *current*.
* ``mark_completed(level)``     — record a level as finished.
* ``is_completed(level)``       — check whether a level was finished.
"""

_unlocked: int = 1  # level 1 is always available  # pylint: disable=invalid-name
_completed: set[int] = set()  # pylint: disable=invalid-name


def get_unlocked() -> int:
    """Return the highest unlocked level number (1-based)."""
    return _unlocked


def unlock_next(current_level: int) -> None:
    """Unlock the level that follows *current_level*, if not already.

    Parameters
    ----------
    current_level : int
        The level the player just completed (1-based).
    """
    global _unlocked  # pylint: disable=global-statement
    next_level = current_level + 1
    _unlocked = max(_unlocked, next_level)


def mark_completed(level: int) -> None:
    """Record *level* as completed."""
    _completed.add(level)


def is_completed(level: int) -> bool:
    """Return ``True`` if the player has completed *level*."""
    return level in _completed
