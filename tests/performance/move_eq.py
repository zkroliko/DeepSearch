import time

from mock.mock import self

from model.field import Field
from model.move import Move
from model.point import Point
from model.view import ViewGenerator
from examples.Scenario1 import Scenario1

start = time.time()

m1 = Move(Field(2, 2), Field(5, 5))
m2 = Move(Field(3, 3), Field(5, 5))

for i in range(0, 1000000):
    m1 == m2

end = time.time() - start

print end
