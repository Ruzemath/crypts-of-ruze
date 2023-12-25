#!/usr/bin/env python3
import copy
import traceback
import tcod
import entity_list
import color
from generator import Generator
from entities import Entity
from procedure_gen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43
    max_room_size = 10
    min_room_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    player = copy.deepcopy(entity_list.player)
    generator = Generator(player)
    generator.dungeon_map = generate_dungeon(max_rooms, min_room_size, max_room_size, map_width, map_height, max_monsters_per_room, generator)
    generator.update()
    generator.message_log.add_message("Hello and welcome, adventurer, to the dungeon!", color.welcome_text)
    
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
            root_console.clear()
            generator.event_handle.on_render(console = root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    generator.event_handle.handle(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                generator.message_log.add_message(traceback.format_exc(), color.error)

if __name__ == "__main__":
    main()
    