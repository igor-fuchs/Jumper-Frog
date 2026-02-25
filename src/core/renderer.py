"""Renderer - handles all drawing operations."""

import pygame

from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE


class Renderer:
    """Creates and manages the display surface."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

    def clear(self, color: tuple[int, int, int]) -> None:
        """Fill the screen with a solid color."""
        self.screen.fill(color)

    def present(self) -> None:
        """Flip the display buffer to show the current frame."""
        pygame.display.flip()
