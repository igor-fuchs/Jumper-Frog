"""PauseOverlay - translucent pause menu drawn on top of the game.

This UI component renders a semi-transparent gray overlay covering the
entire screen, with a "Pause" title and three action buttons:

* **Retornar** — dismiss the overlay and resume gameplay.
* **Reiniciar Partida** — reload the current level from scratch.
* **Voltar ao Menu** — return to the main menu.

Design notes
------------
* The overlay is rendered *on top of* the last game frame so the
  frozen scene remains visible beneath the translucent tint.  This
  approach naturally freezes all entity rendering without needing to
  explicitly pause animations — the game-loop simply skips ``update``
  while the overlay is active.
* The component owns its own input handling (``handle_event``) and
  drawing (``draw``) so ``GameScene`` can delegate to it cleanly.
* Callbacks are injected via the constructor so ``PauseOverlay`` stays
  decoupled from any specific scene or manager.
"""

from typing import Callable

import pygame

from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, LIGHT_GREEN
)
from src.ui.button import Button


class PauseOverlay:
    """Translucent pause menu with resume, restart, and quit buttons.

    Parameters
    ----------
    on_resume : Callable
        Called when the player clicks "Retornar".
    on_restart : Callable
        Called when the player clicks "Reiniciar Partida".
    on_menu : Callable
        Called when the player clicks "Voltar ao Menu".
    """

    BUTTON_WIDTH = 280
    BUTTON_HEIGHT = 52
    BUTTON_GAP = 20

    def __init__(
        self,
        on_resume: Callable,
        on_restart: Callable,
        on_menu: Callable,
    ):
        # ── Semi-transparent overlay surface ─────────────────────────
        self.overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA,
        )
        # RGBA: gray with ~60 % opacity
        self.overlay.fill((40, 40, 40, 150))

        # ── Title ────────────────────────────────────────────────────
        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.title_shadow_font = pygame.font.SysFont("arial", 56, bold=True)

        # ── Buttons ──────────────────────────────────────────────────
        cx = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 60

        labels = ["Retornar", "Reiniciar Partida", "Voltar ao Menu"]
        callbacks = [on_resume, on_restart, on_menu]

        self.buttons: list[Button] = []
        for i, (label, cb) in enumerate(zip(labels, callbacks)):
            rect = pygame.Rect(
                cx - self.BUTTON_WIDTH // 2,
                start_y + i * (self.BUTTON_HEIGHT + self.BUTTON_GAP),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            )
            self.buttons.append(Button(rect, label, cb))

    # ── Input ────────────────────────────────────────────────────────

    def handle_event(
        self,
        mouse_pos: tuple[int, int],
        mouse_clicked: bool,
    ) -> None:
        """Forward mouse state to every pause-menu button.

        Parameters
        ----------
        mouse_pos : tuple[int, int]
            Current mouse cursor position.
        mouse_clicked : bool
            Whether the left mouse button was pressed this frame.
        """
        for btn in self.buttons:
            btn.handle_event(mouse_pos, mouse_clicked)

    # ── Drawing ──────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Render the translucent overlay, title, and buttons.

        This should be called **after** the game scene has drawn its
        last frame so the frozen scene is visible beneath the tint.
        """
        # ── Translucent backdrop ─────────────────────────────────────
        screen.blit(self.overlay, (0, 0))

        # ── Title shadow ─────────────────────────────────────────────
        shadow = self.title_shadow_font.render("Pause", True, BLACK)
        shadow_rect = shadow.get_rect(
            centerx=SCREEN_WIDTH // 2 + 3,
            centery=SCREEN_HEIGHT // 2 - 120 + 3,
        )
        screen.blit(shadow, shadow_rect)

        # ── Title ────────────────────────────────────────────────────
        title = self.title_font.render("Pause", True, LIGHT_GREEN)
        title_rect = title.get_rect(
            centerx=SCREEN_WIDTH // 2,
            centery=SCREEN_HEIGHT // 2 - 120,
        )
        screen.blit(title, title_rect)

        # ── Buttons ──────────────────────────────────────────────────
        for btn in self.buttons:
            btn.draw(screen)
