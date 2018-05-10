from acoAlgorithm.Area import Area
from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field, FieldType

import unittest

import numpy as np

from unittest.mock import MagicMock


class TestPoint(unittest.TestCase):
    # DO NOT CHANGE
    def gen_area(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 1)

        rectangles = [
            Rectangle(Field(2, 2), Field(3, 3), type=FieldType.inaccessible),
            Rectangle(Field(2, 5), Field(3, 6), type=FieldType.inaccessible),
            Rectangle(Field(5, 2), Field(6, 3), type=FieldType.inaccessible),
            Rectangle(Field(5, 5), Field(6, 6), type=FieldType.inaccessible)
        ]
        a.main.size = MagicMock (return_value=64)
        a.all_rectangles = MagicMock(return_value=set(rectangles))
        a += rectangles # TODO: Mocking should work without this instruction
        return a

    def test_init(self):
        a = self.gen_area()

        lm = LightMap(a)

        self.assertEqual(lm.how_many_left(), 48)
        self.assertFalse(lm.finished())

    def test_checked(self):
        a = self.gen_area()
        lm = LightMap(a)

        for i in range(a.main.start.x, a.main.end.y + 1):
            for j in range(a.main.start.y, a.main.end.y + 1):
                if a.rectangle_of(i, j) is None or a.rectangle_of(i, j).type == FieldType.empty:
                    self.assertFalse(lm.is_checked((i, j)))

        for i in range(a.main.start.x, a.main.end.y + 1):
            for j in range(a.main.start.y, a.main.end.y + 1):
                if a.rectangle_of(i, j) is None or a.rectangle_of(i, j).type == FieldType.empty:
                    # Checking field in lm
                    if not lm.is_checked((i, j)):
                        self.assertTrue(lm.look_around_at((i, j)))
                    self.assertTrue(lm.is_checked((i, j)))

    def test_remains_to_be_checked(self):
        a = self.gen_area()
        lm = LightMap(a)

        for i in range(a.main.start.x, a.main.end.y + 1):
            for j in range(a.main.start.y, a.main.end.y + 1):
                if a.rectangle_of(i, j) is None or a.rectangle_of(i, j).type == FieldType.empty:
                    self.assertTrue(lm.remains_to_be_checked((i,j)))
                elif a.rectangle_of(i, j).type == FieldType.inaccessible:
                    self.assertFalse(lm.remains_to_be_checked((i,j)))

    def test_how_many_left(self):
        a = self.gen_area()
        lm = LightMap(a)

        left = lm.how_many_left()

        for i in range(a.main.start.x, a.main.end.y + 1):
            for j in range(a.main.start.y, a.main.end.y + 1):
                if a.rectangle_of(i, j) is None or a.rectangle_of(i, j).type == FieldType.empty:
                    # Checking field in lm
                    left -= 1
                    lm.look_around_at((i, j))
                    self.assertLessEqual(lm.how_many_left(), left)

    def test_finished(self):
        a = self.gen_area()
        lm = LightMap(a)

        self.assertFalse(lm.finished())

        for i in range(a.main.start.x, a.main.end.y + 1):
            for j in range(a.main.start.y, a.main.end.y + 1):
                if a.rectangle_of(i, j) is None or a.rectangle_of(i, j).type == FieldType.empty:
                    # Checking field in lm
                    lm.look_around_at((i, j))

        self.assertTrue(lm.finished())
