"""Game scene - the main gameplay screen.

Hosts the actual game level: a ``Level`` object defines the arena
layout (background, solids, spawn point) while ``GameScene`` owns the
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
from src.core.progress import unlock_next
from src.core.settings import SCREEN_WIDTH, WHITE
from src.entities.frog import Frog
from src.entities.moving_platform import MovingPlatform
from src.entities.trophy import Trophy
from src.levels.level_registry import get_level, total_levels
from src.scenes.scene import Scene
from src.ui.pause_overlay import PauseOverlay
from src.ui.victory_overlay import VictoryOverlay


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

        # ── Solids (built once from the Level object) ───────────────
        self.solids = self.level.build_level()

        # ── Trophy (level goal) ───────────────────────────────
        trophy_x, trophy_y = self.level.get_trophy_position()
        self.trophy = Trophy(trophy_x, trophy_y)

        # ── Victory state ─────────────────────────────────────
        self.completed = False
        self.victory_overlay: VictoryOverlay | None = None

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
        self._keys_down = input_handler.keys_down
        self._keys_up = input_handler.keys_up

        # Victory overlay takes priority
        if self.completed and self.victory_overlay is not None:
            self.victory_overlay.handle_event(
                input_handler.mouse_pos, input_handler.mouse_clicked,
            )
            return

        # ESC toggles pause on / off
        if pygame.K_ESCAPE in input_handler.keys_down:
            self.paused = not self.paused
            return

        if self.paused:
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
        if self.paused or self.completed:
            return

        # Update moving platforms
        for solid in self.solids:
            if isinstance(solid, MovingPlatform):
                solid.update(dt)

        # Carry the frog with any moving platform it is standing on.
        # Must happen *right after* platforms move so the frog stays
        # glued to the surface before ground-support checks run.
        self._carry_on_platform()

        # Let the frog read keyboard state and move
        keys = pygame.key.get_pressed()
        self.frog.update(
            dt,
            keys_pressed=keys,
            keys_down=self._keys_down,
            keys_up=self._keys_up,
            solids=self.solids,
        )

        # Save position before collision for bounce / land detection
        pre_x = self.frog.x
        pre_y = self.frog.y

        # Resolve collisions between the frog and all solids
        collided = resolve_collisions(self.frog, self.solids)

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
        # a few pixels below the frog's feet to account for small
        # gaps created by moving-platform motion between frames.
        if not self.frog.is_jumping and not self.frog.is_charging:
            probe = pygame.Rect(
                self.frog.rect.x,
                self.frog.rect.bottom,
                self.frog.rect.width,
                4,
            )
            supported = any(
                probe.colliderect(s.rect) for s in self.solids
            )
            if not supported:
                self.frog.start_falling()

        # ── Trophy collision ───────────────────────────────────────
        if self.frog.collides_with(self.trophy):
            self._complete_level()

    def render(self, screen: pygame.Surface) -> None:
        """Draw the level: background, walls, frog, and HUD."""
        # ── Background (delegated to the Level subclass) ─────────────
        self.level.render_background(screen)

        # ── Solids ────────────────────────────────────────────────
        for solid in self.solids:
            solid.draw(screen)

        # ── Trophy ────────────────────────────────────────────────
        if not self.completed:
            self.trophy.draw(screen)

        # ── Player ───────────────────────────────────────────────────
        self.frog.draw(screen)

        # ── HUD ──────────────────────────────────────────────────────
        hud_text = self.hud_font.render(
            f"Fase {self.level.level_number}", True, WHITE,
        )
        hud_rect = hud_text.get_rect(centerx=SCREEN_WIDTH // 2, y=20)
        screen.blit(hud_text, hud_rect)

        # ── Pause overlay (drawn last so it covers everything) ───────
        if self.paused:
            self.pause_overlay.draw(screen)

        # ── Victory overlay ───────────────────────────────────────
        if self.completed and self.victory_overlay is not None:
            self.victory_overlay.draw(screen)

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

    # ── Victory helpers ──────────────────────────────────────────

    def _complete_level(self) -> None:
        """Mark the level as completed and show the victory overlay."""
        self.completed = True
        unlock_next(self._level_number)
        is_last = self._level_number >= total_levels()
        self.victory_overlay = VictoryOverlay(
            is_last_level=is_last,
            on_next_level=self._go_next_level if not is_last else None,
            on_menu=self._go_menu,
        )

    def _go_next_level(self) -> None:
        """Advance to the next level."""
        self.manager.switch(
            GameScene(self.manager, level=self._level_number + 1),
        )

    # ── Platform helpers ─────────────────────────────────────────

    def _carry_on_platform(self) -> None:
        """Move the frog along with any moving platform it is standing on.

        A small probe below the frog's feet detects which solid
        supports it.  If that solid is a ``MovingPlatform``, the frog
        is displaced by the platform's frame delta.  The probe is a
        few pixels tall to bridge tiny gaps that appear when a
        vertical platform moves away from the frog between frames.
        """
        if self.frog.is_jumping:
            return

        probe = pygame.Rect(
            self.frog.rect.x,
            self.frog.rect.bottom,
            self.frog.rect.width,
            6,
        )
        for solid in self.solids:
            if (
                isinstance(solid, MovingPlatform)
                and probe.colliderect(solid.rect)
            ):
                self.frog.x += solid.dx
                self.frog.y += solid.dy
                self.frog._sync_rect()  # pylint: disable=protected-access
                break
