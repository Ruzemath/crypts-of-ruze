from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity
        
    @property
    def generator(self) -> Generator:
        return self.entity.dungeon_map.generator
    
    def act(self) -> None: # Method is going to be overridden by its subclasses
        raise NotImplementedError()


class Leave(Action):
    def act(self) -> None:
        raise SystemExit()
    
class DirectionAction(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.generator.dungeon_map.get_blocking_entity_at_location(*self.dest_xy)


    def act(self) -> None:
        raise NotImplementedError()

class Attack(DirectionAction):
    def act(self) -> None:
        target = self.blocking_entity
        
        if not target: # No entity to attack.
            return  

        print(f"You kick the {target.name}, much to its annoyance!")


class Movement(DirectionAction):
    
    def act(self) -> None:
        new_x, new_y = self.dest_xy
        
        if not self.generator.dungeon_map.bounds_check(new_x, new_y): # Can't Move, Out of Bounds
            return
        if not self.generator.dungeon_map.tiles["walkable"][new_x, new_y]: # Can't Move, Tile is Not Walkable
            return
        if self.generator.dungeon_map.get_blocking_entity_at_location(new_x, new_y): # Can't Move, Entity on Tile
            return
        
        self.entity.move(self.dx, self.dy)

class ActionOfChoice(DirectionAction):
    def act(self) -> None:
        if self.blocking_entity:
            return Attack(self.entity, self.dx, self.dy).act()
        else:
            return Movement(self.entity, self.dx, self.dy).act()