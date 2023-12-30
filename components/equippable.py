from __future__ import annotations
from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from equipment_types import EquipmentType
if TYPE_CHECKING:
    from entities import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        xp_bonus: float = 0.0,
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.xp_bonus = xp_bonus


class BronzeDagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.WEAPON, power_bonus = 2)

class SteelSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.WEAPON, power_bonus = 6)

class LeatherTunic(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.ARMOR, defense_bonus = 1)

class SteelPlate(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.ARMOR, defense_bonus = 3)

class BronzeRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.RING, xp_bonus = 0.25)

class SteelRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type = EquipmentType.RING, xp_bonus = 0.5)

