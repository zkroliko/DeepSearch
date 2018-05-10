
import unittest

from acoAlgorithm.Area import Area
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Corner import CornerType
from acoAlgorithm.Field import Field, FieldType


class TestField(unittest.TestCase):
    def test_init(self):
        f1 = Field(5, 9)
        self.assertEqual(f1.x, 5)
        self.assertEqual(f1.y, 9)

    def test_init_abuse_negative(self):
        with self.assertRaises(Exception):
            f1 = Field(-3, 9)

    # Removed due to dependency incjection problem
    # def test_init_abuse_not_in_rectangle(self):
    #     with self.assertRaises(Exception):
    #         f1 = Field(5, 9, rectangle=Rectangle(Field(56, 80), Field(120, 34)))

    def test_type(self):
        f1 = Field(1, 1, type=FieldType.empty)
        self.assertEqual(f1.type, FieldType.empty)
        f2 = Field(1, 3, type=FieldType.inaccessible)
        self.assertEqual(f2.type, FieldType.inaccessible)

    def test_isCorner(self):
        fields = [Field(0, 0), Field(0, 10), Field(10, 10), Field(10, 0)]

        for f in fields:
            self.assertFalse(f.is_corner())

    def test_in(self):
        f1 = Field(0, 0)
        f2 = Field(10, 0)
        f3 = Field(10, 10)
        f4 = Field(0, 10)

        rectangle = Rectangle(f1, f3)

        ft = rectangle.field(3, 8)

        self.assertTrue(ft in rectangle)
        self.assertTrue(f1 in rectangle)
        self.assertTrue(f2 in rectangle)
        self.assertTrue(f3 in rectangle)
        self.assertTrue(f4 in rectangle)

    def test_ge(self):
        f1 = Field(5, 5)
        f2 = Field(5, 5)
        self.assertTrue(f2 >= f1)

    def test_gt(self):
        ff = Field(10, 20)

        f1 = Field(0, 0)
        f2 = Field(3, 5)
        f3 = Field(5, 2)

        fb = Field(0, 0)

        self.assertTrue(ff > f1)
        self.assertTrue(ff > f2)
        self.assertTrue(ff > f3)
        self.assertFalse(f1 > f1)
        self.assertFalse(f1 > fb)

    def test_lt(self):
        ff = Field(5, 5)

        f1 = Field(0, 0)
        f2 = Field(3, 5)
        f3 = Field(5, 2)

        fb = Field(10, 10)

        self.assertTrue(f1 < ff)
        self.assertTrue(f3 < ff)
        self.assertTrue(f2 < ff)
        self.assertFalse(f1 < f1)
        self.assertFalse(fb < f1)

    def test_le(self):
        f1 = Field(5, 5)
        f2 = Field(5, 5)
        self.assertTrue(f2 <= f1)

    # Not really a class method
    def test_sorting(self):
        f1 = Field(20, 100)
        f2 = Field(3, 5)
        f3 = Field(5, 2)
        f4 = Field(100, 100)
        data = [f1, f2, f3, f4]
        data.sort(key=lambda f: (f.x, f.y), reverse=True)

        self.assertEqual(data, [f4, f1, f3, f2])

    def test_str(self):
        f = Field(34, 123)
        self.assertEqual(f.__str__(), "(34,123)")

    def test_confine(self):
        rect = Rectangle(Field(0, 0), Field(15, 15))
        f = rect.field(5, 5)
        expected = Rectangle(Field(4, 4), Field(6, 6))
        self.assertEqual(f.confine(), expected)

    def test_is_free_corner(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 1)

        r = Rectangle(Field(2, 1), Field(5, 5))

        for c in r.corners():
            with self.assertRaises(Exception):
                c.is_free_corner()

        a += r

        for c in r.corners():
            self.assertTrue(c.is_free_corner())

        # We will add a new rectangle which is in contact with the former

        r2 = Rectangle(Field(1, 6), Field(5, 7))

        a += r2

        self.assertTrue(r.bottom_left.is_free_corner())
        self.assertTrue(r.bottom_right.is_free_corner())
        # Not free anymore
        self.assertFalse(r.top_left.is_free_corner())
        self.assertFalse(r.top_right.is_free_corner())

        # Now for the second

        self.assertFalse(r2.bottom_left.is_free_corner())
        self.assertFalse(r2.bottom_right.is_free_corner())
        self.assertTrue(r2.top_left.is_free_corner())
        self.assertTrue(r2.top_right.is_free_corner())

    def test_is_free_corner_diagonally(self):

        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 1)
        base = Rectangle(Field(5, 5), Field(8, 8))

        for c in base.corners():
            with self.assertRaises(Exception):
                c.is_free_corner_diagonally()

        a += base

        for c in base.corners():
            self.assertTrue(c.is_free_corner_diagonally())

        r1 = Rectangle(Field(1, 1), Field(4, 4))
        r2 = Rectangle(Field(9, 9), Field(13, 14))
        r3 = Rectangle(Field(4, 9), Field(1, 12))
        r4 = Rectangle(Field(6, 4), Field(10, 2))
        rs = [r1, r2, r3, r4]

        for r in rs:

            # We will add a new rectangle which is in contact with the former

            a += r

            for c in base.corners():
                if c.is_free_corner():
                    self.assertTrue(c.is_free_corner_diagonally())
                else:
                    self.assertFalse(not c.is_free_corner_diagonally())

            # Now for the second

            for c in r.corners():
                if c.is_free_corner():
                    self.assertTrue(c.is_free_corner_diagonally())
                else:
                    self.assertFalse(not c.is_free_corner_diagonally())

    def test_corner(self):
        r = Rectangle(Field(1, 1), Field(4, 4))
        for c in r.corners():
            if r.top_right == c:
                self.assertEqual(c.corner_type, CornerType.top_right)
                self.assertEqual(c.corner_type.value, (0.5, 0.5))
            if r.top_left == c:
                self.assertEqual(c.corner_type, CornerType.top_left)
                self.assertEqual(c.corner_type.value, (-0.5, 0.5))
            if r.bottom_right == c:
                self.assertEqual(c.corner_type, CornerType.bottom_right)
                self.assertEqual(c.corner_type.value, (0.5, -0.5))
            if r.bottom_left == c:
                self.assertEqual(c.corner_type, CornerType.bottom_left)
                self.assertEqual(c.corner_type.value, (-0.5, -0.5))




if __name__ == '__main__':
    unittest.main()
