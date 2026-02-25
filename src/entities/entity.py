"""Entity - abstract base class for all game objects.

Every visible, interactive object in the game world (player, obstacles,
platforms, walls …) inherits from ``Entity``.  The class provides:

* A ``pygame.Rect`` that defines position and size (used for rendering
  **and** collision detection).
* Abstract ``update`` and ``draw`` hooks so the game loop can
  polymorphically iterate over a list of entities.
* A concrete ``collides_with`` helper built on ``Rect.colliderect``.
"""

from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    """Base class that every game entity must inherit from.

    Parameters
    ----------
    x, y : float
        Top-left position of the entity in world coordinates.
    width, height : int
        Pixel dimensions of the entity's bounding box.
    color : tuple[int, int, int]
        RGB fill colour used by the default ``draw`` implementation.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: tuple[int, int, int],
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(int(x), int(y), width, height)

    # ── Abstract hooks ───────────────────────────────────────────────

    @abstractmethod
    def update(self, dt: float, **kwargs) -> None:
        """Update entity state.  *dt* is seconds since last frame."""

    # ── Concrete helpers ─────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Render the entity as a filled rectangle.

        Subclasses can override this to draw sprites or more complex
        shapes; the default is a solid-colour box.
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def collides_with(self, other: "Entity") -> bool:
        """Return ``True`` if this entity's rect overlaps *other*'s rect."""
        return self.rect.colliderect(other.rect)

    def _sync_rect(self) -> None:
        """Synchronise the ``Rect`` position with ``self.x / self.y``.

        Call this after modifying ``x`` or ``y`` so that collision
        detection stays accurate.
        """
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
