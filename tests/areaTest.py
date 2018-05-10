import unittest

from acoAlgorithm.Area import Area
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field


class TestArea(unittest.TestCase):
    def test_init(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 4)
        self.assertEqual(a.resolution, 4)
        self.assertEqual(a.width(), 8)
        self.assertEqual(a.height(), 8)

    def test_root(self):
        a = Area(Rectangle(Field(0, 0), Field(1023, 1023)), 8)
        other = Area(Rectangle(Field(0, 0), Field(1023, 1023)), 8)

        for child in a.children:
            while child.is_subindexed():
                child = child.bottom_left
            self.assertEquals(child.get_root(), a)
            # Abusive
            self.assertNotEqual(child.get_root(), child)
            self.assertNotEqual(child.get_root(), child.parent)
            self.assertNotEqual(child.get_root(), other)

    def test_init_subindexes(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 2)
        self.assertTrue(a.bottom_left.main == Rectangle(Field(0, 0), Field(3, 3)))
        self.assertTrue(a.bottom_right.main == Rectangle(Field(4, 0), Field(7, 3)))
        self.assertTrue(a.top_left.main == Rectangle(Field(0, 4), Field(3, 7)))
        self.assertTrue(a.top_right.main == Rectangle(Field(4, 4), Field(7, 7)))

    def test_init_subsubindexes(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 3)
        self.assertTrue(a.bottom_left.bottom_left.main == Rectangle(Field(0, 0), Field(1, 1)))
        self.assertTrue(a.bottom_left.bottom_right.main == Rectangle(Field(2, 0), Field(3, 1)))
        self.assertTrue(a.bottom_left.top_left.main == Rectangle(Field(0, 2), Field(1, 3)))
        self.assertTrue(a.bottom_left.top_right.main == Rectangle(Field(2, 2), Field(3, 3)))

    def test_add_simple(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 1)
        r = Rectangle(Field(0, 0), Field(4, 4))
        self.assertFalse(r in a.rectangles)
        a += r
        self.assertTrue(r in a.rectangles)

    def test_add_simple2(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        r = Rectangle(Field(0, 0), Field(6, 6))
        a += r
        self.assertTrue(r in a.bottom_left.rectangles)

    def test_add_simple3(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 3)
        r = Rectangle(Field(8, 10), Field(10, 11))
        a += r
        self.assertTrue(r in a.top_right.bottom_left.rectangles)

    def test_add_multiple(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        r = Rectangle(Field(6, 6), Field(10, 10))
        self.assertFalse(r in a.bottom_left.rectangles)
        self.assertFalse(r in a.bottom_right.rectangles)
        self.assertFalse(r in a.top_left.rectangles)
        self.assertFalse(r in a.top_right.rectangles)
        a += r
        self.assertTrue(r in a.bottom_left.rectangles)
        self.assertTrue(r in a.bottom_right.rectangles)
        self.assertTrue(r in a.top_left.rectangles)
        self.assertTrue(r in a.top_right.rectangles)

    def test_add_multiple_list(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)),1)
        rectangles = [
            Rectangle(Field(2 ,2), Field(3, 3)),
            Rectangle(Field(2, 5), Field(3, 5)),
            Rectangle(Field(5, 2), Field(6, 3)),
            Rectangle(Field(5, 5), Field(6, 6))
        ]
        a += rectangles
        # Check
        self.assertEqual(set(rectangles),a.all_rectangles())

    def test_add_coinciding(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        base = Rectangle(Field(6, 6), Field(10, 10))
        r1 = Rectangle(Field(6, 6), Field(10, 10))
        r2 = Rectangle(Field(4, 4), Field(8, 8))
        r3 = Rectangle(Field(10, 10), Field(13, 13))
        rs = [r1, r2, r3]

        a += base

        for r in rs:
            with self.assertRaises(Exception):
                a += r

    def test_remove(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 1)
        r = Rectangle(Field(0, 0), Field(4, 4))
        self.assertFalse(r in a.rectangles)
        a += r
        self.assertTrue(r in a.rectangles)
        a -= r
        self.assertFalse(r in a.rectangles)

    def test_remove2(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        r = Rectangle(Field(0, 0), Field(6, 6))
        self.assertFalse(r in a.bottom_left.rectangles)
        a += r
        self.assertTrue(r in a.bottom_left.rectangles)
        a -= r
        self.assertFalse(r in a.bottom_left.rectangles)

    def test_remove3(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 3)
        r = Rectangle(Field(8, 10), Field(10, 11))
        self.assertFalse(r in a.top_right.bottom_left.rectangles)
        a += r
        self.assertTrue(r in a.top_right.bottom_left.rectangles)
        a -= r
        self.assertFalse(r in a.top_right.bottom_left.rectangles)

    def test_remove_multiple(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        r = Rectangle(Field(6, 6), Field(10, 10))
        self.assertFalse(r in a.bottom_left.rectangles)
        self.assertFalse(r in a.bottom_right.rectangles)
        self.assertFalse(r in a.top_left.rectangles)
        self.assertFalse(r in a.top_right.rectangles)
        a += r
        self.assertTrue(r in a.bottom_left.rectangles)
        self.assertTrue(r in a.bottom_right.rectangles)
        self.assertTrue(r in a.top_left.rectangles)
        self.assertTrue(r in a.top_right.rectangles)
        a -= r
        self.assertFalse(r in a.bottom_left.rectangles)
        self.assertFalse(r in a.bottom_right.rectangles)
        self.assertFalse(r in a.top_left.rectangles)
        self.assertFalse(r in a.top_right.rectangles)

    def test_rectangles_in_contact(self):
        a = Area(Rectangle(Field(0, 0), Field(31, 31)), 2)

        target = Rectangle(Field(5, 5), Field(10, 10))

        a += Rectangle(Field(10, 10), Field(30, 30))
        a += Rectangle(Field(0, 0), Field(6, 6))
        a += Rectangle(Field(7, 0), Field(9, 9))
        a += Rectangle(Field(0, 9), Field(5, 9))

        self.assertTrue(a.rectangles_in_contact(target).__len__() is 4)

    def test_all_rectangles(self):
        a = Area(Rectangle(Field(0, 0), Field(127, 127)), 4)
        original = set()
        for i in range(0, 100):
            rect = Rectangle(Field(i, i), Field(i, i))
            original.add(rect)
            a += rect
        result = a.all_rectangles()
        self.assertEqual(original, result)

    def test_all_rectangles_complex(self):
        a = Area(Rectangle(Field(0, 0), Field(511, 511)), 4)
        original = set()
        for i in range(1, 20):
            for j in range(1, 20):
                rect = (Rectangle(Field(i * 6, j * 6), Field(i * 6 + 2, j * 6 + 2)))
                original.add(rect)
                a += rect
        result = a.all_rectangles()
        self.assertEqual(original, result)
