"""Level 2 - intermediate arena with static and moving platforms.

The second level introduces more complex platforming: additional static
walls for collision, and two moving platforms (one horizontal, one
vertical) that demonstrate how dynamic surfaces work.
"""

from src.entities.entity import Entity
from src.entities.moving_platform import MovingPlatform
from src.entities.wall import Wall
from src.levels.level import Level


class Level2(Level):
    """Concrete layout for level 2.

    Internal obstacles
    ------------------
    * A large static platform at the bottom-left.
    * A static platform at the upper-right area.
    * A horizontal moving platform in the middle.
    * A vertical moving platform on the right side.
    """

    def __init__(self):
        super().__init__(level_number=2)

    def _build_obstacles(self) -> list[Entity]:
        """Return the obstacles and moving platforms for level 2."""
        return [
            # Static platforms
            Wall(100, 450, 200, 20),    # lower-left static platform
            Wall(550, 250, 150, 20),    # upper-right static platform

            # Horizontal moving platform (travels 200 px to the right)
            MovingPlatform(
                x=200, y=320, width=120, height=20,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=200, speed=100,
            ),
            # Vertical moving platform (travels 180 px downward)
            MovingPlatform(
                x=600, y=350, width=100, height=20,
                axis=MovingPlatform.AXIS_VERTICAL,
                distance=180, speed=80,
            ),
        ]

    def get_trophy_position(self) -> tuple[float, float]:
        """Place the trophy on top of the upper-right static platform."""
        # The platform is at (550, 250, 150, 20) → centre it on top
        from src.entities.trophy import Trophy  # lazy import
        return (
            550 + 150 // 2 - Trophy.DEFAULT_SIZE // 2,
            250 - Trophy.DEFAULT_SIZE,
        )
