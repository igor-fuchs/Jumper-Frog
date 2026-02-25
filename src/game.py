"""Game class - manages the game loop and global state."""

import pygame

from src.core.renderer import Renderer
from src.core.input_handler import InputHandler
from src.core.game_loop import GameLoop
from src.manager.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene


class Game:
    """Initialises Pygame, wires everything together and starts the loop."""

    def __init__(self):
        pygame.init()

        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.game_loop = GameLoop(self.renderer, self.input_handler)

        # Scene management
        self.scene_manager = SceneManager()
        self.scene_manager.switch(MenuScene(self.scene_manager))

        # The game loop delegates to the scene manager
        self.game_loop.set_scene(self.scene_manager)

    def run(self) -> None:
        """Start the game."""
        self.game_loop.run()
        pygame.quit()
