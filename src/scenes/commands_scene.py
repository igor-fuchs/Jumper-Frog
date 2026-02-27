"""Commands scene - displays game controls.

Shows a list of keyboard commands the player can use during gameplay.
A ``BackButton`` in the top-left corner returns to the main menu.
"""

import os

import pygame

from src.core.input_handler import InputHandler
from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    DARK_GREEN, LIGHT_GREEN, BLACK,
    DARK_GRAY, LIGHT_GRAY
)
from src.scenes.scene import Scene
from src.ui.back_button import BackButton
from src.ui.textbox import TextBox

_BG_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir,
    "assets", "background", "menu.png",
)


class CommandsScene(Scene):
    """Shows the game controls/commands with a back arrow."""

    def __init__(self, manager):
        super().__init__(manager)

        # Fonts
        self.title_font = pygame.font.SysFont("arial", 52, bold=True)

        # ── Back button (reusable UI component) ─────────────────────
        self.back_button = BackButton(callback=self._go_back)

        # ── Background image (same as menu) ──────────────────────────
        self._bg_image: pygame.Surface | None = None
        if os.path.isfile(_BG_PATH):
            img = pygame.image.load(_BG_PATH).convert()
            self._bg_image = pygame.transform.scale(
                img, (SCREEN_WIDTH, SCREEN_HEIGHT),
            )

        # ── Commands — two-column layout (key | action) ─────────────
        commands = [
            ("A  ou  \u2190", "Mover para a esquerda"),
            ("D  ou  \u2192", "Mover para a direita"),
            ("ESPAÇO (segurar)", "Carregar pulo"),
            ("ESPAÇO (soltar)", "Pular"),
            ("ESC", "Pausar | Retomar o jogo"),
        ]

        key_width = 220
        action_width = 310
        box_height = 40
        gap_y = 12
        gap_x = 10
        start_y = 180

        total_row_width = key_width + gap_x + action_width
        row_x = (SCREEN_WIDTH - total_row_width) // 2

        self.textboxes: list[TextBox] = []
        for i, (key, action) in enumerate(commands):
            y = start_y + i * (box_height + gap_y)

            key_rect = pygame.Rect(row_x, y, key_width, box_height)
            action_rect = pygame.Rect(
                row_x + key_width + gap_x, y,
                action_width, box_height,
            )

            self.textboxes.append(
                TextBox(key_rect, key, font_size=20,
                        bg_color=DARK_GRAY, border_color=LIGHT_GRAY)
            )
            self.textboxes.append(
                TextBox(action_rect, action, font_size=20,
                        bg_color=DARK_GRAY, border_color=LIGHT_GRAY)
            )

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        """Process mouse input — only the back button is interactive."""
        self.back_button.handle_event(
            input_handler.mouse_pos, input_handler.mouse_clicked,
        )

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        # Background image or fallback solid colour
        if self._bg_image is not None:
            screen.blit(self._bg_image, (0, 0))
        else:
            screen.fill((20, 60, 20))

        # ── Back button ──────────────────────────────────────────────
        self.back_button.draw(screen)

        # ── Title ────────────────────────────────────────────────────
        shadow = self.title_font.render("Comandos", True, BLACK)
        shadow_rect = shadow.get_rect(
            centerx=SCREEN_WIDTH // 2 + 3, y=53,
        )
        screen.blit(shadow, shadow_rect)

        title = self.title_font.render("Comandos", True, LIGHT_GREEN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        screen.blit(title, title_rect)

        # Decorative line
        pygame.draw.line(
            screen, DARK_GREEN,
            (80, 120), (SCREEN_WIDTH - 80, 120), 2,
        )

        # ── Command text boxes ───────────────────────────────────────
        for tb in self.textboxes:
            tb.draw(screen)

    # ── Navigation ───────────────────────────────────────────────────

    def _go_back(self) -> None:
        from src.scenes.menu_scene import MenuScene
        self.manager.switch(MenuScene(self.manager))
