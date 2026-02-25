"""Scene - abstract base class for game scenes."""

from abc import ABC, abstractmethod

import pygame

from src.core.input_handler import InputHandler


class Scene(ABC):
    """Base class that every scene must inherit from."""

    def __init__(self, manager):
        """
        Args:
            manager: SceneManager instance to allow scene transitions.
        """
        self.manager = manager

    @abstractmethod
    def handle_events(self, input_handler: InputHandler) -> None:
        """Process input for this scene."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update scene logic. *dt* is seconds since last frame."""

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Draw the scene onto *screen*."""
