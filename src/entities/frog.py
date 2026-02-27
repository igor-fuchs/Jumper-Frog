"""Frog - the player-controlled character.

Represented as a GREEN square that the player moves horizontally with
**A / D** or the **arrow keys** while grounded.

Jump mechanic
-------------
* **Spacebar press** enters the *charging* state.
* **Holding spacebar** accumulates charge time (up to
  ``jump_max_charge``).  Charge time is **directly proportional** to
  the launch power.
* **Releasing spacebar** launches the frog at a fixed angle
  (``jump_angle``, default 60°) in the direction the frog is facing.
* While airborne, **gravity** pulls the frog back down. The frog
  lands when it reaches or exceeds the y-level it jumped from.
* Wall collisions during flight **invert the horizontal velocity**
  (bounce) while vertical displacement continues uninterrupted.
  This response is triggered externally via :meth:`bounce_horizontal`.

All jump-related constants are exposed as instance attributes so they
can be tuned per-level or per-power-up in the future.

Collision response is handled externally by the scene or a collision
manager — ``Frog`` only exposes its rect and velocity so the caller
can push it out of overlapping objects.
"""

import math
import os

import pygame

from src.core.settings import BASE_DIR, GREEN
from src.entities.entity import Entity


class Frog(Entity):
    """Player-controlled frog entity.

    Parameters
    ----------
    x, y : float
        Initial spawn position (top-left corner).
    width, height : int
        Size of the frog square in pixels.  Defaults to 40 × 40.
    speed : float
        Horizontal ground movement speed in pixels / second.
    jump_angle : float
        Jump launch angle in **degrees** measured from the horizontal.
        A larger angle means a more vertical jump.
    jump_max_charge : float
        Maximum charge duration in seconds.  Holding spacebar beyond
        this value has no additional effect.
    jump_min_power : float
        Launch speed (px / s) for an instantaneous tap of spacebar.
    jump_max_power : float
        Launch speed (px / s) for a fully-charged jump.
    gravity : float
        Downward acceleration in px / s² applied while airborne.
    """

    # ── States ───────────────────────────────────────────────────────
    STATE_GROUNDED = "grounded"
    STATE_CHARGING = "charging"
    STATE_AIRBORNE = "airborne"
    STATE_FALLING = "falling"  # special airborne state for walk-off-the-edge

    # ── Visual states (determine which sprite to show) ───────────────
    VISUAL_DEFAULT = "default"
    VISUAL_WALKING = "walking"
    VISUAL_PREPARING = "preparing"
    VISUAL_JUMPING = "jumping"
    VISUAL_FALLING = "falling"
    VISUAL_ON_EDGE_FRONT = "on_edge_front"
    VISUAL_ON_EDGE_BACK = "on_edge_back"
    VISUAL_OVERCHARGE = "overcharge"

    # Map physics states with a fixed visual to their sprite key.
    _STATE_TO_VISUAL = {
        STATE_CHARGING: VISUAL_PREPARING,
        STATE_AIRBORNE: VISUAL_JUMPING,
        STATE_FALLING:  VISUAL_FALLING,
    }

    # Charge ratio threshold above which the overcharge sprite is used.
    OVERCHARGE_THRESHOLD = 1

    # ── Size defaults ────────────────────────────────────────────────
    DEFAULT_WIDTH = 36
    DEFAULT_HEIGHT = 26

    # ── Movement defaults ────────────────────────────────────────────
    DEFAULT_SPEED = 100.0

    # ── Jump defaults (all exposed as properties for future tuning) ──
    DEFAULT_JUMP_ANGLE = 60.0
    DEFAULT_JUMP_MAX_CHARGE = 1.0
    DEFAULT_JUMP_MIN_POWER = 200.0
    DEFAULT_JUMP_MAX_POWER = 550.0
    DEFAULT_GRAVITY = 800.0

    # ── Animation defaults ────────────────────────────────────────────
    WALK_FRAME_DURATION = 0.12   # seconds per walking animation frame
    EDGE_THRESHOLD = 20          # pixels from centre to detect platform edge

    # ── Asset directory ──────────────────────────────────────────────
    _ASSETS_DIR = os.path.join(BASE_DIR, "assets", "frogs")

    def __init__(
        self,
        x: float,
        y: float,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        speed: float = DEFAULT_SPEED,
        jump_angle: float = DEFAULT_JUMP_ANGLE,
        jump_max_charge: float = DEFAULT_JUMP_MAX_CHARGE,
        jump_min_power: float = DEFAULT_JUMP_MIN_POWER,
        jump_max_power: float = DEFAULT_JUMP_MAX_POWER,
        gravity: float = DEFAULT_GRAVITY,
    ):
        super().__init__(x, y, width, height, color=GREEN)

        # ── Ground movement ──────────────────────────────────────────
        self.speed = speed

        # ── Jump configuration ───────────────────────────────────────
        self.jump_angle = jump_angle
        self.jump_max_charge = jump_max_charge
        self.jump_min_power = jump_min_power
        self.jump_max_power = jump_max_power
        self.gravity = gravity

        # ── Runtime state ────────────────────────────────────────────
        self.state: str = self.STATE_GROUNDED
        self.facing: int = 1  # 1 = right, -1 = left

        # Velocity components (px / s)
        self.vx: float = 0.0
        self.vy: float = 0.0

        # Internal jump bookkeeping
        self._charge_time: float = 0.0
        self._ground_y: float = y  # y-level to land back on

        # ── Sprite & animation ───────────────────────────────────────
        self._sprites: dict = {}
        self._visual_state: str = self.VISUAL_DEFAULT
        self._walk_frame: int = 0
        self._walk_timer: float = 0.0
        self._load_sprites()

    # ── Sprite loading ───────────────────────────────────────────────

    def _load_sprites(self) -> None:
        """Load and scale all frog sprite assets from disk.

        All images except *jumping.png* are 18 × 13 and are scaled to
        ``(width, height)`` (default 36 × 26).  *jumping.png* is
        18 × 17 and is scaled keeping the same horizontal factor so
        that its aspect ratio is preserved.
        """
        def _load(
            filename: str,
            size: tuple[int, int] | None = None,
        ) -> pygame.Surface:
            if size is None:
                size = (self.width, self.height)
            path = os.path.join(self._ASSETS_DIR, filename)
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), size,
            )

        jump_height = int(17 * self.width / 18)  # keep aspect ratio

        self._sprites = {
            self.VISUAL_DEFAULT: _load("default.png"),
            self.VISUAL_WALKING: [
                _load("walking_1.png"),
                _load("walking_2.png"),
                _load("walking_3.png"),
            ],
            self.VISUAL_PREPARING: _load("preparing.png"),
            self.VISUAL_JUMPING: _load(
                "jumping.png", (self.width, jump_height),
            ),
            self.VISUAL_FALLING: _load("screaming.png"),
            self.VISUAL_ON_EDGE_FRONT: _load("looking_front.png"),
            self.VISUAL_ON_EDGE_BACK: _load("looking_back.png"),
            self.VISUAL_OVERCHARGE: _load("overcharge.png"),
        }

    # ── Convenience queries ──────────────────────────────────────────

    @property
    def is_jumping(self) -> bool:
        """``True`` while the frog is in the air (jumping or falling)."""
        return self.state in (self.STATE_AIRBORNE, self.STATE_FALLING)

    @property
    def is_charging(self) -> bool:
        """``True`` while the player is charging the jump."""
        return self.state == self.STATE_CHARGING

    @property
    def charge_ratio(self) -> float:
        """Current charge as a fraction 0.0 – 1.0."""
        if self.jump_max_charge <= 0:
            return 1.0
        return min(self._charge_time / self.jump_max_charge, 1.0)

    # ── Update ───────────────────────────────────────────────────────

    def update(self, dt: float, **kwargs) -> None:
        """Advance the frog one frame.

        Expected *kwargs*:

        * ``keys_pressed`` — continuous key state
          (``pygame.key.ScancodeWrapper``).
        * ``keys_down`` — ``set[int]`` of keys pressed this frame.
        * ``keys_up`` — ``set[int]`` of keys released this frame.
        """
        keys_pressed = kwargs.get("keys_pressed")
        if keys_pressed is None:
            return

        keys_down: set = kwargs.get("keys_down", set())
        keys_up: set = kwargs.get("keys_up", set())

        if self.state == self.STATE_GROUNDED:
            self._update_grounded(dt, keys_pressed, keys_down)
        elif self.state == self.STATE_CHARGING:
            self._update_charging(dt, keys_pressed, keys_up)
        elif self.state == self.STATE_AIRBORNE:
            self._update_airborne(dt)
        elif self.state == self.STATE_FALLING:
            self._update_falling(dt,  keys_pressed)

        self._sync_rect()

        # ── Visual state & animation ─────────────────────────────────
        solids = kwargs.get("solids")
        self._visual_state = self._resolve_visual_state(solids)
        self._advance_walk_animation(dt)

    # ── State updates ────────────────────────────────────────────────

    def _update_grounded(
        self,
        dt: float,
        keys_pressed: pygame.key.ScancodeWrapper,
        keys_down: set,
    ) -> None:
        """Handle horizontal movement and jump initiation."""
        # Horizontal direction
        self.vx = 0.0
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.vx = -1.0
            self.facing = -1
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.vx = 1.0
            self.facing = 1

        # Apply horizontal movement
        self.x += self.vx * self.speed * dt

        # Start charging a jump
        if pygame.K_SPACE in keys_down:
            self.state = self.STATE_CHARGING
            self._charge_time = 0.0
            self._ground_y = self.y

    def _update_charging(
        self,
        dt: float,
        keys_pressed: pygame.key.ScancodeWrapper,
        keys_up: set,
    ) -> None:
        """Accumulate charge; allow facing change while held."""
        # Allow the player to choose direction while charging
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.facing = -1
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.facing = 1

        # Accumulate charge (capped at max)
        self._charge_time = min(
            self._charge_time + dt, self.jump_max_charge,
        )

        # Launch on spacebar release (or if space is no longer held,
        # which covers edge cases like un-pausing after the key was
        # released while the game was frozen).
        if pygame.K_SPACE in keys_up or not keys_pressed[pygame.K_SPACE]:
            self._launch_jump()

    def _update_airborne(self, dt: float) -> None:
        """Apply velocity and gravity while in the air."""
        self._apply_physics(dt)

        # Landing: falling and reached (or passed) the original ground
        if self.vy > 0 and self.y >= self._ground_y:
            self.y = self._ground_y
            self.land()

    def _update_falling(
        self,
        dt: float,
        keys_pressed: pygame.key.ScancodeWrapper,
    ) -> None:
        """Apply gravity and allow horizontal steering after walking off a ledge.

        Unlike :meth:`_update_airborne`, the frog has no launch impulse;
        it simply falls under gravity while the player can steer left/right
        at ``self.speed``.  Landing is handled externally by the scene's
        collision resolution, which calls :meth:`land`.
        """
        self.vx = 0.0
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.vx = -self.speed
            self.facing = -1
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.vx = self.speed
            self.facing = 1

        self._apply_physics(dt)

    # ── Animation / visual helpers ────────────────────────────────────

    def _resolve_visual_state(self, solids) -> str:
        """Choose the visual state based on physics state and context.

        Priority (highest first):
        1. charging ≥ 100 % → overcharge
        2. charging < 100 % → preparing
        3. airborne  → jumping
        4. falling   → falling (screaming)
        5. grounded + moving → walking
        6. grounded + idle + near edge → on_edge_front / on_edge_back
        7. grounded + idle → default
        """
        # Overcharge sprite takes priority over the normal preparing
        # sprite when the charge ratio exceeds the threshold.
        if (self.state == self.STATE_CHARGING
                and self.charge_ratio >= self.OVERCHARGE_THRESHOLD):
            return self.VISUAL_OVERCHARGE

        fixed = self._STATE_TO_VISUAL.get(self.state)
        if fixed is not None:
            return fixed

        # Grounded — walking or idle
        if self.vx != 0:
            return self.VISUAL_WALKING

        # Idle — check for edge proximity
        if solids is not None:
            edge_dir = self._detect_edge(solids)
            if edge_dir is not None:
                return (
                    self.VISUAL_ON_EDGE_FRONT
                    if edge_dir == self.facing
                    else self.VISUAL_ON_EDGE_BACK
                )

        return self.VISUAL_DEFAULT

    def _detect_edge(self, solids) -> int | None:
        """Return the direction of a nearby platform edge, or ``None``.

        Two small probes are placed at ``EDGE_THRESHOLD`` pixels to
        the left and right of the frog's horizontal centre, just
        below its feet.  The probes are a few pixels tall to tolerate
        small vertical gaps caused by moving-platform motion.

        Returns
        -------
        int or None
            ``-1`` for a left edge, ``1`` for a right edge, or
            ``None`` if no edge is detected.  When *both* sides are
            edges, the direction the frog is facing takes precedence.
        """
        cx = self.rect.centerx
        bottom = self.rect.bottom

        left_probe = pygame.Rect(
            cx - self.EDGE_THRESHOLD, bottom, 1, 6,
        )
        right_probe = pygame.Rect(
            cx + self.EDGE_THRESHOLD, bottom, 1, 6,
        )

        near_left = not any(
            left_probe.colliderect(w.rect) for w in solids
        )
        near_right = not any(
            right_probe.colliderect(w.rect) for w in solids
        )

        if near_left and near_right:
            return self.facing
        if near_left:
            return -1
        if near_right:
            return 1
        return None

    def _advance_walk_animation(self, dt: float) -> None:
        """Tick the walking sprite timer and cycle frames."""
        if self._visual_state == self.VISUAL_WALKING:
            self._walk_timer += dt
            if self._walk_timer >= self.WALK_FRAME_DURATION:
                self._walk_timer -= self.WALK_FRAME_DURATION
                self._walk_frame = (
                    (self._walk_frame + 1)
                    % len(self._sprites[self.VISUAL_WALKING])
                )
        else:
            self._walk_frame = 0
            self._walk_timer = 0.0

    # ── Drawing ──────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """Render the current sprite instead of a plain rectangle.

        The sprite is flipped horizontally when the frog faces left.
        For the *jumping* sprite (taller than the hitbox) the image is
        drawn so that its **bottom** edge aligns with the hitbox's
        bottom edge, keeping the visual grounded.
        """
        if not self._sprites:
            # Fallback to coloured box when sprites are unavailable
            super().draw(screen)
            return

        visual = self._visual_state
        if visual == self.VISUAL_WALKING:
            sprite = self._sprites[self.VISUAL_WALKING][self._walk_frame]
        else:
            sprite = self._sprites.get(
                visual, self._sprites[self.VISUAL_DEFAULT],
            )

        # Flip horizontally when facing left
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)

        # Align the bottom of the sprite with the bottom of the hitbox
        draw_x = self.rect.x
        draw_y = self.rect.bottom - sprite.get_height()
        screen.blit(sprite, (draw_x, draw_y))

    # ── Movement ─────────────────────────────────────────────────────

    def _apply_physics(self, dt: float) -> None:
        """Apply gravity and integrate velocity into position.

        Shared by :meth:`_update_airborne` and :meth:`_update_falling`
        to avoid duplicating the core physics step.
        """
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    # ── Jump helpers ─────────────────────────────────────────────────

    def _launch_jump(self) -> None:
        """Compute launch velocity from charge and transition to airborne."""
        power = (
            self.jump_min_power
            + self.charge_ratio * (self.jump_max_power - self.jump_min_power)
        )
        angle_rad = math.radians(self.jump_angle)

        self.vx = power * math.cos(angle_rad) * self.facing
        self.vy = -power * math.sin(angle_rad)  # negative = upward

        self.state = self.STATE_AIRBORNE
        # Don't rely on _ground_y for landing — let the scene's
        # collision resolution handle it via land().
        self._ground_y = 9999.0

    def bounce_horizontal(self) -> None:
        """Invert horizontal velocity on wall collision during a jump.

        Called externally by the scene after collision resolution
        detects that the frog was pushed along the x-axis while
        airborne.  Vertical velocity is unaffected so the frog
        continues its arc.
        """
        self.vx = -self.vx

        # Flip the facing direction on bounce so the frog looks toward the direction it's moving.
        self.facing = self.facing * -1

    def hit_ceiling(self) -> None:
        """Cancel upward velocity after hitting a ceiling mid-jump.

        Called externally by the scene when collision resolution
        pushes the frog **downward** (i.e. it struck a surface above).
        Horizontal velocity is preserved so the frog continues its
        horizontal arc, but it will now fall purely under gravity.
        """
        if self.vy < 0:
            self.vy = 0.0

    def land(self) -> None:
        """Transition back to grounded state and zero out velocity.

        May be called internally (ground-level check) or externally
        (e.g. landing on an elevated platform detected by collision).
        """
        self.vx = 0.0
        self.vy = 0.0
        self.state = self.STATE_GROUNDED
        self._ground_y = self.y

    def start_falling(self) -> None:
        """Transition to airborne with zero velocity (walked off a ledge).

        Unlike a jump, there is no horizontal or upward impulse — the
        frog simply begins falling under gravity from its current
        position.  ``_ground_y`` is set to a value far below so the
        internal landing check never fires before collision resolution
        handles the actual landing.
        """
        self.state = self.STATE_FALLING
        self.vx = 0.0
        self.vy = 0.0
        # Ensure the internal "ground" is far below so gravity-based
        # landing inside _update_airborne never triggers prematurely;
        # the scene's collision resolution will call land() when the
        # frog actually hits a surface.
        self._ground_y = 9999.0
