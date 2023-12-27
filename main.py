#!/usr/bin/env python3
import traceback
import tcod
import color
import exceptions
import input_handler
import setup
from entities import Entity

def main() -> None:
    screen_width = 80
    screen_height = 50
    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    handler: input_handler.BaseEventHandler = setup.MainMenu()
    
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
                handler.on_render(console = root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handler.EventHandler):
                        handler.generator.message_log.add_message(traceback.format_exc(), color.error)
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
    