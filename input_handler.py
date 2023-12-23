from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod.event
from action import Action, ActionOfChoice, Leave, Wait
if TYPE_CHECKING:
    from generator import Generator

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    # wasd keys.
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.d: (1, 0),
    tcod.event.KeySym.q: (-1, -1),
    tcod.event.KeySym.e: (1, -1),
    tcod.event.KeySym.z: (-1, 1),
    tcod.event.KeySym.c: (1, 1),
}

WAIT_KEYS = {
    tcod.event.KeySym.TAB,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, generator: Generator):
        self.generator = generator
        
    def handle(self) -> None:
        raise NotImplementedError() 
              
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
class MainGameEventHandler(EventHandler):
    def handle(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.act()
            self.generator.handle_monster_turns()
            self.generator.update()  # Update the FOV 
            
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.generator.player
        
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = ActionOfChoice(player, dx, dy)
        elif key in WAIT_KEYS:
            action = Wait(player)
        elif key == tcod.event.KeySym.ESCAPE:
            action = Leave(player)

        return action

class GameOverEventHandler(EventHandler):
    def handle(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.act()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym

        if key == tcod.event.KeySym.ESCAPE:
            action = Leave(self.generator.player)
        return action