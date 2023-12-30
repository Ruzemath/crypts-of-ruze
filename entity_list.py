from components.ai import HostileEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from components import consumable, equippable
from entities import Actor, Item
from components.level import Level

player = Actor(
    char = "@",
    color = (255, 255, 255),
    name = "Player",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 30, defense = 2, power = 5),
    inventory = Inventory(capacity = 26),
    level = Level(level_up_base = 200),
)

goblin = Actor(
    char = "G",
    color = (51, 153, 51),
    name = "Goblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 10, defense = 0, power = 3),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 35),
)

hobgoblin = Actor(
    char = "H",
    color = (255, 77, 77),
    name = "Hobgoblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 15, defense = 1, power = 4),
    inventory = Inventory(capacity = 0),
    level = Level(xp_given = 100),
)

health_potion = Item(
    char = "!",
    color = (0, 230, 0),
    name = "Health Potion",
    consumable = consumable.HealingConsumable(amount = 5),
)

lightning_scroll = Item(
    char = "~",
    color = (255, 255, 0),
    name = "Lightning Scroll",
    consumable = consumable.LightningDamageConsumable(damage = 20, maximum_range = 5),
)

confusion_scroll = Item(
    char = "~",
    color = (255, 179, 255),
    name = "Confusion Scroll",
    consumable = consumable.ConfusionConsumable(number_of_turns = 10),
)

fireball_scroll = Item(
    char = "~",
    color = (255, 0, 0),
    name = "Fireball Scroll",
    consumable = consumable.FireballDamageConsumable(damage = 12, radius = 3),
)

bronze_dagger = Item(char = "/", color = (205, 127, 50), name = "Bronze Dagger", equippable = equippable.BronzeDagger())

steel_sword = Item(char = "/", color = (113, 121, 126), name = "Steel Sword", equippable = equippable.SteelSword())

leather_tunic = Item(char = "[", color = (98, 74, 46), name = "Leather Tunic", equippable = equippable.LeatherTunic())

steel_plate = Item(char = "[", color = (113, 121, 126), name = "Steel Plate", equippable = equippable.SteelPlate())

bronze_ring = Item(char = "^", color = (205, 127, 50), name = "Bronze Ring", equippable = equippable.BronzeRing())

steel_ring = Item(char = "^", color = (113, 121, 126), name = "Steel Ring", equippable = equippable.SteelRing())



