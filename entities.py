from __future__ import annotations
import copy
from typing import Tuple, TypeVar, TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from map import DungeonMap

T = TypeVar("T", bound = "Entity")
# Class for all entities including player, items, enemies, and others
class Entity:
    dungeon_map: DungeonMap
    def __init__(self, dungeon_map: Optional[DungeonMap] = None, x: int = 0, y: int = 0, 
                 char: str = "?", color: Tuple[int, int, int] = (255, 255, 255), 
                 name: str = "<Unnamed>", blocks_movement: bool = False,):
        
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if dungeon_map:
            self.dungeon_map = dungeon_map
            dungeon_map.entities.add(self)
    
    def spawn(self: T, dungeon_map: DungeonMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.dungeon_map = dungeon_map
        dungeon_map.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, dungeon_map: Optional[DungeonMap] = None) -> None:
        self.x = x
        self.y = y
        if dungeon_map:
            if hasattr(self, "dungeon_map"):  
                self.dungeon_map.entities.remove(self)
            self.dungeon_map = dungeon_map
            dungeon_map.entities.add(self)
            
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy