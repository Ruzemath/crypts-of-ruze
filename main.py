#!/usr/bin/env python3
import copy
import tcod
import entity_list
from generator import Generator
from input_handler import EventHandler
from entities import Entity
from procedure_gen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    max_room_size = 10
    min_room_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    event_handle = EventHandler() 
    player = copy.deepcopy(entity_list.player)
    dungeon_map = generate_dungeon(max_rooms, min_room_size, max_room_size, map_width, map_height, max_monsters_per_room, player)
    generator = Generator(event_handle, dungeon_map, player)
    
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
    