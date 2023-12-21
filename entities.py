from typing import Tuple

# Class for all entities including player, items, enemies, and others
class Entity:
    def __init__(self, x: int, y: int, entity_char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.entity_char = entity_char
        self.color = color
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy