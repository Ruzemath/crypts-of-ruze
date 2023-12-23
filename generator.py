from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from entities import Entity
from input_handler import EventHandler
from map import DungeonMap

class Generator:
    def __init__(self, event_handle: EventHandler, dungeon_map: DungeonMap, player: Entity):
        self.event_handle = event_handle
        self.dungeon_map = dungeon_map
        self.player = player
        self.update()
    
    def handle(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)
        
            if action is None:
                continue
    
            action.act(self, self.player)
            self.update() 
    
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