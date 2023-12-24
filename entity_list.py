from components.ai import HostileEnemy
from components.fighter import Fighter
from entities import Actor

player = Actor(
    char = "@",
    color = (255, 255, 255),
    name = "Player",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 30, defense = 2, power = 5),
)

goblin = Actor(
    char = "G",
    color = (51, 153, 51),
    name = "Goblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 10, defense = 0, power = 3),
)

hobgoblin = Actor(
    char = "H",
    color = (255, 77, 77),
    name = "Hobgoblin",
    ai_cls = HostileEnemy,
    fighter = Fighter(hp = 15, defense = 2, power = 4),
)