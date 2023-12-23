from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity


class BaseComponent:
    entity: Entity  # Owning entity instance.

    @property
    def generate(self) -> Generator:
        return self.entity.dungeon_map.generator