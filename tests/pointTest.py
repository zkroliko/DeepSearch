from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field

import unittest

import numpy as np

from acoAlgorithm.Point import Point


class TestPoint(unittest.TestCase):
    def test_init(self):
        p = Point(3.0, 5.0)
        self.assertAlmostEqual(3.0, p.x, 6)
        self.assertAlmostEqual(5.0, p.y, 6)

    def test_angle(self):
        origin = Point(5, 5)
        test_cases = {
            Point(10, 5): 0,
            Point(5, 10): np.pi/2,
            Point(0, 5): np.pi,
            Point(5, 0): -np.pi*1/2,
            Point(10, 10): np.pi*1/4,
            Point(0, 10): np.pi*3/4,
            Point(0, 0): np.pi*5/4,
            Point(10, 0): -np.pi*1/4,
        }
        for value, result in test_cases.items():
            value.set_origin(origin)
            self.assertAlmostEqual(value.angle, result, 8)

    def test_conversion(self):
        f = Field(5, 5)
        p = Point.field_to_point(f)
        self.assertEqual(p, Point(5, 5))

    def test_conversion2(self):
        r = Rectangle(Field(1, 1), Field(5, 5))
        results = {
            "(1,1)": (0.5, 0.5),
            "(1,5)": (0.5, 5.5),
            "(5,1)": (5.5, 0.5),
            "(5,5)": (5.5, 5.5)
        }

        for c in r.corners():
            r = results[c.__str__()]
            self.assertEqual(Point(r[0], r[1]), Point.corner_to_point(c))
