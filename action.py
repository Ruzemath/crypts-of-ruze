from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity

class Action:
    def act(self, generator: Generator, entity: Entity) -> None:
        raise NotImplementedError()
        """Perform this action with the objects needed to determine its scope.
        `generator` is the scope this action is being performed in.
        `entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """

class Leave(Action):
    def act(self, generator: Generator, entity: Entity) -> None:
        raise SystemExit()

class Movement(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy
    
    def act(self, generator: Generator, entity: Entity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        
        if not generator.dungeon_map.bounds_check(new_x, new_y): # Can't Move, Out of Bounds
            return
        if not generator.dungeon_map.tiles["walkable"][new_x, new_y]: # Can't Move, Tile is Not Walkable
            return

        entity.move(self.dx, self.dy)