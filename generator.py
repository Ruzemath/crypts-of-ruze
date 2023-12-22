from typing import Set, Iterable, Any
from tcod.context import Context
from tcod.console import Console
from action import Leave, Movement
from entities import Entity
from input_handler import EventHandler
from map import DungeonMap

class Generator:
    def __init__(self, entities: Set[Entity], event_handle: EventHandler, dungeon_map: DungeonMap, player: Entity):
        self.entities = entities
        self.event_handle = event_handle
        self.dungeon_map = dungeon_map
        self.player = player
    
    def handle(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)
        
            if action is None:
                continue
            
            if isinstance(action, Movement):
                if self.dungeon_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
                    self.player.move(action.dx, action.dy)
            elif isinstance(action, Leave):
                    raise SystemExit()
    
    def make(self, console: Console, context: Context) -> None:
        self.dungeon_map.make(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.entity_char, fg = entity.color)
        
        context.present(console)
        console.clear()