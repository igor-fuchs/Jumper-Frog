"""BackButton - reusable navigation button to return to a previous scene.

This component encapsulates the "back arrow" pattern used across multiple
scenes.  It handles its own hover state, click detection, drawing, and
scene-transition callback, so every scene that needs a "go back" control
can simply instantiate a ``BackButton`` and delegate to it.

Design notes
------------
* Follows the same public API contract as ``Button`` (``handle_event`` +
  ``draw``), so it is interchangeable where a clickable UI element is
  expected.
* The visual appearance (symbol, colours, position, font size) can be
  customised via constructor keyword arguments, making the component easy
  to *polymorphise* for different contexts (e.g. a "→" forward arrow, a
  different colour scheme, or a larger hit-box).
"""

from typing import Callable, Optional

import pygame

from src.core.settings import WHITE, LIGHT_GREEN, BLACK


class BackButton:
    """Clickable arrow button with hover feedback and a navigation callback.

    Parameters
    ----------
    callback : Callable
        Function invoked when the button is clicked (typically a scene
        transition such as ``lambda: manager.switch(MenuScene(manager))``).
    rect : pygame.Rect, optional
        Hit-box rectangle.  Defaults to a 50 × 50 area at (20, 20).
    symbol : str, optional
        The character rendered inside the button.  Defaults to "←".
    font_size : int, optional
        Size of the symbol font.  Defaults to 36.
    color : tuple, optional
        Default (non-hovered) colour of the symbol.  Defaults to ``WHITE``.
    hover_color : tuple, optional
        Colour of the symbol while the cursor hovers over the hit-box.
        Defaults to ``LIGHT_GREEN``.
    """

    def __init__(
        self,
        callback: Callable,
        *,
        rect: Optional[pygame.Rect] = None,
        symbol: str = "\u2190",
        font_size: int = 36,
        color: tuple = WHITE,
        hover_color: tuple = LIGHT_GREEN,
    ):
        self.callback = callback
        self.rect = rect or pygame.Rect(20, 20, 50, 50)
        self.symbol = symbol
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.color = color
        self.hover_color = hover_color
        self.hovered: bool = False

    # ── Input handling ───────────────────────────────────────────────

    def handle_event(
        self, mouse_pos: tuple[int, int], mouse_clicked: bool
    ) -> bool:
        """Update hover state and fire callback on click.

        Parameters
        ----------
        mouse_pos : tuple[int, int]
            Current mouse cursor position.
        mouse_clicked : bool
            Whether the left mouse button was pressed this frame.

        Returns
        -------
        bool
            ``True`` if the button was clicked (and the callback fired),
            ``False`` otherwise.  Callers can use this to short-circuit
            further event processing in the same frame.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked:
            self.callback()
            return True
        return False

    # ── Drawing ──────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Render the back-arrow symbol onto *screen*.

        The symbol colour changes when the cursor hovers over the
        hit-box, providing visual feedback to the player.
        """
        # Pick colour based on hover state
        current_color = self.hover_color if self.hovered else self.color

        # Render the symbol centred inside the hit-box
        symbol_surf = self.font.render(self.symbol, True, current_color)
        symbol_rect = symbol_surf.get_rect(center=self.rect.center)
        screen.blit(symbol_surf, symbol_rect)
