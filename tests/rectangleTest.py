import unittest

from acoAlgorithm.Area import Area
from acoAlgorithm.Point import Point
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field, FieldType


class TestRectangle(unittest.TestCase):
    def test_init(self):
        f1 = Field(0, 0)
        f2 = Field(10, 0)
        f3 = Field(10, 10)
        f4 = Field(0, 10)

        rectangle = Rectangle(f1, f3)

        real = [f1, f2, f3, f4]

        testing = rectangle.corners()

        for i in range(0, 4):
            self.assertTrue(real[i] == testing[i])

    # This test will check whether the initializer can
    # make sens of input fields that are not exactly right
    # correct way is that vector (start,end) is positive
    def test_init_self_correct(self):
        first = Field(10, 10)
        second = Field(0, 0)

        rect = Rectangle(first, second)

    def test_init_abuse_Narrow(self):
        first = Field(2, 0)
        second = Field(2, 10)

        rect = Rectangle(first, second)

    def test_init_abuse_Flat(self):
        first = Field(0, 5)
        second = Field(10, 5)

        rect = Rectangle(first, second)

    def test_init_one_by_one(self):
        f = Field(4, 4)
        rect = Rectangle(f, f)
        for c in rect.corners():
            self.assertEqual(c.x, f.x)
            self.assertEqual(c.y, f.y)
            self.assertEqual(c.rectangle, rect)

    def test_init_area(self):
        a = Area(Rectangle(Field(0, 0), Field(31, 31)), 2)

        rect = Rectangle(Field(5, 5), Field(10, 10))

        a += rect

        for c in rect.corners():
            self.assertEqual(c.rectangle.area, a)

    def test_init_area_big(self):
        a = Area(Rectangle(Field(0, 0), Field(1023, 1023)), 5)

        rect1 = Rectangle(Field(5, 5), Field(10, 10))
        rect2 = Rectangle(Field(200, 500), Field(1001, 700))
        rect3 = Rectangle(Field(201, 201), Field(201, 201))

        rectangles = {rect1, rect2, rect3}

        for r in rectangles:
            a += r
            for c in r.corners():
                self.assertEqual(c.rectangle.area, a)

    def test_contains(self):
        big1 = Field(0, 0)
        big2 = Field(10, 10)
        small1 = Field(0, 0)
        small2 = Field(8, 8)

        tiny1 = Field(5, 5)

        big = Rectangle(big1, big2)
        small = Rectangle(small1, small2)

        tiny = Rectangle(tiny1, tiny1)

        self.assertTrue(small in big)
        self.assertTrue(tiny in small)

    def test_contains_point(self):
        rect = Rectangle(Field(5, 5), Field(10, 10))
        test_cases = {
            Point(0, 0): False,
            Point(2, 4): False,
            Point(7, 14): False,
            Point(15, 18): False,
            Point.map_to_point(rect.bottom_left): False,
            Point.map_to_point(rect.bottom_right): False,
            Point.map_to_point(rect.top_left): False,
            Point.map_to_point(rect.top_right): False,
            Point.map_to_point(rect.middle().top_left): True,
            Point.map_to_point(rect.middle().top_right): True,
            Point.map_to_point(rect.middle().bottom_left): True,
            Point.map_to_point(rect.middle().bottom_right): True,

            Point(6, 8): True,
            Point(8, 9): True
        }

        for point, expected in test_cases.items():
            self.assertEqual(point in rect, expected)

    def test_dimensions(self):
        first = Field(0, 0)
        second = Field(9, 9)

        rect = Rectangle(first, second)
        self.assertEqual(rect.height(), 10)
        self.assertEqual(rect.width(), 10)

    def test_size(self):
        first = Field(0, 0)
        second = Field(9, 9)

        rect = Rectangle(first, second)
        self.assertEqual(rect.size(), 100)

    def test_middle(self):
        first = Field(0, 0)
        second = Field(10, 10)
        rect = Rectangle(first, second)

        self.assertTrue(rect.middle(), Field(5, 5).rectangle)

    def test_middle_rect(self):
        first = Field(0, 0)
        second = Field(9, 9)
        rect = Rectangle(first, second)

        self.assertTrue(rect.middle(), Rectangle(Field(4, 4), Field(5, 5)))

    def test_middle_rect_width(self):
        first = Field(0, 0)
        second = Field(10, 9)
        rect = Rectangle(first, second)

        self.assertTrue(rect.middle(), Rectangle(Field(4, 5), Field(5, 5)))

    def test_middle_rect_height(self):
        first = Field(0, 0)
        second = Field(9, 10)
        rect = Rectangle(first, second)

        self.assertTrue(rect.middle(), Rectangle(Field(5, 4), Field(5, 5)))

    def test_str(self):
        first = Field(0, 0)
        second = Field(17, 10)

        expected = "(0,10)	...	(17,10)\n" \
                   "...		...		...\n" \
                   "(0,0)	...	(17,0)"

        rect = Rectangle(first, second)

        self.assertEqual(rect.__str__(), expected)

    def test_and_none(self):
        big1 = Field(5, 5)
        big2 = Field(10, 10)
        small1 = Field(1, 1)
        small2 = Field(4, 4)

        big = Rectangle(big1, big2)
        small = Rectangle(small1, small2)

        self.assertEqual(None, big & small)

    def test_and_contains(self):
        big1 = Field(0, 0)
        big2 = Field(10, 10)
        small1 = Field(4, 4)
        small2 = Field(8, 8)

        big = Rectangle(big1, big2)
        small = Rectangle(small1, small2)

        self.assertEqual(small, big & small)
        self.assertEqual(small & big, big & small)

    def test_and_1to1_intersection(self):
        first_s = Field(0, 0)
        first_e = Field(9, 11)
        second_s = Field(4, 3)
        second_e = Field(12, 12)

        result = Rectangle(Field(4, 3), Field(9, 11))

        first = Rectangle(first_s, first_e)
        second = Rectangle(second_s, second_e)

        self.assertEqual(result, first & second)

    def test_and_2to0_intersection_horizontal_left(self):
        first_s = Field(0, 0)
        first_e = Field(10, 10)
        second_s = Field(6, 4)
        second_e = Field(15, 9)

        result = Rectangle(Field(6, 4), Field(10, 9))

        first = Rectangle(first_s, first_e)
        second = Rectangle(second_s, second_e)

        self.assertTrue(result == first & second)

    def test_and_2to0_intersection_horizontal_right(self):
        first_s = Field(10, 0)
        first_e = Field(20, 10)
        second_s = Field(8, 4)
        second_e = Field(16, 9)

        result = Rectangle(Field(10, 4), Field(16, 9))

        first = Rectangle(first_s, first_e)
        second = Rectangle(second_s, second_e)

        self.assertTrue(result == first & second)

    def test_and_2to0_intersection_vertical_left(self):
        first_s = Field(0, 0)
        first_e = Field(10, 10)
        second_s = Field(4, 5)
        second_e = Field(8, 15)

        result = Rectangle(Field(4, 5), Field(8, 10))

        first = Rectangle(first_s, first_e)
        second = Rectangle(second_s, second_e)

        self.assertTrue(result == first & second)

    def test_and_2to0_intersection_vertical_right(self):
        first_s = Field(0, 10)
        first_e = Field(10, 20)
        second_s = Field(4, 5)
        second_e = Field(8, 15)

        result = Rectangle(Field(4, 10), Field(8, 15))

        first = Rectangle(first_s, first_e)
        second = Rectangle(second_s, second_e)

        self.assertTrue(result == first & second)

    def test_hash_true(self):
        first = Field(0, 0)
        second = Field(9, 9)

        rect1 = Rectangle(first, second)
        rect2 = Rectangle(first, second)

        self.assertEqual(rect1.__hash__(), rect2.__hash__())

    def test_confine(self):
        rect = Rectangle(Field(5, 5), Field(9, 9))
        confine = Rectangle(Field(4, 4), Field(10, 10))
        self.assertEqual(rect.confine(), confine)

    # Loooooong, could be be shorter probably
    def test_confine_edge(self):
        a = Area(Rectangle(Field(0, 0), Field(63, 63)), 4)
        # Corner
        rect = Rectangle(Field(0, 0), Field(0, 0), area=a)
        expected = Rectangle(Field(0, 0), Field(1, 1))
        result = rect.confine()
        self.assertEqual(expected, result)
        # Bottom edge
        for i in range(1, 63):
            rect = Rectangle(Field(i, 0), Field(i, 0), area=a)
            expected = Rectangle(Field(i - 1, 0), Field(i + 1, 1))
            result = rect.confine()
            self.assertEqual(expected, result)
        # Corner
        rect = Rectangle(Field(63, 0), Field(63, 0), area=a)
        expected = Rectangle(Field(62, 0), Field(63, 1))
        result = rect.confine()
        self.assertEqual(expected, result)
        # Right edge
        for i in range(1, 63):
            rect = Rectangle(Field(63, i), Field(63, i), area=a)
            expected = Rectangle(Field(62, i - 1), Field(63, i + 1))
            result = rect.confine()
            self.assertEqual(expected, result)
        # Corner
        rect = Rectangle(Field(63, 63), Field(63, 63), area=a)
        expected = Rectangle(Field(62, 62), Field(63, 63))
        result = rect.confine()
        self.assertEqual(expected, result)
        # Top edge
        for i in range(1, 63):
            rect = Rectangle(Field(i, 63), Field(i, 63), area=a)
            expected = Rectangle(Field(i - 1, 62), Field(i + 1, 63))
            result = rect.confine()
            self.assertEqual(expected, result)
        # Corner
        rect = Rectangle(Field(0, 63), Field(0, 63), area=a)
        expected = Rectangle(Field(0, 62), Field(1, 63))
        result = rect.confine()
        self.assertEqual(expected, result)
        # Left edge
        for i in range(1, 63):
            rect = Rectangle(Field(0, i), Field(0, i), area=a)
            expected = Rectangle(Field(0, i - 1), Field(1, i + 1))
            result = rect.confine()
            self.assertEqual(expected, result)

    def test_confine_area(self):
        rect = Rectangle(Field(0, 0), Field(15, 15))
        rect.area = Area(rect, resolution=1)
        confine = Rectangle(Field(0, 0), Field(15, 15))
        self.assertEqual(rect.confine(), confine)

    def test_free_corners(self):
        a = Area(Rectangle(Field(0, 0), Field(63, 63)), 4)

        r = Rectangle(Field(2, 1), Field(5, 5))

        for c in r.corners():
            with self.assertRaises(Exception):
                c.is_free_corner()

        a += r

        for c in r.corners():
            if c in r.free_corners():
                self.assertTrue(c.is_free_corner())
            else:
                self.assertFalse(c.is_free_corner())

        # We will add a new rectangle which is in contact with the former

        r2 = Rectangle(Field(1, 6), Field(5, 7))

        a += r2

        for c in r.corners():
            if c in r.free_corners():
                self.assertTrue(c.is_free_corner())
            else:
                self.assertFalse(c.is_free_corner())

        # Second rectangle

        for c in r2.corners():
            if c in r2.free_corners():
                self.assertTrue(c.is_free_corner())
            else:
                self.assertFalse(c.is_free_corner())

    # Don't finish until this symmetric
    def test_contact(self):
        # We will ALWAYS swap the arguments to ensure
        # the same result for both combinations
        # There are 5 cases using 6 rectangles
        r1small = Rectangle(Field(1, 1), Field(1, 1))
        r1big = Rectangle(Field(0, 0), Field(1, 1))
        r2small = Rectangle(Field(2, 2), Field(2, 2))
        r2big = Rectangle(Field(2, 2), Field(3, 3))
        r3big = Rectangle(Field(2, 0), Field(3, 1))
        # And 1 extra result
        exResult = Rectangle(Field(2, 0), Field(2, 2))
        #
        # self.assertEqual(r1small.contact(r2small),r2small)
        # self.assertEqual(r1big.contact(r1small),r1small)
        # self.assertEqual(r1big.contact(r2big),r1small)

    def test_is_in_contact(self):
        r1 = Rectangle(Field(3, 3), Field(5, 5))
        r2 = Rectangle(Field(6, 6), Field(8, 8))
        r3 = Rectangle(Field(6, 3), Field(8, 5))
        r4 = Rectangle(Field(9, 3), Field(12, 5))

        self.assertTrue(r1.is_in_contact(r2))
        self.assertTrue(r2.is_in_contact(r3))
        self.assertTrue(r3.is_in_contact(r2))
        self.assertTrue(r2.is_in_contact(r4))
        self.assertTrue(r3.is_in_contact(r2))
        self.assertFalse(r1.is_in_contact(r4))

        # Diagonal
        self.assertTrue(r1.is_in_contact_diagonal(r2))
        self.assertTrue(r2.is_in_contact_diagonal(r4))
        self.assertFalse(r1.is_in_contact_diagonal(r3))
        self.assertFalse(r1.is_in_contact_diagonal(r4))
        self.assertFalse(r2.is_in_contact_diagonal(r3))
        self.assertFalse(r3.is_in_contact_diagonal(r4))

        # Not diagonal
        self.assertFalse(r1.is_in_contact_v_h(r2))
        self.assertFalse(r2.is_in_contact_v_h(r4))
        self.assertTrue(r1.is_in_contact_v_h(r3))
        self.assertFalse(r1.is_in_contact_v_h(r4))
        self.assertTrue(r2.is_in_contact_v_h(r3))
        self.assertTrue(r3.is_in_contact_v_h(r4))

    def test_is_joinable(self):
        r1 = Rectangle(Field(3, 3), Field(5, 5))
        r2 = Rectangle(Field(6, 6), Field(8, 8))
        r3 = Rectangle(Field(6, 3), Field(8, 5))
        r4 = Rectangle(Field(9, 3), Field(12, 5))

        rb = Rectangle(Field(0, 0), Field(11, 2))
        rs = Rectangle(Field(5, 6), Field(5, 6))

        test = {
            (r1, r2): False,
            (r1, r3): True,
            (r1, r4): False,
            (r2, r3): True,
            (r2, r4): False,
            (r3, r4): True
        }

        for (first, second), value in test.items():
            self.assertEqual(first.is_joinable(second), value)
            self.assertEqual(second.is_joinable(first), value)

        # Now abusive cases

        test_big = {
            (r1, rb): False,
            (r2, rb): False,
            (r3, rb): False,
            (r4, rb): False,
            (r1, rs): False,
            (r2, rs): False,
            (r3, rs): False,
            (r4, rs): False,
        }

        for (first, second), value in test_big.items():
            self.assertEqual(first.is_joinable(second), value)
            self.assertEqual(second.is_joinable(first), value)

    def test_join(self):
        r1 = Rectangle(Field(3, 3), Field(5, 5))
        r2 = Rectangle(Field(6, 6), Field(8, 8))
        r3 = Rectangle(Field(6, 3), Field(8, 5))
        r4 = Rectangle(Field(9, 3), Field(12, 5))

        test = {
            (r1, r3): Rectangle(Field(3, 3), Field(8, 5)),
            (r2, r3): Rectangle(Field(6, 3), Field(8, 8)),
            (r3, r4): Rectangle(Field(6, 3), Field(12, 5)),
        }

        for (first, second), value in test.items():
            self.assertEqual(first.join(second), value)
            self.assertEqual(first.join(second), value)

    def test_join_area_type(self):
        a = Area(Rectangle(Field(0, 0), Field(63, 63)), 2)

        r1 = Rectangle(Field(3, 3), Field(5, 5), type=FieldType.inaccessible, area=None)
        r2 = Rectangle(Field(6, 6), Field(8, 8), type=FieldType.inaccessible, area=None)
        r3 = Rectangle(Field(6, 3), Field(8, 5), type=FieldType.inaccessible, area=None)
        r4 = Rectangle(Field(9, 3), Field(12, 5), type=FieldType.inaccessible, area=None)

        test = [(r1, r3), (r2, r3), (r3, r4)]

        for (first, second) in test:
            a.clear()
            a += first
            a += second
            result = first.join(second)
            self.assertEqual(result.area, a)
            self.assertEqual(result.type, FieldType.inaccessible)
            # Other way around
            a.clear()
            a += first
            a += second
            result = second.join(first)
            self.assertEqual(result.area, a)
            self.assertEqual(result.type, FieldType.inaccessible)

    def test_corner_shell(self):
        test_cases = {
            Rectangle(Field(0, 0), Field(5, 5)): Rectangle(Point(-0.5, -0.5), Point(5.5, 5.5)),
            Rectangle(Field(2, 2), Field(4, 4)): Rectangle(Point(1.5, 1.5), Point(4.5, 4.5))
        }

        for case, expected in test_cases.items():
            self.assertEqual(case.corner_shell(),expected)


if __name__ == '__main__':
    unittest.main()
