from .base import *
from ..navigator import Navigator, NavigatorTimoutError
from config import ASCII_TILES


class HuntState(BaseState):
    """
    Set up to activate as soon as the agent reaches the home position if the flag is missing,
    Will randomly navigate around, first filling out the map then to random positions. Uses
    Last known position of the agent to detect if any other state (combat) took over. then hands
    control back to the lower states (return) assuming the flag carrier has been killed.
    """

    def __init__(self, agent):
        super(HuntState, self).__init__(agent=agent)

        self._triggered = False
        self._last_pos = None

        self._target_pos = None

    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        self._last_pos = position

        if self._target_pos == position:
            self._target_pos = None

        if self._agent.memory[self._target_pos] not in (
            ASCII_TILES["empty"],
            self._agent.memory.NotExplored,
        ):
            self._target_pos = None

        if self._target_pos is None:
            self._target_pos = self._agent.memory.get_random_unexplored()

        if self._target_pos is None:
            self._target_pos = self._agent.memory.get_random_of_type(
                ASCII_TILES["empty"]
            )

        try:
            path_to_random = Navigator.grid_nav(
                self._agent.memory,
                position,
                self._target_pos,
                visible_world,
                self._agent.color,
                fro="hunt state",
            )
        except NavigatorTimoutError:
            path_to_random = []

        if len(path_to_random) == 0:
            self._target_pos = None
            return [("move", position)]

        return [("move", path_to_random[0])]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        if (
            self._last_pos is not None
            and abs(position[0] - self._last_pos[0])
            + abs(position[1] - self._last_pos[1])
            > 1
        ):

            self._triggered = False

        if position == self._agent.home_pos:
            # This will only trigger if the game has not ended (flag is missing)
            self._triggered = True

        return self._triggered
