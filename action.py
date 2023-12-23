from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity

class Action:
    def act(self, generator: Generator, entity: Entity) -> None: # Method is going to be overridden by its subclasses
        raise NotImplementedError()


class Leave(Action):
    def act(self, generator: Generator, entity: Entity) -> None:
        raise SystemExit()
    
class DirectionAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def act(self, generator: Generator, entity: Entity) -> None:
        raise NotImplementedError()

class Attack(DirectionAction):
    def act(self, generator: Generator, entity: Entity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        target = generator.dungeon_map.get_blocking_entity_at_location(new_x, new_y)
        
        if not target: # No entity to attack.
            return  

        print(f"You kick the {target.name}, much to its annoyance!")


class Movement(DirectionAction):
    
    def act(self, generator: Generator, entity: Entity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        
        if not generator.dungeon_map.bounds_check(new_x, new_y): # Can't Move, Out of Bounds
            return
        if not generator.dungeon_map.tiles["walkable"][new_x, new_y]: # Can't Move, Tile is Not Walkable
            return
        if generator.dungeon_map.get_blocking_entity_at_location(new_x, new_y): # Can't Move, Entity on Tile
            return
        
        entity.move(self.dx, self.dy)

class ActionOfChoice(DirectionAction):
    def act(self, generator: Generator, entity: Entity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy

        if generator.dungeon_map.get_blocking_entity_at_location(new_x, new_y):
            return Attack(self.dx, self.dy).act(generator, entity)
        else:
            return Movement(self.dx, self.dy).act(generator, entity)