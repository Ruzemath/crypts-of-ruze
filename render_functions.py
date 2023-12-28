from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import color
if TYPE_CHECKING:
    from tcod.console import Console
    from generator import Generator
    from map import DungeonMap

def get_names_at_location(x: int, y: int, dungeon_map: DungeonMap) -> str:
    if not dungeon_map.bounds_check(x, y) or not dungeon_map.visible[x, y]:
        return ""

    names = ", ".join(entity.name for entity in dungeon_map.entities if entity.x == x and entity.y == y)
    return names.capitalize()

def render_bar(console: Console, current_value: int, maximum_value: int, total_width: int) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)
    console.draw_rect(x = 0, y = 45, width = total_width, height = 1, ch=  1, bg=  color.bar_empty)

    if bar_width > 0:
        console.draw_rect(x = 0, y = 45, width = bar_width, height = 1, ch = 1, bg = color.bar_filled)

    console.print(x = 1, y = 45, string = f"HP: {current_value}/{maximum_value}", fg = color.bar_text)

def render_dungeon_level(console: Console, dungeon_level: int, location: Tuple[int, int]) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location
    console.print(x = x, y = y, string = f"Dungeon level: {dungeon_level}")

def render_names_at_mouse_location(console: Console, x: int, y: int, generator: Generator) -> None:
    mouse_x, mouse_y = generator.mouse_location

    names_at_mouse_location = get_names_at_location(x = mouse_x, y = mouse_y, dungeon_map = generator.dungeon_map)
    console.print(x = x, y = y, string = names_at_mouse_location)