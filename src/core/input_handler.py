"""Input handler - captures and processes player input.

Collects mouse and keyboard state each frame so that scenes and
entities can query it without touching ``pygame.event`` directly.
"""

import pygame


class InputHandler:
    """Collects and provides per-frame input state.

    Attributes
    ----------
    events : list[pygame.event.Event]
        Raw event list captured this frame.
    mouse_pos : tuple[int, int]
        Current mouse cursor position.
    mouse_clicked : bool
        ``True`` during the frame where the left mouse button was pressed.
    keys_pressed : pygame.key.ScancodeWrapper
        Snapshot of all keyboard keys held down this frame (continuous).
    keys_down : set[int]
        Set of key constants that were *just pressed* this frame (edge).
    """

    def __init__(self):
        self.events: list[pygame.event.Event] = []
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_clicked: bool = False
        # Continuous key state (held down)
        self.keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        # Edge-triggered key-down events (pressed this frame only)
        self.keys_down: set[int] = set()

    def poll(self) -> bool:
        """Process the event queue. Returns False when the game should quit."""
        self.events = pygame.event.get()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False
        self.keys_down = set()

        for event in self.events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_clicked = True
            if event.type == pygame.KEYDOWN:
                self.keys_down.add(event.key)

        # Update continuous key state after processing events
        self.keys_pressed = pygame.key.get_pressed()

        return True
