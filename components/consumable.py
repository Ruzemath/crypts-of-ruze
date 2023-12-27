from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import components.ai
import components.inventory
import action
import color
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handler import SingleRangedAttackHandler

if TYPE_CHECKING:
    from entities import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[action.Action]:
        """Try to return the action for this item."""
        return action.ItemAction(consumer, self.parent)

    def activate(self, action: action.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()
    
    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)

class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> Optional[action.Action]:
        self.generate.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        self.generate.event_handle = SingleRangedAttackHandler(
            self.generate,
            callback = lambda xy: action.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.generate.dungeon_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot confuse yourself!")

        self.generate.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity = target, previous_ai = target.ai, turns_remaining = self.number_of_turns,
        )
        self.consume()

class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.generate.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")

class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.generate.dungeon_map.actors:
            if actor is not consumer and self.parent.dungeon_map.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.generate.message_log.add_message(
                f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike.")