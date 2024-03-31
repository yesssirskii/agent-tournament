from config import *
from .memory import GridMemory
from .action_queue import ActionQueueObject, ActionQueue


class Agent:
    # called when this agent is instanced (at the beginning of the game)
    def __init__(self, color, index):
        self.color = color  # "blue" or "red"
        self.index = index  # 0, 1, or 2
        self.memory = GridMemory()

        self.home_pos = None
        self.team_flag = (
            ASCII_TILES["blue_flag"]
            if self.color == "blue"
            else ASCII_TILES["red_flag"]
        )

        self.enemy_flag_pos = None
        self.enemy_flag = (
            ASCII_TILES["red_flag"]
            if self.color == "blue"
            else ASCII_TILES["blue_flag"]
        )

        self.home_side = "left" if self.color == "blue" else "right"

        self.action_queue: ActionQueue = ActionQueue(self)

        self.enemy_tiles = [ASCII_TILES["red_agent"], ASCII_TILES["red_agent_f"]]
        self.friendly_tiles = [ASCII_TILES["blue_agent"], ASCII_TILES["blue_agent_f"]]
        if self.color == "red":
            self.enemy_tiles, self.friendly_tiles = (
                self.friendly_tiles,
                self.enemy_tiles,
            )

    @staticmethod
    def get_visible_world_absolute(
        visible_world: list[list[str]], player_position: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            player_position[0] - (len(visible_world) // 2),
            player_position[1] - (len(visible_world[0]) // 2),
        )

    def _commit_to_memory(
        self, player_position: tuple[int, int], visible_world: list[list[str]]
    ):
        rel_pos = self.get_visible_world_absolute(visible_world, player_position)

        for down, row in enumerate(visible_world):
            for cross, cell in enumerate(row):

                _rel_pos = rel_pos[0] + down, rel_pos[1] + cross

                if cell == ASCII_TILES["wall"]:
                    self.memory[_rel_pos] = cell

                if self.home_pos is None and cell == self.team_flag:
                    self.home_pos = _rel_pos

                if self.enemy_flag_pos is None and cell == self.enemy_flag:
                    self.enemy_flag_pos = _rel_pos

    @staticmethod
    def get_visible_targets_relative(
        visible_world, targets, ignore_self=False
    ) -> list[dict]:
        found = []

        for y, row in enumerate(visible_world):
            for x, cell in enumerate(row):

                if (
                    ignore_self
                    and y == len(visible_world) // 2
                    and x == len(visible_world[0]) // 2
                ):
                    continue

                if cell in targets:
                    # cell has a target on it
                    found.append({"cell": cell, "pos": (y, x)})

        return found

    def update(self, visible_world, position, can_shoot, holding_flag):
        position = position[1], position[0]  # setting position to (down, across)
        self._commit_to_memory(position, visible_world)
        return self.action_queue.pop(position, visible_world, can_shoot, holding_flag)

    def terminate(self, reason):
        if reason == "died":
            print(self.color, self.index, "died")
