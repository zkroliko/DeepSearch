import time

from mock.mock import self

from model.field import Field
from model.point import Point
from model.view import ViewGenerator
from examples.Scenario1 import Scenario1

start = time.time()

for i in range(0, 500000):
    Field(3, 3)

end = time.time() - start

print end
