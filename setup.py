"""Handle the loading and initialization of game sessions."""
from __future__ import annotations
import copy
import libtcodpy
import lzma
import pickle
import traceback
from typing import Optional
import tcod
import color
from generator import Generator
import entity_list
import input_handler
from map import GameWorld


# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]


def new_game() -> Generator:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    max_room_size = 10
    min_room_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    player = copy.deepcopy(entity_list.player)

    generator = Generator(player)

    generator.game_world = GameWorld(
        generator = generator,
        max_rooms = max_rooms,
        min_room_size = min_room_size,
        max_room_size = max_room_size,
        map_width = map_width,
        map_height = map_height,
        max_monsters_per_room = max_monsters_per_room,
        max_items_per_room = max_items_per_room,
    )
    generator.game_world.generate_floor()
    generator.update()

    generator.message_log.add_message("Hello and welcome, adventurer, to the Crypts Of Ruze!!!", color.welcome_text)
    return generator

def load_game_file(filename: str) -> Generator:
    """Load a Generator instance from a file."""
    with open(filename, "rb") as f:
        generator = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(generator, Generator)
    return generator

class MainMenu(input_handler.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "CRYPTS OF RUZE",
            fg = color.menu_title,
            alignment = libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Ruze",
            fg = color.menu_title,
            alignment = libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg = color.menu_text,
                bg = color.black,
                alignment = libtcodpy.CENTER,
                bg_blend = libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handler.MainGameEventHandler(load_game_file("savegame.sav"))
            except FileNotFoundError:
                return input_handler.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handler.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handler.MainGameEventHandler(new_game())
        return None