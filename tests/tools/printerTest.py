import unittest
from sets import Set

from acoAlgorithm.Area import Area
from acoAlgorithm.Field import Field, FieldType
from acoAlgorithm.Point import Point
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.View import ViewGenerator
from acoAlgorithm.tools.Printer import Printer


class TestPrinter(unittest.TestCase):

    def gen_area(self):
        # DO NOT CHANGE!!!
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 1)

        rectangles = [
            Rectangle(Field(2, 2), Field(3, 3), type=FieldType.inaccessible),
            Rectangle(Field(2, 5), Field(3, 6), type=FieldType.inaccessible),
            Rectangle(Field(5, 2), Field(6, 3), type=FieldType.inaccessible),
            Rectangle(Field(6, 5), Field(6, 5), type=FieldType.inaccessible)
        ]
        a += rectangles
        return a

    # Only run manually
    def test_simple(self):
        a = self.gen_area()

        v = ViewGenerator(a)
        v.shine_from(Point(4, 4))

        # Just for printing
        printer = Printer(a)
        printer.set_view(v.lm)
        printer.to_file("view.txt")
