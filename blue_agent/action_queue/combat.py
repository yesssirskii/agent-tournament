from .base import *
from ..navigator import Navigator
from random import random


_normalise_to_1 = lambda x: 0 if x == 0 else x // abs(x)


class CombatState(BaseState):
    def get_action_queue(
        self, position, visible_world, can_shoot, holding_flag
    ) -> ActionQueueObject:

        shoot_action = self._get_shoot_action(position, visible_world)
        if shoot_action:
            # we are aligned with the enemy

            if can_shoot:
                return [shoot_action]

            # we are aligned with the enemy but can not shoot
            return [("move", position)]

        # we are not aligned with the enemy
        align_actions = self._get_align_actions(position, visible_world)

        return align_actions

    def _get_shoot_action(self, position, visible_world):
        row_enemies, column_enemies = self._get_aligned_enemies(visible_world)

        if row_enemies:
            # shoot along the row in the right direction
            enemy_infront = row_enemies[0] < 5
            if enemy_infront:
                return "shoot", (position[0], position[1] - 1)
            return "shoot", (position[0], position[1] + 1)

        if column_enemies:
            # shoot along the column in the right direction
            enemy_above = column_enemies[0] < 5
            if enemy_above:
                return "shoot", (position[0] - 1, position[1])
            return "shoot", (position[0] + 1, position[1])

        return None

    def _get_align_actions(self, position, visible_world):
        visible_enemies = self._agent.get_visible_targets_relative(
            visible_world, self._agent.enemy_tiles
        )
        visible_world_pos = self._agent.get_visible_world_absolute(
            visible_world, position
        )
        enemy_pos = (
            visible_world_pos[0] + visible_enemies[0]["pos"][0],
            visible_world_pos[1] + visible_enemies[0]["pos"][1],
        )
        # move one tile towards the enemy
        path = Navigator.grid_nav(
            self._agent.memory, position, enemy_pos, visible_world, self._agent.color
        )

        if path[0][0] == enemy_pos[0] or path[0][1] == enemy_pos[1]:
            # Only one tile away from being lined up with the enemy

            relative_enemy_pos = (
                _normalise_to_1(enemy_pos[0] - path[0][0]) + path[0][0],
                _normalise_to_1(enemy_pos[1] - path[0][1]) + path[0][0],
            )

            if random() < 0.2:
                return [("move", path[0]), ("shoot", relative_enemy_pos)]

        return [("move", path[0])]

    def _get_aligned_enemies(self, visible_world):
        h1, h2 = len(visible_world) // 2, len(visible_world[0]) // 2
        visible_row = visible_world[h1]
        visible_column = [_[h2] for _ in visible_world]

        row_enemies = []
        for i, x in enumerate(visible_row):
            if x in self._agent.enemy_tiles:
                row_enemies.append(i)

        column_enemies = []
        for i, x in enumerate(visible_column):
            if x in self._agent.enemy_tiles:
                column_enemies.append(i)

        return row_enemies, column_enemies

    def get_state_valid(self, position, visible_world, can_shoot, holding_flag) -> bool:
        """
        Move to combat state if any enemy is visible
        """
        return bool(
            self._agent.get_visible_targets_relative(
                visible_world, self._agent.enemy_tiles
            )
        )
