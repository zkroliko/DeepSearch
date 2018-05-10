import unittest

from unittest.mock import MagicMock

from acoAlgorithm.Area import Area
from acoAlgorithm.Field import Field
from acoAlgorithm.Point import Point
from acoAlgorithm.Ray import Ray
from acoAlgorithm.Rectangle import Rectangle


class TestRay(unittest.TestCase):
    def test_init(self):
        start = Point(2, 2)
        end = Point(8, 4)
        ray = Ray(start, end)
        # Checking
        self.assertEqual(ray.start, start)
        self.assertEqual(ray.end, end)

    def test_shell(self):
        start = Field(1, 1)
        end = Field(4, 4)
        ray = Ray(start, end)
        expected = Rectangle(start, end)
        # Checking
        result = ray.rectangle_shell()
        self.assertEqual(result, expected)

    def test_shell2(self):
        start = Field(0.5, 0.5)
        end = Field(4.5, 4.5)
        ray = Ray(start, end)
        expected = Rectangle(Field(0, 0), Field(5, 5))
        # Checking
        result = ray.rectangle_shell()
        self.assertEqual(result, expected)

    def test_collides(self):
        ray = Ray(Point(2, 2), Point(20, 20))
        test_cases = {
            Rectangle(Field(0, 5), Field(3, 5)): False,
            Rectangle(Field(0, 5), Field(2, 6)): False,
            Rectangle(Field(0, 2), Field(2, 3)): True,
            Rectangle(Field(0, 3), Field(3, 4)): True,
            Rectangle(Field(0, 3), Field(2, 3)): False,
            Rectangle(Field(2, 0), Field(3, 2)): True,
            Rectangle(Field(5, 0), Field(8, 5)): True,
            Rectangle(Field(0, 0), Field(24, 24)): True,
            Rectangle(Field(8, 8), Field(24, 24)): True,
            Rectangle(Field(22, 22), Field(24, 24)): False,
            Rectangle(Field(0, 5), Field(6, 5)): True,
            Rectangle(Field(0, 0), Field(4, 4)): True,
            Rectangle(Field(3, 3), Field(4, 4)): True,
            Rectangle(Field(3, 3), Field(5, 5)): True,
            Rectangle(Field(0, 6), Field(8, 8)): True
        }

        for rectangle, result in test_cases.items():
            self.assertEqual(ray.collides(rectangle), result)

    def test_valid(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 1)
        rectangles = [
            Rectangle(Field(2, 2), Field(3, 3)),
            Rectangle(Field(2, 5), Field(3, 6)),
            Rectangle(Field(5, 2), Field(6, 3)),
            Rectangle(Field(5, 5), Field(6, 6))
        ]
        a += rectangles

        origin = Point(4, 4)

        test_cases = {
            Point(0, 0): False,
            Point(7, 0): False,
            Point(0, 7): False,
            Point(7, 7): False,
            Point(2, 2): False,
            Point(2, 6): False,
            Point(5, 6): False,
            Point(2, 9): False,
            Point(6, 10): False,
            Point(0, 4): True,
            Point(4, 0): True,
            Point(7, 4): True,
            Point(4, 7): True,
            Point(4, 4): True,
            Point(1, 4): True,
            Point(2, 4): True,
            Point(3, 4): True,
            Point(4, 7): True,
            Point(3, 9): True,
            Point(3, 10): True,
            Point(4, 10): True,
            Point(5, 10): True,
            Point(5, 2): False,
        }

        for target, expected in test_cases.items():
            ray = Ray(origin, target, area=a)
            self.assertEqual(ray.valid(), expected)

    def test_valid2(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 1)
        rectangles = [
            Rectangle(Field(4, 2), Field(4, 3)),
            Rectangle(Field(2, 4), Field(3, 4)),
            Rectangle(Field(4, 5), Field(4, 6)),
            Rectangle(Field(5, 4), Field(6, 4))
        ]
        a += rectangles

        origin = Point(4, 4)

        test_cases = {
            Point(0, 0): True,
            Point(7, 0): False,
            Point(0, 7): False,
            Point(7, 7): True,
            Point(2, 2): True,
            Point(2, 6): True,
            Point(5, 6): False,
            Point(2, 9): False,
            Point(6, 10): False,
            Point(0, 4): False,
            Point(4, 0): False,
            Point(7, 4): False,
            Point(4, 7): False,
            Point(4, 4): True,
            Point(1, 4): False,
            Point(2, 4): False,
            Point(3, 4): False,
            Point(4, 7): False,
            Point(3, 9): False,
            Point(3, 10): False,
            Point(4, 10): False,
            Point(5, 10): False,
            Point(5, 2): False,
        }

        for target, expected in test_cases.items():
            ray = Ray(origin, target, area=a)
            self.assertEqual(ray.valid(), expected)


if __name__ == '__main__':
    unittest.main()
