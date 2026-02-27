"""VictoryOverlay - congratulations screen shown when a level is completed.

Displays a translucent overlay with a congratulatory message and
contextual buttons:

* **Intermediate levels** — "Próxima Fase" and "Voltar ao Menu".
* **Final level** — a "Jogo Completo!" message and only "Voltar ao Menu".

The overlay follows the same visual pattern as :class:`PauseOverlay`.
"""

from typing import Callable

import pygame

from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, LIGHT_GREEN,
)
from src.ui.button import Button


class VictoryOverlay:
    """Translucent victory menu with conditional navigation buttons.

    Parameters
    ----------
    is_last_level : bool
        When ``True`` the overlay shows "Jogo Completo!" and only
        the menu button.  Otherwise it shows "Parabéns!" with both
        next-level and menu buttons.
    on_next_level : Callable | None
        Called when the player clicks "Próxima Fase".  May be
        ``None`` on the last level.
    on_menu : Callable
        Called when the player clicks "Voltar ao Menu".
    """

    BUTTON_WIDTH = 280
    BUTTON_HEIGHT = 52
    BUTTON_GAP = 20

    def __init__(
        self,
        is_last_level: bool,
        on_next_level: Callable | None,
        on_menu: Callable,
    ):
        self.is_last_level = is_last_level

        # ── Semi-transparent overlay surface ─────────────────────────
        self.overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA,
        )
        self.overlay.fill((20, 20, 20, 170))

        # ── Fonts ────────────────────────────────────────────────────
        self.title_font = pygame.font.SysFont("arial", 52, bold=True)
        self.shadow_font = pygame.font.SysFont("arial", 52, bold=True)

        # ── Title text ───────────────────────────────────────────────
        self.title_text = (
            "Jogo Completo!" if is_last_level else "Parabéns!"
        )

        # ── Buttons ──────────────────────────────────────────────────
        cx = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 20

        self.buttons: list[Button] = []

        if not is_last_level and on_next_level is not None:
            next_rect = pygame.Rect(
                cx - self.BUTTON_WIDTH // 2,
                start_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            )
            self.buttons.append(
                Button(next_rect, "Próxima Fase", on_next_level),
            )
            start_y += self.BUTTON_HEIGHT + self.BUTTON_GAP

        menu_rect = pygame.Rect(
            cx - self.BUTTON_WIDTH // 2,
            start_y,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT,
        )
        self.buttons.append(Button(menu_rect, "Voltar ao Menu", on_menu))

    # ── Input ────────────────────────────────────────────────────────

    def handle_event(
        self,
        mouse_pos: tuple[int, int],
        mouse_clicked: bool,
    ) -> None:
        """Forward mouse state to every button."""
        for btn in self.buttons:
            btn.handle_event(mouse_pos, mouse_clicked)

    # ── Drawing ──────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Render the translucent overlay, title, and buttons."""
        screen.blit(self.overlay, (0, 0))

        # ── Title shadow ─────────────────────────────────────────────
        shadow = self.shadow_font.render(self.title_text, True, BLACK)
        shadow_rect = shadow.get_rect(
            centerx=SCREEN_WIDTH // 2 + 3,
            centery=SCREEN_HEIGHT // 2 - 100 + 3,
        )
        screen.blit(shadow, shadow_rect)

        # ── Title ────────────────────────────────────────────────────
        title = self.title_font.render(
            self.title_text, True, LIGHT_GREEN,
        )
        title_rect = title.get_rect(
            centerx=SCREEN_WIDTH // 2,
            centery=SCREEN_HEIGHT // 2 - 100,
        )
        screen.blit(title, title_rect)

        # ── Buttons ──────────────────────────────────────────────────
        for btn in self.buttons:
            btn.draw(screen)
