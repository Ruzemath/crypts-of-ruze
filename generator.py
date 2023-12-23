from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from input_handler import EventHandler
if TYPE_CHECKING:
    from entities import Entity
    from map import DungeonMap
    
class Generator:
    dungeon_map: DungeonMap
    
    def __init__(self, player: Entity):
        self.event_handle: EventHandler = EventHandler(self)
        self.player = player
    
    def handle_monster_turns(self) -> None:
        for entity in self.dungeon_map.entities - {self.player}:
             print(f'The {entity.name} wonders when it will get to take a real turn.')
             
    
    def update(self) -> None: # Updates the fov of the player
        self.dungeon_map.visible[:] = compute_fov(
            self.dungeon_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = 8,
        )
        # If a tile is in FOV it should be seen as encountered too.
        self.dungeon_map.encountered |= self.dungeon_map.visible
        
    def make(self, console: Console, context: Context) -> None:
        self.dungeon_map.make(console)
        
        context.present(console)
        console.clear()
    
    