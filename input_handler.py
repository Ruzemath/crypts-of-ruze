from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod.event
from action import Action, ActionOfChoice, Leave
if TYPE_CHECKING:
    from generator import Generator

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, generator: Generator):
        self.generator = generator
        
    def handle(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.act()

            self.generator.handle_monster_turns()
            self.generator.update()  # Update the FOV 
              
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.generator.player

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.w:
            action = ActionOfChoice(player, dx = 0, dy = -1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.s:
            action = ActionOfChoice(player, dx = 0, dy = 1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            action = ActionOfChoice(player, dx = -1, dy = 0)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.d:
            action = ActionOfChoice(player, dx = 1, dy = 0)
        elif key == tcod.event.KeySym.ESCAPE:
            action = Leave(player)

        # No valid key was pressed
        return action