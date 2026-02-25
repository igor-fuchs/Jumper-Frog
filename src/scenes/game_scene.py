"""Game scene - the main gameplay screen.

Hosts the actual game level: a ``Level`` object defines the arena
layout (background, walls, spawn point) while ``GameScene`` owns the
game-loop integration (input, update with collision, render order).

The ``Level`` subclass provides all level-specific data via a clean
interface (see :mod:`src.levels.level`), so ``GameScene`` never needs
to know about individual level layouts.
"""

import pygame

from src.core.collision import resolve_collisions
from src.core.input_handler import InputHandler
from src.core.settings import SCREEN_WIDTH, WHITE
from src.entities.frog import Frog
from src.levels.level_registry import get_level
from src.scenes.scene import Scene
from src.ui.back_button import BackButton


class GameScene(Scene):
    """Gameplay scene that runs a specific level.

    Parameters
    ----------
    manager : SceneManager
        Scene manager used for navigation (back to levels screen).
    level : int
        1-based level number.  A matching ``Level`` subclass is looked
        up via :func:`~src.levels.level_registry.get_level`.
    """

    def __init__(self, manager, level: int = 1):
        super().__init__(manager)

        # ── Level data ───────────────────────────────────────────────
        self.level = get_level(level)

        # ── Fonts ────────────────────────────────────────────────────
        self.hud_font = pygame.font.SysFont("arial", 22, bold=True)

        # ── Back button → returns to level selection ─────────────────
        self.back_button = BackButton(callback=self._go_back)

        # ── Player ───────────────────────────────────────────────────
        spawn_x, spawn_y = self.level.get_spawn_position()
        self.frog = Frog(x=spawn_x, y=spawn_y)

        # ── Walls (built once from the Level object) ─────────────────
        self.walls = self.level.build_level()

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        """Process input: back button and ESC key."""
        # Back button (mouse)
        if self.back_button.handle_event(
            input_handler.mouse_pos, input_handler.mouse_clicked,
        ):
            return

        # ESC also returns to levels screen
        if pygame.K_ESCAPE in input_handler.keys_down:
            self._go_back()

    def update(self, dt: float) -> None:
        """Update entities and resolve collisions each frame."""
        # Let the frog read keyboard state and move
        keys = pygame.key.get_pressed()
        self.frog.update(dt, keys_pressed=keys)

        # Resolve collisions between the frog and all walls
        resolve_collisions(self.frog, self.walls)

    def render(self, screen: pygame.Surface) -> None:
        """Draw the level: background, walls, frog, and HUD."""
        # ── Background (delegated to the Level subclass) ─────────────
        self.level.render_background(screen)

        # ── Walls ────────────────────────────────────────────────────
        for wall in self.walls:
            wall.draw(screen)

        # ── Player ───────────────────────────────────────────────────
        self.frog.draw(screen)

        # ── Back button ──────────────────────────────────────────────
        self.back_button.draw(screen)

        # ── HUD ──────────────────────────────────────────────────────
        hud_text = self.hud_font.render(
            f"Fase {self.level.level_number}", True, WHITE,
        )
        hud_rect = hud_text.get_rect(centerx=SCREEN_WIDTH // 2, y=2)
        screen.blit(hud_text, hud_rect)

    # ── Navigation ───────────────────────────────────────────────────

    def _go_back(self) -> None:
        """Return to the level-selection screen."""
        from src.scenes.levels_scene import LevelsScene
        self.manager.switch(LevelsScene(self.manager))
