"""Level - abstract base class that defines the layout of a game level.

Every concrete level (``Level1``, ``Level2`` …) inherits from ``Level``
and overrides the hooks that provide solids, spawn position, and visual
rendering of the background / scenery.

Responsibilities of a ``Level`` subclass
-----------------------------------------
* **Boundary walls** — provided by the base class via
  :meth:`_build_boundary_walls` (same for every level).
* **Internal obstacles** — returned by :meth:`_build_obstacles`, which
  each subclass **must** implement.
* **Background rendering** — :meth:`render_background` can be overridden
  to paint a custom backdrop (the default is a solid grey fill).
* **Player spawn** — :meth:`get_spawn_position` can be overridden to
  change where the ``Frog`` appears.

``GameScene`` creates a ``Level`` via the :func:`level_registry.get`
factory, calls the build helpers once in ``__init__``, and delegates
``render_background`` every frame.
"""

from abc import ABC, abstractmethod

import pygame

from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRAY
from src.entities.entity import Entity
from src.entities.wall import Wall


# Thickness (pixels) of the boundary walls that enclose every level.
_BOUNDARY_THICKNESS = 20


class Level(ABC):
    """Abstract base defining the contract for a game level.

    Parameters
    ----------
    level_number : int
        Numeric identifier displayed in the HUD (1-based).
    """

    def __init__(self, level_number: int):
        self.level_number = level_number

    # ── Solids ────────────────────────────────────────────────────────

    def build_level(self) -> list[Entity]:
        """Return the full list of solids for this level.

        Combines the shared boundary walls with the level-specific
        internal obstacles.  Called once when ``GameScene`` initialises.
        """
        return self._build_boundary_walls() + self._build_obstacles()

    @staticmethod
    def _build_boundary_walls() -> list[Wall]:
        """Create the four boundary walls that exist in every level."""
        t = _BOUNDARY_THICKNESS
        return [
            Wall(0, 0, SCREEN_WIDTH, t),                    # top
            Wall(0, SCREEN_HEIGHT - t, SCREEN_WIDTH, t),     # bottom
            Wall(0, 0, t, SCREEN_HEIGHT),                    # left
            Wall(SCREEN_WIDTH - t, 0, t, SCREEN_HEIGHT),     # right
        ]

    @abstractmethod
    def _build_obstacles(self) -> list[Entity]:
        """Return the internal obstacles specific to this level.

        Subclasses **must** implement this, returning a (possibly empty)
        list of ``Entity`` instances (``Wall``, ``MovingPlatform``, etc.)
        that form the level's unique layout.
        """

    # ── Player spawn ─────────────────────────────────────────────────

    def get_spawn_position(self) -> tuple[float, float]:
        """Return the (x, y) position where the Frog should spawn.

        The default places the frog at the bottom-centre of the arena.
        Override in a subclass to customise.
        """
        from src.entities.frog import Frog  # lazy import to avoid cycle
        x = SCREEN_WIDTH // 2 - Frog.DEFAULT_WIDTH // 2
        y = SCREEN_HEIGHT - 80
        return (x, y)

    # ── Trophy ───────────────────────────────────────────────────────

    def get_trophy_position(self) -> tuple[float, float]:
        """Return the (x, y) position where the goal trophy is placed.

        The default places the trophy at the top-centre of the arena.
        Override in a subclass to customise.
        """
        from src.entities.trophy import Trophy  # lazy import
        x = SCREEN_WIDTH // 2 - Trophy.DEFAULT_SIZE // 2
        y = _BOUNDARY_THICKNESS + 20
        return (x, y)

    # ── Rendering ────────────────────────────────────────────────────

    def render_background(self, screen: pygame.Surface) -> None:
        """Draw the level background before entities are rendered.

        The default is a simple solid grey fill.  Subclasses can
        override this to paint terrain, tiles, or decorative elements.
        """
        screen.fill(GRAY)
