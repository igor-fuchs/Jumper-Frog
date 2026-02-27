"""Level 1 - introductory arena with static and moving platforms.

The first level introduces the player to basic platforming: static
walls for collision, and two moving platforms (one horizontal, one
vertical) that demonstrate how dynamic surfaces work.
"""

from src.entities.entity import Entity
from src.entities.moving_platform import MovingPlatform
from src.entities.wall import Wall
from src.levels.level import Level


class Level1(Level):
    """Concrete layout for level 1."""

    def __init__(self):
        super().__init__(level_number=1)

    def _build_obstacles(self) -> list[Entity]:
        """Return the obstacles and moving platforms for level 1."""
        return [
            Wall(290, 470, 80, 20),

            Wall(560, 420, 80, 20),      # landing after swing
            Wall(640, 360, 20, 80),     # vertical wall barrier

            Wall(660, 360, 60, 20),      # ledge 1 (right side)
            Wall(500, 300, 70, 20),      # ledge 2 (middle)

            Wall(220, 240, 80, 20),      # ledge 3 (left side)

            Wall(200, 190, 20, 70),      # small wall
            Wall(140, 190, 60, 20),      # small ledge

            MovingPlatform(
                x=350, y=110, width=70, height=20,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=200, speed=100,
            ),

            Wall(620, 80, 60, 20),       # high-right ledge
        ]

    def get_trophy_position(self) -> tuple[float, float]:
        """Place the trophy on top of the upper-right static platform."""
        from src.entities.trophy import Trophy  # lazy import
        x = 650
        y = 80
        return (
            x - Trophy.DEFAULT_SIZE // 2,
            y - Trophy.DEFAULT_SIZE,
        )
