import copy
from datetime import datetime

class LifeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[False for x in range(0, width)] for y in range(0, height)]
        self.fps = 2
        self._next_ts = datetime.now().timestamp()

    def set(self, x, y, status):
        self.cells[y][x] = status

    def get(self, x, y):
        return self.cells[y][x]

    def next(self):
        cur_ts = datetime.now().timestamp()
        if cur_ts < self._next_ts:
            return

        self._next_ts = cur_ts + (1 / self.fps)

        nextCells = [[False for x in range(0, self.width)] for y in range(0, self.height)]

        for x in range(0, self.width):
            for y in range(0, self.height):
                nextCells[y][x] = self.__next_cell(x, y)

        self.cells = nextCells

    def __next_cell(self, x, y):
        surroundCells = [
            self.__is_alive(x - 1, y - 1),
            self.__is_alive(x - 1, y + 0),
            self.__is_alive(x - 1, y + 1),
            self.__is_alive(x + 0, y - 1),
            self.__is_alive(x + 0, y + 1),
            self.__is_alive(x + 1, y - 1),
            self.__is_alive(x + 1, y + 0),
            self.__is_alive(x + 1, y + 1),
        ]
        aliveCount = len(list(filter(lambda cell: cell, surroundCells)))

        if self.cells[y][x]:
            return 2 <= aliveCount <= 3
        else:
            return aliveCount == 3

    def __is_alive(self, x, y):
        x = self.width - 1 if x < 0 else x
        x = 0 if x >= self.width else x
        y = self.height -1 if y < 0 else y
        y = 0 if y >= self.height else y

        return self.cells[y][x]

    def __is_outer(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def get_cells(self):
        return copy.deepcopy(self.cells)

