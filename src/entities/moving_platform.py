"""MovingPlatform - a solid platform that travels back and forth.

A ``MovingPlatform`` behaves exactly like a :class:`Wall` for
collision purposes, but it oscillates between two endpoints along
either the horizontal or vertical axis.

The platform exposes ``dx`` and ``dy`` — the displacement it applied
this frame — so that external code (e.g. ``GameScene``) can carry
entities that are standing on top of it.
"""

import pygame

from src.core.settings import BLUE
from src.entities.entity import Entity


class MovingPlatform(Entity):
    """A platform that moves between two points at a constant speed.

    Parameters
    ----------
    x, y : float
        Starting top-left position.
    width, height : int
        Dimensions in pixels.
    axis : str
        ``"horizontal"`` or ``"vertical"`` — the axis of motion.
    distance : float
        Total travel distance in pixels from the start position.
    speed : float
        Movement speed in pixels / second.
    color : tuple[int, int, int], optional
        Fill colour (defaults to ``BLUE``).
    """

    AXIS_HORIZONTAL = "horizontal"
    AXIS_VERTICAL = "vertical"

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        axis: str,
        distance: float,
        speed: float = 80.0,
        color: tuple[int, int, int] = BLUE,
    ):
        super().__init__(x, y, width, height, color)

        self.axis = axis
        self.distance = abs(distance)
        self.speed = speed

        # Origin is the start position on the movement axis.
        self._origin_x = x
        self._origin_y = y

        # +1 = moving toward end, -1 = moving back toward origin
        self._direction: int = 1

        # How far along the path (0 → distance) we currently are.
        self._progress: float = 0.0

        # Frame displacement (set each update so the scene can carry
        # entities riding on this platform).
        self.dx: float = 0.0
        self.dy: float = 0.0

    # ── Update ───────────────────────────────────────────────────────

    def update(self, dt: float, **kwargs) -> None:
        """Move the platform along its axis and bounce at the endpoints."""
        step = self.speed * dt * self._direction
        self._progress += step

        # Clamp and reverse at boundaries
        if self._progress >= self.distance:
            self._progress = self.distance
            self._direction = -1
        elif self._progress <= 0:
            self._progress = 0
            self._direction = 1

        old_x, old_y = self.x, self.y

        if self.axis == self.AXIS_HORIZONTAL:
            self.x = self._origin_x + self._progress
        else:
            self.y = self._origin_y + self._progress

        self.dx = self.x - old_x
        self.dy = self.y - old_y
        self._sync_rect()

    # ── Drawing ──────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the platform with a subtle border for visual distinction."""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (20, 70, 160), self.rect, 2)
