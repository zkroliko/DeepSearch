from acoAlgorithm.Area import Area
from acoAlgorithm.Move import Move
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field, FieldType

import unittest

import numpy as np

from acoAlgorithm.Point import Point


class TestMove(unittest.TestCase):
    def test_init(self):
        start = Field(2, 2)
        end = Field(8, 4)
        m = Move(start, end)
        self.assertEqual(m.source, start)
        self.assertEqual(m.target, end)

    def gen_area(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        a += Rectangle(Field(0, 0), Field(5, 2), type=FieldType.inaccessible)
        a += Rectangle(Field(0, 3), Field(2, 7), type=FieldType.inaccessible)
        return a

    def test_valid(self):
        a = self.gen_area()
        positions = {
            (2, 4): False,
            (3, 4): True,
            (4, 4): True,
            (2, 3): False,
            (3, 3): False,
            (4, 3): True,
            (2, 2): False,
            (2, 3): False,
            (2, 4): False
        }

        for (x, y), val in positions.items():
            self.assertEqual(Move(Field(3, 3), Field(x, y)).valid(a), val)

    def test_valid2(self):
        a = self.gen_area()
        positions = {
            (3, 3): True,
            (4, 5): True,
            (5, 5): True,
            (3, 4): True,
            (4, 4): False,
            (5, 4): True,
            (3, 3): True,
            (3, 4): True,
            (3, 5): True
        }

        for (x, y), val in positions.items():
            self.assertEqual(Move(Field(4, 4), Field(x, y)).valid(a), val)
