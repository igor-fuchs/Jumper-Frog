"""Level registry - maps level numbers to their concrete Level classes.

This module acts as a simple factory: call :func:`get_level` with a
level number and receive a fully-initialised ``Level`` instance.

When new levels are added to the project, they only need to be
registered in the ``_REGISTRY`` dict below — no changes required in
``GameScene`` or ``LevelsScene``.
"""

from src.levels.level import Level
from src.levels.level_1 import Level1
from src.levels.level_2 import Level2
from src.levels.level_3 import Level3


# ── Registry ─────────────────────────────────────────────────────────
# Maps 1-based level numbers → callables that return a Level instance.
_REGISTRY: dict[int, type[Level]] = {
    1: Level1,
    2: Level2,
    3: Level3,
}


def get_level(number: int) -> Level:
    """Return an initialised ``Level`` for the given *number*.

    Parameters
    ----------
    number : int
        1-based level number.

    Returns
    -------
    Level
        A concrete ``Level`` subclass instance ready to be used by
        ``GameScene``.

    Raises
    ------
    KeyError
        If the level number is not registered.
    """
    level_cls = _REGISTRY.get(number)
    if level_cls is None:
        raise KeyError(
            f"Level {number} is not registered. "
            f"Available levels: {sorted(_REGISTRY.keys())}"
        )
    return level_cls()


def total_levels() -> int:
    """Return the number of registered levels."""
    return len(_REGISTRY)
