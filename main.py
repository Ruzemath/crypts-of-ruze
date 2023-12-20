#!/usr/bin/env python3
import tcod

from action import Escape, Movement
from input_handler import EventHandler


def main() -> None:
    screen_width = 150
    screen_height = 100
    
    player_xcor = int(screen_width/2)
    player_ycor = int(screen_height/2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handle = EventHandler()
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "Roguelike Tutorial",
        vsync = True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order = "F")
        while True:
            root_console.print(x = player_xcor, y = player_ycor, string = "#")
            context.present(root_console)
            root_console.clear()
            
            for event in tcod.event.wait():
                action = event_handle.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, Movement):
                    player_xcor += action.dx
                    player_ycor += action.dy
                elif isinstance(action, Escape):
                    raise SystemExit()

if __name__ == "__main__":
    main()
    