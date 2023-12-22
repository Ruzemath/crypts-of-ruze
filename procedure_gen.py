from __future__ import annotations
import random
import tile_types
import tcod
from map import DungeonMap
from typing import Iterator, Tuple

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
    
    
def generate_dungeon(map_width, map_height) -> DungeonMap:
    dungeon = DungeonMap(map_width, map_height)
    room1 = RectRoom(x = 20, y = 15, width = 10, height = 15)
    room2 = RectRoom(x = 35, y = 15, width = 10, height = 15)
    
    dungeon.tiles[room1.inner] = tile_types.floor
    dungeon.tiles[room2.inner] = tile_types.floor
    
    for x, y in L_tunnel(room2.center, room1.center):
        dungeon.tiles[x,y] = tile_types.floor
    return dungeon