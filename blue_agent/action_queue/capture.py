from .base import *


class CaptureState(BaseState):
    """
    Monitors movement of the agent, if any repetitive movement is detected, it will
    assume the agent is stuck in a feedback loop and will enforce a random movement
    """

    def __init__(self, agent):
        super(CaptureState, self).__init__(agent=agent)

        self._old_path = []

    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        return [("move", position)]

    @property
    def _old_path_collapsed(self):
        collapsed = {}

        for pos in self._old_path:
            collapsed[pos] = collapsed.get(pos, 0) + 1

        return collapsed

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        self._old_path.append(position)

        if len(self._old_path) > 20:
            self._old_path.pop(0)

        # If the agent has been in the same position for more than 5 times over the last 20 moves
        if max(self._old_path_collapsed.values()) > 5:
            self._old_path = []
            return True

        return False