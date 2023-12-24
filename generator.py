from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from input_handler import MainGameEventHandler
from render_functions import render_bar
if TYPE_CHECKING:
    from entities import Actor
    from map import DungeonMap
    from input_handler import EventHandler
    
class Generator:
    dungeon_map: DungeonMap
    
    def __init__(self, player: Actor):
        self.event_handle: EventHandler = MainGameEventHandler(self)
        self.player = player
    
    def handle_monster_turns(self) -> None:
        for entity in set(self.dungeon_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.act()
             
    
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
        render_bar(
            console = console,
            current_value = self.player.fighter.hp,
            maximum_value = self.player.fighter.max_hp,
            total_width = 20,
        )
        
        context.present(console)
        console.clear()
    
    