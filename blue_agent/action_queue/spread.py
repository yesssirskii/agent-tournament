from .base import *


class SpreadState(BaseState):
    def __init__(self, agent):
        super().__init__(agent)

        self._spread_counter = 0
        self._spread_direction = None

    def _compute_spread_direction(self, visible_world):
        """
        Uses the average position of all friendly agents to determine the direction to spread in.
        """

        friendly_agents = []

        for y, row in enumerate(visible_world):
            for x, tile in enumerate(row):
                if tile in self._agent.friendly_tiles:
                    friendly_agents.append(
                        (x - (len(row) // 2), y - (len(visible_world) // 2))
                    )

        rx, ry = zip(*friendly_agents)
        rx, ry = sum(rx), sum(ry)

        if abs(rx) > abs(ry):
            return (0, 1) if rx < 0 else (0, -1)

        return (1, 0) if ry < 0 else (-1, 0)

    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        if self._spread_direction is None:
            self._spread_direction = self._compute_spread_direction(visible_world)

        self._spread_counter += 1

        return [
            (
                "move",
                (
                    position[0] + self._spread_direction[0],
                    position[1] + self._spread_direction[1],
                ),
            )
        ]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        # agents can only spread once (at the start of the game)
        return self._spread_counter < 5
