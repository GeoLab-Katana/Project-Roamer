import random


class Translator:
    def __init__(self, start_c, end_c, size):
        self._start = start_c
        self._end = end_c
        self._size = size
        chunk_x = (end_c[0] - start_c[0]) / size[0]
        chunk_y = (end_c[1] - start_c[1]) / size[1]
        self._chunk = (chunk_x, chunk_y)

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
        random_x = random.uniform(0, self._chunk[0])
        random_y = random.uniform(0, self._chunk[1])
        x += random_x
        y += random_y
        return x, y
