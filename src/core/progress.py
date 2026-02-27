"""Progress tracker — keeps track of the highest unlocked level.

This module provides simple functions to query and advance the
player's progression.  State is kept in-memory (resets on restart).

Usage
-----
* ``get_unlocked()`` → ``int``  — highest level the player may play.
* ``unlock_next(current)``      — unlock the level after *current*.
"""

_unlocked: int = 1  # level 1 is always available


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
    if next_level > _unlocked:
        _unlocked = next_level
