"""Collision manager - detects and resolves overlaps between entities.

Provides a simple AABB (axis-aligned bounding-box) collision system.
The main entry point is :func:`resolve_collisions`, which pushes a
moving entity out of any solid obstacles it overlaps with.

The resolution uses the **minimum-penetration** approach: the entity is
displaced along whichever axis has the *smallest* overlap, producing
natural "sliding" behaviour when the player moves diagonally or along a
wall.
"""

from src.entities.entity import Entity


def resolve_collisions(
    entity: Entity,
    solids: list[Entity],
) -> list[Entity]:
    """Detect and resolve collisions between *entity* and every solid.

    For each overlapping solid the function pushes *entity* out along
    the axis of least penetration and updates its ``rect``.

    Parameters
    ----------
    entity : Entity
        The moving entity to test (e.g. the player ``Frog``).
    solids : list[Entity]
        Static or dynamic obstacles that *entity* cannot pass through.

    Returns
    -------
    list[Entity]
        The subset of *solids* that *entity* was actually colliding
        with this frame (useful for hit-reaction logic later).
    """
    collided: list[Entity] = []

    for solid in solids:
        if not entity.collides_with(solid):
            continue

        collided.append(solid)

        # Calculate overlap on each axis
        overlap_left = entity.rect.right - solid.rect.left
        overlap_right = solid.rect.right - entity.rect.left
        overlap_top = entity.rect.bottom - solid.rect.top
        overlap_bottom = solid.rect.bottom - entity.rect.top

        # Find the minimum penetration axis
        min_overlap = min(overlap_left, overlap_right,
                         overlap_top, overlap_bottom)

        # Push entity out along that axis
        if min_overlap == overlap_left:
            entity.x = solid.rect.left - entity.width
        elif min_overlap == overlap_right:
            entity.x = solid.rect.right
        elif min_overlap == overlap_top:
            entity.y = solid.rect.top - entity.height
        else:
            entity.y = solid.rect.bottom

        # Keep rect synchronised after displacement
        entity._sync_rect()  # pylint: disable=protected-access

    return collided
