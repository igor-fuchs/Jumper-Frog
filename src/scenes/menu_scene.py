"""Menu scene - main menu screen."""

import os
import sys

import pygame

from src.core.input_handler import InputHandler
from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    LIGHT_GREEN, BLACK
)
from src.scenes.scene import Scene
from src.ui.button import Button

_BG_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir,
    "assets", "background", "menu.png",
)


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
        labels = ["Iniciar", "Comandos", "Sair"]
        callbacks = [self._on_start, self._on_commands, self._on_quit]

        for i, (label, cb) in enumerate(zip(labels, callbacks)):
            rect = pygame.Rect(
                cx - self.BUTTON_WIDTH // 2,
                start_y + i * (self.BUTTON_HEIGHT + self.BUTTON_GAP),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            )
            self.buttons.append(Button(rect, label, cb))

        # ── Credits text ───────────────────────────────────────────────
        self.credit_font = pygame.font.SysFont("arial", 16, bold=True)

        # ── Background image ─────────────────────────────────────────
        self._bg_image: pygame.Surface | None = None
        if os.path.isfile(_BG_PATH):
            img = pygame.image.load(_BG_PATH).convert()
            self._bg_image = pygame.transform.scale(
                img, (SCREEN_WIDTH, SCREEN_HEIGHT),
            )

    # ── Event handlers ───────────────────────────────────────────────

    def _on_start(self) -> None:
        from src.scenes.levels_scene import LevelsScene
        self.manager.switch(LevelsScene(self.manager))

    def _on_commands(self) -> None:
        from src.scenes.commands_scene import CommandsScene
        self.manager.switch(CommandsScene(self.manager))

    def _on_quit(self) -> None:
        pygame.quit()
        sys.exit()

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        for btn in self.buttons:
            btn.handle_event(input_handler.mouse_pos, input_handler.mouse_clicked)

    def update(self, dt: float) -> None:
        pass  # no dynamic logic yet

    def render(self, screen: pygame.Surface) -> None:
        # Background image or fallback gradient
        if self._bg_image is not None:
            screen.blit(self._bg_image, (0, 0))
        else:
            top_color = (20, 60, 20)
            bottom_color = (10, 30, 10)
            top_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
            bot_rect = pygame.Rect(
                0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2
            )
            screen.fill(top_color, top_rect)
            screen.fill(bottom_color, bot_rect)

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

        # Buttons
        for btn in self.buttons:
            btn.draw(screen)

        # Credits
        credits_box = self.credit_font.render("Criado por: Igor Fuchs Pereira", True, LIGHT_GREEN)
        credits_rect = credits_box.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 40)
        screen.blit(credits_box, credits_rect)
