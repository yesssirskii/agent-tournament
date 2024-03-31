from .base import *
from ..navigator import Navigator


class SearchState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        target_flag_pos = self._get_target_flag_pos(position)
        queue = self._get_action_queue_to(target_flag_pos, position, visible_world)
        if queue:
            # go to the flag
            return queue

        # go to unexplored areas of the map
        unexplored_pos = self._agent.memory.get_random_unexplored()
        queue = self._get_action_queue_to(unexplored_pos, position, visible_world)
        return queue

    def _get_target_flag_pos(self, position) -> tuple[int, int]:
        if self._agent.enemy_flag_pos is not None:
            # the enemy flag has been spotted
            return self._agent.enemy_flag_pos

        # the enemy flag location is unknown
        # assume the enemy flag is 32 tiles towards the enemy side
        assumed_flag_distance = (0, 32 if self._agent.home_side == "left" else -32)
        assumed_flag_pos = (
            position[0] + assumed_flag_distance[0],
            position[1] + assumed_flag_distance[1],
        )
        return assumed_flag_pos

    def _get_action_queue_to(self, target_pos, position, visible_world):
        path = Navigator.grid_nav(
            self._agent.memory,
            position,
            target_pos,
            visible_world,
            self._agent.color,
            fro="calling from search",
        )
        return [("move", m) for m in path]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        if holding_flag:
            return False

        map_fully_explored = self._agent.memory.get_random_unexplored() is None

        if map_fully_explored:
            return False

        return True
