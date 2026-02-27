"""Levels scene - level selection screen.

Displays a grid of selectable level squares.  Locked levels are shown
with a dimmed appearance and a lock icon; unlocked levels react to
hover and clicks.  A ``BackButton`` in the top-left corner returns the
player to the main menu.
"""

import pygame

from src.core.input_handler import InputHandler
from src.core.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    DARK_GREEN, GREEN, LIGHT_GREEN, WHITE, BLACK,
    DARK_GRAY, GRAY, LIGHT_GRAY,
)
from src.levels.level_registry import total_levels
from src.scenes.scene import Scene
from src.ui.back_button import BackButton


class LevelsScene(Scene):
    """Displays a grid of level squares with lock/unlock logic."""

    SQUARE_SIZE = 120
    SQUARE_GAP = 40
    NUM_LEVELS = total_levels()

    def __init__(self, manager):
        super().__init__(manager)

        # How many levels are unlocked (1-based: value 1 = level 1 unlocked)
        self.unlocked: int = 1

        # Fonts
        self.title_font = pygame.font.SysFont("arial", 52, bold=True)
        self.level_font = pygame.font.SysFont("arial", 40, bold=True)
        self.lock_font = pygame.font.SysFont("arial", 28)

        # ── Back button (reusable UI component) ─────────────────────
        self.back_button = BackButton(callback=self._go_back)

        # ── Level squares ────────────────────────────────────────────
        total_width = (
            self.NUM_LEVELS * self.SQUARE_SIZE
            + (self.NUM_LEVELS - 1) * self.SQUARE_GAP
        )
        start_x = (SCREEN_WIDTH - total_width) // 2
        center_y = SCREEN_HEIGHT // 2

        self.level_rects: list[pygame.Rect] = []
        for i in range(self.NUM_LEVELS):
            x = start_x + i * (self.SQUARE_SIZE + self.SQUARE_GAP)
            y = center_y - self.SQUARE_SIZE // 2
            self.level_rects.append(
                pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
            )

        # Hover tracking for level squares
        self.hovered_level: int = -1

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        """Process mouse input for the back button and level squares."""
        mouse_pos = input_handler.mouse_pos
        clicked = input_handler.mouse_clicked

        # Delegate to the reusable BackButton; skip further checks if clicked
        if self.back_button.handle_event(mouse_pos, clicked):
            return

        # Level squares
        self.hovered_level = -1
        for i, rect in enumerate(self.level_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_level = i
                if clicked and (i + 1) <= self.unlocked:
                    self._on_level_selected(i + 1)
                break

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        # Background
        screen.fill((20, 60, 20))

        # ── Back button ──────────────────────────────────────────────
        self.back_button.draw(screen)

        # ── Title ────────────────────────────────────────────────────
        shadow = self.title_font.render("Fases", True, BLACK)
        shadow_rect = shadow.get_rect(
            centerx=SCREEN_WIDTH // 2 + 3, y=53,
        )
        screen.blit(shadow, shadow_rect)

        title = self.title_font.render("Fases", True, LIGHT_GREEN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        screen.blit(title, title_rect)

        # Decorative line
        pygame.draw.line(
            screen, DARK_GREEN,
            (80, 120), (SCREEN_WIDTH - 80, 120), 2,
        )

        # ── Level squares ────────────────────────────────────────────
        for i, rect in enumerate(self.level_rects):
            level_num = i + 1
            is_unlocked = level_num <= self.unlocked
            is_hovered = (self.hovered_level == i)

            # Shadow
            shadow_rect = rect.move(4, 4)
            pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=10)

            # Background color
            if is_unlocked:
                bg = GREEN if is_hovered else DARK_GREEN
            else:
                bg = GRAY if is_hovered else DARK_GRAY

            pygame.draw.rect(screen, bg, rect, border_radius=10)

            # Border
            border_color = LIGHT_GREEN if (is_hovered and is_unlocked) else WHITE
            pygame.draw.rect(
                screen, border_color, rect,
                width=2, border_radius=10,
            )

            # Level number or lock icon
            if is_unlocked:
                num_surf = self.level_font.render(str(level_num), True, WHITE)
                num_rect = num_surf.get_rect(center=rect.center)
                screen.blit(num_surf, num_rect)
            else:
                # Show number (dimmed) + lock symbol
                num_surf = self.level_font.render(
                    str(level_num), True, LIGHT_GRAY,
                )
                num_rect = num_surf.get_rect(
                    centerx=rect.centerx, centery=rect.centery - 10,
                )
                screen.blit(num_surf, num_rect)

                lock_surf = self.lock_font.render("\U0001F512", True, LIGHT_GRAY)
                lock_rect = lock_surf.get_rect(
                    centerx=rect.centerx, centery=rect.centery + 25,
                )
                screen.blit(lock_surf, lock_rect)

    # ── Navigation helpers ───────────────────────────────────────────

    def _go_back(self) -> None:
        from src.scenes.menu_scene import MenuScene
        self.manager.switch(MenuScene(self.manager))

    def _on_level_selected(self, level: int) -> None:
        """Open the gameplay scene for the chosen level."""
        from src.scenes.game_scene import GameScene
        self.manager.switch(GameScene(self.manager, level=level))
