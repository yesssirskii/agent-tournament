import random
from typing import *


class GridMemory:
    # Return flag for when .get is called in an uncommitted position
    class NotExplored: ...

    def __init__(self):
        self._grid = {}

    def __getitem__(self, item: [int, int]):
        if item in self._grid:
            return self._grid[item]

        return self.NotExplored

    def __setitem__(self, key: [int, int], value):
        self._grid[key] = value

    @property
    def rect(self):
        return (
            min(x for x, _ in self._grid),
            min(y for _, y in self._grid),
            max(x for x, _ in self._grid),
            max(y for _, y in self._grid),
        )

    def get_random_of_type(self, type) -> Union[None, tuple[int, int]]:
        packed = []
        rect = self.rect

        for x in range(rect[0], rect[2] + 1):
            for y in range(rect[1], rect[3] + 1):
                if self[x, y] is type:
                    packed.append((x, y))

        if packed:
            return random.choice(packed)

        return None

    def get_random_unexplored(self) -> Union[None, tuple[int, int]]:
        return self.get_random_of_type(self.NotExplored)

    def __repr__(self):
        return f"DynamicGridMemory({self._grid})"
