"""Level 3 - challenging vertical ascent with moving obstacles.

The third level forces the player to chain precise jumps across a
winding path of narrow static ledges, oscillating platforms, and
vertical lifts.  Timing and charge control are critical — one missed
jump sends the frog tumbling back down.
"""

from src.entities.entity import Entity
from src.entities.moving_platform import MovingPlatform
from src.entities.wall import Wall
from src.levels.level import Level


class Level3(Level):
    """Concrete layout for level 3."""

    def __init__(self):
        super().__init__(level_number=3)

    def _build_obstacles(self) -> list[Entity]:
        """Return the obstacles and moving platforms for level 3."""
        return [
            # Static platforms
            Wall(730, 450, 50, 20),    # lower-right static platform

            # Horizontal moving platform on the early path
            MovingPlatform(
                x=20, y=420, width=120, height=20,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=400, speed=170,
            ),

            # Walls connected
            Wall(100, 300, 100, 20),    # Middle-left static platform
            Wall(200, 240, 20, 80),    # Middle-left vertical platform

            Wall(300, 270, 70, 20),    # middle platform before to blue platform
            
            # Vertical moving platform
            MovingPlatform(
                x=450, y=50, width=20, height=100,
                axis=MovingPlatform.AXIS_VERTICAL,
                distance=150, speed=120,
            ),

            Wall(500, 240, 70, 20),    # upper-right platform blue platform

            Wall(600, 150, 100, 20),    # upper-right

            # near the trophy
            MovingPlatform(
                x=120, y=100, width=70, height=20,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=100, speed=170,
            ),

            Wall(25, 80, 50, 20),    # trophy platform
        ]

    def get_trophy_position(self) -> tuple[float, float]:
        """Place the trophy on top of the upper-right static platform."""
        from src.entities.trophy import Trophy  # lazy import
        x = 50
        y = 80
        return (
            x - Trophy.DEFAULT_SIZE // 2,
            y - Trophy.DEFAULT_SIZE,
        )
