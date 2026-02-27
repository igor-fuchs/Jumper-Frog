"""Renderer - handles all drawing operations."""

import os

import pygame

from src.core.settings import BASE_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

_ICON_PATH = os.path.join(BASE_DIR, "assets", "frogs", "default.png")


class Renderer:
    """Creates and manages the display surface."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        # Window icon
        if os.path.isfile(_ICON_PATH):
            icon = pygame.image.load(_ICON_PATH).convert_alpha()
            pygame.display.set_icon(icon)

    def clear(self, color: tuple[int, int, int]) -> None:
        """Fill the screen with a solid color."""
        self.screen.fill(color)

    def present(self) -> None:
        """Flip the display buffer to show the current frame."""
        pygame.display.flip()
