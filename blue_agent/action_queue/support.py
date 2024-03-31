from .base import *
from ..navigator import Navigator


class SupportState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        flag_carrier_relative_vision = self._agent.get_visible_targets_relative(
            visible_world, [self._agent.friendly_tiles[1]], ignore_self=True
        )[0]["pos"]

        flag_carrier_relative_player = (
            flag_carrier_relative_vision[0] - (len(visible_world[0]) // 2),
            flag_carrier_relative_vision[1] - (len(visible_world) // 2),
        )

        flag_carrier_absolute = (
            flag_carrier_relative_player[0] + position[0],
            flag_carrier_relative_player[1] + position[1],
        )

        path = Navigator.grid_nav(
            self._agent.memory,
            position,
            flag_carrier_absolute,
            visible_world,
            self._agent.color,
            fro="SupportState",
        )

        if len(path) <= 0:
            return [("move", position)]

        return [("move", _) for _ in path[:1]]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:

        if holding_flag:
            return False

        flag_carrier = self._agent.get_visible_targets_relative(
            visible_world, [self._agent.friendly_tiles[1]], ignore_self=True
        )

        # True if we can see the flag carrier

        return bool(flag_carrier)
