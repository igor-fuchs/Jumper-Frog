"""Wall - a static solid obstacle that blocks entity movement.

Walls are drawn as dark-gray rectangles.  They do not move or update
their own state — their only purpose is to occupy space so that other
entities (e.g. the ``Frog``) can collide with them and be pushed back.

Because ``Wall`` inherits from ``Entity``, it is automatically
compatible with the generic collision-detection helpers and can be
included in any list of entities that the scene iterates over.
"""

from src.core.settings import DARK_GRAY
from src.entities.entity import Entity


class Wall(Entity):
    """Immovable rectangular wall used as a collision boundary.

    Parameters
    ----------
    x, y : float
        Top-left position of the wall in pixels.
    width, height : int
        Dimensions of the wall in pixels.
    color : tuple[int, int, int], optional
        Fill colour.  Defaults to ``DARK_GRAY``.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: tuple[int, int, int] = DARK_GRAY,
    ):
        super().__init__(x, y, width, height, color)

    # Walls are static — nothing to update each frame.
    def update(self, dt: float, **kwargs) -> None:  # noqa: D401
        """No-op: walls do not move or change state."""
