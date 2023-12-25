from components.ai import HostileEnemy
from components.fighter import Fighter
from components.consumable import HealingConsumable
from components.inventory import Inventory
from entities import Actor, Item

player = Actor(
    char = "@",
    color = (255, 255, 255),
    name = "Player",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 30, defense = 2, power = 5),
    inventory = Inventory(capacity = 26)
)

goblin = Actor(
    char = "G",
    color = (51, 153, 51),
    name = "Goblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 10, defense = 0, power = 3),
    inventory = Inventory(capacity = 0)
)

hobgoblin = Actor(
    char = "H",
    color = (255, 77, 77),
    name = "Hobgoblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 15, defense = 2, power = 4),
    inventory = Inventory(capacity = 0)
)

health_potion = Item(
    char = "!",
    color = (127, 0, 255),
    name = "Health Potion",
    consumable = HealingConsumable(amount = 4),
)