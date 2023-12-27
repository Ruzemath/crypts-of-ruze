#!/usr/bin/env python3
import copy
import traceback
import tcod
import entity_list
import color
import exceptions
import input_handler
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
    max_items_per_room = 2

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    player = copy.deepcopy(entity_list.player)
    generator = Generator(player)
    generator.dungeon_map = generate_dungeon(max_rooms, min_room_size, max_room_size, map_width, map_height, max_monsters_per_room, max_items_per_room, generator)
    generator.update()
    generator.message_log.add_message("Hello and welcome, adventurer, to the dungeon!", color.welcome_text)
    handler: input_handler.BaseEventHandler = input_handler.MainGameEventHandler(generator)
    
    # Console 
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "Roguelike Tester",
        vsync = True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order = "F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handler.EventHandler):
                        handler.generator.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            # TODO: Add the save function here
            raise
        except BaseException:  # Save on any other unexpected exception.
            # TODO: Add the save function here
            raise

if __name__ == "__main__":
    main()
    