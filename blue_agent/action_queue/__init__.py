from .spread import SpreadState
from .random import RandomState
from .dodge import DodgeState
from .combat import CombatState
from .search import SearchState
from .bring import BringState
from .support import SupportState
from .hunt import HuntState
from .capture import CaptureState
from .base import BaseState

from typing import *
import random
from config import ASCII_TILES

ActionQueueObject = list[tuple[str, tuple[int, int]]]

STATE_PRIORITY_LIST = [
    RandomState,
    #  - Move randomly
    SearchState,
    #  - Navigate to flag
    #  - Navigate to unseen territory
    BringState,
    #  - If we got the flag return home
    HuntState,
    #  - If our flag is missing hunt for the enemies
    SupportState,
    #  - If you can see a friendly carrying a flag, follow (combat will take over if necessary)
    CombatState,
    #  - If you see an enemy, attempt to align to it and shoot it
    CaptureState,
    #  - If we are stuck in a feedback loop, break it
    DodgeState,
    #  - If a bullet is on a collision axis with us, move out of collision axis
    SpreadState,
    #  - Always spread out at the start of a game
]


class ActionQueue:
    def __init__(self, agent):
        self._host = agent

        self._state_priority_list: List[BaseState] = [
            _(agent) for _ in STATE_PRIORITY_LIST
        ]

        self._current_state: BaseState = self._state_priority_list[-1]

        self._action_queue = []
        self._action_queue_belongs = self._current_state

    def _get_action_direction(
        self, relative: tuple[int, int], position: tuple[int, int]
    ):
        step = relative[0] - position[0], relative[1] - position[1]

        try:
            direction = {
                (0, 1): "right",
                (0, -1): "left",
                (-1, -0): "up",
                (1, 0): "down",
            }[step]
        except KeyError:
            # tries to move into wall
            direction = random.choice(["right", "left", "up", "down"])

            self._action_queue = []

        return direction

    def _get(self, position, visible_world, can_shoot, holding_flag):
        self._current_state = self._get_current_state(
            position, visible_world, can_shoot, holding_flag
        )

        if (
            self._current_state != self._action_queue_belongs
            and self._state_priority_list.index(self._current_state)
            > self._state_priority_list.index(self._action_queue_belongs)
            and self._action_queue
        ):
            self._action_queue = []

        if self._action_queue is None or not self._action_queue:
            self._action_queue = self._current_state.get_action_queue(
                position, visible_world, can_shoot, holding_flag
            )
            self._action_queue_belongs = self._current_state

        if not self._action_queue:
            raise ValueError(f"State {self._current_state} returned an empty queue.")

        return self._action_queue

    def pop(self, position, visible_world, can_shoot, holding_flag):
        move, action_position = self._get(
            position, visible_world, can_shoot, holding_flag
        ).pop(0)

        if self._host.memory[action_position] == ASCII_TILES["wall"]:
            self._action_queue = []
            try:
                return self.pop(position, visible_world, can_shoot, holding_flag)

            except RecursionError:
                action_position = position

        direction = self._get_action_direction(action_position, position)
        return move, direction

    def _get_current_state(
        self, position, visible_world, can_shoot, holding_flag
    ) -> BaseState:
        for potential_state in reversed(self._state_priority_list):
            if potential_state.get_state_valid(
                position, visible_world, can_shoot, holding_flag
            ):
                break

        else:
            potential_state = self._state_priority_list[0]

        return potential_state
