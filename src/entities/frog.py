"""Frog - the player-controlled character.

Represented as a red square that the player moves horizontally with
**A / D** or the **arrow keys**.  Movement is continuous while the key
is held down, using ``InputHandler.keys_pressed`` for smooth control.

Collision response is handled externally by the scene or a collision
manager — `Frog` only exposes its rect and velocity so the caller can
push it out of overlapping objects.
"""

import pygame

from src.core.settings import RED, SCREEN_WIDTH
from src.entities.entity import Entity


class Frog(Entity):
    """Player-controlled frog entity.

    Parameters
    ----------
    x, y : float
        Initial spawn position (top-left corner).
    width, height : int
        Size of the frog square in pixels.  Defaults to 40 × 40.
    speed : float
        Horizontal movement speed in pixels per second.  Default 250.
    """

    DEFAULT_WIDTH = 40
    DEFAULT_HEIGHT = 40
    DEFAULT_SPEED = 250.0

    def __init__(
        self,
        x: float,
        y: float,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        speed: float = DEFAULT_SPEED,
    ):
        super().__init__(x, y, width, height, color=RED)
        self.speed = speed
        # Horizontal velocity component set each frame (-1, 0, or 1)
        self.vx: float = 0.0

    # ── Update ───────────────────────────────────────────────────────

    def update(self, dt: float, **kwargs) -> None:
        """Move the frog according to the current keyboard state.

        Expects ``keys_pressed`` (a ``pygame.key.ScancodeWrapper``) to
        be passed via *kwargs* so the entity stays decoupled from the
        input handler.
        """
        keys = kwargs.get("keys_pressed")
        if keys is None:
            return

        # Determine horizontal direction from A/D or arrow keys
        self.vx = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = 1.0

        # Apply movement
        self.x += self.vx * self.speed * dt

        # Clamp to screen bounds so the frog cannot leave the window
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))

        # Keep the rect in sync for collision detection
        self._sync_rect()
