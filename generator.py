from typing import Set, Iterable, Any
from tcod.context import Context
from tcod.console import Console
from action import Leave, Movement
from entities import Entity
from input_handler import EventHandler

class Generator:
    def __init__(self, entities: Set[Entity], event_handle: EventHandler, player: Entity):
        self.entities = entities
        self.event_handle = event_handle
        self.player = player
    
    def handle(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handle.dispatch(event)
        
            if action is None:
                continue
            
            if isinstance(action, Movement):
                    self.player.move(dx = action.dx, dy = action.dy)
            elif isinstance(action, Leave):
                    raise SystemExit()
    
    def make(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.entity_char, fg = entity.color)
        
        context.present(console)
        console.clear()