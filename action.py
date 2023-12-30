from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple
import color
import exceptions
if TYPE_CHECKING:
    from generator import Generator
    from entities import Entity, Actor, Item

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity
        
    @property
    def generator(self) -> Generator:
        return self.entity.dungeon_map.generator
    
    def act(self) -> None: # Method is going to be overridden by its subclasses
        raise NotImplementedError()

class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def act(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.generator.dungeon_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.generator.dungeon_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.generator.message_log.add_message(f"You picked up the {item.name}!", fg = color.item_picked_up)
                return

        raise exceptions.Impossible("There is nothing here to pick up.")
    
class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.generator.dungeon_map.get_actor_at_location(*self.target_xy)

    def act(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)
   

class DropItem(ItemAction):
    def act(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)
        self.entity.inventory.drop(self.item)   
         
class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)
        self.item = item

    def act(self) -> None:
        self.entity.equipment.toggle_equip(self.item)
                
class Wait(Action):
    def act(self) -> None:
        pass

class TakeStairs(Action):
    def act(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.generator.dungeon_map.stairs_location:
            self.generator.game_world.generate_floor()
            self.generator.message_log.add_message("You descend the staircase.", color.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")
          
class Direction(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.generator.dungeon_map.get_blocking_entity_at_location(*self.dest_xy)
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.generator.dungeon_map.get_actor_at_location(*self.dest_xy)


    def act(self) -> None:
        raise NotImplementedError()

class Attack(Direction):
    def act(self) -> None:
        target = self.target_actor
        
        if not target: # No entity to attack.
            raise exceptions.Impossible("Nothing to attack.")  

        damage = max(self.entity.fighter.power - target.fighter.defense, 1)
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        
        if self.entity is self.generator.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
            
        if damage > 0:
            self.generator.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            target.fighter.hp -= damage
        else:
            self.generator.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)

class Movement(Direction):
    
    def act(self) -> None:
        dest_x, dest_y = self.dest_xy
        
        if not self.generator.dungeon_map.bounds_check(dest_x, dest_y): # Can't Move, Out of Bounds
            raise exceptions.Impossible("That way is blocked.")
        if not self.generator.dungeon_map.tiles["walkable"][dest_x, dest_y]: # Can't Move, Tile is Not Walkable
             raise exceptions.Impossible("That way is blocked.")
        if self.generator.dungeon_map.get_blocking_entity_at_location(dest_x, dest_y): # Can't Move, Entity on Tile
            raise exceptions.Impossible("That way is blocked.")
        
        self.entity.move(self.dx, self.dy)

class ActionOfChoice(Direction):
    def act(self) -> None:
        if self.target_actor:
            return Attack(self.entity, self.dx, self.dy).act()
        else:
            return Movement(self.entity, self.dx, self.dy).act()

