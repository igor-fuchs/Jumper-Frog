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
    """Concrete layout for level 2."""

    def __init__(self):
        super().__init__(level_number=2)

    def _build_obstacles(self) -> list[Entity]:
        """Return the obstacles and moving platforms for level 2."""
        return [

            # connected platforms
            Wall(530, 250, 170, 20),    # lower-right static platform
            Wall(530, 270, 20, 270),    # lower-right static wall

            # Vertical moving platform 
            MovingPlatform(
                x=610, y=350, width=100, height=20,
                axis=MovingPlatform.AXIS_VERTICAL,
                distance=180, speed=80,
            ),

            # middle plataform
            MovingPlatform(
                x=90, y=400, width=100, height=20,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=250, speed=200,
            ),

            # connected platforms
            Wall(90, 270, 80, 20),    # top-left static platform
            Wall(150, 170, 20, 100),    # top-left static wall

            Wall(370, 100, 60, 20),    # trophy platform
        ]

    def get_trophy_position(self) -> tuple[float, float]:
        """Place the trophy on top of the upper-right static platform."""
        from src.entities.trophy import Trophy  # lazy import
        x = 400
        y = 100
        return (
            x - Trophy.DEFAULT_SIZE // 2,
            y - Trophy.DEFAULT_SIZE,
        )