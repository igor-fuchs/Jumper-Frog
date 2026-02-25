"""Game loop - handles update, render, and timing."""

import pygame

from src.core.settings import FPS
from src.core.renderer import Renderer
from src.core.input_handler import InputHandler


class GameLoop:
    """Runs the core loop: poll input -> update -> render."""

    def __init__(self, renderer: Renderer, input_handler: InputHandler):
        self.renderer = renderer
        self.input_handler = input_handler
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None

    def set_scene(self, scene) -> None:
        """Switch the active scene."""
        self.current_scene = scene

    def run(self) -> None:
        """Execute the loop until the game is quit."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            if not self.input_handler.poll():
                self.running = False
                break

            if self.current_scene:
                self.current_scene.handle_events(self.input_handler)
                self.current_scene.update(dt)
                self.current_scene.render(self.renderer.screen)

            self.renderer.present()
