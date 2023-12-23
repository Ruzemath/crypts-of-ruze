from __future__ import annotations
import random
import tile_types
import tcod
import entity_list
from map import DungeonMap
from typing import Iterator, Tuple, List, TYPE_CHECKING
if TYPE_CHECKING:
    from generator import Generator

class RectRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) /2)
        center_y = int((self.y1 + self.y2) /2)
        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def intersects(self, other: RectRoom) -> bool:
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
    
def monster_spawn(room: RectRoom, dungeon: DungeonMap, max_monsters: int,) -> None:
    number_of_monsters = random.randint(0, max_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_list.goblin.spawn(dungeon, x, y)
            else:
                entity_list.hobgoblin.spawn(dungeon, x, y) 
        

def L_tunnel(begin: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = begin
    x2, y2 = end
    if random.random() < 0.5:  # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:                      # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
    
    
def generate_dungeon(max_rooms: int, min_room_size: int, max_room_size: int, map_width: int, 
                     map_height: int, max_monsters_per_room: int, generator: Generator) -> DungeonMap:
    
    player = generator.player
    dungeon = DungeonMap(generator, map_width, map_height, [player])
    rooms: List[RectRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # RectRoom class makes rectangles easier to work with
        new_room = RectRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0: # player room
            player.place(*new_room.center, dungeon)
        else:  
            for x, y in L_tunnel(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        
        monster_spawn(new_room, dungeon, max_monsters_per_room)
        rooms.append(new_room)

    return dungeon