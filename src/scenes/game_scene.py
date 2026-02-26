"""Game scene - the main gameplay screen.

Hosts the actual game level: a ``Level`` object defines the arena
layout (background, walls, spawn point) while ``GameScene`` owns the
game-loop integration (input, update with collision, render order).

The ``Level`` subclass provides all level-specific data via a clean
interface (see :mod:`src.levels.level`), so ``GameScene`` never needs
to know about individual level layouts.

Pressing **ESC** toggles a translucent pause overlay that freezes all
entity updates while keeping the last game frame visible underneath.
"""

import pygame

from src.core.collision import resolve_collisions
from src.core.input_handler import InputHandler
from src.core.settings import SCREEN_WIDTH, WHITE
from src.entities.frog import Frog
from src.levels.level_registry import get_level
from src.scenes.scene import Scene
from src.ui.pause_overlay import PauseOverlay


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
        self._level_number = level

        # ── Fonts ────────────────────────────────────────────────────
        self.hud_font = pygame.font.SysFont("arial", 22, bold=True)

        # ── Player ───────────────────────────────────────────────────
        spawn_x, spawn_y = self.level.get_spawn_position()
        self.frog = Frog(x=spawn_x, y=spawn_y)

        # ── Walls (built once from the Level object) ─────────────────
        self.walls = self.level.build_level()

        # ── Pause state ──────────────────────────────────────────────
        self.paused = False
        self.pause_overlay = PauseOverlay(
            on_resume=self._resume,
            on_restart=self._restart,
            on_menu=self._go_menu,
        )

        # ── Edge-triggered key sets (filled each frame by handle_events) ─
        self._keys_down: set[int] = set()
        self._keys_up: set[int] = set()

    # ── Scene interface ──────────────────────────────────────────────

    def handle_events(self, input_handler: InputHandler) -> None:
        """Process input: ESC toggles pause; delegates to overlay when paused."""
        # Store edge-triggered key sets for update()
        self._keys_down = input_handler.keys_down
        self._keys_up = input_handler.keys_up

        # ESC toggles pause on / off
        if pygame.K_ESCAPE in input_handler.keys_down:
            self.paused = not self.paused
            return

        if self.paused:
            # While paused only the overlay receives input
            self.pause_overlay.handle_event(
                input_handler.mouse_pos, input_handler.mouse_clicked,
            )
            return

    def update(self, dt: float) -> None:
        """Update entities and resolve collisions each frame.

        All updates are skipped when the game is paused, effectively
        freezing every entity (frog movement, jump physics,
        vehicle / log animations, etc.).
        """
        if self.paused:
            return

        # Let the frog read keyboard state and move
        keys = pygame.key.get_pressed()
        self.frog.update(
            dt,
            keys_pressed=keys,
            keys_down=self._keys_down,
            keys_up=self._keys_up,
            walls=self.walls,
        )

        # Save position before collision for bounce / land detection
        pre_x = self.frog.x
        pre_y = self.frog.y

        # Resolve collisions between the frog and all walls
        collided = resolve_collisions(self.frog, self.walls)

        # Airborne collision reactions
        if self.frog.is_jumping and collided:
            dx = self.frog.x - pre_x
            dy = self.frog.y - pre_y

            # Horizontal bounce: pushed sideways → reflect vx
            if abs(dx) > 0.01:
                self.frog.bounce_horizontal()

            # Floor (pushed upward): land immediately
            if dy < -0.01:
                self.frog.land()
            # Ceiling (pushed downward): cancel upward velocity
            elif dy > 0.01:
                self.frog.hit_ceiling()

        # Ground-support check: if the frog is grounded but has no
        # solid directly below it, it should start falling.  We probe
        # one pixel below the frog's feet to detect support.
        if not self.frog.is_jumping and not self.frog.is_charging:
            probe = pygame.Rect(
                self.frog.rect.x,
                self.frog.rect.bottom,
                self.frog.rect.width,
                1,
            )
            supported = any(
                probe.colliderect(w.rect) for w in self.walls
            )
            if not supported:
                self.frog.start_falling()

    def render(self, screen: pygame.Surface) -> None:
        """Draw the level: background, walls, frog, and HUD."""
        # ── Background (delegated to the Level subclass) ─────────────
        self.level.render_background(screen)

        # ── Walls ────────────────────────────────────────────────────
        for wall in self.walls:
            wall.draw(screen)

        # ── Player ───────────────────────────────────────────────────
        self.frog.draw(screen)

        # ── HUD ──────────────────────────────────────────────────────
        hud_text = self.hud_font.render(
            f"Fase {self.level.level_number}", True, WHITE,
        )
        hud_rect = hud_text.get_rect(centerx=SCREEN_WIDTH // 2, y=2)
        screen.blit(hud_text, hud_rect)

        # ── Pause overlay (drawn last so it covers everything) ───────
        if self.paused:
            self.pause_overlay.draw(screen)

    # ── Pause callbacks ──────────────────────────────────────────────

    def _resume(self) -> None:
        """Dismiss the pause overlay and resume gameplay."""
        self.paused = False

    def _restart(self) -> None:
        """Reload the current level from scratch."""
        self.manager.switch(GameScene(self.manager, level=self._level_number))

    def _go_menu(self) -> None:
        """Return to the main menu."""
        from src.scenes.menu_scene import MenuScene
        self.manager.switch(MenuScene(self.manager))
