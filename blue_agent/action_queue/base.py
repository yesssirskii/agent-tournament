ActionQueueObject = list[tuple[str, tuple[int, int]]]


class BaseState:
    def __init__(self, agent):
        self._agent = agent

    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject: ...
    def get_state_valid(
        self, position, visible_world, can_shoot, holding_flag
    ) -> bool: ...
