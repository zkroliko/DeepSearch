from typing import List

from model.rectangle import Rectangle
from model.field import Field
from model.area import Area
import numpy as np


class BinaryPrinter:
    EMPTY_SEEN = -1.0
    EMPTY_UNSEEN = 0.0
    WALKER = 1.0
    ENEMY_1 = 2.0
    ENEMY_2 = 3.0
    ENEMY_3 = 4.0
    WALL = 5.0

    SYMBOL_TO_VALUE = {"W": 1, "1": 1, "2": 2, "3": 3}

    def __init__(self, area):
        self.area = area
        self.dimension = area.main.width()
        self.fields = np.zeros(shape=(self.dimension, self.dimension), dtype=int)
        self.fill_rectangle(Rectangle(Field(0, 0), Field(self.dimension - 1, self.dimension - 1)),
                            value=self.EMPTY_SEEN)
        self._gen_walls()

    def _gen_walls(self):
        if isinstance(self.area, Area):
            for r in self.area.all_rectangles():
                self.fill_rectangle(r, value=self.WALL)
            pass

    def set_view(self, shadow_map):
        if isinstance(shadow_map, np.ndarray):
            for index, val in np.ndenumerate(shadow_map):
                self.fields[index[0], index[1]] = self.EMPTY_UNSEEN if val else self.EMPTY_SEEN

    def set_position(self, field, symbol):
        if isinstance(field, Field):
            self.fields[field.x][field.y] = symbol

    def fill_rectangle(self, rect, symbol=None, value=None):
        if symbol and not value:
            value = self.SYMBOL_TO_VALUE[symbol]
        if not symbol and not value:
            value = self.EMPTY_UNSEEN
        for i in range(rect.start.x, rect.end.x + 1):
            for j in range(rect.start.y, rect.end.y + 1):
                self.fields[i, j] = value

    def to_file(self, filename):
        f = open(filename, 'w')
        for l in reversed(self.fields):
            for e in l:
                f.write(e.__str__())
            f.write("\n")
