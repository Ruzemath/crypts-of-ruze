from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity
    from map import DungeonMap


class BaseComponent:
    parent: Entity  # Owning entity instance.

    @property
    def dungeon_map(self) -> DungeonMap:
        return self.parent.dungeon_map
    
    @property
    def generate(self) -> Generator:
        return self.dungeon_map.generator