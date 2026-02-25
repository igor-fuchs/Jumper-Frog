"""Level 1 - introductory arena with a few static walls.

The first level is intentionally simple: a grey arena enclosed by
boundary walls with three internal obstacles placed to demonstrate
horizontal and vertical collision from multiple directions.
"""

from src.entities.wall import Wall
from src.levels.level import Level


class Level1(Level):
    """Concrete layout for level 1.

    Internal obstacles
    ------------------
    * A horizontal platform on the mid-left.
    * A vertical wall on the mid-right.
    * A low horizontal obstacle near the bottom.
    """

    def __init__(self):
        super().__init__(level_number=1)

    def _build_obstacles(self) -> list[Wall]:
        """Return the three internal walls that define level 1."""
        return [
            Wall(200, 300, 120, 20),   # horizontal platform mid-left
            Wall(500, 200, 20, 150),   # vertical wall mid-right
            Wall(350, 450, 100, 20),   # low horizontal obstacle
        ]
