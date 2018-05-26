from typing import List

from model.rectangle import Rectangle
from model.field import Field
from model.area import Area
import numpy as np


class TextPrinter:
    EMPTY = ' '
    OCCUPIED = 'x'
    SHADOW = '.'
    START = 'S'

    def __init__(self, area):
        self.area = area
        self.dimension = area.main.width()
        self.fields = np.zeros(shape=(self.dimension, self.dimension), dtype=int).tolist()  # type: List[List]
        self.fill_rectangle(Rectangle(Field(0, 0), Field(self.dimension - 1, self.dimension - 1)), self.EMPTY)
        self._gen_walls()

    def _gen_walls(self):
        if isinstance(self.area, Area):
            for r in self.area.all_rectangles():
                self.fill_rectangle(r, self.OCCUPIED)
            pass

    def set_view(self, shadow_map):
        if isinstance(shadow_map, np.ndarray):
            for index, val in np.ndenumerate(shadow_map):
                if val:
                    self.fields[index[0]][index[1]] = self.SHADOW

    def set_start(self, field):
        if isinstance(field, Field):
            self.fields[field.x][field.y] = self.START

    def set_position(self, field, symbol):
        if isinstance(field, Field):
            self.fields[field.x][field.y] = symbol

    def fill_rectangle(self, rect, symbol):
        for i in range(rect.start.x, rect.end.x + 1):
            for j in range(rect.start.y, rect.end.y + 1):
                self.fields[i][j] = symbol

    def to_file(self, filename):
        f = open(filename, 'w')
        for l in reversed(self.fields):
            for e in l:
                f.write(e.__str__())
            f.write("\n")
