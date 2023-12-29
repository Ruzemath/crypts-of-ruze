from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import numpy as np  # type: ignore
from tcod.console import Console
from entity_list import Actor, Item
import tile_types
if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity


class DungeonMap:
    def __init__(self, generator: Generator, width: int, height: int, entities: Iterable[Entity] = ()):
        self.generator = generator
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value = tile_types.wall, order = "F")
        self.visible = np.full((width, height), fill_value = False, order = "F")
        self.encountered = np.full((width, height), fill_value = False, order = "F")
        self.stairs_location = (0, 0)
    
    @property
    def dungeon_map(self) -> DungeonMap:
        return self
     
    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )
    
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))
    
    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None
    
    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def bounds_check(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def make(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist = [self.visible, self.encountered],
            choicelist = [self.tiles["light"], self.tiles["dark"]],
            default = tile_types.VOID,
        )
        
        entities_sorted_for_rendering = sorted(
            self.entities, key = lambda x: x.render_order.value
        )
        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x = entity.x, y = entity.y, string = entity.char, fg = entity.color
                )

class GameWorld:
    """
    Holds the settings for the Map, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        generator: Generator,
        map_width: int,
        map_height: int,
        max_rooms: int,
        min_room_size: int,
        max_room_size: int,
        current_floor: int = 0
    ):
        self.generator = generator
        self.map_width = map_width
        self.map_height = map_height
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.current_floor = current_floor

    def generate_floor(self) -> None:
        from procedure_gen import generate_dungeon
        self.current_floor += 1

        self.generator.dungeon_map = generate_dungeon(
            max_rooms = self.max_rooms,
            min_room_size = self.min_room_size,
            max_room_size = self.max_room_size,
            map_width = self.map_width,
            map_height = self.map_height,
            generator = self.generator,
        )