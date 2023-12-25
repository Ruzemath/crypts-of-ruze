from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod.event
from tcod import libtcodpy
from action import (Action, ActionOfChoice, Leave, Wait, PickupAction)
import color
import exceptions
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

CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -10,
    tcod.event.KeySym.PAGEDOWN: 10,
}

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, generator: Generator):
        self.generator = generator
        
    def handle(self, event: tcod.event.Event) -> None:
        self.handle_action(self.dispatch(event))

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False
        try:
            action.act()
        except exceptions.Impossible as exc:
            self.generator.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.generator.handle_monster_turns()
        self.generator.update()
        return True
            
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.generator.dungeon_map.bounds_check(event.tile.x, event.tile.y):
            self.generator.mouse_location = event.tile.x, event.tile.y
              
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def on_render(self, console: tcod.console.Console) -> None:
        self.generator.make(console)
    
class MainGameEventHandler(EventHandler):
            
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
        elif key == tcod.event.KeySym.v:
            self.generator.event_handle = HistoryViewer(self.generator)
        elif key == tcod.event.KeySym.SPACE:
            action = PickupAction(player)

        return action

class GameOverEventHandler(EventHandler):
   def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.KeySym.ESCAPE:
            raise SystemExit()

class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, generator: Generator):
        super().__init__(generator)
        self.log_length = len(generator.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment = libtcodpy.CENTER
        )

        # Render the message log using the cursor parameter.
        self.generator.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.generator.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            self.generator.event_handle = MainGameEventHandler(self.generator)