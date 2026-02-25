"""Menu scene - main menu screen."""

import pygame

from src.core.input_handler import InputHandler
from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    DARK_GREEN, LIGHT_GREEN, WHITE, BLACK,
)
from src.scenes.scene import Scene
from src.ui.button import Button
from src.ui.textbox import TextBox


class MenuScene(Scene):
    """Displays the title, three action buttons and a credits text box."""

    BUTTON_WIDTH = 260
    BUTTON_HEIGHT = 52
    BUTTON_GAP = 20

    def __init__(self, manager):
        super().__init__(manager)

        # ── Title ────────────────────────────────────────────────────
        self.title_font = pygame.font.SysFont("arial", 64, bold=True)
        self.title_shadow_font = pygame.font.SysFont("arial", 64, bold=True)

        # ── Buttons ──────────────────────────────────────────────────
        cx = SCREEN_WIDTH // 2
        start_y = 260

        self.buttons: list[Button] = []
        labels = ["Iniciar", "Comandos", "Extra"]
        callbacks = [self._on_start, self._on_commands, self._on_extra]

        for i, (label, cb) in enumerate(zip(labels, callbacks)):
            rect = pygame.Rect(
                cx - self.BUTTON_WIDTH // 2,
                start_y + i * (self.BUTTON_HEIGHT + self.BUTTON_GAP),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            )
            self.buttons.append(Button(rect, label, cb))

        # ── Credits text box ─────────────────────────────────────────
        tb_width, tb_height = 300, 36
        self.textbox = TextBox(
            pygame.Rect(
                cx - tb_width // 2,
                SCREEN_HEIGHT - 60,
                tb_width,
                tb_height,
            ),
            "Criado por: Igor Fuchs Pereira",
        )

    # ── Event handlers ───────────────────────────────────────────────

    def _on_start(self) -> None:
        print("[Menu] Iniciar pressionado")

    def _on_commands(self) -> None:
        print("[Menu] Comandos pressionado")

    def _on_extra(self) -> None:
        print("[Menu] Extra pressionado")

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        for btn in self.buttons:
            btn.handle_event(input_handler.mouse_pos, input_handler.mouse_clicked)

    def update(self, dt: float) -> None:
        pass  # no dynamic logic yet

    def render(self, screen: pygame.Surface) -> None:
        # Background gradient (two halves for a subtle effect)
        top_color = (20, 60, 20)
        bottom_color = (10, 30, 10)
        top_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        bot_rect = pygame.Rect(
            0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2
        )
        screen.fill(top_color, top_rect)
        screen.fill(bottom_color, bot_rect)

        # Decorative line
        pygame.draw.line(
            screen, DARK_GREEN,
            (80, 230), (SCREEN_WIDTH - 80, 230), 2,
        )

        # Title shadow
        shadow = self.title_shadow_font.render("Frog Jumper", True, BLACK)
        shadow_rect = shadow.get_rect(
            centerx=SCREEN_WIDTH // 2 + 3, y=82,
        )
        screen.blit(shadow, shadow_rect)

        # Title
        title = self.title_font.render("Frog Jumper", True, LIGHT_GREEN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=80)
        screen.blit(title, title_rect)

        # Subtitle
        sub_font = pygame.font.SysFont("arial", 20)
        subtitle = sub_font.render(
            "Atravesse a estrada e o rio!", True, WHITE,
        )
        sub_rect = subtitle.get_rect(
            centerx=SCREEN_WIDTH // 2, y=160,
        )
        screen.blit(subtitle, sub_rect)

        # Buttons
        for btn in self.buttons:
            btn.draw(screen)

        # Credits
        self.textbox.draw(screen)
