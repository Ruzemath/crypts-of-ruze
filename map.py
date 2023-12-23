from __future__ import annotations
from typing import Iterable, TYPE_CHECKING
import numpy as np  
from tcod.console import Console
import tile_types
if TYPE_CHECKING:
    from entities import Entity

class DungeonMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value = tile_types.wall, order = "F")
        self.visible = np.full((width, height), fill_value = False, order = "F")
        self.encountered = np.full((width, height), fill_value = False, order = "F")

    def bounds_check(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def make(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist = [self.visible, self.encountered],
            choicelist = [self.tiles["light"], self.tiles["dark"]],
            default = tile_types.VOID
        )
        
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg = entity.color)