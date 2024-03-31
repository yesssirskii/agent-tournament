from .base import *


class RandomState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        # navigator takes "move to current position" as a random move instruction
        return [("move", position)]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        # it is always valid to move randomly
        return True
