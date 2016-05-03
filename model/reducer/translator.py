import random

import math


class Translator:
    def __init__(self, start_c, end_c, size):
        self._start = start_c
        self._end = end_c
        self._size = size
        chunk_x = (end_c[0] - start_c[0]) / size[0]
        chunk_y = (end_c[1] - start_c[1]) / size[1]
        self._chunk = (chunk_x, chunk_y)
        radius = math.sqrt((chunk_x * chunk_x) + (chunk_y * chunk_y))
        radius *= 1.2
        self._radius = radius

    def translate_to_grid(self, real_coordinates):
        x = int((real_coordinates[0] - self._start[0]) / self._chunk[0])
        x = min(x, self._size[0]-1)
        x = max(0, x)
        y = int((real_coordinates[1] - self._start[1]) / self._chunk[1])
        y = min(y, self._size[1]-1)
        y = max(y, 0)
        return x, y

    def translate_from_grid(self, grid_coordinates):
        x = grid_coordinates[0] * self._chunk[0] + self._start[0]
        y = grid_coordinates[1] * self._chunk[1] + self._start[1]
        return x, y

    def random_in_coordinate(self, grid_coordinates):
        x, y = self.translate_from_grid(grid_coordinates)
        random_coordinate = random.uniform(0, self._radius)
        r_exp = random_coordinate * random_coordinate
        x_exp = random.uniform(0, r_exp)
        random_x = math.sqrt(x_exp)
        random_y = math.sqrt(r_exp - x_exp)
        if random_chance():
            random_x = - random_x
        if random_chance():
            random_y = - random_y
        # print(random_x, random_y, random_coordinate)
        x += self._chunk[0] / 2
        y += self._chunk[0] / 2
        x += random_x
        y += random_y
        return x, y


def random_chance():
    return bool(random.getrandbits(1))
