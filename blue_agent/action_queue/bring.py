from .base import *
from ..navigator import Navigator

# returns the flag back home (return is a keyword so bring must be used)


class BringState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        path_home = Navigator.grid_nav(
            self._agent.memory,
            position,
            self._agent.home_pos,
            visible_world,
            self._agent.color,
            fro="return state",
        )
        return [("move", m) for m in path_home]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        return holding_flag and position != self._agent.home_pos
