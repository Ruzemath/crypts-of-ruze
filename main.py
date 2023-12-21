#!/usr/bin/env python3
import tcod

from action import Leave, Movement
from input_handler import EventHandler
from entities import Entity


def main() -> None:
    screen_width = 150
    screen_height = 100

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handle = EventHandler() 
    player = Entity(int(screen_width/2), int(screen_height/2), "#", (255, 255, 255))
    npc = Entity(int((screen_width/2)-5), int(screen_height/2), "NPC", (0, 255, 0))
    
    # Console 
    with tcod.context.new_terminal(
        screen_width,
        screen_height,   
        tileset = tileset,
        title = "Roguelike Tutorial",
        vsync = True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order = "F")
        while True:
            root_console.print(x = player.x, y = player.y, string = player.entity_char, fg = player.color)
            context.present(root_console)
            root_console.clear()
            
            for event in tcod.event.wait():
                action = event_handle.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, Movement):
                    player.move(dx = action.dx, dy = action.dy)
                elif isinstance(action, Leave):
                    raise SystemExit()


if __name__ == "__main__":
    main()
    