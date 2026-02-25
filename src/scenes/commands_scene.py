"""Commands scene - displays game controls.

Shows a list of keyboard commands the player can use during gameplay.
A ``BackButton`` in the top-left corner returns to the main menu.
"""

import pygame

from src.core.input_handler import InputHandler
from src.core.settings import (
    SCREEN_WIDTH,
    DARK_GREEN, LIGHT_GREEN, WHITE, BLACK,
    DARK_GRAY, LIGHT_GRAY,
)
from src.scenes.scene import Scene
from src.ui.back_button import BackButton
from src.ui.textbox import TextBox


class CommandsScene(Scene):
    """Shows the game controls/commands with a back arrow."""

    def __init__(self, manager):
        super().__init__(manager)

        # Fonts
        self.title_font = pygame.font.SysFont("arial", 52, bold=True)

        # ── Back button (reusable UI component) ─────────────────────
        self.back_button = BackButton(callback=self._go_back)

        # ── Commands text boxes ──────────────────────────────────────
        commands = [
            "\u2191  Seta para cima  —  Mover para frente",
            "\u2193  Seta para baixo  —  Mover para trás",
            "\u2190  Seta para esquerda  —  Mover para esquerda",
            "\u2192  Seta para direita  —  Mover para direita",
            "ESC  —  Pausar o jogo",
            "ENTER  —  Confirmar seleção",
        ]

        box_width = 500
        box_height = 40
        gap = 12
        start_y = 180

        self.textboxes: list[TextBox] = []
        cx = SCREEN_WIDTH // 2
        for i, cmd in enumerate(commands):
            rect = pygame.Rect(
                cx - box_width // 2,
                start_y + i * (box_height + gap),
                box_width,
                box_height,
            )
            self.textboxes.append(
                TextBox(rect, cmd, font_size=20,
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
        # Background
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
