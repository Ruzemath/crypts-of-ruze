from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
import numpy as np  
import tcod
from action import Action, Attack, Movement, Wait
from components.base_component import BaseComponent
if TYPE_CHECKING:
    from entities import Actor

class BaseAI(Action, BaseComponent):
    def act(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.dungeon_map.tiles["walkable"], dtype = np.int8)

        for entity in self.entity.dungeon_map.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost = cost, cardinal = 2, diagonal = 3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def act(self) -> None:
        target = self.generator.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.generator.dungeon_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return Attack(self.entity, dx, dy).act()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return Movement(self.entity, dest_x - self.entity.x, dest_y - self.entity.y,).act()

        return Wait(self.entity).act()