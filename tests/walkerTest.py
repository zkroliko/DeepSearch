import unittest

from model.agents.agent import Agent
from model.area import Area
from model.decision_makers.random_behaviour import RandomBehaviour
from model.field import Field, FieldType
from model.rectangle import Rectangle


class TestWalker(unittest.TestCase):
    def test_init(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        w = Agent(a, Field(3, 3), decision_maker=RandomBehaviour())
        self.assertNotEqual(w, None)
        self.assertEqual(w.area, a)

    def test_place(self):
        start = Field(3, 3)
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        w = Agent(a, start, RandomBehaviour())
        self.assertTrue(w.position, start)
        bad_start = Field(323233223, 3322332)
        with self.assertRaises(Exception):
            w.position(bad_start)

    def test_can_step(self):
        a = Area(Rectangle(Field(0, 0), Field(15, 15)), 2)
        w = Agent(a, Field(3, 3), RandomBehaviour())
        a += Rectangle(Field(0, 0), Field(5, 2), type=FieldType.inaccessible)
        a += Rectangle(Field(0, 3), Field(2, 7), type=FieldType.inaccessible)
        positions = {
            (2, 4): False,
            (3, 4): True,
            (4, 4): True,
            (2, 3): False,
            (3, 3): True,
            (4, 3): True,
            (2, 2): False,
            (2, 3): False,
            (2, 4): False
        }

        for (x, y), val in positions.items():
            self.assertEqual(w.can_step(Field(x, y)), val)

        w.change_position(Field(4, 4))

        positions = {
            (3, 3): True,
            (4, 5): True,
            (5, 5): True,
            (3, 4): True,
            (4, 4): True,
            (5, 4): True,
            (3, 3): True,
            (3, 4): True,
            (3, 5): True
        }

        for (x, y), val in positions.items():
            self.assertEqual(w.can_step(Field(x, y)), val)

    def test_complete(self):
        a = Area(Rectangle(Field(0, 0), Field(7, 7)), 1)
        rectangles = [
            Rectangle(Field(2, 2), Field(3, 3), type=FieldType.inaccessible),
            Rectangle(Field(2, 5), Field(3, 6), type=FieldType.inaccessible),
            Rectangle(Field(5, 2), Field(6, 3), type=FieldType.inaccessible),
            Rectangle(Field(5, 5), Field(6, 6), type=FieldType.inaccessible)
        ]
        a += rectangles

        pm = RandomBehaviour()
        start = Field(4, 4)
        # Testing
        test_rectangle1 = Rectangle(Field(3, 3), Field(5, 5))
        test_rectangle2 = Rectangle(Field(2, 2), Field(6, 6))
        test_rectangle3 = Rectangle(Field(1, 1), Field(7, 7))

        walker = Agent(a, start, pm)
        walker.step()
        self.assertTrue(walker.position in test_rectangle1)
        walker.step()
        self.assertTrue(walker.position in test_rectangle2)
        walker.step()
        self.assertTrue(walker.position in test_rectangle3)

        # while not walker.finished():
        #     walker.step()
        #     print walker.position
        #     print walker.view.lm.how_many_left()



if __name__ == '__main__':
    unittest.main()
