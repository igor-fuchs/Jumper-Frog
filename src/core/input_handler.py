"""Input handler - captures and processes player input."""

import pygame


class InputHandler:
    """Collects and provides per-frame input state."""

    def __init__(self):
        self.events: list[pygame.event.Event] = []
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_clicked: bool = False

    def poll(self) -> bool:
        """Process the event queue. Returns False when the game should quit."""
        self.events = pygame.event.get()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False

        for event in self.events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_clicked = True

        return True
