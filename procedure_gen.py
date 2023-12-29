from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING
import tcod
import entity_list
from map import DungeonMap
import tile_types
if TYPE_CHECKING:
    from generator import Generator

max_items_by_floor = [(1, 1),(4, 2),]

max_monsters_by_floor = [(1, 2),(4, 3),(6, 5),]

def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0
    
    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value
    return current_value

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
    
def monster_spawn(room: RectRoom, dungeon: DungeonMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, floor_number))
    number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, floor_number))

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_list.goblin.spawn(dungeon, x, y)
            else:
                entity_list.hobgoblin.spawn(dungeon, x, y) 
    
    for i in range(number_of_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            item_chance = random.random()
            if item_chance < 0.5:
                entity_list.health_potion.spawn(dungeon, x, y)
            elif item_chance < 0.7:
                entity_list.fireball_scroll.spawn(dungeon, x, y)
            elif item_chance < 0.9:
                entity_list.confusion_scroll.spawn(dungeon, x, y)
            else:
                entity_list.lightning_scroll.spawn(dungeon, x, y)
        

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
    
    
def generate_dungeon(max_rooms: int, min_room_size: int, max_room_size: int, 
                     map_width: int, map_height: int, generator: Generator) -> DungeonMap:
    
    player = generator.player
    dungeon = DungeonMap(generator, map_width, map_height, [player])
    rooms: List[RectRoom] = []
    center_of_last_room = (0, 0)
    
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
                
            center_of_last_room = new_room.center
        
        monster_spawn(new_room, dungeon, generator.game_world.current_floor)
        dungeon.tiles[center_of_last_room] = tile_types.stairs
        dungeon.stairs_location = center_of_last_room
        rooms.append(new_room)

    return dungeon