from config import *

NEIGHBOURS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class NavigatorTimoutError(Exception): ...


class Navigator:
    @staticmethod
    def generate_preferred_direction_weights(
        visible_world: list[list[str]], color: str, scale: float
    ) -> dict[tuple[int, int], float]:

        enemy_color = {"blue": "red", "red": "blue"}[color]
        friendlies = []
        center = (len(visible_world) // 2, len(visible_world[0]) // 2)

        for y, row in enumerate(visible_world):
            for x, cell in enumerate(row):
                if cell in (
                    ASCII_TILES[f"{enemy_color}_agent"],
                    ASCII_TILES[f"{enemy_color}_agent_f"],
                ):
                    # return no weights if enemy is visible (to not mess with other algorithms)
                    return {(0, 1): 0.0, (0, -1): 0.0, (-1, 0): 0.0, (1, 0): 0.0}

                if (x, y) == center:
                    continue

                if cell in (
                    ASCII_TILES[f"{color}_agent"],
                    ASCII_TILES[f"{color}_agent_f"],
                ):
                    friendlies.append((x - center[0], y - center[1]))

        if not friendlies:
            return {(0, 1): 0.0, (0, -1): 0.0, (-1, 0): 0.0, (1, 0): 0.0}

        average = (lambda x: (sum(x[0]) / len(x[0]), sum(x[1]) / len(x[1])))(
            tuple(zip(*friendlies))
        )
        if average[0] or average[1]:
            average = (
                average[0] / max(abs(average[0]), abs(average[1])),
                average[1] / max(abs(average[0]), abs(average[1])),
            )

        weights = {
            (0, 1): min(max(average[0], 0), 1) * scale,
            (0, -1): min(max(-average[0], 0), 1) * scale,
            (-1, 0): min(max(average[1], 0), 1) * scale,
            (1, 0): min(max(-average[1], 0), 1) * scale,
        }

        return weights

    @staticmethod
    def grid_nav(
        memory,
        start: tuple[int, int],
        end: tuple[int, int],
        visible_world: list[list[str]],
        color: str,
        *,
        fro: str = "",
    ):
        visited = set()
        queue = [start]
        distances = {start: 0}
        previous = {}
        i = 0

        weights = Navigator.generate_preferred_direction_weights(
            visible_world, color, 0.5
        )

        while queue:
            i += 1

            if i > 50_000:
                raise NavigatorTimoutError

            current = queue.pop(0)

            if current == end:
                break

            for offset in NEIGHBOURS:
                next_position = (current[0] + offset[0], current[1] + offset[1])

                if next_position in visited:
                    continue

                if memory[next_position] == ASCII_TILES["wall"]:
                    continue

                new_distance = (
                    distances[current] + 1 + weights.get((offset[0], offset[1]), 0)
                )

                if (
                    next_position not in distances
                    or new_distance < distances[next_position]
                ):
                    distances[next_position] = new_distance
                    previous[next_position] = current

                    if next_position not in queue:
                        queue.append(next_position)

            visited.add(current)

        path = []
        current = end

        while current in previous:
            path.insert(0, current)
            current = previous[current]

        return path
