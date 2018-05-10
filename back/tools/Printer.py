from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field
from acoAlgorithm.Area import Area
from acoAlgorithm.View import ViewGenerator


class Printer:

    EMPTY = ' '
    OCCUPIED = 'x'
    VISIBLE = '.'
    START = 'S'
    POSITION = 'P'

    def __init__(self, area):
        self.area = area
        self.dimension = area.main.width()
        self.fields = [[0 for x in range(self.dimension)] for x in range(self.dimension)]
        self.fill_rectangle(Rectangle(Field(0, 0), Field(self.dimension-1, self.dimension-1)), self.EMPTY)
        self.__gen_background()

    def __gen_background(self):
        if isinstance(self.area, Area):
            for r in self.area.all_rectangles():
                self.fill_rectangle(r, self.OCCUPIED)
            pass

    def set_view(self, view):
        if isinstance(view, LightMap):
            for field in view.seen:
                if 0 <= field[0] < self.dimension and 0 <= field[1] < self.dimension:
                    self.fields[field[0]][field[1]] = self.VISIBLE

    def set_start(self, field):
        if isinstance(field, Field):
            self.fields[field.x][field.y] = self.START

    def set_position(self, field):
        if isinstance(field, Field):
            self.fields[field.x][field.y] = self.POSITION

    def fill_rectangle(self, rect, symbol):
        for i in range(rect.start.x, rect.end.x+1):
            for j in range(rect.start.y, rect.end.y+1):
                self.fields[i][j] = symbol

    def to_file(self, filename):
        f = open(filename, 'w')
        for l in reversed(self.fields):
            for e in l:
                f.write(e.__str__())
            f.write("\n")
