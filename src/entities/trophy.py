"""Trophy - collectible goal object that completes a level.

The trophy is rendered using the icon at ``assets/icons/trophy.png``
and scaled to the provided dimensions.  It does not move or respond
to input — it simply exists at a position and exposes its ``rect``
for collision detection by the scene.
"""

import os

import pygame

from src.entities.entity import Entity


class Trophy(Entity):
    """Static collectible that marks the level goal.

    Parameters
    ----------
    x, y : float
        Top-left position.
    width, height : int
        Display size in pixels.
    """

    DEFAULT_SIZE = 50

    _ICON_PATH = os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir,
        "assets", "icons", "trophy.png",
    )

    def __init__(
        self,
        x: float,
        y: float,
        width: int = DEFAULT_SIZE,
        height: int = DEFAULT_SIZE,
    ):
        super().__init__(x, y, width, height, color=(255, 215, 0))
        self._sprite = pygame.transform.scale(
            pygame.image.load(self._ICON_PATH).convert_alpha(),
            (width, height),
        )

    # Trophy is static — nothing to update.
    def update(self, dt: float, **kwargs) -> None:  # noqa: D401
        """No-op: the trophy does not move."""

    def draw(self, screen: pygame.Surface) -> None:
        """Render the trophy sprite at its position."""
        screen.blit(self._sprite, self.rect)
