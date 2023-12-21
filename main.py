#!/usr/bin/env python3
import tcod

from generator import Generator
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
    entities = {player, npc}
    generator = Generator(entities, event_handle, player)
    
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
            generator.make(root_console, context)
            events = tcod.event.wait()
            generator.handle(events)

if __name__ == "__main__":
    main()
    