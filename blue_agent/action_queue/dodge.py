from .base import *
from config import ASCII_TILES


class DodgeState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:
        h1, h2 = len(visible_world) // 2, len(visible_world[0]) // 2

        row = visible_world[h1]
        col = [_[h2] for _ in visible_world]

        if ASCII_TILES["bullet"] in row:
            # check for wall above our head
            if visible_world[h1 - 1][h2] == ASCII_TILES["wall"]:
                return [("move", (position[0], position[1] + 1))]

            return [("move", (position[0], position[1] - 1))]

        if ASCII_TILES["bullet"] in col:
            # check for wall to our left
            if visible_world[h1][h2 - 1] == ASCII_TILES["wall"]:
                return [("move", (position[0] + 1, position[1]))]

            return [("move", (position[0] - 1, position[1]))]

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        if not any(ASCII_TILES["bullet"] in row for row in visible_world):
            return False

        # There is a bullet within view

        h1, h2 = len(visible_world) // 2, len(visible_world[0]) // 2

        row = visible_world[h1]
        col = [_[h2] for _ in visible_world]

        if not (ASCII_TILES["bullet"] in row or ASCII_TILES["bullet"] in col):
            return False

        # There is a bullet in line with us (panic)
        return True
